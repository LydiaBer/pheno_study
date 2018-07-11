#!/usr/bin/env python3
import numpy as np
import scipy.stats as stats
import scipy.interpolate as interp
from statsmodels.nonparametric.kernel_regression import KernelReg
import argparse
import pickle
import ROOT as r
r.PyConfig.IgnoreCommandLineOptions = True

from root_pandas import read_root  # noqa
from rootpy.io import root_open  # noqa
from rootpy.plotting import Hist  # noqa
import root_numpy as rnp  # noqa


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


parser = argparse.ArgumentParser(
    description="Produce ROOT input for limit setting",
    prog='makeLimitSettingInput.py')
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
    metavar=('MC_name', 'MC_file'),
    help='MC backgrounds')
parser.add_argument(
    '--sig',
    dest='sig',
    action='append',
    nargs=2,
    metavar=('mass_point', 'signal_MC_file'),
    help='Signal samples')
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
    choices=['3b', '4b'],
    default='4b',
    help='Signal region',
    action='store')
parser.add_argument(
    'data', action='store', metavar='data_file', help='Data ROOT file')
args = parser.parse_args()
f = args.f

if args.region == '3b':
    print("3b signal region unimplemented!")
    exit(1)

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
                    # pT_4 reweighting only applied if < 80 GeV
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


var = 'event_m_hh'

data_df = read_root(args.data, 'sig').query('ntag==4')
data, bins = np.histogram(
    data_df[var].values,
    bins=np.arange(200, 3001, step=50))  # 3001 so 3000 is included

bin_centers = (bins[1:] + bins[:-1]) / 2


mc_bkgs = []
signals = []
mc_2tag = np.zeros_like(data, dtype=np.float64)
mc_2tag_sumw2 = np.zeros_like(data, dtype=np.float64)
if args.mc is None:
    args.mc = []
for mc in args.mc:
    # mc[0] is name, mc[1] is file name
    df_4tag = read_root(mc[1], 'sig').query('ntag==4')
    hist_4tag, _ = np.histogram(
        df_4tag[var].values, bins=bins, weights=df_4tag['mc_sf'].values)
    hist_4tag_sumw2, _ = np.histogram(
        df_4tag[var].values, bins=bins, weights=(df_4tag['mc_sf'].values**2))
    df_2tag = read_root(mc[1], 'sig').query('ntag==2')
    reweight(df_2tag)  # because we subtract after reweighting QCD
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
    mc_bkgs.append((mc[0], hist_4tag, hist_4tag_sumw2))

qcd_df = read_root(args.data, 'sig').query('ntag==2')
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

signals = []
if args.sig is None:
    args.sig = []
for sig in args.sig:
    # sig[0] is mass point, sig[1] is filename
    df = read_root(sig[1], args).query('ntag==4')
    hist, _ = np.histogram(df[var].values, bins=bins,
                           weights=df['mc_sf'].values)
    hist_sumw2, _ = np.histogram(df[var].values, bins=bins,
                                 weights=(df['mc_sf'].values**2))
    signals.append((sig[0], hist, hist_sumw2))

with root_open(f'resolved_{args.region}SR.root',
               'recreate') as out_file:
    for signal in signals:
        mass_point = signal[0]
        signal_hist = signal[1]
        signal_sumw2 = signal[2]
        hist = Hist(bins.size - 1, bins[0], bins[-1],
                    name=f'g_hh_m{mass_point}',
                    title=f'g_hh_m{mass_point}')
        _ = rnp.array2hist(signal_hist, hist, errors=np.sqrt(signal_sumw2))
        hist.Write()

    for mc in mc_bkgs:
        mc_name = mc[0]
        mc_hist = mc[1]
        mc_sumw2 = mc[2]
        hist = Hist(bins.size - 1, bins[0], bins[-1],
                    name=f'{mc_name}_hh',
                    title=f'{mc_name}_hh')
        _ = rnp.array2hist(mc_hist, hist, errors=np.sqrt(mc_sumw2))
        hist.Write()

    qcd_hist = Hist(bins.size - 1, bins[0], bins[-1],
                    name=f'qcd_hh',
                    title=f'qcd_hh')
    _ = rnp.array2hist(qcd, qcd_hist, np.sqrt(qcd_sumw2))
    qcd_hist.Write()

    data_hist = Hist(bins.size - 1, bins[0], bins[-1],
                     name=f'data_hh',
                     title=f'data_hh')
    _ = rnp.array2hist(data, data_hist, np.sqrt(data))
    data_hist.Write()
