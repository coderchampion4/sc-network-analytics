"""
transport_optimizer.py
───────────────────────
Transportation cost optimisation via greedy FC assignment.

Method
──────
  Current routing  : each region assigned to the highest-cost FC
                     (worst-case baseline — simulates unoptimised decisions)
  Optimal routing  : each region assigned to the lowest-cost available FC

Metric: saving_pct = (current_cost − optimal_cost) / current_cost × 100

The Haversine cost matrix from data_generator underpins all calculations.
"""

import pandas as pd


def optimise_transportation_routing(
    transport_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Compare current (suboptimal) routing vs cost-minimised routing per region.

    Parameters
    ----------
    transport_df : pd.DataFrame  FC × Region cost matrix

    Returns
    -------
    pd.DataFrame  Per-region routing comparison with savings
    """
    # ── Current routing: worst FC (highest cost) per region ───────────────────
    current = (
        transport_df
        .sort_values("transport_cost_per_unit", ascending=False)
        .groupby("region")[["fc", "transport_cost_per_unit", "distance_km"]]
        .first()
        .rename(columns={
            "fc"                    : "current_fc",
            "transport_cost_per_unit": "current_cost_per_unit",
            "distance_km"           : "current_distance_km",
        })
        .reset_index()
    )

    # ── Optimal routing: cheapest FC per region ────────────────────────────────
    optimal = (
        transport_df
        .sort_values("transport_cost_per_unit", ascending=True)
        .groupby("region")[["fc", "transport_cost_per_unit", "distance_km"]]
        .first()
        .rename(columns={
            "fc"                    : "optimal_fc",
            "transport_cost_per_unit": "optimal_cost_per_unit",
            "distance_km"           : "optimal_distance_km",
        })
        .reset_index()
    )

    # ── Merge and compute savings ──────────────────────────────────────────────
    result = current.merge(optimal, on="region")
    result["cost_saving_per_unit"] = (
        result["current_cost_per_unit"] - result["optimal_cost_per_unit"]
    ).round(3)
    result["saving_pct"] = (
        result["cost_saving_per_unit"]
        / result["current_cost_per_unit"].replace(0, float("nan"))
        * 100
    ).round(2)
    result["routing_changed"] = (result["current_fc"] != result["optimal_fc"]).astype(int)

    avg_saving    = result["saving_pct"].mean()
    routes_changed= result["routing_changed"].sum()

    print(f"[TRANSPORT]  Avg cost saving per unit: {avg_saving:.1f}% "
          f"| Routes re-assigned: {routes_changed}/{len(result)}")
    return result
