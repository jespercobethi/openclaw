import scipy.io as sio
import numpy as np
import sys

mat_path = r'D:\mpc控制变桨系统\simulink_pitch\comparison_results.mat'
data = sio.loadmat(mat_path)

print('Keys:', list(data.keys()))
for k, v in data.items():
    if not k.startswith('_'):
        print(f'{k}: shape={v.shape if hasattr(v, "shape") else type(v)}')
