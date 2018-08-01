#!/usr/bin/env python3
import atlas_mpl_style as atlas
import numpy as np
import numexpr as ne
import scipy.stats as stats
import scipy.interpolate as interp
from statsmodels.nonparametric.kernel_regression import KernelReg
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from matplotlib.markers import CARETUP
import argparse
import pickle
import ROOT as r
r.PyConfig.IgnoreCommandLineOptions = True

from root_pandas import read_root  # noqa
atlas.use_atlas_style()


class FitFunction:
    def __init__(self, x, y, yerr=None):
        reg = KernelReg([y], [x], var_type='c', reg_type='ll')
        vals = reg.fit(x)[0]
        self.spline = interp.UnivariateSpline(
            x, vals, w=np.isfinite(vals), ext='const')
        # calculate RMS and normalize to stop normalization drifting
        xs = np.linspace(np.min(x), np.max(x), 1000)
        ys = self.spline(xs)
        self.rms = np.sqrt(np.sum(ys**2) / 1000)

    def __repr__(self):
        return f'RMS: {self.rms:.4g}, Spline: {str(self.spline.get_coeffs())}'

    def fit(self, x):
        return self.spline(x) / self.rms


# import root_numpy as rnp
# import rootpy as rpy

parser = argparse.ArgumentParser(
    description="Plot data and background (QCD and MC)", prog='plot.py')
parser.add_argument(
    '--no-kinematic-reweighting',
    dest='no_kinematic_reweighting',
    default=False,
    action='store_true'
)
parser.add_argument(
    '--mc',
    dest='mc',
    action='append',
    nargs=2,
    metavar=('MC_label', 'MC_file'),
    help='MC backgrounds')
parser.add_argument(
    '--norm',
    dest='norm',
    action='store',
    type=float,
    default='0.084',
    help='QCD normalization')

parser.add_argument(
    '-f',
    dest='f',
    action='store',
    type=float,
    default='0.22',
    help='n-jets factor')
parser.add_argument(
    'region',
    choices=['signal', 'control', 'sideband'],
    default='signal',
    help='HH mass region',
    action='store')
parser.add_argument(
    'var',
    choices=[
        'm_hh', 'm_h1', 'pT_h1', 'eta_h1', 'm_h2', 'pT_h2', 'eta_h2', 'njets',
        'pT_4', 'pT_2', 'eta_i', 'dRjj_1', 'dRjj_2'
    ],
    default='m_hh',
    help='Variable to plot',
    action='store')
parser.add_argument(
    'data', action='store', metavar='data_file', help='Data ROOT file')
args = parser.parse_args()
f = args.f
if args.region == 'signal':
    args.region = 'sig'  # match tree name

var_labels = {
    'm_hh': r'$m_{hh}$ [GeV]',
    'm_h1': r'$m^{\textsf{lead}}_{h}$ [GeV]',
    'pT_h1': r'$p_T^{\textsf{lead}}$ [GeV]',
    'eta_h1': r'$\eta^{\textsf{lead}}$ [GeV]',
    'm_h2': r'$m^{\textsf{sublead}}_{h}$ [GeV]',
    'pT_h2': r'$p_T^{\textsf{sublead}}$ [GeV]',
    'eta_h2': r'$\eta^{\textsf{sublead}}$ [GeV]',
    'njets': r'$n_{\textsf{jets}}$',
    'pT_4': r'$p_{T}(h_4)$ [GeV]',
    'pT_2': r'$p_{T}(h_2)$ [GeV]',
    'eta_i': r'$\left< \left| \eta_i \right| \right>$',
    'dRjj_1': r'$\Delta R(j_1, j_2)$',
    'dRjj_2': r'$\Delta R(j_3, j_4)$'
}

# Kinematic reweighting
if args.no_kinematic_reweighting:
    def reweight(df):
        pass
else:
    with open("reweight.pickle", mode='rb') as file:
        all_rwgt_funcs = pickle.load(file)

    def reweight(df):
        sf = np.ones(df.shape[0])
        for rwgt in all_rwgt_funcs:
            for k, v in rwgt.items():
                if k == 'rwgt_pT_4':
                    sel = df[k].values < 80
                    sf[sel] *= v.fit(df[sel][k].values)
                else:
                    sf *= v.fit(df[k].values)
        df['kinematic_sf'] = sf
# End of kinematic reweighting


def nJetsWeight(f, ntag, njets):
    to_pick = 4 - ntag
    pick_from = njets - ntag
    return 1 - stats.binom.cdf(to_pick - 1, n=pick_from, p=f)


def plot_hists(hists, bins, ax=None):
    cumulative = np.zeros_like(hists[0][1])
    cumulative_errs = np.zeros_like(hists[0][1], dtype=np.float64)
    x = np.stack((bins[:-1], bins[1:])).ravel(1)
    if ax is None:
        ax = plt.gca()
    for label, hist, sumw2 in hists:
        y_low = np.stack((cumulative, cumulative)).ravel(1)
        y_high = np.stack((hist, hist)).ravel(1)
        ax.plot(x, y_high, color='k', lw='0.5')
        ax.fill_between(x, y_high, y_low, label=label)
        # ax.bar(x=x, height=hist, width=width, bottom=cumulative, label=label)
        cumulative += hist
        cumulative_errs += sumw2
    cumulative_errs = np.sqrt(cumulative_errs)
    return cumulative, cumulative_errs


def weighted_chisquare(f_obs, f_exp, f_obs_err, f_exp_err):
    "Calculate weighted chi-square using method in arxiv:physics/0605123"
    # selection = np.logical_and(f_obs >= 10, f_exp >= 10)
    selection = True
    w1 = f_obs[selection]
    w2 = f_exp[selection]
    s1 = f_obs_err[selection]  # noqa
    s2 = f_exp_err[selection]  # noqa
    W1 = np.sum(w1)  # noqa
    W2 = np.sum(w2)  # noqa
    X2 = ne.evaluate(
        "sum((W1*w2 - W2*w1)**2 / (W1**2 * s2**2 + W2**2 * s1**2))")
    p = stats.chi2.sf(X2, np.size(w1) - 1)
    return (X2, p)


if args.var in ['njets']:
    var = args.var
elif args.var in [
        'm_hh', 'm_h1', 'pT_h1', 'eta_h1', 'm_h2', 'pT_h2', 'eta_h2'
]:
    var = f'event_{args.var}'
elif args.var in ['pT_4', 'pT_2', 'eta_i', 'dRjj_1', 'dRjj_2']:
    var = f'rwgt_{args.var}'

data, bins = np.histogram(
    read_root(args.data, args.region).query('ntag==4')[var].values,
    bins=(np.arange(3.5, 10.0, step=1) if var == 'njets' else 30))
bin_centers = (bins[1:] + bins[:-1]) / 2

fig, ax, ratio_ax = atlas.ratio_axes()

bkgs = []
mc_2tag = np.zeros_like(data, dtype=np.float64)
mc_2tag_sumw2 = np.zeros_like(data, dtype=np.float64)
if args.mc is None:
    args.mc = []
for mc in args.mc:
    df_4tag = read_root(mc[1], args.region).query('ntag==4')
    hist_4tag, _ = np.histogram(
        df_4tag[var].values, bins=bins, weights=df_4tag['mc_sf'].values)
    hist_4tag_sumw2, _ = np.histogram(
        df_4tag[var].values, bins=bins, weights=(df_4tag['mc_sf'].values**2))
    df_2tag = read_root(mc[1], args.region).query('ntag==2')
    reweight(df_2tag)
    hist_2tag, _ = np.histogram(
        df_2tag[var].values,
        bins=bins,
        weights=(df_2tag['mc_sf'].values * nJetsWeight(
            f, 2, df_2tag['njets'].values) * args.norm
                 * df_2tag['kinematic_sf'].values))
    hist_2tag_sumw2, _ = np.histogram(
        df_2tag[var].values,
        bins=bins,
        weights=(df_2tag['mc_sf'].values * nJetsWeight(
            f, 2, df_2tag['njets'].values) * args.norm
                 * df_2tag['kinematic_sf'].values)**2)

    mc_2tag += hist_2tag
    mc_2tag_sumw2 += hist_2tag_sumw2
    bkgs.append((mc[0], hist_4tag, hist_4tag_sumw2))

qcd_df = read_root(args.data, args.region).query('ntag==2')
reweight(qcd_df)
qcd, _ = np.histogram(
    qcd_df[var].values,
    bins=bins,
    weights=(nJetsWeight(f, 2, qcd_df['njets'].values)
             * args.norm * qcd_df['kinematic_sf'].values))
qcd -= mc_2tag  # Subtract off 2 tag MCs
qcd_sumw2, _ = np.histogram(
    qcd_df[var].values,
    bins=bins,
    weights=(nJetsWeight(f, 2, qcd_df['njets'].values)
             * args.norm * qcd_df['kinematic_sf'].values)**2)
qcd_sumw2 += mc_2tag_sumw2  # Errors add

bkg, bkg_err = plot_hists(bkgs + [('QCD', qcd, qcd_sumw2)], bins, ax=ax)
# bkg_err = np.sqrt((0.1*bkg)**2 + bkg_err**2)
ax.errorbar(bin_centers, data, yerr=np.sqrt(data), fmt='ko', label='Data 16')
x2, p = weighted_chisquare(data, bkg, np.sqrt(data), bkg_err)
bkg_yield = np.sum(bkg)
data_yield = np.sum(data)

handles, labels = ax.get_legend_handles_labels()
ax.legend(reversed(handles), reversed(labels), loc='upper right')

bkg_err /= bkg  # proportional errors
bkg_err = np.stack((bkg_err, bkg_err)).ravel(1)  # double up

ratio_ax.plot([bins[0], bins[-1]], [0, 0], color='black')
ratio_ax.fill_between(
    np.stack((bins[:-1], bins[1:])).ravel(1),
    bkg_err,
    -bkg_err,
    color='black',
    alpha=0.3)
ratio = (data - bkg) / bkg
ratio_ax.errorbar(
    bin_centers, ratio, yerr=(np.sqrt(data) * (ratio / data)), fmt='ko')
out_of_range = np.where(ratio > 1, 1, np.where(ratio < -1, -1, np.NaN))
ratio_ax.plot(bin_centers, out_of_range, marker=CARETUP, color='paper:red')
ratio_ax.set_ylabel(
    r"$\frac{\textsf{Data} - \textsf{Bkg}}{\textsf{Bkg}}$", fontsize=12)
ratio_ax.set_ylim((-1, 1))
ratio_ax.yaxis.set_minor_locator(AutoMinorLocator())
ax.yaxis.set_minor_locator(AutoMinorLocator())
atlas.set_xlabel(var_labels[args.var], ax=ratio_ax)
ax.set_ylim((0, ax.get_ylim()[1]))
atlas.set_ylabel('Events', ax=ax)

region = args.region
if region == 'sig':
    region = 'signal'
region = region.capitalize()

atlas.draw_atlas_label(
    0.3,
    0.97,
    ax=ax,
    status='int',
    energy='13 TeV',
    lumi=24,
    desc=(fr'{region} Region \\ $\chi^2={x2:.3f},\ p={p:.3f}$ \\'
          fr'Bkg. Yield = {bkg_yield:.2f}, \\'
          fr'Data Yield = {data_yield:.5g}'),
    lumi_lt=True)
fig.savefig(f'{args.var}-{region}-f{f}.pdf', transparent=True)
