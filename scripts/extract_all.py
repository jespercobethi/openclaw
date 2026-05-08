with open(r'C:\Users\xuan1\.openclaw\workspace\main\temp_liben.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# 提取各章节关键内容

# 摘要
abs_start = text.find('当前，全球海上风力发电机组')
abs_end = text.find('ABSTRACT', abs_start)
abstract = text[abs_start:abs_end].strip()

# 第2章 - 电机设计（从"2.1 基本设计要求"到"本章小结"）
ch2_start = text.find('2.1 基本设计要求')
ch2_end = text.find('第3章', ch2_start)
if ch2_end == -1:
    ch2_end = text.find('基于Ansys', ch2_start)
ch2 = text[ch2_start:ch2_end].strip() if ch2_start != -1 else 'Not found'

# 第3章 - Ansys仿真
ch3_start = text.find('第3章')
if ch3_start == -1:
    ch3_start = text.find('有限元分析方法简介')
ch3_end = text.find('第4章', ch3_start) if ch3_start != -1 else -1
ch3 = text[ch3_start:ch3_end].strip() if ch3_start != -1 and ch3_end != -1 else 'Not fully found'

# 结论
conc_start = text.find('结论与展望')
conc_end = len(text)
conclusion = text[conc_start:conc_start+5000].strip() if conc_start != -1 else 'Not found'

# 保存
with open(r'C:\Users\xuan1\.openclaw\workspace\main\liben_all_chapters.txt', 'w', encoding='utf-8') as f:
    f.write('=== 摘要 ===\n')
    f.write(abstract[:3000])
    f.write('\n\n=== 第2章（电机设计）===\n')
    f.write(ch2[:8000])
    f.write('\n\n=== 第3章（Ansys仿真）===\n')
    f.write(ch3[:5000])
    f.write('\n\n=== 结论与展望 ===\n')
    f.write(conclusion[:5000])

print(f'Abstract: {len(abstract)} chars')
print(f'Chapter 2: {len(ch2)} chars')
print(f'Chapter 3: {len(ch3)} chars')
print(f'Conclusion: {len(conclusion)} chars')
