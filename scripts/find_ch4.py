with open(r'C:\Users\xuan1\.openclaw\workspace\main\temp_liben.txt', 'r', encoding='utf-8') as f:
    text = f.read()

keywords = ['自抗扰控制理论基础', '偏差耦合同步控制结构分析', '改进偏差耦合同步控制结构设计', '全局平均转速', '扰动相同时的性能比较', '扩展至三台电机']
for kw in keywords:
    idx = text.find(kw)
    if idx != -1:
        print(f'=== "{kw}" at {idx} ===')
        start = max(0, idx - 200)
        end = min(len(text), idx + 5000)
        print(text[start:end])
        print('\n---END---\n')
