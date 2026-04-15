# Obsidian 知识库搭建与重构

> 帮助任何用户从 0 到 1 搭建、清洗、梳理 Obsidian 知识库的全流程 Skill。
> 基于 Karpathy LLM Wiki 架构 + PARA 管理法。

## 触发词

`搭建知识库`、`初始化 Obsidian`、`梳理笔记`、`编译知识库`、`修复死链`、`标签规范化`、`知识库体检`

## 执行流程

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

## 目录结构

```
SKILL.md                          # 主指令文件
references/
├── schema-template.md            # LLM 知识库规则说明书
├── moc-template.md               # 全局仪表盘模板
├── project-dashboard-template.md # 项目 Dashboard 模板
├── yaml-fix-guide.md             # YAML 报错排查指南
└── tag-mapping-template.json     # 标签层级映射模板
```

## 安装

将本仓库克隆到 `~/.hermes/skills/knowledge-management/obsidian-knowledge-base-builder/`。

## License

MIT
