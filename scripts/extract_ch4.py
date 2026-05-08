with open(r'C:\Users\xuan1\.openclaw\workspace\main\temp_liben.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# 提取第4章完整内容
# 从"4.1"或"PMSM数学模型"开始
start = text.find('跟踪微分器TD')
if start == -1:
    start = text.find('4.1')
# 往前找一点
start = max(0, start - 500)

# 找第4章结束位置（第5章或"结论与展望"）
end = text.find('结论与展望', start)
if end == -1:
    end = start + 20000

chapter4 = text[start:end]
with open(r'C:\Users\xuan1\.openclaw\workspace\main\chapter4_extracted.txt', 'w', encoding='utf-8') as f:
    f.write(chapter4)

print(f'Extracted {len(chapter4)} chars')
print(chapter4[:10000])
