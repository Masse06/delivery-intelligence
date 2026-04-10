package com.danimt.deliveryintelligence.infrastructure.adapter.out.persistence;

import com.danimt.deliveryintelligence.domain.model.ZoneProfitability;
import com.danimt.deliveryintelligence.domain.port.out.AnalyticsPort;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public class AnalyticsJdbcAdapter implements AnalyticsPort {

    private final JdbcTemplate jdbcTemplate;

    public AnalyticsJdbcAdapter(JdbcTemplate jdbcTemplate) {
        this.jdbcTemplate = jdbcTemplate;
    }

    @Override
    public List<ZoneProfitability> fetchProfitabilityByZoneAndTime() {

        String sql = """
            SELECT 
                dz.zone_id AS zone_alias, 
                dt.time_slot, 
                ROUND(AVG(fo.tip_percentage), 2) AS avg_tip_percentage,
                CAST(COUNT(fo.order_id) AS INTEGER) AS total_orders
            FROM fact_orders fo
            JOIN dim_zones dz ON fo.zone_id = dz.zone_id
            JOIN dim_times dt ON fo.time_id = dt.time_id
            GROUP BY dz.zone_id, dt.time_slot
            HAVING COUNT(fo.order_id) >= 1 
            ORDER BY avg_tip_percentage DESC
            """;

        return jdbcTemplate.query(sql, (rs, rowNum) -> new ZoneProfitability(
            rs.getString("zone_alias"),
            rs.getString("time_slot"),
            rs.getDouble("avg_tip_percentage"),
            rs.getInt("total_orders")
        ));
    }
}