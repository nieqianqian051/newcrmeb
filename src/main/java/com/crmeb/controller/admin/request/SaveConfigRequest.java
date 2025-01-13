package com.crmeb.controller.admin.request;

import lombok.Data;

import javax.validation.constraints.NotNull;
import java.util.Map;

/**
 * Save configuration request DTO
 *
 * @author Devin
 * @since 2024-01-xx
 */
@Data
public class SaveConfigRequest {
    @NotNull(message = "Configuration values cannot be null")
    private Map<String, Object> values;
}
