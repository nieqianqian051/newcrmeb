package com.crmeb.controller.api.request;

import lombok.Data;

import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;

/**
 * Mobile login request DTO
 *
 * @author Devin
 * @since 2024-01-xx
 */
@Data
public class MobileLoginRequest {
    @NotBlank(message = "Phone number cannot be empty")
    @Pattern(regexp = "^1[3-9]\\d{9}$", message = "Invalid phone number format")
    private String phone;

    @NotBlank(message = "Verification code cannot be empty")
    private String code;
}
