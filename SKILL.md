---
name: obsidian-knowledge-base-builder
description: |
  帮助任何用户从 0 到 1 搭建、清洗、梳理 Obsidian 知识库的全流程 Skill。
  基于 Karpathy LLM Wiki 架构 + PARA 管理法。
  适用于：新 Vault 初始化、旧笔记迁移、混乱知识库重构、标准化现有笔记。
  触发词：搭建知识库、初始化 Obsidian、梳理笔记、编译知识库、修复死链、标签规范化、知识库体检
---

# Obsidian 知识库搭建与重构 (v3.0)

> **核心原则**：知识库不是静态仓库，而是**动态处理器**。Input 必须流向 Process 并产出 Output。
> **设计哲学**：Karpathy LLM Wiki "Input → Compile → Wiki" + PARA 行动导向架构。
> **适用对象**：任何希望建立结构化、可维护、支持 LLM 辅助管理的个人/团队知识库的用户。

---

## 📋 执行流程总览

```
Phase 0: 环境准备 → 确认 Obsidian + Vault 就绪
Phase 1: 目录结构初始化 → 建立 PARA+Wiki 骨架
Phase 2: 数据清洗 → 源目录扫描 → 分类 → 标准化 → 迁移
Phase 3: 关联网络构建 → 死链修复 → MOC 仪表盘 → 索引
Phase 4: 验证与体检 → Lint 检查 → 输出报告
Phase 5: 自动化 → Cron 定时编译 → 持续维护
```

**核心工具**: `scripts/obsidian_builder.py`（Phase 1-4 全自动，纯标准库无依赖）

```bash
python3 scripts/obsidian_builder.py --source <源目录> --vault <Vault路径>
```

**⚠️ 关键交互点**：
- Phase 0 结束 → 向用户确认 Vault 路径
- Phase 2 开始 → 必须拿到用户的源笔记目录路径

---

## 🔧 Phase 0: 环境准备

**目标**：确保 Obsidian 已安装、Vault 已创建、Agent 有读写权限。

### 0.1 安装与创建 Vault

Agent 根据用户 OS 提供对应安装指引（从 [obsidian.md](https://obsidian.md) 下载）。

**Vault 命名建议**: `Second-Brain` 或 `{姓名}-Wiki`
**推荐路径**: `~/Documents/Second-Brain/` (macOS) / `~/Obsidian/Second-Brain/` (Linux)

→ 记录为 `{vault_path}`，后续所有操作基于此。

### 0.2 核心插件

**必装（社区插件）**:

| 插件 | 用途 |
|------|------|
| Templater | 模板引擎，支持 JS 变量 |
| Dataview | 查询和展示笔记数据 |
| Auto Note Mover | 按标签/路径自动归档 |
| Linter | 自动格式化 Markdown + YAML |
| Calendar | 日历视图，辅助 Daily Notes |

**推荐（可选）**: Copilot（本地 LLM）、Smart Connections（语义搜索）、Obsidian Git（版本控制）

### 0.3 关键设置

1. **文件与链接**: 新笔记默认位置 → `00-Inbox`，附件 → `Attachments/`，使用 `[[Wikilinks]]`
2. **Linter**: YAML 时间格式 `YYYY-MM-DD`，启用 YAML Title + Timestamp
3. **Templater**: 模板目录 → `30-Resources/Templates/`

### 0.4 就绪检查

- [ ] Obsidian 已安装，Vault 已创建
- [ ] `{vault_path}` Agent 可读写
- [ ] Templater + Dataview + Linter 已安装
- [ ] 用户已提供源笔记目录 `{source_dir}`

---

## 🏗️ Phase 1: 目录结构初始化

**目标**：建立 PARA+Wiki 标准骨架。

### 标准目录树

```text
{vault_path}/
├── 00-Inbox/              # 📥 速记收件箱（未分类，定期清理）
├── 01-Raw/                # 📦 原始素材（Input）
│   ├── articles/          #    文章剪藏
│   ├── meetings/          #    会议记录
│   ├── imported-notes/    #    导入笔记
│   └── daily-journal/     #    日记
├── 02-Wiki/               # 🧠 编译维基（Process/Output）
│   ├── CLAUDE.md          #    LLM 必读 Schema
│   ├── _index.md          #    全量索引（自动维护）
│   ├── 概念/  人物/  工具/  方法论/  项目/  领域/
├── 03-Outputs/            # 📤 产出（文章/复盘/数据）
├── 10-Projects/           # 🔥 活跃项目
├── 20-Areas/              # 🌍 关注领域
├── 30-Resources/Templates/ # 📚 模板目录
├── 40-Archive/            # 🗄️ 归档
└── Attachments/           # 📎 附件
```

### 核心规则

1. **Raw ≠ Wiki**: Raw 是原材料，Wiki 是加工品，用链接关联，**不复制内容**
2. **Projects vs Archive**: 活跃项目绝不能在 Archive 里
3. **Inbox 清空**: 定期处理，不堆积
4. **Attachments 隔离**: 图片/PDF 统一存放

### 基础模板

Agent 在 `30-Resources/Templates/` 创建三个基础模板：
- `daily-note.md` — 日记（今日重点 + 随手记 + 复盘）
- `new-concept.md` — 概念（定义 + 要点 + 关联 + 场景）
- `new-project.md` — 项目（目标 + 里程碑 + 文档 + 复盘）

### CLAUDE.md（知识库 Schema）

在 `02-Wiki/CLAUDE.md` 写入知识库规则说明书。
→ 模板参考: `references/schema-template.md`

---

## 🧹 Phase 2: 数据清洗与规范化

**目标**：将 `{source_dir}` 清洗、标准化后迁移到 `{vault_path}`。

### 一键执行

```bash
# 完整清洗 + 迁移
python3 scripts/obsidian_builder.py --source {source_dir} --vault {vault_path}

# 只扫描不写入（预览模式）
python3 scripts/obsidian_builder.py --source {source_dir} --vault {vault_path} --dry-run
```

脚本自动完成以下步骤：

### 2.1 扫描与评估

递归扫描 `{source_dir}`，输出统计报告（文件类型、数量、时间跨度）。

### 2.2 自动分类路由

| 文件特征 | 目标目录 |
|----------|----------|
| 含 `会议/meeting/agenda` | `01-Raw/meetings/` |
| 文件名含日期模式 | `01-Raw/daily-journal/` |
| 含 URL 或 `<article>` | `01-Raw/articles/` |
| 含 定义/概念/原理/理论 | `02-Wiki/概念/` |
| 含 代码/API/工具/plugin | `02-Wiki/工具/` |
| 其他 | `01-Raw/imported-notes/` |

### 2.3 Frontmatter 标准化

每个 `.md` 文件确保有：

```yaml
---
title: "文件名"
tags: [分类/子分类]
created: YYYY-MM-DD
updated: YYYY-MM-DD
source: "来源"
status: raw | processing | compiled
---
```

**⚠️ YAML 常见坑**（详见 `references/yaml-fix-guide.md`）：
- 双括号必须加引号: `source: [[链接]]` → `source: "[[链接]]"`
- 含冒号的值必须加引号: `title: A: B` → `title: "A: B"`
- 缺失字段自动补默认值

### 2.4 标签体系层级化

**规则**: 扁平标签 → 层级标签（如 `AI` → `AI/工具`）

→ 映射模板: `references/tag-mapping-template.json`

**Agent 动作**:
1. 统计所有现有标签
2. 识别低频标签（仅 1-2 次），建议合并
3. 向用户展示映射方案，确认后执行

### 2.5 内容净化

- 连续 3+ 空行 → 1 个
- HTML 残留 (`<br>`, `<div>`, `<span>`) → Markdown
- 占位符 (`TODO`, `待补充`) → `> ⚠️ 待补充`
- 文件内重复段落 → 保留一份

### 2.6 消除重复 (Single Source of Truth)

- 文件名相同 / 内容相似度 > 85% → 保留最新
- Wiki 优先 > Projects 优先
- 被替代的文件改为重定向: `> ⚠️ 此笔记已迁移至 [[Wiki版本]]`

---

## 🔗 Phase 3: 关联网络构建

**目标**：消灭孤岛，建立 MOC。脚本自动处理死链修复和 MOC 生成。

### 3.1 死链修复

脚本自动执行：
1. 提取所有 `[[...]]` 链接
2. 目标文件不存在 → 替换为纯文本
3. 输出修复统计

### 3.2 MOC 仪表盘

脚本自动生成 `00-大脑仪表盘.md`（全局入口）。
→ 自定义模板: `references/moc-template.md`

### 3.3 项目页仪表盘化

`02-Wiki/项目/` 下的页面必须是 **Dashboard**，不是简介。
→ 模板: `references/project-dashboard-template.md`

### 3.4 全量索引

生成 `02-Wiki/_index.md`：按类型分组 + 按标签分组 + 孤立页面列表。

### 3.5 双向链接优化

- 高引用笔记（被引 3+ 次）→ 底部添加反向链接区域
- 孤立页面 → 根据内容自动链接到相关笔记

---

## 🔍 Phase 4: 验证与体检

**目标**：确保健康度，脚本自动生成体检报告到 `03-Outputs/复盘/`。

### 检查指标

| 指标 | 目标值 |
|------|--------|
| YAML 通过率 | 100% |
| 属性完整率 | >95% |
| 死链数 | 0 |
| 孤立页面率 | <10% |
| 目录合规性 | 100% |
| 标题一致性 | 100% |
| 标签规范率 | >90% |

---

## 🤖 Phase 5: 自动化配置

若环境支持 Cron：
- **每日编译**: 扫描 Inbox + Raw → 实体提取 → 更新 Wiki
- **每周体检**: Lint 检查（矛盾/孤儿页/过期内容）
- **每月归档**: 30 天无更新的项目 → Archive

---

## 📎 References 文件索引

| 文件 | 用途 |
|------|------|
| `references/schema-template.md` | LLM 知识库规则说明书 (CLAUDE.md) |
| `references/moc-template.md` | 全局仪表盘模板 |
| `references/project-dashboard-template.md` | 项目 Dashboard 模板 |
| `references/yaml-fix-guide.md` | YAML 报错排查指南 |
| `references/tag-mapping-template.json` | 标签层级映射模板 |
| `scripts/obsidian_builder.py` | 一键清洗+迁移+体检脚本（纯标准库） |

---

## ⚠️ Pitfalls

1. **编码问题**: 源笔记可能是 GBK/GB2312（尤其 Windows 导出），脚本已内置多编码检测
2. **YAML 双括号**: Obsidian 的 `[[wikilink]]` 在 YAML 中必须加引号，否则解析失败
3. **Notion/Evernote 导入**: 这类工具导出的 Markdown 常有 HTML 残留，脚本已处理
4. **标签删除要谨慎**: 代表目录分类的标签（`#概念`, `#工具`）应删除（信息已由目录承载），但要先跟用户确认
5. **文件名特殊字符**: Windows 不允许 `/ \ : * ? " < > |`，迁移时需重命名

> **维护**: 发现新的目录结构问题、YAML 坑或清洗场景时，立即更新此 Skill。
