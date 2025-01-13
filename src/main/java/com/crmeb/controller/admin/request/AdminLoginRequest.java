package com.crmeb.controller.admin.request;

import lombok.Data;

import javax.validation.constraints.NotBlank;

/**
 * Admin login request DTO
 *
 * @author Devin
 * @since 2024-01-xx
 */
@Data
public class AdminLoginRequest {
    @NotBlank(message = "Account cannot be empty")
    private String account;

    @NotBlank(message = "Password cannot be empty")
    private String password;
}
