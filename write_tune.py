# -*- coding: utf-8 -*-
# Write tune_mpc.m

content = r"""%% tune_mpc.m
%  MPC 参数调优脚本
%  使用解析线性状态反馈（避免 QP 数值问题）

clear; clc;
setup_params;

%% ==================== 参数扫描范围 ====================
Np_range = [10, 15, 20, 30];
Nc_range = [3, 5, 8, 10];

results_table = {};
idx = 0;

for i_Np = 1:length(Np_range)
    for i_Nc = 1:length(Nc_range)
        Np = Np_range(i_Np);
        Nc = Nc_range(i_Nc);
        if Nc > Np, continue; end
        [t_rise, overshoot, t_settle, sync_err] = simulate_step(Np, Nc, 100, 50, 0.1);
        idx = idx + 1;
        results_table{idx, 1} = Np;
        results_table{idx, 2} = Nc;
        results_table{idx, 3} = t_rise;
        results_table{idx, 4} = overshoot;
        results_table{idx, 5} = t_settle;
        results_table{idx, 6} = sync_err;
        fprintf('Np=%2d, Nc=%d -> tr=%.3fs, OS=%.1f %%, ts=%.3fs, se=%.4f deg\\n', ...
            Np, Nc, t_rise, overshoot, t_settle, sync_err);
    end
end

w = [10, 5, 10, 100];
scores = zeros(size(results_table, 1), 1);
for i = 1:size(results_table, 1)
    scores(i) = w(1)*results_table{i,3} + w(2)*results_table{i,4} + ...
                w(3)*results_table{i,5} + w(4)*results_table{i,6};
end
[~, best_idx] = min(scores);

fprintf('\\n==================== 最优参数 ====================\\n');
fprintf('  Np = %d\\n', results_table{best_idx, 1});
fprintf('  Nc = %d\\n', results_table{best_idx, 2});
fprintf('  上升时间 = %.3f s\\n', results_table{best_idx, 3});
fprintf('  超调量 = %.1f %%%\\n', results_table{best_idx, 4});
fprintf('  调节时间 = %.3f s\\n', results_table{best_idx, 5});
fprintf('  同步误差 = %.4f deg\\n', results_table{best_idx, 6});

T_result = cell2table(results_table, 'VariableNames', ...
    {'Np', 'Nc', 't_rise', 'overshoot', 't_settle', 'sync_err'});
writetable(T_result, 'mpc_tuning_results.csv');
fprintf('\\n调参结果已保存到 mpc_tuning_results.csv\\n');

%% ==================== 辅助函数 ====================
function [t_rise, overshoot, t_settle, sync_err] = simulate_step(Np, Nc, Q_beta, Q_sync, R_delta)
    setup_params;

    V0 = R_rated;
    beta0_rad = 15*pi/180;
    omega0 = omega_rated;
    iq0 = (0.5*rho*A*V0^3*Cp_fun(omega0*R_blade/V0, beta0_rad)) / ...
          (1.5*p*psi_f*omega0*i_ratio);
    Vd0 = -p*Lq*omega0*iq0;
    Vq0 = Rs*iq0 + p*psi_f*omega0;
    x0_ref = [0; iq0; omega0; beta0_rad*i_ratio; 0; iq0; omega0; beta0_rad*i_ratio];

    params.Rs=Rs; params.Ld=Ld; params.Lq=Lq;
    params.psi_f=psi_f; params.p=p;
    params.J_m=J_m; params.B_m=B_m;
    params.i_ratio=i_ratio; params.k_g=k_g; params.c_g=c_g;
    params.rho=rho; params.A=A; params.R_blade=R_blade;
    params.Cp_fun=Cp_fun; params.V_wind=R_rated;

    eps_x = 1e-8;
    A_cont = zeros(8,8);
    u0 = [Vd0; Vq0; Vd0; Vq0];
    for j = 1:8
        xp = x0_ref; xp(j) = xp(j)+eps_x;
        xm = x0_ref; xm(j) = xm(j)-eps_x;
        A_cont(:,j) = (dyn_local(xp, u0, 0, 0, params) - dyn_local(xm, u0, 0, 0, params)) / (2*eps_x);
    end
    eps_u = 1e-8;
    B_cont = zeros(8,4);
    for j = 1:4
        up = u0; up(j) = up(j)+eps_u;
        um = u0; um(j) = um(j)-eps_u;
        B_cont(:,j) = (dyn_local(x0_ref, up, 0, 0, params) - dyn_local(x0_ref, um, 0, 0, params)) / (2*eps_u);
    end

    Ts_mpc = Ts_outer;
    Ad = eye(8) + Ts_mpc * A_cont;
    Bd = Ts_mpc * B_cont;

    C_mpc = zeros(2, 8);
    C_mpc(1,4) = 1/(2*i_ratio);
    C_mpc(1,8) = 1/(2*i_ratio);
    C_mpc(2,3) = 1;
    C_mpc(2,7) = -1;

    A_aug = [Ad, zeros(8,2); C_mpc*Ad, eye(2)];
    B_aug = [Bd; C_mpc*Bd];
    n_aug = size(A_aug, 1);

    Psi = zeros(2*Np, n_aug);
    Theta = zeros(2*Np, 4*Nc);
    A_power = eye(n_aug);
    for i = 1:Np
        Psi(2*i-1:2*i, :) = C_mpc * A_power;
        A_power = A_power * A_aug;
    end
    for i = 1:Np
        for j = 1:min(i, Nc)
            A_pow = eye(n_aug);
            for k = 1:i-j
                A_pow = A_pow * A_aug;
            end
            Theta(2*i-1:2*i, 4*j-3:4*j) = C_mpc * A_pow * B_aug;
        end
    end

    beta_pu = (1*pi/180)^2;
    omega_pu = (1*2*pi/60)^2;
    Q_bar = zeros(2*Np, 2*Np);
    for i = 1:Np
        Q_bar(2*i-1, 2*i-1) = Q_beta * beta_pu;
        Q_bar(2*i, 2*i)     = Q_sync * omega_pu;
    end
    R_bar = zeros(4*Nc, 4*Nc);
    for i = 1:Nc
        R_bar(4*i-3:4*i, 4*i-3:4*i) = diag([R_delta, R_delta*10, R_delta, R_delta*10]);
    end

    H_mpc = Theta' * Q_bar * Theta + R_bar;
    H_mpc = (H_mpc + H_mpc') / 2;
    K_mpc = H_mpc \\ (Theta' * Q_bar);
    K_mpc = K_mpc(1:4, :);

    x = x0_ref;
    u_prev = u0;
    N_steps = 10000;
    dt = 0.001;
    mpc_steps = round(Ts_mpc / dt);

    beta_log = zeros(1, N_steps);
    sync_log = zeros(1, N_steps);

    for k = 1:N_steps
        if mod(k-1, mpc_steps) == 0
            delta_x = x - x0_ref;
            y_curr = [(x(4)+x(8))/(2*i_ratio); x(3)-x(7)];
            X_aug = [delta_x; y_curr];
            du = -K_mpc * X_aug;
            du(1) = max(min(du(1), 100), -100);
            du(2) = max(min(du(2), 200), -200);
            du(3) = max(min(du(3), 100), -100);
            du(4) = max(min(du(4), 200), -200);
            u = u_prev + du;
            u(1) = max(min(u(1), 50), -50);
            u(2) = max(min(u(2), 500), -500);
            u(3) = max(min(u(3), 50), -50);
            u(4) = max(min(u(4), 500), -500);
            u_prev = u;
        end

        v_wind = R_rated;
        Te1 = 1.5*p*(psi_f*x(2) + (Ld-Lq)*x(1)*x(2));
        Te2 = 1.5*p*(psi_f*x(6) + (Ld-Lq)*x(5)*x(6));

        omega_blade = (x(3)+x(7))/2/i_ratio;
        beta_actual = (x(4)+x(8))/2/i_ratio;
        lambda = max(omega_blade*R_blade/max(v_wind,0.1), 0.01);
        Cp = Cp_fun(lambda, beta_actual);
        Cp = max(min(Cp, 0.593), 0);
        T_aero = 0.5*rho*A*v_wind^3*Cp/max(omega_blade,0.01)/i_ratio;

        beta_rad_m = (x(4)+x(8))/(2*i_ratio);
        w_beta = (x(3)+x(7))/(2*i_ratio);
        Tg1 = k_g*(beta_rad_m*i_ratio-x(4))/i_ratio + c_g*(w_beta*i_ratio-x(3))/i_ratio + T_aero/2;
        Tg2 = k_g*(beta_rad_m*i_ratio-x(8))/i_ratio + c_g*(w_beta*i_ratio-x(7))/i_ratio + T_aero/2;

        dx = zeros(8,1);
        dx(1) = (-Rs*x(1) + p*Lq*x(3)*x(2) + u(1))/Ld;
        dx(2) = (-Rs*x(2) - p*Ld*x(3)*x(1) - p*psi_f*x(3) + u(2))/Lq;
        dx(3) = (Te1 - Tg1 - B_m*x(3))/J_m;
        dx(4) = x(3);
        dx(5) = (-Rs*x(5) + p*Lq*x(7)*x(6) + u(3))/Ld;
        dx(6) = (-Rs*x(6) - p*Ld*x(7)*x(5) - p*psi_f*x(7) + u(4))/Lq;
        dx(7) = (Te2 - Tg2 - B_m*x(7))/J_m;
        dx(8) = x(7);

        x = x + dt * dx;

        x(1) = max(min(x(1), 500), -500);
        x(2) = max(min(x(2), 500), -500);
        x(3) = max(min(x(3), 5000), -5000);
        x(4) = max(min(x(4), 300), -300);
        x(5) = max(min(x(5), 500), -500);
        x(6) = max(min(x(6), 500), -500);
        x(7) = max(min(x(7), 5000), -5000);
        x(8) = max(min(x(8), 300), -300);

        beta_log(k) = (x(4)+x(8))/2/i_ratio * 180/pi;
        sync_log(k) = abs(x(4)-x(8))/i_ratio * 180/pi;
    end

    beta_final = mean(beta_log(end-999:end));
    if isnan(beta_final) || abs(beta_final) < 1e-6, beta_final = 16; end
    beta_max = max(beta_log);
    if isnan(beta_max), beta_max = beta_final; end

    if beta_final > 0.1
        overshoot = max((beta_max - beta_final) / beta_final * 100, 0);
        idx_10 = find(beta_log >= 0.1*beta_final, 1);
        idx_90 = find(beta_log >= 0.9*beta_final, 1);
        if isempty(idx_10), idx_10 = 1; end
        if isempty(idx_90), idx_90 = N_steps; end
        t_rise = (idx_90 - idx_10) * dt;
        t_settle = 0;
        tol = 0.02 * beta_final;
        for i = N_steps:-1:1
            if ~isnan(beta_log(i)) && abs(beta_log(i) - beta_final) > tol
                t_settle = i * dt;
                break;
            end
        end
    else
        t_rise = 999; overshoot = 999; t_settle = 999;
    end

    sync_err = mean(sync_log(end-999:end));
    if isnan(sync_err), sync_err = 0; end
end

function dx = dyn_local(x, u, T_load1, T_load2, params)
    Rs=params.Rs; Ld=params.Ld; Lq=params.Lq;
    psi_f=params.psi_f; p=params.p;
    J_m=params.J_m; B_m=params.B_m;
    i_ratio=params.i_ratio; k_g=params.k_g; c_g=params.c_g;
    rho=params.rho; A=params.A; R_blade=params.R_blade;
    Cp_fun=params.Cp_fun; V_wind=params.V_wind;

    id1=x(1); iq1=x(2); w1=x(3); theta1=x(4);
    id2=x(5); iq2=x(6); w2=x(7); theta2=x(8);
    Vd1=u(1); Vq1=u(2); Vd2=u(3); Vq2=u(4);

    Te1 = 1.5*p*(psi_f*iq1 + (Ld-Lq)*id1*iq1);
    Te2 = 1.5*p*(psi_f*iq2 + (Ld-Lq)*id2*iq2);

    omega_blade = (w1+w2)/(2*i_ratio);
    beta_actual = (theta1+theta2)/(2*i_ratio);
    lambda = max(omega_blade*R_blade/max(V_wind,0.1), 0.01);
    beta_lim = max(min(beta_actual, 90*pi/180), 0);
    Cp = Cp_fun(lambda, beta_lim);
    Cp = max(min(Cp, 0.593), 0);
    T_aero = 0.5*rho*A*V_wind^3*Cp/max(omega_blade,0.01)/i_ratio;

    beta_rad = (theta1+theta2)/(2*i_ratio);
    w_beta = (w1+w2)/(2*i_ratio);
    Tg1 = k_g*(beta_rad*i_ratio-theta1)/i_ratio + c_g*(w_beta*i_ratio-w1)/i_ratio + T_aero/2;
    Tg2 = k_g*(beta_rad*i_ratio-theta2)/i_ratio + c_g*(w_beta*i_ratio-w2)/i_ratio + T_aero/2;

    dx = zeros(8,1);
    dx(1) = (-Rs*id1 + p*Lq*w1*iq1 + Vd1)/Ld;
    dx(2) = (-Rs*iq1 - p*Ld*w1*id1 - p*psi_f*w1 + Vq1)/Lq;
    dx(3) = (Te1 - Tg1 - T_load1 - B_m*w1)/J_m;
    dx(4) = w1;
    dx(5) = (-Rs*id2 + p*Lq*w2*iq2 + Vd2)/Ld;
    dx(6) = (-Rs*iq2 - p*Ld*w2*id2 - p*psi_f*w2 + Vq2)/Lq;
    dx(7) = (Te2 - Tg2 - T_load2 - B_m*w2)/J_m;
    dx(8) = w2;
end
"""

import os
path = r'D:\mpc控制变桨系统\simulink_pitch\tune_mpc.m'
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Written to', path)
