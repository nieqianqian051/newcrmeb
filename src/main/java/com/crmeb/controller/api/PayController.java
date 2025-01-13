package com.crmeb.controller.api;

import com.crmeb.common.ApiResult;
import com.crmeb.service.payment.PaymentService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.*;

import java.math.BigDecimal;

/**
 * Payment Controller
 * Maps to original route/api.php payment endpoints
 * Handles payment processing and callbacks
 *
 * Original routes:
 * - ANY /api/pay/notify/:type (支付回调)
 * - GET /api/ali_pay (支付宝复制链接支付)
 * 
 * @author Devin
 * @since 2024-01-xx
 */
@Slf4j
@RestController
@RequestMapping("/api")
@RequiredArgsConstructor
public class PayController {

    private final PaymentService paymentService;

    @PostMapping("/pay/notify/{type}")
    public ApiResult<?> paymentNotify(@PathVariable String type, @RequestBody String notifyData) {
        boolean success = paymentService.handlePaymentNotify(type, notifyData);
        return success ? ApiResult.ok() : ApiResult.fail("Payment notification processing failed");
    }

    @GetMapping("/ali_pay")
    public ApiResult<?> getAlipayUrl(@RequestParam String orderId,
                                    @RequestParam BigDecimal amount,
                                    @RequestParam String subject) {
        try {
            String payUrl = paymentService.createAlipayUrl(orderId, amount, subject);
            return ApiResult.ok(payUrl);
        } catch (Exception e) {
            log.error("Failed to generate Alipay URL", e);
            return ApiResult.fail("Payment URL generation failed");
        }
    }
}
