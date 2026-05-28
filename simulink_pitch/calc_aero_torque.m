function T_aero = calc_aero_torque(V_wind, omega_blade, beta_deg, rho, A, R_blade, Cp_fun)
% 计算气动转矩
%   V_wind:     风速 [m/s]
%   omega_blade: 叶片角速度 [rad/s]
%   beta_deg:   桨距角 [deg]
%   rho:        空气密度 [kg/m³]
%   A:          扫风面积 [m²]
%   R_blade:    叶片长度 [m]
%   Cp_fun:     Cp(λ,β) 函数句柄

% 叶尖速比
lambda = omega_blade * R_blade / max(V_wind, 0.1);

% 桨距角转弧度
beta = beta_deg * pi / 180;

% 限制 lambda 范围避免数值问题
lambda = max(lambda, 0.01);

% Cp 值
Cp = Cp_fun(lambda, beta);
Cp = max(min(Cp, 0.593), 0);  % Betz 极限

% 气动功率 -> 转矩
P_aero = 0.5 * rho * A * V_wind^3 * Cp;
T_aero = P_aero / max(omega_blade, 0.01);
end
