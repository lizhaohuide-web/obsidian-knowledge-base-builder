# Obsidian 知识库搭建与重构

> 🧠 帮助任何用户从 0 到 1 搭建、清洗、梳理 Obsidian 知识库的全流程 Skill。
> 基于 **Karpathy LLM Wiki** 架构 + **PARA** 管理法。

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Skill Version](https://img.shields.io/badge/Version-2.0-blue.svg)](SKILL.md)

---

## ✨ 核心能力

| 能力 | 说明 |
|------|------|
| 🔧 **环境搭建** | 引导安装 Obsidian、创建 Vault、配置 AI 友好型插件 |
| 🏗️ **骨架初始化** | 自动创建 PARA + Wiki 混合目录结构 |
| 🧹 **数据清洗** | 扫描用户指定目录 → 自动分类 → 清洗内容 → 标准化 Frontmatter → 迁移 |
| 🔗 **关联网络** | 修复死链、生成 MOC 仪表盘、构建双向链接、消除重复 |
| 🔍 **健康体检** | YAML 校验、属性完整率、孤立页面检测、输出体检报告 |
| ⏰ **自动维护** | 每日编译、每周体检、每月归档的 Cron 建议 |

## 🚀 执行流程

```
Phase 0: 环境准备 (安装 Obsidian → 创建 Vault → 配置插件)
    ↓
Phase 1: 目录结构初始化 (建立 PARA+Wiki 骨架)
    ↓
Phase 2: 数据清洗 (用户指定目录 → 扫描 → 分类 → 清洗 → 标准化 → 迁移)
    ↓
Phase 3: 关联网络构建 (死链修复 → MOC 仪表盘 → 知识图谱)
    ↓
Phase 4: 验证与体检 (Lint 检查 → 输出报告)
    ↓
Phase 5: 自动化配置 (Cron 定时编译 → 持续维护)
```

## 📂 项目结构

```text
obsidian-knowledge-base-builder/
├── SKILL.md                          # 主指令文件（963 行，完整流程）
├── README.md                         # 本文件
├── LICENSE                           # MIT 许可证
├── .gitignore
└── references/
    ├── schema-template.md            # CLAUDE.md — LLM 必读的知识库规则说明书
    ├── moc-template.md               # 全局仪表盘模板（Map of Content）
    ├── project-dashboard-template.md # 项目 Dashboard 模板
    ├── yaml-fix-guide.md             # YAML 报错排查与修复指南（10 种错误 + 自动修复）
    └── tag-mapping-template.json     # 标签层级映射模板（含中文领域预设）
```

## 🎯 触发词

当用户提到以下任何词时，Agent 应自动加载此 Skill：

```
搭建知识库、初始化 Obsidian、梳理笔记、编译知识库、
修复死链、标签规范化、知识库体检、Obsidian 搭建、
第二大脑、PARA 整理、Karpathy Wiki
```

## 🛠️ 技术亮点

- **完整清洗脚本**：内置 `ObsidianBuilder` Python 类，支持扫描、分类、清洗、迁移、修复死链、生成仪表盘、输出体检报告
- **智能文件分类**：根据内容关键词自动判断文件类型（会议/日记/文章/概念/工具）
- **YAML 自动修复**：10 种常见 YAML 错误对照表 + 自动修复优先级 + 特殊场景处理（Notion 导出/旧版 Obsidian/含代码块）
- **标签层级映射**：预设 50+ 中文标签映射规则，自动将扁平标签转换为层级结构
- **双向链接优化**：自动检测高引用笔记，添加反向链接区域
- **Para+Wiki 混合架构**：结合 Karpathy 的 "Input → Compile → Wiki" 流水线 和 PARA 行动导向架构

## 📋 安装

### 作为 Hermes Skill 安装

```bash
cd ~/.hermes/skills/knowledge-management/
git clone https://github.com/lizhaohuide-web/obsidian-knowledge-base-builder.git
```

### 独立使用

直接阅读 `SKILL.md`，按 Phase 0 → Phase 5 的顺序执行即可。

## 📖 相关项目

- [Karpathy LLM Wiki](https://github.com/karpathy/llmwiki) — 原始灵感来源
- [PARA Method](https://www.fortelabs.com/blog/para/) — Tiago Forte 的知识管理方法论

## 📝 License

MIT License — 详见 [LICENSE](LICENSE)
