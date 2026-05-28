%% run_comparison.m
%  三种控制器对比仿真：MPC vs PID vs ADRC
%  运行前先运行 setup_params.m
%
%  仿真工况：
%    1. 阶跃响应（β_ref: 0→15° at t=30s）
%    2. 阵风扰动（ΔV=3m/s at t=50s）
%    3. 连续湍流风
%
%  输出：时间序列数据 + 对比图 + 性能指标表

clear; clc; close all;

%% ==================== 加载参数 ====================
setup_params;
mpc_controller;

%% ==================== 工况设置 ====================
T_sim = 100;           % 仿真时长
dt_record = 0.01;      % 记录步长 (10ms)
t_vec = 0:dt_record:T_sim;
N_steps = length(t_vec);

% 风速序列
V_wind = R_rated * ones(1, N_steps);
% 阵风扰动 (t=50~60s)
for i = 1:N_steps
    t = t_vec(i);
    if t >= 50 && t < 55
        V_wind(i) = R_rated + V_ramp * (t-50)/5;
    elseif t >= 55 && t < 60
        V_wind(i) = R_rated + V_ramp * (1-(t-55)/5);
    end
end

% 桨距角参考
beta_ref_sim = zeros(1, N_steps);
for i = 1:N_steps
    t = t_vec(i);
    if t >= 30
        beta_ref_sim(i) = 15;  % 15° 阶跃
    end
end

%% ==================== 开环仿真（三种控制器分别运行） ====================
%  使用简化的 ODE 仿真（不依赖 Simulink）

% 控制器列表
controllers = {'MPC', 'PID', 'ADRC'};
n_ctrl = length(controllers);

% 存储结果
results = struct();
for c = 1:n_ctrl
    results(c).name = controllers{c};
    results(c).t = t_vec;
    results(c).x = zeros(8, N_steps);  % 状态
    results(c).u = zeros(4, N_steps);  % 控制量
    results(c).beta = zeros(1, N_steps);  % 桨距角
    results(c).Te = zeros(2, N_steps);    % 电磁转矩
    results(c).sync_err = zeros(1, N_steps);  % 同步误差
    results(c).V_wind = V_wind;
    results(c).beta_ref = beta_ref_sim;
end

%% ==================== MPC 离线数据准备 ====================
% 预计算 MPC 预测矩阵（已在 mpc_controller.m 中完成）

%% ==================== 仿真循环 ====================
for c = 1:n_ctrl
    fprintf('正在仿真 %s 控制器...\n', controllers{c});

    % 初始状态
    x = zeros(8, 1);
    u_prev = [Vd0; Vq0; Vd0; Vq0];

    for k = 1:N_steps
        t = t_vec(k);
        v_wind = V_wind(k);
        beta_ref = beta_ref_sim(k);

        % ============ 计算控制量 ============
        switch controllers{c}
            case 'MPC'
                % MPC 控制
                delta_x = x - x0;
                delta_x = max(min(delta_x, 1e4), -1e4);  % 数值保护

                % 当前输出
                C_out = zeros(2, 8);
                C_out(1, 4) = 1/(2*i_ratio);
                C_out(1, 8) = 1/(2*i_ratio);
                C_out(2, 3) = 1;
                C_out(2, 7) = -1;
                y_curr = C_out * x;
                y_curr = max(min(y_curr, 1e4), -1e4);  % 数值保护

                X_aug = [delta_x; y_curr];

                % 检查 NaN/Inf
                if any(isnan(X_aug)) || any(isinf(X_aug))
                    X_aug = zeros(size(X_aug));
                end

                % 参考
                R_ref = zeros(2*Np, 1);
                for i = 1:Np
                    R_ref(2*i-1) = beta_ref * pi/180;
                    R_ref(2*i) = 0;
                end

                % QP 求解
                f = Theta' * Q_bar * (Psi * X_aug - R_ref);
                f = max(min(f, 1e6), -1e6);  % 数值保护
                lb = repmat(du_min, Nc, 1);
                ub = repmat(du_max, Nc, 1);
                options_qp = optimoptions('quadprog', 'Display', 'off');
                try
                    [delta_U, ~, exitflag] = quadprog(H, f, [], [], [], [], lb, ub, [], options_qp);
                    if exitflag ~= 1
                        delta_U = zeros(4*Nc, 1);
                    end
                catch
                    delta_U = zeros(4*Nc, 1);
                end

                delta_u = delta_U(1:4);
                u = u_prev + delta_u;
                u = max(min(u, u_max), u_min);

            case 'PID'
                % PID 控制
                Kp_pid = 500; Ki_pid = 50; Kd_pid = 5; K_sync_pid = 100;
                beta_act1 = x(4)/i_ratio * 180/pi;
                beta_act2 = x(8)/i_ratio * 180/pi;
                e1 = beta_ref - beta_act1;
                e2 = beta_ref - beta_act2;
                e_sync = beta_act2 - beta_act1;
                Vq1 = Kp_pid*e1 + Kd_pid*(-x(3)) + K_sync_pid*e_sync;
                Vq2 = Kp_pid*e2 + Kd_pid*(-x(7)) - K_sync_pid*e_sync;
                Vq1 = max(min(Vq1, 500), -500);
                Vq2 = max(min(Vq2, 500), -500);
                u = [0; Vq1; 0; Vq2];

            case 'ADRC'
                % ADRC 控制（简化版）
                beta_act1 = x(4)/i_ratio * 180/pi;
                beta_act2 = x(8)/i_ratio * 180/pi;
                e1 = beta_ref - beta_act1;
                e2 = beta_ref - beta_act2;
                Kp_a = 200; Kd_a = 50; K_sync_a = 80;
                e_sync = (x(4) - x(8)) / i_ratio * 180/pi;
                Vq1 = Kp_a*e1 + Kd_a*(-x(3)) - K_sync_a*e_sync;
                Vq2 = Kp_a*e2 + Kd_a*(-x(7)) + K_sync_a*e_sync;
                Vq1 = max(min(Vq1, 500), -500);
                Vq2 = max(min(Vq2, 500), -500);
                u = [0; Vq1; 0; Vq2];
        end

        % ============ 状态更新（前向欧拉） ============
        % 计算气动转矩
        omega_blade = (x(3) + x(7)) / 2 / i_ratio;
        beta_actual = (x(4) + x(8)) / 2 / i_ratio * 180/pi;
        lambda = max(omega_blade * R_blade / max(v_wind, 0.1), 0.01);
        beta_rad = beta_actual * pi/180;
        Cp = c1*(c2/lambda - c3*beta_rad - c4)*exp(-c5/lambda) + c6*lambda;
        Cp = max(min(Cp, 0.593), 0);
        T_aero = 0.5*rho*A*v_wind^3*Cp / max(omega_blade, 0.01) / i_ratio;

        % 齿轮负载
        beta_rad_m = (x(4) + x(8)) / (2*i_ratio);
        w_beta = (x(3) + x(7)) / (2*i_ratio);
        Tg1 = k_g*(beta_rad_m*i_ratio - x(4))/i_ratio + c_g*(w_beta*i_ratio - x(3))/i_ratio;
        Tg2 = k_g*(beta_rad_m*i_ratio - x(8))/i_ratio + c_g*(w_beta*i_ratio - x(7))/i_ratio;

        % 电磁转矩
        Te1 = 1.5*p*(psi_f*x(2) + (Ld-Lq)*x(1)*x(2));
        Te2 = 1.5*p*(psi_f*x(6) + (Ld-Lq)*x(5)*x(6));

        % 状态方程
        dx = zeros(8,1);
        dx(1) = (-Rs*x(1) + p*Lq*x(3)*x(2) + u(1)) / Ld;
        dx(2) = (-Rs*x(2) - p*Ld*x(3)*x(1) - p*psi_f*x(3) + u(2)) / Lq;
        dx(3) = (Te1 - Tg1 - B_m*x(3)) / J_m;
        dx(4) = x(3);
        dx(5) = (-Rs*x(5) + p*Lq*x(7)*x(6) + u(3)) / Ld;
        dx(6) = (-Rs*x(6) - p*Ld*x(7)*x(5) - p*psi_f*x(7) + u(4)) / Lq;
        dx(7) = (Te2 - Tg2 - B_m*x(7)) / J_m;
        dx(8) = x(7);

        x = x + dt_record * dx;
        u_prev = u;

        % 记录数据
        results(c).x(:, k) = x;
        results(c).u(:, k) = u;
        results(c).beta(k) = (x(4) + x(8)) / 2 / i_ratio * 180/pi;
        results(c).Te(:, k) = [Te1; Te2];
        results(c).sync_err(k) = abs(x(4) - x(8)) / i_ratio * 180/pi;
    end
end

%% ==================== 性能指标计算 ====================
fprintf('\n==================== 性能指标对比 ====================\n');
fprintf('%-8s %-12s %-12s %-12s %-12s\n', '控制器', '上升时间(s)', '超调量(%)', '调节时间(s)', '同步误差(°)');
fprintf('--------------------------------------------------------\n');

for c = 1:n_ctrl
    beta = results(c).beta;
    t = results(c).t;

    % 找到阶跃响应段 (t>=30s)
    idx_step = find(t >= 30);
    beta_step = beta(idx_step);
    t_step = t(idx_step);

    % 上升时间 (10%→90%)
    beta_final = mean(beta_step(end-100:end));
    if abs(beta_final) < 1e-6
        beta_final = 15;  % 默认目标值
    end
    beta_10 = 0.1 * beta_final;
    beta_90 = 0.9 * beta_final;
    idx_10 = find(beta_step >= beta_10, 1);
    idx_90 = find(beta_step >= beta_90, 1);
    if isempty(idx_10), idx_10 = 1; end
    if isempty(idx_90), idx_90 = length(beta_step); end
    t_rise = t_step(idx_90) - t_step(idx_10);

    % 超调量
    beta_max = max(beta_step);
    if abs(beta_final) > 1e-6
        overshoot = max((beta_max - beta_final) / beta_final * 100, 0);
    else
        overshoot = 0;
    end

    % 调节时间 (±2%)
    t_settle = 0;
    tol_band = 0.02 * abs(beta_final);
    for i = length(beta_step):-1:1
        if abs(beta_step(i) - beta_final) > tol_band
            t_settle = t_step(i) - t_step(1);
            break;
        end
    end

    % 同步误差 (稳态平均)
    sync_err = results(c).sync_err;
    sync_steady = mean(sync_err(idx_step(end-100:end)));

    results(c).metrics = struct('t_rise', t_rise, 'overshoot', overshoot, ...
                                 't_settle', t_settle, 'sync_err', sync_steady);

    fprintf('%-8s %-12.3f %-12.2f %-12.3f %-12.4f\n', ...
        controllers{c}, t_rise, overshoot, t_settle, sync_steady);
end

%% ==================== 保存数据 ====================
save('comparison_results.mat', 'results', 't_vec', 'V_wind', 'beta_ref_sim');
fprintf('\n✅ 数据已保存到 comparison_results.mat\n');

%% ==================== 绘图 ====================
plot_comparison(results, t_vec, V_wind, beta_ref_sim);
