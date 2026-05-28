%% pid_sfun.m
%  PID 控制器 S-Function（双电机独立 PID + 偏差耦合同步）
%
%  输入 u = [beta_ref; w1; theta1; w2; theta2]  (5维)
%  输出 y = [Vq1; Vq2]  (2维, Vd=0 MTPA)
%
%  结构：每个电机一个 PI 速度环 + 偏差耦合同步补偿

function [sys,x0,str,ts] = pid_sfun(t,x,u,flag)

switch flag
    case 0
        sizes = simsizes;
        sizes.NumContStates  = 0;
        sizes.NumDiscStates  = 4;  % [e_int1, e_int2, e_sync_int1, e_sync_int2]
        sizes.NumOutputs     = 2;
        sizes.NumInputs      = 5;
        sizes.DirFeedthrough = 1;
        sizes.NumSampleTimes = 1;
        sys = simsizes(sizes);
        x0 = zeros(4, 1);
        str = [];
        ts  = [0.001 0];  % 1ms 采样（速度环）

    case 3
        beta_ref = u(1);
        w1 = u(2); theta1 = u(3);
        w2 = u(4); theta2 = u(5);

        % PID 参数
        Kp = 500;
        Ki = 50;
        Kd = 5;
        K_sync = 100;  % 同步增益

        % 传动比
        i_ratio = 800;

        % 桨距角误差（从电机侧角度转换）
        beta_actual1 = theta1 / i_ratio;
        beta_actual2 = theta2 / i_ratio;
        beta_ref_m = beta_ref / i_ratio;

        e1 = beta_ref_m - beta_actual1;
        e2 = beta_ref_m - beta_actual2;

        % 同步误差
        e_sync1 = beta_actual2 - beta_actual1;
        e_sync2 = beta_actual1 - beta_actual2;

        % 积分项（离散状态）
        e_int1 = x(1) + e1 * 0.001;
        e_int2 = x(2) + e2 * 0.001;
        e_sync_int1 = x(3) + e_sync1 * 0.001;
        e_sync_int2 = x(4) + e_sync2 * 0.001;

        % 积分限幅
        e_int1 = max(min(e_int1, 10), -10);
        e_int2 = max(min(e_int2, 10), -10);

        % PID 输出 + 同步补偿
        Vq1 = Kp*e1 + Ki*e_int1 + Kd*(-w1) + K_sync*e_sync1;
        Vq2 = Kp*e2 + Ki*e_int2 + Kd*(-w2) + K_sync*e_sync2;

        % 限幅
        Vq1 = max(min(Vq1, 500), -500);
        Vq2 = max(min(Vq2, 500), -500);

        sys = [Vq1; Vq2];

    case 2
        beta_ref = u(1);
        w1 = u(2); theta1 = u(3);
        w2 = u(4); theta2 = u(5);

        i_ratio = 800;
        Kp = 500; Ki = 50;
        K_sync = 100;

        beta_actual1 = theta1 / i_ratio;
        beta_actual2 = theta2 / i_ratio;
        beta_ref_m = beta_ref / i_ratio;

        e1 = beta_ref_m - beta_actual1;
        e2 = beta_ref_m - beta_actual2;
        e_sync1 = beta_actual2 - beta_actual1;
        e_sync2 = beta_actual1 - beta_actual2;

        e_int1 = x(1) + e1 * 0.001;
        e_int2 = x(2) + e2 * 0.001;
        e_sync_int1 = x(3) + e_sync1 * 0.001;
        e_sync_int2 = x(4) + e_sync2 * 0.001;

        e_int1 = max(min(e_int1, 10), -10);
        e_int2 = max(min(e_int2, 10), -10);

        sys = [e_int1; e_int2; e_sync_int1; e_sync_int2];

    case {1,4,9}
        sys = [];
    otherwise
        error(['Unhandled flag = ',num2str(flag)]);
end
