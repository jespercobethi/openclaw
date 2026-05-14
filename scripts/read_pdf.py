import sys
import fitz

pdf_path = r'D:\论文下载\4.21-李奔-海上大型风机双驱电动变桨系统研究20260429.pdf'
doc = fitz.open(pdf_path)
print(f'Total pages: {doc.page_count}')

for i in range(doc.page_count):
    text = doc[i].get_text()
    print(f'\n===== PAGE {i+1} =====')
    print(text)
