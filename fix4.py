# -*- coding: utf-8 -*-
with open(r'D:/mpc控制变桨系统/simulink_pitch/tune_mpc.m', 'rb') as f:
    content = f.read()

old = b"    K_mpc = (H1 \\ (Theta1' * Q_bar * Theta1"
new = b"    K_mpc = (H1 \\ (Theta1' * Q_bar * Psi"
print('found:', old in content)
content = content.replace(old, new, 1)
with open(r'D:/mpc控制变桨系统/simulink_pitch/tune_mpc.m', 'wb') as f:
    f.write(content)
print('Done!')
