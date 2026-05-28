%% build_closed_loop.m
%  闭环 Simulink：β_ref + x → MPC → Vdq → 双电机 → 状态反馈
%  运行前先运行 setup_params + mpc_controller

if ~exist('Rs','var'), setup_params; end
if ~exist('H','var'), mpc_controller; end

model = 'dual_motor_pitch_mpc';
if bdIsLoaded(model), close_system(model, 0); end
new_system(model);

%% ========== 1. β_ref ==========
add_block('simulink/Sources/Step', [model '/beta_ref'], ...
    'Time', '30', 'Before', '0', 'After', '15', 'Position', [30 250 80 280]);

%% ========== 2. Mux: [β_ref; x(8)] → MPC ==========
add_block('simulink/Signal Routing/Mux', [model '/Mux_mpc_in'], ...
    'Inputs', '[1, 8]', 'Position', [140 200 145 350]);
add_line(model, 'beta_ref/1', 'Mux_mpc_in/1');

%% ========== 3. MPC S-Function ==========
add_block('simulink/User-Defined Functions/S-Function', [model '/MPC'], ...
    'FunctionName', 'mpc_sfun', 'Position', [210 230 360 320]);
add_line(model, 'Mux_mpc_in/1', 'MPC/1');  % MPC输入

%% ========== 4. Demux: MPC输出(4路) ==========
add_block('simulink/Signal Routing/Demux', [model '/Demux_mpc'], ...
    'Outputs', '4', 'Position', [410 230 415 320]);
add_line(model, 'MPC/1', 'Demux_mpc/1');

%% ========== 5. Mux: [Vd1,Vq1,Vd2,Vq2,0,0] → 双电机 ==========
add_block('simulink/Signal Routing/Mux', [model '/Mux_u'], ...
    'Inputs', '6', 'Position', [470 230 475 420]);
add_block('simulink/Sources/Constant', [model '/TL1'], 'Value', '0', 'Position', [380 380 410 400]);
add_block('simulink/Sources/Constant', [model '/TL2'], 'Value', '0', 'Position', [380 420 410 440]);

add_line(model, 'Demux_mpc/1', 'Mux_u/1');  % Vd1
add_line(model, 'Demux_mpc/2', 'Mux_u/2');  % Vq1
add_line(model, 'Demux_mpc/3', 'Mux_u/3');  % Vd2
add_line(model, 'Demux_mpc/4', 'Mux_u/4');  % Vq2
add_line(model, 'TL1/1', 'Mux_u/5');
add_line(model, 'TL2/1', 'Mux_u/6');

%% ========== 6. 双电机 S-Function ==========
add_block('simulink/User-Defined Functions/S-Function', [model '/DualMotor'], ...
    'FunctionName', 'dual_motor_sfun', 'Position', [540 260 700 390]);
add_line(model, 'Mux_u/1', 'DualMotor/1');

%% ========== 7. Demux: 双电机输出12路 ==========
% y = [id1,iq1,w1,θ1,id2,iq2,w2,θ2, Te1,Te2,w1rpm,w2rpm]
add_block('simulink/Signal Routing/Demux', [model '/Demux_y'], ...
    'Outputs', '12', 'Position', [760 240 765 410]);
add_line(model, 'DualMotor/1', 'Demux_y/1');

%% ========== 8. Mux: 前8路状态 → 反馈到 MPC ==========
% 加 Unit Delay 打破代数环（8维向量）
add_block('simulink/Discrete/Unit Delay', [model '/Delay_fb'], ...
    'SampleTime', '0.01', ...
    'Position', [80 380 110 410]);
add_block('simulink/Signal Routing/Mux', [model '/Mux_fb'], ...
    'Inputs', '8', 'Position', [140 360 145 480]);
for i = 1:8
    add_line(model, sprintf('Demux_y/%d', i), sprintf('Mux_fb/%d', i));
end
add_line(model, 'Mux_fb/1', 'Delay_fb/1');
add_line(model, 'Delay_fb/1', 'Mux_mpc_in/2');  % 状态反馈（带延迟打破代数环）

%% ========== 9. Scopes & Terminators ==========
add_block('simulink/Sinks/Scope', [model '/Ctrl_Scope'], 'Position', [870 200 920 240]);
add_line(model, 'MPC/1', 'Ctrl_Scope/1');

add_block('simulink/Sinks/Scope', [model '/State_Scope'], 'Position', [870 300 920 340]);
add_line(model, 'DualMotor/1', 'State_Scope/1');

% 未用的输出端口加 Terminator
for i = 9:12
    blk = sprintf('%s/T%d', model, i);
    add_block('simulink/Sinks/Terminator', blk, 'Position', [870 200+(i-9)*25 895 215+(i-9)*25]);
    add_line(model, sprintf('Demux_y/%d', i), sprintf('T%d/1', i));
end

%% ========== 10. To Workspace ==========
add_block('simulink/Sinks/To Workspace', [model '/x_out'], ...
    'VariableName', 'x_sim', 'Position', [870 400 920 420]);
add_block('simulink/Sinks/To Workspace', [model '/u_out'], ...
    'VariableName', 'u_sim', 'Position', [870 440 920 460]);
add_line(model, 'DualMotor/1', 'x_out/1');
add_line(model, 'MPC/1', 'u_out/1');

%% ========== 仿真参数 ==========
set_param(model, 'StopTime', '100');
set_param(model, 'Solver', 'ode45');
set_param(model, 'MaxStep', '1e-3');
set_param(model, 'RelTol', '1e-6');
set_param(model, 'AbsTol', '1e-8');

save_system(model);
open_system(model);
fprintf('✅ 闭环模型 "%s" 创建完成！\n', model);
