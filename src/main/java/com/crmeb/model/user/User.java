package com.crmeb.model.user;

import lombok.Data;
import org.hibernate.annotations.SQLDelete;
import org.hibernate.annotations.Where;

import javax.persistence.*;
import java.time.LocalDateTime;

/**
 * User entity representing the eb_user table
 * 
 * @author Devin
 * @since 2024-01-xx
 */
@Data
@Entity
@Table(name = "eb_user")
@SQLDelete(sql = "UPDATE eb_user SET is_del = 1 WHERE id = ?")
@Where(clause = "is_del = 0")
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(length = 32)
    private String username;

    @Column(length = 100)
    private String password;

    @Column(name = "real_name", length = 25)
    private String realName;

    private Integer birthday;

    @Column(name = "card_id", length = 20)
    private String cardId;

    @Column(length = 255)
    private String mark;

    @Column(length = 15)
    private String phone;

    @Column(name = "create_time")
    private LocalDateTime createTime;

    @Column(name = "update_time")
    private LocalDateTime updateTime;

    private Boolean status;

    @Column(name = "is_del")
    private Boolean isDel = false;
}
