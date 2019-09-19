#!/usr/bin/env python3
import matplotlib
import traceback
import inspect

matplotlib.use("cairo")
import numpy as np
import matplotlib.pyplot as plt
import atlas_mpl_style as ampl
from probfit import BinnedLH, HistogramPdf, Extended, AddPdf, Normalized
from parse import search
from glob import iglob
from scipy.stats import norm as gaus
from colorama import Fore, Back, Style
import pickle
import ROOT
import cuts

ROOT.ROOT.EnableImplicitMT()

directory = "/data/atlas/atlasdata/DiHiggsPheno/ntuples/150719/corrected_sf"
signal_glob = "signal/loose_noGenFilt_signal*.root"
bgnd_glob = "background/background.root"
disc = "event.m_hh"
syst = 0.00

bounds = (200.0, 1000.0)
n_bins = 10
weight = (
    "mc_sf * event.h1_j1_BTagWeight * event.h1_j2_BTagWeight"
    "* event.h2_j1_BTagWeight * event.h2_j2_BTagWeight"
)
selection, _ = cuts.configure_cuts("resolved-finalSR")

bins = np.linspace(*bounds, n_bins + 1)
bin_centers = (bins[1:] + bins[:-1]) / 2

plt.style.use("print")
ampl.set_color_cycle("Paper")


def signal_params(filename):
    "Extract signal parameter values from filename"
    yuk = search("TopYuk_{:f}", filename).fixed[0]
    lam = search("SlfCoup_{:f}", filename)
    if lam is None:
        lam = -search("SlfCoup_m{:f}", filename).fixed[0]
    else:
        lam = lam.fixed[0]
    return (yuk, lam)


try:
    signals = {
        signal_params(f): (
            ROOT.RDataFrame("preselection", f)
            .Filter(selection)
            .Define("weight", weight)
            .Define("disc", disc)
            .AsNumpy(columns=["weight", "disc"])
        )
        for f in iglob(f"{directory}/{signal_glob}")
    }

    background = (
        ROOT.RDataFrame("preselection", f"{directory}/{bgnd_glob}")
        .Filter(selection)
        .Define("weight", weight)
        .Define("disc", disc)
        .AsNumpy(columns=["weight", "disc"])
    )
except Exception as e:
    print("EXCEPTION")
    print(e)
    print()
    print(inspect.getargvalues(inspect.trace()[-1][0]))
    exit(3)

print(f"Generating background template...")
bkg_hist, _ = np.histogram(background["disc"], weights=background["weight"], bins=bins)
bkg_template = (HistogramPdf(bkg_hist, bins), np.sum(bkg_hist))

print(f"Generating signal templates...")
signal_templates = {}
for (yuk, lam), tree in signals.items():
    hist, _ = np.histogram(tree["disc"], weights=tree["weight"], bins=bins)
    signal_templates[(yuk, lam)] = (HistogramPdf(hist, bins), np.sum(hist))

print(f"Building asimov data (SM signal + background)...")
nominal = signals[(1.0, 1.0)]
asimov_data = np.concatenate([nominal["disc"], background["disc"]])
asimov_data_weights = np.concatenate([nominal["weight"], background["weight"]])
binned_asimov, _ = np.histogram(asimov_data, weights=asimov_data_weights, bins=bins)
binned_asimov_errors = np.sqrt(binned_asimov + syst * binned_asimov ** 2)


print(f"Running fits...")
results = {}
nominal_template = AddPdf(
    Extended(signal_templates[(1.0, 1.0)][0], extname="s"),
    Extended(bkg_template[0], extname="b"),
)

nominal_lh = BinnedLH(
    nominal_template,
    bin_centers,
    bins=n_bins,
    bound=bounds,
    weights=binned_asimov,
    weighterrors=binned_asimov_errors,
    use_w2=True,
    nint_subdiv=3,
    extended=True,
)
print(f"{Style.RESET_ALL}", end="")
nominal_lh_val = 2 * nominal_lh(signal_templates[(1.0, 1.0)][1], bkg_template[1])
nominal_lh.draw()
nominal_lh = nominal_lh_val
plt.savefig("nominal.pdf")
plt.close()


for (yuk, lam), (pdf, norm) in signal_templates.items():
    bkg_norm = bkg_template[1]
    splusb_template = AddPdf(
        Extended(pdf, extname="s"), Extended(bkg_template[0], extname="b")
    )
    splusb = BinnedLH(
        splusb_template,
        bin_centers,
        bins=n_bins,
        bound=bounds,
        weights=binned_asimov,
        weighterrors=binned_asimov_errors,
        use_w2=True,
        nint_subdiv=3,
        extended=True,
    )
    results[(yuk, lam)] = 2 * splusb(norm, bkg_norm) - nominal_lh

with open("results.pickle", mode="wb") as f:
    pickle.dump(results, f)
