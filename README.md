# 普物实验预习报告生成器（Skill）

浙江大学物理实验预习报告的自动化生成规范。把《用霍尔法测直流圆线圈与亥姆霍兹线圈磁场》
预习报告从零做到成品的全过程（含踩过的所有坑）固化成了一个可复用的 skill。

## 这个 skill 做什么

输入一个实验名称 + 日期 + 周次 + 指导教师，输出：

- 可直接上传 **Overleaf** 用 **XeLaTeX** 编译的完整 LaTeX 工程
- 黑白灰原理图（Pillow 生成，无彩色）
- 已编译好的成品 PDF（3 页）
- 编译说明

## 仓库内容

```
SKILL.md               技能主文件：标杆规范 / 铁律 / 超星协议 / 5 步流程 / 故障对照表
README.md              本文件
scripts/
  make_figure.py       黑白原理图生成脚本（依赖 Pillow）
```

## 核心铁律（血泪教训）

1. **不要把 `fontset=windows` 加进 `\documentclass`** —— Overleaf 服务器没有 SimSun/SimHei，
   会报 `Package fontspec Error: The font "SimSun" cannot be found` 并导致编译超时。
   模板原样 + XeLaTeX 即可编译，**不需要改任何设置**。
2. **模板的 `content/config.tex` 与 `content/tail.tex` 保持逐字节不变**，
   不要加 `unicode-math` / `Cambria Math` / `tikz` / `pgfplots` / `float` / `caption` /
   `\setCJKmainfont` 等任何东西。
3. **尾页不许动**：「浙江大学物理实验教学中心制」必须保持居中。
4. **编译器必须是 XeLaTeX**，不是 pdfLaTeX（否则报 `CTeX fontset 'fandol' is unavailable`）。
5. **图必须黑白灰**；预习报告只放原理图，不放实验最终结果图。

## 标杆成品特征

| 项目 | 取值 |
|---|---|
| 页数 | 3 页（封面 / 正文 / 注意事项尾页） |
| 正文字体 | FandolSong（ctex 默认字体集）+ LaTeX 标准数学字体 |
| 小标题 | `实验现象：` `实验原理：` `实验方法：` —— 加粗、与内容同一行、字号同正文 |
| 公式 | 行间 `\[ ... \]` |
| 插图 | 0~2 张黑白原理图，caption 仅一行 |
| 综述字数 | 约 500 字 |

## 使用方法

把本目录放进你的 AI agent 的 skills 目录（例如 DSH 的
`~/.dsh/skills/<name>/SKILL.md`），之后对 agent 说：

> 做《XX 实验》的预习报告，指导教师是 XXX，日期 2026 年 X 月 X 日，周次 N

agent 会自动加载本 skill 并按流程产出压缩包 + 成品 PDF。

## 环境依赖

- **XeLaTeX**（MiKTeX 或 TeX Live）
- **Python 3** + **Pillow**（生成原理图）
- **PyMuPDF**（渲染自检，可选）
