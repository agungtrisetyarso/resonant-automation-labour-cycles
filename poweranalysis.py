
  python power_analysis.py --table      # reproduce manuscript Table 4
  python power_analysis.py --feasible   # countries needed for 80% power
"""

import argparse
import math

import numpy as np
from scipy import stats

W0 = 0.11578          # US omega_0, rad/yr (Appendix B)
N_YEARS = 75.0        # typical labour-share record length
SEED = 20260716


def rayleigh(n_years: float = N_YEARS) -> float:
    """Minimum resolvable angular-frequency separation."""
    return 2.0 * math.pi / n_years


def simulate_power(cv_delta: float, n_countries: int, sigma_omega: float,
                   n_sim: int = 2000, seed: int = SEED) -> dict:
    """
    Rejection rate for H0: b = 0, simulating panels where the model is TRUE.

    Note what is and is not being asked. omega_hat is generated from
    omega_pred, which makes the model true BY ASSUMPTION -- that is the
    point. We are not testing the model; we are asking whether a design
    could detect a model that is true. The answer is a power estimate,
    and it is the only thing synthetic data can legitimately tell us here.
    """
    rng = np.random.default_rng(seed)
    rejections = 0
    slopes = []
    for _ in range(n_sim):
        omega_pred = rng.normal(W0, W0 * cv_delta, n_countries)
        omega_hat = omega_pred + rng.normal(0, sigma_omega, n_countries)
        res = stats.linregress(omega_pred, omega_hat)
        slopes.append(res.slope)
        if res.pvalue < 0.05:
            rejections += 1
    return {
        "cv_delta": cv_delta,
        "n_countries": n_countries,
        "sigma_omega": sigma_omega,
        "power": rejections / n_sim,
        "mean_slope": float(np.mean(slopes)),
        "n_sim": n_sim,
        "seed": seed,
    }


def resolvability(cv_delta: float, n_countries: int, n_sim: int = 2000,
                  seed: int = SEED) -> float:
    """
    Fraction of simulated panels whose predicted omega_0 spread exceeds the
    Rayleigh limit. If this is near zero, per-country spectral tests are
    uninformative regardless of sample size.
    """
    rng = np.random.default_rng(seed)
    ray = rayleigh()
    hits = 0
    for _ in range(n_sim):
        d = rng.normal(W0, W0 * cv_delta, n_countries)
        if d.max() - d.min() > ray:
            hits += 1
    return hits / n_sim


def countries_for_power(cv_delta: float, sigma_omega: float,
                        target: float = 0.80, cap: int = 300) -> int | None:
    """Smallest panel reaching `target` power, or None if unreachable."""
    for n in range(10, cap + 1, 2):
        if simulate_power(cv_delta, n, sigma_omega, n_sim=600)["power"] >= target:
            return n
    return None


def table() -> None:
    """Reproduce manuscript Table 4."""
    print(f"Rayleigh limit (N={N_YEARS:.0f} yr): {rayleigh():.4f} rad/yr")
    print(f"US omega_0: {W0:.5f} rad/yr")
    print(f"seed={SEED}, n_sim=2000\n")
    print(f"{'CV(delta)':>10} {'n':>4} {'sigma=0.012':>12} {'sigma=0.030':>12}")
    for cv in (0.05, 0.10):
        for n in (15, 22):
            a = simulate_power(cv, n, 0.012)["power"]
            b = simulate_power(cv, n, 0.030)["power"]
            print(f"{cv:9.0%} {n:4d} {a:11.0%} {b:11.0%}")
    print()
    print("Realistic cell: CV=5%, sigma=0.030, n=22 -> see above.")
    print("A design that misses a true effect ~6 times in 7.")


def feasible() -> None:
    """How large a panel would be needed?"""
    print("Countries required for 80% power:\n")
    for sigma in (0.012, 0.020, 0.030):
        n = countries_for_power(0.05, sigma)
        status = f"n >= {n}" if n else "> 300 (infeasible)"
        print(f"  CV(delta)=5%, sigma_omega={sigma:.3f}: {status}")
    print("\n  The OECD contains ~38 countries.\n")
    print("Rayleigh limit by record length:")
    for N in (75, 100, 150, 200, 300):
        print(f"  N={N:3d} yr -> {2 * math.pi / N:.4f} rad/yr")
    print("\n  Longer records do not rescue the design, and harmonised")
    print("  labour-share panels of such length do not exist.")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--table", action="store_true", help="reproduce Table 4")
    ap.add_argument("--feasible", action="store_true", help="required panel size")
    args = ap.parse_args()
    if args.table:
        table()
    elif args.feasible:
        feasible()
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
