with open(r'C:\Users\xuan1\.openclaw\workspace\main\temp_liben.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# 找结论正文（不是目录里的"结论与展望"）
# 搜索结论的特征内容
keywords = ['总结全文', '本文的主要研究', '研究工作总结', '主要结论', '创新点如下']
for kw in keywords:
    idx = text.find(kw)
    if idx != -1:
        print(f'=== "{kw}" at {idx} ===')
        print(text[max(0,idx-200):idx+3000])
        print('---END---\n')
        break
else:
    # 尝试找第5章
    idx = text.find('第5章')
    if idx != -1:
        print(f'=== "第5章" at {idx} ===')
        print(text[idx:idx+3000])
