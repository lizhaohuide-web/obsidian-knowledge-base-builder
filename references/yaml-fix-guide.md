---
tags: [文档, YAML, 故障排除]
created: "{{date:YYYY-MM-DD}}"
updated: "{{date:YYYY-MM-DD}}"
source: "经验总结"
---

# YAML 修复指南

> **Context**: YAML parsing errors are the #1 reason LLMs fail to read/update Obsidian notes. This guide covers every known issue and its fix.

## 1. 常见错误与修复对照表

| # | 错误现象 | 错误示例 (Bad) | 正确示例 (Good) | 原因 |
| :--- | :--- | :--- | :--- | :--- |
| 1 | **双括号未引用** | `source: [[Note A]]` | `source: "[[Note A]]"` | `[[` 被 YAML 解析器误认为列表开始 |
| 2 | **多值未整体引用** | `source: [[A]], [[B]]` | `source: "[[A]], [[B]]"` | 逗号暗示列表但格式歧义 |
| 3 | **值中含冒号** | `title: My Note: Subtitle` | `title: "My Note: Subtitle"` | 冒号是 YAML 键值分隔符 |
| 4 | **模板变量** | `date: {{date}}` | `date: "{{date}}"` | 花括号是特殊字符 |
| 5 | **缺少空格** | `tags:[a, b]` | `tags: [a, b]` | YAML 要求冒号后有空格 |
| 6 | **中文字符无引号** | `title: 第一性原理` | `title: "第一性原理"` | 部分 YAML 解析器对中文字符敏感 |
| 7 | **URL 含特殊字符** | `url: https://x.com?a=1&b=2` | `url: "https://x.com?a=1&b=2"` | `&` 在 YAML 中有特殊含义 |
| 8 | **布尔值歧义** | `enabled: yes` | `enabled: true` | `yes`/`no` 在某些解析器中是布尔值 |
| 9 | **数字前导零** | `version: 0123` | `version: "0123"` | 前导零被解析为八进制 |
| 10 | **多行值** | `desc: 第一行\n第二行` | `desc: \|<br>  第一行<br>  第二行` | 换行需用 YAML 多行语法 |

## 2. 自动修复优先级

Agent 修复 YAML 时，按以下顺序执行：

1. **检测 Frontmatter 是否存在**
   - 没有 `---` 开头 → 在文件顶部插入标准 Frontmatter
   - 有开头无结尾 → 补上结尾 `---`

2. **尝试解析**
   - 使用 `yaml.safe_load()` 尝试解析
   - 成功 → 检查必要字段
   - 失败 → 进入正则修复

3. **正则修复（常见模式）**
   ```python
   # 修复双括号
   content = re.sub(r'(\w+):\s*\[\[([^\]]+)\]\]', r'\1: "[[\2]]"', content)
   # 修复多链接
   content = re.sub(r'(\w+):\s*\[\[.*?\]\].*\[\[', lambda m: fix_multi_link(m), content)
   # 修复冒号
   content = re.sub(r'(\w+):\s*([^"\'][^:]*:[^"\']*)$', r'\1: "\2"', content, flags=re.MULTILINE)
   ```

4. **补全缺失字段**
   - 按 `defaults` 字典逐一检查

5. **重建 YAML 块**
   - 按标准顺序输出：`title` → `tags` → `created` → `updated` → `source` → `status`

## 3. 特殊场景处理

### 3.1 从 Notion/Evernote 导出的笔记
- 这些笔记通常**没有 Frontmatter**
- 可能包含大量 HTML 标签
- 日期格式可能是 `2024年3月15日` 或 `Mar 15, 2024`
- **处理**：先转 Markdown，再补 Frontmatter

### 3.2 从 Obsidian 旧版本导出的笔记
- 可能使用了旧版 YAML 格式
- 可能有重复的 Frontmatter 块
- **处理**：保留最新的 Frontmatter 块，删除重复的

### 3.3 包含代码块的笔记
- 代码块中可能有 `---` 被误认为 Frontmatter 边界
- **处理**：用 `^---\n` 和 `\n---\n`（注意前后换行）精确匹配 Frontmatter

## 4. 手动检查清单 (Checklist)

- [ ] 每个文件以 `---` 开头（或第一行前有空行）
- [ ] 每个 Frontmatter 以 `---` 结束
- [ ] 所有键的冒号后有空格
- [ ] 所有含 `[[`、`:`、`,`、`&`、`{`、`}` 的值都用双引号包裹
- [ ] 日期格式统一为 `YYYY-MM-DD`
- [ ] 没有重复的 Frontmatter 块
- [ ] 标签使用层级格式 `[分类/子分类]`

## 5. 验证命令

```bash
# 快速检测哪些文件有 YAML 问题
python -c "
import yaml, sys, os
for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith('.md'):
            path = os.path.join(root, f)
            with open(path) as fp:
                content = fp.read()
            import re
            m = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
            if m:
                try:
                    yaml.safe_load(m.group(1))
                except Exception as e:
                    print(f'❌ {path}: {e}')
"
```
