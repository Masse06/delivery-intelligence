package com.danimt.deliveryintelligence.domain.port.out;

import com.danimt.deliveryintelligence.domain.model.ZoneProfitability;
import java.util.List;

public interface AnalyticsPort {
    List<ZoneProfitability> fetchProfitabilityByZoneAndTime();
}