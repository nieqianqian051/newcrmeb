package com.crmeb.controller.api;

import com.crmeb.common.ApiResult;
import org.springframework.web.bind.annotation.*;
import org.springframework.http.ResponseEntity;
import org.springframework.http.MediaType;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

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
@Slf4j
@RestController
@RequestMapping("/api")
@RequiredArgsConstructor
public class PublicController {

    @GetMapping("/get_copyright")
    public ApiResult<?> getCopyright() {
        return ApiResult.ok(new Object() {
            public final String version = "CRMEB PRO v3.1";
            public final String copyright = "© 2014-2024 CRMEB";
            public final String copyrightImage = "/admin/images/copyright.png";
            public final String copyrightContext = "CRMEB";
            public final String companyImage = "/admin/images/company.png";
            public final String companyName = "西安众邦网络科技有限公司";
            public final String companyAddr = "陕西省西安市雁塔区";
            public final String companyPhone = "400-8888888";
            public final String companyEmail = "admin@crmeb.com";
            public final String recordNo = "陕ICP备00000000号";
        });
    }

    @GetMapping("/get_script")
    public ResponseEntity<String> getScript() {
        return ResponseEntity
            .ok()
            .contentType(MediaType.TEXT_PLAIN)
            .body("");
    }

    @GetMapping("/adminapi/copyright")
    public ApiResult<?> adminCopyright() {
        return ApiResult.ok(new Object() {
            public final String version = "CRMEB PRO v3.1";
            public final String copyright = "© 2014-2024 CRMEB";
            public final String companyName = "西安众邦网络科技有限公司";
        });
    }

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
