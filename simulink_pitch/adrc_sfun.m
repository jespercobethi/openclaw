%% adrc_sfun.m
%  ADRC 控制器 S-Function（自抗扰控制）
%  结构：跟踪微分器(TD) + 扩张状态观测器(ESO) + 非线性反馈(NLSEF)
%
%  输入 u = [beta_ref; w1; theta1; w2; theta2]  (5维)
%  输出 y = [Vq1; Vq2]  (2维)
%
%  参考：王耀锋(2022) ADRC+偏差耦合

function [sys,x0,str,ts] = adrc_sfun(t,x,u,flag)

switch flag
    case 0
        sizes = simsizes;
        sizes.NumContStates  = 0;
        sizes.NumDiscStates  = 18;  % TD(2*2) + ESO(3*2*2) + NLSEF(2)
        sizes.NumOutputs     = 2;
        sizes.NumInputs      = 5;
        sizes.DirFeedthrough = 1;
        sizes.NumSampleTimes = 1;
        sys = simsizes(sizes);
        x0 = zeros(18, 1);
        str = [];
        ts  = [0.001 0];  % 1ms

    case 3
        beta_ref = u(1);
        w1 = u(2); theta1 = u(3);
        w2 = u(4); theta2 = u(5);

        % ADRC 参数
        h = 0.001;          % 采样周期
        r0 = 100;           % TD 速度因子
        h0 = 0.005;         % TD 滤波因子
        beta01 = 200;       % ESO 带宽
        beta02 = 10000;
        beta03 = 100000;
        b0 = 1500;          % 补偿增益
        Kp_adrc = 200;      % NLSEF 比例增益
        Kd_adrc = 50;       % NLSEF 微分增益

        i_ratio = 800;

        % ============ 电机1 ADRC ============
        % TD（跟踪微分器）
        x1_td = x(1); x2_td = x(2);
        beta_ref_m = beta_ref / i_ratio;
        [x1_td_new, x2_td_new] = td_fhan(x1_td, x2_td, beta_ref_m, r0, h0);

        % ESO（扩张状态观测器）- 电机1
        z1 = x(5); z2 = x(6); z3 = x(7);
        y1 = theta1 / i_ratio;
        e_eso = z1 - y1;
        z1_new = z1 + h*(z2 - beta01*e_eso);
        z2_new = z2 + h*(z3 - beta02*fal(e_eso, 0.5, h) + b0*0);
        z3_new = z3 + h*(-beta03*fal(e_eso, 0.25, h));

        % NLSEF（非线性状态误差反馈）
        e1 = x1_td_new - z1_new;
        e2 = x2_td_new - z2_new;
        u0_1 = Kp_adrc*fal(e1, 0.5, h) + Kd_adrc*fal(e2, 0.75, h);
        Vq1 = (u0_1 - z3_new) / b0;

        % ============ 电机2 ADRC ============
        % TD
        x3_td = x(3); x4_td = x(4);
        [x3_td_new, x4_td_new] = td_fhan(x3_td, x4_td, beta_ref_m, r0, h0);

        % ESO - 电机2
        z4 = x(8); z5 = x(9); z6 = x(10);
        y2 = theta2 / i_ratio;
        e_eso2 = z4 - y2;
        z4_new = z4 + h*(z5 - beta01*e_eso2);
        z5_new = z5 + h*(z6 - beta02*fal(e_eso2, 0.5, h) + b0*0);
        z6_new = z6 + h*(-beta03*fal(e_eso2, 0.25, h));

        % NLSEF - 电机2
        e3 = x3_td_new - z4_new;
        e4 = x4_td_new - z5_new;
        u0_2 = Kp_adrc*fal(e3, 0.5, h) + Kd_adrc*fal(e4, 0.75, h);
        Vq2 = (u0_2 - z6_new) / b0;

        % 偏差耦合同步补偿
        K_sync = 80;
        e_sync = (theta1 - theta2) / i_ratio;
        Vq1 = Vq1 - K_sync * e_sync;
        Vq2 = Vq2 + K_sync * e_sync;

        % 限幅
        Vq1 = max(min(Vq1, 500), -500);
        Vq2 = max(min(Vq2, 500), -500);

        sys = [Vq1; Vq2];

    case 2
        % 更新离散状态
        beta_ref = u(1);
        w1 = u(2); theta1 = u(3);
        w2 = u(4); theta2 = u(5);

        h = 0.001; r0 = 100; h0 = 0.005;
        beta01 = 200; beta02 = 10000; beta03 = 100000;
        b0 = 1500; Kp_adrc = 200; Kd_adrc = 50;
        i_ratio = 800;

        % TD 更新
        beta_ref_m = beta_ref / i_ratio;
        [x1_td, x2_td] = td_fhan(x(1), x(2), beta_ref_m, r0, h0);
        [x3_td, x4_td] = td_fhan(x(3), x(4), beta_ref_m, r0, h0);

        % ESO 更新
        z1 = x(5); z2 = x(6); z3 = x(7);
        y1 = theta1 / i_ratio;
        e1 = z1 - y1;
        z1 = z1 + h*(z2 - beta01*e1);
        z2 = z2 + h*(z3 - beta02*fal(e1, 0.5, h));
        z3 = z3 + h*(-beta03*fal(e1, 0.25, h));

        z4 = x(8); z5 = x(9); z6 = x(10);
        y2 = theta2 / i_ratio;
        e2 = z4 - y2;
        z4 = z4 + h*(z5 - beta01*e2);
        z5 = z5 + h*(z6 - beta02*fal(e2, 0.5, h));
        z6 = z6 + h*(-beta03*fal(e2, 0.25, h));

        sys = [x1_td; x2_td; x3_td; x4_td; z1; z2; z3; z4; z5; z6; 0; 0; 0; 0; 0; 0; 0; 0];

    case {1,4,9}
        sys = [];
    otherwise
        error(['Unhandled flag = ',num2str(flag)]);
end
end

%% ========== 辅助函数 ==========
function [x1_new, x2_new] = td_fhan(x1, x2, v, r, h)
    % 跟踪微分器（韩志刚 fhan 函数）
    d = r * h^2;
    a0 = h * x2;
    y = x1 - v + a0;
    a1 = sqrt(d*(d + 8*abs(y)));
    a2 = a0 + sign(y)*(a1 - d)/2;
    sy = (sign(y+d) - sign(y-d))/2;
    a = (a0 + y - a2)*sy + a2;
    sa = (sign(a+d) - sign(a-d))/2;
    fhan = -r*(a/d - sign(a))*sa - r*sign(a);
    x1_new = x1 + h * x2;
    x2_new = x2 + h * fhan;
end

function y = fal(e, alpha, delta)
    % 非线性函数
    if abs(e) <= delta
        y = e / (delta^(1-alpha));
    else
        y = sign(e) * abs(e)^alpha;
    end
end
