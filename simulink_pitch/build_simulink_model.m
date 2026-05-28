%% build_simulink_model.m
%  自动搭建双驱变桨开环 Simulink 模型
%  运行前先运行 setup_params.m 加载参数
%
%  结构：常量电压 → Mux → 双电机S-Fun → Scope
%        （开环，无负载反馈）

%% 加载参数
if ~exist('Rs','var')
    setup_params;
end

%% 关闭旧模型
model = 'dual_motor_pitch_openloop';
if bdIsLoaded(model)
    close_system(model, 0);
end
new_system(model);

%% ========== 电压输入（开环恒定） ==========
add_block('simulink/Sources/Constant', [model '/Vd1'], 'Value', '0', 'Position', [50 200 80 220]);
add_block('simulink/Sources/Constant', [model '/Vq1'], 'Value', '100', 'Position', [50 240 80 260]);
add_block('simulink/Sources/Constant', [model '/Vd2'], 'Value', '0', 'Position', [50 280 80 300]);
add_block('simulink/Sources/Constant', [model '/Vq2'], 'Value', '100', 'Position', [50 320 80 340]);
add_block('simulink/Sources/Constant', [model '/TL1'], 'Value', '0', 'Position', [50 360 80 380]);
add_block('simulink/Sources/Constant', [model '/TL2'], 'Value', '0', 'Position', [50 400 80 420]);

%% ========== Mux 合并 6 路输入 ==========
add_block('simulink/Signal Routing/Mux', [model '/Mux_u'], ...
    'Inputs', '6', 'Position', [150 195 155 425]);

add_line(model, 'Vd1/1', 'Mux_u/1');
add_line(model, 'Vq1/1', 'Mux_u/2');
add_line(model, 'Vd2/1', 'Mux_u/3');
add_line(model, 'Vq2/1', 'Mux_u/4');
add_line(model, 'TL1/1',  'Mux_u/5');
add_line(model, 'TL2/1',  'Mux_u/6');

%% ========== 双电机 S-Function ==========
add_block('simulink/User-Defined Functions/S-Function', [model '/DualMotor'], ...
    'FunctionName', 'dual_motor_sfun', ...
    'Position', [220 250 380 380]);

add_line(model, 'Mux_u/1', 'DualMotor/1');

%% ========== Demux 输出 ==========
add_block('simulink/Signal Routing/Demux', [model '/Demux_y'], ...
    'Outputs', '12', 'Position', [440 230 445 400]);

add_line(model, 'DualMotor/1', 'Demux_y/1');

%% ========== Scopes ==========
add_block('simulink/Sinks/Scope', [model '/States'], 'Position', [550 100 600 140]);
add_block('simulink/Sinks/Scope', [model '/Torques'], 'Position', [550 160 600 200]);

% y(1:8) = 状态, y(9:10) = Te1,Te2, y(11:12) = w_rpm
add_line(model, 'Demux_y/1', 'States/1');
add_line(model, 'Demux_y/2', 'Torques/1');

% 未使用的输出端口加 Terminator
for i = 3:12
    blk = sprintf('%s/T%d', model, i);
    add_block('simulink/Sinks/Terminator', blk, 'Position', [550 200+(i-3)*20 570 215+(i-3)*20]);
    add_line(model, sprintf('Demux_y/%d', i), sprintf('T%d/1', i));
end

%% ========== To Workspace ==========
add_block('simulink/Sinks/To Workspace', [model '/x_out'], ...
    'VariableName', 'x_sim', 'Position', [550 300 600 320]);
add_line(model, 'DualMotor/1', 'x_out/1');

%% ========== 仿真参数 ==========
set_param(model, 'StopTime', '100');
set_param(model, 'Solver', 'ode4');
set_param(model, 'FixedStep', '0.001');
set_param(model, 'RelTol', '1e-4');

%% ========== 保存 ==========
save_system(model);
open_system(model);
fprintf('✅ Simulink 模型 "%s" 创建完成！\n', model);
fprintf('  结构：常量电压 → Mux → 双电机S-Fun → Scope\n');
fprintf('  点击运行即可仿真。\n');
