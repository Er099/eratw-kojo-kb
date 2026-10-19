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

1. **不自己造模板**。函数名、变量位、`SELECTCASE`、`FIRSTTIME`、`CD`、各种 `MESSAGE`/`SUCCESS` 函数，一律以游戏模板或用户已有代码为准。
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

> **完整派发机制、43 种钩子函数、颜色常量、4.980 拦截器 → `09_kojo_framework.md`**
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
| `FLAG:561` | 561 | 精力超群叠加次数 |
| `CSTR:147:処女喪失履歴` | 46 | 处女丧失履历（**不要用 CSTR:1**，那是每日重置的 ONCE） |

**新写口上想加自己的状态位**：
- 官方给口上预留 `TCVAR:350~399`（`TCVAR.csv` 原文「口上用確保領域」），已被占：`350`、`354~357`、`361`、`363`
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
PRINTANY 变量        ; 自动判断数值/字符串
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

- 按 `/` 切分后**等概率**随机取一个，最多 7 段（多余的忽略）
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
CD 变量, 时间             ; 冷却时间
CALL 函数(参数)
CALLEVENT 函数
TRYCALL 函数              ; 函数不存在也不报错（直接跳过）
TRYCALLFORM 格式串        ; 同上，函数名可带 %变量%
TRYCCALLFORM 格式串       ; 函数不存在时进入 CATCH 块（更高级）
CALLFORM 格式串
SIF 条件                  ; 单行 IF（只作用于下一行）
```

> `TRY` 系和 `TRYC` 系的区别：`TRYCALL` 找不到函数就**跳过**；`TRYCCALL` 找不到就**跳到 `CATCH` 块**。eraTW 框架用 `TRYCCALLFORM` 派发口上函数，用 `TRYCALLFORM` 调用可能不存在的可选函数。

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
- 省略参数：数值补 `0`、字符串补 `""`（仅对 `#DIM` 私有变量做参数时成立）
- **类型不自动转换**：数值传进字符串参数会直接报错
- 字符串字面量 `"..."`；格式化字符串 `@"..."`
- 可变长参数：函数声明加 `VARIADIC`，用 `ARGLEN` 取个数、`ARG:0..6` 取值 —— eraTW 的 `TEXTR` 就是这么写的

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
| `STRTRIM(s)` | 去首尾空白 |
| `CHARAT(s, i)` / `UNICODE(s, i)` | 第 i 个字符 / 其码点 |
| `ENCODETOUNI(s)` | 字符串 → Unicode 码点数组 |
| `GETNUM(s, n)` | 取第 n 段（按 `,` 分） |
| `SPLIT 源, 分隔符, 数组, 数量` | **命令**，切分到数组，数量存进第 4 参数 |

### 4.13 数组与批量赋值

```erb
A:10 = 1,2,3              ; 批量赋值，从下标 10 开始
VARSET 变量, 值, 起, 终    ; 批量填充
VARSET CFLAG:ARG:0, 0, 1000, 2000   ; @RESET_CHARA 的写法
SWAP A, B                 ; 交换
ERASE 数组                ; 清空
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
TWAIT 3000           ; 最多等 3 秒
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
| 13 | 奉仕精神 |
| 42 | 戦闘能力 |
| 43 | 教養 |
| 44 | 料理技能 |
| 45 | 音楽技能 |
| 55 | 肛门 |
| 56 | 欲望 |

> ⚠️ 素质是「感**度**」（`TALENT:Ｖ感度`），能力是「感**覚**」（`ABL:Ｖ感覚`）——两个字不同，别写错。

### 5.3 EXP（经验）

`絶頂経験` / `放尿経験` / `Ｖ性交経験` / `Ａ性交経験` / `自慰経験` / `挿入経験` / `苦痛快楽` / `異常経験` / `Ｖ拡張` / `緊縛` —— 全部 0 起累加。

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
| 16 | 以为 602「约会接吻」能用 | 本版**未实装**（`Train.csv` 无 600/601/602）。接吻用 `19`/`20`/`312`/`SCOMF63` |
| 17 | 以为散步是 694 | 是 **604**（`Train.csv: 604,散步`） |
| 18 | `PRINTDATADW 文本` | `PRINTDATA` 系列**不收参数**，`PRINTDATADW` 后面必须直接跟 `DATA`/`DATAFORM`，否则编译报错。要整句文本请用 `PRINTFORMDW` |
| 19 | `%TEXTR("默默/静静的/_")%` 用半角 `_` | 只有**全角 `＿`** 会被转成空串，半角 `_` 会原样显示 |
| 20 | 以为 `DATA`/`DATAFORM` 会依次全显示 | 顶层各项是**等概率选一个**，想全显示要拆块或改用 `DATALIST` |
| 18 | `TALENT:胸围` 和 `BASE:胸围` 混用 | 前者是等级（-2~2），后者是 cm 数值 |

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
| `09_kojo_framework.md` | ~11 KB | 口上派发机制、43 种钩子、MESSAGECHECK、颜色常量、4.980 拦截器 |

**只发 00 就能开工**，01~04、06~09 是按需补充。

- 素材更新后跑 `BUILD.py` 重新生成 01/02/03。
- Emuera 官方文档更新后跑 `EMUERA_KB_SYNC.py` 重新生成 04/05。
- 游戏本体更新后跑 `ERATW_SOURCE_INDEX.py` 重新生成 06/07/08。

---

*本包内容来自：`AI交接说明.txt`、eraTW 4.981 源码实测、Emuera 官方文档（qirchen421.github.io/emuera.sk.doc）全 387 篇、以及本项目历次踩坑记录。*
