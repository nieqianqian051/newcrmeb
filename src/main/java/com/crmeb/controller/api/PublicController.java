package com.crmeb.controller.api;

import com.crmeb.common.ApiResult;
import org.springframework.web.bind.annotation.*;

/**
 * Public Controller
 * Maps to original route/api.php public endpoints
 * Handles public access endpoints that don't require authentication
 *
 * Original routes:
 * - GET /api/site_config (获取网站配置)
 * - GET /api/navigation (获取底部导航)
 * - GET /api/search/hot_keyword (热门搜索关键字获取)
 * - GET /api/search/keyword (搜索关键字关联)
 * - GET /api/get_open_adv (首页开屏广告)
 * 
 * @author Devin
 * @since 2024-01-xx
 */
@RestController
@RequestMapping("/api")
public class PublicController {

    @GetMapping("/site_config")
    public ApiResult<?> getSiteConfig() {
        // TODO: Implement site configuration retrieval
        return ApiResult.ok();
    }

    @GetMapping("/navigation/{templateName}")
    public ApiResult<?> getNavigation(@PathVariable(required = false) String templateName) {
        // TODO: Implement navigation retrieval
        return ApiResult.ok();
    }

    @GetMapping("/search/hot_keyword")
    public ApiResult<?> getHotKeywords() {
        // TODO: Implement hot keywords retrieval
        return ApiResult.ok();
    }

    @GetMapping("/search/keyword")
    public ApiResult<?> searchKeywords(@RequestParam String keyword) {
        // TODO: Implement keyword search
        return ApiResult.ok();
    }

    @GetMapping("/get_open_adv")
    public ApiResult<?> getOpenAdv() {
        // TODO: Implement opening advertisement retrieval
        return ApiResult.ok();
    }
}
