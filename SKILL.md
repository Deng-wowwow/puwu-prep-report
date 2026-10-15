---
name: zju-physics-prep-report
title: 普物实验预习报告
description: 普物实验预习报告生成器。当用户要求写/做「物理实验预习报告」「大物实验预习报告」「普物实验预习报告」，或给出超星学习通某实验章节并要求产出预习报告时使用。产出为可直接上传 Overleaf 编译的压缩包与成品 PDF。
---

# 浙江大学物理实验预习报告生成器

## 来历

本 skill 固化自一次真实的浙江大学物理实验预习报告制作过程（《用霍尔法测直流圆线圈与
亥姆霍兹线圈磁场》），包含了当时踩过的全部坑与全部验收标准。

## 标杆（Benchmark）

用户认可的标准成品：
本机 `大物实验成品\` 目录下的《用霍尔法测直流圆线圈与亥姆霍兹线圈磁场预习报告.pdf`
（3 页、封面 + 正文 + 注意事项尾页）

已用 PyMuPDF 逐页核实其真实特征：

| 项目 | 取值 |
|---|---|
| 页数 | 3 页（封面 / 正文 / 注意事项尾页） |
| 封面 | 校徽图 head.png + 实验名称、指导教师、班级、姓名、学号、实验日期（含星期） |
| 正文字体 | FandolSong（ctex 默认 fandol 字体集）+ LaTeX 标准数学字体 |
| 小标题 | `实验现象：` `实验原理：` `实验方法：` —— 加粗、与内容同一行、字号同正文 |
| 公式 | 行间 `\[ ... \]` |
| 插图 | 0~2 张黑白灰原理图，caption 仅一行 |
| 综述字数 | 约 500 字（模板说明写 300，但标杆实测 500，以标杆为准） |
| 编译器 | XeLaTeX |

## 绝对禁止（血泪教训）

1. **禁止给 `\documentclass` 加 `fontset=windows`** —— Overleaf 服务器无 SimSun/SimHei，会报
   `Package fontspec Error: The font "SimSun" cannot be found` 并导致编译超时。
   用户原话：「没有这行字就可以了」。模板原样 + XeLaTeX 即可编译。**不需要改任何设置。**
2. **禁止修改 `content/config.tex` 与 `content/tail.tex`**（须逐字节一致）。不得加入
   `unicode-math`、`Cambria Math`、`tikz`、`pgfplots`、`float`、`enumitem`、`caption`、
   `\setCJKmainfont` 等任何内容。
3. **禁止改动尾页排版**：「浙江大学物理实验教学中心制」必须保持居中；不得增删「注意事项」缩进；
   不得用 `\begingroup\noindent` 包裹 `\input{content/tail}`。
4. **禁止改动封面校徽与尾页的「浙江大学」字样。**
5. **禁止彩色图**（用户认为不严谨）；**禁止把实验最终结果图放进预习报告**（只放原理图）。
6. **禁止擅自增加章节**：正文只有 综述 / 重点 / 难点 三节。
7. **未经用户明确同意，禁止往 `大物实验成品` 文件夹写文件。**
8. **禁止写死、复用或转交任何人的学习通账号密码。** 抓取课程内容时必须由使用者
   当次提供**自己的**凭据；凭据不得写入任何文件、日志或提交记录，仅内存中使用。

## 已知用户信息

**固定不变（可直接用默认值）**：
- 姓名（占位：`<姓名>`）
- 学号（占位：`<学号>`）
- 班级（占位：`<班级>`）

**必须每次向用户询问，禁止沿用默认值**：
- **指导教师**（每次都可能不同，**必须每次询问**）
- **实验名称**（取超星页面原样全称）
- **实验日期**（含星期；星期几由系统日期计算）
- **周次**（用于最终 PDF 命名：姓名+学号+实验名称+周次）
- **是否插图**（以及插入哪张原理图）

> 动手写 cover.tex 之前，若上述任一字段缺失，**必须先问**，不得擅自填上次的值。

## 模板位置

原始模板（**只读，绝不修改**）：`C:\Users\Deng\Downloads\物理实验预习报告__模板_\`

```
预习报告.tex          主文件
content/config.tex    排版配置（原件）
content/cover.tex     封面（只改填入字段）
content/tail.tex      尾页（原件）
figures/head.png      校徽表头图（原件）
SimSun.ttf            模板自带字体（原件）
```

输出目录建议：`C:\Users\Deng\Desktop\大物实验\<实验简称>预习报告\`

## 工作流程

### 第 1 步 取原始素材（必须来自课程材料，禁止编造）

> **凭据规则（必须严格遵守）**
> - skill 中**不得写死任何人的学习通账号或密码**。
> - 需要抓取课程内容时，**必须由使用者当次自行提供自己的账号密码**；
>   若使用者是别人，必须让对方输入**自己的**账号，**绝不使用、转交或复用他人的凭据**。
> - 账号密码**不得写入任何文件、日志、提交记录或 skill 内容**，仅当次会话内存中使用。
> - 使用完毕后应提示使用者：建议修改密码 / 不要在对话中长期留存明文密码。

超星协议（2026-10 验证可用）：
- 登录页 `https://passport2.chaoxing.com/login`
- 密码用 AES-128-CBC 加密，`key == IV == "u2oh6Vu^HWe4_AES"`，PKCS7，密文 Base64（无 salt）
  （此常量来自站点公开 JS，属于协议参数，**不是凭据**）
- POST `https://passport2.chaoxing.com/fanyalogin`，参数
  `fid=-1, uname=AES(<使用者自己的手机号>), password=AES(<使用者自己的密码>), refer, t=true, forbidotherlogin=0, validate='', doubleFactorLogin=0, independentId=0, independentNameId=0`
- 成功返回 `{"status":true,...}`；`msg2` 为 UTF-8 中文错误信息
- 章节数据 `/mooc-ans/knowledge/cards?clazzid=&courseid=&knowledgeid=&num=N&ut=s&cpi=&mooc2=1`
- 附件地址 `/ananas/status/{objectid}` → JSON 内 `download` / `pdf`
- 必须用 **Python requests**（本机 PowerShell 的 schannel 被沙箱拦，curl/HttpClient 无法建 TLS）

### 第 2 步 写三节正文
```latex
\section{实验综述}

\xiaosi\textbf{实验现象：}……

\xiaosi\textbf{实验原理：}……（推导与行间公式写在此处）
\[
……公式……
\]

\xiaosi\textbf{实验方法：}……

\myspace{2}


\section{实验重点}

\xiaosi ……（约 100 字）

\myspace{2}

\section{实验难点}

\xiaosi ……（约 100 字）

\newpage

\input{content/tail}

\end{document}
```
- 小标题**同行**、`\textbf{}` 加粗、带**全角冒号**、字号同正文
- 公式用行间 `\[ ... \]`（模板已载 amsmath，无需加宏包）

### 第 3 步 插图（可选，0~2 张）
脚本：`scripts/make_figure.py`（Pillow 手绘黑白灰，本机无 matplotlib）
```powershell
$env:PYTHONPATH = "D:\pylibs"
python "<skill>\scripts\make_figure.py" --out "<工程>\figures\hall.png"
```
要点：**文字定位必须用 `draw.textbbox()` 测量后居中**，凭估算坐标会重叠。
插入代码（**不加任何宏包**，graphicx 模板已载）：
```latex
\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.62\textwidth]{figures/hall.png}
    \caption{霍尔效应原理示意图。}
\end{figure}
```

### 第 4 步 编译验证（必做，不得跳过）
```powershell
Set-Location "<工程目录>"
xelatex -interaction=nonstopmode 预习报告.tex    # 连跑两遍
```
三项必须全过：① exit 0 ② 日志无 `^! ` ③ 无 `Missing character`
然后**渲染成图逐页用眼睛检查**：
```python
import pymupdf
d = pymupdf.open("预习报告.pdf")
for i in range(d.page_count):
    d[i].get_pixmap(dpi=115).save(f"p{i+1}.png")
```
检查项：标题字体正确、小标题同行且加粗、图无标签重叠、尾页落款居中、共 3 页。

### 第 5 步 交付（**只给压缩包，不给文件夹**）

用户明确要求：「skill 改一下不要上传文件夹了，直接给压缩包」。
因此每次交付**只产出 zip**（zip 内部的目录结构仍完整，只是交付形式上不另给文件夹）：

```powershell
Add-Type -AssemblyName System.IO.Compression.FileSystem
# 先在临时目录摆好结构，再打包（includeBaseDirectory = $false，避免多套一层）
[System.IO.Compression.ZipFile]::CreateFromDirectory(
    "<暂存目录>", "<实验名>预习报告.zip",
    [System.IO.Compression.CompressionLevel]::Optimal, $false)
```

zip 内部结构（不能多套一层目录）：
```
预习报告.tex            主文件（唯一改动的代码文件之一）
content/config.tex      模板原件
content/cover.tex       仅填字段
content/tail.tex        模板原件
figures/head.png        模板原件
figures/<原理图>.png    黑白原理图（如有）
SimSun.ttf              模板原件
编译说明.txt            含 Overleaf 上传步骤与 XeLaTeX 设置
预习报告.pdf            已编译成品（便于用户先看效果）
```

**打包时可瘦身**：`SimSun.ttf` 占 10 MB（压缩后约 5.6 MB），Overleaf 用不到它
（那边有 FandolSong）。用户嫌上传慢时可排除该文件，**排除后仍能正常编译**。

交付话术要包含：
1. 给用户 zip 的链接，告诉他 **Overleaf → New Project → Upload Project → 拖入 zip**
2. 强调 **Menu → Compiler → XeLaTeX**（漏了必报 fandol 错误）
3. 说明 zip 内已含 `content/`、`figures/` 子目录，Overleaf 会自动保留结构

## 故障对照表（均真实发生）

| 现象 | 真因 | 解法 |
|---|---|---|
| `CTeX fontset 'fandol' is unavailable` | 编译器是 pdfLaTeX | 切到 XeLaTeX |
| `fontspec Error: The font "SimSun" cannot be found` | 加了 `fontset=windows` | 删掉该选项 |
| 编译超时 | `fontset=windows` 导致满服务器找字体 | 同上 |
| `Undefined control sequence`（config.tex） | 私加 `\setCJKmainfont` 却未载 fontspec | 恢复 config.tex 原件 |
| 「文字很奇怪」「字体难看」 | 加了 unicode-math / Cambria Math / tikz | 全删，回模板默认 |
| 大标题字号变小 | `\titleformat` 中 `\normalfont` 重置字号 | 不要自行重定义 section |
| 「实验现象」未变粗 | 用 `\songti\bfseries`（宋体无粗体字形，静默回退） | 用 `\textbf{}`，ctex 自动切黑体 |
| 「注意事项」不居中/被移动 | 用 `\begingroup\noindent` 包裹了 tail | 尾页原样输出 |
| 日期显示「2 026 年」 | `\makebox` 居中 + 字宽变化 | 数字与「年月日」间用 `\ ` 显式空格 |
| 用户问「文件夹怎么上传 Overleaf」 | Overleaf 只接受 zip 或单个文件，**不能上传文件夹** | 交付时直接给 zip（见第 5 步） |

## 用户如何上传到 Overleaf

1. Overleaf → **New Project → Upload Project** → 拖入交付的 zip（或点 `Select a .zip file`）
2. 已有项目时：项目内 **New File 旁的上传按钮（↑）→ Upload Zip**
3. Overleaf 会自动解压并保留 `content/`、`figures/` 结构
4. **Menu → Compiler → XeLaTeX** → Recompile

## 用户环境备忘

- 本机 MiKTeX：`D:\Fds\miktex\bin\x64\`（`xelatex`、`latexmk` 可用），**本地也能编译**
- Python：`C:\Users\Deng\AppData\Local\Programs\Python\Python313\python.exe`
- 第三方库装在 `D:\pylibs`（pymupdf、pillow 等），用时先 `$env:PYTHONPATH = "D:\pylibs"`
- 沙箱只允许写 `C:\Users\Deng\Desktop\大物实验`；写 D 盘或其他目录需用户放行提权，
  **被拒后不要反复申请**，改为把成品放进工作区并说明
