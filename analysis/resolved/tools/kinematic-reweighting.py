#!/usr/bin/env python3
import atlas_mpl_style as atlas
import numpy as np
import numexpr as ne
import scipy.stats as stats
import scipy.optimize as opt
import scipy.interpolate as interp
from statsmodels.nonparametric.kernel_regression import KernelReg
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
from root_pandas import read_root
import pickle

plt.style.use('paper')
input_file = "output.root"
ttbar_file = "ttbar.root"  # hadd nonallhad and allhad after reconstruction


class FitFunction:
    def __init__(self, x, y, yerr=None):
        self.orig_x = x
        reg = KernelReg([y], [x], var_type='c', reg_type='ll')
        self.vals = reg.fit(x)[0]
        self.spline = interp.UnivariateSpline(
            x, self.vals, w=np.isfinite(self.vals), ext='const')
        # calculate RMS and normalize to stop normalization drifting
        xs = np.linspace(np.min(x), np.max(x), 1000)
        ys = self.spline(xs)
        self.rms = np.sqrt(np.sum(ys**2) / 1000)
        self.rms = 1

    def __repr__(self):
        return f'RMS: {self.rms:.4g}, Spline: {str(self.spline.get_coeffs())}'

    def fit(self, x):
        return self.spline(x) / self.rms


def weighted_chisquare(f_obs, f_exp, f_obs_err, f_exp_err):
    "Calculate weighted chi-square using method in arXiv:physics/0605123"
    w1 = f_obs
    w2 = f_exp
    s1 = f_obs_err  # noqa
    s2 = f_exp_err  # noqa
    W1 = np.sum(w1)  # noqa
    W2 = np.sum(w2)  # noqa
    X2 = ne.evaluate(
        "sum((W1*w2 - W2*w1)**2 / (W1**2 * s2**2 + W2**2 * s1**2))")
    p = stats.chi2.sf(X2, np.size(w1) - 1)
    return (X2, p)


def nJetsWeight(f, ntag, njets):
    to_pick = 4 - ntag
    pick_from = njets - ntag
    return 1 - stats.binom.cdf(to_pick - 1, n=pick_from, p=f)


def optimal_f(bkg, ttbar_2tag, data, ttbar_4tag,
              other_sf, ttbar_2tag_other_sf):
    # add one to max because closed range
    bins = np.arange(bkg.njets.min() - 0.5, bkg.njets.max() + 1.0, 1)

    def obj(f, extra=False):
        sf = nJetsWeight(f, bkg.ntag, bkg.njets) * other_sf
        ttbar_2tag_sf = (nJetsWeight(f, ttbar_2tag.ntag, ttbar_2tag.njets)
                         * ttbar_2tag_other_sf)

        bkg_hist, _ = np.histogram(bkg.njets, bins=bins, weights=sf)
        bkg_err_hist, _ = np.histogram(
            bkg.njets, bins=bins, weights=sf**2)

        ttbar_2tag_hist, _ = np.histogram(ttbar_2tag.njets, bins=bins,
                                          weights=ttbar_2tag_sf)
        ttbar_2tag_err_hist, _ = np.histogram(
            ttbar_2tag.njets, bins=bins, weights=ttbar_2tag_sf**2)
        bkg_hist -= ttbar_2tag_hist
        # components squared already
        bkg_err_hist = np.sqrt(bkg_err_hist + ttbar_2tag_err_hist)

        data_hist, _ = np.histogram(data.njets, bins=bins)
        data_hist = data_hist.astype('float64')

        ttbar_4tag_hist, _ = np.histogram(ttbar_4tag.njets, bins=bins,
                                          weights=ttbar_4tag.mc_sf)
        ttbar_4tag_err_hist, _ = np.histogram(
            ttbar_4tag.njets, bins=bins, weights=ttbar_4tag.mc_sf**2)

        data_hist -= ttbar_4tag_hist
        data_err_hist = np.sqrt(data_hist + ttbar_4tag_err_hist)

        chi2, p = weighted_chisquare(bkg_hist, data_hist, bkg_err_hist,
                                     data_err_hist)
        
        # So binning doesn't affect normalization
        data_yield = data.shape[0] - ttbar_4tag.mc_sf.sum()
        bkg_yield = np.sum(sf) - np.sum(ttbar_2tag_sf)
        norm = data_yield / bkg_yield
        if extra:
            return chi2, p, norm, data_yield, bkg_yield
        return chi2

    res = opt.minimize_scalar(
        obj, bounds=[0, 1], method='bounded', args=(False))
    chi2, p, norm, data_yield, bkg_yield = obj(res.x, True)
    print(f"Optimal f = {res.x:.5g}, χ² = {chi2:.5g}, p = {p:.5g}, "
          f"normalization = {norm:.5g} ({data_yield:.5g} / {bkg_yield:.5g})")
    return res.x


sdb = read_root(
    input_file,
    'sideband',
    columns=['ntag', 'njets', 'rwgt'])
ttbar_sdb = read_root(
    ttbar_file,
    'sideband',
    columns=['ntag', 'njets', 'rwgt', 'mc_sf'])

bkg = sdb.query('ntag==2').copy()
data = sdb.query('ntag==4').copy()
ttbar_2tag = ttbar_sdb.query('ntag==2').copy()
ttbar_4tag = ttbar_sdb.query('ntag==4').copy()

rwgt_vars = {
    'rwgt_pT_4': r'$p_T(h_4)$ / GeV',
    'rwgt_pT_2': r'$p_T(h_2)$ / GeV',
    'rwgt_eta_i': r'$<|\eta_i|>$',
    'rwgt_dRjj_1': r'$\Delta R( j_1, j_2 )$',
    'rwgt_dRjj_2': r'$\Delta R( j_3, j_4 )$'
}
iter_num = 1
f = 0.22
all_rwgt_funcs = []
sf = np.ones(bkg.shape[0])
ttbar_2tag_sf = ttbar_2tag.mc_sf.values

with PdfPages('Iterations.pdf') as pdf:
    while True:
        plt.figure(figsize=(8.27, 11.69))
        print(f"Iteration {iter_num}")
        if len(all_rwgt_funcs) != 0:
            for k, v in all_rwgt_funcs[-1].items():
                if k == "rwgt_pT_4":
                    sel = bkg[k] < 80
                    ttbar_sel = ttbar_2tag[k] < 80
                    sf[sel] *= v.fit(bkg[sel][k])
                    ttbar_2tag_sf[ttbar_sel] *= v.fit(
                        ttbar_2tag[ttbar_sel][k])
                else:
                    sf *= v.fit(bkg[k])
                    ttbar_2tag_sf *= v.fit(ttbar_2tag[k])
        print("Optimizing f")
        f = optimal_f(bkg, ttbar_2tag, data, ttbar_4tag, sf, ttbar_2tag_sf)
        bkg['sf'] = sf
        ttbar_2tag['sf'] = ttbar_2tag_sf
        rwgt_funcs = {}
        all_done = []
        for i, var in enumerate(rwgt_vars):
            if var == 'rwgt_pT_4':
                bkg_quer = bkg.query('rwgt_pT_4 < 80')
                ttbar_2tag_quer = ttbar_2tag.query('rwgt_pT_4 < 80')
                ttbar_4tag_quer = ttbar_4tag.query('rwgt_pT_4 < 80')
                bkg_ar = bkg_quer[var]
                ttbar_2tag_ar = ttbar_2tag_quer[var]
                data_ar = data.query('rwgt_pT_4 < 80')[var]
                ttbar_4tag_ar = ttbar_4tag_quer[var]
                tag_sf = nJetsWeight(f, bkg_quer.ntag, bkg_quer.njets)
                ttbar_tag_sf = nJetsWeight(f, ttbar_2tag_quer.ntag,
                                           ttbar_2tag_quer.njets)
                other_sf = bkg_quer['sf']
                ttbar_2tag_other_sf = ttbar_2tag_quer['sf']
                ttbar_4tag_mc_sf = ttbar_4tag_quer['mc_sf']
            else:
                bkg_ar = bkg[var]
                ttbar_2tag_ar = ttbar_2tag[var]
                data_ar = data[var]
                ttbar_4tag_ar = ttbar_4tag[var]
                tag_sf = nJetsWeight(f, bkg.ntag, bkg.njets)
                ttbar_tag_sf = nJetsWeight(f, ttbar_2tag.ntag,
                                           ttbar_2tag.njets)
                other_sf = bkg['sf']
                ttbar_2tag_other_sf = ttbar_2tag['sf']
                ttbar_4tag_mc_sf = ttbar_4tag['mc_sf']

            # Because we divide by background
            min_var = data_ar.min()
            max_var = data_ar.max()
            bins = np.linspace(min_var, max_var, 21)
            bin_centers = (bins[1:] + bins[:-1]) / 2

            # hand calculate density to get errors
            bkg_hist, _ = np.histogram(
                bkg_ar, bins=bins, weights=tag_sf * other_sf, density=False)
            ttbar_2tag_hist, _ = np.histogram(
                ttbar_2tag_ar, bins=bins, weights=(
                    ttbar_tag_sf * ttbar_2tag_other_sf),
                density=False)
            bkg_hist -= ttbar_2tag_hist

            ttbar_4tag_hist, _ = np.histogram(
                ttbar_4tag_ar, bins=bins, weights=ttbar_4tag_mc_sf,
                density=False)
            data_hist = (np.histogram(data_ar, bins=bins, density=False)[0]
                         .astype('float64'))
            data_hist -= ttbar_4tag_hist

            bkg_err, _ = np.histogram(
                bkg_ar,
                bins=bins,
                weights=(tag_sf * other_sf)**2,
                density=False)
            ttbar_2tag_err, _ = np.histogram(
                ttbar_2tag_ar,
                bins=bins,
                weights=(ttbar_tag_sf * ttbar_2tag_other_sf)**2,
                density=False)
            # both currently squared
            bkg_err = np.sqrt(bkg_err + ttbar_2tag_err)

            ttbar_4tag_err, _ = np.histogram(
                ttbar_4tag_ar,
                bins=bins,
                weights=(ttbar_4tag_mc_sf)**2,
                density=False)
            # both currently squared
            data_err = np.sqrt(data_hist + ttbar_4tag_err)

            bkg_norm = np.sum(bkg_hist)
            data_norm = np.sum(data_hist)
            bkg_hist = bkg_hist / bkg_norm
            bkg_err = bkg_err / bkg_norm
            data_hist = data_hist / data_norm
            data_err = data_err / data_norm

            ratio = data_hist / bkg_hist
            ratio_err = np.sqrt((data_err / data_hist)**2 +
                                (bkg_err / bkg_hist)**2) * ratio
            rwgt_func = FitFunction(bin_centers, ratio, ratio_err)
            ax = plt.subplot(len(rwgt_vars), 1, i + 1)
            ax.errorbar(bin_centers, ratio, yerr=ratio_err, fmt='o')

            rwgt_funcs[var] = rwgt_func
            x = np.linspace(min_var, max_var, 1000)
            y = rwgt_func.fit(x)
            extreme = np.max(np.abs(y - 1))
            done = extreme < 0.05
            ax.plot(x, y)
            ax.plot(rwgt_func.orig_x, rwgt_func.vals, 'g:')
            for spine in ax.spines.values():
                spine.set_color('paper:green' if done else 'paper:red')
                spine.set_linewidth(2)

            atlas.set_xlabel(
                f"{rwgt_vars[var]} (max. dev.: {extreme:.4f})", ax=ax)
            all_done.append(done)
        all_rwgt_funcs.append(rwgt_funcs)
        plt.tight_layout()
        plt.subplots_adjust(top=0.95)
        plt.suptitle(f"Iteration {iter_num} (f = {f:.3f})", fontsize=15)
        pdf.savefig()
        plt.close()
        iter_num += 1
        if np.all(all_done) or iter_num >= 100:
            print("\nDone. Optimizing f one final time...")
            sf = np.ones(bkg.shape[0])
            ttbar_2tag_sf = ttbar_2tag.mc_sf.values
            if len(all_rwgt_funcs) != 0:
                for rwgt_dict in all_rwgt_funcs:
                    for k, v in rwgt_dict.items():
                        if k == "rwgt_pT_4":
                            sel = bkg[k] < 80
                            ttbar_sel = ttbar_2tag[k] < 80
                            sf[sel] *= v.fit(bkg[sel][k])
                            ttbar_2tag_sf[ttbar_sel] *= v.fit(
                                ttbar_2tag[ttbar_sel][k])
                        else:
                            sf *= v.fit(bkg[k])
                            ttbar_2tag_sf *= v.fit(ttbar_2tag[k])
            f = optimal_f(bkg, ttbar_2tag, data, ttbar_4tag, sf, ttbar_2tag_sf)
            break

with open("reweight.pickle", mode='wb') as file:
    pickle.dump(all_rwgt_funcs, file)
