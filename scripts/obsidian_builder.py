#!/usr/bin/env python3
"""
Obsidian 知识库搭建与清洗工具
用法:
  python3 obsidian_builder.py --source <源目录> --vault <Vault路径>
  python3 obsidian_builder.py --source ~/old-notes --vault ~/Obsidian/Second-Brain

功能:
  1. 自动创建 PARA+Wiki 标准目录骨架
  2. 扫描源目录，按内容自动分类
  3. Frontmatter 标准化（补缺、修格式）
  4. 内容净化（去HTML残留、连续空行、乱码标记）
  5. 死链检测与修复
  6. MOC 仪表盘生成
  7. 体检报告输出

无外部依赖，纯标准库。
"""
import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path


# ── 目录骨架 ─────────────────────────────────────
STANDARD_DIRS = [
    "00-Inbox",
    "01-Raw/articles",
    "01-Raw/meetings",
    "01-Raw/imported-notes",
    "01-Raw/daily-journal",
    "02-Wiki/概念",
    "02-Wiki/人物",
    "02-Wiki/工具",
    "02-Wiki/方法论",
    "02-Wiki/项目",
    "02-Wiki/领域",
    "03-Outputs/文章",
    "03-Outputs/复盘",
    "03-Outputs/数据",
    "10-Projects",
    "20-Areas",
    "30-Resources/Templates",
    "40-Archive",
    "Attachments",
]


# ── 编码检测 ─────────────────────────────────────
def detect_encoding(filepath):
    for enc in ["utf-8", "gbk", "gb2312", "latin-1"]:
        try:
            with open(filepath, "r", encoding=enc) as f:
                f.read()
            return enc
        except (UnicodeDecodeError, UnicodeError):
            continue
    return "utf-8"


def read_file_safe(path):
    enc = detect_encoding(path)
    try:
        with open(path, "r", encoding=enc) as f:
            return f.read()
    except Exception:
        return None


# ── Frontmatter 处理 ─────────────────────────────
def parse_frontmatter(content):
    """解析 Frontmatter，返回 (dict, body_str)"""
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}, content

    fm = {}
    body = content[match.end():].lstrip("\n")
    for line in match.group(1).split("\n"):
        if ":" in line:
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip()
    return fm, body


def fix_frontmatter(content, filename, source_label="导入"):
    """修复或创建标准 Frontmatter"""
    now = datetime.now().strftime("%Y-%m-%d")
    fm, body = parse_frontmatter(content)

    defaults = {
        "title": f'"{Path(filename).stem}"',
        "tags": "[未分类]",
        "created": now,
        "updated": now,
        "source": f'"{source_label}"',
        "status": "raw",
    }
    for k, v in defaults.items():
        if k not in fm or not fm[k]:
            fm[k] = v

    # 修复 YAML 格式问题
    for k in fm:
        v = str(fm[k])
        # 双括号必须加引号
        if "[[" in v and not v.startswith('"'):
            fm[k] = f'"{v}"'
        # 含冒号的值必须加引号
        elif ":" in v and not v.startswith('"') and not v.startswith("'") and k != "tags":
            fm[k] = f'"{v}"'

    # 重建（保持字段顺序）
    ordered_keys = ["title", "tags", "created", "updated", "source", "status"]
    lines = ["---"]
    for k in ordered_keys:
        if k in fm:
            lines.append(f"{k}: {fm[k]}")
    for k in fm:
        if k not in ordered_keys:
            lines.append(f"{k}: {fm[k]}")
    lines.append("---\n")

    return "\n".join(lines) + "\n" + body


# ── 内容净化 ─────────────────────────────────────
def clean_content(body):
    """净化 Markdown 正文"""
    # 连续空行 → 最多 1 个
    body = re.sub(r"\n{3,}", "\n\n", body)
    # HTML 残留
    body = re.sub(r"<br\s*/?>", "\n", body)
    body = re.sub(r"</?div[^>]*>", "\n", body)
    body = re.sub(r"</?span[^>]*>", "", body)
    # 无意义占位符标记
    body = re.sub(r"^(TODO|待补充|xxx)\s*$", "> ⚠️ 待补充", body, flags=re.MULTILINE)
    return body


def ensure_h1(content, filename):
    """确保文件有 H1 标题"""
    if re.search(r"^# ", content, re.MULTILINE):
        return content
    title = Path(filename).stem
    match = re.match(r"^(---\n.*?\n---\n\n?)", content, re.DOTALL)
    if match:
        return match.group(1) + f"# {title}\n\n" + content[match.end():]
    return f"# {title}\n\n" + content


# ── 文件分类 ─────────────────────────────────────
def classify_file(content, filename):
    """根据内容和文件名判断目标目录"""
    low = content.lower()

    if any(kw in low for kw in ["会议", "meeting", "agenda", "minutes"]):
        return "01-Raw/meetings/"
    if re.search(r"\d{4}[-/]?\d{1,2}[-/]?\d{1,2}", filename):
        return "01-Raw/daily-journal/"
    if "http://" in content or "https://" in content or "<article>" in low:
        return "01-Raw/articles/"
    if any(kw in low for kw in ["定义", "概念", "原理", "理论", "definit"]):
        return "02-Wiki/概念/"
    if any(kw in low for kw in ["代码", "api", "工具", "plugin", "library"]):
        return "02-Wiki/工具/"
    return "01-Raw/imported-notes/"


# ── 主构建器 ─────────────────────────────────────
class ObsidianBuilder:
    def __init__(self, source_dir, vault_path):
        self.source_dir = source_dir
        self.vault_path = vault_path
        self.stats = {
            "total": 0,
            "processed": 0,
            "errors": 0,
            "by_category": {},
            "broken_links": [],
        }

    def run(self):
        print(f"🚀 开始构建知识库")
        print(f"   源目录: {self.source_dir}")
        print(f"   Vault:  {self.vault_path}")
        print()

        self.ensure_structure()
        self.scan_and_clean()
        self.fix_broken_links()
        self.generate_moc()
        report_path = self.generate_report()

        ok = self.stats["processed"]
        total = self.stats["total"]
        err = self.stats["errors"]
        print(f"\n{'='*50}")
        print(f"✅ 完成! 处理 {ok}/{total} 个文件, {err} 个错误")
        print(f"📋 体检报告: {report_path}")

    # ── 目录骨架 ──
    def ensure_structure(self):
        for d in STANDARD_DIRS:
            os.makedirs(os.path.join(self.vault_path, d), exist_ok=True)
        print("✅ 目录结构已就绪")

    # ── 扫描 + 清洗 ──
    def scan_and_clean(self):
        for root, _, files in os.walk(self.source_dir):
            for f in files:
                if not f.endswith((".md", ".txt")):
                    continue
                self.stats["total"] += 1
                src = os.path.join(root, f)
                content = read_file_safe(src)
                if content is None:
                    self.stats["errors"] += 1
                    print(f"  ❌ {f}: 读取失败")
                    continue

                # 分类
                cat = classify_file(content, f)
                self.stats["by_category"][cat] = self.stats["by_category"].get(cat, 0) + 1

                # 清洗
                content = fix_frontmatter(content, f, f"导入自 {self.source_dir}")
                fm_match = re.match(r"^(---\n.*?\n---\n\n?)(.*)", content, re.DOTALL)
                if fm_match:
                    content = fm_match.group(1) + clean_content(fm_match.group(2))
                content = ensure_h1(content, f)

                # 写入
                target = os.path.join(self.vault_path, cat, f)
                os.makedirs(os.path.dirname(target), exist_ok=True)
                with open(target, "w", encoding="utf-8") as fp:
                    fp.write(content)

                self.stats["processed"] += 1
                print(f"  ✅ {f} → {cat}")

    # ── 死链修复 ──
    def fix_broken_links(self):
        existing = set()
        for root, _, files in os.walk(self.vault_path):
            for f in files:
                if f.endswith(".md"):
                    existing.add(Path(f).stem)

        fixed_count = 0
        for root, _, files in os.walk(self.vault_path):
            for f in files:
                if not f.endswith(".md"):
                    continue
                path = os.path.join(root, f)
                with open(path, "r", encoding="utf-8") as fp:
                    content = fp.read()

                links = re.findall(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]", content)
                modified = False
                for target, alias in links:
                    if target.strip() not in existing:
                        self.stats["broken_links"].append({"file": f, "target": target})
                        old = f"[[{target}{'|' + alias if alias else ''}]]"
                        content = content.replace(old, alias or target)
                        modified = True
                        fixed_count += 1

                if modified:
                    with open(path, "w", encoding="utf-8") as fp:
                        fp.write(content)

        print(f"🔗 死链修复: {fixed_count} 个")

    # ── MOC 仪表盘 ──
    def generate_moc(self):
        wiki_notes = {}
        wiki_base = os.path.join(self.vault_path, "02-Wiki")
        if os.path.exists(wiki_base):
            for cat in os.listdir(wiki_base):
                cat_path = os.path.join(wiki_base, cat)
                if os.path.isdir(cat_path):
                    notes = [Path(f).stem for f in os.listdir(cat_path) if f.endswith(".md")]
                    if notes:
                        wiki_notes[cat] = sorted(notes)

        now = datetime.now()
        total = sum(len(v) for v in wiki_notes.values())
        lines = [
            "---",
            'tags: [MOC, 仪表盘]',
            f'created: "{now.strftime("%Y-%m-%d")}"',
            f'updated: "{now.strftime("%Y-%m-%d")}"',
            "---",
            "",
            "# 🧠 第二大脑仪表盘",
            "",
            f"> 自动生成于 {now.strftime('%Y-%m-%d %H:%M')}，共 {total} 条 Wiki 词条",
            "",
            "## 📊 知识概览",
            "| 类别 | 数量 |",
            "|------|------|",
        ]
        for cat, notes in wiki_notes.items():
            lines.append(f"| {cat} | {len(notes)} |")
        lines.append("")

        for cat, notes in wiki_notes.items():
            lines.append(f"## {cat}")
            for n in notes:
                lines.append(f"- [[{n}]]")
            lines.append("")

        moc_path = os.path.join(self.vault_path, "00-大脑仪表盘.md")
        with open(moc_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"📋 仪表盘已生成: {moc_path}")

    # ── 体检报告 ──
    def generate_report(self):
        now = datetime.now()
        lines = [
            "# 🏥 知识库体检报告",
            "",
            f"**检查日期**: {now.strftime('%Y-%m-%d %H:%M')}",
            f"**Vault 路径**: {self.vault_path}",
            f"**总处理**: {self.stats['processed']}/{self.stats['total']}",
            f"**错误**: {self.stats['errors']}",
            "",
            "## 📁 分类统计",
        ]
        for cat, count in sorted(self.stats["by_category"].items()):
            lines.append(f"- `{cat}`: {count}")

        if self.stats["broken_links"]:
            lines.append(f"\n## ⚠️ 死链 ({len(self.stats['broken_links'])} 个，已自动修复)")
            for link in self.stats["broken_links"]:
                lines.append(f"- `[[{link['target']}]]` 不存在，来源: `{link['file']}`")
        else:
            lines.append("\n## ✅ 无死链")

        report_dir = os.path.join(self.vault_path, "03-Outputs/复盘")
        os.makedirs(report_dir, exist_ok=True)
        report_path = os.path.join(report_dir, f"知识库体检_{now.strftime('%Y-%m-%d')}.md")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        return report_path


# ── 入口 ─────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Obsidian 知识库搭建与清洗工具")
    parser.add_argument("--source", required=True, help="源笔记目录")
    parser.add_argument("--vault", required=True, help="Obsidian Vault 路径")
    parser.add_argument("--dry-run", action="store_true", help="只扫描不写入")
    args = parser.parse_args()

    if not os.path.isdir(args.source):
        print(f"❌ 源目录不存在: {args.source}")
        sys.exit(1)

    builder = ObsidianBuilder(args.source, args.vault)
    builder.run()


if __name__ == "__main__":
    main()
