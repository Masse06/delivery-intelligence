package com.danimt.deliveryintelligence.domain.model;

import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor
public class ZoneProfitability {
    private String zoneAlias;
    private String timeSlot;
    private Double avgTipPercentage;
    private Integer totalOrders;
}