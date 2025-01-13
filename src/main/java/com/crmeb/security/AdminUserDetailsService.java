package com.crmeb.security;

import com.crmeb.model.system.SystemAdmin;
import com.crmeb.repository.system.SystemAdminRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

import java.util.Collections;

/**
 * Admin User Details Service
 * Loads user details for admin users
 *
 * @author Devin
 * @since 2024-01-xx
 */
@Service("adminDetailsService")
@RequiredArgsConstructor
public class AdminUserDetailsService implements UserDetailsService {

    private final SystemAdminRepository adminRepository;

    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        SystemAdmin admin = adminRepository.findByAccount(username)
                .orElseThrow(() -> new UsernameNotFoundException("Admin not found: " + username));

        return new org.springframework.security.core.userdetails.User(
                admin.getAccount(),
                admin.getPwd(),
                admin.getStatus(),
                true,
                true,
                true,
                Collections.singletonList(new SimpleGrantedAuthority("ROLE_ADMIN"))
        );
    }
}
