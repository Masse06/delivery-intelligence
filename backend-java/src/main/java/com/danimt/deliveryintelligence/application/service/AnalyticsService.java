package com.danimt.deliveryintelligence.application.service;

import com.danimt.deliveryintelligence.domain.model.ZoneProfitability;
import com.danimt.deliveryintelligence.domain.port.in.GetProfitabilityUseCase;
import com.danimt.deliveryintelligence.domain.port.out.AnalyticsPort;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class AnalyticsService implements GetProfitabilityUseCase {

    private final AnalyticsPort analyticsPort;

    public AnalyticsService(AnalyticsPort analyticsPort) {
        this.analyticsPort = analyticsPort;
    }

    @Override
    public List<ZoneProfitability> execute() {
        return analyticsPort.fetchProfitabilityByZoneAndTime();
    }
}