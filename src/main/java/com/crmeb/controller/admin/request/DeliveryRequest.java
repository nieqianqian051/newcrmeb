package com.crmeb.controller.admin.request;

import lombok.Data;

import javax.validation.constraints.NotBlank;

/**
 * Order delivery request DTO
 *
 * @author Devin
 * @since 2024-01-xx
 */
@Data
public class DeliveryRequest {
    @NotBlank(message = "Delivery company cannot be empty")
    private String company;

    @NotBlank(message = "Tracking number cannot be empty")
    private String trackingNumber;
}
