package com.crmeb.controller.api;

import com.crmeb.common.ApiResult;
import org.springframework.web.bind.annotation.*;

/**
 * Product Controller
 * Maps to original route/api.php product endpoints
 * Handles product listing, categories, and details
 *
 * Original routes:
 * - GET /api/category (商品分类)
 * - GET /api/products (商品列表)
 * - GET /api/product/detail/:id (商品详情)
 * - GET /api/reply/list/:id (商品评价列表)
 * 
 * @author Devin
 * @since 2024-01-xx
 */
@RestController
@RequestMapping("/api")
public class ProductController {

    @GetMapping("/category")
    public ApiResult<?> getCategories() {
        // TODO: Implement category listing
        return ApiResult.ok();
    }

    @GetMapping("/products")
    public ApiResult<?> getProducts(
            @RequestParam(required = false) String keyword,
            @RequestParam(required = false) Integer categoryId,
            @RequestParam(defaultValue = "1") Integer page,
            @RequestParam(defaultValue = "10") Integer size) {
        // TODO: Implement product listing with pagination
        return ApiResult.ok();
    }

    @GetMapping("/product/detail/{id}")
    public ApiResult<?> getProductDetail(@PathVariable Integer id) {
        // TODO: Implement product detail retrieval
        return ApiResult.ok();
    }

    @GetMapping("/reply/list/{id}")
    public ApiResult<?> getProductReviews(
            @PathVariable Integer id,
            @RequestParam(defaultValue = "1") Integer page,
            @RequestParam(defaultValue = "10") Integer size) {
        // TODO: Implement product reviews listing
        return ApiResult.ok();
    }
}
