# -*- coding: utf-8 -*-
"""
eraTW 口上知识库生成器  v1
=========================================================
生成三个按需分发的文件：
    01_模板索引.md   —— 所有口上模板函数的清单（函数名 / 行号 / 用途 / 指令编号反查）
    02_地点表.md     —— 643 个地点 ID（写 604 散步等按地点分的口上时用）
    03_147现状.md    —— 萨丽艾尔口上当前写到哪了（换 AI 时用）

用法：
    双击本文件；或在命令行执行
        python BUILD.py
    路径不对时改下面的 GAME / TEMPLATE_DIR / KOJO_DIR 三个常量。

注意：本脚本只读游戏目录，不修改任何游戏文件。
"""

import os
import re
import io
import sys

# ============ 路径配置（换电脑 / 换版本时改这里）============
BASE = os.path.dirname(os.path.abspath(__file__))

GAME = r"D:\F\口上制作尝试\AI代写代码测试\eraTW"
TEMPLATE_DIR = r"D:\F\口上制作尝试\TW口上汉化精修模版(4.954-4.97X)"
KOJO_DIR = os.path.join(
    GAME, r"ERB\口上・メッセージ関連\個人口上\147 Sariel [サリエル]"
)
PLACE_ERH = os.path.join(GAME, r"ERB\MOVEMENTS\物件関連\PLACE_ERH.ERH")
STR_CSV = os.path.join(GAME, r"CSV\Str.csv")
TRAIN_CSV = os.path.join(GAME, r"CSV\Train.csv")

MAP_NAMES = {
    0: "神社", 1: "寺", 2: "人间之里", 3: "湖", 4: "竹林",
    5: "魔法之森", 6: "冥界", 7: "山麓", 8: "山顶", 9: "地底",
    10: "月", 11: "魔界",
}


# ============ 通用工具 ============
def read_text(path):
    for enc in ("utf-8-sig", "utf-8", "cp932", "shift_jis", "gbk"):
        try:
            with io.open(path, encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, LookupError):
            continue
    with io.open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def human_size(n):
    if n < 1024:
        return "%d B" % n
    if n < 1024 * 1024:
        return "%.1f KB" % (n / 1024.0)
    return "%.1f MB" % (n / 1024.0 / 1024.0)


DECOR_CHARS = set(" \t　;=＝—─-_*#▼◆■□●○※+・")

def clean_comment(line):
    """把 ;===== 标题 ===== 之类的装饰注释清理成纯文本"""
    s = line.strip()
    s = s.lstrip(";").strip()
    s = s.strip(" \t　=＝—─-_*#▼◆■□●○※+・")
    return s.strip()


def is_decor(line):
    s = line.strip()
    return bool(s) and all(c in DECOR_CHARS for c in s)


# ============ 01 模板索引 ============
SECTION_RE = re.compile(r"^;\s*(\d{2,4})\s*[,，、:：]\s*(.+)$")


def build_sections(lines):
    """预扫描所有 `;604,散步（...）` 形式的段落标题 → [(行号, 编号, 标题)]"""
    secs = []
    for i, ln in enumerate(lines):
        m = SECTION_RE.match(ln.strip())
        if m:
            secs.append((i, m.group(1), m.group(2).strip()))
    return secs


def find_section_title(secs, i, cmd):
    """按编号匹配最近的段落标题（编号不一致就不用，避免串台）"""
    if not cmd:
        return ""
    for ln, num, title in reversed(secs):
        if ln >= i:
            continue
        if num.lstrip("0") == cmd.lstrip("0"):
            return title
        # 往上最多找 200 行，超出就放弃
        if i - ln > 200:
            break
    return ""


def parse_template_file(path):
    """返回 (函数列表, 文件行数, 字节数)
    函数项 = (起始行, 函数名, 摘要, 行数, 是否在 SKIP 区)
    """
    text = read_text(path)
    lines = text.splitlines()
    secs = build_sections(lines)

    marks = []
    skip_depth = 0
    for i, ln in enumerate(lines):
        u = ln.strip().upper()
        if u.startswith("[SKIPSTART]"):
            skip_depth += 1
        elif u.startswith("[SKIPEND]"):
            skip_depth = max(0, skip_depth - 1)
        elif ln.startswith("@"):
            m = re.match(r"@([^\s(]+)", ln)
            if m:
                marks.append((i, m.group(1), skip_depth > 0))

    funcs = []
    for k, (i, name, in_skip) in enumerate(marks):
        end = marks[k + 1][0] if k + 1 < len(marks) else len(lines)
        buf = []
        j = i - 1
        while j >= 0 and len(buf) < 2:
            s = lines[j].strip()
            if not s:
                if buf:
                    break
                j -= 1
                continue
            if not s.startswith(";"):
                break
            if not is_decor(s):
                c = clean_comment(s)
                if c:
                    buf.append(c)
            j -= 1
        summary = " / ".join(reversed(buf))[:90]
        if not summary:
            summary = find_section_title(secs, i, extract_cmd(name))[:90]
        funcs.append((i + 1, name, summary, end - i, in_skip))
    return funcs, len(lines), os.path.getsize(path)


def extract_cmd(name):
    """从函数名尾部提取指令编号：..._KX_604 / ..._K147_604 → 604"""
    m = re.search(r"_K(?:\d+|X)_(\d{2,4})$", name)
    return m.group(1) if m else ""


def build_template_index():
    out = []
    out.append("# eraTW 口上模板函数索引")
    out.append("")
    out.append("> 由 `BUILD.py` 自动生成，请勿手改。")
    out.append("> 用途：AI 想知道「某条指令的模板长什么样」时查这里，再让用户贴对应片段。")
    out.append("> 模板目录：`%s`" % TEMPLATE_DIR)
    out.append("")

    if not os.path.isdir(TEMPLATE_DIR):
        out.append("**⚠ 模板目录不存在，请检查 BUILD.py 里的 TEMPLATE_DIR。**")
        return "\n".join(out)

    files = sorted(
        f for f in os.listdir(TEMPLATE_DIR) if f.upper().endswith(".ERB")
    )

    total_funcs = 0
    cmd_map = {}      # 指令编号 -> [(文件, 函数名, 行号)]
    file_blocks = []

    for fn in files:
        path = os.path.join(TEMPLATE_DIR, fn)
        funcs, nlines, nbytes = parse_template_file(path)
        total_funcs += len(funcs)

        block = []
        block.append("### %s" % fn)
        block.append("*%s ／ %d 行 ／ %d 个函数*" % (human_size(nbytes), nlines, len(funcs)))
        block.append("")
        block.append("| 行号 | 函数名 | 用途 |")
        block.append("|---|---|---|")
        for ln, name, summary, _, in_skip in funcs:
            tag = "（SKIP 未编译）" if in_skip else ""
            s = summary.replace("|", "／") or "—"
            block.append("| %d | `%s` | %s%s |" % (ln, name, s, tag))
            cmd = extract_cmd(name)
            if cmd and not in_skip:
                short = name
                short = re.sub(r"^M_KOJO_XXX_", "", short)
                short = re.sub(r"_K(?:\d+|X)_\d{2,4}$", "", short)
                cmd_map.setdefault(cmd, {}).setdefault(fn, []).append((short, ln))
        block.append("")
        file_blocks.append("\n".join(block))

    out.append("## 总览")
    out.append("")
    out.append("| 文件 | 函数数 |")
    out.append("|---|---|")
    for fn in files:
        funcs, _, _ = parse_template_file(os.path.join(TEMPLATE_DIR, fn))
        out.append("| %s | %d |" % (fn, len(funcs)))
    out.append("")
    out.append("合计 **%d** 个模板函数。" % total_funcs)
    out.append("")

    out.append("## 指令编号 → 模板函数 反查")
    out.append("")
    out.append("写某条指令时先在这里查它属于哪个模板文件。")
    out.append("")
    out.append("| 指令 | 包含的函数（行号） | 所在文件 |")
    out.append("|---|---|---|")
    for cmd in sorted(cmd_map, key=lambda x: (len(x), x)):
        for fn, items in cmd_map[cmd].items():
            parts = ["%s : %d" % (s, ln) for s, ln in items]
            out.append("| %s | %s | %s |" % (cmd, " ／ ".join(parts), fn))
    out.append("")
    out.append("---")
    out.append("")

    out.extend(file_blocks)
    return "\n".join(out)


# ============ 02 地点表 ============
def build_place_table():
    out = []
    out.append("# eraTW 地点 ID 对照表")
    out.append("")
    out.append("> 由 `BUILD.py` 自动生成。")
    out.append("> `CFLAG:現在位置` 的值 = 地点 ID = `SELECTCASE` 的 `CASE` 值。")
    out.append("> `MAPID = 地点ID / 100`；取地名用 `NAME_FROM_PLACE(CFLAG:現在位置)`。")
    out.append("")

    if not os.path.isfile(PLACE_ERH):
        out.append("**⚠ 找不到 PLACE_ERH.ERH，请检查 BUILD.py 里的 GAME 路径。**")
        return "\n".join(out)

    erh = read_text(PLACE_ERH)

    places = {}
    for m in re.finditer(r"#DIM\s+CONST\s+P(\S+?)\s*=\s*(\d+)", erh):
        raw, val = m.group(1), int(m.group(2))
        mm = re.match(r"(\d+)(.*)", raw)
        if mm and int(mm.group(1)) == val and mm.group(2):
            places[val] = mm.group(2).strip()

    jp_names = {}
    if os.path.isfile(STR_CSV):
        for line in read_text(STR_CSV).splitlines():
            parts = line.split(",", 1)
            if len(parts) == 2 and parts[0].strip().isdigit():
                n = int(parts[0])
                if 8000 < n < 9000:
                    jp_names[n - 8000] = parts[1].strip()

    groups = {}
    for pid in sorted(places):
        groups.setdefault(pid // 100, []).append(pid)

    out.append("共 **%d** 个地点，分属 %d 个地图。" % (len(places), len(groups)))
    out.append("")

    out.append("## 地图分段速查")
    out.append("")
    out.append("| MAPID | 地图 | ID 段 | 数量 |")
    out.append("|---|---|---|---|")
    for mid in sorted(groups):
        ids = groups[mid]
        out.append("| %d | %s | %d~%d | %d |" % (
            mid, MAP_NAMES.get(mid, "未知"), ids[0], ids[-1], len(ids)))
    out.append("")
    out.append("---")
    out.append("")

    for mid in sorted(groups):
        out.append("## %d %s（%d~%d）" % (
            mid, MAP_NAMES.get(mid, "未知"), groups[mid][0], groups[mid][-1]))
        out.append("")
        out.append("```")
        for pid in groups[mid]:
            cn = places[pid]
            jp = jp_names.get(pid, "")
            if jp and jp != cn:
                out.append("%-5d %s   [%s]" % (pid, cn, jp))
            else:
                out.append("%-5d %s" % (pid, cn))
        out.append("```")
        out.append("")

    return "\n".join(out)


# ============ 03 147 现状 ============
def build_status():
    out = []
    out.append("# 萨丽艾尔（147）口上 —— 当前进度")
    out.append("")
    out.append("> 由 `BUILD.py` 自动生成，反映磁盘上的最新状态。")
    out.append("")

    if not os.path.isdir(KOJO_DIR):
        out.append("**⚠ 找不到 147 口上目录，请检查 BUILD.py 里的 KOJO_DIR。**")
        return "\n".join(out)

    out.append("目录：`%s`" % KOJO_DIR)
    out.append("")

    all_cmds = []
    for fn in sorted(f for f in os.listdir(KOJO_DIR) if f.upper().endswith(".ERB")):
        path = os.path.join(KOJO_DIR, fn)
        funcs, nlines, nbytes = parse_template_file(path)
        out.append("## %s" % fn)
        out.append("*%s ／ %d 行 ／ %d 个函数*" % (human_size(nbytes), nlines, len(funcs)))
        out.append("")
        out.append("| 行号 | 函数名 | 备注 |")
        out.append("|---|---|---|")
        for ln, name, summary, length, in_skip in funcs:
            note = "SKIP 未编译" if in_skip else (summary or "—")
            out.append("| %d | `%s` | %s |" % (ln, name, note))
            m = re.search(r"_MESSAGE_COM_K(?:\d+|X)_(\d+)$", name)
            if m and not in_skip:
                all_cmds.append(m.group(1))
        out.append("")

    out.append("## 已写口上的指令编号")
    out.append("")
    uniq = sorted(set(all_cmds), key=lambda x: int(x))
    out.append("```")
    out.append(" ".join(uniq))
    out.append("```")
    out.append("")
    out.append("共 **%d** 条。" % len(uniq))

    return "\n".join(out)


def build_all_in_one():
    """把 00 + 01 + 02 + 03 拼成一个文件，给上下文大的 AI 一次上传"""
    parts = []
    parts.append("<!-- 本文件由 BUILD.py 自动合并生成：00_核心包 + 01_模板索引 + 02_地点表 + 03_147现状 -->")
    parts.append("")
    for name in ("00_核心包.md", "03_147现状.md", "01_模板索引.md", "02_地点表.md"):
        path = os.path.join(BASE, name)
        if not os.path.isfile(path):
            continue
        parts.append("")
        parts.append("\n\n<!-- ========== 以下内容来自 %s ========== -->\n\n" % name)
        parts.append(read_text(path))
    return "\n".join(parts)


# ============ main ============
def main():
    print("=" * 60)
    print("eraTW 口上知识库生成器")
    print("=" * 60)
    print("游戏目录：%s" % GAME)
    print("模板目录：%s" % TEMPLATE_DIR)
    print("口上目录：%s" % KOJO_DIR)
    print()

    tasks = [
        ("01_模板索引.md", build_template_index),
        ("02_地点表.md", build_place_table),
        ("03_147现状.md", build_status),
    ]

    ok = 0
    for name, fn in tasks:
        try:
            content = fn()
            path = os.path.join(BASE, name)
            with io.open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(content)
            print("  [OK] %-18s %s" % (name, human_size(len(content.encode("utf-8")))))
            ok += 1
        except Exception as e:
            print("  [FAIL] %s -> %s" % (name, e))

    # 合并版
    try:
        content = build_all_in_one()
        path = os.path.join(BASE, "ALL_IN_ONE.md")
        with io.open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(content)
        print("  [OK] %-18s %s" % ("ALL_IN_ONE.md", human_size(len(content.encode("utf-8")))))
    except Exception as e:
        print("  [FAIL] ALL_IN_ONE.md -> %s" % e)

    print()
    print("完成 %d/%d。输出目录：%s" % (ok, len(tasks), BASE))
    print()
    print("用法：")
    print("  每个新 AI 会话先发 00_核心包.md")
    print("  要查模板时再发 01_模板索引.md，写散步时发 02_地点表.md")
    print("  换 AI 时附上 03_147现状.md")
    print("  上下文大的 AI 可以直接发 ALL_IN_ONE.md（一次到位）")


if __name__ == "__main__":
    main()
    if len(sys.argv) > 1 and sys.argv[1] == "--pause":
        input("\n按回车退出...")
