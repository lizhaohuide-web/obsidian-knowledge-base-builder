---
tags: [索引, 知识库, Schema]
updated: "{{date}}"
source: "系统"
---

# 🧠 [用户昵称] 的第二大脑 - Schema (CLAUDE.md)

> **Instructions for LLM**: Read this file before processing any requests related to this knowledge base. This file defines the operating system for the vault.

## 1. 核心原则 (Core Principles)

- **Input ≠ Knowledge**: Raw notes are not knowledge. Knowledge is compiled.
- **Zero Friction Input**: Users drop things in `00-Inbox` or `01-Raw`. No sorting required.
- **Machine Readable**: All files must have valid Frontmatter.
- **Single Source of Truth**: Each entity exists in ONE place. Use links, not copies.
- **Knowledge Flows**: `Inbox` → `Raw` → `Wiki` → `Projects` → `Outputs` → `Archive`
- **Never Delete Raw**: Raw 是原始记录，永远不删除，只通过链接引用。

## 2. 目录结构 (Structure)

| Directory | Purpose | LLM Action |
|-----------|---------|------------|
| `00-Inbox/` | Quick capture | **Process Daily** - extract entities, move to Raw |
| `01-Raw/` | Unprocessed content | **Keep as is**, link from Wiki |
| `02-Wiki/` | Structured Knowledge | **Compile** from Raw, maintain links |
| `03-Outputs/` | Finished products | **Archive** results, link from Projects |
| `10-Projects/` | Active work | **Update** frequently, track status |
| `20-Areas/` | Ongoing responsibilities | **Review** periodically |
| `30-Resources/` | Templates, references | **Read** for templates |
| `40-Archive/` | Completed work | **Move here** when done |
| `Attachments/` | Images, PDFs, media | **Store** all media here |

### Wiki 子目录
- `02-Wiki/概念/` — 抽象概念（定义、理论、原理）
- `02-Wiki/人物/` — 关键人物（专家、历史人物、同事）
- `02-Wiki/工具/` — 软件、API、模型、书籍
- `02-Wiki/方法论/` — 可复用的流程、SOP、框架
- `02-Wiki/项目/` — 项目级的 Wiki 仪表盘
- `02-Wiki/领域/` — 领域知识聚合

## 3. Frontmatter Standards

Every file MUST have this header:

```yaml
---
title: "文件名"
tags: [category/sub-category]
created: YYYY-MM-DD
updated: YYYY-MM-DD
source: "[[Source File]] or URL"
status: raw | processing | compiled
---
```

**Rules**:
- `[[...]]` in YAML values must be quoted: `source: "[[Note]]"`
- All dates: `YYYY-MM-DD` format
- Tags: hierarchical, no flat noise tags
- Status: `raw` (刚导入), `processing` (正在编译), `compiled` (已精炼)

## 4. Linking Strategy

- **Internal**: Use `[[Note Name]]` (Wikilinks, NOT Markdown links)
- **With Alias**: Use `[[Note Name|显示名称]]`
- **External**: Use `[Link Text](URL)`
- **Attachments**: Use `![Alt](../Attachments/filename.png)`
- **Broken Links**: If target doesn't exist, report it or create a stub

## 5. Compilation Rules (For LLM)

When asked to "Compile" or "Organize":

1. Scan `00-Inbox` and `01-Raw`
2. Extract entities (Concepts, People, Tools, Methods)
3. Create/Update files in `02-Wiki/{category}/`
4. Update `02-Wiki/_index.md`
5. Update `00-大脑仪表盘.md`
6. **Never delete** a source file in Raw
7. Add backlinks: `## 🔗 反向链接` section to referenced notes

## 6. Tag Taxonomy

Tags must be hierarchical:

```
AI/基础, AI/模型, AI/Agent, AI/RAG, AI/Prompt
新媒体/小红书, 新媒体/公众号, 新媒体/抖音
个人成长/读书, 个人成长/思维, 个人成长/复盘
编程/Python, 编程/JavaScript, 编程/前端, 编程/后端
玄学/八字, 玄学/紫微斗数, 玄学/奇门遁甲
宗教/佛教, 宗教/禅修
```

**Delete these noise tags**: `概念`, `工具`, `项目`, `会议`, `TODO`, `草稿`, `临时`, `未分类`

## 7. Templates

Templates are in `30-Resources/Templates/`:
- `daily-note.md` — 日记模板
- `new-concept.md` — 新概念模板
- `new-project.md` — 新项目模板

Use Templater syntax: `{{title}}`, `{{date:YYYY-MM-DD}}`

## 8. Health Checks

Run these checks periodically:
- [ ] All files have valid YAML Frontmatter
- [ ] No broken `[[links]]`
- [ ] `00-Inbox` is empty (or near empty)
- [ ] No active projects in `40-Archive`
- [ ] No Raw materials in `02-Wiki`
- [ ] Tags are hierarchical (no flat noise)
