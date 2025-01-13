package com.crmeb.model.request;

import lombok.Data;
import javax.validation.constraints.NotNull;
import java.math.BigDecimal;

@Data
public class RefundRequest {
    @NotNull(message = "Order ID is required")
    private Integer orderId;

    @NotNull(message = "Refund amount is required")
    private BigDecimal amount;

    private String reason;
}
