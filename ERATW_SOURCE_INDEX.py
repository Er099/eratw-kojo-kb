# -*- coding: utf-8 -*-
"""
从 eraTW 源码生成「查表类」知识库文件。

输出：
    06_variable_names.md   变量名全表（编号 | 汉化名 | 日文原名 | 备注）
    07_character_index.md  角色编号表（编号 | 名前 | 呼び名 | 是否有口上）
    08_command_index.md    指令编号表（编号 | 汉化名 | 日文原名）

用法：
    python ERATW_SOURCE_INDEX.py
游戏更新后重跑一次即可。
"""
import os
import io
import re
import glob

GAME = r"D:/F/口上制作尝试/AI代写代码测试/eraTW"
CSV_DIR = os.path.join(GAME, "CSV")
CHAR_DIR = os.path.join(CSV_DIR, "Chara")
KOJO_DIR = os.path.join(GAME, "ERB", "口上・メッセージ関連", "個人口上")
OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# (显示名, 基名, 是否角色变量)
TABLES = [
    ("TALENT", "Talent", True),
    ("ABL", "Abl", True),
    ("EXP", "exp", True),
    ("BASE", "Base", True),
    ("CFLAG", "CFLAG", True),
    ("TCVAR", "TCVAR", True),
    ("TFLAG", "TFLAG", True),
    ("CSTR", "CSTR", True),
    ("MARK", "Mark", True),
    ("STAIN", "Stain", True),
    ("PALAM", "Palam", True),
    ("JUEL", "Juel", True),
    ("BUFF", "BUFF", True),
    ("EQUIP", "Equip", True),
    ("TEQUIP", "Tequip", True),
    ("ITEM", "Item", True),
    ("FLAG", "FLAG", False),
    ("M_CFLAG", "M_CFLAG", True),
    ("M_TFLAG", "M_TFLAG", True),
    ("M_TALENT", "M_TALENT", True),
    ("TRAIN", "Train", False),
]


def read_text(path):
    for enc in ("utf-8-sig", "utf-8", "cp932", "gbk"):
        try:
            with io.open(path, "r", encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, LookupError):
            continue
    with io.open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def parse_table(path):
    """返回 {编号: (名称, 备注)}，跳过注释行与无编号行。"""
    out = {}
    if not os.path.exists(path):
        return out
    for ln in read_text(path).splitlines():
        s = ln.strip()
        if not s or s.startswith(";"):
            continue
        parts = s.split(",", 2)
        if len(parts) < 2:
            continue
        num = parts[0].strip()
        if not re.fullmatch(r"-?\d+", num):
            continue
        name = parts[1].strip()
        note = ""
        if len(parts) > 2:
            note = parts[2].strip().lstrip(";").strip()
        out[int(num)] = (name, note)
    return out


def build_variables():
    lines = []
    lines.append("# eraTW 变量名全表（源码实测）\n")
    lines.append("> 自动生成，请勿手改。生成脚本：`ERATW_SOURCE_INDEX.py`\n")
    lines.append("> 数据源：`%s`\n" % CSV_DIR.replace("\\", "/"))
    lines.append("\n## 先读这段（最容易出错的地方）\n")
    lines.append("eraTW 每个变量都有**两套名称表**，Emuera 同时加载：\n")
    lines.append("- `XXX.csv` = **汉化名**")
    lines.append("- `XXX.als` = **日文原名 + 遗留别名**")
    lines.append("- **有效名称 = csv ∪ als**，两张表里的名字都能用\n")
    lines.append("只有两边都没有的名字才会报「无法识别」。典型例子：`ABL:肛門` ——")
    lines.append("原版叫 `アナル`、汉化叫 `肛门`，`肛門` 是第三种写法，两边都没有，所以报错且**静默失效**。\n")
    lines.append("**最保险的写法**：直接用编号，如 `ABL:147:55`、`TALENT:147:3`，永远不受汉化影响。\n")
    lines.append("> 下表「备注」列来自 csv 的 `;` 注释，通常是取值范围或位含义，写判定前务必看一眼。\n")

    stat = []
    for disp, base, _ in TABLES:
        csv_p = os.path.join(CSV_DIR, base + ".csv")
        als_p = os.path.join(CSV_DIR, base + ".als")
        t_csv = parse_table(csv_p)
        t_als = parse_table(als_p)
        keys = sorted(set(t_csv) | set(t_als))
        if not keys:
            continue
        lines.append("\n---\n\n## %s（%d 项）\n" % (disp, len(keys)))
        has_als = bool(t_als)
        if has_als:
            lines.append("| 编号 | 汉化名 (csv) | 日文原名 (als) | 备注 |")
            lines.append("|---|---|---|---|")
            for k in keys:
                cn = t_csv.get(k, ("", ""))[0]
                jp = t_als.get(k, ("", ""))[0]
                note = t_csv.get(k, ("", ""))[1] or t_als.get(k, ("", ""))[1]
                lines.append("| %d | %s | %s | %s |" % (k, cn, jp, note.replace("|", "\\|")))
        else:
            lines.append("| 编号 | 名称 | 备注 |")
            lines.append("|---|---|---|")
            for k in keys:
                cn, note = t_csv.get(k, ("", ""))
                lines.append("| %d | %s | %s |" % (k, cn, note.replace("|", "\\|")))
        stat.append((disp, len(keys)))

    lines.append("\n---\n\n## 汇总\n")
    lines.append("| 表 | 条目数 |")
    lines.append("|---|---|")
    for d, n in stat:
        lines.append("| %s | %d |" % (d, n))
    lines.append("\n合计 %d 项。\n" % sum(n for _, n in stat))

    out = os.path.join(OUT_DIR, "06_variable_names.md")
    with io.open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))
    return sum(n for _, n in stat)


def build_characters():
    # 已有口上的角色编号
    has_kojo = set()
    if os.path.isdir(KOJO_DIR):
        for d in os.listdir(KOJO_DIR):
            m = re.match(r"^(\d{3})\s", d)
            if m:
                has_kojo.add(int(m.group(1)))

    rows = []
    for p in glob.glob(os.path.join(CHAR_DIR, "Chara*.csv")):
        txt = read_text(p)
        no = name = kana = None
        for ln in txt.splitlines():
            s = ln.strip().lstrip("\ufeff")
            if s.startswith("番号,"):
                v = s.split(",")[1].strip()
                if v.isdigit():
                    no = int(v)
            elif s.startswith("名前,"):
                name = s.split(",")[1].strip()
            elif s.startswith("呼び名,"):
                kana = s.split(",")[1].strip()
        if no is None:
            continue
        rows.append((no, name or "", kana or "", os.path.basename(p)))

    rows.sort()
    lines = []
    lines.append("# eraTW 角色编号表（源码实测）\n")
    lines.append("> 自动生成，请勿手改。生成脚本：`ERATW_SOURCE_INDEX.py`\n")
    lines.append("> 数据源：`%s`\n" % CHAR_DIR.replace("\\", "/"))
    lines.append("\n## 用法\n")
    lines.append("- `TALENT:<编号>:<素质>`、`CFLAG:<编号>:<标记>` 里的编号就是下表第一列。")
    lines.append("- `NO:<角色>` 返回的是**运行时编号**（会随加入队伍变化），而这里的编号是**角色定义编号**，两者不同。")
    lines.append("- 写口上时函数名里的数字用**角色定义编号**，例如 `@M_KOJO_147_MESSAGE_COM_K147_604`。")
    lines.append("- 「口上」列 ✔ 表示 `個人口上/` 下已有该角色的口上目录，可以参照其写法。\n")
    lines.append("| 编号 | 名前（中文） | 呼び名 | 有口上 | 文件 |")
    lines.append("|---:|---|---|:---:|---|")
    for no, name, kana, fn in rows:
        lines.append("| %d | %s | %s | %s | `%s` |" % (
            no, name, kana, "✔" if no in has_kojo else "", fn))
    lines.append("\n共 %d 个角色，其中 %d 个已有口上。\n" % (len(rows), len(has_kojo)))

    out = os.path.join(OUT_DIR, "07_character_index.md")
    with io.open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))
    return len(rows)


def build_commands():
    t_csv = parse_table(os.path.join(CSV_DIR, "Train.csv"))
    t_als = parse_table(os.path.join(CSV_DIR, "Train.als"))
    keys = sorted(set(t_csv) | set(t_als))

    lines = []
    lines.append("# eraTW 指令编号表（源码实测）\n")
    lines.append("> 自动生成，请勿手改。生成脚本：`ERATW_SOURCE_INDEX.py`\n")
    lines.append("> 数据源：`CSV/Train.csv` + `CSV/Train.als`\n")
    lines.append("\n## 用法\n")
    lines.append("- 口上钩子：`@M_KOJO_<NO>_MESSAGE_COM_K<NO>_<指令号>`（普通指令）")
    lines.append("- 性交系：`@M_KOJO_<NO>_MESSAGE_SCOM_K<NO>_<指令号>`")
    lines.append("- 编号**不连续**是正常的：源码里有被注释掉的旧编号（如 `;10,吸乳头`），实际生效的是 `11`。\n")
    lines.append("| 编号 | 汉化名 (csv) | 日文原名 (als) |")
    lines.append("|---:|---|---|")
    for k in keys:
        cn = t_csv.get(k, ("", ""))[0]
        jp = t_als.get(k, ("", ""))[0]
        lines.append("| %d | %s | %s |" % (k, cn, jp))
    lines.append("\n共 %d 条指令。\n" % len(keys))

    out = os.path.join(OUT_DIR, "08_command_index.md")
    with io.open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))
    return len(keys)


if __name__ == "__main__":
    n1 = build_variables()
    n2 = build_characters()
    n3 = build_commands()
    print("  [OK] 06_variable_names.md   %d 项" % n1)
    print("  [OK] 07_character_index.md  %d 个角色" % n2)
    print("  [OK] 08_command_index.md    %d 条指令" % n3)
