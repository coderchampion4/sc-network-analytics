       RANK() OVER (PARTITION BY region ORDER BY transport_cost_per_unit) AS cost_rank
FROM transport_matrix
ORDER BY region, cost_rank;

-- Q3: Seasonal Demand Pattern by Region
SELECT DATE_TRUNC('month', month) AS period,
       region,
       demand,
       AVG(demand) OVER (PARTITION BY region
                         ORDER BY month
                         ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS rolling_3m_avg,
       demand / NULLIF(LAG(demand,12) OVER (PARTITION BY region ORDER BY month),0) - 1 AS yoy_growth
FROM region_demand
ORDER BY region, period;

-- Q4: Cohort-based supply chain strategy view
WITH cohort_stats AS (
    SELECT region,
           AVG(demand)    AS avg_demand,
           STDDEV(demand) AS std_demand,
           STDDEV(demand) / NULLIF(AVG(demand),0) AS cv_demand
    FROM region_demand
    GROUP BY region
)
SELECT region,
       ROUND(avg_demand,0) AS avg_monthly_demand,
       ROUND(cv_demand,3)  AS demand_cv,
       CASE WHEN avg_demand > 1500 AND cv_demand < 0.20 THEN 'HIGH_DEMAND_STABLE'
            WHEN avg_demand < 800                        THEN 'LOW_DEMAND_VOLATILE'
            ELSE 'MED_DEMAND_GROWING' END                AS cohort
FROM cohort_stats
ORDER BY avg_demand DESC;

-- Q5: Network Optimisation – potential re-routing savings
WITH current_routing AS (
    SELECT region,
           MIN(transport_cost_per_unit) AS min_possible_cost,
           MAX(transport_cost_per_unit) AS max_possible_cost
    FROM transport_matrix
    GROUP BY region
)
SELECT t.region,
       t.fc                       AS currently_used_fc,
       t.transport_cost_per_unit  AS current_cost,
       c.min_possible_cost        AS optimal_cost,
       ROUND((t.transport_cost_per_unit - c.min_possible_cost) /
             NULLIF(t.transport_cost_per_unit,0)*100,2) AS saving_pct
FROM transport_matrix t
JOIN current_routing c USING (region)
WHERE t.transport_cost_per_unit = c.max_possible_cost
ORDER BY saving_pct DESC;
