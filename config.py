# =============================================================================
# config.py — Supply Chain Network Analytics configuration
# =============================================================================

import os

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

# ── Dataset ───────────────────────────────────────────────────────────────────
RANDOM_SEED  = 77
START_DATE   = "2022-01-01"
END_DATE     = "2024-12-31"
REGIONS = [
    "North","South","East","West","Central",
    "NE","NW","SE","SW","MidEast","MidWest","FarNorth",
]

# ── Fulfilment Centre configuration ──────────────────────────────────────────
FC_CONFIG = {
    "FC_A": {"capacity":5000, "lat":28.7, "lon":77.1, "opex_per_unit":12.5, "util_target":0.80},
    "FC_B": {"capacity":3500, "lat":19.1, "lon":72.9, "opex_per_unit":10.2, "util_target":0.80},
    "FC_C": {"capacity":4200, "lat":13.0, "lon":80.2, "opex_per_unit":9.8,  "util_target":0.80},
    "FC_D": {"capacity":2800, "lat":22.6, "lon":88.4, "opex_per_unit":11.5, "util_target":0.80},
    "FC_E": {"capacity":3000, "lat":23.0, "lon":72.6, "opex_per_unit":10.8, "util_target":0.80},
    "FC_F": {"capacity":3800, "lat":26.9, "lon":80.9, "opex_per_unit":11.0, "util_target":0.80},
}

# ── Transportation ────────────────────────────────────────────────────────────
TRANSPORT_COST_PER_KM = 0.08   # USD per unit per km

# ── Seasonal multipliers ──────────────────────────────────────────────────────
FC_SEASONAL = {12: 1.2, 6: 0.85, 7: 0.85}
DEMAND_SEASONAL = {12: 1.3, 11: 1.1, 1: 1.1, 6: 0.9, 7: 0.9}

# ── Analysis thresholds ───────────────────────────────────────────────────────
UTIL_TARGET           = 80.0   # % utilisation target
UTIL_OVERLOADED_PCT   = 95.0
UTIL_UNDERUTIL_PCT    = 65.0
N_COHORTS             = 3
TRANSPORT_HIGH_SAVING = 15.0   # % saving threshold for high-priority re-routing
