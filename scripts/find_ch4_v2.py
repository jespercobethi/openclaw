with open(r'C:\Users\xuan1\.openclaw\workspace\main\temp_liben.txt', 'r', encoding='utf-8') as f:
    text = f.read()

keywords = ['扩张状态观测器', '非线性状态误差反馈', '跟踪微分器', '转速环', '同步误差补偿', '全局平均转速', '速度评价指标', '补偿器', '转速偏差', '扰动相同', '扰动不同']
for kw in keywords:
    idx = text.find(kw)
    if idx != -1:
        print(f'=== "{kw}" at {idx} ===')
        print(text[max(0,idx-200):idx+800])
        print('---END---\n')
