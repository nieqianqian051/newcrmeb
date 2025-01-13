package com.crmeb.model.request;

import lombok.Data;
import javax.validation.constraints.NotBlank;

@Data
public class SaveConfigRequest {
    @NotBlank(message = "Menu name is required")
    private String menuName;

    @NotBlank(message = "Value is required")
    private String value;

    private Integer configTabId;
}
