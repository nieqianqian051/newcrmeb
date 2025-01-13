package com.crmeb.model.request;

import lombok.Data;
import javax.validation.constraints.NotBlank;

@Data
public class VerifyCodeRequest {
    @NotBlank(message = "Mobile number is required")
    private String mobile;

    @NotBlank(message = "Type is required")
    private String type;
}
