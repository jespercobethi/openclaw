function T_load = calc_gear_load(theta_m, omega_m, theta_blade, omega_blade, k_g, c_g, i_ratio)
% 计算齿轮传动弹性负载转矩
%   theta_m:     电机转子角度 [rad]
%   omega_m:     电机转子角速度 [rad/s]
%   theta_blade: 叶片角度 [rad]
%   omega_blade: 叶片角速度 [rad/s]
%   k_g:         齿轮啮合刚度 [N·m/rad]
%   c_g:         齿轮啮合阻尼 [N·m·s/rad]
%   i_ratio:     减速比

% 折算到电机侧的叶片角度
theta_blade_ref = theta_blade / i_ratio;
omega_blade_ref = omega_blade / i_ratio;

% 弹性力矩
T_load = k_g * (theta_blade_ref - theta_m) + c_g * (omega_blade_ref - omega_m);
end
