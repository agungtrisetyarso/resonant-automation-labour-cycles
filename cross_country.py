import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

W0 = 0.11578
N_YEARS = 75.0
SEED = 20260716
RAYLEIGH = 2 * math.pi / N_YEARS


def power(cv_delta, n_countries, sigma_omega, n_sim=2000, seed=SEED):
    rng = np.random.default_rng(seed)
    hits = 0
    for _ in range(n_sim):
        wp = rng.normal(W0, W0 * cv_delta, n_countries)
        wh = wp + rng.normal(0, sigma_omega, n_countries)
        if stats.linregress(wp, wh).pvalue < 0.05:
            hits += 1
    return hits / n_sim


def mean_spread(cv_delta, n_countries, n_sim=2000, seed=SEED):
    rng = np.random.default_rng(seed)
    return float(np.mean([
        np.ptp(rng.normal(W0, W0 * cv_delta, n_countries))
        for _ in range(n_sim)
    ]))


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.4))

# ---- Panel A: resolution ----
cvs = np.linspace(0.01, 0.25, 40)
spreads = [mean_spread(cv, 22) for cv in cvs]

ax1.plot(cvs * 100, spreads, color="#1f4e79", lw=2,
         label=r"Mean predicted $\omega_0$ spread ($n=22$)")
ax1.axhline(RAYLEIGH, color="#c00000", ls="--", lw=2,
            label=fr"Rayleigh limit, $N=75$ yr ({RAYLEIGH:.3f})")
ax1.axvspan(2, 7, color="#2e7d32", alpha=0.12)
ax1.text(4.5, 0.098, "Realistic\nCV($\\hat{\\delta}$)",
         ha="center", va="top", fontsize=9, color="#2e7d32", weight="bold")
ax1.axvline(21.49, color="#7f7f7f", ls=":", lw=1.5)
ax1.text(20.6, 0.012, "CV used in\ndiscarded\nsimulation",
         ha="right", va="bottom", fontsize=8, color="#7f7f7f", style="italic")

ax1.set_xlabel(r"Cross-country dispersion of $\hat{\delta}$, CV (%)")
ax1.set_ylabel(r"Angular frequency (rad yr$^{-1}$)")
ax1.set_title("A. Predicted spread vs spectral resolution", fontsize=11)
ax1.legend(fontsize=8, loc="upper left")
ax1.grid(alpha=0.3)
ax1.set_xlim(0, 25)
ax1.set_ylim(0, 0.118)

# ---- Panel B: power ----
ns = [10, 15, 20, 25, 30, 38, 50, 75, 100, 150, 200]
p_real = [power(0.05, n, 0.030, n_sim=800) for n in ns]
p_opt = [power(0.05, n, 0.012, n_sim=800) for n in ns]

ax2.plot(ns, np.array(p_real) * 100, "o-", color="#c00000", lw=2, ms=5,
         label=r"Realistic: $\sigma_{\hat{\omega}}=0.030$")
ax2.plot(ns, np.array(p_opt) * 100, "s--", color="#1f4e79", lw=1.8, ms=4,
         label=r"Optimistic: $\sigma_{\hat{\omega}}=0.012$")
ax2.axhline(80, color="#2e7d32", ls="--", lw=1.5, label="80% power")
ax2.axvline(38, color="#7f7f7f", ls=":", lw=1.5)
ax2.text(36, 52, "OECD\n($\\approx$38)", fontsize=8, color="#7f7f7f",
         ha="right", va="center")

ax2.set_xlabel("Countries in panel")
ax2.set_ylabel(r"Power to reject $b=0$ (%)")
ax2.set_title(r"B. Power when the model is TRUE (CV$(\hat{\delta})=5\%$)",
              fontsize=11)
ax2.legend(fontsize=8, loc="upper left", framealpha=0.95)
ax2.grid(alpha=0.3)
ax2.set_xscale("log")
ax2.set_xticks([10, 20, 38, 50, 100, 200])
ax2.set_xticklabels(["10", "20", "38", "50", "100", "200"])
ax2.set_ylim(0, 100)

plt.tight_layout()
plt.savefig("f4_power.pdf", dpi=300, bbox_inches="tight")
plt.savefig("f4_power.png", dpi=150, bbox_inches="tight")

print(f"Rayleigh (N=75): {RAYLEIGH:.4f}")
print(f"Spread at CV=5%,  n=22: {mean_spread(0.05, 22):.4f}  "
      f"-> resolvable: {mean_spread(0.05, 22) > RAYLEIGH}")
print(f"Spread at CV=21%, n=22: {mean_spread(0.2149, 22):.4f}  "
      f"-> resolvable: {mean_spread(0.2149, 22) > RAYLEIGH}")
print(f"Power at n=22, realistic: {power(0.05, 22, 0.030):.1%}")
print(f"Power at n=38, realistic: {power(0.05, 38, 0.030):.1%}")
print("Written: f4_power.pdf, f4_power.png")
