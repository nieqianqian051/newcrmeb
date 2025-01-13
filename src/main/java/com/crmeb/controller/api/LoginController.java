package com.crmeb.controller.api;

import com.crmeb.common.ApiResult;
import org.springframework.web.bind.annotation.*;

/**
 * Login Controller
 * Maps to original route/api.php login endpoints
 * Handles user authentication and registration
 *
 * Original routes:
 * - POST /api/login (账号密码登录)
 * - POST /api/login/mobile (手机号登录)
 * - POST /api/register (手机号注册)
 * - POST /api/register/verify (验证码发送)
 * - POST /api/register/reset (手机号修改密码)
 * 
 * @author Devin
 * @since 2024-01-xx
 */
@RestController
@RequestMapping("/api")
public class LoginController {

    @PostMapping("/login")
    public ApiResult<?> login(@RequestBody LoginRequest request) {
        // TODO: Implement login logic
        return ApiResult.ok();
    }

    @PostMapping("/login/mobile")
    public ApiResult<?> mobileLogin(@RequestBody MobileLoginRequest request) {
        // TODO: Implement mobile login logic
        return ApiResult.ok();
    }

    @PostMapping("/register")
    public ApiResult<?> register(@RequestBody RegisterRequest request) {
        // TODO: Implement registration logic
        return ApiResult.ok();
    }

    @PostMapping("/register/verify")
    public ApiResult<?> sendVerificationCode(@RequestBody VerifyCodeRequest request) {
        // TODO: Implement verification code sending
        return ApiResult.ok();
    }

    @PostMapping("/register/reset")
    public ApiResult<?> resetPassword(@RequestBody ResetPasswordRequest request) {
        // TODO: Implement password reset
        return ApiResult.ok();
    }
}
