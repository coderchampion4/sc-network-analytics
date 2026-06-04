
-- ============================================================
-- SUPPLY CHAIN NETWORK ANALYTICS SCHEMA
-- ============================================================
CREATE TABLE fc_utilisation (
    month            DATE,
    fc               VARCHAR(10),
    capacity         INTEGER,
    throughput       INTEGER,
    utilisation_pct  DECIMAL(5,2),
    opex_usd         DECIMAL(12,2),
    overcapacity_pct DECIMAL(5,2),
    PRIMARY KEY (month, fc)
);

CREATE TABLE region_demand (
    month      DATE,
    region     VARCHAR(20),
    demand     INTEGER,
    PRIMARY KEY (month, region)
);

CREATE TABLE transport_matrix (
    fc                      VARCHAR(10),
    region                  VARCHAR(20),
    distance_km             DECIMAL(8,1),
    transport_cost_per_unit DECIMAL(8,3),
    PRIMARY KEY (fc, region)
);

-- ============================================================
-- KEY ANALYTICAL QUERIES
-- ============================================================

-- Q1: FC Utilisation vs Target (Gap Analysis)
SELECT fc,
       ROUND(AVG(utilisation_pct),2)   AS avg_utilisation_pct,
       80.0                            AS target_pct,
       ROUND(AVG(utilisation_pct)-80,2)AS gap_vs_target,
       COUNT(CASE WHEN utilisation_pct > 100 THEN 1 END) AS months_overcapacity,
       ROUND(SUM(opex_usd)/1e6, 3)     AS total_opex_usd_millions
FROM fc_utilisation
GROUP BY fc
ORDER BY avg_utilisation_pct DESC;

-- Q2: Network Transportation Cost by FC-Region Pair
SELECT fc,
       region,
       distance_km,
       transport_cost_per_unit,
