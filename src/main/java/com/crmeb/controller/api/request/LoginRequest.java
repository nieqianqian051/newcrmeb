package com.crmeb.controller.api.request;

import lombok.Data;

import javax.validation.constraints.NotBlank;

/**
 * Login request DTO
 *
 * @author Devin
 * @since 2024-01-xx
 */
@Data
public class LoginRequest {
    @NotBlank(message = "Username cannot be empty")
    private String username;

    @NotBlank(message = "Password cannot be empty")
    private String password;
}
