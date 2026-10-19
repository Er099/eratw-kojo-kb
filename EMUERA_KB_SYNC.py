# -*- coding: utf-8 -*-
"""
把 Emuera 官方语法文档同步进 AI 知识库。

输入（由 EMUERA_DOC_INDEX.py 生成）：
    D:/F/口上制作尝试/emuera/AI_EMUERA_INDEX.txt
    D:/F/口上制作尝试/emuera/AI_EMUERA_ZH_ALL.txt

输出：
    04_emuera_syntax_index.md   387 篇索引（分类 + 表格，AI 定位用）
    05_emuera_syntax_full.md    387 篇中文全文（模糊检索 / 权威原文）

用法：
    python EMUERA_KB_SYNC.py
文档更新后重跑一次即可。
"""
import os
import re
import sys
import io

SRC_DIR = r"D:/F/口上制作尝试/emuera"
IDX_SRC = os.path.join(SRC_DIR, "AI_EMUERA_INDEX.txt")
ALL_SRC = os.path.join(SRC_DIR, "AI_EMUERA_ZH_ALL.txt")
OUT_DIR = os.path.dirname(os.path.abspath(__file__))
IDX_OUT = os.path.join(OUT_DIR, "04_emuera_syntax_index.md")
ALL_OUT = os.path.join(OUT_DIR, "05_emuera_syntax_full.md")


def esc(s):
    return s.replace("|", "\\|").strip()


def build_index():
    with io.open(IDX_SRC, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()
    out = []
    out.append("# Emuera 官方语法文档 · 索引（387 篇）\n")
    out.append("> 来源：`emuera.sk.doc` 重构版（原 evilmask 文档），由 `EMUERA_DOC_INDEX.py` 生成。\n")
    out.append("> 本地原文：`D:/F/口上制作尝试/emuera/emuera.sk.doc-feature-tutorial-restructure/docs/`\n")
    out.append("> 全文：同目录 `05_emuera_syntax_full.md`（1.8MB，搜 `===== FILE:` 定位）\n")
    out.append("\n## 怎么用\n")
    out.append("1. 先在本文件搜**命令名**（如 `PRINTFORM`、`SPLIT`、`ARRAYSHIFT`）。\n")
    out.append("2. 拿到「路径」后，去 `05_emuera_syntax_full.md` 里搜同名的 `===== FILE:` 段。\n")
    out.append("3. 索引里的「摘要」通常够判断是不是你要的那篇，不够再看全文。\n")
    out.append("\n> 口上高频语法的**提炼版**在 `00_core.md` 第 4 章，优先看那个；本索引是权威兜底。\n")

    cat = None
    rows = []
    total = 0

    def flush():
        nonlocal rows, total, cat
        if cat is None:
            return
        out.append("\n## %s\n" % cat)
        out.append("| 名称 | 标题 | 签名 | 摘要 | 路径 |")
        out.append("|---|---|---|---|---|")
        for r in rows:
            out.append("| %s |" % " | ".join(r))
        total += len(rows)
        rows = []
        cat = None

    for ln in lines:
        s = ln.strip()
        m = re.match(r"^【(.+?)】\s*(\d+)\s*篇$", s)
        if m:
            flush()
            cat = "%s（%s 篇）" % (m.group(1), m.group(2))
            continue
        if not s or s.startswith("=") or s.startswith("-") or s.startswith("用法") \
           or s.startswith("字段") or s.startswith("Emuera 语法文档索引") or s.startswith("整体模糊"):
            continue
        parts = [p.strip() for p in s.split(" | ")]
        if len(parts) != 5:
            continue
        name, title, sig, summ, path = parts
        rows.append([esc("`%s`" % name) if name else "",
                     esc(title), esc("`%s`" % sig) if sig else "",
                     esc(summ), esc("`%s`" % path.replace("\\", "/"))])
    flush()  # 最后一类也要输出

    out.append("\n---\n\n共 %d 篇。\n" % total)
    out.extend(build_reverse_lookup())
    with io.open(IDX_OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(out))
    return total


CMD_TOKEN = re.compile(r"`([A-Z][A-Z0-9_]{2,})`")
FILE_MARK = re.compile(r"^===== FILE:\s*(.+?)\s*$", re.M)


def build_reverse_lookup():
    """从全文合并文件里提取「反引号内的大写命令名 → 所在文档」，生成反查表。

    解决索引「名称」列粒度太粗的问题：比如 TRYC.zh.md 的名称列只写 `TRYC系`，
    但文档里实际讲了 TRYCALL / TRYCCALL / TRYCCALLFORM 等，AI 搜后者会 0 命中。
    """
    if not os.path.exists(ALL_SRC):
        return []
    with io.open(ALL_SRC, "r", encoding="utf-8") as f:
        body = f.read()

    marks = list(FILE_MARK.finditer(body))
    rev = {}
    for i, m in enumerate(marks):
        path = m.group(1).replace("\\", "/")
        seg_end = marks[i + 1].start() if i + 1 < len(marks) else len(body)
        for tok in CMD_TOKEN.findall(body[m.end():seg_end]):
            rev.setdefault(tok, set()).add(path)

    if not rev:
        return []

    out = ["", "---", "",
           "## 附录：命令反查表（%d 个命令）" % len(rev), "",
           "> 索引「名称」列只写文档标题，粒度较粗（例如 `TRYC.zh.md` 的名称是 `TRYC系`，",
           "> 但它同时讲了 `TRYCALL` / `TRYCCALL` / `TRYCCALLFORM`）。",
           "> **在主索引里搜不到某个命令时，先查这张表**——只要文档正文里以反引号出现过就会收录。", "",
           "| 命令 | 所在文档 |", "|---|---|"]
    for tok in sorted(rev):
        paths = sorted(rev[tok])
        show = paths[:3]
        cell = "<br>".join("`%s`" % p for p in show)
        if len(paths) > 3:
            cell += " 等 %d 篇" % len(paths)
        out.append("| `%s` | %s |" % (tok, cell))
    out.append("")
    return out


def build_all():
    with io.open(ALL_SRC, "r", encoding="utf-8") as f:
        body = f.read()

    header = (
        "# Emuera 官方语法文档 · 中文全文（387 篇）\n\n"
        "> 来源：`emuera.sk.doc` 重构版，由 `EMUERA_DOC_INDEX.py` 合并生成。\n"
        "> 本文件是**权威原文**，口上语法有疑问时以此为准。\n"
        "> 检索：搜 `===== FILE: docs/Reference/PRINTFORM.zh.md` 这种标记可跳到单篇。\n"
        "> 索引（更快定位）：`04_emuera_syntax_index.md`。\n"
        "> 口上高频语法提炼版：`00_core.md` 第 4 章。\n\n"
        "---\n\n"
    )
    # 去掉原文件自带的表头（到第一个 ==== FILE 分隔线之前）
    idx = body.find("===== FILE:")
    if idx > 0:
        # 回退到该行的分隔线起点
        start = body.rfind("\n====", 0, idx)
        body = body[start:] if start > 0 else body[idx:]
    with io.open(ALL_OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(header)
        f.write(body.lstrip("\n"))
    return len(body)


def main():
    for p in (IDX_SRC, ALL_SRC):
        if not os.path.exists(p):
            print("[ERR] 缺少源文件：%s" % p)
            print("      先跑 D:/F/口上制作尝试/emuera/EMUERA_DOC_INDEX.py")
            sys.exit(1)
    n1 = build_index()
    n2 = build_all()
    print("  [OK] 04_emuera_syntax_index.md  %d 篇  %.1f KB" % (n1, os.path.getsize(IDX_OUT) / 1024))
    print("  [OK] 05_emuera_syntax_full.md   %.1f KB" % (os.path.getsize(ALL_OUT) / 1024))


if __name__ == "__main__":
    main()
