import olefile
import struct
import sys

path = r'C:\Users\xuan1\.openclaw\media\inbound\基于多电机驱动的大型风电变桨伺服系统研究---ba0e1272-0dd2-4ca5-a6c1-7db8f38706ea.docx'
out_path = r'C:\Users\xuan1\.openclaw\workspace\main\temp_doc_text.txt'

ole = olefile.OleFileIO(path)
wd = ole.openstream('WordDocument').read()

# Find all sequences of valid UTF-16LE Chinese/text characters
text_parts = []
i = 0
while i < len(wd) - 1:
    char = struct.unpack_from('<H', wd, i)[0]
    if 0x4E00 <= char <= 0x9FFF:  # CJK Unified Ideographs
        start = i
        chars = []
        while i < len(wd) - 1:
            char = struct.unpack_from('<H', wd, i)[0]
            if (0x4E00 <= char <= 0x9FFF) or (0x3000 <= char <= 0x303F) or (0xFF00 <= char <= 0xFFEF) or (0x0020 <= char <= 0x007E) or char in (0x000A, 0x000D, 0x3001, 0x3002) or (0x2000 <= char <= 0x206F):
                chars.append(chr(char))
                i += 2
            else:
                break
        if len(chars) >= 3:
            text_parts.append(''.join(chars))
    else:
        i += 2

full_text = '\n'.join(text_parts)

with open(out_path, 'w', encoding='utf-8') as f:
    f.write(full_text)

print(f"Extracted {len(full_text)} characters to {out_path}")
