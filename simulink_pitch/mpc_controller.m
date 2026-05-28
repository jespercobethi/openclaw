%% mpc_controller.m
%  双驱变桨系统 MPC 控制器
%  基于线性化模型的离散 MPC
%
%  控制目标：
%    1. 桨距角跟踪参考 β_ref
%    2. 双电机同步（θ1 ≈ θ2）
%    3. 满足约束（力矩/转速/桨距角速率）
%
%  日期：2026-05-28

%% ==================== 0. 构建 params 结构体 ====================
params.Rs = Rs; params.Ld = Ld; params.Lq = Lq;
params.psi_f = psi_f; params.p = p;
params.J_m = J_m; params.B_m = B_m;
params.i_ratio = i_ratio; params.k_g = k_g; params.c_g = c_g;
params.rho = rho; params.A = A; params.R_blade = R_blade;
params.Cp_fun = Cp_fun;

%% ==================== 1. 工作点线性化 ====================
%  额定工况：V0=12m/s, β0=15°, ω0=额定
V0 = R_rated;                    % 额定风速
beta0_rad = 15 * pi / 180;       % 稳态桨距角 [rad]
omega0 = omega_rated;            % 稳态电机角速度

% 稳态电流（MTPA: id=0）
iq0 = (0.5 * rho * A * V0^3 * Cp_fun(omega0*R_blade/V0, beta0_rad)) / ...
      (1.5 * p * psi_f * omega0 * i_ratio);  % 粗略估算

% 稳态电压
Vd0 = Rs * 0 - p * Lq * omega0 * iq0;  % Vd = Rs*id - p*Lq*ω*iq
Vq0 = Rs * iq0 + p * Ld * omega0 * 0 + p * psi_f * omega0;

%% ==================== 2. 数值线性化（雅可比矩阵） ====================
%  在工作点 (x0, u0) 处数值求解 A, B 矩阵
%  x = [id1, iq1, ω1, θ1, id2, iq2, ω2, θ2]
%  u = [Vd1, Vq1, Vd2, Vq2]

x0 = [0; iq0; omega0; 0; 0; iq0; omega0; 0];
u0 = [Vd0; Vq0; Vd0; Vq0];
T_load0 = 0;  % 稳态负载力矩

% 数值微分求 A 矩阵
eps_x = 1e-8;
A_cont = zeros(8, 8);
for j = 1:8
    x_plus = x0; x_plus(j) = x_plus(j) + eps_x;
    x_minus = x0; x_minus(j) = x_minus(j) - eps_x;
    f_plus = dual_motor_dynamics(x_plus, u0, T_load0, T_load0, params);
    f_minus = dual_motor_dynamics(x_minus, u0, T_load0, T_load0, params);
    A_cont(:, j) = (f_plus - f_minus) / (2 * eps_x);
end

% 数值微分求 B 矩阵
eps_u = 1e-8;
B_cont = zeros(8, 4);
for j = 1:4
    u_plus = u0; u_plus(j) = u_plus(j) + eps_u;
    u_minus = u0; u_minus(j) = u_minus(j) - eps_u;
    f_plus = dual_motor_dynamics(x0, u_plus, T_load0, T_load0, params);
    f_minus = dual_motor_dynamics(x0, u_minus, T_load0, T_load0, params);
    B_cont(:, j) = (f_plus - f_minus) / (2 * eps_u);
end

% 扰动矩阵 Bw（风速影响）
eps_w = 1e-6;
w0 = V0;
f_plus = dual_motor_dynamics(x0, u0, T_load0, T_load0, params, w0 + eps_w);
f_minus = dual_motor_dynamics(x0, u0, T_load0, T_load0, params, w0 - eps_w);
Bw_cont = (f_plus - f_minus) / (2 * eps_w);

fprintf('✅ 连续状态空间矩阵已线性化：\n');
fprintf('  A_cont: %dx%d\n', size(A_cont));
fprintf('  B_cont: %dx%d\n', size(B_cont));
fprintf('  Bw_cont: %dx%d\n', size(Bw_cont));

%% ==================== 3. 离散化（前向欧拉） ====================
Ts_mpc = Ts_outer;  % MPC 控制周期 = 外环周期 (10ms)
Ad = eye(8) + Ts_mpc * A_cont;
Bd = Ts_mpc * B_cont;
Bwd = Ts_mpc * Bw_cont;

fprintf('✅ 离散化完成 (Ts=%.1fms)\n', Ts_mpc*1000);

%% ==================== 4. 输出矩阵 ====================
%  输出：y = [β_actual, Δω_sync]
%  β_actual = (θ1 + θ2) / (2 * i_ratio)  [rad]
%  Δω_sync  = ω1 - ω2                    [rad/s]

C_mpc = zeros(2, 8);
C_mpc(1, 4) = 1 / (2 * i_ratio);  % θ1 对 β 的贡献
C_mpc(1, 8) = 1 / (2 * i_ratio);  % θ2 对 β 的贡献
C_mpc(2, 3) = 1;                   % ω1
C_mpc(2, 7) = -1;                  % -ω2

D_mpc = zeros(2, 4);

%% ==================== 5. MPC 权重矩阵 ====================
%  状态权重 Q（惩罚桨距角误差 + 同步误差）
Qx = zeros(8, 8);
Qx(4, 4) = 100;   % θ1（桨距角相关）
Qx(8, 8) = 100;   % θ2（桨距角相关）
Qx(3, 3) = 50;    % ω1（同步相关）
Qx(7, 7) = 50;    % ω2（同步相关）

% 控制增量权重 R
Ru = diag([0.1, 0.01, 0.1, 0.01]);  % Vd 权重大，Vq 权重小

%% ==================== 6. 约束定义 ====================
%  控制量约束
u_min = [-50; -T_max*1.5; -50; -T_max*1.5];  % 电压下限
u_max = [ 50;  T_max*1.5;  50;  T_max*1.5];  % 电压上限

%  控制增量约束
du_min = [-100; -200; -100; -200];
du_max = [ 100;  200;  100;  200];

%  输出约束
y_min = [0; -10];        % β≥0, Δω≥-10
y_max = [90*pi/180; 10]; % β≤90°, Δω≤10

%% ==================== 7. 构建 MPC 增量形式 ====================
%  增量状态：Δx(k) = x(k) - x(k-1)
%  增量模型：Δx(k+1) = Ad*Δx(k) + Bd*Δu(k)
%  输出：y(k) = C*x(k)

% 扩展状态空间（含积分）
%  X_aug = [Δx; y]
%  X_aug(k+1) = A_aug * X_aug(k) + B_aug * Δu(k)
A_aug = [Ad,        zeros(8, 2);
         C_mpc*Ad,  eye(2)];

B_aug = [Bd; C_mpc*Bd];

C_aug = [zeros(2, 8), eye(2)];

[n_aug, ~] = size(A_aug);

%% ==================== 8. 构建预测矩阵 ====================
%  Y = Psi * X_aug(k) + Theta * ΔU
%  其中 ΔU = [Δu(k), Δu(k+1), ..., Δu(k+Nc-1)]

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

%% ==================== 9. QP 权重矩阵 ====================
%  目标函数：J = (Y - R)' * Q_bar * (Y - R) + ΔU' * R_bar * ΔU
Q_bar = zeros(2*Np, 2*Np);
for i = 1:Np
    Q_bar(2*i-1, 2*i-1) = Q_beta;   % 桨距角跟踪
    Q_bar(2*i, 2*i)     = Q_sync;   % 同步误差
end

R_bar = zeros(4*Nc, 4*Nc);
for i = 1:Nc
    R_bar(4*i-3:4*i, 4*i-3:4*i) = Ru;
end

% Hessian 矩阵
H = Theta' * Q_bar * Theta + R_bar;
H = (H + H') / 2;  % 确保对称
H = H + 1e-6*eye(size(H));  % 正则化，确保正定
H = H + 1e-6 * eye(size(H));  % 正则化，确保正定

fprintf('✅ MPC 预测模型构建完成\n');
fprintf('  预测时域 Np = %d\n', Np);
fprintf('  控制时域 Nc = %d\n', Nc);
fprintf('  扩展状态维度 = %d\n', n_aug);
fprintf('  Hessian 矩阵维度 = %d x %d\n', size(H));

%% ==================== 辅助函数 ====================
function dx = dual_motor_dynamics(x, u, T_load1, T_load2, params, V_wind)
    if nargin < 6, V_wind = 12; end

    Rs    = params.Rs;    Ld = params.Ld;    Lq = params.Lq;
    psi_f = params.psi_f; p  = params.p;
    J_m   = params.J_m;   B_m = params.B_m;
    i_ratio = params.i_ratio;
    k_g   = params.k_g;   c_g = params.c_g;
    rho   = params.rho;   A  = params.A;
    R_blade = params.R_blade;

    id1 = x(1); iq1 = x(2); w1 = x(3); theta1 = x(4);
    id2 = x(5); iq2 = x(6); w2 = x(7); theta2 = x(8);
    Vd1 = u(1); Vq1 = u(2); Vd2 = u(3); Vq2 = u(4);

    Te1 = 1.5*p*(psi_f*iq1 + (Ld-Lq)*id1*iq1);
    Te2 = 1.5*p*(psi_f*iq2 + (Ld-Lq)*id2*iq2);

    % 齿轮负载
    beta_rad = (theta1 + theta2) / (2*i_ratio);
    omega_beta = (w1 + w2) / (2*i_ratio);
    Tg1 = k_g*(beta_rad*i_ratio - theta1)/i_ratio + c_g*(omega_beta*i_ratio - w1)/i_ratio;
    Tg2 = k_g*(beta_rad*i_ratio - theta2)/i_ratio + c_g*(omega_beta*i_ratio - w2)/i_ratio;

    % 状态方程
    did1 = (-Rs*id1 + p*Lq*w1*iq1 + Vd1) / Ld;
    diq1 = (-Rs*iq1 - p*Ld*w1*id1 - p*psi_f*w1 + Vq1) / Lq;
    dw1  = (Te1 - Tg1 - T_load1 - B_m*w1) / J_m;
    dtheta1 = w1;

    did2 = (-Rs*id2 + p*Lq*w2*iq2 + Vd2) / Ld;
    diq2 = (-Rs*iq2 - p*Ld*w2*id2 - p*psi_f*w2 + Vq2) / Lq;
    dw2  = (Te2 - Tg2 - T_load2 - B_m*w2) / J_m;
    dtheta2 = w2;

    dx = [did1; diq1; dw1; dtheta1; did2; diq2; dw2; dtheta2];
end
