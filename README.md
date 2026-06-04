# Supply Chain Network & Operations Analytics

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.2-150458?logo=pandas)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.4-F7931E?logo=scikit-learn&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-PostgreSQL-336791?logo=postgresql&logoColor=white)
![PowerBI](https://img.shields.io/badge/Power%20BI-Dashboard-F2C811?logo=powerbi&logoColor=black)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)

> **Strategic consulting engagement — Srugenie Technologies Pvt. Ltd.**  
> Hypothesis-driven supply chain network gap analysis, transportation cost optimisation, and K-Means regional cohort segmentation — synthesised into a prioritised C-suite recommendations framework.

---

## Business Problem

Srugenie Technologies operated a 6-FC supply chain network serving 12 geographic regions. Two strategic concerns drove this engagement:

| Concern | Root Cause Found |
|---|---|
| Transportation costs growing faster than revenue | Regions not routed to nearest (cheapest) FC — 100% of routes sub-optimal |
| Stockouts in some regions, excess stock in others | One-size-fits-all inventory policy ignoring regional demand profiles |

---

## Pipeline Architecture

```
Network Data (6 FCs · 12 Regions · 36 months · 72 transport routes)
        │
        ▼
┌──────────────────────────────────┐
│  DATA GENERATION                 │
│  src/data_generator.py           │
│  FC utilisation (monthly),        │
│  Region demand (seasonal+trend), │
│  Haversine transport cost matrix │
└──────────────┬───────────────────┘
               │
       ┌───────┼────────────────────┐
       ▼       ▼                    ▼
┌────────────┐ ┌──────────────────┐ ┌─────────────────┐
│ CAPACITY   │ │ TRANSPORT        │ │ COHORT          │
│ ANALYSIS   │ │ OPTIMISATION     │ │ ANALYSIS        │
│ capacity_  │ │ transport_       │ │ cohort_         │
│ analysis   │ │ optimizer.py     │ │ analysis.py     │
│            │ │                  │ │                 │
│ ANOVA test │ │ Haversine cost   │ │ K-Means (k=3)  │
│ Gap vs 80% │ │ matrix + greedy  │ │ StandardScaler  │
│ target     │ │ optimisation     │ │ 3 segments      │
└──────┬─────┘ └───────┬──────────┘ └────────┬────────┘
       └───────────────┴────────────────────┘
                               │
                               ▼
                  ┌────────────────────────┐
                  │  RECOMMENDATIONS       │
                  │  recommendations.py    │
                  │  Priority 1/2/3 recs  │
                  │  Finding → Action →   │
                  │  Estimated Impact     │
                  └────────────┬───────────┘
                               │
                          CSVs → Power BI
                          + Executive Summary
```

---

## Key Results

| Analysis | Finding |
|---|---|
| FC Utilisation | All 6 FCs within 80–84% — balanced network |
| Transport Optimisation | **81.5% avg cost saving per unit** via re-routing |
| Routes re-assigned | **12 of 12 regions** benefit from re-routing |
| ANOVA (FC utilisation) | F=0.37, p=0.87 — no significant imbalance |
| Cohort segments | 3 distinct regional demand profiles identified |
| HIGH_DEMAND_STABLE | East, FarNorth, West — JIT replenishment recommended |
| MED_DEMAND_GROWING | 7 regions — capacity investment recommended |
| LOW_DEMAND_VOLATILE | MidWest, SE — safety stock buffers recommended |

---

## Tech Stack

| Layer | Tools |
|---|---|
| Data pipeline | Python, Pandas, NumPy |
| Geospatial cost modelling | Haversine formula (great-circle distance) |
| Statistical testing | SciPy (one-way ANOVA) |
| Clustering | Scikit-learn (KMeans, StandardScaler) |
| Database | PostgreSQL-compatible SQL (window functions, CTEs) |
| Visualisation | Power BI (FC utilisation gauges, network map, cohort charts) |

---

## Project Structure

```
sc-network-analytics/
├── main.py                    # Pipeline entry point
├── config.py                  # FC configs, transport params, constants
├── requirements.txt
├── .gitignore
├── src/
│   ├── __init__.py
│   ├── data_generator.py      # FC utilisation, region demand, transport matrix
│   ├── capacity_analysis.py   # ANOVA-based FC utilisation gap analysis
│   ├── transport_optimizer.py # Haversine cost matrix + greedy re-routing
│   ├── cohort_analysis.py     # K-Means regional segmentation
│   └── recommendations.py    # Prioritised C-suite recommendations
├── sql/
│   ├── schema.sql             # Network analytics database schema
│   └── analytical_queries.sql # 5 queries (gap analysis, YoY, optimisation)
├── reports/
│   └── executive_summary.md  # C-suite deliverable summary
├── outputs/                   # Generated at runtime (gitignored)
│   └── .gitkeep
└── data/
    └── .gitkeep
```

---

## Setup & Usage

```bash
git clone https://github.com/coderchampion4/sc-network-analytics.git
cd sc-network-analytics
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python main.py
```

### Outputs

| File | Description |
|---|---|
| `fc_capacity_summary.csv` | Utilisation, status, OpEx per FC |
| `transport_optimisation.csv` | Current vs optimal routing + savings per region |
| `transport_cost_matrix.csv` | Full 6×12 FC-to-region cost matrix |
| `region_cohorts.csv` | Cluster assignment and demand profile per region |
| `strategic_recommendations.csv` | Prioritised recommendations with impact estimates |

---

## SQL Highlights

**YoY demand growth with rolling average** (window function):

```sql
SELECT region,
       DATE_TRUNC('month', month)  AS period,
       demand,
       AVG(demand) OVER (
           PARTITION BY region
           ORDER BY month
           ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
       )  AS rolling_3m_avg,
       demand / NULLIF(
           LAG(demand, 12) OVER (PARTITION BY region ORDER BY month), 0
       ) - 1  AS yoy_growth
FROM region_demand
ORDER BY region, period;
```

**Network optimisation — transport savings per region**:

```sql
WITH current_routing AS (
    SELECT region,
           MIN(transport_cost_per_unit) AS min_possible_cost,
           MAX(transport_cost_per_unit) AS max_possible_cost
    FROM transport_matrix
    GROUP BY region
)
SELECT t.region,
       t.fc                       AS suboptimal_fc,
       ROUND((t.transport_cost_per_unit - c.min_possible_cost)
             / NULLIF(t.transport_cost_per_unit, 0) * 100, 2) AS saving_pct
FROM transport_matrix t
JOIN current_routing c USING (region)
WHERE t.transport_cost_per_unit = c.max_possible_cost
ORDER BY saving_pct DESC;
```

---

## Reports

See [`reports/executive_summary.md`](reports/executive_summary.md) for the C-suite deliverable — structured as Finding → Recommendation → Estimated Impact for each of the 3 priority recommendations.

---

## Methodology Notes

### Haversine Distance
Used to approximate transport distance between FC and region coordinates. More accurate than Euclidean distance for geographically dispersed networks.
```
d = 2R × arcsin(√(sin²(Δlat/2) + cos(lat₁)·cos(lat₂)·sin²(Δlon/2)))
```

### K-Means Cohort Features
Features standardised with `StandardScaler` before clustering to prevent high-volume regions dominating distance calculations.
```
Features: avg_monthly_demand | demand_CV (σ/μ) | demand_growth_proxy
```

---

## Author

**Ashmit Goel** — B.Tech ECE, Jaypee Institute of Information Technology  
[LinkedIn](https://www.linkedin.com/in/ashmit-goel-8ab850299) · [Email](mailto:ashmitg.044@gmail.com)

---

## License

MIT License
