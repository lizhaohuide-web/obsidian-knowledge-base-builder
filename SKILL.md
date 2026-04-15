---
name: obsidian-knowledge-base-builder
description: |
  帮助任何用户从 0 到 1 搭建、清洗、梳理 Obsidian 知识库的全流程 Skill。
  基于 Karpathy LLM Wiki 架构 + PARA 管理法。
  适用于：新 Vault 初始化、旧笔记迁移、混乱知识库重构、标准化现有笔记。
  触发词：搭建知识库、初始化 Obsidian、梳理笔记、编译知识库、修复死链、标签规范化、知识库体检
---

# Obsidian 知识库搭建与重构 (v2.0)

> **核心原则**：知识库不是静态仓库，而是**动态处理器**。Input 必须流向 Process 并产出 Output。
> **设计哲学**：结合 Karpathy LLM Wiki 的 "Input → Compile → Wiki" 流水线 + PARA 行动导向架构。
> **适用对象**：任何希望建立结构化、可维护、支持 LLM 辅助管理的个人/团队知识库的用户。

---

## 📋 执行流程总览

```
Phase 0: 环境准备 (安装 Obsidian → 创建 Vault → 配置插件)
    ↓
Phase 1: 目录结构初始化 (建立 PARA+Wiki 骨架)
    ↓
Phase 2: 数据清洗 (用户指定目录 → 扫描 → 清洗 → 标准化 → 迁移)
    ↓
Phase 3: 关联网络构建 (死链修复 → MOC 仪表盘 → 知识图谱)
    ↓
Phase 4: 验证与体检 (Lint 检查 → 输出报告)
    ↓
Phase 5: 自动化配置 (Cron 定时编译 → 持续维护)
```

**⚠️ 关键交互点**：
- **Phase 0 结束时**：向用户确认 Obsidian 已就绪，询问"请告诉我你的原始笔记存放目录路径"。
- **Phase 2 开始时**：必须拿到用户指定的源目录，否则无法继续。

---

## 🔧 Phase 0: 环境准备

**目标**：确保用户已安装 Obsidian，Vault 已创建，核心插件已配置，环境对 AI Agent 友好。

### 0.1 安装 Obsidian

> **Agent 动作**：根据用户操作系统提供对应指引，引导用户完成安装。

**macOS**:
1. 前往 [obsidian.md](https://obsidian.md) 下载 dmg 安装包
2. 拖拽到 Applications 文件夹
3. 首次启动，授予"完全磁盘访问权限"（系统偏好设置 → 隐私与安全性 → 完全磁盘访问权限 → 添加 Obsidian）

**Windows**:
1. 前往 [obsidian.md](https://obsidian.md) 下载 exe 安装包
2. 运行安装程序，按提示完成
3. 建议安装到非 C 盘路径（如 `D:\Obsidian`）

**Linux**:
1. 推荐 Flatpak: `flatpak install flathub md.obsidian.Obsidian`
2. 或 AppImage: 从官网下载后 `chmod +x Obsidian-*.AppImage && ./Obsidian-*.AppImage`

### 0.2 创建 Vault（知识库仓库）

> **Agent 动作**：引导用户选择 Vault 存储位置。

1. 打开 Obsidian → **Create new vault**
2. 命名建议：`Second-Brain` 或 `[姓名]-Wiki`
3. 选择存储位置（**重要**：选择 Agent 有读写权限的目录）
   - 推荐路径示例：
     - macOS: `~/Documents/Second-Brain/` 或 `~/Obsidian/`
     - Windows: `D:\Obsidian\Second-Brain\`
     - Linux: `~/Obsidian/Second-Brain/`

4. **Vault 路径确认**：Agent 需记录此路径为 `{vault_path}`，后续所有操作基于此。

### 0.3 核心插件配置（AI Agent 友好型）

> **Agent 动作**：引导用户安装以下插件。这些插件使 Obsidian 对 AI Agent 的读写操作更加友好。

**必装插件（社区插件）**：

| 插件 | 用途 | 安装方式 |
|------|------|----------|
| **Templater** | 强大的模板引擎，支持 JS 变量 | 设置 → 社区插件 → 浏览 → 搜索安装 |
| **Dataview** | 查询和展示笔记数据（表格、列表） | 同上 |
| **Auto Note Mover** | 根据标签/路径自动移动笔记 | 同上 |
| **Linter** | 自动格式化 Markdown 和 YAML | 同上 |
| **Calendar** | 日历视图，辅助 Daily Notes | 同上 |

**推荐插件（可选）**：

| 插件 | 用途 |
|------|------|
| **Copilot** | 本地 LLM 集成，Vault 内 AI 对话 |
| **Smart Connections** | 语义搜索，发现笔记间的隐藏关联 |
| **Local REST API** | 暴露 REST API，方便 Agent 远程读写 |
| **Obsidian Git** | 自动 Git 备份，版本控制 |

### 0.4 AI Agent 友好配置

> **Agent 动作**：引导用户修改以下 Obsidian 设置。

1. **设置 → 文件与链接**:
   - 新笔记默认位置 → `Inbox 文件夹` (指向 `00-Inbox`)
   - 新笔记附件存放位置 → `指定文件夹` → 创建 `Attachments/`
   - 使用 `[[Wikilinks]]`（不要用 Markdown 链接，Agent 处理 Wikilinks 更准确）
   - 默认打开模式 → `编辑模式`

2. **设置 → 核心插件**:
   - ✅ 启用 **模板**
   - ✅ 启用 **日记** (Daily Notes)
   - ✅ 启用 **文件恢复**
   - ✅ 启用 **星标**

3. **设置 → Linter 插件** (安装后配置):
   - YAML 时间格式 → `YYYY-MM-DD`
   - 启用 `YAML Title` → 同步文件名
   - 启用 `YAML Timestamp` → 自动写入 `created` / `updated`

4. **设置 → Templater 插件**:
   - 模板文件夹位置 → `30-Resources/Templates/`

### 0.5 环境就绪检查清单

- [ ] Obsidian 已安装并可以正常打开
- [ ] Vault 已创建，路径已记录为 `{vault_path}`
- [ ] 社区插件已启用，Templater + Dataview 已安装
- [ ] Linter 已配置 YAML 格式
- [ ] Agent 确认有 `{vault_path}` 的读写权限
- [ ] 用户已提供需要清洗的原始笔记目录路径 `{source_dir}`

**✅ 通过后进入 Phase 1。**

---

## 🏗️ Phase 1: 目录结构初始化

**目标**：在 `{vault_path}` 下建立标准化的骨架，确保知识流动的清晰路径（Input → Process → Output）。

### 1.1 标准目录树 (PARA + Wiki 混合)

Agent 需在 `{vault_path}` 下创建以下目录结构（若不存在）：

```text
{vault_path}/
├── 00-Inbox/              # 📥 速记收件箱（随手记，未分类，需定期清理）
├── 01-Raw/                # 📦 原始素材（Input：未处理的信息）
│   ├── articles/          #    文章剪藏、博客摘录
│   ├── meetings/          #    会议记录
│   ├── imported-notes/    #    从旧系统导入的笔记
│   └── daily-journal/     #    日记/日志
├── 02-Wiki/               # 🧠 编译维基（Process/Output：结构化的知识）
│   ├── CLAUDE.md          #    知识库说明书（LLM 必读 Schema）
│   ├── _index.md          #    全量索引（自动维护）
│   ├── 概念/              #    抽象概念（定义、理论、原理）
│   ├── 人物/              #    关键人物（专家、历史人物、同事）
│   ├── 工具/              #    软件、API、模型、书籍、课程
│   ├── 方法论/            #    可复用的流程、SOP、框架
│   ├── 项目/              #    项目级的 Wiki 仪表盘
│   └── 领域/              #    领域知识聚合（按用户自定义）
├── 03-Outputs/            # 📤 产出与复盘（报告、分析、文章）
│   ├── 文章/
│   ├── 复盘/
│   └── 数据/
├── 10-Projects/           # 🔥 活跃项目（有明确目标和截止日期的任务）
├── 20-Areas/              # 🌍 关注领域（长期维护的兴趣/职责）
├── 30-Resources/          # 📚 参考资料
│   └── Templates/         #    Templater 模板目录
├── 40-Archive/            # 🗄️ 归档（已完成/不再活跃的项目）
└── Attachments/           # 📎 附件（图片、PDF、音频）
```

### 1.2 核心检查点 (Agent 必读)

1. **Projects vs Archive**: 正在做的项目绝不能在 `40-Archive` 里！
2. **Raw vs Wiki**: `Raw` 是原材料，`Wiki` 是加工品。原材料永远留在 `01-Raw`，加工品进入 `02-Wiki`，两者通过链接关联，**不要复制内容**。
3. **Inbox 清空**: 确保 `00-Inbox` 定期被处理，不堆积。
4. **Attachments 隔离**: 所有图片/PDF 统一存 `Attachments/`，不要散落在笔记目录中。
5. **Templates 就位**: `30-Resources/Templates/` 必须包含基础模板（日记、新项目、新概念）。

### 1.3 创建基础模板文件

> **Agent 动作**：在 `30-Resources/Templates/` 下创建以下模板。

**日记模板** (`30-Resources/Templates/daily-note.md`):
```markdown
---
tags: [日记]
created: "{{date:YYYY-MM-DD}}"
---

# 📅 {{date:YYYY-MM-DD}} 日记

## 🎯 今日重点
- [ ] 

## 📝 随手记

## 🔄 复盘
- 今日完成：
- 明日计划：
```

**新概念模板** (`30-Resources/Templates/new-concept.md`):
```markdown
---
tags: [概念/待分类]
created: "{{date:YYYY-MM-DD}}"
updated: "{{date:YYYY-MM-DD}}"
source: ""
---

# {{title}}

## 定义
> 一句话概括这个概念是什么。

## 核心要点
- 

## 相关概念
- [[关联概念 A]]
- [[关联概念 B]]

## 应用场景
- 
```

**新项目模板** (`30-Resources/Templates/new-project.md`):
```markdown
---
tags: [项目/进行中]
created: "{{date:YYYY-MM-DD}}"
updated: "{{date:YYYY-MM-DD}}"
status: 进行中
---

# 🚀 {{title}}

## 项目目标
> 这个项目要解决什么问题？成功标准是什么？

## 关键里程碑
- [ ] 里程碑 1 — 截止日期：
- [ ] 里程碑 2 — 截止日期：

## 核心文档
- [[商业计划书]]
- [[需求文档]]

## 复盘记录
- [[项目复盘 1]]
```

### 1.4 创建 CLAUDE.md（知识库 Schema）

> **Agent 动作**：在 `02-Wiki/CLAUDE.md` 写入知识库说明书。
> 模板参考：`references/schema-template.md`

---

## 🧹 Phase 2: 数据清洗与规范化

**目标**：将用户指定的 `{source_dir}` 中的原始数据清洗、标准化后迁移到 `{vault_path}`。

### 2.1 扫描与评估

**Agent 动作**：
1. 获取用户提供的 `{source_dir}` 路径
2. 递归扫描目录下所有文件
3. 输出扫描报告：

```
📊 扫描报告
━━━━━━━━━━━━━━━━━━━━━
总文件数: XXX
- Markdown (.md): XX
- 文本 (.txt): XX
- PDF (.pdf): XX
- 图片 (.png/.jpg): XX
- 其他: XX

总大小: XX MB
时间跨度: 最早 20XX-XX-XX → 最晚 20XX-XX-XX
```

4. **向用户确认**："共发现 XX 个文件，是否开始清洗？"

### 2.2 文件分类与路由

**执行逻辑**：根据文件类型和内容特征，决定目标目录。

| 文件特征 | 分类判断 | 目标目录 |
|----------|----------|----------|
| 包含 `# 会议` / `agenda` / `meeting` 关键词 | 会议记录 | `01-Raw/meetings/` |
| 文件名含日期模式 (`2024-*` / `2024*-*`) | 日记/日志 | `01-Raw/daily-journal/` |
| 包含 `http://` 或 `<article>` 标签 | 文章剪藏 | `01-Raw/articles/` |
| 包含定义、理论、概念解释 | 概念笔记 | 先标记，待清洗后入 `02-Wiki/概念/` |
| 包含代码块、技术文档 | 工具笔记 | 先标记，待清洗后入 `02-Wiki/工具/` |
| 其他 | 默认 | `01-Raw/imported-notes/` |

### 2.3 内容清洗规则

#### 2.3.1 Frontmatter 标准化

**必须确保每个 `.md` 文件头部包含**：

```yaml
---
title: "文件名"
tags: [分类/子分类]
created: YYYY-MM-DD
updated: YYYY-MM-DD
source: "来源描述或链接"
status: raw | processing | compiled
---
```

**⚠️ 常见坑与修复策略**：
> 详细指南参考：`references/yaml-fix-guide.md`

1. **YAML 解析错误**：
   - **双括号必须加引号**：`source: [[链接]]` → `source: "[[链接]]"`
   - **多链接必须整体加引号**：`source: [[A]], [[B]]` → `source: "[[A]], [[B]]"`
   - **特殊字符**：如包含 `{{date}}`，必须加引号
   - **冒号问题**：`title: My Note: Subtitle` → `title: "My Note: Subtitle"`

2. **缺失字段补全**：
   - 无 `title`: 用文件名（不含扩展名）
   - 无 `tags`: 补 `[未分类]`
   - 无 `created`: 用文件创建日期或当天日期
   - 无 `updated`: 用当天日期
   - 无 `source`: 补 `"导入自 {source_dir}"`
   - 无 `status`: 补 `raw`

3. **标题一致性**：
   - 确保文件名（如 `第一性原理.md`）与文件内的 H1 标题（`# 第一性原理`）一致
   - **动作**：推荐重命名文件以匹配标题，因为标题通常更准确

#### 2.3.2 标签体系层级化

**执行逻辑**：将扁平、杂乱的标签转换为层级标签。

**通用映射规则**：
- **细化维度**：`AI` → `AI/工具` 或 `AI/理论`（根据内容判断）
- **归拢领域**：`小红书`, `抖音`, `公众号` → `新媒体/小红书` 等
- **删除噪音**：**删除**代表目录分类的标签（如 `#概念`, `#工具`, `#项目`），因为这些信息已由文件所在的目录结构承载

**标签映射参考模板**（见 `references/tag-mapping-template.json`）

**Agent 动作**：
1. 统计所有现有标签
2. 识别低频标签（仅使用 1-2 次的），建议合并到父标签或转为纯文本
3. 向用户展示标签映射方案，确认后执行

#### 2.3.3 内容净化

**清理以下无效内容**：
- 空行过多（连续 3+ 个空行 → 保留 1 个）
- 无意义的占位符（`TODO`, `待补充`, `xxx` → 标记为 `> ⚠️ 待补充`）
- HTML 残留标签（`<br>`, `<div>`, `<span>` → 转换为 Markdown 等效格式）
- 乱码检测：如果一段文字中非 ASCII 字符占比异常，标记为 `> ⚠️ 可能包含乱码`
- 重复段落：检测文件内重复超过 80% 的段落，保留一份

#### 2.3.4 消除重复 (Single Source of Truth)

**执行逻辑**：
1. **扫描**：查找文件名相同或内容相似度 > 85% 的文件
2. **仲裁**：
   - **保留最新版本**：比较 `updated` 日期或文件修改时间
   - **Wiki 优先**：若 `02-Wiki` 有一份，其他目录的同名文件应清空内容，改为**重定向**：
     ```markdown
     > ⚠️ 此笔记已迁移至 [[Wiki 中的文件名]]，此处仅做索引。
     ```
   - **Projects 优先**：项目笔记以 `10-Projects/` 中的为准

### 2.4 批量清洗脚本

> **Agent 动作**：执行以下 Python 脚本完成批量清洗。

```python
"""
Obsidian 笔记批量清洗脚本
用法: python clean_notes.py <source_dir> <vault_path>
"""
import os, re, sys
from datetime import datetime
from pathlib import Path

def detect_encoding(filepath):
    """简单编码检测"""
    for enc in ['utf-8', 'gbk', 'gb2312', 'latin-1']:
        try:
            with open(filepath, 'r', encoding=enc) as f:
                f.read()
            return enc
        except (UnicodeDecodeError, UnicodeError):
            continue
    return 'utf-8'

def fix_frontmatter(content, filename, source_dir):
    """修复或创建 Frontmatter"""
    now = datetime.now().strftime('%Y-%m-%d')
    
    # 提取现有 Frontmatter
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    fm = {}
    body = content
    
    if match:
        raw_fm = match.group(1)
        body = content[match.end():].lstrip('\n')
        # 简单解析
        for line in raw_fm.split('\n'):
            if ':' in line:
                key, _, val = line.partition(':')
                fm[key.strip()] = val.strip()
    
    # 确保必要字段
    defaults = {
        'title': f'"{Path(filename).stem}"',
        'tags': '[未分类]',
        'created': now,
        'updated': now,
        'source': f'"导入自 {source_dir}"',
        'status': 'raw'
    }
    
    for key, val in defaults.items():
        if key not in fm or not fm[key]:
            fm[key] = val
    
    # 修复 YAML 格式问题
    for key in fm:
        val = fm[key]
        if '[[' in str(val) and not val.startswith('"'):
            fm[key] = f'"{val}"'
        if ':' in str(val) and not val.startswith('"') and not val.startswith("'"):
            fm[key] = f'"{val}"'
    
    # 重建 Frontmatter
    new_fm = "---\n"
    for key in ['title', 'tags', 'created', 'updated', 'source', 'status']:
        if key in fm:
            new_fm += f"{key}: {fm[key]}\n"
    # 添加额外字段
    for key in fm:
        if key not in ['title', 'tags', 'title', 'created', 'updated', 'source', 'status']:
            new_fm += f"{key}: {fm[key]}\n"
    new_fm += "---\n\n"
    
    return new_fm + body

def clean_content(body):
    """净化内容"""
    # 去除连续空行
    body = re.sub(r'\n{3,}', '\n\n', body)
    # 清理 HTML 标签
    body = re.sub(r'<br\s*/?>', '\n', body)
    body = re.sub(r'</?div[^>]*>', '\n', body)
    body = re.sub(r'</?span[^>]*>', '', body)
    return body

def clean_notes(source_dir, vault_path):
    """主清洗流程"""
    stats = {'processed': 0, 'errors': 0, 'files': []}
    
    for root, _, files in os.walk(source_dir):
        for f in files:
            if not f.endswith(('.md', '.txt')):
                continue
            
            src_path = os.path.join(root, f)
            encoding = detect_encoding(src_path)
            
            try:
                with open(src_path, 'r', encoding=encoding) as fp:
                    content = fp.read()
                
                # 清洗
                content = fix_frontmatter(content, f, source_dir)
                
                # 分离 Frontmatter 和 body
                match = re.match(r'^(---\n.*?\n---\n\n?)(.*)', content, re.DOTALL)
                if match:
                    fm_part, body = match.group(1), match.group(2)
                    body = clean_content(body)
                    content = fm_part + body
                
                # 确保 H1 标题存在
                if not re.search(r'^# ', content, re.MULTILINE):
                    title = Path(f).stem
                    # 在 Frontmatter 后插入 H1
                    match = re.match(r'^(---\n.*?\n---\n\n?)', content, re.DOTALL)
                    if match:
                        content = match.group(1) + f"# {title}\n\n" + content[match.end():]
                    else:
                        content = f"# {title}\n\n" + content
                
                stats['files'].append(f)
                stats['processed'] += 1
                print(f"✅ {f}")
                
            except Exception as e:
                stats['errors'] += 1
                print(f"❌ {f}: {e}")
    
    return stats
```

### 2.5 迁移执行

**Agent 动作**：
1. 对每个文件执行分类判断（2.2 节）
2. 应用清洗规则（2.3 节）
3. 写入目标目录
4. 处理附件（图片/PDF 移动到 `Attachments/`，笔记中更新链接）
5. 输出迁移报告

---

## 🔗 Phase 3: 关联网络构建

**目标**：让知识流动起来，消灭孤岛（Orphan Pages），建立 MOC（Map of Content）。

### 3.1 死链修复 (Broken Links)

**执行逻辑**：
1. 提取所有 `[[...]]` 链接
2. 检查目标文件是否存在
3. **修复策略**：
   - **路径变更**：若文件移动了（如从旧目录移到 `01-Raw`），批量替换旧路径链接
   - **伪链接清理**：删除或替换 `[[xxx]]`, `[[链接]]`, `[[双向链接]]` 等模板占位符
   - **非笔记引用**：若 `[[技能名]]` 实际指代外部工具而非笔记，将其转为纯文本
   - **别名支持**：若链接形如 `[[文件名|显示名]]`，确认文件名存在即可

### 3.2 建立 MOC 仪表盘 (Map of Content)

**Agent 动作**：创建或更新 `00-大脑仪表盘.md`（全局入口）。
> 模板参考：`references/moc-template.md`

**构建逻辑**：
1. 扫描 `02-Wiki/` 下所有文件
2. 按目录分类（概念/人物/工具/方法论）
3. 扫描 `10-Projects/` 下所有活跃项目
4. 扫描孤立页面（无入链的笔记）
5. 生成仪表盘，将所有内容组织到对应板块

### 3.3 项目页仪表盘化

**执行逻辑**：`02-Wiki/项目/` 下的页面不能只写简介，必须是 **Dashboard**。
> 模板参考：`references/project-dashboard-template.md`

### 3.4 全量索引生成

**Agent 动作**：生成 `02-Wiki/_index.md`。

```markdown
# 📚 全量索引

> 自动生成于 {date}，包含 {count} 条记录。

## 按类型
### 📖 概念 ({count})
- [[概念 A]]
- [[概念 B]]

### 👤 人物 ({count})
- [[人物 A]]

### 🔧 工具 ({count})
- [[工具 A]]

### 📋 方法论 ({count})
- [[方法论 A]]

## 按标签
{按标签分组列出所有笔记}

## 孤立页面
{列出无入链的页面}
```

### 3.5 双向链接优化

**Agent 动作**：
1. 对于高引用笔记（被引用 3+ 次），在其底部添加"反向链接"区域：
   ```markdown
   ---
   ## 🔗 反向链接
   - [[引用此笔记的笔记 A]]
   - [[引用此笔记的笔记 B]]
   ```
2. 对于孤立页面，尝试根据其内容自动链接到相关笔记

---

## 🔍 Phase 4: 验证与体检

**目标**：确保知识库健康度，输出报告。

### 4.1 检查清单 (Linting)

Agent 需运行最终检查，统计以下指标：

| 指标 | 目标值 | 检查方法 |
|------|--------|----------|
| YAML 通过率 | 100% | 尝试解析每个文件的 Frontmatter |
| 属性完整率 | >95% | 检查 tags, created, updated, source 齐全 |
| 死链数 | 0 | 检查所有 `[[链接]]` 是否指向存在文件 |
| 孤立页面率 | <10% | 无入链的笔记占比（模板/日志除外） |
| 目录合规性 | 100% | 无活跃项目在 Archive，无 Raw 素材在 Wiki |
| 标题一致性 | 100% | 文件名与 H1 一致 |
| 标签规范率 | >90% | 无扁平噪音标签，均为层级标签 |

### 4.2 体检报告模板

```markdown
# 🏥 知识库体检报告

**检查日期**: {date}
**Vault 路径**: {vault_path}
**总笔记数**: {total}

## 健康度评分: {score}/100

### ✅ 通过项
- YAML 通过率: 100%
- ...

### ⚠️ 警告项
- 孤立页面: X 个 (X%)
  - 页面 A: 建议链接到 [[相关笔记]]
  - 页面 B: 建议删除或归档

### ❌ 错误项
- 死链: X 个
  - [[死链目标]] 不存在，来源: [[来源笔记]]

### 📊 统计
- 概念笔记: X
- 人物笔记: X
- 工具笔记: X
- 方法论: X
- 活跃项目: X
- 归档项目: X
```

### 4.3 自动化建议 (Cron)

若环境支持 Cron，建议用户设置：
- **每日编译**：扫描 `Inbox` + `Raw` → 实体提取 → 生成/更新 `Wiki`
- **每周体检**：运行 Lint 检查（矛盾检测、孤儿页、过期内容）
- **每月归档**：检查 `10-Projects/`，将超过 30 天无更新的项目移至 `40-Archive/`

---

## 🛠️ 附录：Agent 执行工具箱

### A. 完整清洗 + 迁移脚本

```python
"""
Obsidian 知识库完整清洗 + 迁移脚本
用法: python obsidian_builder.py --source <source_dir> --vault <vault_path>
"""
import os, re, sys, json
from datetime import datetime
from pathlib import Path

class ObsidianBuilder:
    def __init__(self, source_dir, vault_path):
        self.source_dir = source_dir
        self.vault_path = vault_path
        self.stats = {
            'total': 0, 'processed': 0, 'errors': 0,
            'by_category': {}, 'broken_links': [],
            'orphan_pages': [], 'tags': {}
        }
    
    def run(self):
        print(f"🚀 开始构建知识库")
        print(f"   源目录: {self.source_dir}")
        print(f"   Vault:  {self.vault_path}")
        
        self.ensure_structure()
        self.scan_and_clean()
        self.fix_broken_links()
        self.generate_moc()
        self.generate_report()
        
        print(f"\n✅ 完成! 处理 {self.stats['processed']}/{self.stats['total']} 个文件")
    
    def ensure_structure(self):
        """确保目录结构存在"""
        dirs = [
            '00-Inbox', '01-Raw/articles', '01-Raw/meetings',
            '01-Raw/imported-notes', '01-Raw/daily-journal',
            '02-Wiki/概念', '02-Wiki/人物', '02-Wiki/工具',
            '02-Wiki/方法论', '02-Wiki/项目', '02-Wiki/领域',
            '03-Outputs/文章', '03-Outputs/复盘', '03-Outputs/数据',
            '10-Projects', '20-Areas', '30-Resources/Templates',
            '40-Archive', 'Attachments'
        ]
        for d in dirs:
            os.makedirs(os.path.join(self.vault_path, d), exist_ok=True)
        print("✅ 目录结构已就绪")
    
    def classify_file(self, content, filename):
        """根据内容分类文件"""
        content_lower = content.lower()
        
        if any(kw in content_lower for kw in ['会议', 'meeting', 'agenda', 'minutes']):
            return '01-Raw/meetings/'
        if re.search(r'\d{4}[-/]?\d{1,2}[-/]?\d{1,2}', filename):
            return '01-Raw/daily-journal/'
        if 'http://' in content or 'https://' in content or '<article>' in content_lower:
            return '01-Raw/articles/'
        if any(kw in content_lower for kw in ['definit', '概念', '原理', '理论']):
            return '02-Wiki/概念/'
        if any(kw in content_lower for kw in ['代码', 'api', '工具', 'plugin', 'library']):
            return '02-Wiki/工具/'
        return '01-Raw/imported-notes/'
    
    def clean_and_migrate(self, src_path):
        """清洗并迁移单个文件"""
        filename = Path(src_path).name
        content = self.read_file(src_path)
        
        if content is None:
            self.stats['errors'] += 1
            return
        
        # 分类
        category = self.classify_file(content, filename)
        self.stats['by_category'][category] = self.stats['by_category'].get(category, 0) + 1
        
        # 清洗 Frontmatter
        content = self.fix_frontmatter(content, filename)
        
        # 清洗内容
        content = self.clean_content(content)
        
        # 确保标题
        content = self.ensure_heading(content, filename)
        
        # 写入目标
        target_path = os.path.join(self.vault_path, category, filename)
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.stats['processed'] += 1
    
    def read_file(self, path):
        for enc in ['utf-8', 'gbk', 'gb2312', 'latin-1']:
            try:
                with open(path, 'r', encoding=enc) as f:
                    return f.read()
            except (UnicodeDecodeError, UnicodeError):
                continue
        return None
    
    def fix_frontmatter(self, content, filename):
        now = datetime.now().strftime('%Y-%m-%d')
        match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        fm = {}
        body = content
        
        if match:
            body = content[match.end():].lstrip('\n')
            for line in match.group(1).split('\n'):
                if ':' in line:
                    k, _, v = line.partition(':')
                    fm[k.strip()] = v.strip()
        
        defaults = {
            'title': f'"{Path(filename).stem}"',
            'tags': '[未分类]',
            'created': now,
            'updated': now,
            'source': f'"导入"',
            'status': 'raw'
        }
        for k, v in defaults.items():
            if k not in fm:
                fm[k] = v
        
        for k in fm:
            v = fm[k]
            if '[[' in str(v) and not v.startswith('"'):
                fm[k] = f'"{v}"'
        
        new_fm = "---\n"
        for k in ['title', 'tags', 'created', 'updated', 'source', 'status']:
            if k in fm:
                new_fm += f"{k}: {fm[k]}\n"
        for k in fm:
            if k not in defaults:
                new_fm += f"{k}: {fm[k]}\n"
        new_fm += "---\n\n"
        return new_fm + body
    
    def clean_content(self, body):
        body = re.sub(r'\n{3,}', '\n\n', body)
        body = re.sub(r'<br\s*/?>', '\n', body)
        body = re.sub(r'</?div[^>]*>', '\n', body)
        body = re.sub(r'</?span[^>]*>', '', body)
        return body
    
    def ensure_heading(self, content, filename):
        if not re.search(r'^# ', content, re.MULTILINE):
            title = Path(filename).stem
            match = re.match(r'^(---\n.*?\n---\n\n?)', content, re.DOTALL)
            if match:
                return match.group(1) + f"# {title}\n\n" + content[match.end():]
            return f"# {title}\n\n" + content
        return content
    
    def scan_and_clean(self):
        """扫描源目录并清洗"""
        for root, _, files in os.walk(self.source_dir):
            for f in files:
                if f.endswith(('.md', '.txt')):
                    self.stats['total'] += 1
                    self.clean_and_migrate(os.path.join(root, f))
    
    def fix_broken_links(self):
        """修复死链"""
        # 收集所有存在的文件名
        existing = set()
        for root, _, files in os.walk(self.vault_path):
            for f in files:
                if f.endswith('.md'):
                    existing.add(Path(f).stem)
        
        # 检查并修复
        for root, _, files in os.walk(self.vault_path):
            for f in files:
                if not f.endswith('.md'):
                    continue
                path = os.path.join(root, f)
                with open(path, 'r', encoding='utf-8') as fp:
                    content = fp.read()
                
                links = re.findall(r'\[\[([^\]|]+)(?:\|([^\]]+))?\]\]', content)
                modified = False
                for target, alias in links:
                    if target.strip() not in existing:
                        self.stats['broken_links'].append({
                            'file': f, 'target': target
                        })
                        # 替换为纯文本
                        old_link = f"[[{target}{'|' + alias if alias else ''}]]"
                        new_text = alias if alias else target
                        content = content.replace(old_link, new_text)
                        modified = True
                
                if modified:
                    with open(path, 'w', encoding='utf-8') as fp:
                        fp.write(content)
    
    def generate_moc(self):
        """生成仪表盘"""
        # 收集所有 Wiki 笔记
        wiki_notes = {'概念': [], '人物': [], '工具': [], '方法论': [], '项目': []}
        for cat in wiki_notes:
            cat_path = os.path.join(self.vault_path, '02-Wiki', cat)
            if os.path.exists(cat_path):
                for f in os.listdir(cat_path):
                    if f.endswith('.md'):
                        wiki_notes[cat].append(Path(f).stem)
        
        moc = f"""---
tags: [MOC, 仪表盘]
created: "{datetime.now().strftime('%Y-%m-%d')}"
updated: "{datetime.now().strftime('%Y-%m-%d')}"
---

# 🧠 第二大脑仪表盘

> 自动生成于 {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 📊 知识概览
| 类别 | 数量 |
|------|------|
| 概念 | {len(wiki_notes['概念'])} |
| 人物 | {len(wiki_notes['人物'])} |
| 工具 | {len(wiki_notes['工具'])} |
| 方法论 | {len(wiki_notes['方法论'])} |
| 项目 | {len(wiki_notes['项目'])} |

"""
        for cat, notes in wiki_notes.items():
            if notes:
                moc += f"## {cat}\n"
                for n in notes:
                    moc += f"- [[{n}]]\n"
                moc += "\n"
        
        with open(os.path.join(self.vault_path, '00-大脑仪表盘.md'), 'w', encoding='utf-8') as f:
            f.write(moc)
        print("✅ 仪表盘已生成")
    
    def generate_report(self):
        """生成体检报告"""
        report = f"""# 🏥 知识库体检报告

**检查日期**: {datetime.now().strftime('%Y-%m-%d')}
**总处理文件数**: {self.stats['processed']}/{self.stats['total']}
**错误数**: {self.stats['errors']}

## 分类统计
"""
        for cat, count in self.stats['by_category'].items():
            report += f"- {cat}: {count}\n"
        
        if self.stats['broken_links']:
            report += f"\n## ⚠️ 死链 ({len(self.stats['broken_links'])} 个)\n"
            for link in self.stats['broken_links']:
                report += f"- [[{link['target']}]] 不存在，来源: {link['file']}\n"
        
        report_path = os.path.join(self.vault_path, '03-Outputs/复盘', f"知识库体检_{datetime.now().strftime('%Y-%m-%d')}.md")
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"✅ 体检报告已写入: {report_path}")


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("用法: python obsidian_builder.py <source_dir> <vault_path>")
        sys.exit(1)
    
    builder = ObsidianBuilder(sys.argv[1], sys.argv[2])
    builder.run()
```

### B. 标签映射字典模板

> 模板参考：`references/tag-mapping-template.json`

### C. Python 依赖

脚本需要的依赖：
```bash
pip install pyyaml  # 可选，用于更严格的 YAML 解析
```
脚本本身只使用 Python 标准库，无需额外安装。

---

## 📎 References 文件索引

| 文件 | 用途 |
|------|------|
| `references/schema-template.md` | LLM 知识库规则说明书 (CLAUDE.md) |
| `references/moc-template.md` | 全局仪表盘模板 |
| `references/project-dashboard-template.md` | 项目 Dashboard 模板 |
| `references/yaml-fix-guide.md` | YAML 报错排查指南 |
| `references/tag-mapping-template.json` | 标签层级映射模板 |

---

> **Skill 维护**：当发现新的目录结构问题、YAML 坑或清洗场景时，请立即更新此 Skill。保持工具的锋利度。
