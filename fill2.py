import win32com.client, os, shutil

src = r'C:\Users\xuan1\.openclaw\media\inbound\附件6_湖南工程学院研究生创新项目申报书---391f5259-4dc5-4379-b0a7-ad3828bf49dd.doc'
dst = r'C:\Users\xuan1\.openclaw\workspace\main\申请书_已填写_最终版.docx'
shutil.copy2(src, dst)

word = win32com.client.Dispatch('Word.Application')
word.Visible = 0
word.DisplayAlerts = 0
doc = word.Documents.Open(os.path.abspath(dst))

def find_para(keyword):
    for i in range(1, doc.Paragraphs.Count+1):
        if keyword in doc.Paragraphs(i).Range.Text:
            return i
    return None

# === 1. Cover ===
p = find_para('项目名称：')
if p:
    rng = doc.Paragraphs(p).Range
    doc.Range(rng.End, rng.End).Text = '基于多电机驱动的大型风电变桨伺服系统研究'
    print('Cover filled')

# === 2. Section 二 ===
p = find_para('二、立项依据')
if p:
    t = p + 2
    with open(r'C:\Users\xuan1\.openclaw\workspace\main\sec2.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    rng = doc.Paragraphs(t).Range
    rng.Text = content + chr(10)
    rng.Font.Size = 12
    rng.Font.Name = '宋体'
    rng.Font.NameFarEast = '宋体'
    print('Section 二 filled')

# === 3. Section 三 ===
p = find_para('三、研究方案')
if p:
    t = p + 2
    with open(r'C:\Users\xuan1\.openclaw\workspace\main\sec3.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    rng = doc.Paragraphs(t).Range
    rng.Text = content + chr(10)
    rng.Font.Size = 12
    rng.Font.Name = '宋体'
    rng.Font.NameFarEast = '宋体'
    print('Section 三 filled')

# === 4. Section 四 ===
p = find_para('四、研究基础')
if p:
    t = p + 2
    content = '项目负责人研究工作积累：\n\n（请自行填写：课程基础、技能储备、文献积累、科研经历等）\n\n指导教师情况：\n\n（请自行填写谢卫才教授的学术简历，包括研究方向、代表性成果等）'
    rng = doc.Paragraphs(t).Range
    rng.Text = content + chr(10)
    rng.Font.Size = 12
    rng.Font.Name = '宋体'
    rng.Font.NameFarEast = '宋体'
    print('Section 四 filled')

# === 5. Budget table ===
try:
    tbl = doc.Tables(6)
    budget = [
        ['1. 科研业务费', '0.5', '文献数据库使用费、学术论文版面费（1~2篇）、学术交流差旅费'],
        ['2. 实验材料费', '0.3', '仿真软件工具箱授权费、训练数据采集与处理费用'],
        ['3. 仪器设备费', '0.5', '高性能计算机硬件升级（内存/固态硬盘）、外设购置'],
        ['4. 相关经费', '0.2', '论文查重检测费、报告打印装订费、知识产权申请费'],
    ]
    for r, row_data in enumerate(budget):
        for c, val in enumerate(row_data):
            try:
                cell = tbl.Rows(r+2).Cells(c+1)
                cell.Range.Text = val
                cell.Range.Font.Size = 10
                cell.Range.Font.Name = '宋体'
                cell.Range.Font.NameFarEast = '宋体'
            except:
                pass
    try:
        tbl.Rows(6).Cells(1).Range.Text = '合计'
        tbl.Rows(6).Cells(2).Range.Text = '1.5'
    except:
        pass
    print('Budget filled')
except Exception as e:
    print(f'Budget error: {e}')

# === 6. Supervisor opinion ===
p = find_para('指导教师意见')
if p:
    t = p + 2
    opinion = '该项目针对大型风力发电机组多电机变桨伺服系统的协同控制问题，提出了基于模型预测控制的融合控制方案，研究目标明确，技术路线合理，创新点清晰。项目将MPC滚动优化、多电机同步控制和LSTM风速预测前馈三者有机结合，具有较好的理论价值和工程应用前景。申请人已具备扎实的理论基础和仿真技能，研究方案可行，预期成果可期。同意推荐该项目申报研究生科研创新项目。'
    rng = doc.Paragraphs(t).Range
    rng.Text = opinion + chr(10)
    rng.Font.Size = 12
    rng.Font.Name = '宋体'
    rng.Font.NameFarEast = '宋体'
    print('Opinion filled')

doc.Save()
doc.Close()
word.Quit()
print('Done:', dst)
