package com.crmeb.model.request.admin;

import lombok.Data;
import javax.validation.constraints.NotBlank;

@Data
public class AdminLoginRequest {
    @NotBlank(message = "Username is required")
    private String username;

    @NotBlank(message = "Password is required")
    private String password;
}
