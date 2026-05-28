# 双驱变桨伺服系统 Simulink 仿真模型

## 📁 文件结构

```
simulink_pitch/
├── setup_params.m           ← 参数定义（先运行这个）
│
│  ── 开环模型 ──
├── dual_motor_sfun.m        ← 双电机 S-Function（8状态非线性）
├── blade_sfun.m             ← 叶片动力学 S-Function
├── calc_gear_load.m         ← 齿轮弹性负载计算
├── calc_aero_torque.m       ← 气动转矩计算
├── wind_model.m             ← 风速模型（平均+阵风）
├── build_simulink_model.m   ← 搭建开环 Simulink 模型
│
│  ── MPC 控制器 ──
├── mpc_controller.m         ← MPC 算法核心（线性化+离散化+QP）
├── mpc_sfun.m               ← MPC S-Function（供 Simulink 调用）
├── build_closed_loop.m      ← 搭建闭环 Simulink 模型
│
│  ── 对比控制器 ──
├── pid_sfun.m               ← PID + 偏差耦合同步
├── adrc_sfun.m              ← ADRC（TD+ESO+NLSEF + 偏差耦合）
│
│  ── 仿真与分析 ──
├── run_comparison.m         ← 三种控制器对比仿真
├── plot_comparison.m        ← 绘制对比图（6张）
├── tune_mpc.m               ← MPC 参数调优（扫描 Np/Nc/Q/R）
└── README.md
```

## 🚀 使用步骤

### 1. 开环仿真
```matlab
cd simulink_pitch
setup_params
build_simulink_model
sim('dual_motor_pitch_openloop')
```

### 2. 闭环仿真（MPC 控制）
```matlab
cd simulink_pitch
setup_params
mpc_controller
build_closed_loop
sim('dual_motor_pitch_mpc')
```

### 3. 三种控制器对比
```matlab
cd simulink_pitch
run_comparison   % 自动运行 MPC/PID/ADRC + 画图 + 保存数据
```

### 4. MPC 参数调优
```matlab
cd simulink_pitch
tune_mpc   % 扫描 Np/Nc/Q/R 找最优参数
```

## 📊 输出文件

运行 `run_comparison.m` 后生成：
- `comparison_results.mat` — 完整时间序列数据
- `fig1_pitch_tracking.png` — 桨距角跟踪对比
- `fig2_sync_error.png` — 同步误差对比
- `fig3_torque.png` — 电磁转矩对比
- `fig4_control.png` — 控制量对比
- `fig5_metrics.png` — 性能指标柱状图
- `fig6_states.png` — 8个状态轨迹

运行 `tune_mpc.m` 后生成：
- `mpc_tuning_results.csv` — 参数扫描结果表

## 🎛️ 控制器对比

| 特性 | MPC | PID | ADRC |
|------|-----|-----|------|
| 预测能力 | ✅ 多步预测 | ❌ 无 | ❌ 无 |
| 约束处理 | ✅ 显式约束 | ❌ 限幅 | ❌ 限幅 |
| 同步控制 | ✅ 耦合MPC | ⚠️ 偏差耦合 | ⚠️ 偏差耦合 |
| 抗扰能力 | ✅ 前馈+反馈 | ⚠️ 反馈 | ✅ ESO估计 |
| 计算量 | 高（QP） | 低 | 中 |
| 调参难度 | 中 | 低 | 高 |

## ⚙️ 参数来源

| 参数 | 来源 |
|------|------|
| 电气参数 Rs, Ld, Lq, ψf | 李晓凤(2019) |
| 传动机构 i, kg, cg | 李奔(2026) |
| 气动参数 Cp(λ,β) | Heier模型 |
| ADRC 结构 | 王耀锋(2022) |

---
Ciallo～ (∠・ω< )⌒★
