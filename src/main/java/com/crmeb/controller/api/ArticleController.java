package com.crmeb.controller.api;

import com.crmeb.common.ApiResult;
import org.springframework.web.bind.annotation.*;

/**
 * Article Controller
 * Maps to original route/api.php article endpoints
 * Handles article categories, listing and details
 *
 * Original routes:
 * - GET /api/article/category/list (文章分类列表)
 * - GET /api/article/list/:cid (文章列表)
 * - GET /api/article/details/:id (文章详情)
 * - GET /api/article/hot/list (文章热门)
 * 
 * @author Devin
 * @since 2024-01-xx
 */
@RestController
@RequestMapping("/api/article")
public class ArticleController {

    @GetMapping("/category/list")
    public ApiResult<?> getCategories() {
        // TODO: Implement article category listing
        return ApiResult.ok();
    }

    @GetMapping("/list/{cid}")
    public ApiResult<?> getArticles(
            @PathVariable Integer cid,
            @RequestParam(defaultValue = "1") Integer page,
            @RequestParam(defaultValue = "10") Integer size) {
        // TODO: Implement article listing
        return ApiResult.ok();
    }

    @GetMapping("/details/{id}")
    public ApiResult<?> getArticleDetail(@PathVariable Integer id) {
        // TODO: Implement article detail retrieval
        return ApiResult.ok();
    }

    @GetMapping("/hot/list")
    public ApiResult<?> getHotArticles() {
        // TODO: Implement hot articles listing
        return ApiResult.ok();
    }
}
