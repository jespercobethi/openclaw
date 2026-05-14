import win32com.client
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

word = win32com.client.Dispatch('Word.Application')
word.Visible = False

doc_path = os.path.abspath(r'D:\论文下载\4.21-李奔-海上大型风机双驱电动变桨系统研究20260429.doc')
doc = word.Documents.Open(doc_path)
text = doc.Content.Text
doc.Close()
word.Quit()

# Save to file to avoid encoding issues
output_path = r'C:\Users\xuan1\.openclaw\workspace\main\scripts\li奔论文全文.txt'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(text)

print(f'Saved {len(text)} characters to file')
print('First 200 chars:', text[:200])
