package com.crmeb.model.request;

import lombok.Data;
import javax.validation.constraints.NotNull;

@Data
public class SetUserLevelRequest {
    @NotNull(message = "Level ID is required")
    private Integer levelId;

    private Boolean isForever = false;

    private Integer validTime;
}
