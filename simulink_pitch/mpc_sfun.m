function [sys,x0,str,ts] = mpc_sfun(t,x,u,flag)
% MPC 控制器 S-Function（优化版：persistent 缓存参数）
%
% 输入 u = [beta_ref; x_state(8)]  (9维)
% 输出 y = [Vd1; Vq1; Vd2; Vq2]  (4维)

persistent params_loaded H Theta Psi Q_bar Np Nc du_min du_max u_min u_max i_ratio Vq0_init

switch flag
    case 0
        if isempty(params_loaded)
            H       = evalin('base', 'H');
            Theta   = evalin('base', 'Theta');
            Psi     = evalin('base', 'Psi');
            Q_bar   = evalin('base', 'Q_bar');
            Np      = evalin('base', 'Np');
            Nc      = evalin('base', 'Nc');
            du_min  = evalin('base', 'du_min');
            du_max  = evalin('base', 'du_max');
            u_min   = evalin('base', 'u_min');
            u_max   = evalin('base', 'u_max');
            i_ratio = evalin('base', 'i_ratio');
            Vq0_init = evalin('base', 'Vq0');
            params_loaded = true;
        end

        sizes = simsizes;
        sizes.NumContStates  = 0;
        sizes.NumDiscStates  = 10;
        sizes.NumOutputs     = 4;
        sizes.NumInputs      = 9;
        sizes.DirFeedthrough = 1;
        sizes.NumSampleTimes = 1;
        sys = simsizes(sizes);
        x0 = zeros(10, 1);
        str = [];
        ts  = [0.01 0];

    case 3
        beta_ref = u(1);
        x_curr = u(2:9);

        % 上一步状态
        x_prev = x(2:9);
        u_prev = [0; Vq0_init; 0; Vq0_init];

        % 增量状态
        delta_x = x_curr - x_prev;
        delta_x = max(min(delta_x, 1e4), -1e4);

        % 当前输出
        C_out = zeros(2, 8);
        C_out(1, 4) = 1/(2*i_ratio);
        C_out(1, 8) = 1/(2*i_ratio);
        C_out(2, 3) = 1;
        C_out(2, 7) = -1;
        y_curr = C_out * x_curr;
        y_curr = max(min(y_curr, 1e4), -1e4);

        X_aug = [delta_x; y_curr];
        if any(isnan(X_aug)) || any(isinf(X_aug))
            X_aug = zeros(size(X_aug));
        end

        % 参考轨迹
        R_ref = zeros(2*Np, 1);
        beta_ref_rad = beta_ref * pi/180;
        for i = 1:Np
            R_ref(2*i-1) = beta_ref_rad;
            R_ref(2*i) = 0;
        end

        % QP 求解
        f = Theta' * Q_bar * (Psi * X_aug - R_ref);
        f = max(min(f, 1e6), -1e6);
        lb = repmat(du_min, Nc, 1);
        ub = repmat(du_max, Nc, 1);
        opts = optimoptions('quadprog', 'Display', 'off');
        try
            [dU, ~, ef] = quadprog(H, f, [], [], [], [], lb, ub, [], opts);
            if ef ~= 1, dU = zeros(4*Nc, 1); end
        catch
            dU = zeros(4*Nc, 1);
        end

        delta_u = dU(1:4);
        u_new = u_prev + delta_u;
        u_new = max(min(u_new, u_max), u_min);

        sys = u_new;

    case 2
        x_curr = u(2:9);
        sys = [0; x_curr; 1];

    case {1,4,9}
        sys = [];
    otherwise
        error(['Unhandled flag = ',num2str(flag)]);
end
