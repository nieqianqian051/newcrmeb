package com.crmeb.controller.admin;

import com.crmeb.common.ApiResult;
import org.springframework.web.bind.annotation.*;

/**
 * Admin Login Controller
 * Maps to original route/admin.php login endpoints
 * Handles administrator authentication
 *
 * Original routes from admin.php:
 * - POST /admin/login (管理员登录)
 * - POST /admin/logout (退出登录)
 * - GET /admin/info (获取管理员信息)
 * 
 * @author Devin
 * @since 2024-01-xx
 */
@RestController
@RequestMapping("/admin")
public class AdminLoginController {

    @PostMapping("/login")
    public ApiResult<?> login(@RequestBody AdminLoginRequest request) {
        // TODO: Implement admin login
        return ApiResult.ok();
    }

    @PostMapping("/logout")
    public ApiResult<?> logout() {
        // TODO: Implement admin logout
        return ApiResult.ok();
    }

    @GetMapping("/info")
    public ApiResult<?> getAdminInfo() {
        // TODO: Implement admin info retrieval
        return ApiResult.ok();
    }
}
