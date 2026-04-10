package com.danimt.deliveryintelligence.infrastructure.adapter.in.web;

import com.danimt.deliveryintelligence.domain.model.ZoneProfitability;
import com.danimt.deliveryintelligence.domain.port.in.GetProfitabilityUseCase;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/v1/analytics")
@CrossOrigin(origins = "*")
public class AnalyticsController {

    private final GetProfitabilityUseCase getProfitabilityUseCase;

    public AnalyticsController(GetProfitabilityUseCase getProfitabilityUseCase) {
        this.getProfitabilityUseCase = getProfitabilityUseCase;
    }

    @GetMapping("/profitability")
    public ResponseEntity<List<ZoneProfitability>> getProfitabilityInsights() {
        List<ZoneProfitability> insights = getProfitabilityUseCase.execute();
        return ResponseEntity.ok(insights);
    }
}