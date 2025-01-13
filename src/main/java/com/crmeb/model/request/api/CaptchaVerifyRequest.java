package com.crmeb.model.request.api;

import lombok.Data;
import javax.validation.constraints.NotBlank;

@Data
public class CaptchaVerifyRequest {
    @NotBlank(message = "Captcha ID is required")
    private String captchaId;

    @NotBlank(message = "Point position is required")
    private String pointJson;

    @NotBlank(message = "Token is required")
    private String token;
}
