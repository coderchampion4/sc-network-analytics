"""
data_generator.py
─────────────────
Generates three synthetic datasets for the SC network analysis:

  1. region_demand   — monthly demand per region (seasonal + trend)
  2. fc_utilisation  — monthly throughput & utilisation per FC
  3. transport_matrix — Haversine-based cost matrix for every FC-Region pair

Haversine model
───────────────
  transport_cost_per_unit = haversine_km(FC, Region) × COST_PER_KM
"""

import numpy as np
import pandas as pd
from config import (
    RANDOM_SEED, START_DATE, END_DATE, REGIONS, FC_CONFIG,
    TRANSPORT_COST_PER_KM, FC_SEASONAL, DEMAND_SEASONAL,
)


def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance between two lat/lon points in kilometres."""
    R = 6371.0
    dlat = np.radians(lat2 - lat1)
    dlon = np.radians(lon2 - lon1)
    a = (np.sin(dlat / 2) ** 2
         + np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.sin(dlon / 2) ** 2)
    return R * 2 * np.arcsin(np.sqrt(a))


def generate_network_dataset() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Generate all three network datasets.

    Returns
    -------
    demand_df    : Monthly demand per region (seasonal + trend + noise)
    fc_df        : Monthly FC throughput, utilisation, and OpEx
    transport_df : Static FC × Region cost matrix (distance + cost per unit)
    """
    np.random.seed(RANDOM_SEED)
    months = pd.date_range(START_DATE, END_DATE, freq="MS")

    # ── Region coordinates (fixed per simulation run) ─────────────────────────
    region_lats = np.random.uniform(10, 35, len(REGIONS))
    region_lons = np.random.uniform(70, 95, len(REGIONS))
    region_base = {r: np.random.randint(500, 3000) for r in REGIONS}

    # ── 1. Region demand ──────────────────────────────────────────────────────
    demand_rows = []
    for month in months:
        seasonal = DEMAND_SEASONAL.get(month.month, 1.0)
        trend    = 1.0 + 0.005 * ((month.year - 2022) * 12 + month.month)
        for i, region in enumerate(REGIONS):
            base   = region_base[region]
            demand = max(0, int(base * seasonal * trend
                                + np.random.normal(0, base * 0.10)))
            demand_rows.append({
                "month"      : month,
                "region"     : region,
                "demand"     : demand,
                "region_lat" : round(region_lats[i], 4),
                "region_lon" : round(region_lons[i], 4),
            })
    demand_df = pd.DataFrame(demand_rows)

    # ── 2. FC utilisation ─────────────────────────────────────────────────────
    fc_rows = []
    for month in months:
        for fc, cfg in FC_CONFIG.items():
            seasonal  = FC_SEASONAL.get(month.month, 1.0)
            trend_add = 0.002 * ((month.year - 2022) * 12 + month.month)
            raw_util  = (cfg["util_target"] + trend_add) * seasonal + np.random.normal(0, 0.05)
            util      = float(np.clip(raw_util, 0.40, 1.15))
            throughput= int(cfg["capacity"] * util)

            fc_rows.append({
                "month"           : month,
                "fc"              : fc,
                "capacity"        : cfg["capacity"],
                "throughput"      : throughput,
                "utilisation_pct" : round(util * 100, 2),
                "opex_usd"        : round(throughput * cfg["opex_per_unit"], 2),
                "overcapacity_pct": round(max(0.0, util - 1.0) * 100, 2),
            })
    fc_df = pd.DataFrame(fc_rows)

    # ── 3. Transport cost matrix ───────────────────────────────────────────────
    transport_rows = []
    for fc, cfg in FC_CONFIG.items():
        for i, region in enumerate(REGIONS):
            dist = _haversine_km(cfg["lat"], cfg["lon"], region_lats[i], region_lons[i])
            transport_rows.append({
                "fc"                    : fc,
                "region"                : region,
                "distance_km"           : round(dist, 1),
                "transport_cost_per_unit": round(dist * TRANSPORT_COST_PER_KM, 3),
            })
    transport_df = pd.DataFrame(transport_rows)

    print(f"[DATA GEN]  Demand: {len(demand_df):,} records "
          f"| FC utilisation: {len(fc_df):,} records "
          f"| Transport matrix: {len(transport_df)} routes "
          f"({len(FC_CONFIG)} FCs × {len(REGIONS)} regions)")
    return demand_df, fc_df, transport_df
