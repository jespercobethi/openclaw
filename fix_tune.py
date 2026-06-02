# -*- coding: utf-8 -*-
with open(r'D:/mpc控制变桨系统/simulink_pitch/tune_mpc.m', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: Psi construction
content = content.replace(
    'Psi(2*i-1:2*i, :) = C_mpc * A_power;',
    'Psi(2*i-1:2*i, :) = [C_mpc, zeros(2,2)] * A_power;'
)

# Fix 2: Theta construction
content = content.replace(
    'Theta(2*i-1:2*i, 4*j-3:4*j) = C_mpc * A_pow * B_aug;',
    'Theta(2*i-1:2*i, 4*j-3:4*j) = [C_mpc, zeros(2,2)] * A_pow * B_aug;'
)

# Fix 3: K_mpc computation
old_k = "    H_mpc = Theta' * Q_bar * Theta + R_bar;\n    H_mpc = (H_mpc + H_mpc') / 2;\n    K_mpc = H_mpc \\ (Theta' * Q_bar);\n    K_mpc = K_mpc(1:4, :);"

new_k = "    Theta1 = Theta(:, 1:4);\n    H1 = Theta1' * Q_bar * Theta1 + R_bar(1:4, 1:4);\n    H1 = (H1 + H1') / 2;\n    H1 = H1 + 1e-1 * max(abs(diag(H1))) * eye(4);\n    K_mpc = (H1 \\ (Theta1' * Q_bar * Psi))';"

content = content.replace(old_k, new_k)

with open(r'D:/mpc控制变桨系统/simulink_pitch/tune_mpc.m', 'w', encoding='utf-8') as f:
    f.write(content)

print('Done!')
