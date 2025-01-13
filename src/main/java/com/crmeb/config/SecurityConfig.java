package com.crmeb.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.web.SecurityFilterChain;

/**
 * Security Configuration
 * Configures Spring Security for API authentication
 *
 * @author Devin
 * @since 2024-01-xx
 */
@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .csrf().disable()
            .authorizeRequests()
                // Public endpoints
                .antMatchers(
                    "/api/login/**",
                    "/api/register/**",
                    "/api/site_config",
                    "/api/category",
                    "/api/products",
                    "/api/article/**",
                    "/api/wechat/**"
                ).permitAll()
                // Admin endpoints
                .antMatchers("/admin/**").hasRole("ADMIN")
                // Protected endpoints
                .anyRequest().authenticated();
        
        return http.build();
    }
}
