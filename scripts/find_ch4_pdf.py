import fitz

doc = fitz.open(r'C:\Users\xuan1\.openclaw\media\inbound\4.21-李奔-海上大型风机双驱电动变桨系统研究20260429---48ad2cb1-230f-40f6-83e2-5add01777796.pdf')

# 找第4章
for i in range(doc.page_count):
    text = doc[i].get_text()
    if '第4章' in text or '双电机同步控制' in text or '自抗扰' in text:
        print(f'=== Page {i+1} ===')
        print(text[:500])
        print('...')
