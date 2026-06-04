"""
main.py — Supply Chain Network & Operations Analytics
──────────────────────────────────────────────────────
Entry point. Runs the full network analysis pipeline and
generates all outputs including the strategic recommendations.

Usage
─────
    python main.py
"""

import os
import json
import time
import pandas as pd
from config import OUTPUT_DIR
from src import (
    generate_network_dataset,
    capacity_gap_analysis,
    optimise_transportation_routing,
    cohort_analysis,
    generate_recommendations,
)

BANNER = """
╔══════════════════════════════════════════════════════════════════╗
║   SUPPLY CHAIN NETWORK & OPERATIONS ANALYTICS                    ║
║   Strategic Engagement — Srugenie Technologies Pvt. Ltd.         ║
║   Author : Ashmit Goel                                           ║
╚══════════════════════════════════════════════════════════════════╝
"""


def main():
    print(BANNER)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    t0 = time.time()

    # ── Stage 1: Data generation ──────────────────────────────────────────────
    print("▶  Stage 1/5 — Network Data Generation")
    demand_df, fc_df, transport_df = generate_network_dataset()

    # ── Stage 2: Capacity gap analysis ───────────────────────────────────────
    print("\n▶  Stage 2/5 — FC Capacity Utilisation & Gap Analysis")
    fc_summary, anova_result = capacity_gap_analysis(fc_df)

    # ── Stage 3: Transportation optimisation ──────────────────────────────────
    print("\n▶  Stage 3/5 — Transportation Cost Optimisation")
    opt_df = optimise_transportation_routing(transport_df)

    # ── Stage 4: Regional cohort analysis ────────────────────────────────────
    print("\n▶  Stage 4/5 — Regional Demand Cohort Analysis (K-Means)")
    cohort_df = cohort_analysis(demand_df)

    # ── Stage 5: Recommendations ──────────────────────────────────────────────
    print("\n▶  Stage 5/5 — Generating Strategic Recommendations")
    recs_df = generate_recommendations(fc_summary, opt_df, cohort_df, anova_result)

    # ── Export ────────────────────────────────────────────────────────────────
    print("\n▶  Exporting outputs...")
    exports = {
        "fc_capacity_summary.csv"       : fc_summary,
        "transport_optimisation.csv"    : opt_df,
        "transport_cost_matrix.csv"     : transport_df,
        "region_cohorts.csv"            : cohort_df,
        "strategic_recommendations.csv" : recs_df,
    }
    for fname, df in exports.items():
        path = os.path.join(OUTPUT_DIR, fname)
        df.to_csv(path, index=False)
        print(f"  [saved] {fname:42s} ({len(df):,} rows)")

    with open(os.path.join(OUTPUT_DIR, "anova_result.json"), "w") as f:
        json.dump(anova_result, f, indent=2)

    # ── Summary ───────────────────────────────────────────────────────────────
    elapsed = time.time() - t0
    print(f"\n{'─'*65}")
    print("  FC CAPACITY SUMMARY")
    print(f"{'─'*65}")
    print(fc_summary[["fc", "avg_utilisation", "fc_status",
                        "gap_vs_target", "months_overcapacity"]].to_string(index=False))

    print(f"\n{'─'*65}")
    print("  TRANSPORT OPTIMISATION SUMMARY (top 5 regions by saving)")
    print(f"{'─'*65}")
    top5 = opt_df.nlargest(5, "saving_pct")[
        ["region", "current_fc", "optimal_fc", "saving_pct"]
    ]
    print(top5.to_string(index=False))

    print(f"\n  Pipeline completed in {elapsed:.1f}s")
    print(f"{'─'*65}")


if __name__ == "__main__":
    main()
