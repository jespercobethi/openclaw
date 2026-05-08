import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
import os

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'STSong']
plt.rcParams['axes.unicode_minus'] = False

out_dir = r'C:\Users\xuan1\.openclaw\workspace\main\figures'
os.makedirs(out_dir, exist_ok=True)

def draw_box(ax, x, y, w, h, text, color='#4A90D9', text_color='white', fontsize=10):
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05", 
                          facecolor=color, edgecolor='#333333', linewidth=1.5)
    ax.add_patch(box)
    ax.text(x + w/2, y + h/2, text, ha='center', va='center', 
            fontsize=fontsize, color=text_color, fontweight='bold')

def draw_arrow(ax, x1, y1, x2, y2, color='#333333'):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=1.5))

# ==================== 图1: 双驱变桨系统结构图 ====================
fig, ax = plt.subplots(1, 1, figsize=(12, 8))
ax.set_xlim(0, 12)
ax.set_ylim(0, 8)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title('图1  双驱变桨系统结构示意图', fontsize=14, fontweight='bold', pad=20)

# 叶片（大矩形）
blade = FancyBboxPatch((7, 2), 4, 4, boxstyle="round,pad=0.1",
                         facecolor='#E8F4FD', edgecolor='#2C3E50', linewidth=2)
ax.add_patch(blade)
ax.text(9, 4, '叶片', ha='center', va='center', fontsize=14, fontweight='bold', color='#2C3E50')

# 变桨机构
pitch = FancyBboxPatch((5.5, 3), 1.2, 2, boxstyle="round,pad=0.05",
                         facecolor='#F39C12', edgecolor='#E67E22', linewidth=1.5)
ax.add_patch(pitch)
ax.text(6.1, 4, '变桨\n机构', ha='center', va='center', fontsize=9, fontweight='bold', color='white')

# 减速齿轮箱1
gear1 = FancyBboxPatch((3.5, 4.5), 1.5, 1, boxstyle="round,pad=0.05",
                         facecolor='#27AE60', edgecolor='#1E8449', linewidth=1.5)
ax.add_patch(gear1)
ax.text(4.25, 5, '减速齿轮箱1', ha='center', va='center', fontsize=8, fontweight='bold', color='white')

# 减速齿轮箱2
gear2 = FancyBboxPatch((3.5, 2.5), 1.5, 1, boxstyle="round,pad=0.05",
                         facecolor='#27AE60', edgecolor='#1E8449', linewidth=1.5)
ax.add_patch(gear2)
ax.text(4.25, 3, '减速齿轮箱2', ha='center', va='center', fontsize=8, fontweight='bold', color='white')

# 电机1
motor1 = FancyBboxPatch((1, 4.5), 2, 1, boxstyle="round,pad=0.05",
                          facecolor='#4A90D9', edgecolor='#2C5F8A', linewidth=1.5)
ax.add_patch(motor1)
ax.text(2, 5, 'PMSM 电机1', ha='center', va='center', fontsize=9, fontweight='bold', color='white')

# 电机2
motor2 = FancyBboxPatch((1, 2.5), 2, 1, boxstyle="round,pad=0.05",
                          facecolor='#4A90D9', edgecolor='#2C5F8A', linewidth=1.5)
ax.add_patch(motor2)
ax.text(2, 3, 'PMSM 电机2', ha='center', va='center', fontsize=9, fontweight='bold', color='white')

# 箭头
draw_arrow(ax, 3, 5, 3.5, 5)
draw_arrow(ax, 3, 3, 3.5, 3)
draw_arrow(ax, 5, 5, 5.5, 4.2)
draw_arrow(ax, 5, 3, 5.5, 3.8)
draw_arrow(ax, 6.7, 4, 7, 4)

# 标注
ax.text(2, 6, '双驱驱动单元', ha='center', va='center', fontsize=11, 
        fontweight='bold', color='#E74C3C',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#FDEDEC', edgecolor='#E74C3C'))

# 说明文字
ax.text(9, 1, '每片叶片由2台PMSM协同驱动\n通过减速齿轮箱传动至变桨机构\n实现力矩均分与冗余备份',
        ha='center', va='center', fontsize=10, style='italic',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#FEF9E7', edgecolor='#F39C12'))

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

# 第一层：文献调研
draw_box(ax, 4, 8.5, 4, 0.8, '文献调研与理论学习', '#3498DB')

# 第二层：建模
draw_box(ax, 0.5, 6.8, 3, 0.8, 'PMSM电机建模', '#2ECC71')
draw_box(ax, 4.5, 6.8, 3, 0.8, '双电机耦合建模', '#2ECC71')
draw_box(ax, 8.5, 6.8, 3, 0.8, '风速模型建立', '#2ECC71')

# 第三层：控制器设计
draw_box(ax, 1.5, 5, 3.5, 0.8, 'MPC变桨控制器设计', '#E74C3C')
draw_box(ax, 7, 5, 3.5, 0.8, '多层次协同控制策略', '#E74C3C')

# 第四层：前馈
draw_box(ax, 3.5, 3.2, 5, 0.8, 'LSTM风速预测前馈设计', '#9B59B6')

# 第五层：仿真
draw_box(ax, 1, 1.5, 4.5, 0.8, '仿真平台搭建与验证', '#F39C12')
draw_box(ax, 6.5, 1.5, 4.5, 0.8, '对比分析与论文撰写', '#F39C12')

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
ax.text(0.3, 8.5, '第一阶段\n(6-8月)', fontsize=8, color='#7F8C8D', va='center')
ax.text(0.3, 6.8, '第二阶段\n(9-11月)', fontsize=8, color='#7F8C8D', va='center')
ax.text(0.3, 5, '第三阶段\n(12-2月)', fontsize=8, color='#7F8C8D', va='center')
ax.text(0.3, 3.2, '第三阶段\n(12-2月)', fontsize=8, color='#7F8C8D', va='center')
ax.text(0.3, 1.5, '第四阶段\n(3-6月)', fontsize=8, color='#7F8C8D', va='center')

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

# 风速预测模块（左侧）
draw_box(ax, 0.3, 6.5, 2.5, 1, 'LSTM\n风速预测', '#9B59B6', fontsize=10)
ax.text(1.55, 7.8, '前馈通道', ha='center', fontsize=8, color='#9B59B6')

# MPC控制器（核心）
draw_box(ax, 3.5, 4.5, 3.5, 3, 'MPC 控制器\n\n• 桨距角跟踪\n• 叶片内同步\n• 叶片间协调\n• 约束优化', '#E74C3C', fontsize=10)

# 参考输入
draw_box(ax, 3.5, 8, 3.5, 0.7, '桨距角参考 θref', '#3498DB')

# 叶片内同步层
draw_box(ax, 8.5, 6, 2, 1.5, '叶片1\n偏差耦合同步', '#2ECC71', fontsize=9)
draw_box(ax, 8.5, 3.8, 2, 1.5, '叶片2\n偏差耦合同步', '#2ECC71', fontsize=9)
draw_box(ax, 8.5, 1.5, 2, 1.5, '叶片3\n偏差耦合同步', '#2ECC71', fontsize=9)

# 电机
draw_box(ax, 11.5, 6.8, 1.8, 0.7, '电机1', '#4A90D9', fontsize=9)
draw_box(ax, 11.5, 5.5, 1.8, 0.7, '电机2', '#4A90D9', fontsize=9)
draw_box(ax, 11.5, 4.5, 1.8, 0.7, '电机3', '#4A90D9', fontsize=9)
draw_box(ax, 11.5, 3.2, 1.8, 0.7, '电机4', '#4A90D9', fontsize=9)
draw_box(ax, 11.5, 2.2, 1.8, 0.7, '电机5', '#4A90D9', fontsize=9)
draw_box(ax, 11.5, 1.0, 1.8, 0.7, '电机6', '#4A90D9', fontsize=9)

# 被控对象
draw_box(ax, 8.5, 0.2, 5, 0.8, '双驱变桨系统（3叶片×2电机=6电机）', '#F39C12', fontsize=9)

# 反馈
ax.annotate('', xy=(7, 4.8), xytext=(8.5, 0.6),
            arrowprops=dict(arrowstyle='->', color='#E74C3C', lw=1.5, linestyle='dashed'))
ax.text(7.5, 2.5, '状态反馈', ha='center', fontsize=8, color='#E74C3C', rotation=90)

# 箭头连接
draw_arrow(ax, 2.8, 7, 3.5, 6.5)  # 风速预测→MPC
draw_arrow(ax, 5.25, 8, 5.25, 7.5)  # 参考→MPC
draw_arrow(ax, 7, 6, 8.5, 6.75)  # MPC→叶片1
draw_arrow(ax, 7, 5.5, 8.5, 4.55)  # MPC→叶片2
draw_arrow(ax, 7, 5, 8.5, 2.25)  # MPC→叶片3
draw_arrow(ax, 10.5, 7.2, 11.5, 7.15)  # 叶片1→电机1
draw_arrow(ax, 10.5, 6.5, 11.5, 5.85)  # 叶片1→电机2
draw_arrow(ax, 10.5, 5, 11.5, 4.85)  # 叶片2→电机3
draw_arrow(ax, 10.5, 4.3, 11.5, 3.55)  # 叶片2→电机4
draw_arrow(ax, 10.5, 2.7, 11.5, 2.55)  # 叶片3→电机5
draw_arrow(ax, 10.5, 2, 11.5, 1.35)  # 叶片3→电机6

# 层级标注
ax.text(8.5, 8.2, '风轮层级（叶片间协调）', ha='center', fontsize=9, 
        color='#2C3E50', fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.2', facecolor='#EBF5FB', edgecolor='#3498DB'))
ax.text(12.4, 8.2, '叶片层级\n（叶片内同步）', ha='center', fontsize=8, 
        color='#27AE60', fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.2', facecolor='#EAFAF1', edgecolor='#27AE60'))

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

# 流程步骤
steps = [
    (3.5, 9, 3, 0.7, '采集当前状态 x(k)', '#3498DB'),
    (3.5, 7.8, 3, 0.7, '读取风速预测值', '#9B59B6'),
    (3.5, 6.6, 3, 0.7, '构建预测模型\nx(k+i|k) = f(x(k), u)', '#2ECC71'),
    (3.5, 5.2, 3, 0.9, '设定优化目标函数\nJ = 跟踪误差 + 同步误差\n    + 控制量变化率', '#E67E22'),
    (3.5, 3.8, 3, 0.9, '施加约束条件\n• 力矩约束  • 转速约束\n• 角速率约束  • 桨距角范围', '#E74C3C'),
    (3.5, 2.5, 3, 0.7, '求解二次规划(QP)\n获得最优控制序列 u*', '#8E44AD'),
    (3.5, 1.2, 3, 0.7, '执行第一步控制 u*(k)\n输出至变桨电机', '#2C3E50'),
]

for x, y, w, h, text, color in steps:
    draw_box(ax, x, y, w, h, text, color, fontsize=10)

# 箭头
for i in range(len(steps)-1):
    draw_arrow(ax, 5, steps[i][1], 5, steps[i+1][1] + steps[i+1][3])

# 反馈回路
ax.annotate('', xy=(7.5, 9.35), xytext=(7.5, 1.2),
            arrowprops=dict(arrowstyle='->', color='#E74C3C', lw=2, linestyle='dashed',
                           connectionstyle='arc3,rad=-0.5'))
ax.text(8.5, 5.5, '滚动\n优化\nk=k+1', ha='center', fontsize=9, color='#E74C3C', fontweight='bold')

plt.tight_layout()
plt.savefig(os.path.join(out_dir, '图4_MPC控制算法流程图.png'), dpi=200, bbox_inches='tight')
plt.close()
print('图4 done')

# ==================== 图5: 仿真结果对比图（示意图） ====================
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.suptitle('图5  仿真结果对比示意图（待补充实际仿真数据）', fontsize=14, fontweight='bold')

t = np.linspace(0, 10, 500)

# 图a: 桨距角跟踪
ax1 = axes[0]
ref = 15 + 5 * np.sin(0.5 * t)
mpc = ref + 0.3 * np.random.randn(len(t))
adrc = ref + 0.8 * np.random.randn(len(t))
pid = ref + 1.5 * np.random.randn(len(t))
ax1.plot(t, ref, 'k--', linewidth=2, label='参考值')
ax1.plot(t, mpc, 'r-', linewidth=1.2, label='MPC(本文)')
ax1.plot(t, adrc, 'b-', linewidth=1, alpha=0.7, label='ADRC')
ax1.plot(t, pid, 'g-', linewidth=1, alpha=0.7, label='PID')
ax1.set_xlabel('时间/s')
ax1.set_ylabel('桨距角/°')
ax1.set_title('(a) 桨距角跟踪对比')
ax1.legend(fontsize=8)
ax1.grid(True, alpha=0.3)

# 图b: 同步误差
ax2 = axes[1]
mpc_sync = 0.2 * np.exp(-0.5 * t) * np.abs(np.sin(t)) + 0.05 * np.random.randn(len(t))
adrc_sync = 0.5 * np.exp(-0.3 * t) * np.abs(np.sin(t)) + 0.1 * np.random.randn(len(t))
pid_sync = 1.0 * np.exp(-0.2 * t) * np.abs(np.sin(t)) + 0.2 * np.random.randn(len(t))
ax2.plot(t, np.abs(mpc_sync), 'r-', linewidth=1.2, label='MPC(本文)')
ax2.plot(t, np.abs(adrc_sync), 'b-', linewidth=1, alpha=0.7, label='ADRC')
ax2.plot(t, np.abs(pid_sync), 'g-', linewidth=1, alpha=0.7, label='PID')
ax2.set_xlabel('时间/s')
ax2.set_ylabel('同步误差/°')
ax2.set_title('(b) 叶片内双电机同步误差')
ax2.legend(fontsize=8)
ax2.grid(True, alpha=0.3)

# 图c: 功率波动
ax3 = axes[2]
mpc_power = 100 + 0.5 * np.random.randn(len(t))
adrc_power = 100 + 1.2 * np.random.randn(len(t))
pid_power = 100 + 2.5 * np.random.randn(len(t))
ax3.plot(t, mpc_power, 'r-', linewidth=1, label='MPC(本文)')
ax3.plot(t, adrc_power, 'b-', linewidth=0.8, alpha=0.7, label='ADRC')
ax3.plot(t, pid_power, 'g-', linewidth=0.8, alpha=0.7, label='PID')
ax3.set_xlabel('时间/s')
ax3.set_ylabel('输出功率/kW')
ax3.set_title('(c) 输出功率波动对比')
ax3.legend(fontsize=8)
ax3.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(out_dir, '图5_仿真结果对比图.png'), dpi=200, bbox_inches='tight')
plt.close()
print('图5 done')

# ==================== 图6: 双驱变桨系统层级控制架构图 ====================
fig, ax = plt.subplots(1, 1, figsize=(13, 8))
ax.set_xlim(0, 13)
ax.set_ylim(0, 8)
ax.axis('off')
ax.set_title('图6  双驱变桨系统多层次协同控制架构', fontsize=14, fontweight='bold', pad=20)

# 风轮层级框
wind_layer = FancyBboxPatch((0.5, 4.5), 12, 3, boxstyle="round,pad=0.1",
                              facecolor='#EBF5FB', edgecolor='#3498DB', linewidth=2, linestyle='--')
ax.add_patch(wind_layer)
ax.text(6.5, 7.2, '风轮层级 — 叶片间桨距角协调', ha='center', fontsize=12, 
        fontweight='bold', color='#2980B9')

# 叶片层级框
blade_layer = FancyBboxPatch((0.5, 0.5), 12, 3.5, boxstyle="round,pad=0.1",
                               facecolor='#EAFAF1', edgecolor='#27AE60', linewidth=2, linestyle='--')
ax.add_patch(blade_layer)
ax.text(6.5, 3.7, '叶片层级 — 叶片内双电机力矩同步', ha='center', fontsize=12, 
        fontweight='bold', color='#1E8449')

# 风轮层级组件
draw_box(ax, 1, 5.5, 2.5, 1, 'MPC优化器\n（叶片间协调）', '#E74C3C', fontsize=9)
draw_box(ax, 4.5, 5.5, 2, 1, '桨距角\n协调模块', '#F39C12', fontsize=9)
draw_box(ax, 7.5, 5.5, 2, 1, '载荷均衡\n模块', '#F39C12', fontsize=9)
draw_box(ax, 10.5, 5.5, 2, 1, '故障降级\n模块', '#E74C3C', fontsize=9)

# 叶片层级组件
draw_box(ax, 1, 1.2, 2.5, 1.5, '叶片1\n偏差耦合\n同步控制器', '#2ECC71', fontsize=9)
draw_box(ax, 5, 1.2, 2.5, 1.5, '叶片2\n偏差耦合\n同步控制器', '#2ECC71', fontsize=9)
draw_box(ax, 9, 1.2, 2.5, 1.5, '叶片3\n偏差耦合\n同步控制器', '#2ECC71', fontsize=9)

# 每个叶片内的2台电机小框
for bx in [1, 5, 9]:
    draw_box(ax, bx, 0.5, 1.1, 0.5, '电机A', '#4A90D9', fontsize=7)
    draw_box(ax, bx+1.3, 0.5, 1.1, 0.5, '电机B', '#4A90D9', fontsize=7)

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

# ==================== 图7: 叶片内双电机耦合动力学模型示意图 ====================
fig, ax = plt.subplots(1, 1, figsize=(13, 7))
ax.set_xlim(0, 13)
ax.set_ylim(0, 7)
ax.axis('off')
ax.set_title('图7  叶片内双电机耦合动力学模型示意图', fontsize=14, fontweight='bold', pad=20)

# 电机1
m1 = FancyBboxPatch((0.5, 4), 2.5, 2, boxstyle="round,pad=0.1",
                      facecolor='#4A90D9', edgecolor='#2C5F8A', linewidth=2)
ax.add_patch(m1)
ax.text(1.75, 5.3, 'PMSM 电机1', ha='center', va='center', fontsize=10, fontweight='bold', color='white')
ax.text(1.75, 4.5, 'id1, iq1, ωm1, θ1', ha='center', va='center', fontsize=8, color='#E8F4FD')

# 电机2
m2 = FancyBboxPatch((0.5, 1), 2.5, 2, boxstyle="round,pad=0.1",
                      facecolor='#4A90D9', edgecolor='#2C5F8A', linewidth=2)
ax.add_patch(m2)
ax.text(1.75, 2.3, 'PMSM 电机2', ha='center', va='center', fontsize=10, fontweight='bold', color='white')
ax.text(1.75, 1.5, 'id2, iq2, ωm2, θ2', ha='center', va='center', fontsize=8, color='#E8F4FD')

# 减速齿轮箱1
g1 = FancyBboxPatch((4, 4.5), 2, 1.2, boxstyle="round,pad=0.05",
                      facecolor='#27AE60', edgecolor='#1E8449', linewidth=1.5)
ax.add_patch(g1)
ax.text(5, 5.1, '减速齿轮箱1', ha='center', va='center', fontsize=9, fontweight='bold', color='white')
ax.text(5, 4.8, '传动比 i1, 效率 η1', ha='center', va='center', fontsize=7, color='#EAFAF1')

# 减速齿轮箱2
g2 = FancyBboxPatch((4, 1.3), 2, 1.2, boxstyle="round,pad=0.05",
                      facecolor='#27AE60', edgecolor='#1E8449', linewidth=1.5)
ax.add_patch(g2)
ax.text(5, 1.9, '减速齿轮箱2', ha='center', va='center', fontsize=9, fontweight='bold', color='white')
ax.text(5, 1.6, '传动比 i2, 效率 η2', ha='center', va='center', fontsize=7, color='#EAFAF1')

# 变桨机构（耦合点）
coupling = FancyBboxPatch((7, 2.5), 2.5, 2, boxstyle="round,pad=0.1",
                           facecolor='#F39C12', edgecolor='#E67E22', linewidth=2)
ax.add_patch(coupling)
ax.text(8.25, 4, '变桨机构', ha='center', va='center', fontsize=11, fontweight='bold', color='white')
ax.text(8.25, 3.3, '（机械耦合点）', ha='center', va='center', fontsize=9, color='#FEF9E7')
ax.text(8.25, 2.9, 'θpitch = f(θ1, θ2)', ha='center', va='center', fontsize=8, color='#FEF9E7')

# 叶片
blade = FancyBboxPatch((10.5, 2), 2, 3, boxstyle="round,pad=0.1",
                         facecolor='#E8F4FD', edgecolor='#2C3E50', linewidth=2)
ax.add_patch(blade)
ax.text(11.5, 3.5, '叶片', ha='center', va='center', fontsize=12, fontweight='bold', color='#2C3E50')

# 风载荷
ax.annotate('', xy=(12, 3.5), xytext=(13, 3.5),
            arrowprops=dict(arrowstyle='->', color='#E74C3C', lw=3))
ax.text(12.8, 3.8, '风载荷\nTL', ha='center', fontsize=9, color='#E74C3C', fontweight='bold')

# 箭头
draw_arrow(ax, 3, 5, 4, 5.1)
draw_arrow(ax, 3, 2, 4, 1.9)
draw_arrow(ax, 6, 5.1, 7, 4)
draw_arrow(ax, 6, 1.9, 7, 3)
draw_arrow(ax, 9.5, 3.5, 10.5, 3.5)

# 公式标注
ax.text(6.5, 6.3, '耦合关系:', fontsize=10, fontweight='bold', color='#2C3E50')
ax.text(6.5, 5.9, 'θpitch = (θ1/i1 + θ2/i2) / 2', fontsize=9, color='#E74C3C',
        bbox=dict(boxstyle='round,pad=0.2', facecolor='#FDEDEC', edgecolor='#E74C3C'))

plt.tight_layout()
plt.savefig(os.path.join(out_dir, '图7_双电机耦合动力学模型.png'), dpi=200, bbox_inches='tight')
plt.close()
print('图7 done')

print('\nAll 7 figures generated successfully!')
print(f'Output directory: {out_dir}')
