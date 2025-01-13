package com.crmeb.model.request;

import lombok.Data;
import javax.validation.constraints.NotBlank;

@Data
public class ResetPasswordRequest {
    @NotBlank(message = "Mobile number is required")
    private String mobile;

    @NotBlank(message = "New password is required")
    private String password;

    @NotBlank(message = "Verification code is required")
    private String code;
}
