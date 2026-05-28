function [sys,x0,str,ts] = blade_sfun(t,x,u,flag)
% 叶片动力学 S-Function（无参数版，从 workspace 读取）
% 状态 x = [theta_blade, omega_blade]
% 输入 u = [T_motor_total, T_aero]

switch flag
    case 0
        sizes = simsizes;
        sizes.NumContStates  = 2;
        sizes.NumOutputs     = 2;
        sizes.NumInputs      = 2;
        sizes.DirFeedthrough = 0;
        sizes.NumSampleTimes = 1;
        sys = simsizes(sizes);
        x0 = [0; 0];
        str = [];
        ts  = [0 0];
    case 1
        J_blade = evalin('base', 'J_blade');
        B_blade = evalin('base', 'B_blade');

        theta_blade = x(1);
        omega_blade = x(2);
        T_motor_total = u(1);
        T_aero = u(2);

        dtheta = omega_blade;
        domega = (T_aero + T_motor_total - B_blade*omega_blade) / J_blade;

        sys = [dtheta; domega];
    case 3
        sys = x;
    case {2,4,9}
        sys = [];
    otherwise
        error(['Unhandled flag = ',num2str(flag)]);
end
