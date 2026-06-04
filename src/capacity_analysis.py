"""
capacity_analysis.py
────────────────────
FC capacity utilisation gap analysis using ANOVA and variance statistics.

Hypothesis test
───────────────
  H0 : All FCs operate at similar utilisation levels (μ₁ = μ₂ = … = μ₆)
  H1 : At least one FC deviates significantly from target utilisation
  Test: One-way ANOVA on monthly utilisation_pct across FCs
  α = 0.05

FC Status Assignment
────────────────────
  OVERLOADED    — avg utilisation > UTIL_OVERLOADED_PCT (95%)
  OPTIMAL       — 65% ≤ avg utilisation ≤ 95%
  UNDERUTILISED — avg utilisation < UTIL_UNDERUTIL_PCT (65%)
"""

import pandas as pd
from scipy.stats import f_oneway
from config import UTIL_TARGET, UTIL_OVERLOADED_PCT, UTIL_UNDERUTIL_PCT


def capacity_gap_analysis(
    fc_df: pd.DataFrame,
) -> tuple[pd.DataFrame, dict]:
    """
    Compute per-FC utilisation statistics and test for significant differences.

    Parameters
    ----------
    fc_df : pd.DataFrame  Monthly FC utilisation data

    Returns
    -------
    fc_summary  : pd.DataFrame  One row per FC with stats + status
    anova_result: dict          F-stat, p-value, significance flag
    """
    # ── Summary statistics per FC ─────────────────────────────────────────────
    fc_summary = (
        fc_df.groupby("fc")
        .agg(
            avg_utilisation    =("utilisation_pct", "mean"),
            std_utilisation    =("utilisation_pct", "std"),
            max_utilisation    =("utilisation_pct", "max"),
            min_utilisation    =("utilisation_pct", "min"),
            months_overcapacity=("overcapacity_pct", lambda x: (x > 0).sum()),
            total_opex_usd     =("opex_usd",         "sum"),
            avg_throughput     =("throughput",        "mean"),
        )
        .reset_index()
        .round(2)
    )

    fc_summary["gap_vs_target"] = (fc_summary["avg_utilisation"] - UTIL_TARGET).round(2)
    fc_summary["fc_status"] = fc_summary["avg_utilisation"].apply(
        lambda u: "OVERLOADED"     if u > UTIL_OVERLOADED_PCT else
                  "UNDERUTILISED"  if u < UTIL_UNDERUTIL_PCT  else
                  "OPTIMAL"
    )

    # ── ANOVA ─────────────────────────────────────────────────────────────────
    groups = [grp["utilisation_pct"].values for _, grp in fc_df.groupby("fc")]
    f_stat, p_value = f_oneway(*groups)

    anova_result = {
        "f_statistic"     : round(float(f_stat),  4),
        "p_value"         : round(float(p_value), 6),
        "significant"     : bool(p_value < 0.05),
        "overloaded_fcs"  : fc_summary.loc[fc_summary["fc_status"] == "OVERLOADED",  "fc"].tolist(),
        "underutil_fcs"   : fc_summary.loc[fc_summary["fc_status"] == "UNDERUTILISED","fc"].tolist(),
    }

    sig_label = "SIGNIFICANT ✓" if anova_result["significant"] else "not significant"
    print(f"[CAPACITY]  ANOVA F={anova_result['f_statistic']}, "
          f"p={anova_result['p_value']} → {sig_label}")
    print(f"            Overloaded: {anova_result['overloaded_fcs'] or 'None'} "
          f"| Underutilised: {anova_result['underutil_fcs'] or 'None'}")
    return fc_summary, anova_result
