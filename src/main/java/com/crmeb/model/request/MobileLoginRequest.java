package com.crmeb.model.request;

import lombok.Data;
import javax.validation.constraints.NotBlank;

@Data
public class MobileLoginRequest {
    @NotBlank(message = "Mobile number is required")
    private String mobile;

    @NotBlank(message = "Verification code is required")
    private String code;
}
