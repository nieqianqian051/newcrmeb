package com.crmeb.controller.admin.request;

import lombok.Data;

import javax.validation.constraints.NotNull;
import javax.validation.constraints.DecimalMin;
import java.math.BigDecimal;

/**
 * Order refund request DTO
 *
 * @author Devin
 * @since 2024-01-xx
 */
@Data
public class RefundRequest {
    @NotNull(message = "Refund amount cannot be null")
    @DecimalMin(value = "0.01", message = "Refund amount must be greater than 0")
    private BigDecimal amount;

    private String reason;
}
