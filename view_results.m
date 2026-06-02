%% 查看结果
load('D:\mpc控制变桨系统\simulink_pitch\comparison_results.mat', '-mat');

fprintf('==================== 仿真结果 ====================\n\n');

for c = 1:length(results)
    fprintf('【%s】\n', results(c).name);
    fprintf('  最终桨距角: %.4f deg\n', results(c).beta(end));
    fprintf('  最终同步误差: %.6f deg\n', results(c).sync_err(end));
    fprintf('  最终风速: %.1f m/s\n', results(c).V_wind(end));

    % 性能指标
    t = results(c).t;
    beta = results(c).beta;
    idx = t >= 30 & t <= 100;
    beta_step = beta(idx);

    % 上升时间
    beta_final = mean(beta_step(end-500:end));
    beta_10 = 0.1 * beta_final;
    beta_90 = 0.9 * beta_final;
    idx_10 = find(beta_step >= beta_10, 1);
    idx_90 = find(beta_step >= beta_90, 1);
    if isempty(idx_10), idx_10 = 1; end
    if isempty(idx_90), idx_90 = length(beta_step); end
    t_rise = t(idx_90) - t(idx_10);

    % 超调
    beta_max = max(beta_step);
    overshoot = (beta_max - beta_final) / beta_final * 100;
    if overshoot < 0, overshoot = 0; end

    % 稳态误差
    idx_ss = t >= 90;
    ss_error = mean(abs(beta(idx_ss) - 15));

    fprintf('  上升时间: %.3f s\n', t_rise);
    fprintf('  超调量: %.2f %%\n', overshoot);
    fprintf('  稳态误差: %.6f deg\n', ss_error);
    fprintf('\n');
end

fprintf('==================== 绘图 ====================\n');
plot_comparison(results, t_vec, V_wind, beta_ref_sim);
