import olefile, struct

path = r'C:\Users\xuan1\.openclaw\media\inbound\4.21-李奔-海上大型风机双驱电动变桨系统研究20260429---089940d6-ad50-4fae-8961-f3475f9f639e.doc'
ole = olefile.OleFileIO(path)
wd = ole.openstream('WordDocument').read()

text_parts = []
i = 0
while i < len(wd) - 1:
    char = struct.unpack_from('<H', wd, i)[0]
    if 0x4E00 <= char <= 0x9FFF:
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
out = r'C:\Users\xuan1\.openclaw\workspace\main\temp_liben.txt'
with open(out, 'w', encoding='utf-8') as f:
    f.write(full_text)
print(f'Extracted {len(full_text)} chars to {out}')
