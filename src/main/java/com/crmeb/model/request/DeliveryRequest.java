package com.crmeb.model.request;

import lombok.Data;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;

@Data
public class DeliveryRequest {
    @NotNull(message = "Order ID is required")
    private Integer orderId;

    @NotBlank(message = "Delivery company is required")
    private String deliveryCompany;

    @NotBlank(message = "Tracking number is required")
    private String trackingNumber;
}
