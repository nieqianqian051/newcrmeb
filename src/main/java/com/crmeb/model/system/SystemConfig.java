package com.crmeb.model.system;

import lombok.Data;
import javax.persistence.*;
import java.time.LocalDateTime;

/**
 * System Configuration entity
 * Maps to eb_system_config table
 * Stores system configuration values
 *
 * @author Devin
 * @since 2024-01-xx
 */
@Data
@Entity
@Table(name = "eb_system_config")
public class SystemConfig {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(name = "menu_name", length = 255)
    private String menuName;

    @Column(length = 255)
    private String value;

    @Column(name = "config_tab_id")
    private Integer configTabId;

    private Integer type;

    private Integer status;

    @Column(name = "create_time")
    private LocalDateTime createTime;

    @Column(name = "update_time")
    private LocalDateTime updateTime;
}
