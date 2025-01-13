package com.crmeb.model.request;

import lombok.Data;
import javax.validation.constraints.NotBlank;

@Data
public class BindPhoneRequest {
    @NotBlank(message = "Mobile number is required")
    private String phone;

    @NotBlank(message = "Verification code is required")
    private String code;
}
