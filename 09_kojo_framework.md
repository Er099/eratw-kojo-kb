# eraTW 口上框架 · 派发机制与钩子全表

> 数据源：`ERB/口上・メッセージ関連/COMMON_KOJO.ERB`、`KOJO_MESSAGE.ERB`、`ERB/DIM.ERH`、`DLC/实用设置补丁/KOJO_Preset.ERB`
> 版本：4.981 系（含 4.980 拦截器）。本文所有结论都对着源码核实过。

---

## 0. 最重要的一条

口上就是**一堆名字必须完全正确的函数**。框架用 `TRYCALLFORM` 拼出函数名去调：

```erb
TRYCALLFORM M_KOJO%KOJO_NAME%_MESSAGE_COM_K{NO:TARGET}_{LOCAL}
```

`TRYCALLFORM` 的特性是**函数不存在就静默跳过**。所以：

> 名字写错一个字符 → 函数永远不被调用 → 玩家看不到 → **编译不报错、运行不报错、日志也没有**。

这是口上制作里最难查的一类 bug。**改完口上，必须进游戏实测触发那一条指令**，不能只看编译通过。

---

## 1. 派发链

```
玩家选指令
  → 指令实现（COMFxxx.ERB）
    → @KOJO_MESSAGE_SEND("COM", 0, TARGET, ...)
      → 读口上标识符 KOJO_NAME
        → TRYCALLFORM M_KOJO{KOJO_NAME}_MESSAGE_COM_K{NO}_{指令号}
          → 你的口上函数
```

`KOJO_MESSAGE_SEND` 的签名（`KOJO_MESSAGE.ERB:17`）：

```erb
@KOJO_MESSAGE_SEND(ARGS, ARG:1, ARG:2, ARG:3, ARG:4, ARGS:1, ARGS:2, ARG:5, ARG:6, OVERRIDE_TARGET = -1)
```

第一个参数是类别字符串（`"COM"` / `"SCOM"` / …），框架用它拼 `M_KOJO_{ID}_MESSAGE_{类别}_K{NO}_{编号}`。

---

## 2. 入口函数：口上标识符

每个口上必须有一个入口函数，框架靠它确认「这个角色有没有口上、口上叫什么」。

**147 的实际写法**（`147 Sariel [サリエル]/事件.ERB:9`）：

```erb
@M_KOJO_K147(ARG)
#LOCALSIZE 1
#LOCALSSIZE 1
RESULTS = _147        ; ← 口上标识符，注意前面有下划线
RESULTS:1 = 初版      ; ← 版本名
RETURN 1
```

| 要设的 | 含义 | 注意 |
|---|---|---|
| `RESULTS` | 口上标识符 | **必须是 `_147` 这种带前导下划线的形式**。因为框架拼的是 `M_KOJO%RESULTS%_...`，`_147` 拼出 `M_KOJO_147_...` |
| `RESULTS:1` | 版本名 | 显示在口上列表里，如「初版」 |
| `RESULTS:2` | 简介 | 可选，支持 `<br>` |
| `RETURN 1` | 口上存在 | **不能返回 0** |

框架侧的读取逻辑（`COMMON_KOJO.ERB:14`）：

```erb
@KOJO_ACTIVE_INFO(ARG)
RESULT = 0
RESULTS =
IF CFLAG:ARG:口上セレクタ
    TRYCALLFORM M_KOJO_K{NO:ARG}_{CFLAG:ARG:口上セレクタ}
ELSE
    TRYCALLFORM M_KOJO_K{NO:ARG}
ENDIF
SIF RESULTS:1 == ""
    RESULTS:1 = 初始
KOJO_ACTIVE_NAME:ARG = %RESULTS%
```

---

## 3. 口上选择器：CFLAG:998

`CFLAG:角色:口上セレクタ`（= **CFLAG:998**）存的是「这个角色用第几套口上」。

| 值 | 框架拼的函数名 | 含义 |
|---|---|---|
| 0 | `@M_KOJO_K147` | 默认口上 |
| 1 | `@M_KOJO_K147_1` | 第二套 |
| 2 | `@M_KOJO_K147_2` | 第三套 |

- 想做「另一个版本的口上」，入口函数写 `@M_KOJO_K147_1`，其余钩子同样加 `_1` 后缀
- 玩家侧由 `DLC/实用设置补丁/KOJO_Preset.ERB` 的剧本预设系统切换（栏位 0~9 自定义、10~19 内置推荐）
- ⚠️ **不要自己乱写 `CFLAG:998`**，那是框架和 DLC 共用的槽位

---

## 4. 钩子函数全表

`{ID}` = 口上标识符（147 口上是 `147`），`{NO}` = 角色定义编号，`{N}` = 指令/事件编号。

### 4.1 元信息与初始化

| 函数 | 时机 / 作用 |
|---|---|
| `@M_KOJO_K{NO}` | 入口，设置口上标识符 |
| `@M_KOJO_{ID}_COLOR_K{NO}` | 口上色，内部 `SETCOLOR 0xXXXXXX` |
| `@M_KOJO_{ID}_FLAGSETTING_K{NO}` | 开局一次性改素质（配合 `FIRSTTIME`） |
| `@M_KOJO_{ID}_CHECK_K{NO}_{ARGS}` | 口上存在性检查 |

### 4.2 指令类（最常写）

| 函数 | 说明 |
|---|---|
| `@M_KOJO_{ID}_MESSAGE_COM_K{NO}_{N}` | **普通指令**，N = `Train.csv` 编号（如 604 散步） |
| `@M_KOJO_{ID}_MESSAGE_SCOM_K{NO}_{N}` | **性交系指令** |
| `@M_KOJO_{ID}_MESSAGE_COM_K{NO}_DANMAKU` | 弹幕指令（特殊） |

> 指令编号见 `08_command_index.md`。编号**不连续**，被注释掉的旧编号无效。

### 4.3 事件类

| 函数 | 说明 |
|---|---|
| `@M_KOJO_{ID}_DAILY_EVENT_K{NO}_{N}` | 每日事件 |
| `@M_KOJO_{ID}_EVENT_K{NO}_{N}` | 通用事件（N 可以是 `26_1`、`GIFT`、`PANCHIRA`、`GRAVITY` 这类字符串） |
| `@M_KOJO_{ID}_CUSTOM_EVENT_K{NO}_{N}` | 自定义事件 |
| `@M_KOJO_{ID}_SPEVENT_K{NO}_{N}` | 特殊事件 |
| `@M_KOJO_{ID}_ENCOUNTER_K{NO}` | 遭遇 |
| `@M_KOJO_{ID}_IRAI_K{NO}` | 委托 |
| `@M_KOJO_{ID}_MESSAGE_ENDING_K{NO}` | 结局 |

### 4.4 状态变化

| 函数 | 说明 |
|---|---|
| `@M_KOJO_{ID}_MESSAGE_PALAMCNG_B_K{NO}` | 参数变化 B 段 |
| `@M_KOJO_{ID}_MESSAGE_PALAMCNG_B2_K{NO}` | B2 段 |
| `@M_KOJO_{ID}_MESSAGE_PALAMCNG_C_K{NO}` | C 段 |
| `@M_KOJO_{ID}_MESSAGE_PALAMCNG_D_K{NO}` | D 段 |
| `@M_KOJO_{ID}_MESSAGE_PALAMCNG_E_K{NO}` | E 段 |
| `@M_KOJO_{ID}_MESSAGE_PALAMCNG_F_K{NO}` | F 段 |
| `@M_KOJO_{ID}_MESSAGE_MARKCNG_K{NO}` | 刻印变化 |
| `@M_KOJO_{ID}_MESSAGE_COUNTER_K{NO}_{TCVAR:20}` | 计数类（`TCVAR:20` 是计数器编号） |

### 4.5 结果 / 额外资源 / 覆盖

| 函数 | 说明 |
|---|---|
| `@M_KOJO_{ID}_SUCCESS_K{NO}` | 成功（通用） |
| `@M_KOJO_{ID}_SUCCESS_{LOCALS}_K{NO}_{LOCAL}` | 成功（按类别） |
| `@M_KOJO_{ID}_EXTRASOURCE_{LOCALS}_K{NO}_{LOCAL}` | 额外文本来源 |
| `@M_KOJO_{ID}_OVERRIDE_{LOCALS}_K{NO}_{LOCAL}` | 覆盖默认文本 |

> `{LOCALS}` 是类别字符串变量（`COM` / `SCOM` / `CUSTOM_COM` / `CUSTOM_SCOM`），`{LOCAL}` 是对应编号。

---

## 5. MESSAGECHECK：屏蔽系统文本

几乎每个钩子都配一个 `..._MESSAGECHECK_...` 函数。它返回一个**位掩码**，决定这次要不要显示系统默认文本 / 口上文本。

```erb
@M_KOJO_147_MESSAGE_MESSAGECHECK_COM_K147_604
#LOCALSIZE 1
#LOCALSSIZE 1
RESULT = 0        ; 默认：都显示
RETURN 1
```

> 命名顺序是 `M_KOJO{ID}_MESSAGE_MESSAGECHECK_{类别}_K{NO}_{编号}`，
> **`MESSAGECHECK` 在类别前面**，别写成 `MESSAGE_COM_MESSAGECHECK`。
> 实例：`@M_KOJO_YURI百合_MESSAGE_MESSAGECHECK_COM_K1_60`（灵梦百合口上）

框架侧（`KOJO_MESSAGE.ERB:246`）：

```erb
SKIP_MESSAGE = GETBIT(RESULT, 0)   ; bit0 = 屏蔽系统文本
SKIP_KOJO    = GETBIT(RESULT, 1)   ; bit1 = 屏蔽口上文本
```

| RESULT | bit0 | bit1 | 效果 |
|---:|---|---|---|
| 0 | 0 | 0 | 系统文本 + 口上都显示（默认） |
| 1 | 1 | 0 | **只显示口上**（最常用：想让自己的描写替代系统那行） |
| 2 | 0 | 1 | 只显示系统文本 |
| 3 | 1 | 1 | 全屏蔽 |

写法：

```erb
RESULT = 0
SETBIT RESULT, 0     ; 屏蔽系统文本
RETURN 1
```

> ⚠️ 别把 `MESSAGECHECK` 当布尔用。它返回的是掩码，`RETURN 1` 和 `RESULT = 1` 是两回事——**`RETURN 1` 只表示「函数存在」，屏蔽哪部分是 `RESULT` 决定的**。

---

## 6. 返回值语义（三个函数三种意思）

| 函数 | `RETURN 1` | `RETURN 0` |
|---|---|---|
| `@M_KOJO_K{NO}`（入口） | 口上存在 | **口上会被当成不存在** |
| `@M_KOJO_..._MESSAGE_COM_...`（正文） | 已输出文本，跳过自动娇喘兜底 | 触发框架的自动兜底文本 |
| `@M_KOJO_..._MESSAGECHECK_...` | 检查函数存在 | — |

> 正文函数写完一定要 `RETURN 1`。写 `RETURN 0` 会出现「你写的文本 + 系统自动补一句娇喘」的重复。

---

## 7. 颜色常量（`ERB/DIM.ERH:689` 起）

直接写 `SETCOLOR C_RED` 即可，不用记十六进制。

| 常量 | 值 | 常量 | 值 |
|---|---|---|---|
| `C_GREEN` | `0x00FF00` | `C_RED` | `0xFF0000` |
| `C_P_GREEN` | `0x70C070` | `C_D_RED` | `0x990000` |
| `C_L_GREEN` | `0x90EE90` | `C_P_RED` | `0xC07070` |
| `C_TEAL` | `0x008080` | `C_BLUE` | `0x0000FF` |
| `C_M_GREEN` | `0x00FA9A` | `C_AQUA` | `0x66FFFF` |
| `C_YELLOW` | `0xFFFF00` | `C_P_BLUE` | `0x7070C0` |
| `C_P_YELLOW` | `0x505020` | `C_ROYAL_BLUE` | `0x4169E1` |
| `C_CREAM` | `0xFFFFCC` | `C_N_BLUE` | `0x0078B4` |
| `C_ORANGE` | `0xFFA500` | `C_S_BLUE` | `0xA0D2FF` |
| `C_D_ORANGE` | `0xFF6400` | `C_WHITE` | `0xC0C0C0` |
| `C_GRAY` | `0x404040` | `C_L_GRAY` | `0x777777` |
| `C_BLACK` | `0x000000` | `C_GRAY2` | `0x888E7E` |
| `C_PINK` | `0xFFCCFF` | `C_D_PINK` | `0x990099` |
| `C_H_PINK` | `0xFF69B4` | `C_V_PINK` | `0xFF00FF` |
| `C_HEARTPINK` | `0xFFC0CB` | `C_DIM_PINK` | `0xFFAAFF` |
| `C_PURPLE` | `0xCC99FF` | `C_D_PURPLE` | `0x622C99` |
| `C_P_PURPLE` | `0xC070C0` | `C_PURE_WHITE` | `0xFFFFFF` |

专用色（语义色，别乱用）：

| 常量 | 值 | 用途 |
|---|---|---|
| `C_LVUPOK` | `0xFF8C00` | 升级 |
| `C_ORGASM` | `0xFFB400` | 绝顶 |
| `C_FEMORGASM` | `0xFF68DE` | 女性绝顶 |
| `C_F_VIRGIN` | `0xFF78C8` | 女性处女 |
| `C_F_VIRGINLOSS` | `0xF7ABA6` | 女性破瓜 |
| `C_M_VIRGINLOSS` | `0xFF64FF` | 男性童贞丧失 |

---

## 8. KOJO_FUNCCHECK：给 `#FUNCTION` 用的口上接口

`#FUNCTION` 里不能 `CALL`，所以框架提供了 `GETMETH` 桥（`COMMON_KOJO.ERB:43`）：

```erb
RETURNF GETMETH(@"M_KOJO%KOJO_ACTIVE_NAME:CHARA%_FUNCCHECK_K{NO:CHARA}_%SUBTYPE%", 0, , ARG, ARG:1)
```

口上侧要写：

```erb
@M_KOJO_147_FUNCCHECK_K147_ALCOHOL_TASTE(ARG, ARG:1)
#FUNCTION
RETURNF 1
```

> 命名 = `M_KOJO` + **`RESULTS` 的完整值**（`_147`，含前导下划线）+ `_FUNCCHECK_K{NO}_{子类型}`
> → 拼出来是 `M_KOJO_147_FUNCCHECK_K147_ALCOHOL_TASTE`。
> 如果 `RESULTS` 设成别的字符串（如 `YURI百合`），这里也要跟着变。
> 该机制在 4.981 里还没有人口上实际使用，属于预留接口。

配套数组 `KOJO_FUNCCHECK_OP`（`KOJO_MESSAGE.ERH`）用来控制返回语义，每次调用前会被清零。

---

## 9. 4.980 拦截器

`KOJO_MESSAGE.ERB:238` 有一段优先拦截：

```erb
RESULT = 拦截器未激活
TRYCCALLFORM M_KOJO%KOJO_NAME%_MESSAGE_MESSAGECHECK_PRI_GENERAL_K{NO:TARGET}(LOCAL, LOCALS)
CATCH
    RESULT = 拦截器未激活
ENDCATCH
IF RESULT == 拦截器未激活
    RESULT = 0
    TRYCALLFORM M_KOJO%KOJO_NAME%_MESSAGE_MESSAGECHECK_%LOCALS%_K{NO:TARGET}_{LOCAL}
ENDIF
```

- 写了 `_PRI_GENERAL_` 版本，就**优先**走它；不写则退回普通 MESSAGECHECK
- 用 `TRYCCALLFORM`（带 CATCH），所以函数不存在不会报错
- 拦截器可以**整体接管**某类指令的文本，连 MESSAGECHECK 一起绕过

---

## 10. 写口上前的自查清单

- [ ] 入口 `@M_KOJO_K147` 里 `RESULTS = _147`（带下划线）、`RETURN 1`
- [ ] 钩子函数名里的编号是**角色定义编号**（147），不是 `NO:` 运行时编号
- [ ] 指令号来自 `08_command_index.md`，不是自己猜的
- [ ] 正文函数结尾 `RETURN 1`
- [ ] 用了 `MESSAGECHECK` 的话，`RESULT` 用位掩码（`SETBIT RESULT, 0`），不是 `RETURN 1`
- [ ] 颜色用 `C_xxx` 常量，不是手写十六进制
- [ ] 变量名在 `06_variable_names.md` 里查得到（或者直接用编号）
- [ ] **进游戏实际触发一次**，确认文本出现

---

*本文由源码提取 + 人工核实，与 `00_core.md` 第 3 章配合使用。*
