# eraTW 口上知识库 · 使用说明

一套**可携带**的 AI 上下文包。换任何 AI（DeepSeek / Kimi / 通义 / 豆包 / ChatGPT / Claude …），
只要发一个文件，它就能直接接手萨丽艾尔（147）口上的编写工作，**不用再传游戏源码**。

> **在线仓库**：https://github.com/Er099/eratw-kojo-kb
> **给 AI 的链接（首选，国内可用）**：https://er099.github.io/eratw-kojo-kb/00_core.md
> **备用（国内，有 12h 缓存）**：https://cdn.jsdelivr.net/gh/Er099/eratw-kojo-kb@main/00_core.md
> **国外网络**：https://raw.githubusercontent.com/Er099/eratw-kojo-kb/main/00_core.md （⚠️ 国内完全不通）
>
> 👉 **第一次用请先看 [HOWTO.md](HOWTO.md)** —— 保姆级操作教程（开联网、发什么话、怎么验收、常见问题）

---

## 文件清单

| 文件 | 大小 | 作用 | 什么时候发 |
|---|---|---|---|
| **00_core.md** | 34 KB | 规则 + 框架机制 + **Emuera 语法全章（4.1~4.16）** + 变量编号 + 代码片段 + 踩坑清单 | **每个新会话都发** |
| 01_template_index.md | 131 KB | 887 个模板函数的清单，含「指令编号 → 模板函数」反查 | AI 要查某条指令的模板时 |
| 02_places.md | 21 KB | 647 个地点 ID（中文名 + 日文原名），按 12 个地图分组 | 写 604 散步等按地点分的口上时 |
| 03_status.md | 9 KB | 147 口上当前写到哪了（函数清单 + 已实现指令编号） | 换 AI 时附上，让它知道进度 |
| **04_emuera_syntax_index.md** | 68 KB | Emuera 官方文档 **387 篇索引**（名称/标题/签名/摘要/路径） | 语法拿不准、要查准确签名时 |
| 05_emuera_syntax_full.md | 1.7 MB | Emuera 官方文档 **387 篇中文全文** | 一般不发，AI 能读本地时用 |
| **06_variable_names.md** | 115 KB | **变量名全表 2179 项**（编号 / 汉化名 / 日文原名 / 备注），源码实测 | 变量名拿不准时必查 |
| 07_character_index.md | 11 KB | 角色编号表 168 个（名前 / 呼び名 / 是否有口上） | 要确认角色编号时 |
| 08_command_index.md | 9 KB | 指令编号表 229 条（汉化名 / 日文原名） | 写 `MESSAGE_COM_K147_xxx` 前查 |
| 09_kojo_framework.md | 11 KB | 派发机制、29 类钩子、MESSAGECHECK、颜色常量、4.980 拦截器 | 写新钩子 / 排查「文本不显示」时 |
| **ALL_IN_ONE.md** | 197 KB | 00~03 合并成一个 | 上下文大的 AI（Kimi / Claude / Gemini）一次传完 |
| BUILD.py | — | 生成 01/02/03/ALL_IN_ONE 的脚本 | 素材更新后双击重跑 |
| EMUERA_KB_SYNC.py | — | 生成 04/05 的脚本 | Emuera 文档更新后跑一次 |
| ERATW_SOURCE_INDEX.py | — | 生成 06/07/08 的脚本 | 游戏本体更新后跑一次 |
| PUSH.bat | — | 双击推送到 GitHub | 改完知识库后 |

**最小用法：只发 00_core.md 就能开工。** 其余按需补充。

---

## 三种用法（按你的 AI 类型选）

### 用法 A：网页版 AI（最常见）

```
1. 新开对话
2. 上传 00_core.md
3. 说一句：「按这个包里的规则工作。我要写 604 散步的口上，文本如下：……」
```

如果 AI 要查模板细节，再补发 `01_template_index.md`；
要查地点编号，补发 `02_places.md`。

### 用法 B：本地 Agent（WorkBuddy / Cline / Cursor 等，能读本地文件）

不用上传，直接给路径：

```
知识库：D:\F\口上制作尝试\AI知识库\
先读 00_core.md，再读 03_status.md。
游戏源码在 D:\F\口上制作尝试\AI代写代码测试\eraTW\，需要时自己查。
```

### 用法 C：托管到公网（已配置好，最省事）

**仓库地址**：https://github.com/Er099/eratw-kojo-kb

三个入口，按你的 AI 类型选：

| 入口 | 链接 | 适用 | 更新速度 |
|---|---|---|---|
| **GitHub Pages** | `https://er099.github.io/eratw-kojo-kb/00_core.md` | 首选，更新即时 | push 后 1~2 分钟 |
| **jsDelivr CDN** | `https://cdn.jsdelivr.net/gh/Er099/eratw-kojo-kb@main/00_core.md` | 国内网络更稳 | 有缓存，约 12 小时 |
| **GitHub raw** | `https://raw.githubusercontent.com/Er099/eratw-kojo-kb/main/00_core.md` | 国外 AI（ChatGPT/Claude） | 即时 |

**直接复制给 AI 的话：**

```
先读这个文件再开始工作：
https://er099.github.io/eratw-kojo-kb/00_core.md
```

**⚠️ 国内网络实测**（2026-10-18）：

- `raw.githubusercontent.com` → **完全不通**（SSL 被阻断）
- `raw.githack.com` / `cdn.statically.io` → 同样不通
- `cdn.jsdelivr.net` → **可以通**，偶尔抖动，失败重试一次即可
- `er099.github.io` → 一般可通，但不如 jsDelivr 稳

所以：**国内 AI 用 jsDelivr，国外 AI 用 raw 或 Pages**。

其他文件的链接格式一样，把文件名换掉即可：

| 文件 | 文件名 |
|---|---|
| 核心包 | `00_core.md` |
| 模板索引 | `01_template_index.md` |
| 地点表 | `02_places.md` |
| 147 现状 | `03_status.md` |
| 语法索引 | `04_emuera_syntax_index.md` |
| 语法全文 | `05_emuera_syntax_full.md` |
| 四合一 | `ALL_IN_ONE.md` |

**更新后 CDN 还是旧内容怎么办？** 在链接后加 `?v=2`（数字随便改）强制绕过缓存：

```
https://cdn.jsdelivr.net/gh/Er099/eratw-kojo-kb@main/00_core.md?v=2
```

> ⚠️ 不建议把游戏源码（185 MB）传到仓库，超 GitHub 单仓库限制，且没必要——AI 真正需要的只是这份索引。

---

## 开场白模板（直接复制改）

**第一次开新会话时：**

```
我把 eraTW 口上制作的 AI 上下文包发给你了（00_core.md）。
请先完整读一遍，然后按包里的规则工作。

开工前先复述这三条：
① 识别符是 _147
② MESSAGE_COM 结尾写 RETURN 1
③ 旁白用 PRINTFORMD*，对白用 PRINTFORM*

复述完我再发任务。
```

**然后发任务：**

```
要写的指令：604 散步
条件：关系五段都要，按地点分（只写这几个地点：铃奈庵 213、情人旅馆 935、酒场 933）
文本：
【把你的中文文本贴在这里】

输出：可直接粘贴进 日常.ERB 的完整 ERB 代码。
```

**AI 卡住或说「不知道」时：**

```
这个信息在 01_template_index.md 里，我发给你。
（或：这条指令的模板长这样，你自己对照：）
```

---

## 更新知识库

改了不同东西要跑不同脚本（都是双击）：

| 改了什么 | 跑哪个 | 生成 |
|---|---|---|
| 口上进度 / 模板 / 地点 | `BUILD.py` | 01 / 02 / 03 / ALL_IN_ONE |
| Emuera 官方语法文档 | `EMUERA_KB_SYNC.py` | 04 / 05 |
| 游戏本体（CSV / 角色 / 指令） | `ERATW_SOURCE_INDEX.py` | 06 / 07 / 08 |

三个脚本都**不会动 `00_core.md`**——那是手写的，规则变了直接编辑，纯 Markdown。

如果换了电脑或改了目录，打开脚本改开头的路径常量。`BUILD.py` 是这样：

```python
GAME = r"D:\F\口上制作尝试\AI代写代码测试\eraTW"
TEMPLATE_DIR = r"D:\F\口上制作尝试\TW口上汉化精修模版(4.954-4.97X)"
KOJO_DIR = os.path.join(GAME, r"ERB\口上・メッセージ関連\個人口上\147 Sariel [サリエル]")
```

`ERATW_SOURCE_INDEX.py` 改 `GAME` 一行即可；`EMUERA_KB_SYNC.py` 改 `SRC_DIR`。

### 更新到 GitHub（让链接也同步）

重新生成之后，**双击本目录的 `PUSH.bat`** 即可。

它会自动定位 WorkBuddy 自带的 git（系统 PATH 里没有 `git` 命令），然后执行 `git push`，成功后显示 `[OK]`。

> 第一次推送可能弹浏览器让你登录 GitHub，用 `Er099` 账号登录并点 Authorize，之后自动记住。
> 如果报 `CONNECT tunnel failed 502`，是网络到 github.com 不通，过几分钟重试。

推送完成后：

- **GitHub Pages** 1~2 分钟自动更新
- **jsDelivr** 有约 12 小时缓存，急用就在链接后加 `?v=2`

---

## 为什么不能真的「共享」一个知识库

AI 之间没有共享存储。每个对话都是独立的，A 告诉它的东西 B 不知道。

所以真正可行的只有三条路：

| 方式 | 本质 | 成本 |
|---|---|---|
| 每次上传文件 | 你手动搬运 | 免费，最稳 |
| 公网链接 | AI 自己联网读 | 免费，但依赖联网能力 |
| 本地路径 | AI 读你的硬盘 | 免费，但只对本地 Agent 有效 |

本套方案把「要搬运的东西」压到了最小：**24 KB 一个文件**。
这已经接近理论下限——再小就装不下规则和语法了。

---

## 包里有什么（00_core.md 目录）

```
0. 一句话任务          —— AI 该做什么、输出什么格式
1. 硬规则              —— 文本层 / 结构层 / 颜色层，违反会被打回
2. 关系差分            —— 固定五段骨架（所有指令都用它）
3. eraTW 口上框架      —— 函数命名、返回值语义、变量位、颜色
4. Emuera 语法速查     —— 变量体系、PRINT 系、PRINTDATA、TEXTR、控制流、常用函数
5. 变量名与编号        —— TALENT/ABL/EXP/BASE/CSTR 常用条目
6. 代码片段库          —— 骨架、604、扣血变色、随机文本、询问菜单
7. 踩坑清单            —— 18 条真实踩过的坑
8. 配合方式            —— 交付格式、自查清单
9. 本包用法            —— 就是你正在看的这张表
```

---

## 已知局限

1. **AI 不会记得上一次对话**。每次新会话都要重发 00。
2. **AI 读不到你的游戏文件**（除非是本地 Agent）。所以它不能自己查源码，只能靠包里的速查内容。
3. **包的时效性**：`01/02/03` 反映的是生成那一刻的磁盘状态。游戏更新后记得重跑 `BUILD.py`。
4. **AI 可能编造**。如果它给出的函数名/变量名不在包里，让它标注「不确定」，你再让它查 `01_template_index.md`。

---

*生成日期：2026-10-18 ／ 对应游戏版本：eraTW 画蛇添足 4.981 汉化版*
