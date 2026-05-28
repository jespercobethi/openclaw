%% tune_mpc.m
%  MPC 参数调优脚本
%  扫描 Np, Nc, Q_beta, Q_sync, R_delta 参数组合
%  找到最优参数集

clear; clc;
setup_params;

%% ==================== 参数扫描范围 ====================
Np_range = [10, 15, 20, 30];
Nc_range = [3, 5, 8, 10];
Q_beta_range = [50, 100, 200, 500];
Q_sync_range = [20, 50, 100, 200];
R_delta_range = [0.01, 0.05, 0.1, 0.5];

% 固定其他参数，先调 Np 和 Nc
results_table = {};
idx = 0;

for i_Np = 1:length(Np_range)
    for i_Nc = 1:length(Nc_range)
        Np = Np_range(i_Np);
        Nc = Nc_range(i_Nc);

        if Nc > Np, continue; end  % Nc 不能大于 Np

        % 运行简化的阶跃响应仿真
        [t_rise, overshoot, t_settle, sync_err] = simulate_step(Np, Nc, 100, 50, 0.1);

        idx = idx + 1;
        results_table{idx, 1} = Np;
        results_table{idx, 2} = Nc;
        results_table{idx, 3} = t_rise;
        results_table{idx, 4} = overshoot;
        results_table{idx, 5} = t_settle;
        results_table{idx, 6} = sync_err;

        fprintf('Np=%2d, Nc=%d → tr=%.3fs, OS=%.1f%%, ts=%.3fs, se=%.4f°\n', ...
            Np, Nc, t_rise, overshoot, t_settle, sync_err);
    end
end

%% ==================== 找最优参数 ====================
% 综合评分：J = w1*t_rise + w2*overshoot + w3*t_settle + w4*sync_err
w = [10, 5, 10, 100];  % 权重
scores = zeros(size(results_table, 1), 1);
for i = 1:size(results_table, 1)
    scores(i) = w(1)*results_table{i,3} + w(2)*results_table{i,4} + ...
                w(3)*results_table{i,5} + w(4)*results_table{i,6};
end
[~, best_idx] = min(scores);

fprintf('\n==================== 最优参数 ====================\n');
fprintf('  Np = %d\n', results_table{best_idx, 1});
fprintf('  Nc = %d\n', results_table{best_idx, 2});
fprintf('  上升时间 = %.3f s\n', results_table{best_idx, 3});
fprintf('  超调量 = %.1f %%\n', results_table{best_idx, 4});
fprintf('  调节时间 = %.3f s\n', results_table{best_idx, 5});
fprintf('  同步误差 = %.4f °\n', results_table{best_idx, 6});

%% ==================== 保存结果 ====================
T_result = cell2table(results_table, 'VariableNames', ...
    {'Np', 'Nc', 't_rise', 'overshoot', 't_settle', 'sync_err'});
writetable(T_result, 'mpc_tuning_results.csv');
fprintf('\n✅ 调参结果已保存到 mpc_tuning_results.csv\n');

%% ==================== 辅助函数 ====================
function [t_rise, overshoot, t_settle, sync_err] = simulate_step(Np, Nc, Q_beta, Q_sync, R_delta)
    % 简化的阶跃响应仿真
    setup_params;

    % 构建 params 结构体
    params.Rs = Rs; params.Ld = Ld; params.Lq = Lq;
    params.psi_f = psi_f; params.p = p;
    params.J_m = J_m; params.B_m = B_m;
    params.i_ratio = i_ratio; params.k_g = k_g; params.c_g = c_g;
    params.rho = rho; params.A = A; params.R_blade = R_blade;
    params.Cp_fun = Cp_fun;

    % 数值线性化
    V0 = R_rated; beta0_rad = 15*pi/180; omega0 = omega_rated;
    iq0 = (0.5*rho*A*V0^3*Cp_fun(omega0*R_blade/V0, beta0_rad)) / (1.5*p*psi_f*omega0*i_ratio);
    Vd0 = -p*Lq*omega0*iq0;
    Vq0 = Rs*iq0 + p*psi_f*omega0;
    x0_ref = [0; iq0; omega0; 0; 0; iq0; omega0; 0];
    u0 = [Vd0; Vq0; Vd0; Vq0];
    T_load0 = 0;

    % A_cont
    eps_x = 1e-8;
    A_cont = zeros(8,8);
    for j = 1:8
        xp = x0_ref; xp(j) = xp(j)+eps_x;
        xm = x0_ref; xm(j) = xm(j)-eps_x;
        A_cont(:,j) = (dual_motor_dynamics_local(xp,u0,T_load0,T_load0,params) - ...
                        dual_motor_dynamics_local(xm,u0,T_load0,T_load0,params))/(2*eps_x);
    end
    % B_cont
    eps_u = 1e-8;
    B_cont = zeros(8,4);
    for j = 1:4
        up = u0; up(j) = up(j)+eps_u;
        um = u0; um(j) = um(j)-eps_u;
        B_cont(:,j) = (dual_motor_dynamics_local(x0_ref,up,T_load0,T_load0,params) - ...
                        dual_motor_dynamics_local(x0_ref,um,T_load0,T_load0,params))/(2*eps_u);
    end

    % 重新构建 MPC
    Ts_mpc = Ts_outer;
    Ad = eye(8) + Ts_mpc * A_cont;
    Bd = Ts_mpc * B_cont;

    C_mpc = zeros(2, 8);
    C_mpc(1, 4) = 1/(2*i_ratio);
    C_mpc(1, 8) = 1/(2*i_ratio);
    C_mpc(2, 3) = 1;
    C_mpc(2, 7) = -1;

    A_aug = [Ad, zeros(8,2); C_mpc*Ad, eye(2)];
    B_aug = [Bd; C_mpc*Bd];
    C_aug = [zeros(2,8), eye(2)];
    n_aug = size(A_aug, 1);

    % 预测矩阵
    Psi = zeros(2*Np, n_aug);
    Theta = zeros(2*Np, 4*Nc);
    A_power = eye(n_aug);
    for i = 1:Np
        Psi(2*i-1:2*i, :) = C_aug * A_power;
        A_power = A_power * A_aug;
    end
    for i = 1:Np
        for j = 1:min(i, Nc)
            A_pow = eye(n_aug);
            for k = 1:i-j
                A_pow = A_pow * A_aug;
            end
            Theta(2*i-1:2*i, 4*j-3:4*j) = C_aug * A_pow * B_aug;
        end
    end

    Q_bar = zeros(2*Np, 2*Np);
    for i = 1:Np
        Q_bar(2*i-1, 2*i-1) = Q_beta;
        Q_bar(2*i, 2*i) = Q_sync;
    end
    R_bar = zeros(4*Nc, 4*Nc);
    for i = 1:Nc
        R_bar(4*i-3:4*i, 4*i-3:4*i) = diag([R_delta, R_delta*10, R_delta, R_delta*10]);
    end
    H = Theta' * Q_bar * Theta + R_bar;
    H = (H + H') / 2;
    H = H + 1e-6*eye(size(H));  % 正则化

    % 仿真
    x = x0_ref;  % 从工作点开始
    u_prev = [Vd0; Vq0; Vd0; Vq0];
    beta_ref = 15 * pi/180;
    N_steps = 10000;
    dt = 0.001;
    beta_log = zeros(1, N_steps);
    sync_log = zeros(1, N_steps);

    for k = 1:N_steps
        delta_x = x - x0_ref;
        delta_x = max(min(delta_x, 1e4), -1e4);
        C_out = zeros(2, 8);
        C_out(1, 4) = 1/(2*i_ratio);
        C_out(1, 8) = 1/(2*i_ratio);
        C_out(2, 3) = 1;
        C_out(2, 7) = -1;
        y_curr = C_out * x;
        y_curr = max(min(y_curr, 1e4), -1e4);
        X_aug = [delta_x; y_curr];
        if any(isnan(X_aug)) || any(isinf(X_aug))
            X_aug = zeros(size(X_aug));
        end

        R_ref = zeros(2*Np, 1);
        for i = 1:Np
            R_ref(2*i-1) = beta_ref;
            R_ref(2*i) = 0;
        end

        f = Theta' * Q_bar * (Psi * X_aug - R_ref);
        f = max(min(f, 1e6), -1e6);
        lb = repmat([-100; -200; -100; -200], Nc, 1);
        ub = repmat([100; 200; 100; 200], Nc, 1);
        opts = optimoptions('quadprog', 'Display', 'off');
        try
            [dU, ~, ef] = quadprog(H, f, [], [], [], [], lb, ub, [], opts);
            if ef ~= 1, dU = zeros(4*Nc,1); end
        catch
            dU = zeros(4*Nc, 1);
        end
        u = u_prev + dU(1:4);
        u = max(min(u, [50; 500; 50; 500]), [-50; -500; -50; -500]);

        % 状态更新
        Te1 = 1.5*p*(psi_f*x(2) + (Ld-Lq)*x(1)*x(2));
        Te2 = 1.5*p*(psi_f*x(6) + (Ld-Lq)*x(5)*x(6));
        beta_rad_m = (x(4)+x(8))/(2*i_ratio);
        w_beta = (x(3)+x(7))/(2*i_ratio);
        Tg1 = k_g*(beta_rad_m*i_ratio-x(4))/i_ratio + c_g*(w_beta*i_ratio-x(3))/i_ratio;
        Tg2 = k_g*(beta_rad_m*i_ratio-x(8))/i_ratio + c_g*(w_beta*i_ratio-x(7))/i_ratio;

        dx = zeros(8,1);
        dx(1) = (-Rs*x(1) + p*Lq*x(3)*x(2) + u(1)) / Ld;
        dx(2) = (-Rs*x(2) - p*Ld*x(3)*x(1) - p*psi_f*x(3) + u(2)) / Lq;
        dx(3) = (Te1 - Tg1 - B_m*x(3)) / J_m;
        dx(4) = x(3);
        dx(5) = (-Rs*x(5) + p*Lq*x(7)*x(6) + u(3)) / Ld;
        dx(6) = (-Rs*x(6) - p*Ld*x(7)*x(5) - p*psi_f*x(7) + u(4)) / Lq;
        dx(7) = (Te2 - Tg2 - B_m*x(7)) / J_m;
        dx(8) = x(7);

        x = x + dt * dx;
        u_prev = u;

        beta_log(k) = (x(4)+x(8))/2/i_ratio * 180/pi;
        sync_log(k) = abs(x(4)-x(8))/i_ratio * 180/pi;
    end

    % 计算性能指标
    beta_final = mean(beta_log(end-1000:end));
    if abs(beta_final) < 1e-6, beta_final = 15; end
    beta_max = max(beta_log);
    overshoot = max((beta_max - 15)/15*100, 0);

    idx_10 = find(beta_log >= 1.5, 1);
    idx_90 = find(beta_log >= 13.5, 1);
    if isempty(idx_10), idx_10 = 1; end
    if isempty(idx_90), idx_90 = N_steps; end
    t_rise = (idx_90 - idx_10) * dt;

    t_settle = 0;
    for i = N_steps:-1:1
        if abs(beta_log(i) - 15) > 0.3
            t_settle = i * dt;
            break;
        end
    end

    sync_err = mean(sync_log(end-1000:end));
end

function dx = dual_motor_dynamics_local(x, u, T_load1, T_load2, params)
    Rs=params.Rs; Ld=params.Ld; Lq=params.Lq;
    psi_f=params.psi_f; p=params.p;
    J_m=params.J_m; B_m=params.B_m;
    i_ratio=params.i_ratio; k_g=params.k_g; c_g=params.c_g;

    id1=x(1); iq1=x(2); w1=x(3); theta1=x(4);
    id2=x(5); iq2=x(6); w2=x(7); theta2=x(8);
    Vd1=u(1); Vq1=u(2); Vd2=u(3); Vq2=u(4);

    Te1 = 1.5*p*(psi_f*iq1 + (Ld-Lq)*id1*iq1);
    Te2 = 1.5*p*(psi_f*iq2 + (Ld-Lq)*id2*iq2);

    beta_rad = (theta1+theta2)/(2*i_ratio);
    w_beta = (w1+w2)/(2*i_ratio);
    Tg1 = k_g*(beta_rad*i_ratio-theta1)/i_ratio + c_g*(w_beta*i_ratio-w1)/i_ratio;
    Tg2 = k_g*(beta_rad*i_ratio-theta2)/i_ratio + c_g*(w_beta*i_ratio-w2)/i_ratio;

    did1 = (-Rs*id1 + p*Lq*w1*iq1 + Vd1)/Ld;
    diq1 = (-Rs*iq1 - p*Ld*w1*id1 - p*psi_f*w1 + Vq1)/Lq;
    dw1 = (Te1 - Tg1 - T_load1 - B_m*w1)/J_m;
    dtheta1 = w1;
    did2 = (-Rs*id2 + p*Lq*w2*iq2 + Vd2)/Ld;
    diq2 = (-Rs*iq2 - p*Ld*w2*id2 - p*psi_f*w2 + Vq2)/Lq;
    dw2 = (Te2 - Tg2 - T_load2 - B_m*w2)/J_m;
    dtheta2 = w2;

    dx = [did1; diq1; dw1; dtheta1; did2; diq2; dw2; dtheta2];
end
