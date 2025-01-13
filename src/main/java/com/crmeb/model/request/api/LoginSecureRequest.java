package com.crmeb.model.request.api;

import lombok.Data;
import javax.validation.constraints.NotBlank;

@Data
public class LoginSecureRequest {
    @NotBlank(message = "Account is required")
    private String account;

    @NotBlank(message = "Code is required")
    private String code;
}
