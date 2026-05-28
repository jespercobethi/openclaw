function [sys,x0,str,ts] = dual_motor_sfun(t,x,u,flag)
% 双驱变桨伺服系统 S-Function（优化版：persistent 缓存参数）
% 8状态非线性模型
%
% 输入 u = [Vd1, Vq1, Vd2, Vq2, T_load1, T_load2]
% 输出 y = [id1, iq1, w1, theta1, id2, iq2, w2, theta2, Te1, Te2, w1rpm, w2rpm]

persistent params_loaded Rs Ld Lq psi_f p J_m B_m i_ratio k_g c_g

switch flag
    case 0  % 初始化
        % 只读一次参数
        if isempty(params_loaded)
            Rs      = evalin('base', 'Rs');
            Ld      = evalin('base', 'Ld');
            Lq      = evalin('base', 'Lq');
            psi_f   = evalin('base', 'psi_f');
            p       = evalin('base', 'p');
            J_m     = evalin('base', 'J_m');
            B_m     = evalin('base', 'B_m');
            i_ratio = evalin('base', 'i_ratio');
            k_g     = evalin('base', 'k_g');
            c_g     = evalin('base', 'c_g');
            params_loaded = true;
        end

        sizes = simsizes;
        sizes.NumContStates  = 8;
        sizes.NumDiscStates  = 0;
        sizes.NumOutputs     = 12;
        sizes.NumInputs      = 6;
        sizes.DirFeedthrough = 1;
        sizes.NumSampleTimes = 1;
        sys = simsizes(sizes);
        x0 = zeros(8, 1);
        str = [];
        ts  = [0 0];

    case 1  % 微分
        id1 = x(1); iq1 = x(2); w1 = x(3); theta1 = x(4);
        id2 = x(5); iq2 = x(6); w2 = x(7); theta2 = x(8);
        Vd1 = u(1); Vq1 = u(2); Vd2 = u(3); Vq2 = u(4);
        T_load1 = u(5); T_load2 = u(6);

        Te1 = 1.5*p*(psi_f*iq1 + (Ld-Lq)*id1*iq1);
        Te2 = 1.5*p*(psi_f*iq2 + (Ld-Lq)*id2*iq2);

        beta_rad = (theta1+theta2)/(2*i_ratio);
        w_beta = (w1+w2)/(2*i_ratio);
        Tg1 = k_g*(beta_rad*i_ratio-theta1)/i_ratio + c_g*(w_beta*i_ratio-w1)/i_ratio;
        Tg2 = k_g*(beta_rad*i_ratio-theta2)/i_ratio + c_g*(w_beta*i_ratio-w2)/i_ratio;

        did1 = (-Rs*id1 + p*Lq*w1*iq1 + Vd1) / Ld;
        diq1 = (-Rs*iq1 - p*Ld*w1*id1 - p*psi_f*w1 + Vq1) / Lq;
        dw1  = (Te1 - Tg1 - T_load1 - B_m*w1) / J_m;
        dtheta1 = w1;

        did2 = (-Rs*id2 + p*Lq*w2*iq2 + Vd2) / Ld;
        diq2 = (-Rs*iq2 - p*Ld*w2*id2 - p*psi_f*w2 + Vq2) / Lq;
        dw2  = (Te2 - Tg2 - T_load2 - B_m*w2) / J_m;
        dtheta2 = w2;

        sys = [did1; diq1; dw1; dtheta1; did2; diq2; dw2; dtheta2];

    case 3  % 输出
        id1 = x(1); iq1 = x(2); w1 = x(3);
        id2 = x(5); iq2 = x(6); w2 = x(7);

        Te1 = 1.5*p*(psi_f*iq1 + (Ld-Lq)*id1*iq1);
        Te2 = 1.5*p*(psi_f*iq2 + (Ld-Lq)*id2*iq2);
        w1_rpm = w1*60/(2*pi);
        w2_rpm = w2*60/(2*pi);

        sys = [x; Te1; Te2; w1_rpm; w2_rpm];

    case {2,4,9}
        sys = [];
    otherwise
        error(['Unhandled flag = ',num2str(flag)]);
end
