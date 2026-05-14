import win32com.client
import os
import sys

word = win32com.client.Dispatch('Word.Application')
word.Visible = False

doc_path = os.path.abspath(r'D:\论文下载\4.21-李奔-海上大型风机双驱电动变桨系统研究20260429.doc')
doc = word.Documents.Open(doc_path)
text = doc.Content.Text
doc.Close()

# Save to file with error handling
output_path = r'C:\Users\xuan1\.openclaw\workspace\main\scripts\li_ben_full.txt'
with open(output_path, 'w', encoding='utf-8', errors='replace') as f:
    f.write(text)

print(f'Saved {len(text)} characters')
