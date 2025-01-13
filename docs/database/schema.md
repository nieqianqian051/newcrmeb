# CRMEB Database Schema Documentation

## Development Environment
- Database Type: H2 (in-memory)
- JPA Configuration:
  - hibernate.ddl-auto: update
  - show-sql: true
  - database-platform: org.hibernate.dialect.H2Dialect

## Production Environment
- Database Type: MySQL 8.0+
- Configuration:
  - Prefix: eb_
  - Charset: utf8mb4
  - Host: 127.0.0.1
  - Port: 3306
  - Database: crmeb
  - Username: root (configurable)
  - Password: (configurable)

## Core Table Structures

### User Management
1. eb_user (User Accounts)
   - id: INT(10) AUTO_INCREMENT PRIMARY KEY
   - username: VARCHAR(32)
   - password: VARCHAR(100)
   - real_name: VARCHAR(25)
   - birthday: INT(11)
   - card_id: VARCHAR(20)
   - mark: VARCHAR(255)
   - phone: VARCHAR(15)
   - create_time: TIMESTAMP
   - update_time: TIMESTAMP
   - status: TINYINT(1)
   - is_del: TINYINT(1)

2. eb_wechat_user (WeChat Integration)
   - id: INT(10) AUTO_INCREMENT PRIMARY KEY
   - uid: INT(10) [FK -> eb_user.id]
   - unionid: VARCHAR(30)
   - openid: VARCHAR(30)
   - nickname: VARCHAR(64)
   - headimgurl: VARCHAR(256)
   - create_time: TIMESTAMP
   - update_time: TIMESTAMP

### Order Management
1. eb_store_order (Orders)
   - id: INT(10) AUTO_INCREMENT PRIMARY KEY
   - order_id: VARCHAR(32)
   - uid: INT(10) [FK -> eb_user.id]
   - product_id: INT(10) [FK -> eb_store_product.id]
   - total_num: INT(11)
   - total_price: DECIMAL(8,2)
   - paid: TINYINT(1)
   - pay_time: TIMESTAMP
   - status: TINYINT(1)
   - refund_status: TINYINT(1)
   - create_time: TIMESTAMP
   - update_time: TIMESTAMP
   - is_del: TINYINT(1)

### Product Management
1. eb_store_product (Products)
   - id: INT(10) AUTO_INCREMENT PRIMARY KEY
   - product_name: VARCHAR(128)
   - keyword: VARCHAR(255)
   - bar_code: VARCHAR(15)
   - price: DECIMAL(8,2)
   - cost: DECIMAL(8,2)
   - stock: INT(11)
   - sales: INT(11)
   - is_show: TINYINT(1)
   - is_del: TINYINT(1)
   - create_time: TIMESTAMP
   - update_time: TIMESTAMP

### Marketing & Promotions
1. eb_store_coupon_issue (Coupon Distribution)
   - id: INT(10) AUTO_INCREMENT PRIMARY KEY
   - cname: VARCHAR(64)
   - type: TINYINT(1)
   - status: TINYINT(1)
   - is_del: TINYINT(1)
   - create_time: TIMESTAMP
   - update_time: TIMESTAMP

2. eb_store_bargain (Bargain Activities)
   - id: INT(11) AUTO_INCREMENT PRIMARY KEY
   - product_id: INT(11) [FK -> eb_store_product.id]
   - title: VARCHAR(255)
   - price: DECIMAL(10,2)
   - min_price: DECIMAL(10,2)
   - status: TINYINT(1)
   - is_del: TINYINT(1)

3. eb_store_combination (Group Purchase)
   - id: INT(10) AUTO_INCREMENT PRIMARY KEY
   - product_id: INT(10) [FK -> eb_store_product.id]
   - people: INT(2)
   - price: DECIMAL(10,2)
   - status: TINYINT(1)
   - is_del: TINYINT(1)

### System Administration
1. eb_system_admin (Administrators)
   - id: INT(10) AUTO_INCREMENT PRIMARY KEY
   - account: VARCHAR(32)
   - pwd: VARCHAR(100)
   - real_name: VARCHAR(16)
   - roles: VARCHAR(128)
   - last_ip: VARCHAR(16)
   - status: TINYINT(1)
   - is_del: TINYINT(1)

2. eb_system_role (Roles)
   - id: INT(10) AUTO_INCREMENT PRIMARY KEY
   - role_name: VARCHAR(32)
   - rules: TEXT
   - status: TINYINT(1)
   - is_del: TINYINT(1)

3. eb_system_menus (Menu Items)
   - id: INT(10) AUTO_INCREMENT PRIMARY KEY
   - pid: INT(10)
   - name: VARCHAR(16)
   - icon: VARCHAR(16)
   - url: VARCHAR(128)
   - sort: INT(10)
   - is_show: TINYINT(1)

### User Extensions
1. eb_user_address (Delivery Addresses)
   - id: INT(10) AUTO_INCREMENT PRIMARY KEY
   - uid: INT(10) [FK -> eb_user.id]
   - real_name: VARCHAR(32)
   - phone: VARCHAR(16)
   - province: VARCHAR(64)
   - city: VARCHAR(64)
   - district: VARCHAR(64)
   - detail: VARCHAR(256)
   - is_default: TINYINT(1)

2. eb_user_bill (Transaction Records)
   - id: INT(10) AUTO_INCREMENT PRIMARY KEY
   - uid: INT(10) [FK -> eb_user.id]
   - link_id: VARCHAR(32)
   - pm: TINYINT(1)
   - title: VARCHAR(64)
   - number: DECIMAL(8,2)
   - balance: DECIMAL(8,2)
   - mark: VARCHAR(512)
   - create_time: TIMESTAMP
   - status: TINYINT(1)

3. eb_user_level (User Levels)
   - id: INT(10) AUTO_INCREMENT PRIMARY KEY
   - uid: INT(10) [FK -> eb_user.id]
   - level_id: INT(10)
   - grade: INT(10)
   - valid_time: INT(10)
   - is_forever: TINYINT(1)
   - status: TINYINT(1)

## Common Patterns
1. Primary Keys:
   - Usually named 'id'
   - INT(10/11) AUTO_INCREMENT
   - Always NOT NULL

2. Timestamps:
   - create_time: Creation timestamp
   - update_time: Last modification

3. Status Flags:
   - is_del: Soft delete (TINYINT(1))
   - status: Status (TINYINT(1))
   - is_show: Display control (TINYINT(1))

## Java Implementation Notes
1. Entity Mapping:
   ```java
   @Entity
   @Table(name = "eb_store_order")
   @SQLDelete(sql = "UPDATE eb_store_order SET is_del = 1 WHERE id = ?")
   @Where(clause = "is_del = 0")
   ```

2. Data Type Mapping:
   - TINYINT(1) -> Boolean
   - INT -> Integer
   - DECIMAL -> BigDecimal
   - VARCHAR -> String
   - TEXT -> @Column(columnDefinition = "TEXT")
   - TIMESTAMP -> LocalDateTime

3. Relationships:
   - Use @ManyToOne, @OneToMany appropriately
   - Implement lazy loading by default
   - Consider using @Cache for frequently accessed data
