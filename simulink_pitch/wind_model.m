function V = wind_model(t, V_mean, V_ramp, T_ramp_start, T_ramp_dur)
% 风速模型：平均风速 + 斜坡阵风
%   t:             当前时间 [s]
%   V_mean:        平均风速 [m/s]
%   V_ramp:        阵风幅值 [m/s]
%   T_ramp_start:  阵风起始时刻 [s]
%   T_ramp_dur:    阵风持续时间 [s]

% 斜坡阵风
if t < T_ramp_start
    V_gust = 0;
elseif t < T_ramp_start + T_ramp_dur/2
    V_gust = V_ramp * (t - T_ramp_start) / (T_ramp_dur/2);
elseif t < T_ramp_start + T_ramp_dur
    V_gust = V_ramp * (1 - (t - T_ramp_start - T_ramp_dur/2) / (T_ramp_dur/2));
else
    V_gust = 0;
end

V = V_mean + V_gust;
end
