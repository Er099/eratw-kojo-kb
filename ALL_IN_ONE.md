<!-- 本文件由 BUILD.py 自动合并生成：00_core + 01_template_index + 02_places + 03_status -->




<!-- ========== 以下内容来自 00_core.md ========== -->


# eraTW 萨丽艾尔（147）口上制作 · AI 上下文包

> **给接手 AI 的话**：读完本文件你就能直接开始工作，不需要再要游戏源码。
> 需要查具体模板函数时，再向用户要 `01_template_index.md`；需要查地点编号时，要 `02_places.md`。
>
> 适用版本：eraTW 画蛇添足 4.981 汉化版（`AI代写代码测试\eraTW\`）
> 包版本：v1 ／ 生成日期：2026-10-18

---

## 0. 一句话任务

用户（中文母语）自己写萨丽艾尔（角色编号 **147**）的口上文本，**AI 负责把这些文本原样套进 eraTW 的 ERB 代码结构**。

AI **不写剧情、不改文本、不改用户的差分设计**。发现明显错字只指出，不代改。

> **开工前请先复述这三条**（防止跳读）：
> ① 识别符是 `_147`，所有函数名都要带；
> ② `MESSAGE_COM` 结尾写 `RETURN 1`，不是 `0`；
> ③ 旁白用 `PRINTFORMD*`，对白用 `PRINTFORM*`。
>
> 复述完再开始干活。

### 你要输出什么

| 场景 | 输出 |
|---|---|
| 某条指令**第一次**做 | 完整、可直接粘贴的 ERB 函数块 |
| 在某条已有指令上**补一段** | 只给需要替换/插入的片段 + 一句话说明放哪 |
| 用户问「这么写对不对」 | 先说结论（对/不对），再指出具体哪行、为什么、怎么改 |

---

## 1. 硬规则（违反会直接被用户打回）

### 1.1 文本层

1. **一字不改**。中文对白、旁白、剧情全部照抄。错字只提醒。
2. **半角方括号 → 日式引号**：`[你好]` → `「你好」`。全角方括号 `【】` 视原文保留。
3. **不要大量空行**，保持紧凑。缩进用 **Tab**（不是空格）。
4. **PRINTFORM 按阅读体验分配**，不要每句都用 `PRINTFORMW`（会造成「点击地狱」）。一段连续旁白只在段末用 `W`，中间用 `L`。

### 1.2 结构层

1. **不自己造模板**。函数名、变量位、`SELECTCASE`、`FIRSTTIME`、各种 `MESSAGE`/`SUCCESS` 函数，一律以游戏模板或用户已有代码为准。
2. **配对必须完整**：
   - `IF` / `ELSEIF` / `ELSE` → `ENDIF`
   - `SELECTCASE` → `ENDSELECT`（用户特别强调过漏 `ENDSELECT` 的问题）
   - `PRINTDATA` → `ENDDATA`；`DATALIST` → `ENDLIST`
   - `FOR` → `NEXT`；`WHILE` → `WEND`
   - `[SKIPSTART]` → `[SKIPEND]`
3. **函数名必须带识别符 `_147`**（见 §3.1，这是历史事故点）。

### 1.3 颜色层

| 用途 | 命令 |
|---|---|
| 旁白 / 地の文（默认色） | `PRINTFORMDL` / `PRINTFORMDW` |
| 角色对白 / 心声（口上色） | `PRINTFORML` / `PRINTFORMW` |
| 需要临时指定颜色 | `SETCOLOR` … `RESETCOLOR`，配 `PRINTFORM*`（**不能带 D**） |

⚠️ **`D` 后缀 = 忽略 SETCOLOR，强制默认色**。所以 `SETCOLOR C_RED` + `PRINTFORMDW` 是无效组合。

---

## 2. 关系差分（固定五段，顺序与首尾段都不能改）

这是本项目**所有**指令口上的骨架。用户说「亲密<=5」= 第五段，说「只有恋人以上」= 只写第一段。

```erb
;恋人/爱恋
IF TALENT:恋人 || TALENT:恋慕 > 1
	;这里以后填写恋人/爱恋
;恋慕
ELSEIF TALENT:恋慕 == 1
	;这里以后填写恋慕
;思慕
ELSEIF TALENT:思慕
	;这里以后填写思慕
;ABL:9 > 5
ELSEIF ABL:9 > 5
	;这里以后填写ABL:9 > 5
;ABL:9 <= 5
ELSE
	（用户文本放这里）
ENDIF
```

数据含义：

| 表达式 | 含义 |
|---|---|
| `TALENT:恋慕 == 1` | 恋慕 |
| `TALENT:恋慕 > 1` | 爱恋（`Talent.csv` 注释「=2で上位互換」） |
| `TALENT:恋人` | 恋人 |
| `TALENT:思慕` | 思慕 |
| `ABL:9` | 親密（亲密度） |

写的时候可以简写成 `TALENT:147:恋人` 这种带编号的形式，也可以省略编号（默认 `TARGET`）。

---

## 3. eraTW 口上框架机制

> **完整派发机制、29 类钩子 + MESSAGECHECK 变体、颜色常量、4.980 拦截器 → `09_kojo_framework.md`**
> 本章只讲写口上必须记住的部分。

### 3.1 函数命名规则（最重要，历史事故点）

框架靠「`M_KOJO` + 识别符 + 后缀 + `K` + 角色编号」找函数。**识别符**来自口上自己的存在判定函数里设的 `RESULTS`。

本项目 `@M_KOJO_K147(ARG)` 里写了 `RESULTS = _147`，所以识别符是 `_147`，**所有函数名都要带它**：

| 用途 | 函数名 |
|---|---|
| 存在判定（必须 `RETURN 1`） | `@M_KOJO_K147(ARG)` |
| 每回合前基本标志设置 | `@M_KOJO_147_FLAGSETTING_K147` |
| 口上色 | `@M_KOJO_147_COLOR_K147` |
| 剧本专属更新页面 | `@M_KOJO_147_UPDATE_K147` |
| 初次见面 | `@M_KOJO_147_ENCOUNTER_K147` |
| 指令文本 | `@M_KOJO_147_MESSAGE_COM_K147_<编号>` |
| 文本显示开关 | `@M_KOJO_147_MESSAGE_MESSAGECHECK_COM_K147_<编号>` |
| 成否判定 | `@M_KOJO_147_SUCCESS_COM_K147_<编号>` |
| 剧本选项菜单 | `@KOJO_147_OPTION_EXIST_K147` / `@KOJO_147_OPTION_K147` / `@KOJO_147_OPTION_K147_RESULT_1` |
| （可选）文本屏蔽拦截器 | `@M_KOJO_147_MESSAGE_MESSAGECHECK_PRI_GENERAL_K147(ARG, ARGS)` |

> ⚠️ **事故记录**：曾有 AI 建议删掉 `RESULTS = _147`（理由是「初始口上按新规范不写识别符」），结果框架去找 `@M_KOJO_FLAGSETTING_K147`（不存在）→ 游戏弹窗「※警告：(萨丽艾尔_初版剧本)的基本标志未设定」。
> **识别符必须保留。**

### 3.2 返回值语义（三个函数三种意思，绝对不要混）

| 函数类型 | 返回值含义 |
|---|---|
| `..._MESSAGE_COM_...`（文本函数） | `1` = 我输出了文本；`0` = 没输出 → 框架会调 `@AUTO_AEGI`（自动娇喘）兜底。**所有真实口上末尾写 `RETURN 1`** |
| `..._MESSAGE_MESSAGECHECK_COM_...`（显示开关） | **位掩码**，不是布尔：`0`=情景文本+口上都显示；`1`=屏蔽情景文本（地文）；`2`=屏蔽口上；`3`=都屏蔽 |
| `@M_KOJO_K147`（存在判定） | 必须 `1`。返回 `0` 会在剧本选择界面弹红字「剧本错误！请点击重置」 |
| `..._SUCCESS_COM_...` | 只负责设 `TFLAG:192`，**不用写 RETURN**（模板如此） |
| 拦截器 `PRI_GENERAL` | `-1` = 放行（默认）；`0~3` 同 MESSAGECHECK |

MESSAGECHECK 的框架实现（`KOJO_MESSAGE.ERB:236~247`）：

```erb
TRYCCALLFORM M_KOJO%KOJO_NAME%_MESSAGE_MESSAGECHECK_PRI_GENERAL_K{NO:TARGET}(LOCAL, LOCALS)
IF RESULT == 拦截器未激活
	RESULT = 0
	TRYCALLFORM M_KOJO%KOJO_NAME%_MESSAGE_MESSAGECHECK_%LOCALS%_K{NO:TARGET}_{LOCAL}
ENDIF
SKIP_MESSAGE = GETBIT(RESULT, 0)
SKIP_KOJO    = GETBIT(RESULT, 1)
```

> 游戏自带的「文本设定」只有三档（剧本台词+情景文本／仅情景文本／不显示文本），**没有「只显示剧本台词」**。所以「只要口上不要地文」必须靠 MESSAGECHECK 或拦截器。

### 3.3 骨架（新指令的标准写法）

```erb
;========== 文本显示开关（0 = 系统文本 + 口上都显示）==========
@M_KOJO_147_MESSAGE_MESSAGECHECK_COM_K147_604
#LOCALSIZE 1
#LOCALSSIZE 1
RETURN 0

;========== 指令正文 ==========
@M_KOJO_147_MESSAGE_COM_K147_604
#LOCALSIZE 1
#LOCALSSIZE 1
;恋人/爱恋
IF TALENT:恋人 || TALENT:恋慕 > 1
	PRINTFORMW
;恋慕
ELSEIF TALENT:恋慕 == 1
	PRINTFORMW
;思慕
ELSEIF TALENT:思慕
	PRINTFORMW
;ABL:9 > 5
ELSEIF ABL:9 > 5
	PRINTFORMW
;ABL:9 <= 5
ELSE
	PRINTFORMW
ENDIF
RETURN 1
```

需要成否判定的指令（如 414 吃饭、415 招待、416 演奏）再加一个：

```erb
@M_KOJO_147_SUCCESS_COM_K147_414
#LOCALSIZE 1
#LOCALSSIZE 1
TFLAG:192 = 0          ; 0 = 系统决定；-2 强制中止 / -1 强制失败 / 1 强制成功
```

### 3.4 已用的变量位（147 专用）

| 变量 | 编号 | 用途 |
|---|---|---|
| `TFLAG:192` | 192 | 成否判定 |
| `TFLAG:193` | 193 | 成否结果（`1` 大成功 / `0` 成功 / `-1` 失败 / `-2` 中止；421 另有 30/35/200） |
| `TFLAG:194` | 194 | 413 料理分类（`>=100` 禁断 / `3` 甜点 / `2` 主食 / `1` 轻食） |
| `TFLAG:141` | 141 | 416 使用乐器（1 电子琴 / 2 钢琴 / 3 吉他 / 4 小号 / 5 小提琴） |
| `TCVAR:306` | 306 | 414/415 料理评价值（千分位） |
| `FLAG:560` | 560 | 421 祈愿内容 |
| `CSTR:147:処女喪失履歴` | 46 | 处女丧失履历（**不要用 CSTR:1**，那是每日重置的 ONCE） |

> 易混：`FLAG:561` 是「精力强化回数」（`FLAG.csv:98`），147 目前**没用到**；「精力超群」是 `TALENT:152`（als 叫 `絶倫`），两者不是一回事。

**新写口上想加自己的状态位**：

- ⚠️ `TCVAR:350~399` 名义上是「口上用確保領域」（`TCVAR.csv:185` 原文），但**实测这 50 个编号全部已被各口上占用**：350(643 次)、351(699)、352(334)、360(686)、354(214)、399(194)……连最少的 397 也有 5 次。**实际已无空位，别再往里塞。**
- `TCVAR:300~349` 是系统区（饮茶时刻、会话累计值、料理评价值……），同样不能用。
- 结论：**TCVAR 没有给 147 留位置**。需要「每日重置」的临时状态，用 `CFLAG` 自己存值 + 另存一个 `DAY` 比较，跨天时清零。
- `CFLAG:1000~1999` 是「剧本专用保留值域」，但 `@RESET_CHARA` 会清空它（`VARSET CFLAG:ARG:0,0,1000,2000`）
- `CFLAG:6000~6999` 是「中文版自定义保留值域」，**不会被重置** → 要存持久数据用这里
- 建议：`CFLAG:1470~1479`（1000 段内、角色号开头、全库无人使用）；需要跨重置保留则用 `CFLAG:6010~6019`

### 3.5 颜色

```erb
; 口上整体色（改这一行即可换色）
@M_KOJO_147_COLOR_K147
#LOCALSIZE 1
#LOCALSSIZE 1
SETCOLOR 0xD0C0F0      ; 当前是淡紫；改成 0xFF0000 就是红
RETURN 0
```

常用常量（定义在 `ERB\DIM.ERH` 680~760 行）：

| 常量 | 值 | 观感 |
|---|---|---|
| `C_RED` | `0xFF0000` | 纯红 |
| `C_D_RED` | `0x990000` | 暗红 |
| `C_P_RED` | `0xC07070` | 淡红 |
| `C_FLAME` | `0xFF4242` | 火焰红 |
| `C_TORII` | `0xE60033` | 鸟居红 |

只给一行上色（不会污染后续文字）：

```erb
CALL COLORMESSAGE("体力-200", C_RED, 2)     ; 2 = 换行 + WAIT
```

或 `PRINTFORMW %PRINT_COLOR("体力-200", C_RED)%`（eraTW 自带函数）。

---

## 4. Emuera 语法速查（口上最常用）

> 完整文档：`D:/F/口上制作尝试/emuera/emuera.sk.doc-feature-tutorial-restructure/docs/Reference/`（313 篇，`.zh.md` 是中文）
> 索引：`D:/F/口上制作尝试/emuera/AI_EMUERA_INDEX.txt`

### 4.1 变量体系

| 前缀 | 作用域 | 说明 |
|---|---|---|
| `CFLAG:` | 每角色 | 整数，会存盘 |
| `TFLAG:` | 每角色 | 临时整数，**每天重置** |
| `TCVAR:` | 每角色 | 临时整数，**每天重置** |
| `TALENT:` | 每角色 | 素质（可读可写，部分由系统维护） |
| `ABL:` | 每角色 | 能力值（0~5 级） |
| `EXP:` | 每角色 | 经验计数 |
| `BASE:` | 每角色 | 基础值（体力、精力等，带 `MAXBASE:`） |
| `CSTR:` | 每角色 | 字符串（存台词、名字等） |
| `FLAG:` | 全局 | 全局整数 |
| `STR:` | 全局 | 全局字符串 |
| `LOCAL:` / `LOCALS:` | 函数内 | 局部整数 / 字符串，需 `#LOCALSIZE` `#LOCALSSIZE` 声明 |
| `ARG:` / `ARGS:` | 参数 | 函数入参 |
| `RESULT:` / `RESULTS:` | 返回值 | 函数返回值；`RESULT` 是整数，`RESULTS` 是字符串 |
| `RAND:n` | — | 0 ~ n-1 的随机整数 |

**三种写法**（等价）：

```erb
TALENT:恋慕              ; 省略角色 → 默认 TARGET
TALENT:TARGET:恋慕       ; 显式指定
TALENT:147:恋慕          ; 用角色编号（推荐，最稳）
```

**变量名规则（重要）**：`CSV\` 下每个变量都有**两套名称表**，Emuera **同时加载**：

| 文件 | 内容 | 例子 |
|---|---|---|
| `XXX.csv` | 汉化名 | `Abl.csv: 55,肛门` |
| `XXX.als` | **日文原名 + 遗留别名** | `Abl.als: 55,アナル` |

→ **有效名称 = csv ∪ als**。日文原名（`処女`、`音楽技能`、`Ｃ感覚`、`奉仕精神`、`絶頂経験`、`現在位置`）**全部仍然有效**。

**只有两边都没有的名字才报「无法识别」**。典型：`ABL:肛門`（原版叫 `アナル`，汉化叫 `肛门`，`肛門` 是第三种写法）。

> 写名称前的保险做法：去 `CSV\XXX.csv` 或 `CSV\XXX.als` 里复制；或者干脆用数字索引（`ABL:147:55`、`TALENT:147:0`），永远不受汉化影响。

### 4.2 PRINT 系列与后缀

```erb
PRINTFORM  文本      ; 展开 %变量%，不换行
PRINTFORML 文本      ; + 换行
PRINTFORMW 文本      ; + 换行 + WAIT（等玩家点击）
PRINTFORMD 文本      ; D = 忽略 SETCOLOR，用默认色
PRINTFORMDL 文本     ; 默认色 + 换行
PRINTFORMDW 文本     ; 默认色 + 换行 + WAIT
PRINTFORMS 文本      ; 用系统字体（少用）
```

第二括号关键字：

| 关键字 | 含义 |
|---|---|
| 无 | 忽略 `FORCEKANA`，用 `SETCOLOR` 指定的颜色 |
| `K` | 应用 `FORCEKANA`（**不是口上色！**） |
| `D` | 忽略 `SETCOLOR`，用配置的默认色 |

> `K` 与 `D` 不能同时用。eraTW 全库一次 `FORCEKANA` 都没调用过，所以 `PRINTFORMK` 实际上等于普通 `PRINTFORM`——063/151 两个口上用它当「口上色」是误解，**别当范本**。

第三括号：`L` = 换行、`W` = 换行+WAIT、`N` = 只 WAIT 不换行（`N` 不能与 K/D 组合）。

其他输出命令：

```erb
PRINTL 文本          ; 不展开 %
PRINTW 文本          ; 不展开 + 换行 + WAIT
PRINTVL 变量         ; 打印数值
PRINTSL 字符串变量   ; 打印字符串变量
CLEARLINE n          ; 清掉当前行往上 n 行
```

### 4.3 PRINTDATA / DATAFORM / DATALIST / STRDATA

**作用**：一组候选文本里等概率随机选一条，省掉 `SELECTCASE RAND:n`。

```erb
PRINTDATA
	DATA 纯文本项（不展开 %）
	DATAFORM 格式化文本，可写 %变量% / \n / \@条件?A#B\@
	DATALIST
		DATAFORM 多行块第一行
		DATAFORM 多行块第二行
	ENDLIST
ENDDATA
```

| 要点 | 说明 |
|---|---|
| 选择单位 | 每个顶层 `DATA` / `DATAFORM` / `DATALIST` 各算**一个**选项，等概率 |
| 输出单位 | `DATALIST` 内部每个 `DATA`/`DATAFORM` 各占一行，选中该块时**全部输出** |
| 参数 | `PRINTDATA LOCAL` 会把**被选中项的编号**（从 0 开始）存进 `LOCAL` |
| 块内限制 | 只允许 `DATA` / `DATAFORM` / `DATALIST` / `ENDLIST`，**不能写别的命令** |
| 后缀 | 同 PRINT 系：`PRINTDATA(|K|D)(|L|W)` —— `PRINTDATAD`（默认色）、`PRINTDATADL`（默认色+换行）、`PRINTDATADW`（默认色+换行+WAIT）、`PRINTDATAW`（口上色+换行+WAIT） |
| **无参数** | `PRINTDATA` 系列**不接受字符串参数**！`PRINTDATADW 文本` 会编译报错，必须紧跟 `DATA`/`DATAFORM` |
| 颜色 | 想让整块用默认色（= `PRINTFORMD` 效果）直接写 `PRINTDATAD*`；外层 `RESETCOLOR` 也行但有副作用 |
| 块内不能变色 | 块内只允许 DATA 系命令，写不了 `SETCOLOR`。要「部分行变色」必须拆成多个块用 `IF` 分流 |
| 赋值版 | `STRDATA 变量名` … `ENDDATA`：不显示，把选中的字符串塞进变量 |

示例：

```erb
PRINTDATADL
	DATAFORM %CALLNAME:TARGET%歪着头看向这边…
	DATAFORM %CALLNAME:TARGET%轻轻地叹了口气…
	DATAFORM %CALLNAME:TARGET%露出了一丝微笑…
ENDDATA
```

### 4.4 TEXTR（eraTW 自带随机词组函数）

```erb
%TEXTR("甲/乙/丙")%
```

- 按 `/` 切分后**等概率**随机取一个。最多 7 个**参数字符串**（`ARGS`~`ARGS:6`），但**单个字符串内按 `/` 切出的段数没有上限**（源码是先拼成一个串再 `SPLIT`，实测有 18 段的用法）
- **结尾的 `/` 不会产生空选项**：函数内部会删掉首尾斜杠和连续斜杠
  - 想表达「有时什么都不加」必须用**全角下划线 `＿`**：`%TEXTR("甲/乙/＿")%`
- `%TEXTR("/")%` = 空串，没意义（首尾斜杠都被删光，SPLIT 后只剩一个空串）
- 调权重靠**重复**：`%TEXTR("我/我/咱")%` = 我 2/3
- **只看全角 `＿`**：半角 `_`、`/` 都不行，写了会照原样显示出来
- **参数里要嵌 `%变量%` 时必须用 `@"..."`**：

```erb
%TEXTR(@"跑来跑去/捉弄一下%CALLNAME:MASTER%")%     ; ✔
%TEXTR("跑来跑去/捉弄一下%CALLNAME:MASTER%")%      ; ✘ 内层 % 会被截断
```

- 在 `DATAFORM` 里可以直接用（DATAFORM 是 formedString，同一套展开规则）

### 4.5 控制流

```erb
; IF
IF 条件
ELSEIF 条件
ELSE
ENDIF

; SELECTCASE
SELECTCASE 变量
	CASE 1
	CASE 2, 3
	CASE 1 TO 10          ; 范围
	CASE IS >= 100        ; 比较
	CASEELSE
ENDSELECT

; 循环
FOR LOCAL, 0, 10          ; LOCAL = 0..9
NEXT
WHILE 条件
WEND
REPEAT 10                 ; 重复 10 次（配 REND）
REND

; 跳转
GOTO 标签
$标签
BREAK
CONTINUE
RETURN 0                  ; 函数返回
```

### 4.6 常用运算符与函数

```erb
; 逻辑
&& || !                   ; 与 / 或 / 非（注意：不是 AND/OR）
== != > < >= <=

; 数学
LIMIT(值, 下限, 上限)     ; 钳制（最常用）
MAX(a, b)  MIN(a, b)
ABS(x)
RAND:n                    ; 0 ~ n-1
RANDOMIZE

; 位操作（MESSAGECHECK 用）
GETBIT(值, 位)
SETBIT(值, 位)

; 类型转换
TOSTR(数值)               ; 数字 → 字符串
TOINT(字符串)             ; 字符串 → 数字

; 字符串
STRLEN(字符串)
SUBSTRING(字符串, 起, 长)
STRFIND(字符串, 子串)
REPLACE(字符串, 正则, 替换)
SPLIT 字符串, 分隔符, 数组, 数量
STRFORM(格式串)           ; 展开 %变量%
TOUPPER / TOLOWER

; 角色
CALLNAME:角色             ; 显示名（会被改名影响）
NAME:角色                 ; 原名
BASENAME:角色             ; 基础名
ISASSI(角色)              ; 是否是助手
```

### 4.7 常用系统指令

```erb
FIRSTTIME("标签")         ; 每个存档只执行一次（配合 IF 用）
CALL 函数(参数)
CALLEVENT 函数
TRYCALL 函数              ; 函数不存在也不报错（直接跳过）
TRYCALLFORM 格式串        ; 同上，函数名可带 %变量%
TRYCCALLFORM 格式串       ; 函数不存在时进入 CATCH 块（更高级）
CALLFORM 格式串
SIF 条件                  ; 单行 IF（只作用于下一行）
```

> `TRY` 系和 `TRYC` 系的区别：`TRYCALL` 找不到函数就**跳过**；`TRYCCALL` 找不到就**跳到 `CATCH` 块**。eraTW 框架用 `TRYCCALLFORM` 派发口上函数，用 `TRYCALLFORM` 调用可能不存在的可选函数。
>
> ⚠️ **Emuera 没有 `CD`（冷却时间）命令**。eraTW 里「该指令有 CD」是各指令用自己的 `CFLAG` 记时间戳实现的，别照抄不存在的语法。

### 4.8 注释与跳过

```erb
; 单行注释
; 中文注释完全没问题

[SKIPSTART]
; 这里的代码不参与编译
[SKIPEND]
```

> ⚠️ `[SKIPSTART]` ~ `[SKIPEND]` 之间的函数**不会被编译**，改里面等于没改。

### 4.9 自定义函数与参数

```erb
; 定义：参数名写在函数名后面，逗号分隔
@MY_FUNC(ARG:0, ARG:1, ARGS:0)
	; ARG:0 / ARG:1 = 数值参数；ARGS:0 = 字符串参数
	RETURN
```

- 参数是**值传递**，改 `ARG` 不影响调用方
- 调用：`CALL MY_FUNC, 1, 2, "文本"`，或 `CALL MY_FUNC(1, 2, "文本")`
- **类型不自动转换**：数值传进字符串参数会直接报错
- 字符串字面量 `"..."`；格式化字符串 `@"..."`
- 可变长参数：函数声明加 `VARIADIC`，用 `ARGLEN` 取个数、`ARG:0..6` 取值 —— eraTW 的 `TEXTR` 就是这么写的

**省略参数**（官方 `function.zh.md`）：

- 省略时数值补 `0`、字符串补 `""` —— 对 `ARG` / `ARGS` / `#DIM(S)` 私有变量做参数**都成立**（这才是最常用的情形）
- **例外**：用 `A`、`STR` 这类普通变量做参数时，**既不能设初始值，也不能省略参数**
- 部分省略可以：`CALL FOOBAR, , "文本"`（只省第 1 个）
- 相关配置项「允许省略用户定义函数的所有参数」默认 `NO`，正常情况不用动它

**参数初始值**（`ASK_YN` 这类函数就是靠它）：

```erb
@MY_FUNC(ARG:0 = 111, ARGS:0 = "默认", ARG:1, ARG:2 = 200)
```

- 调用侧省略该参数时，自动赋初始值
- 初始值**只能是常量 / 常字符串**，不能写变量：`@FOOBAR, ARG:0 = MASTER` 无效
- 只有 `ARG` / `ARGS` / `#DIM(S)` 私有变量能设初始值；给 `A`、`STR` 这类变量设会被**静默忽略**（不报错，但不起作用）

**引用传递**（ver1.810+，能直接改调用方的变量）：

```erb
@TEST(HOGE)
#DIM REF HOGE
HOGE = 100        ; 调用方传进来的变量被改成 100
```

函数标志：

| 标志 | 含义 |
|---|---|
| 无 | 普通命令函数，用 `CALL`/`JUMP`，`RETURN` 结束 |
| `#FUNCTION` | 表达式函数，返回**数值**，必须 `RETURNF 值` |
| `#FUNCTIONS` | 表达式函数，返回**字符串**，必须 `RETURNF "..."` |
| `#FUNCTIONF` | 表达式函数，返回浮点 |

> `#FUNCTION(S)` 里**不能**用 `WAIT`/`INPUT`/`CALL`（会报错）。要调用别的函数用 `CALLF`。也不能用普通 `RETURN` 结束。

私有变量（写在函数头下面）：

```erb
@MY_FUNC(ARG:0)
#FUNCTION
#DIM 计数              ; 数值，1 个
#DIM 数组, 10          ; 数值，10 个
#DIMS 名字, 5          ; 字符串，5 个
#DIM DYNAMIC 临时, 3   ; 每次调用重新分配（递归安全，略慢）
#DIM CONST 表 = 1,2,3  ; 常量数组，不可改
#LOCALSIZE 20          ; LOCAL 个数
#LOCALSSIZE 10         ; LOCALS 个数
```

> `#DIM` 默认是**静态**的（函数返回后值还留着）。想每次干净，加 `DYNAMIC`。

### 4.10 ERH 与全局定义

- `.ERH` 里写的 `#DIM` 是**全局变量**，所有 ERB 都能引用
- `#DEFINE 名字 值` 是**文本宏**，编译前字符串替换，**不是变量**
- eraTW 的 `ERB\DIM.ERH` 定义了颜色常量（`C_xxx`）、`FLAG` 编号等

```erb
#DIM CONST C_RED = 0xFF0000
```

> ⚠️ 宏是纯文本替换：`#DEFINE A B+C` 在 `A*2` 里会变成 `B+C*2`。写宏一定要带括号。

### 4.11 运算符完整表（优先级从高到低）

| 优先级 | 运算符 | 说明 |
|---|---|---|
| 高 | `~` `!` | 按位取反、逻辑非 |
| ↓ | `*` `\` `%` | 乘、**整除（反斜杠，不是 `/`）**、取余 |
| | `+` `-` | 加减（字符串也能 `+` 拼接） |
| | `<<` `>>` | 位移 |
| | `<` `>` `<=` `>=` | 比较（字符串逐字符比较） |
| | `==` `!=` | 相等（**不能拿数值和字符串比**） |
| | `&` `\|` `^` | 按位与 / 或 / 异或 |
| 低 | `&&` `!&` `\|\|` `!\|` `^^` | 逻辑与 / 与非 / 或 / 或非 / 异或（`!&` `!\|` `^^` 不短路） |
| 最低 | `? #` | 三元 |

- 逻辑运算写 `&&` `||` `!`，**不是** `AND` `OR` `NOT`
- 整除是 `\`；写 `/` 会被当成字符串
- 三元两种写法：
  - 数值：`X = 条件 ? 真值 # 假值`；要放进表达式得加括号 `(条件 ? A # B)`
  - 字符串：`\@条件 ? 真 # 假\@`，可直接写在 `PRINTFORM*` 里
  - `#` 可省略（假值为空串，会有警告）
- 复合赋值：`+= -= *= \= %=`；字符串用 `'=`
- `++` `--` 只能单独成句，不能混进表达式

### 4.12 字符串处理

| 函数 | 作用 |
|---|---|
| `STRLEN(s)` | 长度（按字符算，中文算 1） |
| `SUBSTRING(s, 起, 长)` | 截取 |
| `STRFIND(s, 子串, 起点)` | 查找位置，找不到返回 -1 |
| `STRCOUNT(s, 子串)` | 出现次数 |
| `REPLACE(s, 正则, 替换)` | 正则替换（`TEXTR` 用它压斜杠） |
| `STRFORM(s)` | 展开含 `%变量%` 的字符串 |
| `TOSTR(n)` / `TOINT(s)` | 数值 ↔ 字符串 |
| `TOUPPER(s)` / `TOLOWER(s)` | 大小写 |
| `CHARATU(s, i)` / `UNICODE(s, i)` | 第 i 个字符 / 其码点 |
| `ENCODETOUNI(s)` | 字符串 → Unicode 码点数组 |
| `GETNUM(s, n)` | 取第 n 段（按 `,` 分） |
| `SPLIT 源, 分隔符, 数组, 数量` | **命令**，切分到数组，数量存进第 4 参数 |

### 4.13 数组与批量赋值

```erb
A:10 = 1,2,3              ; 批量赋值，从下标 10 开始
VARSET 变量, 值, 起, 终    ; 批量填充
VARSET CFLAG:ARG:0, 0, 1000, 2000   ; @RESET_CHARA 的写法
SWAP A, B                 ; 交换
VARSET 数组, 0            ; 清空（没有 ERASE 命令）
ARRAYCOPY 目标, 源, 个数
ARRAYSORT 数组, 升序标志
ARRAYREMOVE 数组, 起, 个数
```

> `VARSET` 第 3/4 参数是「起（含）」和「终（**不含**）」。`VARSET CFLAG:X,0,1000,2000` 清的是 1000~1999。

### 4.14 输入与等待

```erb
WAIT                 ; 等一次点击
WAITANYKEY           ; 等任意键
FORCEWAIT            ; 强制等（跳过开关也生效）
TWAIT 3000, 0        ; 最多等 3 秒（第 2 参数：0=接受输入提前结束，非 0=强制等满）
INPUT                ; 读数字 → RESULT
INPUTS               ; 读字符串 → RESULTS
$INPUT               ; 读数字，允许表达式 → RESULT
ONEINPUT / ONEINPUTS ; 只接受一次输入
TINPUT 3000, 0       ; 限时读数字，超时返回 0
TINPUTS 3000, ""     ; 限时读字符串
PRINTBUTTON "[0] 是", 0   ; 生成可点击按钮
INPUTMOUSEKEY        ; 鼠标/按键 → RESULT:0 类型、RESULT:1 值
```

- Emuera 会自动把 `[数字] 文本` 变成按钮；但一行里多个 `[]` 会识别错，这时用 `PRINTBUTTON`
- `ASK_YN "文本"` → `RESULT`：**0 = 是，1 = 否**
- `ASK_M` 参数是**成对**的（文本, 有效性）：1=可选、0=灰显、-1=隐藏；返回选项序号

> ⚠️ `ASK_YN`、`ASK_M`、`COLORMESSAGE` 是 **eraTW 自定义函数，不在 Emuera 官方文档里**（`04`/`05` 搜不到是正常的）。源码里分别用了 1106 / 673 / 3032 次，可以放心用。
> 反之，**`CD`、`ERASE`、`STRTRIM`、`CHARAT`、`PRINTANY` 这些命令不存在**，是早期文档里混进来的幻觉，已删除。

### 4.15 调试与编译错误

```erb
DEBUGPRINT 值 / DEBUGPRINTL / DEBUGPRINTW   ; 只在调试模式输出
ASSERT 条件                                 ; 条件为假时中断（调试模式）
THROW 值                                    ; 抛异常
TRY ... CATCH ... ENDCATCH                  ; 捕获
```

行首特殊注释：

| 写法 | 作用 |
|---|---|
| `;` | 普通注释 |
| `;!;` | **强制当作有效代码**（eramaker 里会当注释） |
| `;#;` | **只在调试模式执行** |

常见编译错误：

| 报错 | 原因 |
|---|---|
| 无法识别的变量名 | csv / als 里都没有（如 `肛門`） |
| 参数数量不符 | 给无参命令传了参（如 `PRINTDATADW 文本`） |
| 表达式类型不匹配 | 数值传进字符串参数，或 `==` 比较数值和字符串 |
| 找不到函数 | 拼错，或用 `TRYCCALLFORM` 派发时目标没定义 |
| `ENDSELECH` / `ENDIFF` | 拼写错误 |

### 4.16 语法查不到时去哪找

| 需求 | 看哪里 |
|---|---|
| 口上高频语法 | 本章（4.1 ~ 4.15） |
| 某个命令的准确签名 | `04_emuera_syntax_index.md`（387 篇索引，搜命令名） |
| 权威原文 / 边界情况 | `05_emuera_syntax_full.md`（中文全文，搜 `===== FILE:`） |
| 本地原始文档 | `D:/F/口上制作尝试/emuera/emuera.sk.doc-feature-tutorial-restructure/docs/` |
| 实际用法范例 | eraTW 源码 `ERB/` 里搜同命令名 |

---

## 5. 变量名与编号速查（147 常用）

> **完整全量表在 `06_variable_names.md`**（2179 项，编号 / 汉化名 / 日文原名 / 备注，源码实测）。
> 角色编号见 `07_character_index.md`（168 个角色），指令编号见 `08_command_index.md`（229 条）。
> 本章只列 147 口上最常碰的那些，查不到就去 06 搜。
> 下面是口上最常读写的部分。

### 5.1 TALENT（素质）

| 编号 | 名称 | 取值 |
|---|---|---|
| 0 | 処女 | 1=处女 2=再生处女 -1=无自觉非处女 |
| 1 | 非童貞 | 0=童贞；bit0=膣性交经验 bit1=肛门性交经验 |
| 2 | 性別 | 1=女性器 2=男性器 3=扶她 |
| 3 | 恋慕 | 1=恋慕 2=爱恋 |
| 4 | 淫乱 | 1 / 2=上位互换 |
| 7 | 恋人 | 1（只能有一个） |
| 8 | 思慕 | 1 |
| 10 | 胆量 | -1=胆怯 1=坚强 |
| 23 | 性的兴趣 | -1=保守 1=好奇 |
| 25 | 一線越えない | 1（不越线） |
| 31 | 自己愛 | -1=压抑 1=解放 |
| 40 | 痛覚 | -1=不怕痛 1=怕痛 |
| 41 | 濡れやすさ | -1=不易湿 1=容易湿 |
| 47/48/49 | 釣りLv / 採集Lv / 調合Lv | 0~ |
| 51 | 器用な指 | 1 |
| 101/102/103/104/106 | Ｃ/Ｖ/Ａ/Ｂ/Ｍ感度 | -1=钝感 0=普通 1=敏感 |
| 105 | 胸围（バストサイズ） | -2=绝壁 -1=贫乳 0=并乳 1=巨乳 2=爆乳 |
| 108 | 臀围（ヒップサイズ） | -2=纤臀 -1=小臀 0=并臀 1=润臀 2=丰臀 |
| 130 | 回復速度 | -1=慢 1=快 |
| 193 | 神霊 | 6=天使 |
| 200 | 魔界人 | 1 |

### 5.2 ABL（能力，0~5）

| 编号 | 名称 |
|---|---|
| 0 / 1 / 2 / 3 / 4 | Ｃ感覚 / Ｖ感覚 / Ａ感覚 / Ｂ感覚 / Ｍ感覚 |
| **9** | **親密**（关系五段用的就是这个） |
| 10 | 従順 |
| 11 | 欲望 |
| 13 | 奉仕精神 |
| 42 | 戦闘能力 |
| 43 | 教養 |
| 44 | 料理技能 |
| 45 | 音楽技能 |
| 55 | 肛门 |

> ⚠️ 素质是「感**度**」（`TALENT:Ｖ感度`），能力是「感**覚**」（`ABL:Ｖ感覚`）——两个字不同，别写错。

### 5.3 EXP（经验）

`絶頂経験` / `放尿経験` / `Ｖ性交経験` / `Ａ性交経験` / `自慰経験` / `挿入経験` / `苦痛快楽経験` / `異常経験` / `Ｖ拡張経験` / `緊縛経験` —— 全部 0 起累加。

> ⚠️ 后三个容易漏写「経験」后缀：`苦痛快楽経験`、`Ｖ拡張経験`、`緊縛経験`。汉化名是 `苦痛快乐经验` / `V扩张经验` / `紧缚经验`。

### 5.4 BASE（基础值）

| 名称 | 说明 |
|---|---|
| `体力` | 配 `MAXBASE:体力` 一起写才生效 |
| `精力` | 同上 |
| `バスト`（22） | 实际胸围 cm（**不要和 TALENT:105 胸围等级搞混**） |
| `ヒップ`（24） | 实际臀围 cm |

### 5.5 CSTR（字符串）

| 编号 | 名称 |
|---|---|
| 1 | `ONCE`（**每天重置**，别拿它存东西） |
| 46 | `処女喪失履歴` |

---

## 6. 代码片段库（可直接改用）

### 6.1 标准指令骨架

见 §3.3。

### 6.2 604 散步（按地点分）

```erb
@M_KOJO_147_MESSAGE_COM_K147_604
#LOCALSIZE 1
#LOCALSSIZE 1
SELECTCASE CFLAG:現在位置        ; = 地点 ID，见 02_places.md
	CASE 213                      ; 铃奈庵
		PRINTFORMW 「%CALLNAME:MASTER%，这里的书真多呢」
	CASE 935                      ; 情人旅馆
		PRINTFORMW 「等、等等，为什么带我来这种地方……」
	CASE 1 TO 70                  ; 神社全境
		PRINTFORMW
	CASEELSE
ENDSELECT
RETURN 1
```

> `MAPID = 地点ID / 100`；取地名：`NAME_FROM_PLACE(CFLAG:現在位置)`。

### 6.3 扣体力并显示红字

```erb
PRINTFORMDW 虫子已经不见了
BASE:MASTER:体力 = LIMIT(BASE:MASTER:体力 - 200, 0, MAXBASE:MASTER:体力)
CALL COLORMESSAGE("体力-200", C_RED, 2)      ; 2 = 换行 + WAIT
```

想显示真实扣除量：

```erb
#DIM L_HP                        ; 必须写在函数开头
L_HP = BASE:MASTER:体力
BASE:MASTER:体力 = LIMIT(L_HP - 200, 0, MAXBASE:MASTER:体力)
CALL COLORMESSAGE("体力-" + TOSTR(L_HP - BASE:MASTER:体力), C_RED, 2)
```

> `RECOVER` 自己会打红字，格式固定为 `体力－200 （角色名）`，**改不了**。想自定义文字就别用它。

### 6.4 随机文本（推荐用 PRINTDATA，别用 SELECTCASE RAND）

```erb
PRINTDATADL
	DATAFORM %CALLNAME:TARGET%安静地站在一旁…
	DATAFORM %CALLNAME:TARGET%望着远处的天空…
	DATAFORM %CALLNAME:TARGET%轻轻理了理头发…
ENDDATA
```

### 6.5 三选一询问（手写 INPUT 循环）

```erb
PRINTFORML [0]接受
PRINTFORML [1]拒绝
PRINTFORML [2]再想想
$inputloop
INPUT
IF RESULT == 0
	; 接受
ELSEIF RESULT == 1
	; 拒绝
ELSEIF RESULT == 2
	; 再想想
ELSE
	CLEARLINE 1
	GOTO inputloop
ENDIF
```

> 二选一可以用现成的 `CALL ASK_YN`。**eraTW 的返回值是 `0=是 / 1=否`**（`COMMON.ERB:1474` 注释原文「戻り値 0=是、1=否」），默认选项文本是「是」「否」：

```erb
CALL ASK_YN
IF RESULT == 0
	; 是
ELSE
	; 否
ENDIF
```

也可以自定义选项文本：`CALL ASK_YN("好", "算了")`。

> ⚠️ era 圈里 `0=是` 和 `1=是` 两种实现都有，换别的游戏/别的版本务必先翻 `@ASK_YN` 的注释。
> 多选项用 `CALL ASK_M`——注意参数是**（文本, 有效性标志）成对**，不是（文本, 返回值）：

```erb
CALL ASK_M("接受", 1, "拒绝", 1, "再想想", 1)
SELECTCASE RESULT          ; RESULT = 被选中项的序号，从 0 开始
	CASE 0
		; 接受
	CASE 1
		; 拒绝
	CASE 2
		; 再想想
ENDSELECT
```

第二个参数的含义：`1`（或任意非 0）= 可选；`0` = 灰显禁用；`-1` = 完全隐藏。所以可以写条件选项：

```erb
CALL ASK_M("接受", 1, "更进一步", TALENT:恋慕, "（隐藏项）", -1)
```

最多 10 组。`ASK_M` 内部自带防错循环（非法输入会 `CLEARLINE` 重来），不用自己写 `$inputloop`。

### 6.6 初次见面

```erb
@M_KOJO_147_ENCOUNTER_K147
#LOCALSIZE 1
#LOCALSSIZE 1
PRINTFORMW 「……」
RETURN 1
```

---

## 7. 踩坑清单（每条都真实踩过）

| # | 坑 | 正确做法 |
|---|---|---|
| 1 | 删掉 `RESULTS = _147` | **必须保留**，否则弹「基本标志未设定」 |
| 2 | `MESSAGE_COM` 结尾写 `RETURN 0` | 真实口上写 **`RETURN 1`**；`0` 会触发自动娇喘兜底 |
| 3 | `MESSAGECHECK` 当成布尔 | 是**位掩码**：`GETBIT(RESULT,0)`=屏蔽系统文本，`GETBIT(RESULT,1)`=屏蔽口上 |
| 4 | `SETCOLOR` + `PRINTFORMD*` | `D` 会无视 SETCOLOR。要变色必须用 `PRINTFORM*`（不带 D） |
| 5 | `PRINTFORMK` 当口上色 | `K` 是 FORCEKANA，不是口上色。口上色改 `@M_KOJO_147_COLOR_K147` |
| 6 | `%TEXTR("A/B/")%` 以为能出空 | 尾部 `/` 会被删掉。要空选项写 `＿` |
| 7 | `%TEXTR("...%变量%...")%` | 必须写 `@"..."`，否则内层 `%` 被截断 |
| 8 | 写 `ABL:147:肛門` | 两套表里都没有。用 `肛门` 或 `55` |
| 9 | `SELECTCASE` 漏 `ENDSELECT` | 必配 |
| 10 | 全角括号 `）` `，` | 代码里一律**半角** `)` `,` |
| 11 | `[SKIPSTART]` 区里改代码 | 不参与编译，等于没改 |
| 12 | `RECOVER` 后再自己打印一次 | `RECOVER` 自带红字提示，会重复两行 |
| 13 | `CSTR:1` 存持久数据 | CSTR:1 是 `ONCE`，每天重置 |
| 14 | `CFLAG:1000~1999` 存重要数据 | `@RESET_CHARA` 会清空，持久数据用 `6000~6999` |
| 15 | 每句都 `PRINTFORMW` | 会造成点击地狱。中间用 `L`，段末用 `W` |
| 16 | 以为 602「约会接吻」能用 | 本版**未实装**（`Train.csv` 无 600/601/602）。接吻是 `19`（継続）/`20`/`312`，都走 `MESSAGE_COM`。**63 是後背位肛交，不是接吻** |
| 17 | 以为散步是 694 | 是 **604**（`Train.csv: 604,散步`） |
| 18 | `PRINTDATADW 文本` | `PRINTDATA` 系列**不收参数**，`PRINTDATADW` 后面必须直接跟 `DATA`/`DATAFORM`，否则编译报错。要整句文本请用 `PRINTFORMDW` |
| 19 | `%TEXTR("默默/静静的/_")%` 用半角 `_` | 只有**全角 `＿`** 会被转成空串，半角 `_` 会原样显示 |
| 20 | 以为 `DATA`/`DATAFORM` 会依次全显示 | 顶层各项是**等概率选一个**，想全显示要拆块或改用 `DATALIST` |
| 21 | `TALENT:胸围` 和 `BASE:胸围` 混用 | 前者是等级（-2~2），后者是 cm 数值 |

---

## 8. 和用户配合的方式

- 用户会发「指令编号 + 条件（关系/技能）+ 中文文本」，AI 输出可粘贴的 ERB。
- 新指令第一次给**完整代码**；之后只给「替换到 XXX 函数 XXX 位置」的片段。
- 用户不喜欢长篇解释：有问题就说哪里/为什么/怎么改；没问题就说「这段没问题，可以直接用」。
- 用户会用 `@文件路径` 指定要改的文件。
- 用户测试后会把游戏里的报错/现象发回来，据此再查框架代码。

### 交付前自查（务必执行）

1. `IF` 与 `ENDIF` 数量差 = 0
2. `SELECTCASE` 与 `ENDSELECT` 配对
3. `PRINTDATA` 与 `ENDDATA` 配对
4. `PRINT` 行数 = 用户文本行数（防漏抄/多抄）
5. 没有残留半角 `[` `]`（对白应已转成 `「」`）
6. `PRINTxxx` 命令后都有空格
7. 函数名带 `_147`
8. 代码里没有全角括号

---

## 9. 这个包怎么用（给用户的说明）

| 文件 | 大小 | 什么时候发 |
|---|---|---|
| `00_core.md` | ~38 KB | **每个新 AI 会话都发这个**，语法 + 框架 + 规则一次到位 |
| `01_template_index.md` | ~130 KB | AI 需要查「某个指令的模板长什么样」时发 |
| `02_places.md` | ~21 KB | 写 604 散步等按地点分的口上时发 |
| `03_status.md` | ~9 KB | 换 AI 时让它知道现在写到哪了 |
| `04_emuera_syntax_index.md` | ~68 KB | 语法拿不准、要查准确签名时发（387 篇官方文档索引） |
| `05_emuera_syntax_full.md` | ~1.7 MB | **一般不用发**。AI 能读本地/联网时用它查权威原文 |
| `06_variable_names.md` | ~115 KB | **变量名拿不准时必查**（2179 项，编号/汉化名/日文原名/备注） |
| `07_character_index.md` | ~11 KB | 角色编号表（168 个角色，含是否有口上） |
| `08_command_index.md` | ~9 KB | 指令编号表（229 条，写 `MESSAGE_COM_K147_xxx` 前查这个） |
| `09_kojo_framework.md` | ~11 KB | 口上派发机制、29 类钩子、MESSAGECHECK、颜色常量、4.980 拦截器 |

**只发 00 就能开工**，01~04、06~09 是按需补充。

- 素材更新后跑 `BUILD.py` 重新生成 01/02/03。
- Emuera 官方文档更新后跑 `EMUERA_KB_SYNC.py` 重新生成 04/05。
- 游戏本体更新后跑 `ERATW_SOURCE_INDEX.py` 重新生成 06/07/08。

---

*本包内容来自：`AI交接说明.txt`、eraTW 4.981 源码实测、Emuera 官方文档（qirchen421.github.io/emuera.sk.doc）全 387 篇、以及本项目历次踩坑记录。*




<!-- ========== 以下内容来自 03_status.md ========== -->


# 萨丽艾尔（147）口上 —— 当前进度

> 由 `BUILD.py` 自动生成，反映磁盘上的最新状态。

目录：`D:\F\口上制作尝试\AI代写代码测试\eraTW\ERB\口上・メッセージ関連\個人口上\147 Sariel [サリエル]`

## 事件.ERB
*6.9 KB ／ 237 行 ／ 8 个函数*

| 行号 | 函数名 | 备注 |
|---|---|---|
| 9 | `M_KOJO_K147` | 口上的存在判定 |
| 20 | `M_KOJO_147_FLAGSETTING_K147` | 如果需要在游戏之初，即使不进行UPDATE也立即修改角色的素质，请写在这里 / FIRSTTIME("素质修改") 的作用是确保每个存档仅修改一次 |
| 92 | `M_KOJO_147_COLOR_K147` | 口上专属颜色设置 |
| 101 | `M_KOJO_147_UPDATE_K147` | 剧本专属更新页面 |
| 109 | `KOJO_147_OPTION_EXIST_K147` | 剧本选项菜单（在能力信息页面的「剧本选项」里显示） |
| 113 | `KOJO_147_OPTION_K147` | — |
| 120 | `KOJO_147_OPTION_K147_RESULT_1` | — |
| 211 | `M_KOJO_147_ENCOUNTER_K147` | 【初次见面事件】 |

## 日常.ERB
*122.4 KB ／ 3588 行 ／ 65 个函数*

| 行号 | 函数名 | 备注 |
|---|---|---|
| 8 | `M_KOJO_147_MESSAGE_COM_K147_300` | MARK:反発刻印(3以上=会話不能) / TCVAR:泥酔(1=通常成功or大失敗) |
| 52 | `M_KOJO_147_MESSAGE_COM_K147_301` | 301,泡茶 / TFLAG:193(1=大成功 0=成功 -1=失敗) |
| 97 | `M_KOJO_147_MESSAGE_COM_K147_302` | 302,身体接觸 / TFLAG:193(1=大成功 0=成功 -1=失敗) |
| 126 | `M_KOJO_147_MESSAGE_COM_K147_303` | 303,道歉 / TFLAG:193(2=点心盒成功 1=大成功 0=成功 -1=失敗 -2=点心盒失敗) |
| 207 | `M_KOJO_147_MESSAGE_COM_K147_305` | 305,索求膝枕（MASTER向TARGET索求膝枕，枕在TARGET腿上） |
| 226 | `M_KOJO_147_MESSAGE_COM_K147_307` | 307,捏臉蛋（其实是有点疼的，会加一点苦痛和反感的SOURCE） |
| 249 | `M_KOJO_147_MESSAGE_COM_K147_309` | ABL:親密(5以上=露出害羞的表情， 反之红着脸甩开手 / 该指令有CD |
| 307 | `M_KOJO_147_SUCCESS_COM_K147_331` | TFLAG:193(1=大成功（度过了愉快的时光） 0=成功（喝下了茶水） -1=失败（怀疑着没有喝下茶水）) / MASTER拥有调和知识则降低发觉下药的概率，角色污臭耐性<0（ |
| 316 | `M_KOJO_147_MESSAGE_MESSAGECHECK_COM_K147_331` | 泡茶(下药) |
| 320 | `M_KOJO_147_MESSAGE_COM_K147_331` | 泡茶(下药) |
| 397 | `M_KOJO_147_SUCCESS_COM_K147_332` | 332,劝酒 / TFLAG:193(0=劝酒成功) |
| 407 | `M_KOJO_147_MESSAGE_MESSAGECHECK_COM_K147_332` | 劝酒 |
| 412 | `M_KOJO_147_MESSAGE_COM_K147_332` | 劝酒 |
| 470 | `M_KOJO_147_SUCCESS_COM_K147_333` | 333,听牢骚 / TFLAG:193(6=大成功(醉酒状态) 5=成功(醉酒状态) 4=失败(醉酒状态) 3=大成功 2=成功 1=失败) |
| 478 | `M_KOJO_147_MESSAGE_MESSAGECHECK_COM_K147_333` | ABL:親密 < 3、拥有反发刻印时无法实行指令 |
| 482 | `M_KOJO_147_MESSAGE_COM_K147_333` | 听牢骚 |
| 549 | `M_KOJO_147_SUCCESS_COM_K147_334` | CFLAG:妊娠自覚状態(1=改为吃饭) / TALENT:酒耐性(-2=改为吃饭) |
| 556 | `M_KOJO_147_MESSAGE_MESSAGECHECK_COM_K147_334` | 碰杯 |
| 560 | `M_KOJO_147_MESSAGE_COM_K147_334` | 碰杯 |
| 610 | `M_KOJO_147_SUCCESS_COM_K147_336` | ABL:親密(4以下=感觉不太好… 9以下=好像很害羞的样子…… 9以上=好像很幸福的样子…… / 该指令有CD |
| 620 | `M_KOJO_147_MESSAGE_MESSAGECHECK_COM_K147_336` | MASTER体型小于角色体型-1，则因体格差别太大而强制失败 / 亲热强度<2、在室外、在浴室、工作中、睡眠中均不可实行指令 |
| 624 | `M_KOJO_147_MESSAGE_COM_K147_336` | 膝枕（MASTER给TARGET膝枕） |
| 698 | `M_KOJO_147_MESSAGE_MESSAGECHECK_COM_K147_350` | 5=被逼迫要求做且无法拒绝 6=被拒绝了，但是并不是不高兴 7=被普通地拒绝 8=被强硬地拒绝 / 98=口上内特殊判定加持时失败 99=口上内特殊判定加持时成功 |
| 703 | `M_KOJO_147_MESSAGE_COM_K147_350` | 推倒（时姦時名为猥亵） |
| 887 | `M_KOJO_147_MESSAGE_COM_K147_351` | 如果态度较差的角色在非烂醉，非因依赖而允许同行的情况下，或者角色正在工作且非烂醉时，是不能带着同行的。 / 如果身处室外，正在下雨，MASTER手里有伞或者角色带着伞则会共用雨伞， |
| 937 | `M_KOJO_147_MESSAGE_MESSAGECHECK_COM_K147_368` | 如果某个技能等级为1以上，则会发生基于技能的自由行动 / 详细内容参考ERB\MOVEMENTS\自由行動\FREE_ACT_10.ERB |
| 942 | `M_KOJO_147_MESSAGE_COM_K147_368` | 陪同行動 |
| 1304 | `M_KOJO_147_自由行動判定_K147` | 自由行动判定用函数 / 如果在与上述模板对应的 CASE 编号中返回 -1，这个自由行动将不会被触发 |
| 1318 | `M_KOJO_147_MESSAGE_MESSAGECHECK_COM_K147_403` | 403,休憩 |
| 1323 | `M_KOJO_147_MESSAGE_COM_K147_403` | 休憩 |
| 1355 | `M_KOJO_147_MESSAGE_MESSAGECHECK_COM_K147_405` | 不可带3人外出约会，若角色和MASTER之中一人气力过低，或者角色处于工作日，或者角色态度较低时接受了角色的依赖，都无法外出 / 更详细请参考ERB\コマンド関連\COMF\日常系 |
| 1360 | `M_KOJO_147_MESSAGE_COM_K147_405` | 外出(同行時变成约会 |
| 1422 | `M_KOJO_147_MESSAGE_MESSAGECHECK_COM_K147_410` | 如果TALENT:MASTER:清掃中毒，扫除的态度会异常积极 / 以及……可以在UFUFU中途（仅顺推，被逆推是不行的）进行扫除（会被瞪的） |
| 1427 | `M_KOJO_147_MESSAGE_COM_K147_410` | 扫除 |
| 1526 | `M_KOJO_147_MESSAGE_MESSAGECHECK_COM_K147_411` | TFLAG:194(3=夏天的烈日 2=危险的天气 1=恶劣的天气 （如果在危险/恶劣天气下训练会扣除更多体力气力）0=屋内or通常天气 / 如果MASTER比角色更强，就会变成M |
| 1531 | `M_KOJO_147_MESSAGE_COM_K147_411` | 战斗训练 |
| 1835 | `M_KOJO_147_MESSAGE_MESSAGECHECK_COM_K147_412` | 若MASTER的教养大于角色，则是由MASTER教导TARGET， 反之亦然 / 不同天气会导致学习时间增减 |
| 1840 | `M_KOJO_147_MESSAGE_COM_K147_412` | 学习 |
| 1946 | `M_KOJO_147_MESSAGE_MESSAGECHECK_COM_K147_413` | TFLAG:194(100以上=禁断的菜单（跳蛋食物） 3=甜点 2=主食 1=轻食 / 如果要细致到某一盘料理，可以用DISHNAME == ""(引号内填上料理的名称),制作相 |
| 1951 | `M_KOJO_147_MESSAGE_COM_K147_413` | 料理 |
| 2340 | `M_KOJO_147_SUCCESS_COM_K147_414` | 在特殊节分吃相应的料理，会有特殊地文，详见ERB\口上・メッセージ関連\EVENT_MESSAGE_COM400.ERB / 可以根据料理的点数做差分TCVAR:306（料理評価値 |
| 2348 | `M_KOJO_147_MESSAGE_MESSAGECHECK_COM_K147_414` | TFLAG:192在这里控制对料理的评价值，=1则最低500分，最高700分；=-1则固定为400分；=-2中止指令，=0则系统自行计算 |
| 2353 | `M_KOJO_147_MESSAGE_COM_K147_414` | 吃饭（MASTER和TARGET一起吃饭） |
| 2449 | `M_KOJO_147_SUCCESS_COM_K147_415` | 415,招待吃饭（和414吃饭几乎一样，函数都是调用的414的，唯一的不同在于MASTER不会吃） / TFLAG:193(1=大成功 0=成功 -1=失败) |
| 2456 | `M_KOJO_147_MESSAGE_MESSAGECHECK_COM_K147_415` | 招待吃饭（和414吃饭几乎一样，函数都是调用的414的，唯一的不同在于MASTER不会吃） |
| 2461 | `M_KOJO_147_MESSAGE_COM_K147_415` | 招待吃饭（和414吃饭几乎一样，函数都是调用的414的，唯一的不同在于MASTER不会吃） |
| 2553 | `M_KOJO_147_SUCCESS_COM_K147_416` | 参与演奏也是有CD的 / COMF文件路径：ERB\コマンド関連\COMF\日常系\COMF416 演奏する.ERB |
| 2561 | `M_KOJO_147_MESSAGE_MESSAGECHECK_COM_K147_416` | 宴会时，ABL:MASTER:音楽技能 < 3 指令强制失败 |
| 2566 | `M_KOJO_147_MESSAGE_COM_K147_416` | 演奏 |
| 2658 | `M_KOJO_147_MESSAGE_MESSAGECHECK_COM_K147_421` | 子宝祈願：只有恋人/爱恋才有文本 / 其他祈愿：输出随机文本 |
| 2663 | `M_KOJO_147_MESSAGE_COM_K147_421` | 祈願 |
| 2698 | `M_KOJO_147_MESSAGE_MESSAGECHECK_COM_K147_440` | 模板里这块是按所在地点做差分的（SELECTCASE CFLAG:MASTER:300，十几个地点）， / 本口上不使用那个差分，只按关系差分 |
| 2703 | `M_KOJO_147_MESSAGE_COM_K147_440` | 等待 |
| 2740 | `M_KOJO_147_MESSAGE_MESSAGECHECK_COM_K147_445` | TFLAG:193=採集物ID（0=什么都没找到）、TFLAG:194=个数 / ABL:9>5 与 ABL:9<=5 共用同一段文本 |
| 2745 | `M_KOJO_147_MESSAGE_COM_K147_445` | 採集 |
| 3301 | `M_KOJO_147_MESSAGE_MESSAGECHECK_COM_K147_448` | 1 陷阱损坏、1 捕获到猎物、10 设置昆虫诱捕装置 / 11 破弃昆虫诱捕装置、12 昆虫诱捕装置捕获到虫子 |
| 3306 | `M_KOJO_147_MESSAGE_COM_K147_448` | 设置陷阱／查看陷阱 |
| 3423 | `M_KOJO_147_MESSAGE_MESSAGECHECK_COM_K147_449` | 虫子的名称 可通过 MUSHI_NAME 来表示和确定 / 冬天没有虫子 |
| 3428 | `M_KOJO_147_MESSAGE_COM_K147_449` | 捕虫 |
| 3545 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_600` | SKIP 未编译 |
| 3550 | `M_KOJO_XXX_MESSAGE_COM_KX_600` | SKIP 未编译 |
| 3561 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_601` | SKIP 未编译 |
| 3566 | `M_KOJO_XXX_MESSAGE_COM_KX_601` | SKIP 未编译 |
| 3577 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_602` | SKIP 未编译 |
| 3582 | `M_KOJO_XXX_MESSAGE_COM_KX_602` | SKIP 未编译 |

## 已写口上的指令编号

```
300 301 302 303 305 307 309 331 332 333 334 336 350 351 368 403 405 410 411 412 413 414 415 416 421 440 445 448 449
```

共 **29** 条。



<!-- ========== 以下内容来自 01_template_index.md ========== -->


# eraTW 口上模板函数索引

> 由 `BUILD.py` 自动生成，请勿手改。
> 用途：AI 想知道「某条指令的模板长什么样」时查这里，再让用户贴对应片段。
> 模板目录：`D:\F\口上制作尝试\TW口上汉化精修模版(4.954-4.97X)`

## 总览

| 文件 | 函数数 |
|---|---|
| M_KOJO_KX_X2_BANQUET.ERB | 5 |
| M_KOJO_KX_X2_COUNTER系.ERB | 152 |
| M_KOJO_KX_X2_CUSTOM_CHECKS.ERB | 9 |
| M_KOJO_KX_X2_CUSTOM_EVENTS.ERB | 1 |
| M_KOJO_KX_X2_EVENTCOM.ERB | 7 |
| M_KOJO_KX_X2_IMAGE.ERB | 11 |
| M_KOJO_KX_X2_MARRIAGE.ERB | 7 |
| M_KOJO_KX_X2_New_Api.ERB | 16 |
| M_KOJO_KX_X2_事件系.ERB | 72 |
| M_KOJO_KX_X2_侍奉系指令.ERB | 11 |
| M_KOJO_KX_X2_依頼.ERB | 21 |
| M_KOJO_KX_X2_其他系指令.ERB | 30 |
| M_KOJO_KX_X2_刻印取得.ERB | 2 |
| M_KOJO_KX_X2_弾幕勝負.ERB | 1 |
| M_KOJO_KX_X2_性交系指令.ERB | 20 |
| M_KOJO_KX_X2_性骚扰指令.ERB | 46 |
| M_KOJO_KX_X2_施虐系指令.ERB | 13 |
| M_KOJO_KX_X2_日常系指令.ERB | 183 |
| M_KOJO_KX_X2_日记.ERB | 6 |
| M_KOJO_KX_X2_日记（简易版）.ERB | 28 |
| M_KOJO_KX_X2_派生指令.ERB | 23 |
| M_KOJO_KX_X2_爱抚系指令.ERB | 25 |
| M_KOJO_KX_X2_特有COUNTER指令.ERB | 4 |
| M_KOJO_KX_X2_硬核系指令.ERB | 17 |
| M_KOJO_KX_X2_育儿事件.ERB | 22 |
| M_KOJO_KX_X2_自定义派生指令.ERB | 25 |
| M_KOJO_KX_X2_自定义系指令.ERB | 10 |
| M_KOJO_KX_X2_诶嘿嘿文本库函数.ERB | 15 |
| M_KOJO_KX_X2_道具系指令.ERB | 15 |
| M_KOJO_KX_X2_高潮.ERB | 45 |
| M_KOJO_KX_X2_高潮（详细版）.ERB | 45 |

合计 **887** 个模板函数。

## 指令编号 → 模板函数 反查

写某条指令时先在这里查它属于哪个模板文件。

| 指令 | 包含的函数（行号） | 所在文件 |
|---|---|---|
| 00 | MESSAGE_PALAMCNG_A : 264 | M_KOJO_KX_X2_高潮.ERB |
| 00 | MESSAGE_PALAMCNG_A : 478 | M_KOJO_KX_X2_高潮（详细版）.ERB |
| 10 | EVENT : 1362 | M_KOJO_KX_X2_事件系.ERB |
| 10 | DIARY_XXX : 320 | M_KOJO_KX_X2_日记（简易版）.ERB |
| 10 | MESSAGE_SCOM : 420 | M_KOJO_KX_X2_派生指令.ERB |
| 11 | MESSAGE_COUNTER_MESSAGECHECK : 142 ／ MESSAGE_COUNTER : 147 | M_KOJO_KX_X2_COUNTER系.ERB |
| 11 | EVENT : 1494 | M_KOJO_KX_X2_事件系.ERB |
| 11 | MESSAGE_SCOM : 493 | M_KOJO_KX_X2_派生指令.ERB |
| 11 | MESSAGE_COM : 987 | M_KOJO_KX_X2_爱抚系指令.ERB |
| 11 | MESSAGE_CUSTOM_COM : 131 | M_KOJO_KX_X2_自定义系指令.ERB |
| 12 | MESSAGE_COUNTER_MESSAGECHECK : 157 ／ MESSAGE_COUNTER : 162 | M_KOJO_KX_X2_COUNTER系.ERB |
| 12 | EVENT : 1522 ／ DAILY_EVENT_MESSAGECHECK : 3678 ／ DAILY_EVENT : 3690 | M_KOJO_KX_X2_事件系.ERB |
| 12 | MESSAGE_SCOM : 565 | M_KOJO_KX_X2_派生指令.ERB |
| 12 | MESSAGE_COM : 1061 | M_KOJO_KX_X2_爱抚系指令.ERB |
| 12 | MESSAGE_CUSTOM_COM : 168 | M_KOJO_KX_X2_自定义系指令.ERB |
| 13 | MESSAGE_COUNTER_MESSAGECHECK : 172 ／ MESSAGE_COUNTER : 177 | M_KOJO_KX_X2_COUNTER系.ERB |
| 13 | SUCCESS_CUSTOM_COM : 22 ／ MESSAGE_CUSTOM_COM : 32 | M_KOJO_KX_X2_MARRIAGE.ERB |
| 13 | EVENT : 1598 | M_KOJO_KX_X2_事件系.ERB |
| 13 | MESSAGE_SCOM : 599 | M_KOJO_KX_X2_派生指令.ERB |
| 13 | MESSAGE_COM : 1076 | M_KOJO_KX_X2_爱抚系指令.ERB |
| 14 | MESSAGE_COUNTER_MESSAGECHECK : 187 ／ MESSAGE_COUNTER : 192 | M_KOJO_KX_X2_COUNTER系.ERB |
| 14 | EVENT : 1631 | M_KOJO_KX_X2_事件系.ERB |
| 14 | MESSAGE_SCOM : 671 | M_KOJO_KX_X2_派生指令.ERB |
| 15 | MESSAGE_COUNTER_MESSAGECHECK : 202 ／ MESSAGE_COUNTER : 207 | M_KOJO_KX_X2_COUNTER系.ERB |
| 15 | EVENT : 1658 | M_KOJO_KX_X2_事件系.ERB |
| 15 | MESSAGE_SCOM : 704 | M_KOJO_KX_X2_派生指令.ERB |
| 15 | MESSAGE_COM : 1152 | M_KOJO_KX_X2_爱抚系指令.ERB |
| 16 | MESSAGE_COUNTER_MESSAGECHECK : 217 ／ MESSAGE_COUNTER : 222 | M_KOJO_KX_X2_COUNTER系.ERB |
| 16 | EVENT : 1724 | M_KOJO_KX_X2_事件系.ERB |
| 16 | MESSAGE_SCOM : 738 | M_KOJO_KX_X2_派生指令.ERB |
| 17 | MESSAGE_COUNTER_MESSAGECHECK : 232 ／ MESSAGE_COUNTER : 237 | M_KOJO_KX_X2_COUNTER系.ERB |
| 17 | EVENT : 1749 | M_KOJO_KX_X2_事件系.ERB |
| 17 | MESSAGE_SCOM : 810 | M_KOJO_KX_X2_派生指令.ERB |
| 18 | EVENT : 2027 | M_KOJO_KX_X2_事件系.ERB |
| 19 | EVENT : 2070 | M_KOJO_KX_X2_事件系.ERB |
| 19 | MESSAGE_SCOM : 844 | M_KOJO_KX_X2_派生指令.ERB |
| 19 | MESSAGE_COM : 1229 | M_KOJO_KX_X2_爱抚系指令.ERB |
| 20 | MESSAGE_COUNTER_MESSAGECHECK : 250 ／ MESSAGE_COUNTER : 255 | M_KOJO_KX_X2_COUNTER系.ERB |
| 20 | EVENT : 2107 | M_KOJO_KX_X2_事件系.ERB |
| 20 | MESSAGE_COM : 1244 | M_KOJO_KX_X2_爱抚系指令.ERB |
| 20 | MESSAGE_PALAMCNG_A : 394 | M_KOJO_KX_X2_高潮.ERB |
| 20 | MESSAGE_PALAMCNG_A : 608 | M_KOJO_KX_X2_高潮（详细版）.ERB |
| 21 | MESSAGE_COUNTER_MESSAGECHECK : 265 ／ MESSAGE_COUNTER : 270 | M_KOJO_KX_X2_COUNTER系.ERB |
| 21 | EVENT : 2230 | M_KOJO_KX_X2_事件系.ERB |
| 21 | MESSAGE_COM : 1321 | M_KOJO_KX_X2_爱抚系指令.ERB |
| 21 | MESSAGE_PALAMCNG_A : 406 | M_KOJO_KX_X2_高潮.ERB |
| 21 | MESSAGE_PALAMCNG_A : 620 | M_KOJO_KX_X2_高潮（详细版）.ERB |
| 22 | MESSAGE_COUNTER_MESSAGECHECK : 280 ／ MESSAGE_COUNTER : 285 | M_KOJO_KX_X2_COUNTER系.ERB |
| 22 | EVENT : 2320 | M_KOJO_KX_X2_事件系.ERB |
| 22 | MESSAGE_COM : 1394 | M_KOJO_KX_X2_爱抚系指令.ERB |
| 22 | MESSAGE_PALAMCNG_A : 418 | M_KOJO_KX_X2_高潮.ERB |
| 22 | MESSAGE_PALAMCNG_A : 632 | M_KOJO_KX_X2_高潮（详细版）.ERB |
| 23 | MESSAGE_COUNTER_MESSAGECHECK : 295 ／ MESSAGE_COUNTER : 300 | M_KOJO_KX_X2_COUNTER系.ERB |
| 23 | EVENT : 2394 | M_KOJO_KX_X2_事件系.ERB |
| 23 | MESSAGE_COM : 1458 | M_KOJO_KX_X2_爱抚系指令.ERB |
| 23 | MESSAGE_PALAMCNG_A : 456 ／ MESSAGE_PALAMCNG_A2 : 559 | M_KOJO_KX_X2_高潮.ERB |
| 23 | MESSAGE_PALAMCNG_A : 670 ／ MESSAGE_PALAMCNG_A2 : 773 | M_KOJO_KX_X2_高潮（详细版）.ERB |
| 24 | MESSAGE_COUNTER_MESSAGECHECK : 310 ／ MESSAGE_COUNTER : 315 | M_KOJO_KX_X2_COUNTER系.ERB |
| 24 | EVENT : 2420 | M_KOJO_KX_X2_事件系.ERB |
| 25 | MESSAGE_COUNTER_MESSAGECHECK : 325 ／ MESSAGE_COUNTER : 330 | M_KOJO_KX_X2_COUNTER系.ERB |
| 25 | EVENT : 2457 | M_KOJO_KX_X2_事件系.ERB |
| 25 | MESSAGE_COM : 1523 | M_KOJO_KX_X2_爱抚系指令.ERB |
| 26 | MESSAGE_COUNTER_MESSAGECHECK : 340 ／ MESSAGE_COUNTER : 345 | M_KOJO_KX_X2_COUNTER系.ERB |
| 26 | EVENT : 2561 | M_KOJO_KX_X2_事件系.ERB |
| 26 | MESSAGE_PALAMCNG_A : 468 | M_KOJO_KX_X2_高潮.ERB |
| 26 | MESSAGE_PALAMCNG_A : 682 | M_KOJO_KX_X2_高潮（详细版）.ERB |
| 27 | MESSAGE_COUNTER_MESSAGECHECK : 354 ／ MESSAGE_COUNTER : 359 | M_KOJO_KX_X2_COUNTER系.ERB |
| 27 | EVENT : 2629 | M_KOJO_KX_X2_事件系.ERB |
| 28 | MESSAGE_COUNTER_MESSAGECHECK : 368 ／ MESSAGE_COUNTER : 373 | M_KOJO_KX_X2_COUNTER系.ERB |
| 28 | EVENT : 2711 | M_KOJO_KX_X2_事件系.ERB |
| 29 | EVENT : 2791 | M_KOJO_KX_X2_事件系.ERB |
| 30 | MESSAGE_COUNTER_MESSAGECHECK : 386 ／ MESSAGE_COUNTER : 391 | M_KOJO_KX_X2_COUNTER系.ERB |
| 30 | EVENT : 2818 | M_KOJO_KX_X2_事件系.ERB |
| 31 | MESSAGE_COUNTER_MESSAGECHECK : 401 ／ MESSAGE_COUNTER : 406 | M_KOJO_KX_X2_COUNTER系.ERB |
| 31 | EVENT : 2866 | M_KOJO_KX_X2_事件系.ERB |
| 32 | MESSAGE_COUNTER_MESSAGECHECK : 416 ／ MESSAGE_COUNTER : 421 | M_KOJO_KX_X2_COUNTER系.ERB |
| 32 | EVENT : 2899 | M_KOJO_KX_X2_事件系.ERB |
| 33 | MESSAGE_COUNTER_MESSAGECHECK : 431 ／ MESSAGE_COUNTER : 436 | M_KOJO_KX_X2_COUNTER系.ERB |
| 33 | EVENT : 3342 | M_KOJO_KX_X2_事件系.ERB |
| 34 | MESSAGE_COUNTER_MESSAGECHECK : 446 ／ MESSAGE_COUNTER : 451 | M_KOJO_KX_X2_COUNTER系.ERB |
| 34 | EVENT : 3358 | M_KOJO_KX_X2_事件系.ERB |
| 35 | MESSAGE_COUNTER_MESSAGECHECK : 461 ／ MESSAGE_COUNTER : 466 | M_KOJO_KX_X2_COUNTER系.ERB |
| 36 | MESSAGE_COUNTER_MESSAGECHECK : 476 ／ MESSAGE_COUNTER : 481 | M_KOJO_KX_X2_COUNTER系.ERB |
| 39 | MESSAGE_COUNTER_MESSAGECHECK : 492 ／ MESSAGE_COUNTER : 497 | M_KOJO_KX_X2_COUNTER系.ERB |
| 40 | MESSAGE_COM : 50 | M_KOJO_KX_X2_道具系指令.ERB |
| 41 | MESSAGE_COUNTER_MESSAGECHECK : 510 ／ MESSAGE_COUNTER : 515 | M_KOJO_KX_X2_COUNTER系.ERB |
| 41 | MESSAGE_COM : 89 | M_KOJO_KX_X2_道具系指令.ERB |
| 42 | MESSAGE_COM : 128 | M_KOJO_KX_X2_道具系指令.ERB |
| 43 | MESSAGE_COUNTER_MESSAGECHECK : 525 ／ MESSAGE_COUNTER : 530 | M_KOJO_KX_X2_COUNTER系.ERB |
| 43 | MESSAGE_COM : 167 | M_KOJO_KX_X2_道具系指令.ERB |
| 44 | MESSAGE_COUNTER_MESSAGECHECK : 539 ／ MESSAGE_COUNTER : 544 | M_KOJO_KX_X2_COUNTER系.ERB |
| 44 | MESSAGE_COM : 206 | M_KOJO_KX_X2_道具系指令.ERB |
| 45 | MESSAGE_COM : 250 | M_KOJO_KX_X2_道具系指令.ERB |
| 46 | MESSAGE_COM : 289 | M_KOJO_KX_X2_道具系指令.ERB |
| 47 | MESSAGE_COM : 328 | M_KOJO_KX_X2_道具系指令.ERB |
| 48 | MESSAGE_COM : 367 | M_KOJO_KX_X2_道具系指令.ERB |
| 49 | MESSAGE_COM : 406 | M_KOJO_KX_X2_道具系指令.ERB |
| 50 | MESSAGE_COUNTER_MESSAGECHECK : 557 ／ MESSAGE_COUNTER : 562 | M_KOJO_KX_X2_COUNTER系.ERB |
| 50 | MESSAGE_COM : 432 | M_KOJO_KX_X2_道具系指令.ERB |
| 51 | MESSAGE_COUNTER_MESSAGECHECK : 572 ／ MESSAGE_COUNTER : 577 | M_KOJO_KX_X2_COUNTER系.ERB |
| 52 | MESSAGE_COUNTER_MESSAGECHECK : 587 ／ MESSAGE_COUNTER : 592 | M_KOJO_KX_X2_COUNTER系.ERB |
| 53 | MESSAGE_COUNTER_MESSAGECHECK : 602 ／ MESSAGE_COUNTER : 607 | M_KOJO_KX_X2_COUNTER系.ERB |
| 54 | MESSAGE_COUNTER_MESSAGECHECK : 617 ／ MESSAGE_COUNTER : 622 | M_KOJO_KX_X2_COUNTER系.ERB |
| 55 | MESSAGE_COUNTER_MESSAGECHECK : 632 ／ MESSAGE_COUNTER : 637 | M_KOJO_KX_X2_COUNTER系.ERB |
| 56 | MESSAGE_COUNTER_MESSAGECHECK : 647 ／ MESSAGE_COUNTER : 652 | M_KOJO_KX_X2_COUNTER系.ERB |
| 57 | MESSAGE_COUNTER_MESSAGECHECK : 662 ／ MESSAGE_COUNTER : 667 | M_KOJO_KX_X2_COUNTER系.ERB |
| 58 | MESSAGE_COUNTER_MESSAGECHECK : 677 ／ MESSAGE_COUNTER : 682 | M_KOJO_KX_X2_COUNTER系.ERB |
| 59 | MESSAGE_COUNTER_MESSAGECHECK : 692 ／ MESSAGE_COUNTER : 697 | M_KOJO_KX_X2_COUNTER系.ERB |
| 60 | MESSAGE_COUNTER_MESSAGECHECK : 707 ／ MESSAGE_COUNTER : 712 | M_KOJO_KX_X2_COUNTER系.ERB |
| 60 | MESSAGE_COM : 115 | M_KOJO_KX_X2_性交系指令.ERB |
| 60 | SUCCESS_SCOM : 2879 ／ MESSAGE_MESSAGECHECK_SCOM : 2888 ／ MESSAGE_SCOM : 2893 | M_KOJO_KX_X2_日常系指令.ERB |
| 61 | MESSAGE_COUNTER_MESSAGECHECK : 722 ／ MESSAGE_COUNTER : 727 | M_KOJO_KX_X2_COUNTER系.ERB |
| 61 | MESSAGE_COM : 209 | M_KOJO_KX_X2_性交系指令.ERB |
| 61 | MESSAGE_MESSAGECHECK_SCOM : 2913 ／ MESSAGE_SCOM : 2918 | M_KOJO_KX_X2_日常系指令.ERB |
| 62 | MESSAGE_COM : 302 | M_KOJO_KX_X2_性交系指令.ERB |
| 62 | SUCCESS_SCOM : 2931 ／ MESSAGE_MESSAGECHECK_SCOM : 2940 ／ MESSAGE_SCOM : 2945 | M_KOJO_KX_X2_日常系指令.ERB |
| 63 | MESSAGE_COM : 390 | M_KOJO_KX_X2_性交系指令.ERB |
| 63 | SUCCESS_SCOM : 2970 ／ MESSAGE_MESSAGECHECK_SCOM : 2979 ／ MESSAGE_SCOM : 2984 | M_KOJO_KX_X2_日常系指令.ERB |
| 64 | MESSAGE_COM : 479 | M_KOJO_KX_X2_性交系指令.ERB |
| 65 | MESSAGE_COM : 536 | M_KOJO_KX_X2_性交系指令.ERB |
| 66 | MESSAGE_COM : 599 | M_KOJO_KX_X2_性交系指令.ERB |
| 67 | MESSAGE_COM : 662 | M_KOJO_KX_X2_性交系指令.ERB |
| 68 | MESSAGE_COM : 725 | M_KOJO_KX_X2_性交系指令.ERB |
| 69 | MESSAGE_COM : 788 | M_KOJO_KX_X2_性交系指令.ERB |
| 70 | MESSAGE_COUNTER_MESSAGECHECK : 741 ／ MESSAGE_COUNTER : 746 | M_KOJO_KX_X2_COUNTER系.ERB |
| 70 | MESSAGE_COM : 851 | M_KOJO_KX_X2_性交系指令.ERB |
| 71 | MESSAGE_COUNTER_MESSAGECHECK : 756 ／ MESSAGE_COUNTER : 761 | M_KOJO_KX_X2_COUNTER系.ERB |
| 71 | MESSAGE_COM : 915 | M_KOJO_KX_X2_性交系指令.ERB |
| 72 | MESSAGE_COUNTER_MESSAGECHECK : 771 ／ MESSAGE_COUNTER : 776 | M_KOJO_KX_X2_COUNTER系.ERB |
| 72 | MESSAGE_COM : 967 | M_KOJO_KX_X2_性交系指令.ERB |
| 73 | MESSAGE_COUNTER_MESSAGECHECK : 786 ／ MESSAGE_COUNTER : 791 | M_KOJO_KX_X2_COUNTER系.ERB |
| 73 | MESSAGE_COM : 1023 | M_KOJO_KX_X2_性交系指令.ERB |
| 74 | MESSAGE_COUNTER_MESSAGECHECK : 801 ／ MESSAGE_COUNTER : 806 | M_KOJO_KX_X2_COUNTER系.ERB |
| 74 | MESSAGE_COM : 1079 | M_KOJO_KX_X2_性交系指令.ERB |
| 75 | MESSAGE_COUNTER_MESSAGECHECK : 816 ／ MESSAGE_COUNTER : 821 | M_KOJO_KX_X2_COUNTER系.ERB |
| 75 | MESSAGE_COM : 1135 | M_KOJO_KX_X2_性交系指令.ERB |
| 76 | MESSAGE_COUNTER_MESSAGECHECK : 831 ／ MESSAGE_COUNTER : 836 | M_KOJO_KX_X2_COUNTER系.ERB |
| 77 | MESSAGE_COUNTER_MESSAGECHECK : 846 ／ MESSAGE_COUNTER : 851 | M_KOJO_KX_X2_COUNTER系.ERB |
| 78 | MESSAGE_COUNTER_MESSAGECHECK : 860 ／ MESSAGE_COUNTER : 865 | M_KOJO_KX_X2_COUNTER系.ERB |
| 79 | MESSAGE_COM : 1176 | M_KOJO_KX_X2_性交系指令.ERB |
| 80 | MESSAGE_COUNTER_MESSAGECHECK : 878 ／ MESSAGE_COUNTER : 883 | M_KOJO_KX_X2_COUNTER系.ERB |
| 80 | MESSAGE_COM : 83 | M_KOJO_KX_X2_侍奉系指令.ERB |
| 80 | SUCCESS_SCOM : 3021 ／ MESSAGE_MESSAGECHECK_SCOM : 3030 ／ MESSAGE_SCOM : 3035 | M_KOJO_KX_X2_日常系指令.ERB |
| 81 | MESSAGE_COM : 129 | M_KOJO_KX_X2_侍奉系指令.ERB |
| 82 | MESSAGE_COM : 177 | M_KOJO_KX_X2_侍奉系指令.ERB |
| 83 | MESSAGE_COUNTER_MESSAGECHECK : 893 ／ MESSAGE_COUNTER : 898 | M_KOJO_KX_X2_COUNTER系.ERB |
| 83 | MESSAGE_COM : 221 | M_KOJO_KX_X2_侍奉系指令.ERB |
| 84 | MESSAGE_COUNTER_MESSAGECHECK : 907 ／ MESSAGE_COUNTER : 912 | M_KOJO_KX_X2_COUNTER系.ERB |
| 84 | MESSAGE_COM : 265 | M_KOJO_KX_X2_侍奉系指令.ERB |
| 85 | MESSAGE_COUNTER_MESSAGECHECK : 921 ／ MESSAGE_COUNTER : 926 | M_KOJO_KX_X2_COUNTER系.ERB |
| 85 | MESSAGE_COM : 304 | M_KOJO_KX_X2_侍奉系指令.ERB |
| 86 | MESSAGE_COUNTER_MESSAGECHECK : 936 ／ MESSAGE_COUNTER : 941 | M_KOJO_KX_X2_COUNTER系.ERB |
| 87 | MESSAGE_COUNTER_MESSAGECHECK : 951 ／ MESSAGE_COUNTER : 956 | M_KOJO_KX_X2_COUNTER系.ERB |
| 88 | MESSAGE_COUNTER_MESSAGECHECK : 966 ／ MESSAGE_COUNTER : 971 | M_KOJO_KX_X2_COUNTER系.ERB |
| 88 | MESSAGE_COM : 348 | M_KOJO_KX_X2_侍奉系指令.ERB |
| 89 | MESSAGE_COUNTER_MESSAGECHECK : 981 ／ MESSAGE_COUNTER : 986 | M_KOJO_KX_X2_COUNTER系.ERB |
| 90 | MESSAGE_COUNTER_MESSAGECHECK : 996 ／ MESSAGE_COUNTER : 1001 | M_KOJO_KX_X2_COUNTER系.ERB |
| 90 | MESSAGE_COM : 118 | M_KOJO_KX_X2_其他系指令.ERB |
| 91 | MESSAGE_COUNTER_MESSAGECHECK : 1011 ／ MESSAGE_COUNTER : 1016 | M_KOJO_KX_X2_COUNTER系.ERB |
| 91 | MESSAGE_COM : 159 | M_KOJO_KX_X2_其他系指令.ERB |
| 92 | MESSAGE_COM : 200 | M_KOJO_KX_X2_其他系指令.ERB |
| 93 | MESSAGE_COUNTER_MESSAGECHECK : 1042 ／ MESSAGE_COUNTER : 1047 | M_KOJO_KX_X2_COUNTER系.ERB |
| 93 | MESSAGE_COM : 263 | M_KOJO_KX_X2_其他系指令.ERB |
| 94 | MESSAGE_COUNTER_MESSAGECHECK : 1056 ／ MESSAGE_COUNTER : 1061 | M_KOJO_KX_X2_COUNTER系.ERB |
| 94 | MESSAGE_COM : 326 | M_KOJO_KX_X2_其他系指令.ERB |
| 96 | MESSAGE_COM : 71 | M_KOJO_KX_X2_其他系指令.ERB |
| 100 | MESSAGE_COM : 119 | M_KOJO_KX_X2_施虐系指令.ERB |
| 100 | SUCCESS_CUSTOM_COM : 191 ／ MESSAGE_MESSAGECHECK_CUSTOM_COM : 199 ／ MESSAGE_CUSTOM_COM : 202 | M_KOJO_KX_X2_自定义系指令.ERB |
| 101 | MESSAGE_COM : 162 | M_KOJO_KX_X2_施虐系指令.ERB |
| 101 | MESSAGE_MESSAGECHECK_CUSTOM_COM : 261 ／ MESSAGE_CUSTOM_COM : 264 | M_KOJO_KX_X2_自定义系指令.ERB |
| 102 | MESSAGE_COM : 206 | M_KOJO_KX_X2_施虐系指令.ERB |
| 103 | MESSAGE_COM : 250 | M_KOJO_KX_X2_施虐系指令.ERB |
| 104 | MESSAGE_COM : 294 | M_KOJO_KX_X2_施虐系指令.ERB |
| 105 | MESSAGE_COM : 346 | M_KOJO_KX_X2_施虐系指令.ERB |
| 106 | MESSAGE_COM : 398 | M_KOJO_KX_X2_施虐系指令.ERB |
| 107 | MESSAGE_COM : 450 | M_KOJO_KX_X2_施虐系指令.ERB |
| 108 | MESSAGE_COM : 502 | M_KOJO_KX_X2_施虐系指令.ERB |
| 120 | MESSAGE_COUNTER_MESSAGECHECK : 1074 ／ MESSAGE_COUNTER : 1079 | M_KOJO_KX_X2_COUNTER系.ERB |
| 120 | MESSAGE_COM : 395 | M_KOJO_KX_X2_其他系指令.ERB |
| 121 | MESSAGE_COUNTER_MESSAGECHECK : 1088 ／ MESSAGE_COUNTER : 1093 | M_KOJO_KX_X2_COUNTER系.ERB |
| 121 | MESSAGE_COM : 436 | M_KOJO_KX_X2_其他系指令.ERB |
| 122 | MESSAGE_COUNTER_MESSAGECHECK : 1102 ／ MESSAGE_COUNTER : 1107 | M_KOJO_KX_X2_COUNTER系.ERB |
| 123 | MESSAGE_COUNTER_MESSAGECHECK : 1116 ／ MESSAGE_COUNTER : 1121 | M_KOJO_KX_X2_COUNTER系.ERB |
| 123 | MESSAGE_COM : 477 | M_KOJO_KX_X2_其他系指令.ERB |
| 124 | MESSAGE_COUNTER_MESSAGECHECK : 1130 ／ MESSAGE_COUNTER : 1135 | M_KOJO_KX_X2_COUNTER系.ERB |
| 124 | MESSAGE_COM : 518 | M_KOJO_KX_X2_其他系指令.ERB |
| 125 | MESSAGE_COUNTER_MESSAGECHECK : 1144 ／ MESSAGE_COUNTER : 1149 | M_KOJO_KX_X2_COUNTER系.ERB |
| 125 | MESSAGE_COM : 559 | M_KOJO_KX_X2_其他系指令.ERB |
| 126 | MESSAGE_COUNTER_MESSAGECHECK : 1158 ／ MESSAGE_COUNTER : 1163 | M_KOJO_KX_X2_COUNTER系.ERB |
| 126 | MESSAGE_COM : 600 | M_KOJO_KX_X2_其他系指令.ERB |
| 127 | MESSAGE_COUNTER_MESSAGECHECK : 1172 ／ MESSAGE_COUNTER : 1177 | M_KOJO_KX_X2_COUNTER系.ERB |
| 127 | MESSAGE_COM : 641 | M_KOJO_KX_X2_其他系指令.ERB |
| 128 | MESSAGE_COUNTER_MESSAGECHECK : 1186 ／ MESSAGE_COUNTER : 1191 | M_KOJO_KX_X2_COUNTER系.ERB |
| 129 | MESSAGE_COUNTER_MESSAGECHECK : 1200 ／ MESSAGE_COUNTER : 1205 | M_KOJO_KX_X2_COUNTER系.ERB |
| 130 | MESSAGE_COM : 688 | M_KOJO_KX_X2_其他系指令.ERB |
| 131 | MESSAGE_COM : 751 | M_KOJO_KX_X2_其他系指令.ERB |
| 132 | MESSAGE_COM : 814 | M_KOJO_KX_X2_其他系指令.ERB |
| 133 | MESSAGE_COM : 877 | M_KOJO_KX_X2_其他系指令.ERB |
| 140 | MESSAGE_COM : 74 | M_KOJO_KX_X2_硬核系指令.ERB |
| 144 | MESSAGE_COM : 118 | M_KOJO_KX_X2_硬核系指令.ERB |
| 150 | MESSAGE_COM : 158 | M_KOJO_KX_X2_硬核系指令.ERB |
| 180 | MESSAGE_COM : 946 | M_KOJO_KX_X2_其他系指令.ERB |
| 181 | MESSAGE_COM : 987 | M_KOJO_KX_X2_其他系指令.ERB |
| 182 | MESSAGE_COM : 1028 | M_KOJO_KX_X2_其他系指令.ERB |
| 183 | MESSAGE_COM : 1069 | M_KOJO_KX_X2_其他系指令.ERB |
| 184 | MESSAGE_COM : 1111 | M_KOJO_KX_X2_其他系指令.ERB |
| 186 | MESSAGE_COM : 1167 | M_KOJO_KX_X2_其他系指令.ERB |
| 188 | MESSAGE_COM : 1209 | M_KOJO_KX_X2_其他系指令.ERB |
| 189 | MESSAGE_COM : 1265 | M_KOJO_KX_X2_其他系指令.ERB |
| 191 | MESSAGE_COM : 1307 | M_KOJO_KX_X2_其他系指令.ERB |
| 192 | MESSAGE_COM : 1348 | M_KOJO_KX_X2_其他系指令.ERB |
| 300 | SUCCESS_COM : 18 ／ MESSAGE_MESSAGECHECK_COM : 30 ／ MESSAGE_COM : 35 | M_KOJO_KX_X2_日常系指令.ERB |
| 301 | SUCCESS_COM : 72 ／ MESSAGE_MESSAGECHECK_COM : 82 ／ MESSAGE_COM : 87 | M_KOJO_KX_X2_日常系指令.ERB |
| 302 | SUCCESS_COM : 107 ／ MESSAGE_MESSAGECHECK_COM : 117 ／ MESSAGE_COM : 122 | M_KOJO_KX_X2_日常系指令.ERB |
| 303 | SUCCESS_COM : 145 ／ MESSAGE_MESSAGECHECK_COM : 154 ／ MESSAGE_COM : 159 | M_KOJO_KX_X2_日常系指令.ERB |
| 304 | SUCCESS_COM : 189 ／ MESSAGE_MESSAGECHECK_COM : 198 ／ MESSAGE_COM : 203 | M_KOJO_KX_X2_日常系指令.ERB |
| 305 | SUCCESS_COM : 239 ／ MESSAGE_MESSAGECHECK_COM : 249 ／ MESSAGE_COM : 254 | M_KOJO_KX_X2_日常系指令.ERB |
| 306 | MESSAGE_MESSAGECHECK_COM : 285 ／ MESSAGE_COM : 290 | M_KOJO_KX_X2_日常系指令.ERB |
| 307 | SUCCESS_COM : 319 ／ MESSAGE_MESSAGECHECK_COM : 329 ／ MESSAGE_COM : 334 | M_KOJO_KX_X2_日常系指令.ERB |
| 308 | SUCCESS_COM : 365 ／ MESSAGE_MESSAGECHECK_COM : 373 ／ MESSAGE_COM : 378 | M_KOJO_KX_X2_日常系指令.ERB |
| 309 | SUCCESS_COM : 396 ／ MESSAGE_MESSAGECHECK_COM : 406 ／ MESSAGE_COM : 411 | M_KOJO_KX_X2_日常系指令.ERB |
| 310 | SUCCESS_COM : 14 ／ MESSAGE_MESSAGECHECK_COM : 23 ／ MESSAGE_COM : 26 | M_KOJO_KX_X2_性骚扰指令.ERB |
| 311 | SUCCESS_COM : 78 ／ MESSAGE_MESSAGECHECK_COM : 89 ／ MESSAGE_COM : 92 | M_KOJO_KX_X2_性骚扰指令.ERB |
| 312 | SUCCESS_COM : 155 ／ MESSAGE_MESSAGECHECK_COM : 168 ／ MESSAGE_COM : 171 | M_KOJO_KX_X2_性骚扰指令.ERB |
| 313 | SUCCESS_COM : 232 ／ MESSAGE_MESSAGECHECK_COM : 240 ／ MESSAGE_COM : 243 | M_KOJO_KX_X2_性骚扰指令.ERB |
| 314 | SUCCESS_COM : 305 ／ MESSAGE_MESSAGECHECK_COM : 312 ／ MESSAGE_COM : 315 | M_KOJO_KX_X2_性骚扰指令.ERB |
| 315 | SUCCESS_COM : 353 ／ MESSAGE_MESSAGECHECK_COM : 360 ／ MESSAGE_COM : 363 | M_KOJO_KX_X2_性骚扰指令.ERB |
| 316 | SUCCESS_COM : 418 ／ MESSAGE_MESSAGECHECK_COM : 425 ／ MESSAGE_COM : 428 | M_KOJO_KX_X2_性骚扰指令.ERB |
| 317 | MESSAGE_MESSAGECHECK_COM : 470 ／ MESSAGE_COM : 473 | M_KOJO_KX_X2_性骚扰指令.ERB |
| 318 | MESSAGE_MESSAGECHECK_COM : 527 ／ MESSAGE_COM : 530 | M_KOJO_KX_X2_性骚扰指令.ERB |
| 320 | MESSAGE_MESSAGECHECK_COM : 577 ／ MESSAGE_COM : 580 | M_KOJO_KX_X2_性骚扰指令.ERB |
| 322 | MESSAGE_MESSAGECHECK_COM : 627 ／ MESSAGE_COM : 630 | M_KOJO_KX_X2_性骚扰指令.ERB |
| 323 | MESSAGE_MESSAGECHECK_COM : 676 ／ MESSAGE_COM : 679 | M_KOJO_KX_X2_性骚扰指令.ERB |
| 330 | MESSAGE_MESSAGECHECK_COM : 722 ／ MESSAGE_COM : 725 | M_KOJO_KX_X2_性骚扰指令.ERB |
| 331 | SUCCESS_COM : 440 ／ MESSAGE_MESSAGECHECK_COM : 463 ／ MESSAGE_COM : 468 | M_KOJO_KX_X2_日常系指令.ERB |
| 332 | SUCCESS_COM : 512 ／ MESSAGE_MESSAGECHECK_COM : 524 ／ MESSAGE_COM : 529 | M_KOJO_KX_X2_日常系指令.ERB |
| 333 | SUCCESS_COM : 563 ／ MESSAGE_MESSAGECHECK_COM : 572 ／ MESSAGE_COM : 577 | M_KOJO_KX_X2_日常系指令.ERB |
| 334 | SUCCESS_COM : 609 ／ MESSAGE_MESSAGECHECK_COM : 618 ／ MESSAGE_COM : 623 | M_KOJO_KX_X2_日常系指令.ERB |
| 335 | SUCCESS_COM : 655 ／ MESSAGE_MESSAGECHECK_COM : 664 ／ MESSAGE_COM : 669 | M_KOJO_KX_X2_日常系指令.ERB |
| 336 | SUCCESS_COM : 690 ／ MESSAGE_MESSAGECHECK_COM : 701 ／ MESSAGE_COM : 706 | M_KOJO_KX_X2_日常系指令.ERB |
| 337 | SUCCESS_COM : 739 ／ MESSAGE_MESSAGECHECK_COM : 747 ／ MESSAGE_COM : 752 | M_KOJO_KX_X2_日常系指令.ERB |
| 350 | MESSAGE_MESSAGECHECK_COM : 837 ／ MESSAGE_COM : 842 | M_KOJO_KX_X2_日常系指令.ERB |
| 351 | MESSAGE_COM : 909 | M_KOJO_KX_X2_日常系指令.ERB |
| 352 | SUCCESS_COM : 929 ／ MESSAGE_MESSAGECHECK_COM : 938 ／ MESSAGE_COM : 943 | M_KOJO_KX_X2_日常系指令.ERB |
| 353 | MESSAGE_MESSAGECHECK_COM : 961 ／ MESSAGE_COM : 966 | M_KOJO_KX_X2_日常系指令.ERB |
| 354 | MESSAGE_MESSAGECHECK_COM : 978 ／ MESSAGE_COM : 983 | M_KOJO_KX_X2_日常系指令.ERB |
| 355 | MESSAGE_MESSAGECHECK_COM : 1000 ／ MESSAGE_COM : 1005 | M_KOJO_KX_X2_日常系指令.ERB |
| 356 | SUCCESS_COM : 1015 ／ MESSAGE_MESSAGECHECK_COM : 1024 ／ MESSAGE_COM : 1029 | M_KOJO_KX_X2_日常系指令.ERB |
| 360 | MESSAGE_MESSAGECHECK_COM : 1053 ／ MESSAGE_COM : 1058 | M_KOJO_KX_X2_日常系指令.ERB |
| 361 | MESSAGE_MESSAGECHECK_COM : 1164 ／ MESSAGE_COM : 1169 | M_KOJO_KX_X2_日常系指令.ERB |
| 363 | SUCCESS_COM : 1287 ／ MESSAGE_MESSAGECHECK_COM : 1296 ／ MESSAGE_COM : 1301 | M_KOJO_KX_X2_日常系指令.ERB |
| 364 | MESSAGE_MESSAGECHECK_COM : 1320 ／ MESSAGE_COM : 1325 | M_KOJO_KX_X2_日常系指令.ERB |
| 365 | MESSAGE_MESSAGECHECK_COM : 1339 ／ MESSAGE_COM : 1344 | M_KOJO_KX_X2_日常系指令.ERB |
| 368 | MESSAGE_MESSAGECHECK_COM : 1361 ／ MESSAGE_COM : 1366 | M_KOJO_KX_X2_日常系指令.ERB |
| 402 | MESSAGE_MESSAGECHECK_COM : 1477 ／ MESSAGE_COM : 1482 | M_KOJO_KX_X2_日常系指令.ERB |
| 403 | MESSAGE_MESSAGECHECK_COM : 1500 ／ MESSAGE_COM : 1505 | M_KOJO_KX_X2_日常系指令.ERB |
| 405 | MESSAGE_MESSAGECHECK_COM : 1524 ／ MESSAGE_COM : 1529 | M_KOJO_KX_X2_日常系指令.ERB |
| 406 | MESSAGE_COM : 312 | M_KOJO_KX_X2_日记.ERB |
| 406 | MESSAGE_MESSAGECHECK_COM : 366 ／ MESSAGE_COM : 371 | M_KOJO_KX_X2_日记（简易版）.ERB |
| 410 | MESSAGE_MESSAGECHECK_COM : 1558 ／ MESSAGE_COM : 1563 | M_KOJO_KX_X2_日常系指令.ERB |
| 411 | MESSAGE_MESSAGECHECK_COM : 1587 ／ MESSAGE_COM : 1592 | M_KOJO_KX_X2_日常系指令.ERB |
| 412 | MESSAGE_MESSAGECHECK_COM : 1638 ／ MESSAGE_COM : 1643 | M_KOJO_KX_X2_日常系指令.ERB |
| 413 | MESSAGE_MESSAGECHECK_COM : 1666 ／ MESSAGE_COM : 1671 | M_KOJO_KX_X2_日常系指令.ERB |
| 414 | SUCCESS_COM : 1715 ／ MESSAGE_MESSAGECHECK_COM : 1724 ／ MESSAGE_COM : 1729 | M_KOJO_KX_X2_日常系指令.ERB |
| 415 | SUCCESS_COM : 1762 ／ MESSAGE_MESSAGECHECK_COM : 1771 ／ MESSAGE_COM : 1776 | M_KOJO_KX_X2_日常系指令.ERB |
| 416 | SUCCESS_COM : 1817 ／ MESSAGE_MESSAGECHECK_COM : 1826 ／ MESSAGE_COM : 1831 | M_KOJO_KX_X2_日常系指令.ERB |
| 417 | MESSAGE_MESSAGECHECK_COM : 1875 ／ MESSAGE_COM : 1880 | M_KOJO_KX_X2_日常系指令.ERB |
| 421 | MESSAGE_MESSAGECHECK_COM : 1916 ／ MESSAGE_COM : 1921 | M_KOJO_KX_X2_日常系指令.ERB |
| 431 | MESSAGE_MESSAGECHECK_COM : 1955 ／ MESSAGE_COM : 1960 | M_KOJO_KX_X2_日常系指令.ERB |
| 432 | MESSAGE_MESSAGECHECK_COM : 1981 ／ MESSAGE_COM : 1986 | M_KOJO_KX_X2_日常系指令.ERB |
| 436 | MESSAGE_MESSAGECHECK_COM : 2007 ／ MESSAGE_COM : 2012 | M_KOJO_KX_X2_日常系指令.ERB |
| 440 | MESSAGE_MESSAGECHECK_COM : 2058 ／ MESSAGE_COM : 2063 | M_KOJO_KX_X2_日常系指令.ERB |
| 441 | MESSAGE_MESSAGECHECK_COM : 2097 ／ MESSAGE_COM : 2102 | M_KOJO_KX_X2_日常系指令.ERB |
| 442 | MESSAGE_MESSAGECHECK_COM : 2124 ／ MESSAGE_COM : 2129 | M_KOJO_KX_X2_日常系指令.ERB |
| 445 | MESSAGE_MESSAGECHECK_COM : 2161 ／ MESSAGE_COM : 2166 | M_KOJO_KX_X2_日常系指令.ERB |
| 448 | MESSAGE_MESSAGECHECK_COM : 2193 ／ MESSAGE_COM : 2198 | M_KOJO_KX_X2_日常系指令.ERB |
| 449 | MESSAGE_MESSAGECHECK_COM : 2237 ／ MESSAGE_COM : 2242 | M_KOJO_KX_X2_日常系指令.ERB |
| 483 | MESSAGE_MESSAGECHECK_COM : 2280 ／ MESSAGE_COM : 2285 | M_KOJO_KX_X2_日常系指令.ERB |
| 484 | MESSAGE_MESSAGECHECK_COM : 2316 ／ MESSAGE_COM : 2321 | M_KOJO_KX_X2_日常系指令.ERB |
| 490 | MESSAGE_MESSAGECHECK_COM : 2349 ／ MESSAGE_COM : 2354 | M_KOJO_KX_X2_日常系指令.ERB |
| 603 | SUCCESS_COM : 2440 ／ MESSAGE_MESSAGECHECK_COM : 2449 ／ MESSAGE_COM : 2454 | M_KOJO_KX_X2_日常系指令.ERB |
| 604 | MESSAGE_MESSAGECHECK_COM : 2475 ／ MESSAGE_COM : 2480 | M_KOJO_KX_X2_日常系指令.ERB |
| 605 | SUCCESS_COM : 2497 ／ MESSAGE_MESSAGECHECK_COM : 2506 ／ MESSAGE_COM : 2511 | M_KOJO_KX_X2_日常系指令.ERB |
| 610 | SUCCESS_COM : 2525 ／ MESSAGE_MESSAGECHECK_COM : 2534 ／ MESSAGE_COM : 2539 | M_KOJO_KX_X2_日常系指令.ERB |
| 613 | SUCCESS_COM : 2557 ／ MESSAGE_MESSAGECHECK_COM : 2566 ／ MESSAGE_COM : 2571 | M_KOJO_KX_X2_日常系指令.ERB |
| 614 | MESSAGE_MESSAGECHECK_COM : 2579 ／ MESSAGE_COM : 2584 | M_KOJO_KX_X2_日常系指令.ERB |
| 615 | MESSAGE_MESSAGECHECK_COM : 2606 ／ MESSAGE_COM : 2611 | M_KOJO_KX_X2_日常系指令.ERB |
| 617 | SUCCESS_COM : 2637 ／ MESSAGE_MESSAGECHECK_COM : 2646 ／ MESSAGE_COM : 2651 | M_KOJO_KX_X2_日常系指令.ERB |
| 618 | MESSAGE_MESSAGECHECK_COM : 2662 ／ MESSAGE_COM : 2667 | M_KOJO_KX_X2_日常系指令.ERB |
| 620 | MESSAGE_MESSAGECHECK_COM : 2679 ／ MESSAGE_COM : 2684 | M_KOJO_KX_X2_日常系指令.ERB |
| 621 | MESSAGE_MESSAGECHECK_COM : 2738 ／ MESSAGE_COM : 2743 | M_KOJO_KX_X2_日常系指令.ERB |
| 626 | MESSAGE_MESSAGECHECK_COM : 2776 ／ MESSAGE_COM : 2781 | M_KOJO_KX_X2_日常系指令.ERB |
| 698 | MESSAGE_MESSAGECHECK_COM : 2831 ／ MESSAGE_COM : 2836 | M_KOJO_KX_X2_日常系指令.ERB |
| 699 | MESSAGE_MESSAGECHECK_COM : 2846 ／ MESSAGE_COM : 2851 | M_KOJO_KX_X2_日常系指令.ERB |

---

### M_KOJO_KX_X2_BANQUET.ERB
*6.4 KB ／ 193 行 ／ 5 个函数*

| 行号 | 函数名 | 用途 |
|---|---|---|
| 26 | `M_KOJO_XXX_EVENT_KX_BANQUET` | BANQUET_ID=宴会编号（对应 Add_Banquet_<编号>_*.ERB 的元数据） / ARG=预留数值参数（当前调用恒为0） |
| 93 | `M_KOJO_XXX_EVENT_KX_BANQUET_1` | 特定宴会口上：编号1（灵梦一时兴起的酒宴） / BANQUET_ID=1，对应 Add_Banquet_1_Reimu's Spontaneous Drinking Party.E |
| 121 | `M_KOJO_XXX_EVENT_KX_BANQUET_22` | 特定宴会口上：编号22（湖畔嬉水） / BANQUET_ID=22，对应 Add_Banquet_22_Lakeside Summer Funtime.ERB |
| 142 | `M_KOJO_XXX_EVENT_KX_BANQUET_TYPE_宴会` | 所有CATEGORY为「宴会」的宴会，若没有特定编号口上，则回落到此 / 函数名末段必须与CATEGORY字段值逐字一致（中文），TRYCALLFORM才能命中 |
| 180 | `M_KOJO_XXX_EVENT_KX_BANQUET_TYPE_演唱会` | 类别口上：演唱会 / 所有CATEGORY为「演唱会」的宴会（编号5、11），若没有特定编号口上，则回落到此 |

### M_KOJO_KX_X2_COUNTER系.ERB
*33.8 KB ／ 1210 行 ／ 152 个函数*

| 行号 | 函数名 | 用途 |
|---|---|---|
| 64 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_1` | コミュニケーション 交流 / 距離が近い 离得好近 |
| 69 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_1` | — |
| 79 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_2` | チラ見 偷瞟 |
| 84 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_2` | — |
| 94 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_3` | おはなし 搭话 |
| 99 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_3` | — |
| 109 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_4` | いい匂い 飘来好闻的味道 |
| 114 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_4` | — |
| 124 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_9` | 中だし後 忍受精液的瘙痒 |
| 129 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_9` | — |
| 142 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_11` | ベリーソフト 亲昵 / 近寄ってくる 靠近身侧 |
| 147 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_11` | — |
| 157 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_12` | 笑顔を浮かべる 露出笑容 |
| 162 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_12` | — |
| 172 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_13` | 構って欲しがる 想要被搭理 |
| 177 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_13` | — |
| 187 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_14` | 身をすり寄せる 依偎过来 |
| 192 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_14` | — |
| 202 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_15` | 見つめてくる 凝视 |
| 207 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_15` | — |
| 217 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_16` | 肩にあご乗せ 把下巴搁在你的肩头 |
| 222 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_16` | — |
| 232 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_17` | 差し入れ 犒劳（恢复力气） |
| 237 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_17` | — |
| 250 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_20` | ソフト 软性性骚扰 / 色っぽい仕草 以性感姿势挑逗 |
| 255 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_20` | — |
| 265 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_21` | 見つめる 盯着看（同上，强调让对象（玩家）感受到被盯着） |
| 270 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_21` | — |
| 280 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_22` | 体を摺り寄せる 缠上你的身体 |
| 285 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_22` | — |
| 295 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_23` | スカートめくり 掀起（玩家）的裙子 |
| 300 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_23` | — |
| 310 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_24` | 息を吹きかける 在耳边吹气 |
| 315 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_24` | — |
| 325 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_25` | 尻を撫でる 摸屁股 |
| 330 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_25` | — |
| 340 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_26` | 腕抱き付き 挽着你的胳膊 |
| 345 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_26` | — |
| 354 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_27` | 谷間を見せる 秀出乳沟 |
| 359 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_27` | — |
| 368 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_28` | 尻ズリ 下面有个同名的，这里是※隔着衣物※用（她的）鸡巴蹭（你的）屁股 |
| 373 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_28` | — |
| 386 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_30` | セクハラ 性骚扰 以下开始为诶嘿嘿时触发 / キス 接吻 |
| 391 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_30` | — |
| 401 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_31` | 後ろから抱きつく 从后面抱住 |
| 406 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_31` | — |
| 416 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_32` | 前ろから抱きつく 从前面抱住 |
| 421 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_32` | — |
| 431 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_33` | 胸を揉ませる 揉胸 |
| 436 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_33` | — |
| 446 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_34` | 股間をまさぐる 揉裆 |
| 451 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_34` | — |
| 461 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_35` | スカートの中を見せる 掀起（她的）裙子给你看里面 |
| 466 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_35` | — |
| 476 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_36` | 後ろから胸もみもみ 从身后揉胸 |
| 481 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_36` | — |
| 492 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_39` | 飴強奪 抢走嘴里的糖（亲吻） / 2026年1月24日 4.976修复机制 |
| 497 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_39` | — |
| 510 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_41` | おねだり 央求 / 正常位Ｖおねだり 央求正常位V插入 |
| 515 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_41` | — |
| 525 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_43` | 後背位Ｖ挿入おねだり 央求背后位V插入 |
| 530 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_43` | — |
| 539 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_44` | 後背位Ａおねだり 央求背后位A插入 |
| 544 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_44` | — |
| 557 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_50` | 愛撫 爱抚 / 手淫 |
| 562 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_50` | — |
| 572 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_51` | 口淫 |
| 577 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_51` | — |
| 587 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_52` | 素股 |
| 592 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_52` | — |
| 602 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_53` | パイズリ 乳交 |
| 607 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_53` | — |
| 617 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_54` | 足コキ 足交 |
| 622 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_54` | — |
| 632 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_55` | アナル愛撫 A爱抚 |
| 637 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_55` | — |
| 647 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_56` | アナル舐め 舔菊 |
| 652 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_56` | — |
| 662 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_57` | 指挿入 指插入 |
| 667 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_57` | — |
| 677 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_58` | 胸愛撫 胸爱抚 |
| 682 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_58` | — |
| 692 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_59` | 乳首吸い 吸乳头 |
| 697 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_59` | — |
| 707 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_60` | ディープキス 深吻 |
| 712 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_60` | — |
| 722 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_61` | 誤爆挿入 素股时误插入 |
| 727 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_61` | — |
| 741 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_70` | 奉仕 （让你）侍奉 / クンニ強制 （让你）舔豆 |
| 746 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_70` | — |
| 756 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_71` | フェラチオ強制 （让你）口交 |
| 761 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_71` | — |
| 771 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_72` | アナル奉仕 （让你）舔菊 |
| 776 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_72` | — |
| 786 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_73` | ぱふぱふ 啪敷啪敷（用乳房给你洗脸） |
| 791 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_73` | — |
| 801 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_74` | 乳合わせ （两个女性）磨乳房 |
| 806 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_74` | — |
| 816 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_75` | タワシ洗い 海藻刷（风俗项目，用阴毛为你打泡沫，在游戏里指的夹住手臂用阴部磨蹭） |
| 821 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_75` | — |
| 831 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_76` | 強制アソコ愛撫 （让你）用手爱抚（她的）小穴 |
| 836 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_76` | — |
| 846 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_77` | 乳を吸わせる （让你）吸乳头 |
| 851 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_77` | — |
| 860 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_78` | 尻ズリ （她）用肉棒磨蹭你的臀沟 |
| 865 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_78` | — |
| 878 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_80` | 性交 / 挿入される（MASTER受け） 被正常位V插入（玩家被插入） |
| 883 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_80` | — |
| 893 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_83` | 後背位Ｖ挿入される（MASTER受け） 被背后位V插入（玩家被插入） |
| 898 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_83` | — |
| 907 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_84` | 腰振りＶ受け 摆腰被V插入（玩家被插入） |
| 912 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_84` | — |
| 921 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_85` | 騎乗位Ｖ 女性主导骑乘位V（玩家插入） |
| 926 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_85` | — |
| 936 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_86` | だいしゅきホールド 内射爱的抱抱（高潮时四肢缠住玩家索要内射） |
| 941 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_86` | — |
| 951 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_87` | Ａ挿入する（TARGET受け） 女性主导骑乘位Ａ（玩家插入） |
| 956 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_87` | — |
| 966 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_88` | 腰振りＶ （她主导骑乘位V时）摆腰（玩家插入） |
| 971 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_88` | — |
| 981 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_89` | 腰振りＡ （她主导骑乘位Ａ时）摆腰（玩家插入） |
| 986 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_89` | — |
| 996 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_90` | 後背位Ａ挿入される（MASTER受け） 被背后位Ａ插入（玩家被插入） |
| 1001 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_90` | — |
| 1011 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_91` | イラマチオされる（MASTER受け） 被深喉（玩家被插入） |
| 1016 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_91` | — |
| 1027 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_92` | アナル開発許可を求める 央求开发你的肛门 狂气小白兔表示不考虑实装（SKIP 未编译） |
| 1032 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_92` | —（SKIP 未编译） |
| 1042 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_93` | 腰振り逆Ａ 玩家骑乘位时摆腰（玩家被插入A） |
| 1047 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_93` | — |
| 1056 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_94` | 正常位Ａ挿入される 被正常位Ａ插入（玩家被插入） |
| 1061 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_94` | — |
| 1074 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_120` | 120～139 抱住模式（仅限女生之间触发对方主导） / 頭撫で 摸头 |
| 1079 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_120` | — |
| 1088 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_121` | 髪梳き 梳头 |
| 1093 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_121` | — |
| 1102 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_122` | 抱きつき 投入（玩家）怀抱中 |
| 1107 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_122` | — |
| 1116 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_123` | 抱きしめ 把玩家拥入怀抱 |
| 1121 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_123` | — |
| 1130 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_124` | 頬撫で 摸脸颊 |
| 1135 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_124` | — |
| 1144 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_125` | くすぐり 挠痒 |
| 1149 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_125` | — |
| 1158 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_126` | 膝枕させる 索求玩家的膝枕 |
| 1163 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_126` | — |
| 1172 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_127` | 匂いを嗅ぐ 闻味道 |
| 1177 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_127` | — |
| 1186 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_128` | 話しかける 咬耳朵说悄悄话 |
| 1191 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_128` | — |
| 1200 | `M_KOJO_XXX_MESSAGE_COUNTER_MESSAGECHECK_KX_129` | 首筋舐め 舔脖子 |
| 1205 | `M_KOJO_XXX_MESSAGE_COUNTER_KX_129` | — |

### M_KOJO_KX_X2_CUSTOM_CHECKS.ERB
*11.4 KB ／ 302 行 ／ 9 个函数*

| 行号 | 函数名 | 用途 |
|---|---|---|
| 20 | `M_KOJO_XXX_CHECK_KX_FALL_STATE_OVERRIDE` | 覆写判定 / RETURN=1，以自定义条件覆盖原版条件 =0，自定义条件与原版条件需要同时满足 =-1 禁止转变为该陷落状态 |
| 43 | `M_KOJO_XXX_CHECK_KX_FALL_STATE` | RESULT(S) 存储每个条件的结果及其描述文本 / “/”（斜杠）分割之后的内容会作为悬浮提示（可以通过一些变量调整是否要展示提示） |
| 88 | `M_KOJO_XXX_CHECK_KX_CCOM_ORDER` | ARG是CCOM编号，ARG:1是原始权重 / 返回0表示不改变，-1表示完全禁用 |
| 101 | `M_KOJO_XXX_CHECK_KX_ONABARE_HOLE` | 决定@ONABARE中的自慰是否限制玩弄哪个洞 / 返回0表示使用原版判定，1指定阴道，2指定肛门 |
| 121 | `M_KOJO_XXX_CHECK_KX_OSHITAOSARE` | 概率判定 格式为：1/概率 角色越强势概率越高→分母越小 / RETURN =正值 则返回新的夺主导权概率 若=0或负数 则采用原版的概率机制 |
| 145 | `M_KOJO_XXX_CHECK_KX_JOB` | @ERB\MOVEMENTS\JOB_仕事内容.ERB / REUTRN 1以启用自定义内容 |
| 162 | `M_KOJO_XXX_CHECK_KX_CHARADATA` | 料理部分，请完全遵循CharaData的格式 / 移动部分与CharaData有格式差异，请仔细参考样例 |
| 257 | `M_KOJO_CHECK_KX_COM_BLOCKED` | 0 = 不屏蔽 / 小心使用，不当的屏蔽可能会导致游戏无法继续 |
| 287 | `M_KOJO_XXX_FUNCCHECK_KX_ALCOHOL_TASTE` | RETURNF 0 且 KOJO_FUNCCHECK_OP:0=0 表示不覆写（使用原版值） / 旧修饰值TFLAG:口上特殊補正仍会追加在覆写结果之后 |

### M_KOJO_KX_X2_CUSTOM_EVENTS.ERB
*4.1 KB ／ 100 行 ／ 1 个函数*

| 行号 | 函数名 | 用途 |
|---|---|---|
| 59 | `M_KOJO_EVENT_KX_FAIRY_PRANK` | Add_ACCOMPLICECOUNT = 共犯数量 / Add_SCENARIO       = 当前场景ID（与 SELECTED_PRANK 一致） |

### M_KOJO_KX_X2_EVENTCOM.ERB
*1.3 KB ／ 30 行 ／ 7 个函数*

| 行号 | 函数名 | 用途 |
|---|---|---|
| 3 | `M_KOJO_XXX_EVENT_KX_EVENTCOM` | 看不懂说明不需要使用以下模板，以免造成无法预料的错误 / 在每条指令本体函数@COMXX执行之前触发 |
| 7 | `M_KOJO_XXX_EVENT_KX_EVENTCOMEND_PRI` | 在指令回合结束之后触发，但比其他的 EVENTCOMEND 触发更早执行（高优先级） |
| 11 | `M_KOJO_XXX_EVENT_KX_EVENTCOMEND` | 在指令回合结束之后触发 |
| 16 | `M_KOJO_XXX_EVENT_KX_AFTERTRAIN_BEGIN` | 功能与事件31(@EVENTTRAIN内触发）重叠，但不要求玩家已遇见该角色，必然在@EVENTTRAIN内触发 / 在@AFTERTRAIN之前触发，用于清除后续的标志位等 |
| 20 | `M_KOJO_XXX_EVENT_KX_AFTERTRAIN_END` | 在@AFTERTRAIN相关处理结束时触发 |
| 25 | `M_KOJO_XXX_EVENT_KX_BEFORETRAIN_END` | 功能与@KX_BEFORETRAIN_XXX(@BEFORETRAIN内触发）重叠 / 在@BEFORETRAIN相关处理结束时触发，用于清除@KX_BEFORETRAIN_XXX |
| 29 | `M_KOJO_XXX_EVENT_KX_MONTH_CHANGE` | 当月份变更（新月份开始）时触发 |

### M_KOJO_KX_X2_IMAGE.ERB
*8.0 KB ／ 315 行 ／ 11 个函数*

| 行号 | 函数名 | 用途 |
|---|---|---|
| 13 | `M_KOJO_XXX_IMAGE_KX_特殊服装` | 将特殊服装存入RESULTS / 格式为 %服装%%特殊服装% 请适当加入"_"等分隔符（SKIP 未编译） |
| 62 | `M_KOJO_XXX_IMAGE_KX_体形` | 格式为 %体型%%服装% 请适当加入"_"等分隔符 / "巨乳"已在游戏中实现，可通过 %体型%巨乳%服装% 追加（SKIP 未编译） |
| 90 | `M_KOJO_XXX_IMAGE_KX_特殊表情` | 将鼠标悬停时的表情存入RESULTS:1 / "通常","笑顔","怒り","発情","睡眠"已在游戏中实现（SKIP 未编译） |
| 116 | `M_KOJO_XXX_IMAGE_KX_特殊表情COM` | 将鼠标悬停时的表情存入RESULTS:1 / "自慰","爱抚","性交"已在游戏中实现（SKIP 未编译） |
| 143 | `M_KOJO_XXX_IMAGE_KX_差分` | 将差分存入RESULTS / 格式为 {CHARA}%差分% 请适当加入"_"等分隔符（SKIP 未编译） |
| 169 | `M_KOJO_XXX_IMAGE_KX_特殊照れ` | 格式为 %特殊害羞%害羞 / "裸"已在游戏中实现，可通过 %特殊害羞%裸害羞 追加（SKIP 未编译） |
| 195 | `M_KOJO_XXX_IMAGE_KX_特殊吐息` | 格式为 %特殊喘息%喘息 / "裸"已在游戏中实现，可通过 %特殊喘息%裸喘息 追加（SKIP 未编译） |
| 221 | `M_KOJO_XXX_IMAGE_KX_特殊汗` | 格式为 %特殊汗液%汗 / "裸"已在游戏中实现，可通过 %特殊汗液%裸汗 追加（SKIP 未编译） |
| 245 | `M_KOJO_XXX_IMAGE_KX_特殊エフェクトチェック` | 判断参数"特效"是否包含固有特效 / 请按示例使用STRFIND（SKIP 未编译） |
| 265 | `M_KOJO_XXX_IMAGE_KX_特殊エフェクト` | 将特殊特效存入RESULTS数组 / 通过RETURN返回追加的特效数量（SKIP 未编译） |
| 293 | `M_KOJO_XXX_IMAGE_KX_自慰エフェクト` | 将自慰特效存入RESULTS数组 / 通过RETURN返回追加的特效数量（SKIP 未编译） |

### M_KOJO_KX_X2_MARRIAGE.ERB
*8.4 KB ／ 261 行 ／ 7 个函数*

| 行号 | 函数名 | 用途 |
|---|---|---|
| 22 | `M_KOJO_XXX_SUCCESS_CUSTOM_COM_KX_13` | 设置TFLAG:192为1则求婚成功，为0则失败 / 若不写此函数，则使用默认的求婚成功判定 |
| 32 | `M_KOJO_XXX_MESSAGE_CUSTOM_COM_KX_13` | COM13（求婚）的剧本 / TFLAG:193 == 0 时为求婚失败，否则为求婚成功 |
| 55 | `M_KOJO_XXX_EVENT_KX_WEDDING_PREPARATIONS` | "DATE"   — 决定婚礼日期时 / "GUESTS" — 确认宾客名单时 |
| 82 | `M_KOJO_XXX_EVENT_KX_CUSTOM_WEDDING` | 注意：入栈必须带"来源 + 场景参数"（婚宴固定用 31），与出栈一一配对； / TCVAR:DRESSED_FOR_BANQUET 标记已废弃，不要再写 |
| 114 | `M_KOJO_XXX_EVENT_KX_WEDDING` | 不使用 MESSAGECHECK 时，本函数只写新娘的文本， / 司仪 SPTALK 誓词问答、INPUT 提示由系统通用文本负责（交互式调用） |
| 234 | `M_KOJO_XXX_CHECK_KX_CUSTOM_WEDDING` | "COST"	 — 返回自定义婚礼的费用（RESULT） / "LOCATION" — 返回自定义婚礼的场地编号（RESULT） |
| 255 | `M_KOJO_XXX_CHECK_KX_WEDDING_GUESTS` | 按优先级排列，前面的宾客优先入席 / 最多支持到RESULT:19（20位宾客） |

### M_KOJO_KX_X2_New_Api.ERB
*10.4 KB ／ 315 行 ／ 16 个函数*

| 行号 | 函数名 | 用途 |
|---|---|---|
| 25 | `M_KOJO_XXX_SUCCESS_KX_PRI_GENERAL` | 返回值[1]:	HACK钩子，用于屏蔽并重新钩回SELECTCOM / 备　注:在独立指令判定前进行全局拦截。非常适合处理诸如“睡眠/时停等特定状态下一律大成功/大失败”、“多条同（SKIP 未编译） |
| 77 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_PRI_GENERAL_KX` | 3 = 屏蔽情景文本，屏蔽口上文本（完全静音跳过） / 备　注:用于多条指令共用一套判定逻辑的情况（SKIP 未编译） |
| 122 | `M_KOJO_XXX_EXTRASOURCE_COM_KX_PRI_GENERAL` | 1 = 覆盖模式（执行完此函数后，拦截跳过该指令专属的 EXTRASOURCE 及其兜底） / 备　注:用于全局状态下的参数干涉。由于分为 COM(常规) 和 SCOM(派生)，若（SKIP 未编译） |
| 159 | `KOJO_XXX_CUSTOM_BUTTON_CONDITION_KX_Y` | 如果RETURN 1，按钮就会显示（SKIP 未编译） |
| 166 | `KOJO_XXX_CUSTOM_BUTTON_KX_Y` | 如果按钮被点击（SKIP 未编译） |
| 178 | `KOJO_XXX_CUSTOM_TALENT_SET_KX` | —（SKIP 未编译） |
| 198 | `KOJO_XXX_COM_NAME_KX_Y` | 指令名（SKIP 未编译） |
| 204 | `KOJO_XXX_COM_ABLE_KX_Y` | 指令使用条件，与通常的@COM_ABLE函数相同，如果RETURN 1则指令显示为可执行（SKIP 未编译） |
| 211 | `KOJO_XXX_COM_KX_Y` | 指令执行内容。描述经验值和参数的增减，与通常的@COM函数相同 / RETURN 1=执行指令 / RETURN 0=指令失败了（函数意义：跳过@SOURCE_CHECK的SOUR（SKIP 未编译） |
| 218 | `M_KOJO_XXX_MESSAGE_COM_KX_W` | 指令消息。描述指令的情景文本， / W的值是(270 + Y)。SELECTCOM/PREVCOM会代入此值（SKIP 未编译） |
| 254 | `M_KOJO_XXX_OVERRIDE_COM_KX_Y` | —（SKIP 未编译） |
| 260 | `M_KOJO_XXX_OVERRIDE_SCOM_KX_Y` | —（SKIP 未编译） |
| 271 | `M_KOJO_XXX_OVERRIDE_COM_KX_PRI_GENERAL` | 如果想针对某类指令统一转发、覆写逻辑，可以在这里拦截（SKIP 未编译） |
| 284 | `M_KOJO_XXX_OVERRIDE_SCOM_KX_PRI_GENERAL` | —（SKIP 未编译） |
| 303 | `KOJO_XXX_VERSION_KX` | —（SKIP 未编译） |
| 310 | `KOJO_XXX_VERSION_UPDATE_KX` | 当存档的CFLAG:kojo_version小于KOJO_XXX_VERSION_KX时加载更新（SKIP 未编译） |

### M_KOJO_KX_X2_事件系.ERB
*142.2 KB ／ 4242 行 ／ 72 个函数*

| 行号 | 函数名 | 用途 |
|---|---|---|
| 31 | `M_KOJO_KX_X` | 对于别人版，将函数名中的X替换成一个未被占用的编号即可 / 对于初期版，请直接删去 _X |
| 59 | `M_KOJO_XXX_FLAGSETTING_KX` | 若不想在代码上纠结太多，也可以不作什么改动 / 此处的角色变量※不能※省去编号，所以请将下方的所有X替换为角色编号并取消注释 |
| 109 | `M_KOJO_XXX_COLOR_KX` | 口上色的设置 / 玩家在设置里启用口上色设定后才能显示 |
| 121 | `M_KOJO_XXX_UPDATE_KX` | 用于升级存档时更新数据 / 如果不知道用法，说明没有使用此函数的需要（SKIP 未编译） |
| 133 | `KOJO_XXX_OPTION_EXIST_KX` | 此系统设计的目的，是为了加快版本更新的速度。把与版本更新无关的剧本侧选项拆分出来，不必每次升级都出现，而且可以不通过手动更新UPDATE来访问剧本选项。 / 选项存在性函数，该函数（SKIP 未编译） |
| 141 | `KOJO_XXX_OPTION_KX` | 如何使用打印按钮函数，请参考ERB\fromEN\NEW_UPDATE\笔记 for KOJO_OPTION.txt中的笔记、以及UPDATE_MAIN.ERB中的函数注释、不足之（SKIP 未编译） |
| 190 | `M_KOJO_XXX_ENCOUNTER_KX` | 可以在此处调用OPTION进行素质修改等，但在这之前查看角色信息仍然会显示更改前的，玩家在那里也能点击剧本选项 / 如果有无需确定、在切换到该剧本后立即改变的角色信息，请写到FLA |
| 208 | `KX_BEFORETRAIN_XXX` | 因为顺序在来访判断之前，可以通过设置 CFLAG:次日访问 = 1 强制角色来访 / 能做的事情很多，但请设置好条件 |
| 221 | `M_KOJO_XXX_SPEVENT_MESSAGECHECK_KX_Y` | —（SKIP 未编译） |
| 236 | `M_KOJO_XXX_SPEVENT_KX_1` | TCVAR:中止接吻 = 1 / ERB\イベント関連\DATE_CMN.ERB |
| 250 | `M_KOJO_XXX_SPEVENT_KX_2` | SETBIT CFLAG:约会后事件标志, 1 / ERB\イベント関連\DATE_CMN.ERB |
| 282 | `M_KOJO_XXX_SPEVENT_KX_3` | 约会回家 / ERB\イベント関連\DATE_CMN.ERB |
| 325 | `M_KOJO_XXX_SPEVENT_KX_4` | 参见ERB\fromEN\DAYEVENT.ERB / 早晨 H 事件（诶嘿嘿） |
| 386 | `M_KOJO_XXX_SPEVENT_KX_5` | 早安的非H事件 |
| 446 | `M_KOJO_XXX_SPEVENT_KX_6` | 入睡时的H事件（诶嘿嘿） |
| 496 | `M_KOJO_XXX_SPEVENT_KX_7` | 入睡后的非H事件 |
| 536 | `M_KOJO_XXX_CHECK_KX_DAYEVENT_COND` | DE系统的CHECKS系控制接口 / 用于控制该角色是否允许触发特定事件，以及覆盖系统的默认条件 |
| 659 | `M_KOJO_XXX_EVENT_KX_1` | 与角色相遇 / ERB\イベント関連\情事発覚.ERB |
| 765 | `M_KOJO_XXX_EVENT_KX_2` | ERB\イベント関連\BEFORETRAIN.ERB (ARG == 1, 2, 3 的情况) / ERB\MOVEMENTS\SLEEP.ERB (ARG == 4 的情况) |
| 831 | `M_KOJO_XXX_EVENT_KX_3` | ERB\イベント関連\EVENTCOMEND.ERB（ARG == 6 的情况） / ERB\MOVEMENTS\MOVEMENTS.ERB（ARG == 7, ARG:1 ==  |
| 1032 | `M_KOJO_XXX_EVENT_KX_4` | 移动中经过角色 / ERB\コマンド関連\COMF\日常系\COMF400 移動.ERB |
| 1065 | `M_KOJO_XXX_EVENT_KX_5` | 不够亲密的其他角色进入时，气氛变得尴尬了（不能进行某些亲密举动了） / ERB\ステータス表示関連\INFO.ERB |
| 1098 | `M_KOJO_XXX_EVENT_KX_6` | 目击了MASTER与其他人的情事 / ERB\イベント関連\情事発覚.ERB |
| 1198 | `M_KOJO_XXX_EVENT_KX_7` | 与MASTER的情事被其他角色撞破 / ERB\イベント関連\情事発覚.ERB |
| 1302 | `M_KOJO_XXX_EVENT_KX_8` | 满足条件之后，下次见到角色时触发 / ERB\イベント関連\情事発覚.ERB |
| 1330 | `M_KOJO_XXX_EVENT_KX_9` | 没有什么有效的应对方法，但其实也没有什么干预的必要 / ERB\イベント関連\ボッシュート.ERB |
| 1362 | `M_KOJO_XXX_EVENT_KX_10` | ERB\ステータス計算関連\SOURCE\SOURCE.ERB （ARG == 2 && ARG:1 == 1的情况） / ERB\イベント関連\情事発覚.ERB （ARG ==  |
| 1494 | `M_KOJO_XXX_EVENT_KX_11` | 关于催眠检测，请见上文提及处 / ERB\コマンド関連\COMF\日常系\COMF400 移動.ERB |
| 1522 | `M_KOJO_XXX_EVENT_KX_12` | 潜入卧室 / ERB\コマンド関連\COMF\日常系\侵入.ERB |
| 1598 | `M_KOJO_XXX_EVENT_KX_13` | 宴会的准备和善后无口上接口 / ERB\MOVEMENTS\JOB_仕事開始終了処理.ERB |
| 1631 | `M_KOJO_XXX_EVENT_KX_14` | 食事系 / ERB\イベント関連\ボッシュート.ERB |
| 1658 | `M_KOJO_XXX_EVENT_KX_15` | ERB\コマンド関連\USERCOM.ERB（ARG == 2的情况） / ERB\イベント関連\AFTER_AFFAIR.ERB（ARG == 3的情况） |
| 1724 | `M_KOJO_XXX_EVENT_KX_16` | 陪睡 / ERB\コマンド関連\USERCOM.ERB |
| 1749 | `M_KOJO_XXX_EVENT_KX_17` | 时间停止终了时 / ERB\時間停止解除.ERB |
| 2027 | `M_KOJO_XXX_EVENT_KX_18` | ERB\イベント関連\妊娠関連\HININSHITE.ERB（ARG == 1 的情况） / ERB\イベント関連\妊娠関連\OGAMITAOSHI.ERB（ARG == 2, 3 |
| 2070 | `M_KOJO_XXX_EVENT_KX_19` | ERB\イベント関連\APPEND_SYS.ERB（ARG == 1, 2 的情况） / ERB\SHOP関連\SHOP_住環境設定.ERB（ARG == 3 的情况） |
| 2107 | `M_KOJO_XXX_EVENT_KX_20` | ERB\MOVEMENTS\SLEEP.ERB / ERB\イベント関連\デート終了タイムアップ処理.ERB（只有一条，其实只是用于应对极端情况的） |
| 2230 | `M_KOJO_XXX_EVENT_KX_21` | 陷落素质（与部分性素质）取得时 / ERB\イベント関連\EVENTTURNEND.ERB |
| 2320 | `M_KOJO_XXX_EVENT_KX_22` | 所以在相同的情况下，可能触发的ARG数值也会有多个，需要注意 / ERB\イベント関連\AFTERTRA.ERB |
| 2394 | `M_KOJO_XXX_EVENT_KX_23` | 关于催眠检测，请见上文提及处 / ERB\コマンド関連\COMF\日常系\COMF400 移動.ERB |
| 2420 | `M_KOJO_XXX_EVENT_KX_24` | 在获得[妊娠]，即受精开始之后20日之后触发 / ERB\イベント関連\妊娠関連\PREGNANCY.ERB |
| 2457 | `M_KOJO_XXX_EVENT_KX_25` | 出产 / ERB\イベント関連\妊娠関連\BIRTH.ERB |
| 2501 | `M_KOJO_XXX_EVENT_KX_26_1` | 被发现自慰时的自定义判定函数 / RETURN -1 强制失败，RETURN 1 强制成功 |
| 2522 | `M_KOJO_XXX_EVENT_KX_ONABARE_1` | RETURN 2 表示开启地文，RETURN 其他值则关闭地文 / ARG表示自慰部位，0 = V自慰，1 = A自慰 |
| 2534 | `M_KOJO_XXX_EVENT_KX_ONABARE_2` | RETURN 2 表示开启地文，RETURN 其他值则关闭地文 / ARG表示自慰部位，0 = V自慰，1 = A自慰 |
| 2547 | `M_KOJO_XXX_EVENT_KX_ONABARE_3` | 如果想要用这四个参数的话，请直接把口上写在这里，因为调用主函数的时候这些参数是不可用的 / 当MASTER为女性时，根本无法选择该选项，更不会触发此函数，所以可以放心写肉棒 |
| 2561 | `M_KOJO_XXX_EVENT_KX_26` | 这个是主函数哦 |
| 2629 | `M_KOJO_XXX_EVENT_KX_27` | 邀请去房间、单纯约会需要角色拥有恋慕，而邀请去宴会则思慕和恋慕均可 / ERB\イベント関連\情事発覚.ERB |
| 2711 | `M_KOJO_XXX_EVENT_KX_28` | 脱衣口上 / ERB\コマンド関連\USERCOM_服を脱がせる.ERB |
| 2791 | `M_KOJO_XXX_EVENT_KX_29` | 角色愤怒值满，进入怒/泣状态 / ERB\イベント関連\EVENTCOMEND.ERB |
| 2818 | `M_KOJO_XXX_EVENT_KX_30` | ERB\イベント関連\EVENTCOMEND2.ERB / ARG == 1 或 2 的情况由函数 @被逆推終了 管理，路径为 ERB\コマンド関連\COMF\COMF850 抜け |
| 2866 | `M_KOJO_XXX_EVENT_KX_31` | 差分参考使用：CFLAG:オナバレ（被发现自慰，会显示「TARGET把脸埋在了枕头里面」） / ERB\イベント関連\AFTERTRA.ERB |
| 2899 | `M_KOJO_XXX_EVENT_KX_32` | 连锁行动：与正在自由行动的角色相性大于100的另一名角色可能会加入该行动（做差分可以考虑这个） / ERB\MOVEMENTS\自由行動\MOVEMENT_自由行動.ERB |
| 3342 | `M_KOJO_XXX_EVENT_KX_33` | 跨年的瞬间与TARGET在同一地点时触发 / ERB\ステータス表示関連\INFO.ERB |
| 3358 | `M_KOJO_XXX_EVENT_KX_34` | ERB\ステータス計算関連\TRACHECK_ABLUP.ERB / ERB\イベント関連\EVENTTURNEND.ERB（获得[乐器知识]和[相对音感]） |
| 3614 | `M_KOJO_XXX_DAILY_EVENT_MESSAGECHECK_KX_2` | TARGET　欲情之珠＋1000 / ERB\イベント関連\デイリーイベント\DAIRY_EV2.ERB |
| 3628 | `M_KOJO_XXX_DAILY_EVENT_KX_2` | — |
| 3646 | `M_KOJO_XXX_DAILY_EVENT_MESSAGECHECK_KX_4` | TARGET決定明天去見MASTER / ERB\イベント関連\デイリーイベント\DAIRY_EV4 MONOOMOI.ERB |
| 3658 | `M_KOJO_XXX_DAILY_EVENT_KX_4` | — |
| 3678 | `M_KOJO_XXX_DAILY_EVENT_MESSAGECHECK_KX_12` | TARGET表示遺憾 / ERB\イベント関連\デイリーイベント\DAIRY_EV12 特訓.ERB |
| 3690 | `M_KOJO_XXX_DAILY_EVENT_KX_12` | — |
| 3764 | `M_KOJO_XXX_EVENT_KX_GIFT` | STRCOUNT(礼物的属性, 需要检定的属性)：寻找礼物中指定属性的强度（出现次数） / ERB\イベント関連\贈り物関連\贈り物.ERB |
| 3821 | `M_KOJO_XXX_MESSAGE_COM_KX_MUSHI_BATTLE` | ERB\コマンド関連\COMF\日常系\COMF483 ムシバトル.ERB / ERB\コマンド関連\COMF\日常系\MUSHI_BATTLE.ERB |
| 3934 | `M_KOJO_XXX_MESSAGE_COM_KX_SUIKA` | 当AIM与西瓜重合时打下，便是大成功；若AIM与西瓜距离为1时打下，便是成功，否则为失败（扫帚可以多打一次） / 参加的角色会随机成为「诚实者」或「说谎者」，「诚实者」永远说真话， |
| 4072 | `KOJO_XXX_SF_CONTRACT_EVENT_KX` | 炮友契约相关 / ERB\コマンド関連\COMF\日常系\COMF357 セフレ契約.ERB |
| 4108 | `KX_XXX_ROOM_DESCRIPTION` | 对角色私室的描写 / ERB\ANOTHER_TALK.ERB |
| 4127 | `M_KOJO_XXX_EVENT_KX_LOST_VIRGIN_STOP` | ERB\ステータス計算関連\TRACHECK_LOST_VIRGIN.ERB / 在所有插入指令之前均有调用 |
| 4144 | `M_KOJO_XXX_EVENT_KX_PERMISSION_1` | 若因为该函数导致推倒强制失败/成功，TCVAR:初次拥抱 会被设置为98/99，可以在推倒指令的地方检测 / ERB\コマンド関連\COMF\日常系\COMF350 押し倒す.ER |
| 4160 | `M_KOJO_XXX_EVENT_KX_PERMISSION_2` | 该函数并非在推倒判定之初调用，所以若在里面写了口上，由于情绪不足等原因推倒失败时并不会显示 / ERB\コマンド関連\COMF\日常系\COMF350 押し倒す.ERB |
| 4175 | `RUN_INTO_XXX_EVENT_KX` | 这一块的本体代码现在有bug，基本上触发不了 / ERB\イベント関連\お出かけイベント\お出かけイベント.ERB |
| 4208 | `M_KOJO_XXX_CHECK_KX_IRAI_BLOCKED` | 18 - 有谁能帮我做一下吗！ / ERB\コマンド関連\COMF\依頼\CTRL_IRAI.ERB |
| 4228 | `M_KOJO_XXX_EVENT_KX_GRAVITY` | 请注意严格设置条件，否则可能造成角色长期被定在同一个地点 / ERB\MOVEMENTS\MOVEMENT_キャラ移動処理.ERB |

### M_KOJO_KX_X2_侍奉系指令.ERB
*8.3 KB ／ 385 行 ／ 11 个函数*

| 行号 | 函数名 | 用途 |
|---|---|---|
| 12 | `M_KOJO_XXX_SUCCESS_COM_KX_XX` | 指令成否判定 / 剧本侧覆写式接管指令的结果的规则，以TFLAG:192返回成否鉴定值。0表示剧本侧不干涉COM本体设定，其余值的定义具体参照COMXX。（SKIP 未编译） |
| 17 | `M_KOJO_XXX_EXTRASOURCE_COM_KX_XX` | —（SKIP 未编译） |
| 22 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_XX` | 做任何事（SKIP 未编译） |
| 27 | `M_KOJO_XXX_MESSAGE_COM_KX_XX` | —（SKIP 未编译） |
| 83 | `M_KOJO_XXX_MESSAGE_COM_KX_80` | 80,手淫 / 说明：角色用手为玩家手淫。关键差分：时奸中、初次、射精时、通常陷落嵌套。 |
| 129 | `M_KOJO_XXX_MESSAGE_COM_KX_81` | 拔出追加分支：TCVAR:MASTER:112 == 8时，角色先在体内射精后拔出再口交。 / 具体分支可参考@MESSAGE_COM81中TCVAR:MASTER:112的各个取 |
| 177 | `M_KOJO_XXX_MESSAGE_COM_KX_82` | 说明：角色用乳房为玩家乳交。关键差分：时奸中、初次、射精时、胸围尺寸差分、通常陷落嵌套。 / 胸部尺寸相关：TALENT:胸围决定胸部大小（-2绝壁/-1贫乳/0普通/1巨乳/2爆 |
| 221 | `M_KOJO_XXX_MESSAGE_COM_KX_83` | 说明：角色用大腿为玩家素股。关键差分：时奸中、初次、射精时、通常陷落嵌套。 / 素股是用大腿夹住阴茎摩擦的侍奉行为。 |
| 265 | `M_KOJO_XXX_MESSAGE_COM_KX_84` | 说明：角色用涂满泡沫的身体为玩家提供泡泡浴服务。此指令较为特殊，通常不在时奸场景中使用，因此省略时奸判定分支。 / 关键差分：初次、射精时、通常陷落嵌套。 |
| 304 | `M_KOJO_XXX_MESSAGE_COM_KX_85` | 85,足交 / 说明：角色用足部为玩家足交。关键差分：时奸中、初次、射精时、通常陷落嵌套。 |
| 348 | `M_KOJO_XXX_MESSAGE_COM_KX_88` | 说明：角色用嘴进行真空吸引式口交。关键差分：时奸中、初次、射精时、通常陷落嵌套。 / 真空口交比普通口交更具刺激性，可在台词中体现吸引感和窒息感。 |

### M_KOJO_KX_X2_依頼.ERB
*68.6 KB ／ 2093 行 ／ 21 个函数*

| 行号 | 函数名 | 用途 |
|---|---|---|
| 13 | `M_KOJO_XXX_IRAI_KX` | 依赖口上・所有依赖的共通口上 / 以下依赖改称委托 |
| 201 | `M_KOJO_XXX_IRAI_1_KX` | 内容：帮助TARGET打扫房间 / 发生率是10，发生条件是需要MASTER和TARGET住在同一个地区。 |
| 281 | `M_KOJO_XXX_IRAI_2_KX` | （TARGET可以是委托人，也可以与委托无关，请自行分辨） / 发生率是15，发生条件是需要MASTER和委托人住在同一个地区，能够去委托人的房间并且亲密 >= 2。 |
| 366 | `M_KOJO_XXX_IRAI_3_KX` | 内容：和TARGET一起玩 / 发生率是15，发生条件是TARGET持有 TALENT:幼稚 |
| 428 | `M_KOJO_XXX_IRAI_4_KX` | 内容：指导TARGET练习料理 / 发生率是10，发生条件是 TARGET的料理技能 < MASTER的料理技能，并且 MASTER的料理技能 >=2，以及 TARGET的亲密 > |
| 495 | `M_KOJO_XXX_IRAI_5_KX` | 内容：帮TARGET做弹幕特训 / 发生率是10，发生条件是：TARGET的战斗能力 <= MASTER的战斗能力，且 TARGET亲密 >= 2，以及主地图不能在人间之里 |
| 562 | `M_KOJO_XXX_IRAI_6_KX` | （TARGET可以是委托人，也可以是与委托无关的角色，请自行分辨） / 发生率是10，发生条件是 TARGET的教养 <= MASTER的教养 |
| 690 | `M_KOJO_XXX_IRAI_7_KX` | 发生率是80，发生条件是需要MASTER和TARGET住在同一个地区，在冬之月的15~31号之间，和 TARGET的亲密 >= 3 / 在过了冬之月31号，也就是新年的时候这个委托 |
| 773 | `M_KOJO_XXX_IRAI_8_KX` | （需要写在比 系统的 BEFORETRAIN 要早，在每次读档后又不会被本体愚蠢的 SETUP_ALL_LETTERS 覆盖掉的地方，推荐 FLAGSETTINGS） / （FRO |
| 851 | `M_KOJO_XXX_IRAI_9_KX` | （TARGET可以是委托人，也可以是失主，请自行分辨） / 发生率是1，发生条件是 TARGET的信赖度 >= 30 |
| 928 | `M_KOJO_XXX_IRAI_10_KX` | （TARGET可以是委托人，也可以是与委托无关的角色，请自行分辨） / 发生率是3，发生条件是 TARGET的信赖度 >= 30 |
| 1021 | `M_KOJO_XXX_IRAI_11_KX` | （TARGET可以是委托人，也可以是目标角色，请自行分辨） / 发生率是3，发生条件是 TARGET的信赖度 >= 30 |
| 1100 | `M_KOJO_XXX_IRAI_12_KX` | （TARGET可以是委托人，也可以是目标角色，请自行分辨） / 发生率是2，发生条件是 委托人的战斗能力 >= 1 |
| 1240 | `M_KOJO_XXX_IRAI_13_KX` | 内容：提供美味的鱼 / 发生率是3，发生条件是TARGET不讨厌鱼料理 |
| 1305 | `M_KOJO_XXX_IRAI_14_KX` | 内容：提供5块木材给TARGET / 在冬之月发生率是10，其他季节发生率是3，没有发生条件 |
| 1373 | `M_KOJO_XXX_IRAI_15_KX` | 因为无视TARGET是否是 处女 或者 无知，会夺取初吻，会破瓜，中途不会调用任何口上，并且最后统一都是内射， / 所以这里再提（luo）醒（suo）一遍：想要阻止委托出现的话，请 |
| 1440 | `M_KOJO_XXX_IRAI_16_KX` | 发生率是5，发生条件是 MASTER的话术等级 >= 1 / 这个委托建议先看完整体的机制再写【传送门16】 |
| 1696 | `M_KOJO_XXX_IRAI_17_KX` | 内容：凭借TARGET模糊的记忆做出并送上料理 / 发生率是5，发生条件是 TARGET不是 阿求（毕竟阿求不会忘嘛） |
| 1846 | `M_KOJO_XXX_IRAI_18_KX` | 内容：将TARGET点的菜肴送到 / 发生率是5，无发生条件 |
| 1997 | `M_KOJO_XXX_IRAI_依頼名_KX` | 请在“依頼名”部分填写对应委托的名字 / 因为在通用模板那里对具体委托调用的时候，是直接用的 M_KOJO_XXX_IRAI_%IRAI_NAME%_KX 的格式 |
| 2049 | `M_KOJO_XXX_IRAI_Y_KX` | 依赖口上模板，想加新的口上复制这个就是了 / 一般依赖Y：（SKIP 未编译） |

### M_KOJO_KX_X2_其他系指令.ERB
*24.9 KB ／ 1407 行 ／ 30 个函数*

| 行号 | 函数名 | 用途 |
|---|---|---|
| 40 | `M_KOJO_XXX_SUCCESS_COM_KX_XX` | —（SKIP 未编译） |
| 45 | `M_KOJO_XXX_EXTRASOURCE_COM_KX_XX` | —（SKIP 未编译） |
| 49 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_XX` | —（SKIP 未编译） |
| 71 | `M_KOJO_XXX_MESSAGE_COM_KX_96` | LOCALSSIZE 1 / RETURN 0 |
| 118 | `M_KOJO_XXX_MESSAGE_COM_KX_90` | LOCALSSIZE 1 / RETURN 0 |
| 159 | `M_KOJO_XXX_MESSAGE_COM_KX_91` | LOCALSSIZE 1 / RETURN 0 |
| 200 | `M_KOJO_XXX_MESSAGE_COM_KX_92` | LOCALSSIZE 1 / RETURN 0 |
| 263 | `M_KOJO_XXX_MESSAGE_COM_KX_93` | LOCALSSIZE 1 / RETURN 0 |
| 326 | `M_KOJO_XXX_MESSAGE_COM_KX_94` | LOCALSSIZE 1 / RETURN 0 |
| 395 | `M_KOJO_XXX_MESSAGE_COM_KX_120` | LOCALSSIZE 1 / RETURN 0 |
| 436 | `M_KOJO_XXX_MESSAGE_COM_KX_121` | LOCALSSIZE 1 / RETURN 0 |
| 477 | `M_KOJO_XXX_MESSAGE_COM_KX_123` | LOCALSSIZE 1 / RETURN 0 |
| 518 | `M_KOJO_XXX_MESSAGE_COM_KX_124` | LOCALSSIZE 1 / RETURN 0 |
| 559 | `M_KOJO_XXX_MESSAGE_COM_KX_125` | LOCALSSIZE 1 / RETURN 0 |
| 600 | `M_KOJO_XXX_MESSAGE_COM_KX_126` | LOCALSSIZE 1 / RETURN 0 |
| 641 | `M_KOJO_XXX_MESSAGE_COM_KX_127` | LOCALSSIZE 1 / RETURN 0 |
| 688 | `M_KOJO_XXX_MESSAGE_COM_KX_130` | LOCALSSIZE 1 / RETURN 0 |
| 751 | `M_KOJO_XXX_MESSAGE_COM_KX_131` | LOCALSSIZE 1 / RETURN 0 |
| 814 | `M_KOJO_XXX_MESSAGE_COM_KX_132` | LOCALSSIZE 1 / RETURN 0 |
| 877 | `M_KOJO_XXX_MESSAGE_COM_KX_133` | LOCALSSIZE 1 / RETURN 0 |
| 946 | `M_KOJO_XXX_MESSAGE_COM_KX_180` | LOCALSSIZE 1 / RETURN 0 |
| 987 | `M_KOJO_XXX_MESSAGE_COM_KX_181` | LOCALSSIZE 1 / RETURN 0 |
| 1028 | `M_KOJO_XXX_MESSAGE_COM_KX_182` | LOCALSSIZE 1 / RETURN 0 |
| 1069 | `M_KOJO_XXX_MESSAGE_COM_KX_183` | LOCALSSIZE 1 / RETURN 0 |
| 1111 | `M_KOJO_XXX_MESSAGE_COM_KX_184` | LOCALSSIZE 1 / RETURN 0 |
| 1167 | `M_KOJO_XXX_MESSAGE_COM_KX_186` | LOCALSSIZE 1 / RETURN 0 |
| 1209 | `M_KOJO_XXX_MESSAGE_COM_KX_188` | LOCALSSIZE 1 / RETURN 0 |
| 1265 | `M_KOJO_XXX_MESSAGE_COM_KX_189` | LOCALSSIZE 1 / RETURN 0 |
| 1307 | `M_KOJO_XXX_MESSAGE_COM_KX_191` | LOCALSSIZE 1 / RETURN 0 |
| 1348 | `M_KOJO_XXX_MESSAGE_COM_KX_192` | LOCALSSIZE 1 / RETURN 0 |

### M_KOJO_KX_X2_刻印取得.ERB
*2.1 KB ／ 79 行 ／ 2 个函数*

| 行号 | 函数名 | 用途 |
|---|---|---|
| 6 | `M_KOJO_XXX_MESSAGE_MARKCNG_MESSAGECHECK_KX` | 刻印取得 |
| 9 | `M_KOJO_XXX_MESSAGE_MARKCNG_KX` | — |

### M_KOJO_KX_X2_弾幕勝負.ERB
*8.1 KB ／ 197 行 ／ 1 个函数*

| 行号 | 函数名 | 用途 |
|---|---|---|
| 40 | `M_KOJO_XXX_MESSAGE_COM_KX_DANMAKU` | 决斗结束	      ④ 宣布败犬/人生的胜利者，处理乐谱 / 决斗后		⑤ **调用 "戦闘後" 的口上内容**， 进行各种决斗后的数据处理 |

### M_KOJO_KX_X2_性交系指令.ERB
*24.2 KB ／ 1235 行 ／ 20 个函数*

| 行号 | 函数名 | 用途 |
|---|---|---|
| 54 | `M_KOJO_XXX_SUCCESS_COM_KX_XX` | TFLAG:192 = -1 强制失败 / TFLAG:192 = -2 指令中止（SKIP 未编译） |
| 61 | `M_KOJO_XXX_EXTRASOURCE_COM_KX_XX` | 数值计算控制函数 / 提供对COM设计的各类数值进行改动的时点。与COMXX一致，可以做到任何事。（SKIP 未编译） |
| 67 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_XX` | 文本控制函数 / 控制是否需要略过通用情景描写和/或剧本台词（SKIP 未编译） |
| 115 | `M_KOJO_XXX_MESSAGE_COM_KX_60` | LOCALSSIZE 1 / RETURN 0 |
| 209 | `M_KOJO_XXX_MESSAGE_COM_KX_61` | LOCALSSIZE 1 / RETURN 0 |
| 302 | `M_KOJO_XXX_MESSAGE_COM_KX_62` | LOCALSSIZE 1 / RETURN 0 |
| 390 | `M_KOJO_XXX_MESSAGE_COM_KX_63` | LOCALSSIZE 1 / RETURN 0 |
| 479 | `M_KOJO_XXX_MESSAGE_COM_KX_64` | LOCALSSIZE 1 / RETURN 0 |
| 536 | `M_KOJO_XXX_MESSAGE_COM_KX_65` | LOCALSSIZE 1 / RETURN 0 |
| 599 | `M_KOJO_XXX_MESSAGE_COM_KX_66` | LOCALSSIZE 1 / RETURN 0 |
| 662 | `M_KOJO_XXX_MESSAGE_COM_KX_67` | LOCALSSIZE 1 / RETURN 0 |
| 725 | `M_KOJO_XXX_MESSAGE_COM_KX_68` | LOCALSSIZE 1 / RETURN 0 |
| 788 | `M_KOJO_XXX_MESSAGE_COM_KX_69` | LOCALSSIZE 1 / RETURN 0 |
| 851 | `M_KOJO_XXX_MESSAGE_COM_KX_70` | LOCALSSIZE 1 / RETURN 0 |
| 915 | `M_KOJO_XXX_MESSAGE_COM_KX_71` | LOCALSSIZE 1 / RETURN 0 |
| 967 | `M_KOJO_XXX_MESSAGE_COM_KX_72` | LOCALSSIZE 1 / RETURN 0 |
| 1023 | `M_KOJO_XXX_MESSAGE_COM_KX_73` | LOCALSSIZE 1 / RETURN 0 |
| 1079 | `M_KOJO_XXX_MESSAGE_COM_KX_74` | LOCALSSIZE 1 / RETURN 0 |
| 1135 | `M_KOJO_XXX_MESSAGE_COM_KX_75` | LOCALSSIZE 1 / RETURN 0 |
| 1176 | `M_KOJO_XXX_MESSAGE_COM_KX_79` | LOCALSSIZE 1 / RETURN 0 |

### M_KOJO_KX_X2_性骚扰指令.ERB
*26.9 KB ／ 773 行 ／ 46 个函数*

| 行号 | 函数名 | 用途 |
|---|---|---|
| 14 | `M_KOJO_XXX_SUCCESS_COM_KX_310` | PREVCOM == 305，表示前回指令为膝枕，躺在TARGET大腿上摸屁股 / TFLAG:400 == 1，约会地点旁边的人作出了反应 |
| 23 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_310` | 当ABL:親密 > 5时， 会无视口上侧使用TFLAG:192（除了== -2以外）的干预，使TFLAG:193被重新赋值，最低为2。 / 值得一提的是，如果角色在工作中，则无法实 |
| 26 | `M_KOJO_XXX_MESSAGE_COM_KX_310` | 摸屁股 |
| 30 | `M_KOJO_XXX_MESSAGE_COM_KX_310_1` | — |
| 78 | `M_KOJO_XXX_SUCCESS_COM_KX_311` | CFLAG:317==2&&TCVAR:20（32=从身前抱住 60=强制接吻 73=洗面奶（用胸部搓脸） 74=互相磨乳房 77=要求吸乳头 ＶＡ性交（85=Ｖ插入状态 87=Ａ |
| 89 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_311` | 或者无志气在非UFUFU时，没有与TARGET取得UFUFU的既成事实，也无法实行指令 / 工作时一视同仁地无法实行指令 |
| 92 | `M_KOJO_XXX_MESSAGE_COM_KX_311` | 拥抱 |
| 96 | `M_KOJO_XXX_MESSAGE_COM_KX_311_1` | — |
| 155 | `M_KOJO_XXX_SUCCESS_COM_KX_312` | TFLAG:400（1=约会地点旁边的人作出了反应） / 如果除了思慕以外的任何陷落状态都没有，会导致指令进入冷却时间 |
| 168 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_312` | 工作时一视同仁地无法实行指令 / 进入CD后，除非是逆推，否则必须等一个小时后才能实施指令 |
| 171 | `M_KOJO_XXX_MESSAGE_COM_KX_312` | 接吻 |
| 175 | `M_KOJO_XXX_MESSAGE_COM_KX_312_1` | — |
| 232 | `M_KOJO_XXX_SUCCESS_COM_KX_313` | 可以用%OPPAI_DESCRIPTION(TARGET, 1)%对胸部进行描述，TEQUIP:1表示TARGET穿着上衣（至少穿着BRA），并且上衣可以扒开，用%SHOW_TOP |
| 240 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_313` | 亲热强度<2、睡眠中、陪睡时、约会中、无志气又不在UFUFU状态，均无法执行指令 / 值得一提的是，如果角色在工作中，则无法实行指令，但唯独美宵是例外。 |
| 243 | `M_KOJO_XXX_MESSAGE_COM_KX_313` | 胸爱抚 |
| 247 | `M_KOJO_XXX_MESSAGE_COM_KX_313_1` | — |
| 305 | `M_KOJO_XXX_SUCCESS_COM_KX_314` | TFLAG:400（1=约会地点旁边的人作出了反应） / TEQUIP:0 > 1表示TARGET穿着下装（至少穿着内裤）并且下装可以被掀开，用%SHOW_BOTTOM(TARGE |
| 312 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_314` | 亲热强度<2、睡眠中、工作中、陪睡中、约会中、非UFUFU时的无志气，均不可实行指令 |
| 315 | `M_KOJO_XXX_MESSAGE_COM_KX_314` | 肛门爱抚 |
| 319 | `M_KOJO_XXX_MESSAGE_COM_KX_314_1` | — |
| 353 | `M_KOJO_XXX_SUCCESS_COM_KX_315` | TEQUIP:0 > 1表示TARGET穿着下装（至少穿着内裤）并且下装可以被掀开，用%SHOW_BOTTOM(TARGET)%表示下装 / TFLAG:400（1=约会地点旁边的 |
| 360 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_315` | 亲热强度<2、睡眠中、工作中、陪睡中、约会中、非UFUFU时的无志气，均不可实行指令 |
| 363 | `M_KOJO_XXX_MESSAGE_COM_KX_315` | 阴蒂爱抚 |
| 367 | `M_KOJO_XXX_MESSAGE_COM_KX_315_1` | — |
| 418 | `M_KOJO_XXX_SUCCESS_COM_KX_316` | TEQUIP:0 > 1表示TARGET穿着下装（至少穿着内裤）并且下装可以被掀开，用%SHOW_BOTTOM(TARGET)%表示下装 / TFLAG:400（1=约会地点旁边的 |
| 425 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_316` | 亲热强度<2、TEQUIP:0 & 4（穿着不能把手伸进去的衣服）、睡眠中、工作中、陪睡中、约会中、V正在被插入、非UFUFU时的无志气，均不可实行指令 |
| 428 | `M_KOJO_XXX_MESSAGE_COM_KX_316` | 手指插入 |
| 432 | `M_KOJO_XXX_MESSAGE_COM_KX_316_1` | — |
| 470 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_317` | TFLAG:194 :表示选项的结果（1，激烈地动腰 ；2，慢慢地抽插；3，扭动着腰）（0就是没有出现选项） / ABL:Ｖ感覚 < 2，还不太舒服，忍耐着抽插；< 5，开始涌上快 |
| 473 | `M_KOJO_XXX_MESSAGE_COM_KX_317` | 动起腰身（Ｖ） |
| 477 | `M_KOJO_XXX_MESSAGE_COM_KX_317_1` | — |
| 527 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_318` | TFLAG:194 :表示选项的结果（1，激烈地动腰 ；2，慢慢地抽插；3，扭动着腰）（0就是没有出现选项） / ABL:Ａ感覚 < 2，皱起眉头，还不太舒服；< 5，发出甜美的叫 |
| 530 | `M_KOJO_XXX_MESSAGE_COM_KX_318` | 动起腰身（Ａ） |
| 534 | `M_KOJO_XXX_MESSAGE_COM_KX_318_1` | — |
| 577 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_320` | TARGET没有性器官（如梅蒂欣）、MASTER无法/没有勃起、振动棒插入中、与TARGET存在体格差而未达成条件、 / 时停中TARGET为处女而润滑不足、在浴室而没有塑料地毯， |
| 580 | `M_KOJO_XXX_MESSAGE_COM_KX_320` | 对方主導正常位 |
| 584 | `M_KOJO_XXX_MESSAGE_COM_KX_320_1` | — |
| 627 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_322` | 站立位会加300点TARGET的露出SOURCE / TARGET没有性器官（如梅蒂欣）、MASTER无法/没有勃起、振动棒插入中、与TARGET存在体格差而未达成条件、在浴室而没 |
| 630 | `M_KOJO_XXX_MESSAGE_COM_KX_322` | 对方主導後背位 |
| 634 | `M_KOJO_XXX_MESSAGE_COM_KX_322_1` | — |
| 676 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_323` | 不在室内，或者在浴室而没有塑料地毯就会变成站立位，用!INROOM(CFLAG:PLAYER:現在位置) && !(BATHROOM() && ITEM:20)检查 / TARGE |
| 679 | `M_KOJO_XXX_MESSAGE_COM_KX_323` | 对方主導後背位Ａ |
| 683 | `M_KOJO_XXX_MESSAGE_COM_KX_323_1` | — |
| 722 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_330` | 睡眠中、约会中、陪睡中、无志气、TARGET没有穿可以掀起来的下装、或者TARGET全裸时均不可实行指令 / 值得一提的是，如果角色在工作中，则无法实行指令，但唯独美宵是例外。 |
| 725 | `M_KOJO_XXX_MESSAGE_COM_KX_330` | 掀起裙子 |
| 729 | `M_KOJO_XXX_MESSAGE_COM_KX_330_1` | — |

### M_KOJO_KX_X2_施虐系指令.ERB
*13.0 KB ／ 536 行 ／ 13 个函数*

| 行号 | 函数名 | 用途 |
|---|---|---|
| 34 | `M_KOJO_XXX_SUCCESS_COM_KX_XX` | 指令成否判定 / 剧本侧覆写式接管指令的结果的规则，以TFLAG:192返回成否鉴定值。0表示剧本侧不干涉COM本体设定，其余值的定义具体参照COMXX。（SKIP 未编译） |
| 39 | `M_KOJO_XXX_EXTRASOURCE_COM_KX_XX` | —（SKIP 未编译） |
| 44 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_XX` | 做任何事（SKIP 未编译） |
| 49 | `M_KOJO_XXX_MESSAGE_COM_KX_XX` | —（SKIP 未编译） |
| 119 | `M_KOJO_XXX_MESSAGE_COM_KX_100` | 受虐属性高时可增加角色兴奋表现的差分。 / 情景描写参考@MESSAGE_COM100 |
| 162 | `M_KOJO_XXX_MESSAGE_COM_KX_101` | 此指令在Train.csv中标记为未使用，模板仅供参考结构。 / 情景描写参考@MESSAGE_COM101 |
| 206 | `M_KOJO_XXX_MESSAGE_COM_KX_102` | 可考虑差分：是否被绳缚中(TEQUIP:縄)、对象痛觉(TALENT:痛觉)。 / 情景描写参考@MESSAGE_COM102 |
| 250 | `M_KOJO_XXX_MESSAGE_COM_KX_103` | 可考虑差分：玩家是否擅长用针(TALENT:擅长用针)或施虐狂。 / 情景描写参考@MESSAGE_COM103 |
| 294 | `M_KOJO_XXX_MESSAGE_COM_KX_104` | 装着时可考虑差分：时奸中的视觉剥夺反应。 / 情景描写参考@MESSAGE_COM104 |
| 346 | `M_KOJO_XXX_MESSAGE_COM_KX_105` | 装着时可考虑差分：时奸中的被缚状态反应、绳缚技巧差分。 / 情景描写参考@MESSAGE_COM105 |
| 398 | `M_KOJO_XXX_MESSAGE_COM_KX_106` | 口球装着时角色无法正常说话，可在台词中体现含混不清的发音。 / 情景描写参考@MESSAGE_COM106 |
| 450 | `M_KOJO_XXX_MESSAGE_COM_KX_107` | 拘束状态下对象无法自由行动，可在台词中体现无力感或抵抗反应。 / 情景描写参考@MESSAGE_COM107 |
| 502 | `M_KOJO_XXX_MESSAGE_COM_KX_108` | 受虐属性高时可增加角色兴奋表现的差分。 / 情景描写参考@MESSAGE_COM108 |

### M_KOJO_KX_X2_日常系指令.ERB
*95.2 KB ／ 3048 行 ／ 183 个函数*

| 行号 | 函数名 | 用途 |
|---|---|---|
| 18 | `M_KOJO_XXX_SUCCESS_COM_KX_300` | TCVAR:烂醉(没有大成功的情况，1=通常成功or大失败) / 由于内容过多，需要请参考地文：ERB\口上・メッセージ関連\EVENT_MESSAGE_COM300.ERB |
| 30 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_300` | 可选项：关于地文描述的显示设置 / 如果返回0，则地文与口上都会显示；如果返回1，则地文会隐藏，口上会显示；如果返回2，则地文会显示，口上会隐藏；如果返回3则均会被隐藏 |
| 35 | `M_KOJO_XXX_MESSAGE_COM_KX_300` | 会话 |
| 72 | `M_KOJO_XXX_SUCCESS_COM_KX_301` | 当MASTER和美铃的亲密达到7级后，大成功时会有1/5的概率模仿美铃泡茶的样子 / GETBIT(TCVAR:MASTER:特別的茶水, 0)表示使用了ITEM红茶叶，本次泡的是 |
| 82 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_301` | 注：若口上侧无管理则TCVAR:20（COUNTER触发）时强制成功 / 指令CD中、睡眠中、陪睡中、在浴场、宴会中、约会中不在待客室、在外出（非主地图）时，TARGET亲密 <  |
| 87 | `M_KOJO_XXX_MESSAGE_COM_KX_301` | 泡茶 |
| 107 | `M_KOJO_XXX_SUCCESS_COM_KX_302` | TFLAG:193(1=大成功 0=成功 -1=失败) / 不处于约会时，执行指令会使指令进入CD |
| 117 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_302` | 若口上侧无管理则TCVAR:20（COUNTER触发）时强制成功 / 非约会时指令处于CD中、睡眠中、陪睡中、工作中均不可实行指令 |
| 122 | `M_KOJO_XXX_MESSAGE_COM_KX_302` | 身体接触 |
| 145 | `M_KOJO_XXX_SUCCESS_COM_KX_303` | TFLAG:193(2=送上点心盒后成功 1=大成功 0=成功 -1=失败 -2=送上点心盒后失败) / 如果TARGET的TALENT:胆量 < 0则哭泣，反之则生气 |
| 154 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_303` | 大成功清空愤怒值，普通成功愤怒减半 |
| 159 | `M_KOJO_XXX_MESSAGE_COM_KX_303` | 道歉 |
| 189 | `M_KOJO_XXX_SUCCESS_COM_KX_304` | TCVAR:315（=1 没法帮忙，如映姬的审判， =2 代表帮忙也不会加快进度的工作， 如椛的看守） / CFLAG:350 == 41（会话） ／／ 46（玩耍）或者 TCVA |
| 198 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_304` | 如果工作是参加宴会、TCVAR:315 == 1（没法帮忙）、约会中，均不可实行指令 |
| 203 | `M_KOJO_XXX_MESSAGE_COM_KX_304` | 帮忙干活 |
| 239 | `M_KOJO_XXX_SUCCESS_COM_KX_305` | 如果TALENT:妊娠，则贴在肚子上听动静 / 该指令有CD |
| 249 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_305` | 如果TALENT:MASTER:体型 > TALENT:体型 + 2，则指令会强制失败，使TFLAG:193 = -5，并大量消减TARGET的体力与气力，减少好感度 / 亲热强度 |
| 254 | `M_KOJO_XXX_MESSAGE_COM_KX_305` | 索求膝枕（MASTER向TARGET索求膝枕，枕在TARGET腿上） |
| 285 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_306` | 因此这个指令没有TFLAG:192来进行控制 / 亲热强度< 1，工作中，不可实行指令 |
| 290 | `M_KOJO_XXX_MESSAGE_COM_KX_306` | 撫摸肚子（地文内的描述更像是子宫按摩） |
| 319 | `M_KOJO_XXX_SUCCESS_COM_KX_307` | ABL:従順 >= 5，一边露出害羞的表情一边任MASTER为所欲为… / 其他则甩开手 |
| 329 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_307` | 注意：若口上侧无管理，则拥抱模式下必定成功 / 亲热强度<1、工作中、约会中不在待客室均不可实行指令 |
| 334 | `M_KOJO_XXX_MESSAGE_COM_KX_307` | 捏臉蛋（其实是有点疼的，会加一点苦痛和反感的SOURCE） |
| 365 | `M_KOJO_XXX_SUCCESS_COM_KX_308` | 陪睡/睡眠时恶作剧限定指令，不需要考虑其他差分了 / TFLAG:193(1=大成功 0=成功 -1=失败,) |
| 373 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_308` | 捅脸颊 |
| 378 | `M_KOJO_XXX_MESSAGE_COM_KX_308` | 捅脸颊 |
| 396 | `M_KOJO_XXX_SUCCESS_COM_KX_309` | ABL:親密(5以上=露出害羞的表情， 反之红着脸甩开手 / 该指令有CD |
| 406 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_309` | 注意：若口上侧无管理，则拥抱模式下必定成功 / 亲热强度 < 1、眠姦中、工作中、指令CD中而不在陪睡/恶作剧状态，均不可实行指令 |
| 411 | `M_KOJO_XXX_MESSAGE_COM_KX_309` | 摸头 |
| 440 | `M_KOJO_XXX_SUCCESS_COM_KX_331` | TFLAG:193(1=大成功（度过了愉快的时光） 0=成功（喝下了茶水） -1=失败（怀疑着没有喝下茶水）) / MASTER拥有调和知识则降低发觉下药的概率，角色污臭耐性<0（ |
| 463 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_331` | 注:若睡眠药强度>=2时，仍继续下睡眠药，则指令强制失败（具体表现为：角色睡意太高，打着哈欠拒绝了茶） |
| 468 | `M_KOJO_XXX_MESSAGE_COM_KX_331` | 泡茶(下药) |
| 512 | `M_KOJO_XXX_SUCCESS_COM_KX_332` | <10时，本次喝的酒不合口味，减少CFLAG:不会喝酒的值 / 和其他指令不一样，地文在COMF文件里，路径：ERB\コマンド関連\COMF\日常系\COMF332 お酒をふるまう |
| 524 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_332` | 在浴室、在外出（非主地图）时，TARGET亲密 < 3、CFLAG:妊娠自覚状態、约会而不在待客室时均无法实行指令 |
| 529 | `M_KOJO_XXX_MESSAGE_COM_KX_332` | 劝酒 |
| 563 | `M_KOJO_XXX_SUCCESS_COM_KX_333` | 333,听牢骚 / TFLAG:193(6=大成功(醉酒状态) 5=成功(醉酒状态) 4=失败(醉酒状态) 3=大成功 2=成功 1=失败) |
| 572 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_333` | ABL:親密 < 3、拥有反发刻印时无法实行指令 |
| 577 | `M_KOJO_XXX_MESSAGE_COM_KX_333` | 听牢骚 |
| 609 | `M_KOJO_XXX_SUCCESS_COM_KX_334` | CFLAG:妊娠自覚状態(1=改为吃饭) / TALENT:酒耐性(-2=改为吃饭) |
| 618 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_334` | 碰杯 |
| 623 | `M_KOJO_XXX_MESSAGE_COM_KX_334` | 碰杯 |
| 655 | `M_KOJO_XXX_SUCCESS_COM_KX_335` | 如果TARGET的CFLAG:職種 == JOB_酔いつぶれる则无法实行指令 / TFLAG:193(1=大成功 （舒服地醒来了）0=成功 -1=失败（几乎没有任何帮助）) |
| 664 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_335` | 照料（MASTER照料喝醉的TARGET） |
| 669 | `M_KOJO_XXX_MESSAGE_COM_KX_335` | 照料（MASTER照料喝醉的TARGET） |
| 690 | `M_KOJO_XXX_SUCCESS_COM_KX_336` | ABL:親密(4以下=感觉不太好… 9以下=好像很害羞的样子…… 9以上=好像很幸福的样子…… / 该指令有CD |
| 701 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_336` | MASTER体型小于角色体型-1，则因体格差别太大而强制失败 / 亲热强度<2、在室外、在浴室、工作中、睡眠中均不可实行指令 |
| 706 | `M_KOJO_XXX_MESSAGE_COM_KX_336` | 膝枕（MASTER给TARGET膝枕） |
| 739 | `M_KOJO_XXX_SUCCESS_COM_KX_337` | 因为COMF文件最后会使TARGET = CHARA，TFLAG:194 = CHILDNUM，所以可以直接拿来用 / 儿童的名字可以用%CHILDNAME:TARGET:(TFL |
| 747 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_337` | 和孩子互动 |
| 752 | `M_KOJO_XXX_MESSAGE_COM_KX_337` | 和孩子互动 |
| 837 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_350` | 如果flagsetting内口上内特殊判定未设置为1，则特殊判定将不会生效 / 如果TFLAG:パール期限值为真（也就是说MASTER因为惩罚正在被塞入肛珠）的时候指令强制失败…… |
| 842 | `M_KOJO_XXX_MESSAGE_COM_KX_350` | 推倒（时姦時名为猥亵） |
| 909 | `M_KOJO_XXX_MESSAGE_COM_KX_351` | 如果态度较差的角色在非烂醉，非因依赖而允许同行的情况下，或者角色正在工作且非烂醉时，是不能带着同行的。 / 如果身处室外，正在下雨，MASTER手里有伞或者角色带着伞则会共用雨伞， |
| 929 | `M_KOJO_XXX_SUCCESS_COM_KX_352` | FLAG:甲斐性無(1=强制中止指令) / TFLAG:193 (1=成功 0=失败) |
| 938 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_352` | 亲热强度 < 2、GET_TARGETNUM() > 1时无法实行指令 |
| 943 | `M_KOJO_XXX_MESSAGE_COM_KX_352` | 告白 |
| 961 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_353` | FLAG:甲斐性無(1=强制中止指令) / 要注意此时TARGET是睡着的，最好不要写太多语言描写 |
| 966 | `M_KOJO_XXX_MESSAGE_COM_KX_353` | 猥褻（睡眠时恶作剧） |
| 978 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_354` | CFLAG:お招き（0以外=睡着了，微微扭动着身体） / 非恋慕状态无法陪睡，如果开启了补丁的话，爱欲也可以陪睡 |
| 983 | `M_KOJO_XXX_MESSAGE_COM_KX_354` | 陪睡 |
| 1000 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_355` | 355,时间停止（应该仅限于对此时地文的修改） / 如果口上设定中角色在时间停止时无法行动，请不要写任何对角色言行的描写，尽量写成类似地文的风格。 |
| 1005 | `M_KOJO_XXX_MESSAGE_COM_KX_355` | 时间停止（应该仅限于对此时地文的修改） |
| 1015 | `M_KOJO_XXX_SUCCESS_COM_KX_356` | 356,邀请去阴暗处 / 有COM统合判定；EXPOSURE_CHARA_IS_SHY(TARGET)判定不通过 或者 TALENT:无知 就能成功 |
| 1024 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_356` | 没有合意、在待客室时不可实行指令 |
| 1029 | `M_KOJO_XXX_MESSAGE_COM_KX_356` | 邀请去阴暗处 |
| 1053 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_360` | 本函数只是 SIKOU 投票 + 口上按 TCVAR:20（对象的 Counter行動值）分岐。 / 门禁 COM_ABLE360：仅逆推可选（CFLAG:诶嘿嘿==2）、时停/T |
| 1058 | `M_KOJO_XXX_MESSAGE_COM_KX_360` | 任凭摆布 |
| 1164 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_361` | MASTER气力归零后无法进行抵抗 / 地文路径和任凭摆布一样 |
| 1169 | `M_KOJO_XXX_MESSAGE_COM_KX_361` | 进行抵抗（和任凭摆布的影响度计算是反着来的，行动时间翻倍，除此之外没有太大区别……） |
| 1287 | `M_KOJO_XXX_SUCCESS_COM_KX_363` | （角色持有 幼稚素质时，MASTER携带特定书籍《御伽草子》才可使用） / TFLAG:193(1=大成功 0=成功 -1=失败)（没有地文分歧） |
| 1296 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_363` | 朗读 |
| 1301 | `M_KOJO_XXX_MESSAGE_COM_KX_363` | 朗读 |
| 1320 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_364` | 364,撒豆子(仅在节分日（冬之月3日），对鬼族的TARGET可用，会使TARGET获得极大的痛苦） / TFLAG:193表示撒豆子参加的人数 |
| 1325 | `M_KOJO_XXX_MESSAGE_COM_KX_364` | 撒豆子(仅在节分日（冬之月3日），对鬼族的TARGET可用，会使TARGET获得极大的痛苦） |
| 1339 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_365` | 由于素材是在COMF文件中当时随机生成的，不会保存，所以没有办法直接检查卖的是什么素材， / 由于生成素材的循环中，生成时采集经验+1，如果生成素材为空则再+2，总共3次循环。如果 |
| 1344 | `M_KOJO_XXX_MESSAGE_COM_KX_365` | 素材购入 |
| 1361 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_368` | 如果某个技能等级为1以上，则会发生基于技能的自由行动 / 详细内容参考ERB\MOVEMENTS\自由行動\FREE_ACT_10.ERB |
| 1366 | `M_KOJO_XXX_MESSAGE_COM_KX_368` | 陪同行動 |
| 1462 | `M_KOJO_XXX_自由行動判定_KX` | 自由行动判定用函数 / 如果在与上述模板对应的 CASE 编号中返回 -1，这个自由行动将不会被触发 |
| 1477 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_402` | 402,就寝 / TFLAG:193(0=通常 1=一家三口排成了川字) |
| 1482 | `M_KOJO_XXX_MESSAGE_COM_KX_402` | 就寝 |
| 1500 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_403` | 403,休憩 |
| 1505 | `M_KOJO_XXX_MESSAGE_COM_KX_403` | 休憩 |
| 1524 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_405` | 不可带3人外出约会，若角色和MASTER之中一人气力过低，或者角色处于工作日，或者角色态度较低时接受了角色的依赖，都无法外出 / 更详细请参考ERB\コマンド関連\COMF\日常系 |
| 1529 | `M_KOJO_XXX_MESSAGE_COM_KX_405` | 外出(同行時变成约会 |
| 1558 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_410` | 如果TALENT:MASTER:清扫中毒，扫除的态度会异常积极 / 以及……可以在UFUFU中途（仅顺推，被逆推是不行的）进行扫除（会被瞪的） |
| 1563 | `M_KOJO_XXX_MESSAGE_COM_KX_410` | 扫除 |
| 1587 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_411` | TFLAG:194(3=夏天的烈日 2=危险的天气 1=恶劣的天气 （如果在危险/恶劣天气下训练会扣除更多体力气力）0=屋内or通常天气 / 如果MASTER比角色更强，就会变成M |
| 1592 | `M_KOJO_XXX_MESSAGE_COM_KX_411` | 战斗训练 |
| 1638 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_412` | 若MASTER的教养大于角色，则是由MASTER教导TARGET， 反之亦然 / 不同天气会导致学习时间增减 |
| 1643 | `M_KOJO_XXX_MESSAGE_COM_KX_412` | 学习 |
| 1666 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_413` | TFLAG:194(100以上=禁断的菜单（跳蛋食物） 3=甜点 2=主食 1=轻食 / 如果要细致到某一盘料理，可以用DISHNAME == ""(引号内填上料理的名称)，制作相 |
| 1671 | `M_KOJO_XXX_MESSAGE_COM_KX_413` | 料理 |
| 1715 | `M_KOJO_XXX_SUCCESS_COM_KX_414` | 在特殊节分吃相应的料理，会有特殊地文，详见ERB\口上・メッセージ関連\EVENT_MESSAGE_COM400.ERB / 可以根据料理的点数做差分TCVAR:306（料理評価値 |
| 1724 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_414` | TFLAG:192在这里控制对料理的评价值，=1则最低500分，最高700分；=-1则固定为400分；=-2中止指令，=0则系统自行计算 |
| 1729 | `M_KOJO_XXX_MESSAGE_COM_KX_414` | 吃饭（MASTER和TARGET一起吃饭） |
| 1762 | `M_KOJO_XXX_SUCCESS_COM_KX_415` | 415,招待吃饭（和414吃饭几乎一样，函数都是调用的414的，唯一的不同在于MASTER不会吃） / TFLAG:193(1=大成功 0=成功 -1=失败) |
| 1771 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_415` | 招待吃饭（和414吃饭几乎一样，函数都是调用的414的，唯一的不同在于MASTER不会吃） |
| 1776 | `M_KOJO_XXX_MESSAGE_COM_KX_415` | 招待吃饭（和414吃饭几乎一样，函数都是调用的414的，唯一的不同在于MASTER不会吃） |
| 1817 | `M_KOJO_XXX_SUCCESS_COM_KX_416` | 参与演奏也是有CD的 / COMF文件路径：ERB\コマンド関連\COMF\日常系\COMF416 演奏する.ERB |
| 1826 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_416` | 宴会时，ABL:MASTER:音楽技能 < 3指令强制失败 |
| 1831 | `M_KOJO_XXX_MESSAGE_COM_KX_416` | 演奏 |
| 1875 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_417` | 在非陪睡状态下，如果随机值为5且未取得UFUFU的合意，TFLAG:193 = 2；如果随机值为2且TARGET无接吻经验，TFLAG:193 = 3 / TFLAG:193(0= |
| 1880 | `M_KOJO_XXX_MESSAGE_COM_KX_417` | 午睡 |
| 1916 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_421` | 由于条件很复杂，需要参考ERB\指令関連\COMF\日常系\COMF421 願掛け.ERB / 以下仅列出几个通用祈愿内容 |
| 1921 | `M_KOJO_XXX_MESSAGE_COM_KX_421` | 祈願 |
| 1955 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_431` | 当满足钱汤指令的实行条件（在人里/旧地狱的钱汤）时，该指令不可用（也就是说431和432指令是相互冲突的） / TFLAG:400为真表示在公共场所洗澡，路人做出了反应 |
| 1960 | `M_KOJO_XXX_MESSAGE_COM_KX_431` | 在浴室里放松 |
| 1981 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_432` | TFLAG:211(4=没能进去（地底温泉番台的妖怪投来了愤怒的视线） 1=进入钱汤） / 钱汤的地文在ERB\コマンド関連\COMF\日常系\COMF432 銭湯.ERB |
| 1986 | `M_KOJO_XXX_MESSAGE_COM_KX_432` | 钱汤（即付费澡堂） |
| 2007 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_436` | 见COMMON.ERB @EXP_UP；文本阶段在指令体结算之后、EVENTCOMEND重快照之前，增量即本次读书所得）。 / 经验编号用 GETNUM(EXP, "经验名") 按 |
| 2012 | `M_KOJO_XXX_MESSAGE_COM_KX_436` | 读书 |
| 2058 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_440` | 仅在地图入口处可执行此命令 CHK_ENTRANCE(CFLAG:MASTER:現在位置, MAIN_MAP) / 差分较多，具体可参考地文ERB\口上・メッセージ関連\EVENT |
| 2063 | `M_KOJO_XXX_MESSAGE_COM_KX_440` | 等待 |
| 2097 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_441` | 441,听课(慧音专用版的学习，只能在慧音工作时实施该指令） |
| 2102 | `M_KOJO_XXX_MESSAGE_COM_KX_441` | 听课(慧音专用版的学习，只能在慧音工作时实施该指令） |
| 2124 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_442` | 木材种类用%WOOD_NAME(数字)%表示（12是竹子，646是香木，其余的详见ERB\コマンド関連\COMF\日常系\WoodData.ERB / 砍树的地文在COMF文件里， |
| 2129 | `M_KOJO_XXX_MESSAGE_COM_KX_442` | 伐采 |
| 2161 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_445` | TFLAG:193表示採集物的物品ID, == 0就是什么都没有找到，物品ID详见CSV/ITEM.CSV / TFLAG:194表示这次采集到的物品数量 |
| 2166 | `M_KOJO_XXX_MESSAGE_COM_KX_445` | 采集 |
| 2193 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_448` | FLAG:194,猎物的编号，具体可参考地文ERB\口上・メッセージ関連\EVENT_MESSAGE_COM400.ERB / 虫子的名称 可通过 MUSHI_NAME 来表示和确 |
| 2198 | `M_KOJO_XXX_MESSAGE_COM_KX_448` | 设下陷阱 \ 设下昆虫诱捕装置 |
| 2237 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_449` | 虫子的名称 可通过 MUSHI_NAME 来表示和确定 / 冬天没有虫子 |
| 2242 | `M_KOJO_XXX_MESSAGE_COM_KX_449` | 捕虫 |
| 2280 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_483` | TFLAG:194是MASTER的排名（MASTER排名为1代表TARGET失败） / 战斗期间的口上包含在EVENT系模板中，这里写战斗之后的内容 |
| 2285 | `M_KOJO_XXX_MESSAGE_COM_KX_483` | 斗虫 |
| 2316 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_484` | 如果角色为说谎者，则在打西瓜失败后获得更多的欢乐，反之则降低欢乐获取值，获得受动与征服（均为SOURCE） / 打西瓜中途的口上包含在EVENT系模板中，这里写打西瓜结束后的内容 |
| 2321 | `M_KOJO_XXX_MESSAGE_COM_KX_484` | 打西瓜 |
| 2349 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_490` | 内容过多，请参考ERB\コマンド関連\COMF\日常系\COMF490 アイテム.ERB / 如果不想细写的话，可以用ITEMTYPE粗略给ITEM分种类 |
| 2354 | `M_KOJO_XXX_MESSAGE_COM_KX_490` | 道具 |
| 2391 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_600` | 目前未实装 / 600,约会会话（SKIP 未编译） |
| 2396 | `M_KOJO_XXX_MESSAGE_COM_KX_600` | 约会会话（SKIP 未编译） |
| 2407 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_601` | 601,约会时身体接触（SKIP 未编译） |
| 2412 | `M_KOJO_XXX_MESSAGE_COM_KX_601` | 约会时身体接触（SKIP 未编译） |
| 2423 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_602` | 602,约会时接吻（SKIP 未编译） |
| 2428 | `M_KOJO_XXX_MESSAGE_COM_KX_602` | 约会时接吻（SKIP 未编译） |
| 2440 | `M_KOJO_XXX_SUCCESS_COM_KX_603` | TFLAG:193(1=大成功 0=成功 -1=失败)(失败时只会犹豫地握住手 / 连续实施牵手指令会变成拉手（见之后的模板） |
| 2449 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_603` | 牵手 |
| 2454 | `M_KOJO_XXX_MESSAGE_COM_KX_603` | 牵手 |
| 2475 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_604` | 约会时、CFLAG:現在位置代表MASTER移动的目标位置 / 部分角色（小町和若鹭姬）会导致移动所需时间增减 |
| 2480 | `M_KOJO_XXX_MESSAGE_COM_KX_604` | 散步（其实就是约会时的移动指令） |
| 2497 | `M_KOJO_XXX_SUCCESS_COM_KX_605` | 605,绕道（会导致到达目的地的所需时间增加10分钟） / TFLAG:193(1=大成功 0=成功 -1=失败)(没有地文差分) |
| 2506 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_605` | 若口上侧无管理则TCVAR:20（COUNTER触发）时强制成功 |
| 2511 | `M_KOJO_XXX_MESSAGE_COM_KX_605` | 绕道（会导致到达目的地的所需时间增加10分钟） |
| 2525 | `M_KOJO_XXX_SUCCESS_COM_KX_610` | 可以实施该指令的地点： / 933=地底酒场（旧地狱街道）、218=人里小料理屋（商家町）444=夜雀小店（竹林入口）（如果米斯琪在工作中则不可用）、中有之道（这个地方要求必须外出 |
| 2534 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_610` | 请TARGET吃饭 |
| 2539 | `M_KOJO_XXX_MESSAGE_COM_KX_610` | 请TARGET吃饭 |
| 2557 | `M_KOJO_XXX_SUCCESS_COM_KX_613` | 613,赚钱	[目前已弃用] |
| 2566 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_613` | 赚钱	[目前已弃用] |
| 2571 | `M_KOJO_XXX_MESSAGE_COM_KX_613` | 赚钱	[目前已弃用] |
| 2579 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_614` | 614,采购食材 / TFLAG:193(1=购入且获得了约会经验 0=购入 -1=没有购入) |
| 2584 | `M_KOJO_XXX_MESSAGE_COM_KX_614` | 采购食材 |
| 2606 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_615` | 可以实行该指令的地方：地蔵小路,倒垂的柳树下,霧之湖,玄武之泽,大蛤蟆之池,绝景之丘,山之湖,天界 / TFLAG:193(1=大成功 0=成功 -1=失败) |
| 2611 | `M_KOJO_XXX_MESSAGE_COM_KX_615` | 吃便当 |
| 2637 | `M_KOJO_XXX_SUCCESS_COM_KX_617` | 617,邀请去甜品店 / TFLAG:193(1=大成功（十分喜悦） 0=成功 -1=失败)(地文分岐只是为了大成功而追加，并无实际加成 |
| 2646 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_617` | 邀请去甜品店 |
| 2651 | `M_KOJO_XXX_MESSAGE_COM_KX_617` | 邀请去甜品店 |
| 2662 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_618` | 618,花屋 / 似乎没有什么检查是否购买的直接方法 |
| 2667 | `M_KOJO_XXX_MESSAGE_COM_KX_618` | 花屋 |
| 2679 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_620` | TFLAG:193(1=借好书了 0=没有借书） / ITEM:10X (X =1 战术指南书  X = 2 料理指南书  X = 3 字典  X = 4 御伽草子  X = 5  |
| 2684 | `M_KOJO_XXX_MESSAGE_COM_KX_620` | 铃奈庵 |
| 2738 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_621` | 在非约会时（约会时必然会一起钓鱼），如果当前角色ABL:TARGET:親密 >= 5 - TALENT:TARGET:釣魚Lv，且非工作状态，意识清醒，就会一起钓鱼。否则不会。 / |
| 2743 | `M_KOJO_XXX_MESSAGE_COM_KX_621` | 钓鱼 |
| 2776 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_626` | 如果想细致地写礼物的名字、种类和形容词的话，将下面的代码取消注释就行了，根据需要使用相应的LOCALS，不用就删掉 / 想写得更加具体请参考ERB\イベント関連\贈り物関連\贈り物 |
| 2781 | `M_KOJO_XXX_MESSAGE_COM_KX_626` | 土产屋 |
| 2831 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_698` | 如果不启用无条件访问补丁的话， / 1.角色工作中、2.如果催眠强度不够，既没有角色的恋慕也不是爱人，还不在发情状态、3.角色愤怒>50、4.角色睡眠中，这些条件成立的话无法使用指 |
| 2836 | `M_KOJO_XXX_MESSAGE_COM_KX_698` | 进入房间 |
| 2846 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_699` | 699,外出 |
| 2851 | `M_KOJO_XXX_MESSAGE_COM_KX_699` | 外出 |
| 2879 | `M_KOJO_XXX_SUCCESS_SCOM_KX_60` | 根据膝枕和被膝枕的区别，分为角色被掏耳朵和主角被掏耳朵。可以用 PREVCOM进行侦测前一个指令到底是什么来检测到底是谁掏谁 / TFLAG:193(1=大成功 0=成功 -1=失 |
| 2888 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_SCOM_KX_60` | 掏耳朵 |
| 2893 | `M_KOJO_XXX_MESSAGE_SCOM_KX_60` | 掏耳朵 |
| 2913 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_SCOM_KX_61` | (TARGET睡眠时间or衰弱)陪睡时、前一个指令为拥抱，后接就寝，会让就寝变成抱枕 / MASTER\@ TALENT:105 > 0 ? 把脸埋进TARGET的胸部 # 将TA |
| 2918 | `M_KOJO_XXX_MESSAGE_SCOM_KX_61` | 抱枕 |
| 2931 | `M_KOJO_XXX_SUCCESS_SCOM_KX_62` | ABL:欲望(5以上=欲求不满的眼神） / ABL:親密(5以上=脸变得通红） |
| 2940 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_SCOM_KX_62` | TFLAG:102 == 3（被逆推时），指令强制成功 |
| 2945 | `M_KOJO_XXX_MESSAGE_SCOM_KX_62` | 亲额头 |
| 2970 | `M_KOJO_XXX_SUCCESS_SCOM_KX_63` | 睡着时，ABL:親密 >= 8则接吻结束后露出微笑，ABL:親密 >= 5则有点难受地皱起眉头，其他情况下神情扭曲并转过脸 / 正常情况下，TALENT:恋慕则把嘴唇抵过来，ABL |
| 2979 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_SCOM_KX_63` | TFLAG:102 == 3（被逆推时），指令强制成功 |
| 2984 | `M_KOJO_XXX_MESSAGE_SCOM_KX_63` | 更多的接吻 |
| 3021 | `M_KOJO_XXX_SUCCESS_SCOM_KX_80` | 约会出发后道中时，牵手后会让牵手变成拉手（会走得更快，减少到达目的地所需的时间） / TFLAG:193(1=大成功 0=成功 （开心地快步走）-1=失败)（无辜地快步走） |
| 3030 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_SCOM_KX_80` | 拉手 |
| 3035 | `M_KOJO_XXX_MESSAGE_SCOM_KX_80` | 拉手 |

### M_KOJO_KX_X2_日记.ERB
*11.8 KB ／ 336 行 ／ 6 个函数*

| 行号 | 函数名 | 用途 |
|---|---|---|
| 119 | `DIARY_XXX_KX_EXIST` | 0 = 没有日记（系统判定该角色不写日记） / 1 = 有日记（系统会继续调用其他日记接口） |
| 140 | `DIARY_XXX_AFTER_CHECK_KX` | SIF CFLAG:XX:好感度 <= LAST_LP + 3 / NOTOUCH_DAY |
| 166 | `DIARY_XXX_BEFORE_CHECK_KX` | 思慕：       TALENT:XX:思慕 / 初次见面：   CFLAG:XX:面識 |
| 213 | `DIARY_XXX_TEXT_KX` | MODE == "デイリー" 时，建议显示角色表情/服装； / MODE == "コマンド" 时，可加入角色对日记内容的评论反应。 |
| 296 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_406` | —（SKIP 未编译） |
| 312 | `M_KOJO_XXX_MESSAGE_COM_KX_406` | SPTALK = 用于日记阅读后的反应对话 / 如果 TFLAG:194 != XX，说明正在阅读他人日记，需另行处理。 |

### M_KOJO_KX_X2_日记（简易版）.ERB
*10.3 KB ／ 379 行 ／ 28 个函数*

| 行号 | 函数名 | 用途 |
|---|---|---|
| 17 | `DIARY_XXX_KX_EXIST` | 存在判定 / 返回1则日记系统会处理该角色的日记 |
| 27 | `DIARY_XXX_BEFORE_CHECK_KX` | 简易版自动遍历DIARY_XXX_KX_1_HAPPEN ~ DIARY_XXX_KX_100_HAPPEN / 根据各HAPPEN的返回值判定是否写入日记 |
| 50 | `DIARY_XXX_AFTER_CHECK_KX` | 事后处理 / 每日事件读取日记后的收尾处理，可管理标志位等 |
| 62 | `DIARY_XXX_TEXT_KX` | "コマンド"：[阅读日记]指令读取 / PAGECOUNT = 写入的第几页 |
| 107 | `DIARY_XXX_KX_1_HAPPEN` | 第1页 |
| 122 | `DIARY_XXX_KX_1` | －－－－－－－－－－－－－－－－－－－－－－－－－－－－－ |
| 131 | `DIARY_XXX_KX_2_HAPPEN` | 第2页 |
| 144 | `DIARY_XXX_KX_2` | －－－－－－－－－－－－－－－－－－－－－－－－－－－－－ |
| 153 | `DIARY_XXX_KX_3_HAPPEN` | 第3页 |
| 166 | `DIARY_XXX_KX_3` | －－－－－－－－－－－－－－－－－－－－－－－－－－－－－ |
| 175 | `DIARY_XXX_KX_4_HAPPEN` | 第4页 |
| 188 | `DIARY_XXX_KX_4` | －－－－－－－－－－－－－－－－－－－－－－－－－－－－－ |
| 197 | `DIARY_XXX_KX_5_HAPPEN` | 第5页 |
| 210 | `DIARY_XXX_KX_5` | －－－－－－－－－－－－－－－－－－－－－－－－－－－－－ |
| 219 | `DIARY_XXX_KX_6_HAPPEN` | 第6页 |
| 232 | `DIARY_XXX_KX_6` | －－－－－－－－－－－－－－－－－－－－－－－－－－－－－ |
| 241 | `DIARY_XXX_KX_7_HAPPEN` | 第7页 |
| 254 | `DIARY_XXX_KX_7` | －－－－－－－－－－－－－－－－－－－－－－－－－－－－－ |
| 263 | `DIARY_XXX_KX_8_HAPPEN` | 第8页 |
| 276 | `DIARY_XXX_KX_8` | －－－－－－－－－－－－－－－－－－－－－－－－－－－－－ |
| 285 | `DIARY_XXX_KX_9_HAPPEN` | 第9页 |
| 298 | `DIARY_XXX_KX_9` | －－－－－－－－－－－－－－－－－－－－－－－－－－－－－ |
| 307 | `DIARY_XXX_KX_10_HAPPEN` | 第10页 |
| 320 | `DIARY_XXX_KX_10` | －－－－－－－－－－－－－－－－－－－－－－－－－－－－－ |
| 331 | `DIARY_XXX_KX_YY_HAPPEN` | —（SKIP 未编译） |
| 344 | `DIARY_XXX_KX_YY` | －－－－－－－－－－－－－－－－－－－－－－－－－－－－－（SKIP 未编译） |
| 366 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_406` | 返回2：显示描述，隐藏口上 / 返回3：隐藏描述和口上 |
| 371 | `M_KOJO_XXX_MESSAGE_COM_KX_406` | 阅读日记 |

### M_KOJO_KX_X2_派生指令.ERB
*19.7 KB ／ 866 行 ／ 23 个函数*

| 行号 | 函数名 | 用途 |
|---|---|---|
| 82 | `M_KOJO_XXX_MESSAGE_SCOM_KX_1` | 日文：シックスナイン / 双方互相口交的体位 |
| 115 | `M_KOJO_XXX_MESSAGE_SCOM_KX_2` | 日文：岩清水 / 刺激阴道壁使其大量分泌爱液的指令 |
| 148 | `M_KOJO_XXX_MESSAGE_SCOM_KX_3` | 日文：Gスポット刺激 / 用指交或道具刺激G点的指令 |
| 181 | `M_KOJO_XXX_MESSAGE_SCOM_KX_4` | 日文：乱れ牡丹 / 69姿势中同时刺激女方的阴部和肛门的指令 |
| 214 | `M_KOJO_XXX_MESSAGE_SCOM_KX_5` | 日文：手淫フェラ / 一边手淫一边口交的指令 |
| 247 | `M_KOJO_XXX_MESSAGE_SCOM_KX_6` | 日文：挿入Ｇスポ責め / 插入状态下针对G点的刺激 |
| 280 | `M_KOJO_XXX_MESSAGE_SCOM_KX_7` | 日文：挿入子宮口責め / 插入状态下针对子宫口的刺激 |
| 313 | `M_KOJO_XXX_MESSAGE_SCOM_KX_8` | 日文：６９パイズリ / 69姿势中使用乳交刺激的指令 |
| 347 | `M_KOJO_XXX_MESSAGE_SCOM_KX_9` | 两名角色同时为主人口交的多人指令 / 需要搭档台词模板：@M_KOJO_XXX_MESSAGE_SCOM_KX_9_2 |
| 383 | `M_KOJO_XXX_MESSAGE_SCOM_KX_9_2` | 真实执行对象ID可通过 MASTER_POSE(SET_M, SET_P, 1) 取得： / 返回前一回合中用嘴（SET_M）含住MASTER阴茎（SET_P）的角色编号 |
| 420 | `M_KOJO_XXX_MESSAGE_SCOM_KX_10` | 两名角色同时用大腿夹住主人肉棒的多人指令 / 需要搭档台词模板：@M_KOJO_XXX_MESSAGE_SCOM_KX_10_2 |
| 456 | `M_KOJO_XXX_MESSAGE_SCOM_KX_10_2` | 真实执行对象ID可通过 MASTER_POSE(SET_C, SET_P, 1) 取得： / 返回前一回合中用阴蒂/素股部位（SET_C）夹住MASTER阴茎（SET_P）的角色编 |
| 493 | `M_KOJO_XXX_MESSAGE_SCOM_KX_11` | 两名角色同时用胸部为主人服务的多人指令 / 需要搭档台词模板：@M_KOJO_XXX_MESSAGE_SCOM_KX_11_2 |
| 529 | `M_KOJO_XXX_MESSAGE_SCOM_KX_11_2` | 真实执行对象ID可通过 MASTER_POSE(SET_B, SET_P, 1) 取得： / 返回前一回合中用胸部（SET_B）夹住MASTER阴茎（SET_P）的角色编号 |
| 565 | `M_KOJO_XXX_MESSAGE_SCOM_KX_12` | 日文：パイズリフェラ / 用乳交夹住肉棒的同时进行口交的指令 |
| 599 | `M_KOJO_XXX_MESSAGE_SCOM_KX_13` | 两名角色轮流被插入的多人指令 / 需要搭档台词模板：@M_KOJO_XXX_MESSAGE_SCOM_KX_13_2 |
| 635 | `M_KOJO_XXX_MESSAGE_SCOM_KX_13_2` | 真实执行对象ID可通过 MASTER_POSE(SET_V, SET_P, 1) 取得： / 返回前一回合中用阴道（SET_V）接受MASTER阴茎（SET_P）的角色编号 |
| 671 | `M_KOJO_XXX_MESSAGE_SCOM_KX_14` | 日文：Ｓ状結腸責め / 通过肛门深部刺激S状结肠的指令 |
| 704 | `M_KOJO_XXX_MESSAGE_SCOM_KX_15` | 日文：膣裏責め / 从肛门侧隔着阴道壁进行刺激的指令 |
| 738 | `M_KOJO_XXX_MESSAGE_SCOM_KX_16` | 两名角色轮流被肛门插入的多人指令 / 需要搭档台词模板：@M_KOJO_XXX_MESSAGE_SCOM_KX_16_2 |
| 774 | `M_KOJO_XXX_MESSAGE_SCOM_KX_16_2` | 真实执行对象ID可通过 MASTER_POSE(SET_A, SET_P, 1) 取得： / 返回前一回合中用肛门（SET_A）接受MASTER阴茎（SET_P）的角色编号 |
| 810 | `M_KOJO_XXX_MESSAGE_SCOM_KX_17` | 日文：乳首同時吸い / 两名角色同时吸吮乳头的多人指令 |
| 844 | `M_KOJO_XXX_MESSAGE_SCOM_KX_19` | （此编号在CSV中对应519，跳过18号） / 模仿哺乳行为的指令，需要角色处于乳汁分泌状态 |

### M_KOJO_KX_X2_爱抚系指令.ERB
*38.3 KB ／ 1595 行 ／ 25 个函数*

| 行号 | 函数名 | 用途 |
|---|---|---|
| 129 | `M_KOJO_XXX_SUCCESS_COM_KX_XX` | —（SKIP 未编译） |
| 134 | `M_KOJO_XXX_EXTRASOURCE_COM_KX_XX` | —（SKIP 未编译） |
| 139 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_XX` | 做任何事（SKIP 未编译） |
| 144 | `M_KOJO_XXX_MESSAGE_COM_KX_XX` | —（SKIP 未编译） |
| 182 | `M_KOJO_XXX_MESSAGE_COM_KX_0` | LOCALSSIZE 1 / RETURN 0 |
| 297 | `M_KOJO_XXX_MESSAGE_COM_KX_1` | LOCALSSIZE 1 / RETURN 0 |
| 363 | `M_KOJO_XXX_MESSAGE_COM_KX_2` | LOCALSSIZE 1 / RETURN 0 |
| 416 | `M_KOJO_XXX_MESSAGE_COM_KX_3` | LOCALSSIZE 1 / RETURN 0 |
| 500 | `M_KOJO_XXX_MESSAGE_COM_KX_4` | LOCALSSIZE 1 / RETURN 0 |
| 566 | `M_KOJO_XXX_MESSAGE_COM_KX_5` | LOCALSSIZE 1 / RETURN 0 |
| 653 | `M_KOJO_XXX_MESSAGE_COM_KX_6` | LOCALSSIZE 1 / RETURN 0 |
| 758 | `M_KOJO_XXX_MESSAGE_COM_KX_7` | LOCALSSIZE 1 / RETURN 0 |
| 832 | `M_KOJO_XXX_MESSAGE_COM_KX_8` | LOCALSSIZE 1 / RETURN 0 |
| 912 | `M_KOJO_XXX_MESSAGE_COM_KX_9` | LOCALSSIZE 1 / RETURN 0 |
| 987 | `M_KOJO_XXX_MESSAGE_COM_KX_11` | LOCALSSIZE 1 / RETURN 0 |
| 1061 | `M_KOJO_XXX_MESSAGE_COM_KX_12` | LOCALSSIZE 1 / RETURN 0 |
| 1076 | `M_KOJO_XXX_MESSAGE_COM_KX_13` | LOCALSSIZE 1 / RETURN 0 |
| 1152 | `M_KOJO_XXX_MESSAGE_COM_KX_15` | LOCALSSIZE 1 / RETURN 0 |
| 1229 | `M_KOJO_XXX_MESSAGE_COM_KX_19` | LOCALSSIZE 1 / RETURN 0 |
| 1244 | `M_KOJO_XXX_MESSAGE_COM_KX_20` | LOCALSSIZE 1 / RETURN 0 |
| 1321 | `M_KOJO_XXX_MESSAGE_COM_KX_21` | LOCALSSIZE 1 / RETURN 0 |
| 1394 | `M_KOJO_XXX_MESSAGE_COM_KX_22` | 为了让对方对自己出手而进行诱惑，就是诱受 / 无描写，因为是玩家的行动，玩家的露出、液体和情欲上升，因此不可时停发动。 |
| 1432 | `M_KOJO_XXX_SUCCESS_COM_KX_23` | ピロートーク 枕边话（SKIP 未编译） |
| 1458 | `M_KOJO_XXX_MESSAGE_COM_KX_23` | LOCALSSIZE 1 / RETURN 0 |
| 1523 | `M_KOJO_XXX_MESSAGE_COM_KX_25` | LOCALSSIZE 1 / RETURN 0 |

### M_KOJO_KX_X2_特有COUNTER指令.ERB
*5.2 KB ／ 130 行 ／ 4 个函数*

| 行号 | 函数名 | 用途 |
|---|---|---|
| 53 | `UNIQUE_COUNTER1_ABLE_KX_XXX` | 在此函数中编写该COUNTER的触发条件。 / RETURN 1 表示该COUNTER可用，RETURN 0 表示不可用。 |
| 70 | `UNIQUE_COUNTER1_FREQUENCY_KX_XXX` | @UNIQUE_COUNTER{INDEX}_FREQUENCY_KX_XXX / RESULTS指定COUNTER的触发类别，RETURN指定频率补正值。 |
| 88 | `UNIQUE_COUNTER1_MESSAGE_KX_XXX` | COUNTER1 文本 / @UNIQUE_COUNTER{INDEX}_MESSAGE_KX_XXX |
| 100 | `UNIQUE_COUNTER1_SOURCE_KX_XXX` | COUNTER1 数值计算与内部处理 / @UNIQUE_COUNTER{INDEX}_SOURCE_KX_XXX |

### M_KOJO_KX_X2_硬核系指令.ERB
*11.7 KB ／ 562 行 ／ 17 个函数*

| 行号 | 函数名 | 用途 |
|---|---|---|
| 35 | `M_KOJO_XXX_SUCCESS_COM_KX_XX` | —（SKIP 未编译） |
| 40 | `M_KOJO_XXX_EXTRASOURCE_COM_KX_XX` | —（SKIP 未编译） |
| 44 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_XX` | —（SKIP 未编译） |
| 74 | `M_KOJO_XXX_MESSAGE_COM_KX_140` | LOCALSSIZE 1 / RETURN 0 |
| 118 | `M_KOJO_XXX_MESSAGE_COM_KX_144` | LOCALSSIZE 1 / RETURN 0 |
| 158 | `M_KOJO_XXX_MESSAGE_COM_KX_150` | LOCALSSIZE 1 / RETURN 0 |
| 203 | `M_KOJO_XXX_MESSAGE_COM_KX_101` | 101,鞭  使用鞭子抽打（SKIP 未编译） |
| 230 | `M_KOJO_XXX_MESSAGE_COM_KX_102` | 102,蝋燭  滴蜡（SKIP 未编译） |
| 257 | `M_KOJO_XXX_MESSAGE_COM_KX_103` | 103,針  针刺（SKIP 未编译） |
| 284 | `M_KOJO_XXX_MESSAGE_COM_KX_141` | 141,拳交  手拳插入阴道（SKIP 未编译） |
| 311 | `M_KOJO_XXX_MESSAGE_COM_KX_142` | 142,肛門拳交  手拳插入肛门（SKIP 未编译） |
| 338 | `M_KOJO_XXX_MESSAGE_COM_KX_143` | 143,両穴拳交  双手拳同时插入V和A（SKIP 未编译） |
| 365 | `M_KOJO_XXX_MESSAGE_COM_KX_145` | 145,肛門奉仕強制  强制角色进行肛门服务（SKIP 未编译） |
| 393 | `M_KOJO_XXX_MESSAGE_COM_KX_146` | 146,浣腸  灌肠器+肛塞 / TEQUIP:浣腸 灌肠状态（SKIP 未编译） |
| 432 | `M_KOJO_XXX_MESSAGE_COM_KX_147` | 147,拡張氣球  插入气球扩张肛门 / TEQUIP:拡張バルーン 扩张气球状态（SKIP 未编译） |
| 471 | `M_KOJO_XXX_MESSAGE_COM_KX_148` | 148,肛門電極  在肛门安装电极 / TEQUIP:アナル電極 肛门电极状态（SKIP 未编译） |
| 509 | `M_KOJO_XXX_MESSAGE_COM_KX_149` | 149,预留空位（SKIP 未编译） |

### M_KOJO_KX_X2_育儿事件.ERB
*16.9 KB ／ 483 行 ／ 22 个函数*

| 行号 | 函数名 | 用途 |
|---|---|---|
| 72 | `M_KOJO_XXX_EVENT_KX_CHILD_RAISING_回復` | —（SKIP 未编译） |
| 86 | `M_KOJO_XXX_EVENT_KX_CHILD_RAISING_離乳` | —（SKIP 未编译） |
| 98 | `M_KOJO_XXX_EVENT_KX_CHILD_RAISING_玩具` | —（SKIP 未编译） |
| 110 | `M_KOJO_XXX_EVENT_KX_CHILD_RAISING_つかまり立ち` | —（SKIP 未编译） |
| 122 | `M_KOJO_XXX_EVENT_KX_CHILD_RAISING_よちよち` | —（SKIP 未编译） |
| 135 | `M_KOJO_XXX_EVENT_KX_CHILD_RAISING_会話寸前` | —（SKIP 未编译） |
| 147 | `M_KOJO_XXX_EVENT_KX_CHILD_RAISING_喋る` | —（SKIP 未编译） |
| 159 | `M_KOJO_XXX_EVENT_KX_CHILD_RAISING_語彙` | —（SKIP 未编译） |
| 171 | `M_KOJO_XXX_EVENT_KX_CHILD_RAISING_しつけ` | —（SKIP 未编译） |
| 183 | `M_KOJO_XXX_EVENT_KX_CHILD_RAISING_就学` | —（SKIP 未编译） |
| 195 | `M_KOJO_XXX_EVENT_KX_CHILD_RAISING_自立前` | —（SKIP 未编译） |
| 207 | `M_KOJO_XXX_EVENT_KX_CHILD_RAISING_自立` | —（SKIP 未编译） |
| 232 | `M_KOJO_XXX_EVENT_KX_CHILD_RAISING_登下校` | ARG  == 1 : 放学时（从寺子屋回来） / ERB\イベント関連\妊娠関連\CHILD_MOVEMENT.ERB |
| 260 | `M_KOJO_XXX_EVENT_KX_CHILD_RAISING_吃飯` | ARGS == "自立前" : 自立前阶段 / ERB\イベント関連\妊娠関連\CHILD_MOVEMENT.ERB |
| 291 | `M_KOJO_XXX_EVENT_KX_CHILD_RAISING_BATH` | ARGS == "自立前" : 自立前（基本能自己洗） / ERB\イベント関連\妊娠関連\CHILD_MOVEMENT.ERB |
| 319 | `M_KOJO_XXX_EVENT_KX_CHILD_RAISING_SLEEPING` | ARGS == "自立前" : 自立前（自己去睡觉） / ERB\イベント関連\妊娠関連\CHILD_MOVEMENT.ERB |
| 344 | `M_KOJO_XXX_EVENT_KX_CHILD_RAISING_OYASUMI` | 触发条件：选择"就寝"命令时，若有孩子且满足条件则触发 / ERB\コマンド関連\COMF\日常系\COMF402 就寝.ERB |
| 364 | `M_KOJO_XXX_EVENT_KX_CHILD_RAISING_TOY` | ARGS == "自立前" : 自立前（较为成熟的玩耍方式） / ERB\イベント関連\妊娠関連\CHILD_MOVEMENT.ERB |
| 392 | `M_KOJO_XXX_EVENT_KX_CHILD_RAISING_OTHER` | ARGS == "自立前" : 自立前的其他日常行为 / ERB\イベント関連\妊娠関連\CHILD_MOVEMENT.ERB |
| 425 | `M_KOJO_XXX_EVENT_KX_CHILD_DAILY_寺子屋` | ARG  = 孩子的编号（%CHILDNAME:YOME:ARG%） / ERB\イベント関連\デイリーイベント\DAIRY_EV22 子供が寺子屋で.ERB |
| 449 | `M_KOJO_XXX_EVENT_KX_CHILD_DAILY_口上手紙` | —（SKIP 未编译） |
| 468 | `M_KOJO_XXX_EVENT_KX_CHILD_DAILY_共通手紙` | —（SKIP 未编译） |

### M_KOJO_KX_X2_自定义派生指令.ERB
*19.6 KB ／ 715 行 ／ 25 个函数*

| 行号 | 函数名 | 用途 |
|---|---|---|
| 44 | `M_KOJO_XXX_MESSAGE_CUSTOM_SCOM_KX_2` | 2,A乱牡丹 / 对着镜子，背后座位A插入（SKIP 未编译） |
| 63 | `M_KOJO_XXX_MESSAGE_CUSTOM_SCOM_KX_3` | 3,对镜掰开小穴（SKIP 未编译） |
| 82 | `M_KOJO_XXX_MESSAGE_CUSTOM_SCOM_KX_5` | 5,双女上位（SKIP 未编译） |
| 131 | `M_KOJO_XXX_MESSAGE_CUSTOM_SCOM_KX_5_2` | 搭档用文本函数，TARGET被重定向为剧本角色，但并不是指令的执行对象。但注意，会在真正的执行对象调用文本后再调用。（SKIP 未编译） |
| 178 | `M_KOJO_XXX_MESSAGE_CUSTOM_SCOM_KX_6` | 6,指交两人（SKIP 未编译） |
| 194 | `M_KOJO_XXX_MESSAGE_CUSTOM_SCOM_KX_6_2` | 搭档用文本函数，TARGET被重定向为剧本角色，请注意，此时剧本角色并不是指令的执行对象。搭档文本会在真正的执行对象调用文本后再调用。（SKIP 未编译） |
| 211 | `M_KOJO_XXX_MESSAGE_CUSTOM_SCOM_KX_7` | 7,V插入同时指交（SKIP 未编译） |
| 274 | `M_KOJO_XXX_MESSAGE_CUSTOM_SCOM_KX_7_2` | 搭档用文本函数，TARGET被重定向为剧本角色，请注意，此时剧本角色并不是指令的执行对象。搭档文本会在真正的执行对象调用文本后再调用。（SKIP 未编译） |
| 311 | `M_KOJO_XXX_MESSAGE_CUSTOM_SCOM_KX_8` | 8,V插入并指交两人（SKIP 未编译） |
| 380 | `M_KOJO_XXX_MESSAGE_CUSTOM_SCOM_KX_8_2` | 搭档用文本函数，TARGET被重定向为剧本角色，请注意，此时剧本角色并不是指令的执行对象。搭档文本会在真正的执行对象调用文本后再调用。（SKIP 未编译） |
| 420 | `M_KOJO_XXX_MESSAGE_CUSTOM_SCOM_KX_9` | 9,三人乳交（SKIP 未编译） |
| 439 | `M_KOJO_XXX_MESSAGE_CUSTOM_SCOM_KX_10` | 10,三人口交（SKIP 未编译） |
| 458 | `M_KOJO_XXX_MESSAGE_CUSTOM_SCOM_KX_11` | 11,双女上位同时指交（SKIP 未编译） |
| 477 | `M_KOJO_XXX_MESSAGE_CUSTOM_SCOM_KX_12` | 12,双人手交（SKIP 未编译） |
| 500 | `M_KOJO_XXX_MESSAGE_CUSTOM_SCOM_KX_12_2` | 搭档用文本函数，TARGET被重定向为剧本角色，请注意，此时剧本角色并不是指令的执行对象。搭档文本会在真正的执行对象调用文本后再调用。（SKIP 未编译） |
| 529 | `M_KOJO_XXX_MESSAGE_CUSTOM_SCOM_KX_13` | 13,双手手交（SKIP 未编译） |
| 548 | `M_KOJO_XXX_MESSAGE_CUSTOM_SCOM_KX_14` | 14,同时口爆侵犯（SKIP 未编译） |
| 567 | `M_KOJO_XXX_MESSAGE_CUSTOM_SCOM_KX_15` | 15,体外射精（SKIP 未编译） |
| 586 | `M_KOJO_XXX_MESSAGE_CUSTOM_SCOM_KX_16` | 16,三人叠塔（SKIP 未编译） |
| 605 | `M_KOJO_XXX_MESSAGE_CUSTOM_SCOM_KX_17` | 17,三穴插入（SKIP 未编译） |
| 624 | `M_KOJO_XXX_MESSAGE_CUSTOM_SCOM_KX_18` | 18,分身群交（SKIP 未编译） |
| 640 | `M_KOJO_XXX_MESSAGE_CUSTOM_SCOM_KX_19` | —（SKIP 未编译） |
| 648 | `M_KOJO_XXX_MESSAGE_CUSTOM_SCOM_KX_20` | 20,双人腹交（SKIP 未编译） |
| 667 | `M_KOJO_XXX_MESSAGE_CUSTOM_SCOM_KX_21` | 21,双人足交（SKIP 未编译） |
| 690 | `M_KOJO_XXX_MESSAGE_CUSTOM_SCOM_KX_21_2` | 搭档用文本函数，TARGET被重定向为剧本角色，请注意，此时剧本角色并不是指令的执行对象。搭档文本会在真正的执行对象调用文本后再调用。（SKIP 未编译） |

### M_KOJO_KX_X2_自定义系指令.ERB
*10.7 KB ／ 281 行 ／ 10 个函数*

| 行号 | 函数名 | 用途 |
|---|---|---|
| 12 | `M_KOJO_XXX_MESSAGE_CUSTOM_COM_KX_1` | 换泳衣的动作默认是角色自己换而非你先生辅助，这点注意 / 地文位置：ERB\fromEN\Custom_Commands\Add_CUSTOM_COM1.ERB |
| 51 | `M_KOJO_XXX_MESSAGE_CUSTOM_COM_KX_2` | TFLAG:193（进入游泳时穿的各种泳衣，和9001相同，因此可考虑直接把口上文本搬过来） / 地文位置：ERB\fromEN\Custom_Commands\Add_CUSTO |
| 110 | `M_KOJO_XXX_MESSAGE_CUSTOM_COM_KX_3` | TFLAG:194（天气区分，见下） / 地文位置：ERB\fromEN\Custom_Commands\Add_CUSTOM_COM3.ERB |
| 131 | `M_KOJO_XXX_MESSAGE_CUSTOM_COM_KX_11` | 地文位置：ERB\fromEN\Custom_Commands\Add_CUSTOM_COM11 换衣服.ERB / 顺带一提地文里并没有涉及具体操作...所以在这一点上可以稍微奔 |
| 168 | `M_KOJO_XXX_MESSAGE_CUSTOM_COM_KX_12` | GET_DIGIT(TFLAG:194,2) 下衣 / GET_DIGIT(TFLAG:194,1) 内裤 |
| 191 | `M_KOJO_XXX_SUCCESS_CUSTOM_COM_KX_100` | STRCOUNT(CHECK_PHOTO:4, @"_{TARGET}◇") == STRCOUNT(CHECK_PHOTO:4, @"◇") && STRCOUNT(CHECK_ |
| 199 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_CUSTOM_COM_KX_100` | 可选项：关于地文描述的显示设置 / 如果返回0，则地文与口上都会显示；如果返回1，则地文会隐藏，口上会显示；如果返回2，则地文会显示，口上会隐藏；如果返回3则均会被隐藏 |
| 202 | `M_KOJO_XXX_MESSAGE_CUSTOM_COM_KX_100` | — |
| 261 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_CUSTOM_COM_KX_101` | 可选项：关于地文描述的显示设置 / 如果返回0，则地文与口上都会显示；如果返回1，则地文会隐藏，口上会显示；如果返回2，则地文会显示，口上会隐藏；如果返回3则均会被隐藏 |
| 264 | `M_KOJO_XXX_MESSAGE_CUSTOM_COM_KX_101` | — |

### M_KOJO_KX_X2_诶嘿嘿文本库函数.ERB
*14.6 KB ／ 382 行 ／ 15 个函数*

| 行号 | 函数名 | 用途 |
|---|---|---|
| 54 | `XXX_UFUFU_KX` | §1 门禁谓词：这个角色现在愿不愿意说 H 台词 / 阈值按角色调整（如思慕起步的角色加 TALENT:思慕 一行） |
| 86 | `XXX_SEX_KX` | （池自己决定成败；失败 RETURN 0 自然落到自动喘息。禁硬写 RETURN 1） / 禁用：细分函数不想填就整个删掉，TRYCALLFORM 静默跳过 |
| 188 | `XXX_SEX_KX_立位` | 先填通用支（1 句即跑）；不想填的分支函数整个删掉，分发自动跳过 / 体位描写含"压/抱/站"才进对应分支（分支是内容的事实描述，不是愿望） |
| 202 | `XXX_SEX_KX_抱合` | — |
| 216 | `XXX_SEX_KX_背对` | — |
| 230 | `XXX_SEX_KX_通用` | — |
| 250 | `XXX_SEX_KX_站立后入A` | §4 A 池：与 V 池镜像（站立后入A / 后入A / 通用A） / 先填通用支；不想填的分支函数整个删掉，分发自动跳过 |
| 264 | `XXX_SEX_KX_后入A` | — |
| 278 | `XXX_SEX_KX_通用A` | — |
| 298 | `XXX_SEX_KX_余韵` | 或本轮已拔出但 TCVAR:V挿入管理FLAG/A挿入管理FLAG == PLAYER（上回合插入快照）。 / 调用点：性交系/爱抚系各指令的"上回合插入"分支 |
| 310 | `XXX_SEX_KX_初回` | §6 专属事件表（绑定触发事件，不过池） |
| 319 | `XXX_SEX_KX_破瓜` | — |
| 328 | `XXX_SEX_KX_A破瓜` | — |
| 337 | `XXX_SEX_KX_射精` | — |
| 358 | `XXX_SEX_KX_DEBUG` | §8 诊断（游戏内打印当前三维，分支是否命中当场可见） |

### M_KOJO_KX_X2_道具系指令.ERB
*8.2 KB ／ 453 行 ／ 15 个函数*

| 行号 | 函数名 | 用途 |
|---|---|---|
| 20 | `M_KOJO_XXX_SUCCESS_COM_KX_XX` | 指令成否判定 / 剧本侧覆写式接管指令的结果的规则，以TFLAG:192返回成否鉴定值。0表示剧本侧不干涉COM本体设定，其余值的定义具体参照COMXX。（SKIP 未编译） |
| 25 | `M_KOJO_XXX_EXTRASOURCE_COM_KX_XX` | —（SKIP 未编译） |
| 30 | `M_KOJO_XXX_MESSAGE_MESSAGECHECK_COM_KX_XX` | 做任何事（SKIP 未编译） |
| 35 | `M_KOJO_XXX_MESSAGE_COM_KX_XX` | —（SKIP 未编译） |
| 50 | `M_KOJO_XXX_MESSAGE_COM_KX_40` | 40,跳蛋 |
| 89 | `M_KOJO_XXX_MESSAGE_COM_KX_41` | 41,電動按摩棒 |
| 128 | `M_KOJO_XXX_MESSAGE_COM_KX_42` | 42,陰蒂夾 |
| 167 | `M_KOJO_XXX_MESSAGE_COM_KX_43` | 43,飛機杯 |
| 206 | `M_KOJO_XXX_MESSAGE_COM_KX_44` | 44,振動棒 |
| 250 | `M_KOJO_XXX_MESSAGE_COM_KX_45` | 45,肛用振動棒 |
| 289 | `M_KOJO_XXX_MESSAGE_COM_KX_46` | 46,後庭拉珠 |
| 328 | `M_KOJO_XXX_MESSAGE_COM_KX_47` | 47,乳頭夾 |
| 367 | `M_KOJO_XXX_MESSAGE_COM_KX_48` | 48,搾乳機 |
| 406 | `M_KOJO_XXX_MESSAGE_COM_KX_49` | 49,乳頭跳蛋 |
| 432 | `M_KOJO_XXX_MESSAGE_COM_KX_50` | 50,避孕套装备 |

### M_KOJO_KX_X2_高潮.ERB
*15.9 KB ／ 576 行 ／ 45 个函数*

| 行号 | 函数名 | 用途 |
|---|---|---|
| 72 | `M_KOJO_XXX_MESSAGE_PALAMCNG_MESSAGECHECK_B_KX` | RESULTS:0 = 1时跳过情景文本 / RESULTS:1 = 1时跳过口上文本（SKIP 未编译） |
| 77 | `M_KOJO_XXX_MESSAGE_PALAMCNG_MESSAGECHECK_B2_KX` | —（SKIP 未编译） |
| 82 | `M_KOJO_XXX_MESSAGE_PALAMCNG_MESSAGECHECK_A_KX_00` | —（SKIP 未编译） |
| 87 | `M_KOJO_XXX_MESSAGE_PALAMCNG_MESSAGECHECK_A_KX_0` | —（SKIP 未编译） |
| 92 | `M_KOJO_XXX_MESSAGE_PALAMCNG_MESSAGECHECK_A_KX_1` | —（SKIP 未编译） |
| 97 | `M_KOJO_XXX_MESSAGE_PALAMCNG_MESSAGECHECK_A_KX_2` | —（SKIP 未编译） |
| 102 | `M_KOJO_XXX_MESSAGE_PALAMCNG_MESSAGECHECK_A_KX_3` | —（SKIP 未编译） |
| 107 | `M_KOJO_XXX_MESSAGE_PALAMCNG_MESSAGECHECK_A_KX_4` | —（SKIP 未编译） |
| 112 | `M_KOJO_XXX_MESSAGE_PALAMCNG_MESSAGECHECK_A_KX_5` | —（SKIP 未编译） |
| 117 | `M_KOJO_XXX_MESSAGE_PALAMCNG_MESSAGECHECK_A_KX_6` | —（SKIP 未编译） |
| 122 | `M_KOJO_XXX_MESSAGE_PALAMCNG_MESSAGECHECK_A_KX_7` | —（SKIP 未编译） |
| 127 | `M_KOJO_XXX_MESSAGE_PALAMCNG_MESSAGECHECK_A_KX_8` | —（SKIP 未编译） |
| 132 | `M_KOJO_XXX_MESSAGE_PALAMCNG_MESSAGECHECK_A_KX_9` | —（SKIP 未编译） |
| 137 | `M_KOJO_XXX_MESSAGE_PALAMCNG_MESSAGECHECK_A_KX_20` | —（SKIP 未编译） |
| 142 | `M_KOJO_XXX_MESSAGE_PALAMCNG_MESSAGECHECK_A_KX_21` | —（SKIP 未编译） |
| 147 | `M_KOJO_XXX_MESSAGE_PALAMCNG_MESSAGECHECK_A_KX_22` | —（SKIP 未编译） |
| 152 | `M_KOJO_XXX_MESSAGE_PALAMCNG_MESSAGECHECK_A_KX_23` | —（SKIP 未编译） |
| 157 | `M_KOJO_XXX_MESSAGE_PALAMCNG_MESSAGECHECK_A_KX_26` | —（SKIP 未编译） |
| 168 | `M_KOJO_XXX_MESSAGE_PALAMCNG_B_KX` | @KOJO_MESSAGE_SEND中PALAM类型CASE 2自动调用 / 情景文本PALAM_MESSAGE_B已由@KOJO_MESSAGE_SEND统一调用 |
| 216 | `M_KOJO_XXX_MESSAGE_PALAMCNG_B2_KX` | 对象睡眠中的高潮口上（睡眠奸） / @KOJO_MESSAGE_SEND中PALAM类型CASE 2自动调用（恶作剧时） |
| 264 | `M_KOJO_XXX_MESSAGE_PALAMCNG_A_KX_00` | 射精部位：非TARGET（射精对象不是当前TARGET） / 由TCVAR:50（口上输出用射精部位）Bit位判断调用 |
| 276 | `M_KOJO_XXX_MESSAGE_PALAMCNG_A_KX_0` | 射精部位：避孕套（TCVAR:50 Bit 0） |
| 287 | `M_KOJO_XXX_MESSAGE_PALAMCNG_A_KX_1` | 射精部位：膣内（TCVAR:50 Bit 1） |
| 298 | `M_KOJO_XXX_MESSAGE_PALAMCNG_A_KX_2` | 射精部位：肛内（TCVAR:50 Bit 2） |
| 310 | `M_KOJO_XXX_MESSAGE_PALAMCNG_A_KX_3` | 射精部位：手淫（TCVAR:50 Bit 3） / 指令名称：手淫（COM80） |
| 322 | `M_KOJO_XXX_MESSAGE_PALAMCNG_A_KX_4` | 射精部位：口淫（TCVAR:50 Bit 4） / 指令名称：口交（COM81） |
| 334 | `M_KOJO_XXX_MESSAGE_PALAMCNG_A_KX_5` | 射精部位：乳交（TCVAR:50 Bit 5） / 指令名称：乳交（COM82） |
| 346 | `M_KOJO_XXX_MESSAGE_PALAMCNG_A_KX_6` | 射精部位：素股（TCVAR:50 Bit 6） / 指令名称：素股（COM83） |
| 358 | `M_KOJO_XXX_MESSAGE_PALAMCNG_A_KX_7` | 射精部位：足交（TCVAR:50 Bit 7） / 指令名称：足交（COM85） |
| 370 | `M_KOJO_XXX_MESSAGE_PALAMCNG_A_KX_8` | 射精部位：泡泡浴（TCVAR:50 Bit 8） / 指令名称：泡泡浴（COM84） |
| 382 | `M_KOJO_XXX_MESSAGE_PALAMCNG_A_KX_9` | 射精部位：肛门侍奉（TCVAR:50 Bit 9） / 指令名称：肛门侍奉（COM1145） |
| 394 | `M_KOJO_XXX_MESSAGE_PALAMCNG_A_KX_20` | 射精部位：手淫口交（TCVAR:50 Bit 20） / 指令名称：手淫口交（COM1505） |
| 406 | `M_KOJO_XXX_MESSAGE_PALAMCNG_A_KX_21` | 射精部位：乳夹口交（TCVAR:50 Bit 21） / 指令名称：乳夹口交（COM1512） |
| 418 | `M_KOJO_XXX_MESSAGE_PALAMCNG_A_KX_22` | 射精部位：六九式（TCVAR:50 Bit 22） / 指令名称：六九式（COM1501） |
| 456 | `M_KOJO_XXX_MESSAGE_PALAMCNG_A_KX_23` | 射精部位：深喉插入（TCVAR:50 Bit 23） / 指令名称：深喉插入（COM1140） |
| 468 | `M_KOJO_XXX_MESSAGE_PALAMCNG_A_KX_26` | 射精部位：授乳PLAY（TCVAR:50 Bit 26） / 指令名称：授乳PLAY（COM1519） |
| 482 | `M_KOJO_XXX_MESSAGE_PALAMCNG_A2_KX_0` | 睡眠中玩家射精时的口上（睡眠奸 + Player系） / 射精部位：避孕套 - 睡眠中 |
| 493 | `M_KOJO_XXX_MESSAGE_PALAMCNG_A2_KX_1` | 射精部位：膣内 - 睡眠中 |
| 504 | `M_KOJO_XXX_MESSAGE_PALAMCNG_A2_KX_2` | 射精部位：肛内 - 睡眠中 |
| 515 | `M_KOJO_XXX_MESSAGE_PALAMCNG_A2_KX_3` | 射精部位：手淫 - 睡眠中 |
| 526 | `M_KOJO_XXX_MESSAGE_PALAMCNG_A2_KX_4` | 射精部位：口淫 - 睡眠中 |
| 537 | `M_KOJO_XXX_MESSAGE_PALAMCNG_A2_KX_5` | 射精部位：乳交 - 睡眠中 |
| 548 | `M_KOJO_XXX_MESSAGE_PALAMCNG_A2_KX_7` | 射精部位：足交 - 睡眠中 |
| 559 | `M_KOJO_XXX_MESSAGE_PALAMCNG_A2_KX_23` | 射精部位：深喉插入 - 睡眠中 |
| 570 | `M_KOJO_XXX_MESSAGE_PALAMCNG_F_KX` | 挑逗时的口上 |

### M_KOJO_KX_X2_高潮（详细版）.ERB
*20.6 KB ／ 791 行 ／ 45 个函数*

| 行号 | 函数名 | 用途 |
|---|---|---|
| 67 | `M_KOJO_XXX_MESSAGE_PALAMCNG_MESSAGECHECK_B_KX` | RESULTS:0 = 1时跳过情景文本 / RESULTS:1 = 1时跳过口上文本（SKIP 未编译） |
| 72 | `M_KOJO_XXX_MESSAGE_PALAMCNG_MESSAGECHECK_B2_KX` | —（SKIP 未编译） |
| 77 | `M_KOJO_XXX_MESSAGE_PALAMCNG_MESSAGECHECK_A_KX_00` | —（SKIP 未编译） |
| 82 | `M_KOJO_XXX_MESSAGE_PALAMCNG_MESSAGECHECK_A_KX_0` | —（SKIP 未编译） |
| 87 | `M_KOJO_XXX_MESSAGE_PALAMCNG_MESSAGECHECK_A_KX_1` | —（SKIP 未编译） |
| 92 | `M_KOJO_XXX_MESSAGE_PALAMCNG_MESSAGECHECK_A_KX_2` | —（SKIP 未编译） |
| 97 | `M_KOJO_XXX_MESSAGE_PALAMCNG_MESSAGECHECK_A_KX_3` | —（SKIP 未编译） |
| 102 | `M_KOJO_XXX_MESSAGE_PALAMCNG_MESSAGECHECK_A_KX_4` | —（SKIP 未编译） |
| 107 | `M_KOJO_XXX_MESSAGE_PALAMCNG_MESSAGECHECK_A_KX_5` | —（SKIP 未编译） |
| 112 | `M_KOJO_XXX_MESSAGE_PALAMCNG_MESSAGECHECK_A_KX_6` | —（SKIP 未编译） |
| 117 | `M_KOJO_XXX_MESSAGE_PALAMCNG_MESSAGECHECK_A_KX_7` | —（SKIP 未编译） |
| 122 | `M_KOJO_XXX_MESSAGE_PALAMCNG_MESSAGECHECK_A_KX_8` | —（SKIP 未编译） |
| 127 | `M_KOJO_XXX_MESSAGE_PALAMCNG_MESSAGECHECK_A_KX_9` | —（SKIP 未编译） |
| 132 | `M_KOJO_XXX_MESSAGE_PALAMCNG_MESSAGECHECK_A_KX_20` | —（SKIP 未编译） |
| 137 | `M_KOJO_XXX_MESSAGE_PALAMCNG_MESSAGECHECK_A_KX_21` | —（SKIP 未编译） |
| 142 | `M_KOJO_XXX_MESSAGE_PALAMCNG_MESSAGECHECK_A_KX_22` | —（SKIP 未编译） |
| 147 | `M_KOJO_XXX_MESSAGE_PALAMCNG_MESSAGECHECK_A_KX_23` | —（SKIP 未编译） |
| 152 | `M_KOJO_XXX_MESSAGE_PALAMCNG_MESSAGECHECK_A_KX_26` | —（SKIP 未编译） |
| 163 | `M_KOJO_XXX_MESSAGE_PALAMCNG_B_KX` | @KOJO_MESSAGE_SEND中PALAM类型CASE 2自动调用 / 情景文本PALAM_MESSAGE_B已由@KOJO_MESSAGE_SEND统一调用 |
| 378 | `M_KOJO_XXX_MESSAGE_PALAMCNG_B2_KX` | 对象睡眠中的高潮口上（睡眠奸） / @KOJO_MESSAGE_SEND中PALAM类型CASE 2自动调用（恶作剧时） |
| 478 | `M_KOJO_XXX_MESSAGE_PALAMCNG_A_KX_00` | 射精部位：非TARGET（射精对象不是当前TARGET） / 由TCVAR:50（口上输出用射精部位）Bit位判断调用 |
| 490 | `M_KOJO_XXX_MESSAGE_PALAMCNG_A_KX_0` | 射精部位：避孕套（TCVAR:50 Bit 0） |
| 501 | `M_KOJO_XXX_MESSAGE_PALAMCNG_A_KX_1` | 射精部位：膣内（TCVAR:50 Bit 1） |
| 512 | `M_KOJO_XXX_MESSAGE_PALAMCNG_A_KX_2` | 射精部位：肛内（TCVAR:50 Bit 2） |
| 524 | `M_KOJO_XXX_MESSAGE_PALAMCNG_A_KX_3` | 射精部位：手淫（TCVAR:50 Bit 3） / 指令名称：手淫（COM80） |
| 536 | `M_KOJO_XXX_MESSAGE_PALAMCNG_A_KX_4` | 射精部位：口淫（TCVAR:50 Bit 4） / 指令名称：口交（COM81） |
| 548 | `M_KOJO_XXX_MESSAGE_PALAMCNG_A_KX_5` | 射精部位：乳交（TCVAR:50 Bit 5） / 指令名称：乳交（COM82） |
| 560 | `M_KOJO_XXX_MESSAGE_PALAMCNG_A_KX_6` | 射精部位：素股（TCVAR:50 Bit 6） / 指令名称：素股（COM83） |
| 572 | `M_KOJO_XXX_MESSAGE_PALAMCNG_A_KX_7` | 射精部位：足交（TCVAR:50 Bit 7） / 指令名称：足交（COM85） |
| 584 | `M_KOJO_XXX_MESSAGE_PALAMCNG_A_KX_8` | 射精部位：泡泡浴（TCVAR:50 Bit 8） / 指令名称：泡泡浴（COM84） |
| 596 | `M_KOJO_XXX_MESSAGE_PALAMCNG_A_KX_9` | 射精部位：肛门侍奉（TCVAR:50 Bit 9） / 指令名称：肛门侍奉（COM1145） |
| 608 | `M_KOJO_XXX_MESSAGE_PALAMCNG_A_KX_20` | 射精部位：手淫口交（TCVAR:50 Bit 20） / 指令名称：手淫口交（COM1505） |
| 620 | `M_KOJO_XXX_MESSAGE_PALAMCNG_A_KX_21` | 射精部位：乳夹口交（TCVAR:50 Bit 21） / 指令名称：乳夹口交（COM1512） |
| 632 | `M_KOJO_XXX_MESSAGE_PALAMCNG_A_KX_22` | 射精部位：六九式（TCVAR:50 Bit 22） / 指令名称：六九式（COM1501） |
| 670 | `M_KOJO_XXX_MESSAGE_PALAMCNG_A_KX_23` | 射精部位：深喉插入（TCVAR:50 Bit 23） / 指令名称：深喉插入（COM1140） |
| 682 | `M_KOJO_XXX_MESSAGE_PALAMCNG_A_KX_26` | 射精部位：授乳PLAY（TCVAR:50 Bit 26） / 指令名称：授乳PLAY（COM1519） |
| 696 | `M_KOJO_XXX_MESSAGE_PALAMCNG_A2_KX_0` | 睡眠中玩家射精时的口上（睡眠奸 + Player系） / 射精部位：避孕套 - 睡眠中 |
| 707 | `M_KOJO_XXX_MESSAGE_PALAMCNG_A2_KX_1` | 射精部位：膣内 - 睡眠中 |
| 718 | `M_KOJO_XXX_MESSAGE_PALAMCNG_A2_KX_2` | 射精部位：肛内 - 睡眠中 |
| 729 | `M_KOJO_XXX_MESSAGE_PALAMCNG_A2_KX_3` | 射精部位：手淫 - 睡眠中 |
| 740 | `M_KOJO_XXX_MESSAGE_PALAMCNG_A2_KX_4` | 射精部位：口淫 - 睡眠中 |
| 751 | `M_KOJO_XXX_MESSAGE_PALAMCNG_A2_KX_5` | 射精部位：乳交 - 睡眠中 |
| 762 | `M_KOJO_XXX_MESSAGE_PALAMCNG_A2_KX_7` | 射精部位：足交 - 睡眠中 |
| 773 | `M_KOJO_XXX_MESSAGE_PALAMCNG_A2_KX_23` | 射精部位：深喉插入 - 睡眠中 |
| 785 | `M_KOJO_XXX_MESSAGE_PALAMCNG_F_KX` | 挑逗时的口上 / @KOJO_MESSAGE_SEND中PALAM类型CASE 6自动调用 |




<!-- ========== 以下内容来自 02_places.md ========== -->


# eraTW 地点 ID 对照表

> 由 `BUILD.py` 自动生成。
> `CFLAG:現在位置` 的值 = 地点 ID = `SELECTCASE` 的 `CASE` 值。
> `MAPID = 地点ID / 100`；取地名用 `NAME_FROM_PLACE(CFLAG:現在位置)`。

共 **647** 个地点，分属 12 个地图。

## 地图分段速查

| MAPID | 地图 | ID 段 | 数量 |
|---|---|---|---|
| 0 | 神社 | 1~70 | 70 |
| 1 | 寺 | 101~140 | 40 |
| 2 | 人间之里 | 201~281 | 44 |
| 3 | 湖 | 301~348 | 45 |
| 4 | 竹林 | 401~466 | 60 |
| 5 | 魔法之森 | 501~545 | 34 |
| 6 | 冥界 | 601~655 | 52 |
| 7 | 山麓 | 701~762 | 60 |
| 8 | 山顶 | 801~874 | 60 |
| 9 | 地底 | 901~949 | 43 |
| 10 | 月 | 1001~1072 | 55 |
| 11 | 魔界 | 1101~1186 | 84 |

---

## 0 神社（1~70）

```
1     鸟居   [鳥居]
2     境内
3     功德箱   [賽銭箱]
4     本堂
5     净手池   [手水舎]
6     库房   [物置]
7     土间   [土間]
8     厨房   [台所]
9     起居室   [居間]
10    走廊   [縁側]
11    庭院   [庭]
12    更衣间   [脱衣所]
13    澡堂   [風呂]
14    厕所   [トイレ]
15    灵梦私室   [霊夢私室]
16    破旧小屋   [ボロ小屋]
17    小的仓库   [小さい納戸]
18    壁橱间   [押入れ]
19    大的仓库   [大きい納戸]
20    本殿内部
21    守矢神社分社
22    参道
23    温泉·更衣间   [温泉・脱衣所]
24    温泉
25    镇守之森   [鎮守の森]
26    三妖精之家・入口
27    三妖精之家·大厅   [三妖精の家・広間]
28    三妖精之家・樓梯
29    三妖精之家·厨房   [三妖精の家・台所]
30    三妖精之家·澡堂   [三妖精の家・風呂]
31    三妖精之家·二层走廊   [三妖精の家・二階廊下]
32    桑尼私室   [サニー私室]
33    露娜私室   [ルナ私室]
34    斯塔私室   [スター私室]
35    三妖精之家·地下室   [三妖精の家・地下室]
36    梦幻遗迹前   [夢幻遺跡前]
37    梦幻遗迹·一层廊道   [夢幻遺跡・一階通路]
38    梦幻遗迹·盥洗间   [夢幻遺跡・洗面所]
39    梦幻遗迹·浴室   [夢幻遺跡・浴室]
40    梦幻遗迹·厕所   [夢幻遺跡・トイレ]
41    梦幻遗迹·食堂兼会客厅   [夢幻遺跡・食堂兼談話室]
42    梦幻遗迹·调理室   [夢幻遺跡・調理室]
43    梦美私室   [夢美私室]
44    千百合私室   [ちゆり私室]
45    夢幻遺跡・樓梯
46    梦幻遗迹·二层廊道   [夢幻遺跡・二階通路]
47    梦幻遗迹·舰桥   [夢幻遺跡・艦橋]
48    梦幻遗迹·第一资料室   [夢幻遺跡・第一資料室]
49    梦幻遗迹·研究室   [夢幻遺跡・研究室]
50    梦幻遗迹·第二资料室   [夢幻遺跡・第二資料室]
51    梦幻遗迹·仓库   [夢幻遺跡・倉庫]
52    别馆   [離れ]
53    仓库   [納戸]
54    小人的虫笼   [小人の虫かご]
55    和室
56    阿吽的小屋   [あうんの棲家]
57    大温泉
58    大主卧
59    大厨房
60    大客厅
61    地之间   [地の間]
62    水之间   [水の間]
63    火之间   [火の間]
64    风之间   [风の間]
65    光之间   [光の間]
66    暗之间   [暗の間]
67    宴会厅
68    大广场
69    先代巫女的小屋
70    贝子的暂居处
```

## 1 寺（101~140）

```
101   山门   [山門]
102   境内
103   本堂
104   讲堂   [講堂]
105   经藏   [経蔵]
106   后院   [裏庭]
107   土间   [土間]
108   起居室   [居間]
109   女苑私室
110   走廊   [縁側]
111   厨房   [台所]
112   澡堂   [風呂]
113   纳兹琳私室   [ナズーリン私室]
114   村纱私室   [ムラサ私室]
115   星私室
116   一轮私室   [一輪私室]
117   鵺私室   [ぬえ私室]
118   白莲私室   [白蓮私室]
119   别馆   [離れ]
120   库房   [物置]
121   墓地
122   钟楼   [鐘楼]
123   灵庙大门   [霊廟大門]
124   灵庙广场   [霊廟広場]
125   屠自古私室
126   道场   [道場]
127   布都私室
128   神子私室
129   客房   [客間]
130   走廊   [廊下]
131   枯山水
132   调药室   [調薬室]
133   浴室   [湯殿]
134   藏   [蔵]
135   走廊   [廊下]
136   响子私室   [響子私室]
137   猯藏的小屋   [マミゾウの棲家]
138   钟楼   [鐘楼]
139   邪仙楼
140   地藏小路   [お地蔵通り]
```

## 2 人间之里（201~281）

```
201   人里的门   [人里の門]
202   中央广场   [中央広場]
203   南大街   [南通り]
204   东大街   [東通り]
205   北大街   [北通り]
206   西大街   [西通り]
207   龙神像   [龍神像]
208   雷鼓的房间   [雷鼓の部屋]
209   八桥的房间   [八橋の部屋]
210   弁弁的房间   [弁々の部屋]
211   酒屋
212   咖啡馆   [カフェ]
213   铃奈庵   [鈴奈庵]
214   长屋前   [長屋前]
215   花屋
216   杂货店   [食料品店]
217   甜品店   [甘味所]
218   小料理屋
219   集会所
220   瞭望楼   [物見櫓]
221   稗田邸
222   寺子屋
223   公共浴室   [銭湯]
224   慧音宅
225   情侣酒店   [連れ込み宿]
226   小铃私室   [小鈴私室]
227   蔬菜店   [八百屋]
228   包场浴场   [貸切浴場]
229   阿求私室
230   空的房间   [空き部屋]
231   蛮奇的房间   [蛮奇の部屋]
232   莲子的房间   [蓮子の部屋]
233   梅莉的房间   [メリーの部屋]
234   雪的房间   [ユキの部屋]
235   舞的房间   [マイの部屋]
236   公用厕所   [共同便所]
237   公用水井   [共同井戸]
238   鲵吞亭   [鯢呑亭]
239   美宵的房间   [美宵の部屋]
241   空的房间   [空き部屋]
242   麟的房间
243   空的房间   [空的部屋]
280   警察署
281   小兔姬私室   [小兎姫私室]
```

## 3 湖（301~348）

```
301   正门   [正門]
302   庭院   [庭]
303   守卫小屋   [守衛小屋]
304   空的小屋   [空き小屋]
305   仓库   [納屋]
306   后院   [裏庭]
307   东阳台   [東テラス]
308   西阳台   [西テラス]
309   大厅   [広間]
310   图书馆   [図書館]
311   帕秋莉私室   [パチュリー私室]
312   小恶魔私室   [小悪魔私室]
313   厨房
314   食堂
315   会客厅   [応接間]
316   一层厕所   [一階トイレ]
319   二层走廊   [二階廊下]
320   咲夜私室
321   空的房间   [空き部屋]
322   二层厕所   [二階トイレ]
323   妖精女仆的值班室   [メイド妖精詰め所]
324   大露台   [大バルコニー]
326   蕾米莉亚私室   [レミリア私室]
327   小露台   [小バルコニー]
328   地下走廊   [地下廊下]
329   仓库   [倉庫]
330   佣人间   [使用人部屋]
331   地下室
332   更衣间   [脱衣所]
333   大浴场   [大浴場]
334   废洋馆·入口   [廃洋館・入り口]
335   废洋馆·大厅   [廃洋館・広間]
336   廃洋館・樓梯
337   废洋馆·厨房   [廃洋館・キッチン]
338   废洋馆·澡堂   [廃洋館・風呂]
339   废洋馆·二层走廊   [廃洋館・二階廊下]
340   露娜萨私室   [ルナサ私室]
341   梅露兰私室   [メルラン私室]
342   莉莉卡私室   [リリカ私室]
343   湖畔
344   蕾蒂的冰屋   [レティのかまくら]
345   琪露诺的冰屋   [チルノのかまくら]
346   大妖精宅
347   雾之湖   [霧の湖]
348   雾之湖·湖底   [霧の湖・湖底]
```

## 4 竹林（401~466）

```
401   永远亭入口   [永遠亭入口]
403   等候室   [待合室]
404   诊察室   [診察室]
405   配药室   [調剤室]
406   来客用厕所   [来客用トイレ]
407   走廊   [廊下]
408   中走廊   [中廊下]
409   走廊   [縁側]
410   帝私室   [てゐ私室]
411   铃仙私室   [鈴仙私室]
412   空的房间   [空き部屋]
413   永琳私室
414   辉夜私室   [輝夜私室]
415   大厅   [広間]
416   起居室   [居間]
417   厨房   [台所]
418   厕   [厠]
419   更衣间   [脱衣所]
420   澡堂   [風呂]
421   庭院   [庭]
422   后院   [裏庭]
424   库房   [物置]
426   二层走廊   [二階廊下]
427   仓库   [倉庫]
428   二层空的房间   [二階空き部屋]
430   地下室
431   兔的洞穴   [兎の洞穴]
432   影狼的家   [影狼の家]
433   斜角的竹林   [斜角の竹林]
434   迷失的小道   [迷いの小道]
435   水井   [井戸]
436   无名之丘   [無名の丘]
437   梅蒂欣的家   [メディスンの家]
438   太阳花田   [太陽の畑]
439   拉尔瓦的家   [ラルバの家]
440   废屋   [廃屋]
441   温泉
442   空的小屋   [空き小屋]
443   米斯蒂亚的家   [ミスティアの家]
444   夜雀的小摊   [夜雀の屋台]
445   妹红的家   [妹紅の家]
446   祠
447   竹林入口
450   玄关   [玄関]
451   胡桃私室   [くるみ私室]
452   艾丽私室   [エリー私室]
453   餐厅   [ダイニング]
454   浴室   [バス]
455   厕所   [トイレ]
456   仓库   [倉庫]
457   梦月私室   [夢月私室]
458   走廊   [廊下]
459   幻月私室
460   空的房间   [空き部屋]
461   客厅   [リビング]
462   阳台   [テラス]
463   幽香私室
464   露台   [バルコニー]
465   大堂   [ホール]
466   庭院   [庭]
```

## 5 魔法之森（501~545）

```
501   魔法之森入口   [魔法の森入り口]
502   香霖堂
503   岔道   [分かれ道]
506   无缘冢   [無縁塚]
507   菌菇群生地   [キノコ群生地]
508   魔法之广场   [魔法の広場]
509   再思之道   [再思の道]
510   雾雨魔法店   [霧雨魔法店]
511   魔理沙宅·起居室   [魔理沙宅・居間]
512   魔理沙宅·寝室   [魔理沙宅・寝室]
513   魔理沙宅·研究房间   [魔理沙宅・研究部屋]
514   魔理沙宅·澡堂   [魔理沙宅・風呂]
515   魔理沙宅·仓库   [魔理沙宅・倉庫]
520   人偶洋馆前   [人形の館前]
521   人偶洋馆·爱丽丝的房间   [人形の館・アリスの部屋]
522   人偶洋馆·神绮的房间   [人形の館・神綺の部屋]
523   人偶洋馆·梦子的房间   [人形の館・夢子の部屋]
524   人偶洋馆·研究室   [人形の館・研究室]
525   人偶洋馆·客厅   [人形の館・リビング]
526   人偶洋馆·澡堂   [人形の館・風呂]
528   人偶洋馆·仓库   [人形の館・倉庫]
529   人偶洋馆·露台   [人形の館・バルコニー]
530   人偶洋馆·二层   [人形の館・二階]
531   人偶洋馆·空的房间   [人形の館・空き部屋]
534   轻飘飘的艾伦魔法商店   [ふわふわエレン魔法の店]
535   艾伦宅·寝室   [エレン宅・寝室]
536   艾伦宅·仓库   [エレン宅・倉庫]
537   艾伦宅·澡堂   [エレン宅・風呂]
540   古木的大树   [古木の大樹]
541   朱鹭子的栖息处   [朱鷺子の棲み処]
542   莉格露的栖息处   [リグルの棲み処]
543   露米娅的栖息处   [ルーミアの棲み処]
544   成美的小屋   [成美の小屋]
545   慧之子的栖息处   [慧之子の棲み処,;慧之子の棲息処]
```

## 6 冥界（601~655）

```
601   中有之道   [中有の道]
602   赛河原   [賽の河原]
603   积石冢   [積石塚]
604   彼岸
605   地狱   [地獄]
606   日狭美的家   [日狭美の家,;日狭美的家]
607   残无的家   [残無の家,;残無的家]
608   润美的家   [潤美の家]
609   璎花的家   [瓔花の家]
610   是非曲直厅大堂   [是非曲直庁ホール]
612   法庭   [法廷]
613   是非曲直厅走廊   [是非曲直庁廊下]
614   是非曲直厅等候室   [是非曲直庁ラウンジ]
615   映姬的房间   [映姫の部屋]
616   小町的房间   [小町の部屋]
617   澡堂   [風呂]
618   空的房间   [空き部屋]
620   冥界之门   [冥界の門]
621   庭院   [庭]
622   走廊   [廊下]
623   幽幽子私室   [幽々子私室]
624   妖梦私室   [妖夢私室]
625   空室
626   厨房   [台所]
627   澡堂   [風呂]
628   起居室   [居間]
629   西行妖
630   八云邸玄关   [八雲邸玄関]
631   八云邸走廊   [八雲邸廊下]
632   八云邸庭   [八雲邸庭]
633   紫私室
634   空房间   [空部屋]
635   橙私室
636   八云邸澡堂   [八雲邸風呂]
637   八云邸厨房   [八雲邸台所]
638   蓝私室   [藍私室]
639   八云邸起居室   [八雲邸居間]
640   异界的关卡   [異界の関所]
641   畜生界大都市   [畜生メトロポリス]
642   灵长园   [霊長園]
643   灵长园的澡堂   [霊長園の風呂]
644   袿姬的房间   [袿姫の部屋]
645   磨弓的房间   [磨弓の部屋]
646   八千慧宅的澡堂   [八千慧宅の風呂]
647   八千慧宅的客厅   [八千慧宅のリビング]
648   八千慧宅的寝室   [八千慧宅の寝室]
650   早鬼宅的客厅   [早鬼宅のリビング]
651   早鬼宅的寝室   [早鬼宅の寝室]
652   早鬼宅的澡堂   [早鬼宅の風呂]
653   尤魔宅的客厅   [尤魔宅のリビング]
654   尤魔宅的寝室   [尤魔宅の寝室]
655   尤魔宅的澡堂   [尤魔宅の風呂]
```

## 7 山麓（701~762）

```
701   树海道入口   [樹海道入り口]
702   山道·通往沼泽之道   [山道・沢へ続く道]
703   玄武之泽   [玄武の沢]
704   河童的宣传站   [河童のアジト]
705   山道·中腹   [山道・中腹]
706   厄神的家   [厄神の家]
707   山道·分岐点   [山道・分岐点]
708   大蛤蟆之池   [大蝦蟇の池]
709   莉莉们的家   [リリーたちの家]
710   猫之里   [猫の里]
711   休憩所
712   间歇泉地下中枢   [間欠泉地下センター]
715   秋姊妹的家·畑   [秋姉妹の家・畑]
716   秋姊妹的家·土间   [秋姉妹の家・土間]
717   秋姊妹的家·寝室   [秋姉妹の家・寝室]
718   秋姊妹的家·客厅   [秋姉妹の家・居間]
719   秋姊妹的家·和室   [秋姉妹の家・座敷]
720   仙人的宅邸·厨房   [仙人の屋敷・台所]
721   仙人的宅邸·澡堂   [仙人の屋敷・風呂]
722   仙人的宅邸·道场   [仙人の屋敷・道場]
723   仙人的宅邸·二层客厅   [仙人の屋敷・二階客間]
724   仙人的宅邸·书斋   [仙人の屋敷・書斎]
725   仙人的宅邸·大鹫的房间   [仙人の屋敷・大鷲の部屋]
726   仙人的宅邸·起居室   [仙人の屋敷・居間]
727   仙人的宅邸·华扇私室   [仙人の屋敷・華扇私室]
728   仙人的宅邸·空的房间   [仙人の屋敷・空き部屋]
729   仙人的宅邸·玄关   [仙人の屋敷・玄関]
730   仙人的宅邸·庭   [仙人の屋敷・庭]
731   帚木
732   通向山顶的路   [山頂への道]
733   正邪的藏身处   [正邪の隠れ家]
734   小屋
735   淋浴区   [水浴び場]
736   圣域入口
737   招财猫的家   [招き猫の家]
738   森林深处   [森の深奥]
739   秘天崖
740   山童的宣传站   [山童のアジト]
741   猿猴通路
742   美天居所
743   圣域深林道
744   合欢宅邸
745   月都秘道
746   姥芽大宅
747   圣域深道
748   魑魅的草棚
749   山中密道
750   驯子的小屋
751   浅间净秽山
752   四季竖穴
753   浅间的房间
754   空房间
755   化石丛林荒地
756   月海通路
757   巧克力河
758   化石深道
759   磐永神社本殿
760   磐永神社内屋
761   浴室
762   空房间
```

## 8 山顶（801~874）

```
801   山顶入口   [山頂入り口]
802   桥   [橋]
803   索道站   [索道駅]
804   守矢神社鸟居   [守矢神社鳥居]
805   顶上   [頂上]
806   瀑布背面   [滝の裏]
807   椛宅
808   文宅
809   果宅
810   山小屋
811   境内
812   本殿
813   社务所   [社務所]
814   湖畔
815   庭院   [庭]
816   走廊   [縁側]
817   神奈子私室
818   诹访子私室   [諏訪子私室]
819   起居室   [居間]
820   早苗私室
821   土间   [土間]
822   厨房   [台所]
823   空室
824   厕所   [トイレ]
825   澡堂   [風呂]
826   走廊   [廊下]
830   玄云海   [玄雲海]
831   比那名居邸前
832   有顶天街   [有頂天街]
833   桃园   [桃園]
834   比那名居邸土间   [比那名居邸土間]
835   比那名居邸会客厅   [比那名居邸応接間]
836   比那名居邸厨房
837   比那名居邸澡堂   [比那名居邸風呂]
838   比那名居邸客厅   [比那名居邸居間]
839   比那名居邸和室
840   天子私室
841   衣玖私室
842   比那名居邸库房   [比那名居邸物置]
851   久侘歌的小屋   [久侘歌の小屋]
852   驹草的小屋   [駒草の小屋]
853   魅须丸的小屋   [魅須丸の小屋]
854   龙宅前院
855   虹龙洞   [虹龍洞]
856   百百世的住所   [百々世の住処]
860   龙宅一楼走廊
861   龙宅客厅
862   龙宅餐厅
863   龙宅厨房
864   龙宅厕所
865   龙宅客卧
866   龙宅一楼浴室
867   后院
868   龙宅二楼走廊
869   龙宅客卧
870   龙宅二楼卫浴
871   工作间
872   典的卧室
873   龙的卧室
874   大露台
```

## 9 地底（901~949）

```
901   地灵殿前   [地霊殿前]
904   大客厅   [大広間]
905   一层走廊   [一階廊下]
906   一层厕所   [一階トイレ]
909   厨房
910   食料库   [食料庫]
911   阿空私室   [お空私室]
912   阿燐私室   [お燐私室]
913   食堂
914   二层走廊   [二階廊下]
915   露台   [バルコニー]
916   库房   [物置]
917   二层厕所   [二階トイレ]
918   恋私室   [こいし私室]
919   觉私室   [さとり私室]
920   书斋   [書斎]
921   澡堂   [風呂]
922   更衣间   [脱衣所]
923   后院   [裏庭]
925   薔薇园   [バラ園]
926   中庭
928   灼热地狱遗迹   [灼熱地獄跡]
929   地狱的人工太阳   [地獄の人工太陽]
930   旧血池地狱   [旧血の池地獄]
931   大街   [大通り]
932   后街   [裏通り]
933   酒场   [酒場]
934   温泉
935   情人旅馆   [ラブホ]
936   勇仪的家   [勇儀の家]
937   空屋   [空き屋]
938   鬼的聚集场所   [鬼の溜まり場]
939   小胡同   [路地裏]
940   帕露西的家   [パルスィの家]
941   山女的家   [ヤマメの家]
942   琪斯美的家   [キスメの家]
943   茅屋   [あばら屋]
944   街道   [通り]
945   河岸   [川岸]
946   桥   [橋]
947   血枪的栖息处   [ちやりの棲み処,;ちやりの棲息処,;原 地藏 一直未调用]
948   竖井底部   [縦穴の底]
949   托卡马克装置核心
```

## 10 月（1001~1072）

```
1001  槐安通路
1002  月之都
1003  玉兔街
1004  广场
1005  探女宅·起居室
1006  探女宅·寝室
1007  闲置的房子
1008  铃瑚宅
1009  清兰宅
1010  饭店
1011  甜品店
1012  酒屋
1013  蔬菜店
1014  桃林
1015  沙滩
1016  入海口
1020  绵月亭·门
1021  绵月亭·玄关
1022  一层回廊
1023  门卫值班室
1024  玉兔食堂
1025  玉兔值班室
1026  食堂
1027  厨房
1028  食料库
1029  绵月亭·更衣间
1030  绵月亭·澡堂
1031  宝物库
1032  铃仙二号私室
1033  绵月亭·空的房间
1035  中庭
1036  凉亭
1040  二层回廊
1041  丰姬私室
1042  依姬私室
1043  书斋
1044  会客厅
1050  哆来咪宅·起居室
1051  哆来咪宅·寝室
1052  哆来咪宅·仓库
1053  哆来咪宅·盥洗间
1054  哆来咪宅·澡堂
1055  哆来咪宅·厕所
1060  纯狐邸·玄关
1061  起居室
1062  厨房
1063  纯狐邸·空的房间
1064  克劳恩皮丝私室
1065  库房
1066  纯狐邸·更衣间
1067  纯狐邸·澡堂
1068  纯狐邸·中庭
1070  屋顶
1071  纯狐私室
1072  赫卡提亚私室
```

## 11 魔界（1101~1186）

```
1101  传送点
1102  萨拉的小屋
1103  萨拉的小屋·浴室
1104  万魔殿·仿
1105  黄昏街
1106  魔界商贸城
1107  星辰之家外
1108  先知环形路
1109  智者写字楼外
1110  流光巷
1111  渡鸦小区·小路
1112  船夫别墅区
1113  别墅区·闲置的冈崎宅
1114  别墅区·闲置的风见宅
1115  别墅区·闲置的怨灵宅
1116  星辰之家·5F电梯口
1117  星辰之家·5F走廊
1118  雪的公寓
1119  雪的公寓·浴室
1120  舞的公寓
1121  舞的公寓·浴室
1122  空屋子
1123  空浴室
1124  奥莲姬的公寓
1125  奥莲姬的公寓·浴室
1126  里香的公寓
1127  里香的公寓·浴室
1128  露易兹的公寓
1129  露易兹的公寓·浴室
1130  智者写字楼·3F走廊
1131  朝仓研究室·准备室
1132  朝仓研究室·无菌室
1133  朝仓研究室·走廊
1134  朝仓研究室·总实验室
1135  朝仓研究室·数据处理室
1136  朝仓研究室·储存室
1137  理香子的小屋
1138  理香子的小屋·浴室
1139  渡鸦小区·6F电梯口
1140  渡鸦小区·6F走廊
1141  明罗宅·道场
1142  明罗宅·厨房
1143  明罗宅·卧室
1144  明罗宅·浴室
1145  魔眼宅·仪式间
1146  魔眼宅·厨房
1147  魔眼宅·卧室
1148  魔眼宅·浴室
1149  矜羯罗宅·练功房
1150  矜羯罗宅·厨房
1151  矜羯罗宅·卧室
1152  矜羯罗宅·浴室
1153  万魔殿·庭院
1154  万魔殿·大厅
1155  万魔殿·一层左走廊
1156  万魔殿·厨房
1157  万魔殿·饭堂
1158  万魔殿·一层右走廊
1159  万魔殿·菜园
1160  万魔殿·中控室
1161  万魔殿·会客厅
1162  万魔殿·二层左走廊
1163  万魔殿·二层右走廊
1164  万魔殿·宴会厅
1165  万魔殿·梦子卧室
1166  万魔殿·大浴室
1167  万魔殿·神绮卧室
1168  万魔殿·空屋
1169  万魔殿·传送点
1170  万魔殿·闲置的爱丽丝卧室
1173  堕落神殿·殿外
1174  堕落神殿·主教堂
1175  堕落神殿·会客室
1176  堕落神殿·厨房
1177  堕落神殿·二楼走廊
1178  堕落神殿·厕所
1179  堕落神殿·浴室
1180  堕落神殿·依莉斯的卧室
1181  堕落神殿·萨丽爱尔的卧室
1182  冰雪世界·冰原
1183  冰雪世界·冰湖
1184  法界
1185  空屋子
1186  空浴室
```
