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