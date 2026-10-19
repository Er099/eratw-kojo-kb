# -*- coding: utf-8 -*-
"""
知识库自检脚本 VERIFY.py
========================
扫描知识库 md 里的 ```erb 代码块，逐项校验其中的符号是否真实存在：

  1. [VAR]  变量名   CFLAG:xxx / TFLAG:xxx / TCVAR:xxx ... 是否在 CSV 名称表中
  2. [CMD]  行首命令 PRINTFORMD / SETCOLOR ... 是否在 eraTW 源码或 Emuera 文档中出现
  3. [FUNC] 函数名   @xxx / CALL xxx / TRYCALLFORM xxx 是否在 eraTW 源码中定义

用法:
    python VERIFY.py                 # 扫默认文件（00_core.md、09_kojo_framework.md）
    python VERIFY.py 00_core.md      # 只扫指定文件
    python VERIFY.py --rebuild       # 强制重建源码符号缓存

输出: VERIFY_REPORT.txt（同时打印摘要到控制台）

注意: 报告里的 [CMD]/[FUNC] 命中不一定是错误——
      md 里可能有「错误写法」示范，或函数在其它 mod 中定义。需人工判断。
"""
import os
import re
import sys
import json
import glob

BASE = os.path.dirname(os.path.abspath(__file__))
ERA = r"D:\F\口上制作尝试\AI代写代码测试\eraTW"
CSVD = os.path.join(ERA, "CSV")
ERBD = os.path.join(ERA, "ERB")
CACHE = os.path.join(BASE, ".cache")
SYM_CACHE = os.path.join(CACHE, "erb_symbols.json")
REPORT = os.path.join(BASE, "VERIFY_REPORT.txt")

DEFAULT_TARGETS = ["00_core.md", "09_kojo_framework.md"]

# 变量表名 -> CSV 文件名主干（csv / als 两种后缀都会读）
VAR_TABLES = {
    "CFLAG": "CFLAG", "FLAG": "FLAG", "TFLAG": "TFLAG", "TCVAR": "TCVAR",
    "TALENT": "Talent", "ABL": "Abl", "EXP": "exp", "BASE": "Base",
    "CSTR": "CSTR", "MARK": "Mark", "JUEL": "Juel", "PALAM": "Palam",
    "STAIN": "Stain", "ITEM": "Item", "EQUIP": "Equip", "BUFF": "BUFF",
    "M_CFLAG": "M_CFLAG", "M_FLAG": "M_FLAG", "M_TALENT": "M_TALENT",
    "M_TFLAG": "M_TFLAG", "DAY": "DAY",
}

# 变量表后面出现的「角色引用」写法，不是变量名
CHAR_REFS = {"ARG", "ARGS", "MASTER", "TARGET", "ASSI", "PLAYER", "ENEMY",
             "TRAINEE", "MY", "CALLNAME"}

# 行首这些 token 是语法关键字，不查命令表
KEYWORDS = {
    "IF", "ELSEIF", "ELSE", "ENDIF", "FOR", "NEXT", "WHILE", "WEND", "DO", "LOOP",
    "REPEAT", "REREPEAT", "BREAK", "CONTINUE", "RETURN", "GOTO", "GOSUB",
    "SELECTCASE", "CASE", "CASEELSE", "ENDSELECT", "TRY", "CATCH", "ENDTRY",
    "TRYCALLLIST", "SIF", "AND", "OR", "NOT", "TRUE", "FALSE", "TOLOWER",
    "DATA", "DATAFORM", "DATALIST", "ENDLIST", "SKIPSTART", "SKIPEND",
    "FUNCTION", "FUNCTIONS", "END", "PRINT", "PRINTV", "PRINTVL", "PRINTS",
    "PRINTFORM", "PRINTFORMW", "PRINTFORML", "PRINTFORMS", "PRINTFORMC",
    "PRINTFORMD", "PRINTFORMK", "PRINTFORMDW", "PRINTFORMDL",
    # 角色表达式（可出现在行首，不是命令）
    "BASENAME", "ISASSI", "CALLNAME", "NAME", "NO", "MASTER", "TARGET",
    "ASSI", "PLAYER", "ENEMY", "TRAINEE", "ARG", "ARGS",
}

# 教学示例里的假函数名，不是真实符号
DEMO_FUNCS = {"MY_FUNC", "TEST", "HOGE", "FUNC", "SAMPLE", "FUNC_NAME",
              "M_KOJO", "M_KOJO_K", "函数", "格式串", "函数名", "标签"}

# #DIM 声明局部变量用的正则（用于把 L_HP 之类识别成变量而非命令）
DIM_RE = re.compile(
    r"^\s*#DIM(?:S)?\s+(?:(?:REF|CONST|SAVEDATA|GLOBAL|DYNAMIC|CHARADATA|"
    r"PRIVATE|REFFROM|REFTO)\s+)*([A-Za-z_][A-Za-z0-9_]*)", re.I)


# ---------------------------------------------------------------- 变量表

def load_table(stem):
    """读 XXX.csv + XXX.als，返回 (names:set, maxid:int)"""
    names = set()
    maxid = -1
    for ext in (".csv", ".als"):
        p = os.path.join(CSVD, stem + ext)
        if not os.path.exists(p):
            continue
        with open(p, "r", encoding="utf-8-sig", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith(";"):
                    continue
                parts = line.split(",", 1)
                if len(parts) != 2:
                    continue
                num = parts[0].strip()
                # 名称后面可能跟 ,;注释 或 ,注释，取第一段
                name = parts[1].split(",")[0].strip()
                if not num.isdigit():
                    continue
                maxid = max(maxid, int(num))
                if name and not name.startswith(";"):
                    names.add(name)
    return names, maxid


def load_all_tables():
    out = {}
    for tab, stem in VAR_TABLES.items():
        out[tab] = load_table(stem)
    return out


# ---------------------------------------------------------------- 源码符号索引

def build_symbol_cache(force=False):
    """扫描 ERB 源码，提取所有行首命令 + @函数名，缓存到 .cache"""
    files = glob.glob(os.path.join(ERBD, "**", "*.ERB"), recursive=True)
    files += glob.glob(os.path.join(ERBD, "**", "*.ERH"), recursive=True)
    sig = "%d:%d" % (len(files), sum(os.path.getsize(f) for f in files))

    if not force and os.path.exists(SYM_CACHE):
        try:
            with open(SYM_CACHE, "r", encoding="utf-8") as f:
                data = json.load(f)
            if data.get("sig") == sig:
                print("[cache] 源码符号缓存有效 (%d 命令 / %d 函数)"
                      % (len(data["commands"]), len(data["functions"])))
                return set(data["commands"]), set(data["functions"])
        except Exception:
            pass

    print("[scan] 正在扫描 %d 个 ERB 文件（首次约 30 秒）..." % len(files))
    cmd_re = re.compile(r"^\s*([A-Z][A-Z0-9_]{1,})")
    func_re = re.compile(r"^\s*@([A-Za-z0-9_\u3040-\u30ff\u4e00-\u9fff]+)")
    commands, functions = set(), set()

    for i, path in enumerate(files):
        if i % 800 == 0:
            print("       ... %d/%d" % (i, len(files)))
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    m = cmd_re.match(line)
                    if m:
                        commands.add(m.group(1))
                    m = func_re.match(line)
                    if m:
                        functions.add(m.group(1))
        except Exception:
            continue

    os.makedirs(CACHE, exist_ok=True)
    with open(SYM_CACHE, "w", encoding="utf-8") as f:
        json.dump({"sig": sig, "commands": sorted(commands),
                   "functions": sorted(functions)}, f, ensure_ascii=False)
    print("[scan] 完成: %d 命令 / %d 函数" % (len(commands), len(functions)))
    return commands, functions


def load_doc_commands():
    """从 04_emuera_syntax_index.md 提取文档中出现过的命令名"""
    p = os.path.join(BASE, "04_emuera_syntax_index.md")
    cmds = set()
    if not os.path.exists(p):
        return cmds
    with open(p, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            # 索引行形如: PRINTFORM | ... ，取首列的大写词
            for tok in re.findall(r"\b([A-Z][A-Z0-9_]{1,})\b", line[:80]):
                cmds.add(tok)
    return cmds


# ---------------------------------------------------------------- md 解析

def extract_erb_blocks(path):
    """返回 [(起始行号, [代码行...])]"""
    blocks = []
    cur = None
    start = 0
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for no, line in enumerate(f, 1):
            s = line.rstrip("\n")
            if cur is None and re.match(r"^\s*```erb\s*$", s, re.I):
                cur = []
                start = no + 1
            elif cur is not None and re.match(r"^\s*```\s*$", s):
                blocks.append((start, cur))
                cur = None
            elif cur is not None:
                cur.append(s)
    if cur:
        blocks.append((start, cur))
    return blocks


# ---------------------------------------------------------------- 校验

VAR_RE = re.compile(
    r"\b(" + "|".join(sorted(VAR_TABLES, key=len, reverse=True)) + r")\s*:\s*"
    r"([A-Za-z0-9_\u3040-\u30ff\u4e00-\u9fff]+)"
)
CMD_RE = re.compile(r"^\s*([A-Z][A-Z0-9_]{1,})\b")
FUNC_DEF_RE = re.compile(r"^\s*@([A-Za-z0-9_\u3040-\u30ff\u4e00-\u9fff]+)")
FUNC_CALL_RE = re.compile(
    r"\b(?:TRYCALLFORM|CALLFORM|TRYCALL|CALL|JUMPFORM|TRYJUMPFORM|JUMP|TRYJUMP)\s+"
    r"([A-Za-z0-9_\u3040-\u30ff\u4e00-\u9fff]+)"
)


def verify_file(path, tables, src_cmds, doc_cmds, src_funcs):
    issues = []
    known_cmds = src_cmds | doc_cmds
    for start, lines in extract_erb_blocks(path):
        # 块内 #DIM 声明的局部变量，出现在行首时不算命令
        local_vars = set()
        for line in lines:
            m = DIM_RE.match(line)
            if m:
                local_vars.add(m.group(1).upper())
        for off, line in enumerate(lines):
            no = start + off
            code = line.split(";", 1)[0]          # 去掉行尾注释
            if not code.strip():
                continue

            # 1) 变量名
            for m in VAR_RE.finditer(code):
                tab, name = m.group(1), m.group(2)
                if name.isdigit():
                    names, maxid = tables[tab]
                    if maxid >= 0 and int(name) > maxid:
                        issues.append((no, "VAR", "%s:%s 编号超出表范围（最大 %d）"
                                       % (tab, name, maxid), line.strip()))
                    continue
                if name.upper() in CHAR_REFS or name in CHAR_REFS:
                    continue
                names, _ = tables[tab]
                if name not in names:
                    issues.append((no, "VAR", "%s:%s 不在 %s.csv/.als 名称表中"
                                   % (tab, name, VAR_TABLES[tab]), line.strip()))

            # 2) 行首命令
            m = CMD_RE.match(code)
            if m:
                cmd = m.group(1)
                if (cmd not in KEYWORDS and cmd not in VAR_TABLES
                        and cmd not in known_cmds and cmd not in local_vars):
                    issues.append((no, "CMD", "行首命令 %s 未在 eraTW 源码/Emuera 文档中出现"
                                   % cmd, line.strip()))

            # 3) 函数
            m = FUNC_DEF_RE.match(code)
            if m:
                fn = m.group(1)
                if fn not in DEMO_FUNCS and not fn.startswith(("M_KOJO_147", "M_KOJO_K147")):
                    if fn not in src_funcs:
                        issues.append((no, "FUNC", "@%s 未在 eraTW 源码中定义" % fn,
                                       line.strip()))
            for m in FUNC_CALL_RE.finditer(code):
                fn = m.group(1)
                if fn not in DEMO_FUNCS and fn not in src_funcs:
                    issues.append((no, "FUNC", "调用的 %s 未在 eraTW 源码中定义" % fn,
                                   line.strip()))
    return issues


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    force = "--rebuild" in sys.argv
    targets = args or DEFAULT_TARGETS

    print("=" * 60)
    print("知识库符号自检  VERIFY.py")
    print("=" * 60)

    tables = load_all_tables()
    src_cmds, src_funcs = build_symbol_cache(force)
    doc_cmds = load_doc_commands()
    print("[load] 变量表 %d 张 / 文档命令 %d 个" % (len(tables), len(doc_cmds)))

    all_lines = []
    total = 0
    for t in targets:
        p = os.path.join(BASE, t) if not os.path.isabs(t) else t
        if not os.path.exists(p):
            print("[skip] 找不到 %s" % t)
            continue
        blocks = extract_erb_blocks(p)
        issues = verify_file(p, tables, src_cmds, doc_cmds, src_funcs)
        total += len(issues)
        all_lines.append("\n### %s  (代码块 %d 个, 问题 %d 条)" % (t, len(blocks), len(issues)))
        print("\n[%s] 代码块 %d 个 → 问题 %d 条" % (t, len(blocks), len(issues)))
        for no, kind, msg, src in issues:
            all_lines.append("  L%-5d [%s] %s" % (no, kind, msg))
            all_lines.append("          > %s" % src)
            print("  L%-5d [%s] %s" % (no, kind, msg))

    header = ["=" * 60,
              "知识库符号自检报告  %s" % __import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M"),
              "扫描文件: %s" % ", ".join(targets),
              "问题合计: %d 条" % total,
              "=" * 60]
    with open(REPORT, "w", encoding="utf-8") as f:
        f.write("\n".join(header + all_lines) + "\n")

    print("\n" + "-" * 60)
    print("合计 %d 条问题 → 详见 %s" % (total, REPORT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
