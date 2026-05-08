import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
import os

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'STSong']
plt.rcParams['axes.unicode_minus'] = False

out_dir = r'C:\Users\xuan1\.openclaw\workspace\main\figures'
os.makedirs(out_dir, exist_ok=True)

# 黑白风格配色
WHITE = '#FFFFFF'
LIGHT_GRAY = '#E8E8E8'
MID_GRAY = '#C0C0C0'
DARK_GRAY = '#808080'
BLACK = '#000000'
HATCH_1 = '///'
HATCH_2 = '\\\\\\'
HATCH_3 = 'xxx'
HATCH_4 = '...'

def draw_box(ax, x, y, w, h, text, facecolor=WHITE, edgecolor=BLACK, fontsize=10, 
             hatch=None, linewidth=1.5, text_color=BLACK, bold=True):
    rect = plt.Rectangle((x, y), w, h, facecolor=facecolor, edgecolor=edgecolor, 
                          linewidth=linewidth, hatch=hatch)
    ax.add_patch(rect)
    weight = 'bold' if bold else 'normal'
    ax.text(x + w/2, y + h/2, text, ha='center', va='center', 
            fontsize=fontsize, color=text_color, fontweight=weight)

def draw_arrow(ax, x1, y1, x2, y2, color=BLACK, lw=1.5):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=lw))

def draw_dashed_arrow(ax, x1, y1, x2, y2, color=BLACK, lw=1.5):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=lw, linestyle='dashed'))

# ==================== 图1: 双驱变桨系统结构图 ====================
fig, ax = plt.subplots(1, 1, figsize=(12, 8))
ax.set_xlim(0, 12)
ax.set_ylim(0, 8)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title('图1  双驱变桨系统结构示意图', fontsize=14, fontweight='bold', pad=20)

# 叶片
blade = plt.Rectangle((7.2, 2), 3.8, 4, facecolor=LIGHT_GRAY, edgecolor=BLACK, 
                        linewidth=2, hatch=HATCH_1)
ax.add_patch(blade)
ax.text(9.1, 4, '叶片', ha='center', va='center', fontsize=14, fontweight='bold')

# 变桨机构
draw_box(ax, 5.5, 3, 1.3, 2, '变桨\n机构', facecolor=MID_GRAY, fontsize=10, linewidth=2)

# 减速齿轮箱1
draw_box(ax, 3.3, 4.5, 1.7, 1, '减速齿轮箱1', facecolor=LIGHT_GRAY, hatch=HATCH_2, fontsize=9)

# 减速齿轮箱2
draw_box(ax, 3.3, 2.5, 1.7, 1, '减速齿轮箱2', facecolor=LIGHT_GRAY, hatch=HATCH_2, fontsize=9)

# 电机1
draw_box(ax, 0.8, 4.5, 2.2, 1, 'PMSM 电机1', facecolor=WHITE, fontsize=10, linewidth=2)

# 电机2
draw_box(ax, 0.8, 2.5, 2.2, 1, 'PMSM 电机2', facecolor=WHITE, fontsize=10, linewidth=2)

# 箭头
draw_arrow(ax, 3, 5, 3.3, 5)
draw_arrow(ax, 3, 3, 3.3, 3)
draw_arrow(ax, 5, 5, 5.5, 4.2)
draw_arrow(ax, 5, 3, 5.5, 3.8)
draw_arrow(ax, 6.8, 4, 7.2, 4)

# 标注框
ax.text(2, 6.2, '双驱驱动单元', ha='center', va='center', fontsize=11, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.3', facecolor=WHITE, edgecolor=BLACK, linewidth=1.5))

# 说明
ax.text(9.1, 1, '每片叶片由2台PMSM协同驱动\n通过减速齿轮箱传动至变桨机构\n实现力矩均分与冗余备份',
        ha='center', va='center', fontsize=10, style='italic',
        bbox=dict(boxstyle='round,pad=0.3', facecolor=WHITE, edgecolor=DARK_GRAY, linewidth=1))

plt.tight_layout()
plt.savefig(os.path.join(out_dir, '图1_双驱变桨系统结构图.png'), dpi=200, bbox_inches='tight')
plt.close()
print('图1 done')

# ==================== 图2: 技术路线图 ====================
fig, ax = plt.subplots(1, 1, figsize=(12, 10))
ax.set_xlim(0, 12)
ax.set_ylim(0, 10)
ax.axis('off')
ax.set_title('图2  技术路线图', fontsize=14, fontweight='bold', pad=20)

# 第一层
draw_box(ax, 4, 8.5, 4, 0.8, '文献调研与理论学习', facecolor=WHITE, linewidth=2)

# 第二层
draw_box(ax, 0.5, 6.8, 3, 0.8, 'PMSM电机建模', facecolor=LIGHT_GRAY, hatch=HATCH_1)
draw_box(ax, 4.5, 6.8, 3, 0.8, '双电机耦合建模', facecolor=LIGHT_GRAY, hatch=HATCH_1)
draw_box(ax, 8.5, 6.8, 3, 0.8, '风速模型建立', facecolor=LIGHT_GRAY, hatch=HATCH_1)

# 第三层
draw_box(ax, 1.5, 5, 3.5, 0.8, 'MPC变桨控制器设计', facecolor=WHITE, linewidth=2)
draw_box(ax, 7, 5, 3.5, 0.8, '多层次协同控制策略', facecolor=WHITE, linewidth=2)

# 第四层
draw_box(ax, 3.5, 3.2, 5, 0.8, 'LSTM风速预测前馈设计', facecolor=MID_GRAY, hatch=HATCH_3)

# 第五层
draw_box(ax, 1, 1.5, 4.5, 0.8, '仿真平台搭建与验证', facecolor=LIGHT_GRAY, hatch=HATCH_4, linewidth=2)
draw_box(ax, 6.5, 1.5, 4.5, 0.8, '对比分析与论文撰写', facecolor=LIGHT_GRAY, hatch=HATCH_4, linewidth=2)

# 箭头
draw_arrow(ax, 6, 8.5, 2, 7.6)
draw_arrow(ax, 6, 8.5, 6, 7.6)
draw_arrow(ax, 6, 8.5, 10, 7.6)
draw_arrow(ax, 2, 6.8, 3.25, 5.8)
draw_arrow(ax, 6, 6.8, 8.75, 5.8)
draw_arrow(ax, 3.25, 5, 6, 4)
draw_arrow(ax, 8.75, 5, 6, 4)
draw_arrow(ax, 6, 3.2, 3.25, 2.3)
draw_arrow(ax, 6, 3.2, 8.75, 2.3)

# 阶段标注
for y, txt in [(8.5, '第一阶段(6-8月)'), (6.8, '第二阶段(9-11月)'), 
               (5, '第三阶段(12-2月)'), (3.2, '第三阶段(12-2月)'), (1.5, '第四阶段(3-6月)')]:
    ax.text(0.2, y, txt, fontsize=7, color=DARK_GRAY, va='center', style='italic')

plt.tight_layout()
plt.savefig(os.path.join(out_dir, '图2_技术路线图.png'), dpi=200, bbox_inches='tight')
plt.close()
print('图2 done')

# ==================== 图3: 多电机协同控制系统总体框图 ====================
fig, ax = plt.subplots(1, 1, figsize=(14, 9))
ax.set_xlim(0, 14)
ax.set_ylim(0, 9)
ax.axis('off')
ax.set_title('图3  双驱变桨多电机协同控制系统总体框图', fontsize=14, fontweight='bold', pad=20)

# 风速预测
draw_box(ax, 0.3, 6.5, 2.5, 1, 'LSTM\n风速预测', facecolor=LIGHT_GRAY, hatch=HATCH_3, fontsize=10)
ax.text(1.55, 7.8, '前馈通道', ha='center', fontsize=8, color=DARK_GRAY)

# MPC控制器
draw_box(ax, 3.5, 4.5, 3.5, 3, '', facecolor=WHITE, linewidth=2.5)
ax.text(5.25, 7, 'MPC 控制器', ha='center', va='center', fontsize=12, fontweight='bold')
ax.text(5.25, 6.3, '--- 目标函数 ---', ha='center', va='center', fontsize=8, color=DARK_GRAY)
ax.text(5.25, 5.7, '桨距角跟踪误差', ha='center', va='center', fontsize=9)
ax.text(5.25, 5.2, '叶片内同步误差', ha='center', va='center', fontsize=9)
ax.text(5.25, 4.7, '叶片间协调误差', ha='center', va='center', fontsize=9)

# 参考输入
draw_box(ax, 3.5, 8, 3.5, 0.7, '桨距角参考 θref', facecolor=WHITE, linewidth=1.5)

# 叶片层控制器
for i, (y, label) in enumerate([(6, '叶片1 偏差耦合同步'), 
                                  (3.8, '叶片2 偏差耦合同步'),
                                  (1.5, '叶片3 偏差耦合同步')]):
    draw_box(ax, 8.5, y, 2.2, 1.5, label, facecolor=LIGHT_GRAY, hatch=HATCH_1, fontsize=9)

# 电机
for y, label in [(6.8, '电机1'), (5.5, '电机2'), (4.5, '电机3'), 
                  (3.2, '电机4'), (2.2, '电机5'), (1.0, '电机6')]:
    draw_box(ax, 11.8, y, 1.6, 0.7, label, facecolor=WHITE, linewidth=1.5)

# 被控对象
draw_box(ax, 8.5, 0.1, 5, 0.7, '双驱变桨系统(3叶片×2电机=6电机)', facecolor=MID_GRAY, hatch=HATCH_4, fontsize=9)

# 反馈
ax.annotate('', xy=(7, 4.8), xytext=(8.5, 0.45),
            arrowprops=dict(arrowstyle='->', color=BLACK, lw=1.5, linestyle='dashed'))
ax.text(7.3, 2.5, '状\n态\n反\n馈', ha='center', va='center', fontsize=8, color=DARK_GRAY)

# 连接箭头
draw_arrow(ax, 2.8, 7, 3.5, 6.5)
draw_arrow(ax, 5.25, 8, 5.25, 7.5)
draw_arrow(ax, 7, 6, 8.5, 6.75)
draw_arrow(ax, 7, 5.5, 8.5, 4.55)
draw_arrow(ax, 7, 5, 8.5, 2.25)
draw_arrow(ax, 10.7, 7.2, 11.8, 7.15)
draw_arrow(ax, 10.7, 6.5, 11.8, 5.85)
draw_arrow(ax, 10.7, 5, 11.8, 4.85)
draw_arrow(ax, 10.7, 4.3, 11.8, 3.55)
draw_arrow(ax, 10.7, 2.7, 11.8, 2.55)
draw_arrow(ax, 10.7, 2, 11.8, 1.35)

# 层级标注
ax.text(9.6, 8.5, '风轮层级(叶片间协调)', ha='center', fontsize=9, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.2', facecolor=WHITE, edgecolor=BLACK, linewidth=1))
ax.text(12.6, 8.5, '叶片层级\n(叶片内同步)', ha='center', fontsize=8, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.2', facecolor=LIGHT_GRAY, edgecolor=BLACK, linewidth=1))

plt.tight_layout()
plt.savefig(os.path.join(out_dir, '图3_多电机协同控制系统总体框图.png'), dpi=200, bbox_inches='tight')
plt.close()
print('图3 done')

# ==================== 图4: MPC控制算法流程图 ====================
fig, ax = plt.subplots(1, 1, figsize=(10, 10))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')
ax.set_title('图4  MPC控制算法流程图', fontsize=14, fontweight='bold', pad=20)

steps = [
    (3.5, 9, 3, 0.7, '采集当前状态 x(k)', WHITE, None),
    (3.5, 7.8, 3, 0.7, '读取风速预测值', LIGHT_GRAY, HATCH_3),
    (3.5, 6.6, 3, 0.7, '构建预测模型', WHITE, HATCH_1),
    (3.5, 5.2, 3, 0.9, '设定优化目标函数\nJ = 跟踪误差 + 同步误差\n    + 控制量变化率', LIGHT_GRAY, None),
    (3.5, 3.8, 3, 0.9, '施加约束条件\n力矩/转速/角速率/桨距角', WHITE, HATCH_2),
    (3.5, 2.5, 3, 0.7, '求解QP问题\n获得最优控制序列 u*', MID_GRAY, HATCH_4),
    (3.5, 1.2, 3, 0.7, '执行第一步控制 u*(k)', WHITE, None),
]

for x, y, w, ht, text, fc, hatch in steps:
    draw_box(ax, x, y, w, ht, text, facecolor=fc, hatch=hatch, fontsize=10, linewidth=1.5)

for i in range(len(steps)-1):
    draw_arrow(ax, 5, steps[i][1], 5, steps[i+1][1] + steps[i+1][3])

# 反馈回路
ax.annotate('', xy=(7.5, 9.35), xytext=(7.5, 1.2),
            arrowprops=dict(arrowstyle='->', color=BLACK, lw=2, linestyle='dashed',
                           connectionstyle='arc3,rad=-0.5'))
ax.text(8.8, 5.5, '滚动\n优化\nk=k+1', ha='center', fontsize=9, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.2', facecolor=WHITE, edgecolor=BLACK, linewidth=1))

plt.tight_layout()
plt.savefig(os.path.join(out_dir, '图4_MPC控制算法流程图.png'), dpi=200, bbox_inches='tight')
plt.close()
print('图4 done')

# ==================== 图5: 仿真结果对比图 ====================
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.suptitle('图5  仿真结果对比图(示意图，待补充实际仿真数据)', fontsize=13, fontweight='bold')

t = np.linspace(0, 10, 500)
np.random.seed(42)

# (a)
ax1 = axes[0]
ref = 15 + 5 * np.sin(0.5 * t)
mpc = ref + 0.3 * np.random.randn(len(t))
adrc = ref + 0.8 * np.random.randn(len(t))
pid = ref + 1.5 * np.random.randn(len(t))
ax1.plot(t, ref, 'k--', linewidth=2, label='参考值')
ax1.plot(t, mpc, 'k-', linewidth=1.5, label='MPC(本文)')
ax1.plot(t, adrc, 'k-.', linewidth=1, alpha=0.7, label='ADRC')
ax1.plot(t, pid, 'k:', linewidth=1, alpha=0.7, label='PID')
ax1.set_xlabel('时间/s', fontsize=10)
ax1.set_ylabel('桨距角/°', fontsize=10)
ax1.set_title('(a) 桨距角跟踪对比', fontsize=11)
ax1.legend(fontsize=8, frameon=True, edgecolor=BLACK)
ax1.grid(True, alpha=0.3, linestyle='-')

# (b)
ax2 = axes[1]
mpc_sync = 0.2 * np.exp(-0.5 * t) * np.abs(np.sin(t)) + 0.05 * np.abs(np.random.randn(len(t)))
adrc_sync = 0.5 * np.exp(-0.3 * t) * np.abs(np.sin(t)) + 0.1 * np.abs(np.random.randn(len(t)))
pid_sync = 1.0 * np.exp(-0.2 * t) * np.abs(np.sin(t)) + 0.2 * np.abs(np.random.randn(len(t)))
ax2.plot(t, mpc_sync, 'k-', linewidth=1.5, label='MPC(本文)')
ax2.plot(t, adrc_sync, 'k-.', linewidth=1, alpha=0.7, label='ADRC')
ax2.plot(t, pid_sync, 'k:', linewidth=1, alpha=0.7, label='PID')
ax2.set_xlabel('时间/s', fontsize=10)
ax2.set_ylabel('同步误差/°', fontsize=10)
ax2.set_title('(b) 叶片内双电机同步误差', fontsize=11)
ax2.legend(fontsize=8, frameon=True, edgecolor=BLACK)
ax2.grid(True, alpha=0.3, linestyle='-')

# (c)
ax3 = axes[2]
mpc_power = 100 + 0.5 * np.random.randn(len(t))
adrc_power = 100 + 1.2 * np.random.randn(len(t))
pid_power = 100 + 2.5 * np.random.randn(len(t))
ax3.plot(t, mpc_power, 'k-', linewidth=1.2, label='MPC(本文)')
ax3.plot(t, adrc_power, 'k-.', linewidth=0.8, alpha=0.7, label='ADRC')
ax3.plot(t, pid_power, 'k:', linewidth=0.8, alpha=0.7, label='PID')
ax3.set_xlabel('时间/s', fontsize=10)
ax3.set_ylabel('输出功率/kW', fontsize=10)
ax3.set_title('(c) 输出功率波动对比', fontsize=11)
ax3.legend(fontsize=8, frameon=True, edgecolor=BLACK)
ax3.grid(True, alpha=0.3, linestyle='-')

for ax in axes:
    ax.spines['top'].set_linewidth(1.5)
    ax.spines['right'].set_linewidth(1.5)
    ax.spines['bottom'].set_linewidth(1.5)
    ax.spines['left'].set_linewidth(1.5)

plt.tight_layout()
plt.savefig(os.path.join(out_dir, '图5_仿真结果对比图.png'), dpi=200, bbox_inches='tight')
plt.close()
print('图5 done')

# ==================== 图6: 多层次协同控制架构图 ====================
fig, ax = plt.subplots(1, 1, figsize=(13, 8))
ax.set_xlim(0, 13)
ax.set_ylim(0, 8)
ax.axis('off')
ax.set_title('图6  双驱变桨系统多层次协同控制架构', fontsize=14, fontweight='bold', pad=20)

# 风轮层级框
wind_layer = plt.Rectangle((0.5, 4.5), 12, 3, facecolor=WHITE, edgecolor=BLACK, 
                              linewidth=2, linestyle='--')
ax.add_patch(wind_layer)
ax.text(6.5, 7.2, '风轮层级 — 叶片间桨距角协调', ha='center', fontsize=12, fontweight='bold')

# 叶片层级框
blade_layer = plt.Rectangle((0.5, 0.5), 12, 3.5, facecolor=LIGHT_GRAY, edgecolor=BLACK, 
                               linewidth=2, linestyle='--')
ax.add_patch(blade_layer)
ax.text(6.5, 3.7, '叶片层级 — 叶片内双电机力矩同步', ha='center', fontsize=12, fontweight='bold')

# 风轮层组件
draw_box(ax, 1, 5.5, 2.5, 1, 'MPC优化器\n(叶片间协调)', facecolor=WHITE, linewidth=2)
draw_box(ax, 4.5, 5.5, 2, 1, '桨距角\n协调模块', facecolor=LIGHT_GRAY, hatch=HATCH_1)
draw_box(ax, 7.5, 5.5, 2, 1, '载荷均衡\n模块', facecolor=LIGHT_GRAY, hatch=HATCH_2)
draw_box(ax, 10.5, 5.5, 2, 1, '故障降级\n模块', facecolor=MID_GRAY, hatch=HATCH_3)

# 叶片层组件
draw_box(ax, 1, 1.2, 2.5, 1.5, '叶片1\n偏差耦合同步控制器', facecolor=WHITE, fontsize=9, linewidth=1.5)
draw_box(ax, 5, 1.2, 2.5, 1.5, '叶片2\n偏差耦合同步控制器', facecolor=WHITE, fontsize=9, linewidth=1.5)
draw_box(ax, 9, 1.2, 2.5, 1.5, '叶片3\n偏差耦合同步控制器', facecolor=WHITE, fontsize=9, linewidth=1.5)

# 电机
for bx in [1, 5, 9]:
    draw_box(ax, bx, 0.5, 1.1, 0.5, '电机A', facecolor=LIGHT_GRAY, fontsize=7)
    draw_box(ax, bx+1.3, 0.5, 1.1, 0.5, '电机B', facecolor=LIGHT_GRAY, fontsize=7)

# 层间箭头
for bx in [2.25, 6.25, 10.25]:
    draw_arrow(ax, bx, 4.5, bx, 3)

# 风轮层内箭头
draw_arrow(ax, 3.5, 6, 4.5, 6)
draw_arrow(ax, 6.5, 6, 7.5, 6)
draw_arrow(ax, 9.5, 6, 10.5, 6)

plt.tight_layout()
plt.savefig(os.path.join(out_dir, '图6_多层次协同控制架构图.png'), dpi=200, bbox_inches='tight')
plt.close()
print('图6 done')

# ==================== 图7: 叶片内双电机耦合动力学模型 ====================
fig, ax = plt.subplots(1, 1, figsize=(13, 7))
ax.set_xlim(0, 13)
ax.set_ylim(0, 7)
ax.axis('off')
ax.set_title('图7  叶片内双电机耦合动力学模型示意图', fontsize=14, fontweight='bold', pad=20)

# 电机1
draw_box(ax, 0.5, 4, 2.5, 2, 'PMSM 电机1\n\nid1, iq1, ωm1, θ1', facecolor=WHITE, fontsize=10, linewidth=2)

# 电机2
draw_box(ax, 0.5, 1, 2.5, 2, 'PMSM 电机2\n\nid2, iq2, ωm2, θ2', facecolor=WHITE, fontsize=10, linewidth=2)

# 减速齿轮箱1
draw_box(ax, 4, 4.5, 2, 1.2, '减速齿轮箱1\n传动比i1, 效率η1', facecolor=LIGHT_GRAY, hatch=HATCH_2, fontsize=9)

# 减速齿轮箱2
draw_box(ax, 4, 1.3, 2, 1.2, '减速齿轮箱2\n传动比i2, 效率η2', facecolor=LIGHT_GRAY, hatch=HATCH_2, fontsize=9)

# 变桨机构
draw_box(ax, 7, 2.5, 2.5, 2, '变桨机构\n(机械耦合点)\n\nθpitch = f(θ1,θ2)', facecolor=MID_GRAY, hatch=HATCH_4, fontsize=10, linewidth=2)

# 叶片
blade = plt.Rectangle((10.5, 2), 2, 3, facecolor=LIGHT_GRAY, edgecolor=BLACK, 
                        linewidth=2, hatch=HATCH_1)
ax.add_patch(blade)
ax.text(11.5, 3.5, '叶片', ha='center', va='center', fontsize=12, fontweight='bold')

# 风载荷
ax.annotate('', xy=(12, 3.5), xytext=(13, 3.5),
            arrowprops=dict(arrowstyle='->', color=BLACK, lw=3))
ax.text(12.8, 3.8, '风载荷\nTL', ha='center', fontsize=9, fontweight='bold')

# 连接箭头
draw_arrow(ax, 3, 5, 4, 5.1)
draw_arrow(ax, 3, 2, 4, 1.9)
draw_arrow(ax, 6, 5.1, 7, 4)
draw_arrow(ax, 6, 1.9, 7, 3)
draw_arrow(ax, 9.5, 3.5, 10.5, 3.5)

# 公式
ax.text(6.5, 6.3, '耦合关系:', fontsize=10, fontweight='bold')
ax.text(6.5, 5.9, 'θpitch = (θ1/i1 + θ2/i2) / 2', fontsize=9,
        bbox=dict(boxstyle='round,pad=0.2', facecolor=WHITE, edgecolor=BLACK, linewidth=1))

plt.tight_layout()
plt.savefig(os.path.join(out_dir, '图7_双电机耦合动力学模型.png'), dpi=200, bbox_inches='tight')
plt.close()
print('图7 done')

print('\nAll 7 figures (academic B/W style) generated!')
