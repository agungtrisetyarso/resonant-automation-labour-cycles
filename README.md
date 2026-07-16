# Resonant Automation Labour Cycles

Code and data for the manuscript submitted to Structural Change and Economic Dynamics

**Title:** A resonant LC model of automation-driven labour-share cycles: an a priori multi-decadal frequency and its spectral validation

**Authors:** Agung Trisetyarso<sup>a,*</sup>, Fithra Faisal Hastiadi<sup>b</sup>, Kridanto Surendro<sup>c</sup>

<sup>a</sup>School of Computer Science, Bina Nusantara University, Jakarta, Indonesia  
<sup>b</sup>Faculty of Economics and Business, Universitas Indonesia, Depok, Indonesia  
<sup>c</sup>School of Electrical Engineering and Informatics, Institut Teknologi Bandung, Bandung, Indonesia  

*Corresponding author: trisetyarso@binus.ac.id

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## Overview

This repository contains all code, notebooks, calibration scripts, and supplementary materials required to fully reproduce the analyses, figures, tables, and results of the associated manuscript submitted to Structural Change and Economic Dynamics.

We map the Acemoglu–Restrepo task-based framework to a classical resonant **LC circuit** (human adaptive capacity as capacitor *C*, automation capital stock as inductor *L*). This yields a damped harmonic-oscillator equation for labour-share dynamics. The undamped natural frequency 

**ω₀ ≈ 0.1158 rad year⁻¹ (≈54.3-year cycle)** 

is predicted **a priori** from parameters calibrated exclusively on independent capital-stock and human-capital data (BLS/BEA and NBER/BLS), with **no fitting** to the labour-share or productivity–pay gap validation series.

Reskilling-driven dissipation is incorporated via a Lindblad master equation purely as an analytic and numerical convenience for integrating the classical damped oscillator; **no quantum-computational advantage is claimed or required** for this low-dimensional model.

## Key Results

- **A priori multi-decadal frequency**: Fixed entirely by independently calibrated *L* ≈ 74.6 year² and *C* ≈ 1.0; reproduces ω₀ exactly.
- **Spectral validation** (Welch PSD + phase-randomized Fourier surrogates, 10 000 realisations):
  - U.S. labour share of income (FRED, 1950–2023): power at 54.3 years reaches 95.1st percentile (**p = 0.0490**)
  - EPI Productivity–Pay Gap (1948–2025): reaches 99.76th percentile (**p = 0.0024**)
- Robust to alternative detrending (HP filter λ=1600), IAAFT surrogates, varying Welch window/overlap parameters, block-bootstrap, and disjoint sub-samples (1950–1990 & 1990–2025).
- **Out-of-sample forecasting** (model calibrated only on data up to 2017):
  - 2018–2025 hold-out RMSE = **72.36** (lowest among all compared models)
  - Outperforms linear trend (4911), ETS (3124), Hodrick–Prescott (2789), ARIMA(1,1,0) (1847), and all ablation variants.
- **Policy lever**: Counterfactual increase in reskilling intensity (R → 2R) attenuates future oscillation amplitude.
- Compact two-mode operator representation of the coupled labour–capital dynamics, integrated as an open quantum system (Lindblad) for convenience.

## Repository Structure

```
resonant-automation-labour-cycles/
├── README.md
├── LICENSE
├── requirements.txt
├── calibration/
│   ├── calibration_scripts.py          # L, C, g derivation from raw BLS/BEA & NBER data
│   └── g_derivation.ipynb
├── notebooks/
│   ├── spectral_robustness.ipynb       # Welch PSD, surrogate tests, all robustness checks (Fig. 1)
│   ├── forecasting.ipynb               # Out-of-sample forecast, baselines, ablations, policy counterfactuals (Fig. 2, Table 1)
│   └── open_system_integration.ipynb   # QuTiP Lindblad master-equation integration & Monte Carlo trajectories
├── scripts/
│   ├── psd_welch_surrogates.py
│   ├── model_damped_oscillator.py
│   └── generate_figures.py
├── data/                               # Public data fetch scripts or cached series (FRED, EPI, BLS/BEA, NBER)
└── figures/                            # Reproducible output figures (PNG/PDF)
```

## Getting Started

### 1. Clone and install dependencies

```bash
git clone https://github.com/agungtrisetyarso/resonant-automation-labour-cycles.git
cd resonant-automation-labour-cycles
pip install -r requirements.txt
```

Core dependencies include:
- **QuTiP** (≥4.7) — for Lindblad master equation integration (`mesolve`, Monte Carlo trajectories)
- numpy, scipy, pandas, matplotlib, seaborn
- statsmodels (or equivalent) for spectral analysis
- jupyter, ipywidgets (for notebooks)

### 2. Reproduce the main results

**Calibration (independent parameters only)**  
```bash
python calibration/calibration_scripts.py
# or
jupyter notebook calibration/g_derivation.ipynb
```

**Spectral analysis & significance testing** (reproduces Figure 1 and all robustness checks)
```bash
jupyter notebook notebooks/spectral_robustness.ipynb
```

**Forecasting, ablations, and policy counterfactuals** (reproduces Figure 2, Table 1)
```bash
jupyter notebook notebooks/forecasting.ipynb
```

**Open-system (Lindblad) integration**
```bash
jupyter notebook notebooks/open_system_integration.ipynb
```

All random seeds, surrogate generation, and numerical tolerances are fixed in the notebooks/scripts for exact reproducibility.

## Data Sources & Access

All data are **publicly available**; no proprietary or restricted datasets are used.

| Series | Source | Period | Access |
|--------|--------|--------|--------|
| Labour share of income | FRED `LABSHPUSA156NRUG` | 1950–2023 | https://fred.stlouisfed.org/ |
| EPI Productivity–Pay Gap | Economic Policy Institute | 1948–2025 | https://www.epi.org/ |
| Automation capital stock (L) | BLS/BEA — real private fixed assets (information-processing equipment & software) | 1950–2017 | https://www.bea.gov/ |
| Human adaptive capacity (C) | NBER + BLS occupational training & skill-biased technical change | — | NBER data portal / BLS |

Exact series URLs, vintages, and access dates (27 April 2026 for FRED) are documented in the manuscript (Section 2.2 and Supplementary Note 1).

## Citation

When using this code or data, please cite the forthcoming paper:

> Trisetyarso, A., Hastiadi, F. F., & Surendro, K. (2026). A resonant LC model of automation-driven labour-share cycles: an a priori multi-decadal frequency and its spectral validation. *Physica A* (submitted).

A preprint citation / DOI will be added here upon posting or acceptance.

## Licence

This repository is released under the **MIT License** (see `LICENSE`).

## Contact

**Agung Trisetyarso** (corresponding author)  
School of Computer Science, Bina Nusantara University  
Jakarta, Indonesia  
trisetyarso@binus.ac.id

## Acknowledgements

We gratefully acknowledge the maintainers of the Federal Reserve Economic Data (FRED), Economic Policy Institute (EPI), U.S. Bureau of Labor Statistics (BLS), Bureau of Economic Analysis (BEA), and National Bureau of Economic Research (NBER) for providing open access to the macroeconomic series used in this study.

Numerical integration of the open-system dynamics was performed with [QuTiP](https://qutip.org/). All other analyses used the standard scientific Python ecosystem.

---

*This README is written to be fully consistent with the submitted manuscript. The Lindblad formulation is used strictly as a classical integrator; the work is entirely classical econophysics and makes no claim of quantum computational advantage.*
