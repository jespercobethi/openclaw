function plot_comparison(results, t_vec, V_wind, beta_ref_sim)
% 绘制三种控制器对比图

colors = {'b', 'r', 'g'};
line_styles = {'-', '--', '-.'};
n_ctrl = length(results);

%% ========== 图1：桨距角跟踪对比 ==========
figure('Name', '桨距角跟踪对比', 'Position', [100 100 1000 500]);

subplot(2,1,1);
hold on; grid on;
plot(t_vec, beta_ref_sim, 'k--', 'LineWidth', 2, 'DisplayName', '参考 β_{ref}');
for c = 1:n_ctrl
    plot(t_vec, results(c).beta, [colors{c}, line_styles{c}], 'LineWidth', 1.5, ...
        'DisplayName', results(c).name);
end
xlabel('时间 [s]'); ylabel('桨距角 [°]');
title('桨距角跟踪对比');
legend('Location', 'best');
xlim([25 80]);

subplot(2,1,2);
hold on; grid on;
plot(t_vec, V_wind, 'k-', 'LineWidth', 1.5, 'DisplayName', '风速');
xlabel('时间 [s]'); ylabel('风速 [m/s]');
title('风速扰动');
legend('Location', 'best');
xlim([25 80]);

saveas(gcf, 'fig1_pitch_tracking.png');

%% ========== 图2：同步误差对比 ==========
figure('Name', '同步误差对比', 'Position', [100 100 1000 400]);
hold on; grid on;
for c = 1:n_ctrl
    plot(t_vec, results(c).sync_err, [colors{c}, line_styles{c}], 'LineWidth', 1.5, ...
        'DisplayName', results(c).name);
end
xlabel('时间 [s]'); ylabel('同步误差 [°]');
title('双电机同步误差对比');
legend('Location', 'best');
xlim([25 80]);
saveas(gcf, 'fig2_sync_error.png');

%% ========== 图3：电磁转矩对比 ==========
figure('Name', '电磁转矩对比', 'Position', [100 100 1200 600]);
for c = 1:n_ctrl
    subplot(n_ctrl, 1, c);
    hold on; grid on;
    plot(t_vec, results(c).Te(1,:), 'b-', 'LineWidth', 1, 'DisplayName', 'T_{e1}');
    plot(t_vec, results(c).Te(2,:), 'r--', 'LineWidth', 1, 'DisplayName', 'T_{e2}');
    xlabel('时间 [s]'); ylabel('转矩 [N·m]');
    title([results(c).name, ' 电磁转矩']);
    legend('Location', 'best');
    xlim([25 80]);
end
saveas(gcf, 'fig3_torque.png');

%% ========== 图4：控制量对比 ==========
figure('Name', '控制量对比', 'Position', [100 100 1200 600]);
for c = 1:n_ctrl
    subplot(n_ctrl, 1, c);
    hold on; grid on;
    plot(t_vec, results(c).u(2,:), 'b-', 'LineWidth', 1, 'DisplayName', 'V_{q1}');
    plot(t_vec, results(c).u(4,:), 'r--', 'LineWidth', 1, 'DisplayName', 'V_{q2}');
    xlabel('时间 [s]'); ylabel('电压 [V]');
    title([results(c).name, ' 控制电压']);
    legend('Location', 'best');
    xlim([25 80]);
end
saveas(gcf, 'fig4_control.png');

%% ========== 图5：性能指标柱状图 ==========
figure('Name', '性能指标对比', 'Position', [100 100 800 400]);

metrics_names = {'上升时间', '超调量', '调节时间', '同步误差'};
metrics_data = zeros(n_ctrl, 4);
for c = 1:n_ctrl
    if isfield(results(c), 'metrics') && ~isempty(results(c).metrics)
        m = results(c).metrics;
        metrics_data(c, 1) = m.t_rise;
        metrics_data(c, 2) = m.overshoot;
        metrics_data(c, 3) = m.t_settle;
        metrics_data(c, 4) = m.sync_err;
    end
end

for i = 1:4
    subplot(1, 4, i);
    bar(metrics_data(:, i));
    set(gca, 'XTickLabel', {results.name});
    ylabel(metrics_names{i});
    title(metrics_names{i});
    grid on;
end
saveas(gcf, 'fig5_metrics.png');

%% ========== 图6：状态轨迹 ==========
figure('Name', '状态轨迹', 'Position', [100 100 1200 800]);

state_names = {'i_{d1} [A]', 'i_{q1} [A]', '\omega_1 [rad/s]', '\theta_1 [rad]', ...
               'i_{d2} [A]', 'i_{q2} [A]', '\omega_2 [rad/s]', '\theta_2 [rad]'};

for s = 1:8
    subplot(2, 4, s);
    hold on; grid on;
    for c = 1:n_ctrl
        plot(t_vec, results(c).x(s,:), [colors{c}, line_styles{c}], 'LineWidth', 1, ...
            'DisplayName', results(c).name);
    end
    xlabel('时间 [s]'); ylabel(state_names{s});
    title(state_names{s});
    if s == 1, legend('Location', 'best'); end
    xlim([25 80]);
end
saveas(gcf, 'fig6_states.png');

fprintf('✅ 6张对比图已保存！\n');
end
