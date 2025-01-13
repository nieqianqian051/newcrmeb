package com.crmeb.config;

import com.crmeb.security.AdminAuthenticationFilter;
import com.crmeb.security.JwtAuthenticationFilter;
import lombok.RequiredArgsConstructor;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;

/**
 * Security Configuration
 * Configures Spring Security for API authentication
 *
 * @author Devin
 * @since 2024-01-xx
 */
@Configuration
@EnableWebSecurity
@RequiredArgsConstructor
public class SecurityConfig {

    private final JwtAuthenticationFilter jwtAuthenticationFilter;
    private final AdminAuthenticationFilter adminAuthenticationFilter;

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .csrf().disable()
            .cors().and()
            .sessionManagement()
                .sessionCreationPolicy(SessionCreationPolicy.STATELESS)
                .and()
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
                .anyRequest().authenticated()
                .and()
            .addFilterBefore(jwtAuthenticationFilter, UsernamePasswordAuthenticationFilter.class)
            .addFilterBefore(adminAuthenticationFilter, JwtAuthenticationFilter.class);
        
        return http.build();
    }
}
