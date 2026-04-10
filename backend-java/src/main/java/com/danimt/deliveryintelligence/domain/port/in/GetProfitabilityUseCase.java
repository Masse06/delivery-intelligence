package com.danimt.deliveryintelligence.domain.port.in;

import com.danimt.deliveryintelligence.domain.model.ZoneProfitability;
import java.util.List;

public interface GetProfitabilityUseCase {
    List<ZoneProfitability> execute();
}