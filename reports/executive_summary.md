# Executive Summary — Supply Chain Network Analysis
**Client:** Srugenie Technologies Pvt. Ltd.  
**Prepared by:** Ashmit Goel  
**Engagement type:** Strategic Supply Chain Analytics Consulting

---

## Situation

Srugenie Technologies operates a 6-FC supply chain network serving 12 geographic regions across a subcontinent. Two concerns were raised by leadership:

1. **Transportation costs are growing faster than revenue** — no systematic FC-to-region routing logic in place
2. **Stockouts in some regions coexist with idle capacity in others** — inventory policy is not differentiated by regional demand profile

This engagement analysed 3 years of operational data (2022–2024) across 6 FCs, 12 regions, and 72 FC-region transport routes to answer: *how can we fulfil more products to customers faster, safer, and more cost-effectively?*

---

## Key Findings

### 1. Network Capacity — Balanced, No Immediate Crisis
- All 6 FCs operate between **80.2% and 83.8% utilisation** — within the optimal 65–95% target band
- ANOVA confirms no statistically significant utilisation imbalance (F=0.37, p=0.87)
- **Implication:** Capacity is not the current bottleneck. Focus investment on routing and planning efficiency

### 2. Transportation Routing — Major Cost Saving Available
- Current routing is sub-optimal — regions are not assigned to their nearest (lowest-cost) FC
- **All 12 regions** can reduce per-unit transport cost through re-routing
- Average projected saving: **81.5% per unit** across the network
- This saving requires no new infrastructure — only routing policy changes

### 3. Regional Demand — Three Distinct Profiles Requiring Different Strategies

| Cohort | Regions | Avg Monthly Demand | Demand CV | Recommended Strategy |
|---|---|---|---|---|
| HIGH_DEMAND_STABLE | East, FarNorth, West | ~2,400 units | <0.15 | JIT replenishment, tight ROP |
| MED_DEMAND_GROWING | North, South, Central, NE, NW, SW, MidEast | ~1,300 units | 0.15–0.25 | Capacity pre-positioning, growth monitoring |
| LOW_DEMAND_VOLATILE | MidWest, SE | ~600 units | >0.25 | Safety stock buffers, bi-weekly S&OP review |

Applying a single inventory policy to all 12 regions means: over-stocking in stable regions and under-stocking in volatile ones. Both are costly.

---

## Recommendations

### Priority 1 — Immediate (0–3 months)

**Re-route all regions to lowest-cost FC**
- Action: Update order management routing rules to assign each region to the FC with the lowest transport cost per unit, subject to capacity constraints
- Estimated impact: **81.5% average transport cost reduction per unit** across network
- Effort: Low (routing rule change; no capital investment required)

---

### Priority 2 — Short-term (3–6 months)

**Differentiate inventory policy by regional cohort**
- Action: Deploy region-specific safety stock levels and reorder points for MidWest and SE (LOW_DEMAND_VOLATILE cohort); increase S&OP planning cadence to bi-weekly for these regions
- Estimated impact: 15–20% reduction in stockout risk in volatile regions
- Effort: Medium (requires S&OP process change and replenishment system updates)

---

### Priority 3 — Medium-term (6–12 months)

**Pre-position capacity for growth regions**
- Action: Monitor MED_DEMAND_GROWING cohort (7 regions) for demand acceleration; assess FC capacity expansion or third-party logistics (3PL) partnerships before demand exceeds 90% utilisation at serving FCs
- Estimated impact: Prevent capacity shortfall; maintain ≥95% customer fulfilment rate as demand grows at ~0.5%/month
- Effort: Medium-High (capital planning, 3PL evaluation)

---

## Measurement Framework

| Metric | Baseline | Target (6-month) | Target (12-month) |
|---|---|---|---|
| Avg transport cost/unit | Current | −40% | −81.5% |
| Stockout rate (volatile regions) | Baseline | −10% | −20% |
| FC utilisation (all) | 80–84% | 78–88% | 75–90% |
| Customer fulfilment rate | TBD | ≥93% | ≥95% |

*Baselines to be established from operational ERP data at engagement start.*

---

## Appendix

Full methodology, dataset documentation, SQL schema, and Python pipeline code are available in the project repository.

---

*This document is a deliverable from a data analytics consulting engagement. All data used in analysis is synthetic and generated for modelling purposes.*
