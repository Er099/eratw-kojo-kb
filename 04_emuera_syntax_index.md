# Emuera 官方语法文档 · 索引（387 篇）

> 来源：`emuera.sk.doc` 重构版（原 evilmask 文档），由 `EMUERA_DOC_INDEX.py` 生成。

> 本地原文：`D:/F/口上制作尝试/emuera/emuera.sk.doc-feature-tutorial-restructure/docs/`

> 全文：同目录 `05_emuera_syntax_full.md`（1.8MB，搜 `===== FILE:` 定位）


## 怎么用

1. 先在本文件搜**命令名**（如 `PRINTFORM`、`SPLIT`、`ARRAYSHIFT`）。

2. 拿到「路径」后，去 `05_emuera_syntax_full.md` 里搜同名的 `===== FILE:` 段。

3. 索引里的「摘要」通常够判断是不是你要的那篇，不够再看全文。


> 口上高频语法的**提炼版**在 `00_core.md` 第 4 章，优先看那个；本索引是权威兜底。


## 指令与函数参考（313 篇）

| 名称 | 标题 | 签名 | 摘要 | 路径 |
|---|---|---|---|---|
| `ABS` | ABS, SIGN |  | 这是分别用于计算绝对值和表示正负方向的命令/表达式函数。 | `docs/Reference/ABS.zh.md` |
| `ADDCHARA` | ADDCHARA |  | 从 CharaXX.csv 文件中添加指定编号的角色。 | `docs/Reference/ADDCHARA.zh.md` |
| `ADDCOPYCHARA` | ADDCOPYCHARA |  | 新增一个与参数指定登记编号 (CharaID) 的角色数据完全相同的角色。也就是说，这是 ADDCHARA 的一个变体。 | `docs/Reference/ADDCOPYCHARA.zh.md` |
| `ADDDEFCHARA` | ADDDEFCHARA |  | 执行游戏开始时的系统角色添加处理。 | `docs/Reference/ADDDEFCHARA.zh.md` |
| `ADDVOIDCHARA` | ADDVOIDCHARA |  | 此指令用于不依赖 CSV 文件添加角色。 | `docs/Reference/ADDVOIDCHARA.zh.md` |
| `ALIGNMENT` | ALIGNMENT, CURRENTALIGN |  | ALIGNMENT 之后的文本行将按指定位置对齐。 | `docs/Reference/ALIGNMENT.zh.md` |
| `ARGLEN` | ARGLEN |  | 返回当前函数调用中传入的可变长参数（VARIADIC）的数量。仅在用 VARIADIC 关键字声明的函数内返回有意义的值。 | `docs/Reference/ARGLEN.zh.md` |
| `ARRAYCOPY` | ARRAYCOPY |  | 实现无差别数组复制指令 ARRAYCOPY | `docs/Reference/ARRAYCOPY.zh.md` |
| `ARRAYMSORT` | ARRAYMSORT |  | ARRAYMSORT 将 variableName1 按升序排序，并按照相同的顺序重新排列 variableName2 及后续的数组。 | `docs/Reference/ARRAYMSORT.zh.md` |
| `ARRAYMSORTEX` | ARRAYMSORTEX |  | 与本家的 [ARRAYMSORTEX](https://osdn.net/projects/emuera/wiki/excom#h5-ARRAYMSORT.20array_a.7B.2C.20array_b....7D) 函数类似。 | `docs/Reference/ARRAYMSORTEX.zh.md` |
| `ARRAYREMOVE` | ARRAYREMOVE |  | 实现用于部分删除数组元素的指令 ARRAYREMOVE。 | `docs/Reference/ARRAYREMOVE.zh.md` |
| `ARRAYSHIFT` | ARRAYSHIFT |  | 实现用于数组位移的命令 ARRAYSHIFT | `docs/Reference/ARRAYSHIFT.zh.md` |
| `ARRAYSORT` | ARRAYSORT |  | 对数组变量进行排序的ARRAYSORT实现 | `docs/Reference/ARRAYSORT.zh.md` |
| `ASSERT` | ASSERT |  | DEBUG 系列命令仅在以[调试模式](../Emuera/debug.zh.md)启动时才会执行。 | `docs/Reference/ASSERT.zh.md` |
| `AWAIT` | AWAIT |  | 暂停ERB的执行，进行Windows的处理。 | `docs/Reference/AWAIT.zh.md` |
| `BACKGROUND` | BACKGROUND操作系 |  | 制作者：Neo_Kesha | `docs/Reference/BACKGROUND.zh.md` |
| `BAR` | BAR(L) |  | 绘制一个条形图，表示第一个参数相对于第二个参数的比例。第三个参数可以设置条形的长度。 | `docs/Reference/BAR.zh.md` |
| `BARSTR` | BARSTR |  | 将使用相同参数的[BAR](./BAR.zh.md)命令所显示的字符串赋值给RESULTS:0或返回该字符串。 | `docs/Reference/BARSTR.zh.md` |
| `BEGIN` | BEGIN |  | BEGIN 通过调用各种系统指令来推进游戏进程。 | `docs/Reference/BEGIN.zh.md` |
| `BINPUT` | BINPUT(S) |  | 仅接受在执行时已按钮化的值的 INPUT(S)。 | `docs/Reference/BINPUT.zh.md` |
| `BITARRAY` | BITSET / BITGET / BITTOGGLE / BITINDEXOFFIRST |  | 使用整数数组模拟位图（Bitmap），提供位的设置、读取、翻转和查找功能。 | `docs/Reference/BITARRAY.zh.md` |
| `BITMAP_CACHE_ENABLE` | BITMAP_CACHE_ENABLE |  | 制作者：JukesBouver99 | `docs/Reference/BITMAP_CACHE_ENABLE.zh.md` |
| `BIT_OPERATION` | BIT操作系 |  | 这是用于位操作的函数。 | `docs/Reference/BIT_OPERATION.zh.md` |
| `BREAKBUTTON` | BREAKBUTTON |  | 强制更新画面的按钮化状态。 | `docs/Reference/BREAKBUTTON.zh.md` |
| `CALL` | CALL |  | 调用以@开头的字符串定义的函数 | `docs/Reference/CALL.zh.md` |
| `CALLEVENT` | CALLEVENT |  | 将事件函数作为事件函数调用。 | `docs/Reference/CALLEVENT.zh.md` |
| `CALLF` | CALLF, CALLFORMF |  | 以下摘自私家改造版更新日志： | `docs/Reference/CALLF.zh.md` |
| `CALLSHARP` | CALLSHARP |  | 制作者：Neo_Kesha | `docs/Reference/CALLSHARP.zh.md` |
| `CALLSTR` | CALLSTR系 |  | 与 CALL、JUMP 及其 TRY 系统类似，但允许通过一个字符串表达式来指定完整的函数调用行（包括函数名和参数）。 | `docs/Reference/CALLSTR.zh.md` |
| `CALLTRAIN` | CALLTRAIN |  | 需要预先将命令编号赋值给SELECTCOM:(1～)，并以要执行的命令数量作为参数来执行。 | `docs/Reference/CALLTRAIN.zh.md` |
| `CARRAY` | SUMCARRAY, CMATCH, MAXCARRAY, MINCARRAY |  | 这是遍历角色间的 [SUMARRAY](./SUMARRAY.zh.md)、[MATCH](./MATCH.zh.md)、[MAXARRAY](./MAXMINARRAY.zh.md)、[MINARRAY](./MAXMINARRAY.zh.md) 的变体。 | `docs/Reference/CARRAY.zh.md` |
| `CBGCLEAR` | CBGCLEAR |  | 解除所有通过以CBG开头的各种CBG系命令设置的背景图片设定。 | `docs/Reference/CBGCLEAR.zh.md` |
| `CBGCLEARBUTTON` | CBGCLEARBUTTON |  | 解除由 [CBGSETBUTTONSPRITE](./CBGSETBUTTONSPRITE.zh.md) 命令设置的按钮配置。 | `docs/Reference/CBGCLEARBUTTON.zh.md` |
| `CBGREMOVEMAPB` | CBGREMOVEMAPB |  | 解除由 [CBGSETBMAPG](./CBGSETBMAPG.zh.md) 命令设置的按钮映射配置。 | `docs/Reference/CBGREMOVEMAPB.zh.md` |
| `CBGREMOVERANGE` | CBGREMOVERANGE |  | 解除由 [CBGSETG](./CBGSETG.zh.md)、[CBGSETSPRITE](./CBGSETSPRITE.zh.md)、[CBGSETBUTTONSPRITE](./CBGSETBUTTONSPRITE.zh.md) 命令设置的图像中，Z深度在 zMin 以上 zMax 以下（含）的图像。 | `docs/Reference/CBGREMOVERANGE.zh.md` |
| `CBGSETBMAPG` | CBGSETBMAPG |  | 将gID指定的Graphics设置为客户端区域的按钮映射。 | `docs/Reference/CBGSETBMAPG.zh.md` |
| `CBGSETBUTTONSPRITE` | CBGSETBUTTONSPRITE |  | 此命令与[CBGSETBMAPG](./CBGSETBMAPG.zh.md)命令设置的按钮映射联动，用于设置可选择的按钮。 | `docs/Reference/CBGSETBUTTONSPRITE.zh.md` |
| `CBGSETG` | CBGSETG |  | 将指定gID的Graphics设置为在客户端区域内显示。 | `docs/Reference/CBGSETG.zh.md` |
| `CBGSETSPRITE` | CBGSETSPRITE |  | 将指定资源名 spriteName 对应的精灵（sprite）设置为在客户端区域显示。 | `docs/Reference/CBGSETSPRITE.zh.md` |
| `CHARATU` | CHARATU |  | 获取字符串中指定位置字符的式中函数CHARATU | `docs/Reference/CHARATU.zh.md` |
| `CHKCHARADATA` | CHKCHARADATA |  | 返回 dat 文件夹内由 chara_*.dat 表示的文件名所对应的数据信息。 | `docs/Reference/CHKCHARADATA.zh.md` |
| `CHKDATA` | CHKDATA |  | 将saveID所指定编号的文件数据信息赋值给RESULT:0和RESULTS:0。 | `docs/Reference/CHKDATA.zh.md` |
| `CLEARIMAGELAYER` | CLEARIMAGELAYER / CLEARIMAGELAYER_ALL |  | CLEARIMAGELAYER：清除指定 depth 的 [SETIMAGELAYER](./SETIMAGELAYER.zh.md) 图层。 | `docs/Reference/CLEARIMAGELAYER.zh.md` |
| `CLEARLINE` | CLEARLINE |  | 删除指定行数的字符串（行数的计数方式与LINECOUNT相同）。 | `docs/Reference/CLEARLINE.zh.md` |
| `CLEARMEMORY` | CLEARMEMORY |  | 释放内存，并返回释放的内存量（单位为 byte）。 | `docs/Reference/CLEARMEMORY.zh.md` |
| `CLEARTEXTBOX` | CLEARTEXTBOX |  | 清除最底部输入栏中的所有文本。 | `docs/Reference/CLEARTEXTBOX.zh.md` |
| `CLIENTFIELD` | CLIENTWIDTH, CLIENTHEIGHT |  | 获取客户端区域（窗口绘图区域）的当前宽度或高度。 | `docs/Reference/CLIENTFIELD.zh.md` |
| `COLOR_FROM` | COLOR_FROMNAME, COLOR_FROMRGB |  | COLOR_FROMNAME 将给定的参数作为颜色名进行判断，并返回 0xRRGGBB 格式的数值。 | `docs/Reference/COLOR_FROM.zh.md` |
| `CONTINUE` | CONTINUE, BREAK |  | 可在 [REPEAT](./REPEAT.zh.md)、[FOR](./FOR.zh.md)、[WHILE](./WHILE.zh.md)、[DO](./DO.zh.md) 内部使用的循环控制指令。 | `docs/Reference/CONTINUE.zh.md` |
| `CONVERT` | CONVERT |  | ※处只能填入2、8、10、16。 | `docs/Reference/CONVERT.zh.md` |
| `COPYCHARA` | COPYCHARA |  | 将第一个参数指定的登记编号 (CharaID) 角色的所有数据复制到第二个参数指定的登记编号 (CharaID) 角色。 | `docs/Reference/COPYCHARA.zh.md` |
| `CSVNAME` | CSVNAME系 |  | 这是直接调用 CSV 中定义的 NAME、CALLNAME、NICKNAME、MASTERNAME 的函数。 | `docs/Reference/CSVNAME.zh.md` |
| `CSV_STATUS` | CSV状态获取函数 |  | 这是直接调用 CSV 中定义的值的函数。 | `docs/Reference/CSV_STATUS.zh.md` |
| `CUPCHECK` | CUPCHECK |  | CUPCHECK 是 CUP、CDOWN 对应的 UPCHECK。 | `docs/Reference/CUPCHECK.zh.md` |
| `CUSTOMDRAWLINE` | CUSTOMDRAWLINE, DRAWLINEFORM |  | 使用指定的字符串显示一行分隔符。DRAWLINEFORM 支持 FORM 语法。 | `docs/Reference/CUSTOMDRAWLINE.zh.md` |
| `CVARSET` | CVARSET |  | 此命令用于对指定已注册角色，向其角色变量的特定元素赋值。 | `docs/Reference/CVARSET.zh.md` |
| `DEBUGPRINT` | DEBUGPRINT 系列 |  | DEBUG 系列命令仅在以[调试模式](../Emuera/debug.zh.md)启动时才会执行。 | `docs/Reference/DEBUGPRINT.zh.md` |
| `DELALLCHARA` | DELALLCHARA |  | 删除所有已注册的角色。 效果等同于以下脚本： | `docs/Reference/DELALLCHARA.zh.md` |
| `DELCHARA` | DELCHARA |  | 删除指定ID的角色。 | `docs/Reference/DELCHARA.zh.md` |
| `DELDATA` | DELDATA |  | 删除由 saveID 指定编号的文件数据。 | `docs/Reference/DELDATA.zh.md` |
| `DISABLE_INPUT_MACRO` | DISABLE_INPUT_MACRO ![](../assets/images/IconSK.webp) |  | 关闭所有输入（textbox + SEQUENCEINPUT）的宏解析。调用后，输入按字面整段喂入，不再解析 (...) 重复宏，不再按 n 拆分，也不再处理 e MesSkip。 | `docs/Reference/DISABLE_INPUT_MACRO.zh.md` |
| `DO` | DO-LOOP |  | [REPEAT～REND](./REPEAT.zh.md) 和 [FOR～NEXT](./FOR.zh.md) 一样，是一种循环结构。 | `docs/Reference/DO.zh.md` |
| `DOTRAIN` | DOTRAIN |  | 强制进行TRAIN的命令。 | `docs/Reference/DOTRAIN.zh.md` |
| `DRAWLINE` | DRAWLINE |  | 从屏幕右端到左端用 - 画一条线 | `docs/Reference/DRAWLINE.zh.md` |
| `DT_CELL` | DataTable 单元格管理相关函数 |  | 操作 DataTable（数据库，基于 [DataTable](https://learn.microsoft.com/zh-cn/dotnet/api/system.data.datatable?view=netframework-4.8) 类）单元格的函数。 | `docs/Reference/DT_CELL.zh.md` |
| `DT_COLUMN` | DataTable 列管理相关函数 |  | DataTable （数据库，基于 [DataTable](https://learn.microsoft.com/zh-cn/dotnet/api/system.data.datatable?view=netframework-4.8) 类）的列的操作相关的一系列函数。 | `docs/Reference/DT_COLUMN.zh.md` |
| `DT_MANAGE` | DataTable 管理相关函数 |  | DataTable （数据库，基于 [DataTable](https://learn.microsoft.com/zh-cn/dotnet/api/system.data.datatable?view=netframework-4.8) 类）的创建 / 删除 / 判断是否存在 / 数据清除 / 大小写无视设定相关的一系列函数。 | `docs/Reference/DT_MANAGE.zh.md` |
| `DT_ROW` | DataTable 行管理相关函数 |  | DataTable （数据库，基于 [DataTable](https://learn.microsoft.com/zh-cn/dotnet/api/system.data.datatable?view=netframework-4.8) 类）的行的操作相关的一系列函数。 | `docs/Reference/DT_ROW.zh.md` |
| `DT_SELECT` | DT_SELECT |  | 从名为 dataTableName 的 DataTable 中选择满足 filterExpression 的行，将其 id 列的值按照 sortRule 的规则排序、依次代入 output 数组中。返回被选择的行的总数。 | `docs/Reference/DT_SELECT.zh.md` |
| `DT_SERIALIZATION` | DataTable 序列化相关函数 |  | DataTable （数据库，基于 [DataTable](https://learn.microsoft.com/zh-cn/dotnet/api/system.data.datatable?view=netframework-4.8) 类）与 XML互相转换的函数。 | `docs/Reference/DT_SERIALIZATION.zh.md` |
| `ENABLE_INPUT_MACRO` | ENABLE_INPUT_MACRO ![](../assets/images/IconSK.webp) |  | 恢复输入宏解析（默认行为）。调用 DISABLE_INPUT_MACRO 后可用此函数恢复原版 PressEnterKey 的宏解析、n 拆分和 e MesSkip 处理。 | `docs/Reference/ENABLE_INPUT_MACRO.zh.md` |
| `ENUMFILES` | ENUMFILES |  | 将文件夹dir下满足pattern规则的文件名代入RESULTS数组。返回符合条件的文件数。 | `docs/Reference/ENUMFILES.zh.md` |
| `ENUMFUNC` | ENUMFUNC 系列 |  | 将定义的函数名中包含 keyword 的具体函数名保存到 RESULTS 数组，同时返回总数（RESULT）。 | `docs/Reference/ENUMFUNC.zh.md` |
| `ENUMMACRO` | ENUMMACRO 系列 |  | 将定义的宏名中包含 keyword 的具体宏名保存到 RESULTS 数组，同时返回总数（RESULT）。 | `docs/Reference/ENUMMACRO.zh.md` |
| `ENUMVAR` | ENUMVAR 系列 |  | 将定义的变量 / 常量名中包含 keyword 的具体变量 / 常量名保存到 RESULTS 数组，同时返回总数（RESULT）。 | `docs/Reference/ENUMVAR.zh.md` |
| `ERDNAME` | ERDNAME |  | 指定 ERD 变量的下标，返回元素的名称。可以用 dimension 来指定数组维度（与文件名规则相同，从左开始依次为 1, 2, 3） | `docs/Reference/ERDNAME.zh.md` |
| `ESCAPE` | ESCAPE |  | 对参数字符串中的正则表达式元字符进行转义，使其在正则表达式中被视为普通文本，并返回转义后的字符串。 | `docs/Reference/ESCAPE.zh.md` |
| `EVAL` | EVAL / EVALS / EVALF |  | 将传入的字符串 expression 作为 ERB 表达式在运行时进行动态解析与求值。 | `docs/Reference/EVAL.zh.md` |
| `EXISTCSV` | EXISTCSV |  | 检查对应的角色是否已定义，并将结果赋值给RESULT:0或直接返回。 | `docs/Reference/EXISTCSV.zh.md` |
| `EXISTFILE` | EXISTFILE |  | 判断 Emuera.exe 同级以及下级子目录（无法使用 .. 访问父级目录）的相对路径是否存在文件 relativePath。 | `docs/Reference/EXISTFILE.zh.md` |
| `EXISTFUNCTION` | EXISTFUNCTION |  | 判定是否定义过以参数 funcName 为名的函数 / 行内函数。 | `docs/Reference/EXISTFUNCTION.zh.md` |
| `EXISTMETH` | EXISTMETH |  | 检查是否存在指定的表达式中函数，如果是#FUNCTION则返回1，如果是#FUNCTIONS则返回2，否则返回0。 | `docs/Reference/EXISTMETH.zh.md` |
| `EXISTSIMAGELAYER` | EXISTSIMAGELAYER |  | 检测指定 depth 的 [SETIMAGELAYER](./SETIMAGELAYER.zh.md) 图层是否存在。 | `docs/Reference/EXISTSIMAGELAYER.zh.md` |
| `EXISTSOUND` | EXISTSOUND |  | 判断音频资源目录 ./sound/ 中是否存在参数 MediaFile 指定的音频文件；存在返回 1，不存在返回 0。 | `docs/Reference/EXISTSOUND.zh.md` |
| `EXISTVAR` | EXISTVAR |  | 如果存在与 varName 同名的变量 / 常量则返回对应的正整数，否则返回 0。 | `docs/Reference/EXISTVAR.zh.md` |
| `FINDCHARA` | FINDCHARA, FINDLASTCHARA |  | FINDCHARA 指令通过指定角色变量和值，返回变量等于该值的角色的登记编号 (CharaID)。 | `docs/Reference/FINDCHARA.zh.md` |
| `FINDELEMENT` | FINDELEMENT |  | 此函数用于从数组的指定范围内查找特定元素的位置。 | `docs/Reference/FINDELEMENT.zh.md` |
| `FIND_CHARADATA` | FIND_CHARADATA |  | 在 dat 文件夹中搜索可以作为 [LOADCHARA](./LOADCHARA.zh.md) 目标的文件，并将文件名（chara_*.dat 中的 * 部分）代入 RESULTS。 | `docs/Reference/FIND_CHARADATA.zh.md` |
| `FLOWINPUT` | FLOWINPUT,FLOWINPUTS |  | 为流程中的 INPUT（例如在 @SHOW_SHOP 内）添加默认值、是否允许左键点击以及是否允许跳过等选项。 | `docs/Reference/FLOWINPUT.zh.md` |
| `FONT_OPERATION` | 字体操作相关 |  | 将后续文字更改为指定样式 | `docs/Reference/FONT_OPERATION.zh.md` |
| `FOR` | FOR-NEXT |  | FOR～NEXT 是 [REPEAT～REND](./REPEAT.zh.md) 的功能增强版。 | `docs/Reference/FOR.zh.md` |
| `FORCEKANA` | FORCEKANA |  | 指定显示命令的平假名/片假名转换。 | `docs/Reference/FORCEKANA.zh.md` |
| `FORCEWAIT` | FORCEWAIT |  | 这是一个无法通过右键点击或宏跳过功能跳过的 [WAIT](./WAIT.zh.md) 指令。 | `docs/Reference/FORCEWAIT.zh.md` |
| `FORCE_BEGIN` | FORCE_BEGIN |  | 忽略流程控制的影响，强制执行 BEGIN 命令。 | `docs/Reference/FORCE_BEGIN.zh.md` |
| `FORCE_QUIT` | FORCE_QUIT |  | 未附加 WAIT 的 QUIT。（即直接退出） | `docs/Reference/FORCE_QUIT.zh.md` |
| `FORCE_QUIT_AND_RESTART` | FORCE_QUIT_AND_RESTART |  | 未附加 WAIT 的 QUIT_AND_RESTART。（即直接重启） | `docs/Reference/FORCE_QUIT_AND_RESTART.zh.md` |
| `FORM` | CALLFORM, JUMPFORM, GOTOFORM |  | 与 [CALL](./CALL.zh.md)、[JUMP](./JUMP.zh.md)、[GOTO](./GOTO.zh.md) 相同，但可以像 [PRINTFORM](./PRINT.zh.md) 一样指定函数名。 | `docs/Reference/FORM.zh.md` |
| `GCLEAR` | GCLEAR |  | 将指定gID的Graphics对象的整个区域替换为指定颜色。 | `docs/Reference/GCLEAR.zh.md` |
| `GCREATE` | GCREATE |  | 以指定尺寸创建指定 gID 的 Graphics。 | `docs/Reference/GCREATE.zh.md` |
| `GCREATED` | GCREATED |  | 如果指定gID的Graphics已创建则返回1，未创建（包括已销毁）则返回0。 | `docs/Reference/GCREATED.zh.md` |
| `GCREATEFROMFILE` | GCREATEFROMFILE |  | 使用相对于 resources 文件夹的路径指定图像文件，打开该图像并创建 Graphics。 | `docs/Reference/GCREATEFROMFILE.zh.md` |
| `GDASHSTYLE` | GDASHSTYLE |  | 指定GDRAWLINE的线条样式。DashStyle和DashCap分别可以使用C#的DashStyle、DashCap枚举的数值来指定。 | `docs/Reference/GDASHSTYLE.zh.md` |
| `GDISPOSE` | GDISPOSE |  | 销毁指定gID的Graphics对象。 | `docs/Reference/GDISPOSE.zh.md` |
| `GDRAWG` | GDRAWG |  | 将指定的 srcID 对应的 Graphics 绘制到指定的 destID 对应的 Graphics 上。 | `docs/Reference/GDRAWG.zh.md` |
| `GDRAWGWITHMASK` | GDRAWGWITHMASK |  | 在指定的 destID 的 Graphics 上，使用 maskID 的 Graphics 作为蒙版，绘制 srcID 的 Graphics。 | `docs/Reference/GDRAWGWITHMASK.zh.md` |
| `GDRAWGWITHROTATE` | GDRAWGWITHROTATE |  | 将 destID 指定的图像顺时针旋转 Angle 的角度，并把旋转后的图像粘贴到 gID 指定的图像。 | `docs/Reference/GDRAWGWITHROTATE.zh.md` |
| `GDRAWLINE` | GDRAWLINE |  | 在gID指定的Graphics上，从fromX,fromY坐标到forX,forY坐标绘制一条直线。 | `docs/Reference/GDRAWLINE.zh.md` |
| `GDRAWSPRITE` | GDRAWSPRITE |  | 在指定gID的Graphics上，绘制指定spriteName的Sprite。 | `docs/Reference/GDRAWSPRITE.zh.md` |
| `GDRAWTEXT` | GDRAWTEXT |  | 在 gID 指定的 Graphics 中绘制 text。字体、描边等使用 GSETFONT / GSETPEN 指定的样式。 | `docs/Reference/GDRAWTEXT.zh.md` |
| `GETCHARA` | GETCHARA |  | 判断指定角色是否在当前持有的角色列表中，如果在则返回其在列表中的位置，否则返回-1。 | `docs/Reference/GETCHARA.zh.md` |
| `GETCOLOR` | GETCOLOR 系列 |  | 分别将颜色代码赋值给 RESULT:0 或返回。 | `docs/Reference/GETCOLOR.zh.md` |
| `GETCONFIG` | GETCONFIG(S) |  | 获取配置项及 [replace.csv](../Emuera/replace.zh.md) 设置项的整数值或字符串值。 | `docs/Reference/GETCONFIG.zh.md` |
| `GETCSVNOBY` | GETCSVNOBY系 |  | 通过角色的名字反查角色注册编号 (NO)。是 [CSVNAME系](CSVNAME.zh.md) 的逆操作：CSVNAME 从编号查名字，GETCSVNOBY 从名字查编号。 | `docs/Reference/GETCSVNOBY.zh.md` |
| `GETDISPLAYLINE` | GETDISPLAYLINE |  | 从已显示的行中，返回指定行的字符串 | `docs/Reference/GETDISPLAYLINE.zh.md` |
| `GETDOINGFUNCTION` | GETDOINGFUNCTION |  | 返回当前正在执行的函数的标签名。若在系统待机中（如标题画面）调用，则返回空字符串。 | `docs/Reference/GETDOINGFUNCTION.zh.md` |
| `GETKEY` | GETKEY, GETKEYTRIGGERED |  | GETKEY 返回键盘及鼠标按键的状态。 | `docs/Reference/GETKEY.zh.md` |
| `GETLINESTR` | GETLINESTR |  | 将参数字符串传递给 [CUSTOMDRAWLINE](./CUSTOMDRAWLINE.zh.md)、[DRAWLINEFORM](./CUSTOMDRAWLINE.zh.md) 时，返回将显示的字符串。 | `docs/Reference/GETLINESTR.zh.md` |
| `GETLINEY` | GETLINEY |  | 返回指定行号的物理 Y 坐标（左下原点），与 [SETIMAGELAYER](./SETIMAGELAYER.zh.md) 的坐标系一致。 | `docs/Reference/GETLINEY.zh.md` |
| `GETMEMORYUSAGE` | GETMEMORYUSAGE |  | 返回当前运行中的 Emuera 占用的内存使用量（单位为 byte）。 | `docs/Reference/GETMEMORYUSAGE.zh.md` |
| `GETMETH` | GETMETH,GETMETHS,GETMETHF |  | 可以从字符串调用式中函数。GETMETH 对应 #FUNCTION，GETMETHS 对应 #FUNCTIONS，GETMETHF 对应 #FUNCTIONF。 | `docs/Reference/GETMETH.zh.md` |
| `GETMILLISECOND` | GETMILLISECOND |  | 获取自公元0001年1月1日起经过的时间，单位为毫秒。 | `docs/Reference/GETMILLISECOND.zh.md` |
| `GETNUM` | GETNUM |  | 从各 CSV 文件中定义的名称获取其对应的数值，并赋值给 RESULT:0。 | `docs/Reference/GETNUM.zh.md` |
| `GETPALAMLV` | GETPALAMLV, GETEXPLV |  | 将给定值与 PALAMLV 和 EXPLV 进行比较，并将该参数在 PALAMLV 和 EXPLV 中达到或超过的等级赋值给 RESULT:0。 | `docs/Reference/GETPALAMLV.zh.md` |
| `GETPLATFORM` | GETPLATFORM |  | 返回当前运行平台的整数编码。 | `docs/Reference/GETPLATFORM.zh.md` |
| `GETSECOND` | GETSECOND |  | 获取自公元0001年1月1日起经过的时间（以秒为单位），并赋值给RESULT:0。 | `docs/Reference/GETSECOND.zh.md` |
| `GETSETVAR` | SETVAR / GETVAR 系列 |  | 名为 varName 的变量 / 常量的 GET / SET 函数（常量无法使用 SET 修改值）。 | `docs/Reference/GETSETVAR.zh.md` |
| `GETTIME` | GETTIME |  | 将计算机的当前日期/时间信息赋值给 RESULT:0 和 RESULTS:0。 | `docs/Reference/GETTIME.zh.md` |
| `GFILLRECTANGLE` | GFILLRECTANGLE |  | 在指定的gID对应的Graphics上，绘制由x, y, width, height定义的矩形。 | `docs/Reference/GFILLRECTANGLE.zh.md` |
| `GGETBRUSH` | GGETBRUSH |  | 返回 gID 代表的图像中 GSETBRUSH 所指定的颜色（cARGB）。 | `docs/Reference/GGETBRUSH.zh.md` |
| `GGETCOLOR` | GGETCOLOR |  | 获取指定gID的Graphics在指定位置的颜色，以0xAARRGGBB格式的整数值返回。 | `docs/Reference/GGETCOLOR.zh.md` |
| `GGETFONT` | GGETFONT |  | 返回指定的 gID 使用 GSETFONT 设置的字体名称。 | `docs/Reference/GGETFONT.zh.md` |
| `GGETFONTSIZE` | GGETFONTSIZE |  | 返回指定的 gID 使用 GSETFONT 设置的字体大小。 | `docs/Reference/GGETFONTSIZE.zh.md` |
| `GGETFONTSTYLE` | GGETFONTSTYLE |  | 返回指定的 gID 使用 GSETFONT 设置的字体样式标记。 | `docs/Reference/GGETFONTSTYLE.zh.md` |
| `GGETPEN` | GGETPEN |  | 返回 gID 代表的图像中 GSETPEN 所指定的颜色（cARGB）。 | `docs/Reference/GGETPEN.zh.md` |
| `GGETPENWIDTH` | GGETPENWIDTH |  | 返回 gID 代表的图像中 GSETPEN 所指定的画笔宽度。 | `docs/Reference/GGETPENWIDTH.zh.md` |
| `GGETTEXTSIZE` | GGETTEXTSIZE |  | 预测 GDRAWTEXT 使用指定的参数绘制时生成的 Width / Height（分别代入 RESULT:0 / RESULT:1）。 | `docs/Reference/GGETTEXTSIZE.zh.md` |
| `GOTO` | GOTO |  | 跳转到函数内由$定义的标签处 | `docs/Reference/GOTO.zh.md` |
| `GROUPCHECK` | GROUPMATCH, NOSAMES, ALLSAMES |  | 所有参数必须是同一类型。 | `docs/Reference/GROUPCHECK.zh.md` |
| `GSAVELOAD` | GSAVE, GLOAD |  | GSAVE 将指定 gID 的 Graphics 图像以 png 格式输出并保存，文件名带有 fileNo 编号。 | `docs/Reference/GSAVELOAD.zh.md` |
| `GSETBRUSH` | GSETBRUSH |  | 为指定ID的Graphics对象设置指定颜色的画刷。 | `docs/Reference/GSETBRUSH.zh.md` |
| `GSETCOLOR` | GSETCOLOR |  | 将指定ID的Graphics对象在指定位置的像素替换为指定颜色。 | `docs/Reference/GSETCOLOR.zh.md` |
| `GSETFONT` | GSETFONT |  | 为指定gID的Graphics对象设置指定名称和尺寸的字体。 | `docs/Reference/GSETFONT.zh.md` |
| `GSETPEN` | GSETPEN |  | 为指定gID的Graphics对象设置指定颜色和宽度的画笔。 | `docs/Reference/GSETPEN.zh.md` |
| `GWIDTHHEIGHT` | GWIDTH, GHEIGHT |  | 获取指定gID的Graphics的宽度或高度。 | `docs/Reference/GWIDTHHEIGHT.zh.md` |
| `G_POLYGON` | G_POLYGON 系列 |  | G_POLYGON_POINT_ADD向指定gID的图形添加顶点。 | `docs/Reference/G_POLYGON.zh.md` |
| `HOTKEY_STATE` | HOTKEY_STATE / HOTKEY_STATE_INIT |  | 管理快捷键状态的函数。 | `docs/Reference/HOTKEY_STATE.zh.md` |
| `HTML_ESCAPE` | HTML_ESCAPE |  | 将目标字符串转义为HTML格式（转换为字符引用）。 | `docs/Reference/HTML_ESCAPE.zh.md` |
| `HTML_GETPRINTEDSTR` | HTML_GETPRINTEDSTR |  | 获取已显示行中由lineNo指定行的内容，以HTML格式字符串形式返回。 | `docs/Reference/HTML_GETPRINTEDSTR.zh.md` |
| `HTML_POPPRINTINGSTR` | HTML_POPPRINTINGSTR |  | 获取当前 [PRINT](./PRINT.zh.md) 中处于换行等待状态的字符串缓冲区的 HTML 格式内容，并清空缓冲区。 | `docs/Reference/HTML_POPPRINTINGSTR.zh.md` |
| `HTML_PRINT` | HTML_PRINT |  | 这是一个使用类似HTML标签进行[PRINT](./PRINT.zh.md)的命令。 | `docs/Reference/HTML_PRINT.zh.md` |
| `HTML_PRINTC` | HTML_PRINTC / HTML_PRINTLC |  | [HTML_PRINT](./HTML_PRINT.zh.md) 的右对齐和左对齐变体。使用 HTML 标签进行渲染，但对齐位置不同。 | `docs/Reference/HTML_PRINTC.zh.md` |
| `HTML_PRINT_ISLAND` | HTML_PRINT_ISLAND,HTML_PRINT_ISLAND_CLEAR |  | 其标签语法与 [HTML_PRINT](HTML_PRINT.zh.md) 相同，但不依赖于行信息。 | `docs/Reference/HTML_PRINT_ISLAND.zh.md` |
| `HTML_STRINGLEN` | HTML_STRINGLEN |  | HTML_PRINT 返回 html 渲染结果的宽度，有多行的情况下则返回第一行宽度。 | `docs/Reference/HTML_STRINGLEN.zh.md` |
| `HTML_STRINGLINES` | HTML_STRINGLINES |  | html 在 HTML_PRINT 中打印的结果，按 width（半角字符数）分割后的行数。 | `docs/Reference/HTML_STRINGLINES.zh.md` |
| `HTML_SUBSTRING` | HTML_SUBSTRING |  | 使用 HTML_PRINT 命令打印 html 时，返回不超过 width（半角字符数量）的部分。 | `docs/Reference/HTML_SUBSTRING.zh.md` |
| `HTML_TAGSPLIT` | HTML_TAGSPLIT |  | 将目标字符串解释为HTML字符串，分割为标签和纯文本，并将分割数量赋值给RESULT，分割后的字符串赋值给RESULTS。 | `docs/Reference/HTML_TAGSPLIT.zh.md` |
| `HTML_TOPLAINTEXT` | HTML_TOPLAINTEXT |  | 将目标HTML字符串转换为纯文本。 | `docs/Reference/HTML_TOPLAINTEXT.zh.md` |
| `IF` | (S)IF |  | SIF 在条件表达式成立时，执行下一行。不成立时，则跳过下一行。 | `docs/Reference/IF.zh.md` |
| `INPUT` | INPUT(S) |  | 等待输入，INPUT将输入的数字赋值给RESULT，INPUTS将输入的字符串赋值给RESULTS | `docs/Reference/INPUT.zh.md` |
| `INPUTANY` | INPUTANY |  | 同时接受整数和字符串输入的 INPUT 命令 | `docs/Reference/INPUTANY.zh.md` |
| `INPUTMOUSEKEY` | INPUTMOUSEKEY |  | INPUTMOUSEKEY 指令用于直接识别鼠标或键盘的输入。 | `docs/Reference/INPUTMOUSEKEY.zh.md` |
| `INRANGEARRAY` | INRANGEARRAY, INRANGECARRAY |  | INRANGEARRAY 返回指定数组中，值满足 minValue <= value < maxValue 的元素数量。 | `docs/Reference/INRANGEARRAY.zh.md` |
| `ISACTIVE` | ISACTIVE |  | 返回 Emuera 窗口的状态。 | `docs/Reference/ISACTIVE.zh.md` |
| `ISDEFINED` | ISDEFINED |  | 如果定义了与macroName同名的宏(#DEFINE XXX)，则返回1。如果没有定义，则返回0。 | `docs/Reference/ISDEFINED.zh.md` |
| `JUMP` | JUMP |  | 以 @ 开头的字符串定义的函数 | `docs/Reference/JUMP.zh.md` |
| `LINEISEMPTY` | LINEISEMPTY |  | 判断当前正在[PRINT](./PRINT.zh.md)的行是否为空行的指令。 | `docs/Reference/LINEISEMPTY.zh.md` |
| `LOADCHARA` | LOADCHARA |  | 第一个参数指定要加载数据的文件名（的一部分）。实际的文件名将是chara_*.dat。 | `docs/Reference/LOADCHARA.zh.md` |
| `LOADDATA` | LOADDATA |  | 加载由 saveID 指定编号的文件数据。 | `docs/Reference/LOADDATA.zh.md` |
| `LOADGLOBAL` | LOADGLOBAL |  | 加载 GLOBAL 与 GLOBALS。保存目标文件为 global.sav。 | `docs/Reference/LOADGLOBAL.zh.md` |
| `LOADTEXT` | LOADTEXT |  | LOADTEXT 命令版本会读取 textXX.sav 文件并将其结果赋值给 RESULTS:0。 | `docs/Reference/LOADTEXT.zh.md` |
| `MAP_ENHANCED` | MAP 扩展操作函数 |  | Skia（SkiaSharp版）新增的 MAP 扩展操作函数。提供批量合并、条件删除、条件查找功能。 | `docs/Reference/MAP_ENHANCED.zh.md` |
| `MAP_GETKEYS` | MAP_GETKEYS / MAP_VALUES |  | 输出 MAP（键值对映射数组，或称「字典」，[Dictionary](https://docs.microsoft.com/zh-cn/dotnet/api/system.collections.generic.dictionary-2?view=netframework-4.8)）中保存的键名（key）或值（value）。 | `docs/Reference/MAP_GETKEYS.zh.md` |
| `MAP_MANAGE` | MAP 管理相关函数 |  | 创建 / 删除 / 判断是否存在 MAP（键值对映射数组，或称「字典」，[Dictionary](https://docs.microsoft.com/zh-cn/dotnet/api/system.collections.generic.dictionary-2?view=netframework-4.8)）的一系列函数。 | `docs/Reference/MAP_MANAGE.zh.md` |
| `MAP_OPERATION` | MAP 操作相关函数 |  | 操作已保存的 MAP（键值对映射数组，或称「字典」，[Dictionary](https://docs.microsoft.com/zh-cn/dotnet/api/system.collections.generic.dictionary-2?view=netframework-4.8)）的一系列函数。 | `docs/Reference/MAP_OPERATION.zh.md` |
| `MAP_SERIALIZATION` | MAP 序列化相关函数 |  | 将 MAP（键值对映射数组，或称「字典」，[Dictionary](https://docs.microsoft.com/zh-cn/dotnet/api/system.collections.generic.dictionary-2?view=netframework-4.8)）与 XML 或字符串互相转换的函数。想把 MAP 的内容保存到文件（数据持久化）的时候可以使用。 | `docs/Reference/MAP_SERIALIZATION.zh.md` |
| `MATCH` | MATCH |  | MATCH 函数用于返回 array 指定的数组变量中，与 value 值相等的元素数量。 | `docs/Reference/MATCH.zh.md` |
| `MATCHALL` | MATCHALL / MATCHALLEX |  | 在数组中搜索所有匹配值的索引，返回匹配数量。 | `docs/Reference/MATCHALL.zh.md` |
| `MATH_EXTENSION` | 数学扩展函数 |  | 以下摘自私家改造版更新日志 | `docs/Reference/MATH_EXTENSION.zh.md` |
| `MAX` | MAX, MIN, LIMIT, INRANGE |  | MAX 返回参数中的最大值。 | `docs/Reference/MAX.zh.md` |
| `MAXMINARRAY` | MAXARRAY, MINARRAY |  | 返回数组最大值或最小值的函数。 | `docs/Reference/MAXMINARRAY.zh.md` |
| `MONEYSTR` | MONEYSTR |  | 对于参数给定的数值，将附有[已设定的货币单位](../Emuera/replace.zh.md)的字符串赋值给RESULTS:0或返回。 | `docs/Reference/MONEYSTR.zh.md` |
| `MOUSEB` | MOUSEB |  | 获取鼠标悬停中的按钮内容 | `docs/Reference/MOUSEB.zh.md` |
| `MOUSEXY` | MOUSEX, MOUSEY |  | 获取鼠标光标当前的X坐标或Y坐标。 | `docs/Reference/MOUSEXY.zh.md` |
| `ONEINPUT` | ONEINPUT(S) |  | 单字符限定输入自动处理指令 ONEINPUT、ONEINPUTS | `docs/Reference/ONEINPUT.zh.md` |
| `OUTPUTLOG` | OUTPUTLOG |  | 这是日志输出命令 OUTPUTLOG。过度使用会缩短磁盘寿命，请适度使用。 | `docs/Reference/OUTPUTLOG.zh.md` |
| `PICKUPCHARA` | PICKUPCHARA |  | 此指令仅保留参数指定的角色，并删除所有其他角色。 | `docs/Reference/PICKUPCHARA.zh.md` |
| `PLAYBGM` | PLAYBGM |  | 循环播放指定的音频文件（位于 ./sound/ 目录下）。 | `docs/Reference/PLAYBGM.zh.md` |
| `PLAYSOUND` | PLAYSOUND |  | 播放一次指定的音频文件（位于 ./sound/ 目录下）。 | `docs/Reference/PLAYSOUND.zh.md` |
| `POWER` | POWER |  | 命令和函数形式的参数不同。 | `docs/Reference/POWER.zh.md` |
| `PRINT` | PRINT 系 | `PRINT(\|V\|S\|FORM\|FORMS)(\|K\|D)(\|L\|W\|N)` | PRINT系列的基本指令。 | `docs/Reference/PRINT.zh.md` |
| `PRINTBUTTON` | PRINTBUTTON 系列 | `PRINTBUTTON(\|C\|LC)` | PRINTBUTTON 指令用于生成可通过鼠标点击的按钮。 | `docs/Reference/PRINTBUTTON.zh.md` |
| `PRINTC` | PRINTC 系列 | `PRINT(\|FORM)(C\|LC)(\|K\|D)` | 这是 PRINTC 系列命令。 | `docs/Reference/PRINTC.zh.md` |
| `PRINTCLENGTH` | PRINTCLENGTH |  | 返回配置项[PRINTC的字符数](../Emuera/config.md#printc_1)的值。与 RESULT = GETCONFIG("PRINTC的字符数") 同义。 | `docs/Reference/PRINTCLENGTH.zh.md` |
| `PRINTCPERLINE` | PRINTCPERLINE |  | 将[配置PRINTC排列数量](../Emuera/config.md#printc)中指定的数值赋值给RESULT:0，或返回该值。默认值为3。 | `docs/Reference/PRINTCPERLINE.zh.md` |
| `PRINTDATA` | PRINTDATA 系列 | `PRINTDATA(\|K\|D)(\|L\|W)` | 这是 PRINTDATA 系列指令。根据私家改造版 readme 的说明， | `docs/Reference/PRINTDATA.zh.md` |
| `PRINTN` | PRINTN 系列 | `PRINT(\|V\|S\|FORM\|FORMS)N` | 这是不换行的 PRINTW 命令。仅添加在上述基本的 PRINT 命令中。 | `docs/Reference/PRINTN.zh.md` |
| `PRINTPLAIN` | PRINTPLAIN | `PRINTPLAIN(\|FORM)` | 将参数字符串作为纯文本输出。此时即使存在按钮字符串（如0等）也不会将其按钮化。 | `docs/Reference/PRINTPLAIN.zh.md` |
| `PRINTSINGLE` | PRINTSINGLE 系列 | `PRINTSINGLE(\|V\|S\|FORM\|FORMS)(\|K\|D)` | PRINTSINGLE 系列与 PRINTL 几乎相同，但 PRINTSINGLE 系列不会对字符串进行换行，始终在一行内显示。 | `docs/Reference/PRINTSINGLE.zh.md` |
| `PRINT_IMG` | PRINT_IMG |  | 在行中显示指定的图像。 | `docs/Reference/PRINT_IMG.zh.md` |
| `PRINT_RECT` | PRINT_RECT |  | 在行内显示一个宽度为字体大小参数百分比的长方形。或者，在行内显示一个x、y、宽度、高度分别为参数百分比的长方形。 | `docs/Reference/PRINT_RECT.zh.md` |
| `PRINT_SPACE` | PRINT_SPACE |  | 创建一个宽度为参数指定字体大小百分比的无内容显示空间。 | `docs/Reference/PRINT_SPACE.zh.md` |
| `PRINT_STATUS` | PRINT_STATUS 相关函数 |  | 分别简易显示当前状态。PRINT_ABL、PRINT_TALENT、PRINT_MARK、PRINT_EXP、PRINT_PALAM 请将角色登记编号 (CharaID) 指定为参数。 | `docs/Reference/PRINT_STATUS.zh.md` |
| `PUTFORM` | PUTFORM |  | PUTFORM 只能在名为 @SAVEINFO 的特殊函数中使用。 | `docs/Reference/PUTFORM.zh.md` |
| `QUIT` | QUIT |  | 执行一次 [WAIT](./WAIT.zh.md) 后结束 Emuera | `docs/Reference/QUIT.zh.md` |
| `QUIT_AND_RESTART` | QUIT_AND_RESTART |  | 和 QUIT 一样，插入 WAIT 后重启 Emuera。 | `docs/Reference/QUIT_AND_RESTART.zh.md` |
| `RAND` | RAND |  | 与同名的变量功能几乎相同。 | `docs/Reference/RAND.zh.md` |
| `RANDOMIZE` | RANDOMIZE, DUMPRAND, INITRAND |  | 这些是用于控制通过 RAND:X 获取的随机数的指令。 | `docs/Reference/RANDOMIZE.zh.md` |
| `README` | 命令・式中函数一览 | `PRINT(\|V\|S\|FORM\|FORMS)(\|K\|D)(\|L\|W) ; PRINTSINGLE(\|V\|S\|FORM\|FORMS)(\|K\|D) ; PRINT(\|FORM)(C\|LC)(\|K\|D) ; PRINTDATA(\|K\|D)(\|L\|W)` | ![](../assets/images/Iconeramaker.webp) - eramaker 中已有的命令 | `docs/Reference/README.zh.md` |
| `REDRAW` | REDRAW, CURRENTREDRAW |  | 当参数指定为0时，抑制非强制性的绘图请求（仅在需要用户输入的时刻等强制绘图时机进行绘图）。 | `docs/Reference/REDRAW.zh.md` |
| `REGEXPMATCH` | REGEXPMATCH |  | 如果 str 符合 pattern 正则表达式规则，返回匹配到的结果数量，否则返回 0。 | `docs/Reference/REGEXPMATCH.zh.md` |
| `REPEAT` | REPEAT-REND |  | REPEAT～REND之间的代码块，将按照参数指定的次数进行循环。循环次数被记录在COUNT变量中。 | `docs/Reference/REPEAT.zh.md` |
| `REPLACE` | REPLACE |  | 在目标字符串中搜索目标模式，如果匹配成功，则用替换字符串进行替换。 | `docs/Reference/REPLACE.zh.md` |
| `RESETDATA` | RESETDATA |  | 初始化除全局变量外的所有变量。 | `docs/Reference/RESETDATA.zh.md` |
| `RESETGLOBAL` | RESETGLOBAL |  | 具体来说，将数值型全局变量赋值为0，将字符串型全局变量赋值为空字符串。 | `docs/Reference/RESETGLOBAL.zh.md` |
| `RESET_STAIN` | RESET_STAIN |  | 这是初始化第1个参数所指定角色的STAIN的指令。初始值与BEGIN TRAIN时赋入的值相同，可通过[_replace.csv的污渍初始值](../Emuera/replace.zh.md)进行指定。 | `docs/Reference/RESET_STAIN.zh.md` |
| `RESTART` | RESTART |  | 返回当前正在执行的函数的开头。使用DYNAMIC定义的动态变量不会被初始化 | `docs/Reference/RESTART.zh.md` |
| `RETURN` | RETURN |  | 将参数指定的值赋值给 RESULT，并结束正在执行的函数。 | `docs/Reference/RETURN.zh.md` |
| `REUSELASTLINE` | REUSELASTLINE |  | 使用指定的格式化字符串重写最后一行， | `docs/Reference/REUSELASTLINE.zh.md` |
| `SAVECHARA` | SAVECHARA |  | 将指定角色的数据保存到文件的指令。 | `docs/Reference/SAVECHARA.zh.md` |
| `SAVEDATA` | SAVEDATA |  | 将当前状态保存到由 saveID 指定编号的文件中。 | `docs/Reference/SAVEDATA.zh.md` |
| `SAVEGAME` | SAVEGAME, LOADGAME |  | SAVEGAME 用于呼出存档画面，LOADGAME 用于呼出读档画面。两者都只能在 SHOP 状态下调用。 | `docs/Reference/SAVEGAME.zh.md` |
| `SAVEGLOBAL` | SAVEGLOBAL |  | 保存 GLOBAL 和 GLOBALS 变量。保存目标为 global.sav。 | `docs/Reference/SAVEGLOBAL.zh.md` |
| `SAVENOS` | SAVENOS |  | 作为命令时，获取配置[显示存档数据数量](../Emuera/config.md#_10)中指定的数量，并赋值给指定的数值变量。默认值为20。 | `docs/Reference/SAVENOS.zh.md` |
| `SAVETEXT` | SAVETEXT |  | 将 text 指定的文本保存到文件名为 textXX.txt 的文件中（例如，如果 fileNo 为 2，则文件名为 text02.txt）。 | `docs/Reference/SAVETEXT.zh.md` |
| `SELECTCASE` | SELECTCASE |  | 这是一个分支结构。其行为模仿了 Visual Basic 的同名结构。 | `docs/Reference/SELECTCASE.zh.md` |
| `SEQUENCEINPUT` | SEQUENCEINPUT ![](../assets/images/IconSK.webp) |  | 在下一次输入等待（INPUT/TINPUT/INPUTS/TINPUTS等）时，将指定字符串作为用户输入自动提交。调用 SEQUENCEINPUT 后，下一次进入 WaitInput 状态时，引擎调用 PressEnterKey 处理排队的字符串，行为与在文本框中输入并按回车一致。 | `docs/Reference/SEQUENCEINPUT.zh.md` |
| `SETANIMETIMER` | SETANIMETIMER / GETANIMETIMER |  | 为动画精灵指定以毫秒为单位的重绘间隔。 | `docs/Reference/SETANIMETIMER.zh.md` |
| `SETBGCOLOR` | SETBGCOLOR |  | 此命令用于将背景色更改为指定颜色。 | `docs/Reference/SETBGCOLOR.zh.md` |
| `SETBGMVOLUME` | SETBGMVOLUME |  | 将 PLAYBGM 的音量设置为 0 ～ 100 之间。 | `docs/Reference/SETBGMVOLUME.zh.md` |
| `SETCOLOR` | SETCOLOR, RESETCOLOR |  | 将文字颜色更改为指定颜色，该设置将持续生效，直到调用RESETCOLOR。 | `docs/Reference/SETCOLOR.zh.md` |
| `SETCOLORBYNAME` | SETCOLORBYNAME, SETBGCOLORBYNAME |  | 此指令用于根据预定义的颜色名称来指定字体显示颜色或背景颜色。 | `docs/Reference/SETCOLORBYNAME.zh.md` |
| `SETFONT` | SETFONT 系命令 |  | CHKFONT 用于检查指定名称的字体是否已安装。 | `docs/Reference/SETFONT.zh.md` |
| `SETIMAGELAYER` | SETIMAGELAYER |  | 在独立图层上渲染指定 Sprite。与 [CBGSETSPRITE](./CBGSETSPRITE.zh.md) 不同，SETIMAGELAYER 的图层与文本行解耦，支持视口裁剪和跟随滚动。 | `docs/Reference/SETIMAGELAYER.zh.md` |
| `SETIMAGELAYERL` | SETIMAGELAYERL |  | [SETIMAGELAYER](./SETIMAGELAYER.zh.md) 的行相对定位版本。自动设置 followScroll=1，始终锚定当前显示行。定位参数 xpos/ypos 为相对行位置的偏移，与 [HTML_PRINT](./HTML_PRINT.zh.md) 的 标签的 xpos/ypos 属性语义一致。当 xpos=0, ypos=0 时，渲染位置与同行的 完全一致（包括 ShapePositionShift 偏移）。 | `docs/Reference/SETIMAGELAYERL.zh.md` |
| `SETSOUNDVOLUME` | SETSOUNDVOLUME |  | 将 PLAYSOUND 的音量设置为 0 ～ 100 之间。 | `docs/Reference/SETSOUNDVOLUME.zh.md` |
| `SKIA_RENDER` | SET_TEXT_DRAWING_MODE / SET_SKIA_QUALITY |  | Skia（SkiaSharp版）新增的渲染控制 API。动态控制文本的渲染管线和 SkiaSharp 质量参数。 | `docs/Reference/SKIA_RENDER.zh.md` |
| `SKIPLOG` | SKIPLOG |  | 用于手动控制通过左键点击等方式跳过日志的状态。非0值启用跳过，0值解除跳过状态。 | `docs/Reference/SKIPLOG.zh.md` |
| `SKIP_RELATE` | SKIP系 |  | PRINT等画面输出指令以及WAIT、TWAIT等与控制相关的指令群。 | `docs/Reference/SKIP_RELATE.zh.md` |
| `SORTCHARA` | SORTCHARA |  | 根据任意键对角色列表进行排序。 | `docs/Reference/SORTCHARA.zh.md` |
| `SOUNDCONTROL` | SOUNDCONTROL, BGMCONTROL, GETSOUNDORBGMINFO, ISPLAYINGSOUND, ISPLAYINGBGM |  | 控制声音通道的播放。 | `docs/Reference/SOUNDCONTROL.zh.md` |
| `SPLIT` | SPLIT, STRJOIN |  | SPLIT 命令将第一个参数指定的字符串，以第二个参数指定的字符串作为分隔符进行分割，并将结果赋值给第三个参数指定的字符串数组变量。 | `docs/Reference/SPLIT.zh.md` |
| `SPRITEANIMEADDFRAME` | SPRITEANIMEADDFRAME |  | 向spriteName指定的资源名所对应的动画精灵添加帧。 | `docs/Reference/SPRITEANIMEADDFRAME.zh.md` |
| `SPRITEANIMECREATE` | SPRITEANIMECREATE |  | 创建一个动画精灵，其资源名由 spriteName 指定，尺寸由 width 和 height 指定。创建成功时返回非0值。 | `docs/Reference/SPRITEANIMECREATE.zh.md` |
| `SPRITECREATE` | SPRITECREATE |  | 基于 gID 所指定的 Graphics 图像的全部或部分，创建一个资源名为 spriteName 的精灵。 | `docs/Reference/SPRITECREATE.zh.md` |
| `SPRITECREATED` | SPRITECREATED |  | 若指定名称的精灵已创建则返回1，若未创建或已销毁则返回0。 | `docs/Reference/SPRITECREATED.zh.md` |
| `SPRITECREATEFROMFILE` | SPRITECREATEFROMFILE |  | 直接从图像文件创建 Sprite。可以一步完成 [GCREATEFROMFILE](./GCREATEFROMFILE.zh.md) 创建 Graphics 再用 [SPRITECREATE](./SPRITECREATE.zh.md) 创建 Sprite 的两步操作。 | `docs/Reference/SPRITECREATEFROMFILE.zh.md` |
| `SPRITEDISPOSE` | SPRITEDISPOSE |  | 废弃（释放）由 spriteName 指定的资源名所对应的精灵。 | `docs/Reference/SPRITEDISPOSE.zh.md` |
| `SPRITEDISPOSEALL` | SPRITEDISPOSEALL |  | 销毁所有 SPRITE。若参数为 0，则仅销毁 ERB 上创建的 SPRITE；若参数非 0，则同时销毁 resources 内 CSV 创建的所有 SPRITE。 | `docs/Reference/SPRITEDISPOSEALL.zh.md` |
| `SPRITEGETCOLOR` | SPRITEGETCOLOR |  | 获取指定spriteName资源名对应的精灵在指定位置的颜色，以0xAARRGGBB格式的整数值返回。 | `docs/Reference/SPRITEGETCOLOR.zh.md` |
| `SPRITEMOVE` | SPRITEMOVE |  | 将指定的值加到指定名称的精灵的相对位置的X、Y坐标上。 | `docs/Reference/SPRITEMOVE.zh.md` |
| `SPRITEPOSXY` | SPRITEPOSX, SPRITEPOSY |  | 获取指定名称的精灵的相对位置的 X、Y 坐标。 | `docs/Reference/SPRITEPOSXY.zh.md` |
| `SPRITESETPOS` | SPRITESETPOS |  | 设置指定名称的精灵的相对位置 X、Y。 | `docs/Reference/SPRITESETPOS.zh.md` |
| `SPRITEWIDTHHEIGHT` | SPRITEWIDTH, SPRITEHEIGHT |  | 获取指定名称的精灵的宽度或高度。 | `docs/Reference/SPRITEWIDTHHEIGHT.zh.md` |
| `SQL_CONNECT` | SQL 连接管理 |  | SQLite 数据库的连接与断开相关函数。 | `docs/Reference/SQL_CONNECT.zh.md` |
| `SQL_EXECUTE` | SQL 执行操作 |  | SQLite 数据库的 SQL 语句执行相关函数。 | `docs/Reference/SQL_EXECUTE.zh.md` |
| `SQL_PARAM` | SQL 参数化查询 |  | SQLite 参数化查询相关函数，用于防止 SQL 注入攻击。 | `docs/Reference/SQL_PARAM.zh.md` |
| `SQL_READER` | SQL Reader 操作 |  | SQLite 查询结果（Reader）的读取与操作相关函数。 | `docs/Reference/SQL_READER.zh.md` |
| `SQL_XML` | SQL XML 导入导出 |  | SQLite 数据库与 XML 文件之间的导入导出相关函数。支持 MAP 格式、DataTable 格式和自定义格式的 XML 互操作。 | `docs/Reference/SQL_XML.zh.md` |
| `SQRT` | SQRT |  | 返回参数的平方根。由于小数部分会被舍去，建议在使用前先将数值放大。 | `docs/Reference/SQRT.zh.md` |
| `STOPBGM` | STOPBGM |  | 停止 PLAYBGM 正在播放的音轨。 | `docs/Reference/STOPBGM.zh.md` |
| `STOPCALLTRAIN` | STOPCALLTRAIN |  | 如果在 [CALLTRAIN](./CALLTRAIN.zh.md) 指令正在运行时被调用，则会立即终止 CALLTRAIN 的处理。 | `docs/Reference/STOPCALLTRAIN.zh.md` |
| `STOPSOUND` | STOPSOUND |  | 停止 PLAYSOUND 正在播放的音轨。 | `docs/Reference/STOPSOUND.zh.md` |
| `STRCOUNT` | STRCOUNT |  | 获取字符串中指定子字符串的数量的指令。将匹配的数量赋值给RESULT:0或返回该值。 | `docs/Reference/STRCOUNT.zh.md` |
| `STRDATA` | STRDATA |  | 此指令用于将字符串赋值给指定的字符串型变量，而非使用 [PRINTDATA](./PRINTDATA.zh.md) 来显示字符串。 | `docs/Reference/STRDATA.zh.md` |
| `STRFIND` | STRFIND |  | 第一参数指定被搜索的目标字符串，使用字符串表达式。第二参数指定要搜索的字符串，使用字符串表达式。 | `docs/Reference/STRFIND.zh.md` |
| `STRFORM` | STRFORM |  | 将给定的字符串视为与PRINTFORM等相同的格式化字符串，并返回展开后的字符串。 | `docs/Reference/STRFORM.zh.md` |
| `STRICT_FONT_FALLBACK` | STRICT_FONT_FALLBACK |  | 切换字体回退的严格模式。 | `docs/Reference/STRICT_FONT_FALLBACK.zh.md` |
| `STRLEN` | STRLEN系 |  | STRLEN、STRLENS、STRLENFORM 用于测量字符串长度，并将结果赋值给 RESULT:0。 | `docs/Reference/STRLEN.zh.md` |
| `SUBSTRING` | SUBSTRING |  | 返回指定字符串表达式中，从第一个参数指定的位置开始、长度为第二个参数指定字符数的子字符串。 | `docs/Reference/SUBSTRING.zh.md` |
| `SUMARRAY` | SUMARRAY |  | 此函数用于返回数组值的总和。 | `docs/Reference/SUMARRAY.zh.md` |
| `SWAP` | SWAP |  | 交换变量1和变量2的内容。 | `docs/Reference/SWAP.zh.md` |
| `SWAPCHARA` | SWAPCHARA |  | 交换指定两个角色的登记编号 (CharaID)。 | `docs/Reference/SWAPCHARA.zh.md` |
| `TEXTBOX` | 输入框相关命令 |  | SETTEXTBOX：将输入框内容替换为 text。 | `docs/Reference/TEXTBOX.zh.md` |
| `TEXT_BGC` | TEXT_BGC_ON / TEXT_BGC_OFF |  | TEXT_BGC_ON 为后续所有行设置整行背景色。TEXT_BGC_OFF 清除背景色，恢复透明。 | `docs/Reference/TEXT_BGC.zh.md` |
| `THROW` | THROW |  | 此命令会强制引发错误，并使用给定的参数字符串进行错误显示。 | `docs/Reference/THROW.zh.md` |
| `TIMES` | TIMES |  | 将第二参数的浮点数乘以第一参数的变量。默认设置下会舍去小数部分。 | `docs/Reference/TIMES.zh.md` |
| `TINPUT` | TINPUT(S) |  | 这是带有时间限制的输入接收命令。第一个参数是时间限制（毫秒），但即使设置小于100ms的值也无法精确运作。 | `docs/Reference/TINPUT.zh.md` |
| `TINPUTNF` | TINPUT(S)NF |  | 与 [TINPUT](TINPUT.zh.md) / [TINPUTS](TINPUT.zh.md) 功能完全相同，但不强制滚动到底部。 | `docs/Reference/TINPUTNF.zh.md` |
| `TOINT` | TOINT, ISNUMERIC, TOFLOAT |  | TOINT 将参数字符串数值化，并将结果赋值给 RESULT:0 或直接返回。但是，只有由半角数字构成的字符串才能被数值化。 | `docs/Reference/TOINT.zh.md` |
| `TONEINPUT` | TONEINPUT |  | 参数分别与 [TINPUT、TINPUTS](./TINPUT.zh.md) 相同。 | `docs/Reference/TONEINPUT.zh.md` |
| `TONEINPUTNF` | TONEINPUT(S)NF |  | 与 [TONEINPUT](TONEINPUT.zh.md) / [TONEINPUTS](TONEINPUT.zh.md) 功能完全相同，但不强制滚动到底部。 | `docs/Reference/TONEINPUTNF.zh.md` |
| `TOOLTIP_EXTENSION` | TOOLTIPS 功能扩展 |  | HTML_PRINT 的提示框功能扩展。 | `docs/Reference/TOOLTIP_EXTENSION.zh.md` |
| `TOOLTIP_SET` | TOOLTIP_SETDELAY, TOOLTIP_SETDURATION |  | TOOLTIP_SETDELAY 用于设置工具提示显示前的延迟时间，单位为毫秒。 | `docs/Reference/TOOLTIP_SET.zh.md` |
| `TOOLTIP_SETCOLOR` | TOOLTIP_SETCOLOR |  | 设置工具提示的前景色和背景色，使用 0xRRGGBB 格式的数值。第一个参数是文字颜色，第二个参数是背景颜色。 | `docs/Reference/TOOLTIP_SETCOLOR.zh.md` |
| `TOSTR` | TOSTR |  | 将数值转换为字符串的命令。 | `docs/Reference/TOSTR.zh.md` |
| `TOUPPER` | TOUPPER, TOLOWER, TOHALF, TOFULL |  | 将参数字符串进行特定转换后的结果赋值给 RESULTS:0 或作为返回值。 | `docs/Reference/TOUPPER.zh.md` |
| `TRY` | TRYJUMP, TRYCALL, TRYGOTO |  | 与 [JUMP](./JUMP.zh.md)、[CALL](./CALL.zh.md)、[GOTO](./GOTO.zh.md) 相同，但即使指定的函数不存在也不会报错。 | `docs/Reference/TRY.zh.md` |
| `TRYC` | TRYC系 |  | TRYC 系列指令可以在函数调用时，控制当函数未找到时的行为。 | `docs/Reference/TRYC.zh.md` |
| `TRYCALLF` | TRYCALLF |  | 附加 TRY 功能的 CALLF 函数。 | `docs/Reference/TRYCALLF.zh.md` |
| `TRYCALLFORMF` | TRYCALLFORMF |  | 附加 TRY 功能的 CALLFORMF 函数。 | `docs/Reference/TRYCALLFORMF.zh.md` |
| `TRYFORM` | TRYCALLFORM, TRYJUMPFORM, TRYGOTOFORM |  | 与 [JUMP](./JUMP.zh.md)、[CALL](./CALL.zh.md)、[GOTO](./GOTO.zh.md) 相同，但可以像 [PRINTFORM](./PRINT.zh.md) 一样指定函数名，即使函数不存在也不会报错。 | `docs/Reference/TRYFORM.zh.md` |
| `TRYLIST` | TRYLIST系 |  | 这是一个用于指定多个函数（标签）并仅调用第一个找到的函数的语法。 | `docs/Reference/TRYLIST.zh.md` |
| `TWAIT` | TWAIT |  | 第一参数为限制时间，第二参数为输入接收标志。 | `docs/Reference/TWAIT.zh.md` |
| `UNCHECKED` | UNCHECKED 计算 |  | Skia（SkiaSharp版）新增。在 C# 的 unchecked 上下文中执行运算，溢出时不抛出异常，而是回环折返（wrap-around）。 | `docs/Reference/UNCHECKED.zh.md` |
| `UNICODE` | UNICODE, ENCODETOUNI |  | UNICODE 是根据参数值返回对应 Unicode 字符的命令/式中函数。 | `docs/Reference/UNICODE.zh.md` |
| `UPCHECK` | UPCHECK |  | 将TARGET的UP、DOWN状态值累加到PALAM中，并显示增减量 | `docs/Reference/UPCHECK.zh.md` |
| `UPDATECHECK` | UPDATECHECK |  | 从 GameBase.csv 配置的 バージョン情報URL 获取最新版本信息，如果当前版本不是最新版则弹出对话框提醒更新。 | `docs/Reference/UPDATECHECK.zh.md` |
| `VAR` | VARI,VARS |  | 可以在函数中的任意位置定义函数本地的动态变量。 | `docs/Reference/VAR.zh.md` |
| `VARSET` | VARSET |  | 将第二参数的值赋值给指定变量数组的指定范围。 | `docs/Reference/VARSET.zh.md` |
| `VARSETEX` | VARSETEX |  | 与本家的 [VARSET](https://osdn.net/projects/emuera/wiki/excom#h5-VARSET.20.3C.E5.A4.89.E6.95.B0.E5.90.8D.3E.7B.2C.20.3C.E6.95.B0.E5.BC.8F.20or.20.E6.96.87.E5.AD.97.E5.88.97.E5.BC.8F.3E.2C.20.3C.E9.85.8D.E5.88.97.E7.AF.84.E5.9B.B2.E5.88.9D.E5.80.A4.3E.2C.20.3C.E9.85.8D.E5.88.97.E7.AF.84.E5.9B.B2.E7.B5.82.E5.80.A4.2B1.3E.7D) 类似，将名为 varName（字符串）的变量赋值为 value，而不是直接使用变量标识符。 | `docs/Reference/VARSETEX.zh.md` |
| `VARSIZE` | VARSIZE |  | 命令和表达式中函数的规格不同。 | `docs/Reference/VARSIZE.zh.md` |
| `WAIT` | WAIT |  | 等待一次鼠标点击或 Enter 键输入 | `docs/Reference/WAIT.zh.md` |
| `WAITANYKEY` | WAITANYKEY |  | 等待任意按键输入或鼠标点击的 [WAIT](./WAIT.zh.md) 指令。 | `docs/Reference/WAITANYKEY.zh.md` |
| `WHILE` | WHILE-WEND |  | 这是类似于 [REPEAT～REND](./REPEAT.zh.md) 或 [FOR～NEXT](./FOR.zh.md) 的一种循环结构。 | `docs/Reference/WHILE.zh.md` |
| `XML_ADDATTRIBUTE` | XML_ADDATTRIBUTE 系列 |  | 根据 xpath 选择的元素节点 / 属性（详见 [XPath 的介绍](https://www.octoparse.jp/blog/xpath-introduction)）添加新的属性「attrName=attrValue」到指定的 XML 中。省略参数 attrValue 时，新增的属性值默认设为空字符串。当 xpath 的匹配结果存在多个时，必须将参数 doSetAll 设为 0 以外的数值才能成功新增属性。 | `docs/Reference/XML_ADDATTRIBUTE.zh.md` |
| `XML_ADDNODE` | XML_ADDNODE 系列 |  | 根据 xpath 选择的元素节点（详见 [XPath 的介绍](https://www.octoparse.jp/blog/xpath-introduction)）添加新的元素节点到指定的 XML 中。当 xpath 的匹配结果存在多个时，必须将参数 doSetAll 设为 0 以外的数值才能成功新增节点。 | `docs/Reference/XML_ADDNODE.zh.md` |
| `XML_GET` | XML_GET 系列 |  | 根据 xpath 选择的元素节点（详见 [XPath 的介绍](https://www.runoob.com/xpath/xpath-tutorial.html)）在指定的 XML 中检索。 | `docs/Reference/XML_GET.zh.md` |
| `XML_MANAGE` | XML_DOCUMENT 处理系列 |  | 关于 [XmlDocument](https://docs.microsoft.com/zh-cn/dotnet/api/system.xml.xmldocument?view=netframework-4.8) 的生成、删除、判断是否存在的一系列函数。若 xmlId 为整数，则使用其字符串转换结果值([TOSTR](https://osdn.net/projects/emuera/wiki/exmeth#h5-str.20TOSTR.28int.20value.2C.20str.20format.20.3D.20.22.22.29))。 | `docs/Reference/XML_MANAGE.zh.md` |
| `XML_REMOVEATTRIBUTE` | XML_REMOVEATTRIBUTE 系列 |  | 从指定的 XML 中删除 xpath 选择的属性（详见 [XPath 的介绍](https://www.octoparse.jp/blog/xpath-introduction)）。当 xpath 的匹配结果存在多个时，必须将参数 doSetAll 设为 0 以外的数值才能成功删除属性。删除属性成功时，返回已删除属性的数量；失败时返回 0。 | `docs/Reference/XML_REMOVEATTRIBUTE.zh.md` |
| `XML_REMOVENODE` | XML_REMOVENODE 系列 |  | 从指定的 XML 中删除（根节点除外）xpath 选择的节点（详见 [XPath 的介绍](https://www.octoparse.jp/blog/xpath-introduction)）。 | `docs/Reference/XML_REMOVENODE.zh.md` |
| `XML_REPLACE` | XML_REPLACE 系列 |  | 从指定的 XML 中将 xpath 选择的节点（详见 [XPath 的介绍](https://www.octoparse.jp/blog/xpath-introduction)）替换为参数 newXml（新的 XML 文本）。当 xpath 的匹配结果存在多个时，必须将参数 doSetAll 设为 0 以外的数值才能成功更新节点。更新节点成功时，返回已更新节点的数量；失败时返回 0。 | `docs/Reference/XML_REPLACE.zh.md` |
| `XML_SET` | XML_SET 系列 |  | 从指定的 XML 中将 xpath 选择的节点（详见 [XPath 的介绍](https://www.octoparse.jp/blog/xpath-introduction)）内容设为 value。当 xpath 的匹配结果存在多个时，必须将参数 doSetAll 设为 0 以外的数值才能成功更新节点。更新节点成功时，返回已更新节点的数量；失败时返回 0。 | `docs/Reference/XML_SET.zh.md` |
| `XML_TOSTR` | XML_TOSTR |  | 以 XML 文本形式返回 xmlId 指定的 [XmlDocument](https://docs.microsoft.com/zh-cn/dotnet/api/system.xml.xmldocument?view=netframework-4.8) 中保存的内容。若 xmlId 为整数，则使用其字符串转换结果值([TOSTR](https://osdn.net/projects/emuera/wiki/exmeth#h5-str.20TOSTR.28int.20value.2C.20str.20format.20.3D.20.22.22.29))。 | `docs/Reference/XML_TOSTR.zh.md` |

## 教程（28 篇）

| 名称 | 标题 | 签名 | 摘要 | 路径 |
|---|---|---|---|---|
| `assignment` | 赋值语句 |  | Reference 分类: [算术](../Reference/README.zh.md#arithmetic) | `docs/tutorial/assignment.zh.md` |
| `basic-output` | 基本输出 |  | Reference 分类: [PRINT 系列](../Reference/README.zh.md#print) / [显示操作・字体操作](../Reference/README.zh.md#display-font) | `docs/tutorial/basic-output.zh.md` |
| `call` | 函数与 CALL |  | Reference 分类: [函数系列（CALL 等）](../Reference/README.zh.md#function-call) / [RETURN 系列](../Reference/README.zh.md#return) / [输入・等待](../Reference/README.zh.md#input-wait) | `docs/tutorial/call.zh.md` |
| `character-variables` | 角色变量 |  | Reference 分类: [角色操作・引用](../Reference/README.zh.md#character-operations) / [变量操作・CSV 引用](../Reference/README.zh.md#variable-operations) | `docs/tutorial/character-variables.zh.md` |
| `command-vs-expression` | 命令 vs 表达式 — 两种求值路径的根本差异 |  | Reference 分类: [函数系列（CALL 等）](../Reference/README.zh.md#function-call) | `docs/tutorial/command-vs-expression.zh.md` |
| `condition` | 条件分支 |  | Reference 分类: [循环・分支语法](../Reference/README.zh.md#flow-control) | `docs/tutorial/condition.zh.md` |
| `constant-folding` | 常量折叠（Constant Folding） |  | Reference 分类: [变量声明系列](../Reference/README.zh.md#variable-operations) | `docs/tutorial/constant-folding.zh.md` |
| `dynamic-reflection` | 动态解析与反射 |  | Reference 分类: [变量操作・CSV 引用](../Reference/README.zh.md#variable-operations) / [字符串操作・引用](../Reference/README.zh.md#string-operations) | `docs/tutorial/dynamic-reflection.zh.md` |
| `erb-format-extension` | ERB 文件格式扩展 |  | Reference 分类: [存档操作](../Reference/README.zh.md#save-data) / [图像处理相关](../Reference/README.zh.md#image) / [音频系列](../Reference/README.zh.md#sound) | `docs/tutorial/erb-format-extension.zh.md` |
| `event-functions` | 事件函数 |  | Reference 分类: [调试辅助・系统流程控制](../Reference/README.zh.md#debug-system-flow) | `docs/tutorial/event-functions.zh.md` |
| `evolution` | 版本演进对照 |  | 比较 ERABASIC 生态各版本的功能演进。以 Emuera 为基准线，整理 EM+EE 及各变体的扩展。 | `docs/tutorial/evolution.zh.md` |
| `file-types` | 文件类型与处理顺序 |  | [ERB 书式](../eramaker/ERB_format.zh.md) — ERB 文件格式 | `docs/tutorial/file-types.zh.md` |
| `form-syntax` | FORM 语法（格式化字符串） |  | Reference 分类: [字符串操作・引用](../Reference/README.zh.md#string-operations) | `docs/tutorial/form-syntax.zh.md` |
| `hello-world` | Hello World |  | [ERB 书式](../eramaker/ERB_format.zh.md) — eramaker 的 ERB 格式（历史参考） | `docs/tutorial/hello-world.zh.md` |
| `html-syntax` | HTML 标签语法参考 |  | Reference 分类: [HTML 系列](../Reference/README.zh.md#html-related) / [图像处理相关](../Reference/README.zh.md#image) | `docs/tutorial/html-syntax.zh.md` |
| `index` | ERABASIC 教程 |  | 本教程以 Emuera 为基准线，按照 Emuera → EM+EE → 各变体 的演进路线组织。eramaker 仅作为历史参考。 | `docs/tutorial/index.zh.md` |
| `interaction` | 交互系统：INPUT 与 AWAIT |  | Reference 分类: [输入・等待](../Reference/README.zh.md#input-wait) / [AWAIT 相关](../Reference/README.zh.md#await) | `docs/tutorial/interaction.zh.md` |
| `intro` | ERABASIC 简介 |  | [函数·预处理器](../Emuera/function.zh.md) — 函数声明的完整规格 | `docs/tutorial/intro.zh.md` |
| `jump` | 跳转 |  | Reference 分类: [循环・分支语法](../Reference/README.zh.md#flow-control) | `docs/tutorial/jump.zh.md` |
| `line-types` | 行类型与结构 |  | [函数·预处理器](../Emuera/function.zh.md) — 函数与预处理行的完整规格 | `docs/tutorial/line-types.zh.md` |
| `loop` | 循环 |  | Reference 分类: [循环・分支语法](../Reference/README.zh.md#flow-control) | `docs/tutorial/loop.zh.md` |
| `method-safety` | 函数安全性与 METHOD_SAFE |  | Reference 分类: [函数系列（CALL 等）](../Reference/README.zh.md#function-call) | `docs/tutorial/method-safety.zh.md` |
| `rename-macro` | Rename 宏：[[名字]] 编译期替换 |  | [文件类型与处理顺序](file-types.zh.md) — CSV/ERH/ERB 的配置与读取顺序 | `docs/tutorial/rename-macro.zh.md` |
| `resources` | 资源设置 — 图像资源的准备方法 |  | 前置章节：[HTML 标签语法](html-syntax.zh.md)（ 标签的 src 属性引用资源名） | `docs/tutorial/resources.zh.md` |
| `runtime-mechanics` | 运行时机制 |  | Reference 分类: [函数系列（CALL 等）](../Reference/README.zh.md#function-call) / [RETURN 系列](../Reference/README.zh.md#return) | `docs/tutorial/runtime-mechanics.zh.md` |
| `system-flow` | 状态机流程 |  | Reference 分类: [调试辅助・系统流程控制](../Reference/README.zh.md#debug-system-flow) | `docs/tutorial/system-flow.zh.md` |
| `values-types` | 值、类型与变量 |  | [变量规格](../Emuera/variables.zh.md) — 内置变量完整列表 | `docs/tutorial/values-types.zh.md` |
| `variable-declaration` | 变量声明系统 |  | Reference 分类: [变量操作・CSV 引用](../Reference/README.zh.md#variable-operations) | `docs/tutorial/variable-declaration.zh.md` |

## 手册/杂项（15 篇）

| 名称 | 标题 | 签名 | 摘要 | 路径 |
|---|---|---|---|---|
| `Emuera-etc` | Emuera 补充说明 |  | [eratoho总结 V3 Emuera 补充说明](https://seesaawiki.jp/eratoho/d/Emuera%a4%cb%a4%c4%a4%a4%a4%c6%a4%ce%ca%e4%c2%ad) | `docs/manual/Emuera-etc.zh.md` |
| `HowToUseGit` | git是什么 |  | [eratoho汇总 V3 Git的使用方法](https://seesaawiki.jp/eratoho/d/Git%a4%ce%bb%c8%a4%a4%a4%ab%a4%bf) | `docs/manual/HowToUseGit.zh.md` |
| `LTOL-license` | 关于LTOL许可证 |  | [eratoho汇总 V3 LTOL许可证](https://seesaawiki.jp/eratoho/d/LTOL%a5%e9%a5%a4%a5%bb%a5%f3%a5%b9%a4%cb%a4%c4%a4%a4%a4%c6) | `docs/manual/LTOL-license.zh.md` |
| `README` | 制作手册 |  | 计划整理在era制作中可参考的手册 | `docs/manual/README.zh.md` |
| `WhatIsLicense` | 关于许可证 |  | //wiki的许可证页面是LTOL页面， | `docs/manual/WhatIsLicense.zh.md` |
| `eratohowiki-ERB-QandA` | ERB开发Q&A |  | [eratoho总结 V3 ERB开发Q&A](https://seesaawiki.jp/eratoho/d/ERB%b3%ab%c8%afQ%26A) | `docs/manual/eratohowiki-ERB-QandA.zh.md` |
| `eratohowiki-ERBmanual` | ERB语法讲座 |  | 这部分几乎是直接复制过来的，需要调整 | `docs/manual/eratohowiki-ERBmanual.zh.md` |
| `erawiki-ERBmanual` | 变体制作/ERB制作实践篇 |  | [era系列相关话题讨论汇总Wiki V3 ERB制作实践篇](https://seesaawiki.jp/eraseries/d/ERB%c0%bd%ba%ee%bc%c2%c1%a9%ca%d4) | `docs/manual/erawiki-ERBmanual.zh.md` |
| `erawiki-modification-QandA` | 系统改造 Q&A |  | [era 系列讨论串 总结 Wiki V3 系统改造 Q&A](https://seesaawiki.jp/eraseries/d/%a5%b7%a5%b9%a5%c6%a5%e0%b2%fe%c2%a4Q%26A) | `docs/manual/erawiki-modification-QandA.zh.md` |
| `erawiki-title` | 制作变体/标题准备篇 |  | [era系列讨论汇总Wiki V3 标题准备篇](https://seesaawiki.jp/eraseries/d/%a5%bf%a5%a4%a5%c8%a5%eb%bd%e0%c8%f7%ca%d4) | `docs/manual/erawiki-title.zh.md` |
| `erawiki-title2` | 变体制作/标题实践篇 |  | [era系列讨论汇总Wiki V3 标题实践篇](https://seesaawiki.jp/eraseries/d/%a5%bf%a5%a4%a5%c8%a5%eb%bc%c2%c1%a9%ca%d4) | `docs/manual/erawiki-title2.zh.md` |
| `erawiki-tutorial` | 变体制作/教程 |  | [era系列讨论汇总Wiki V3 教程](https://seesaawiki.jp/eraseries/d/%a5%c1%a5%e5%a1%bc%a5%c8%a5%ea%a5%a2%a5%eb) | `docs/manual/erawiki-tutorial.zh.md` |
| `erawiki-vscode-git` | 使用VSCode进行git操作 |  | 本页面总结了Discord某个服务器的发言 | `docs/manual/erawiki-vscode-git.zh.md` |
| `glossary` | 术语集 |  | 想要添加的项目请发送至[Discord](https://discord.com/channels/428432103042973706/1236190714954514452) | `docs/manual/glossary.zh.md` |
| `modification-manual` | 改造入门 |  | [era系列讨论汇总Wiki V3 改造入门](https://seesaawiki.jp/eraseries/d/%b2%fe%c2%a4%c6%fe%cc%e7) | `docs/manual/modification-manual.zh.md` |

## Emuera 本体（21 篇）

| 名称 | 标题 | 签名 | 摘要 | 路径 |
|---|---|---|---|---|
| `ERH` | 头文件 |  | 在ERB文件夹中，除了扩展名为ERB的文件外，还可以放置扩展名为ERH的文件。 | `docs/Emuera/ERH.zh.md` |
| `HTML_PRINT` | HTML_PRINT相关 |  | 这里介绍以HTML_PRINT命令为首的html相关命令。 | `docs/Emuera/HTML_PRINT.zh.md` |
| `README` |  |  |  | `docs/Emuera/README.zh.md` |
| `config` | 运行设置(emuera.config) |  | Emuera在首次启动时会在exe文件同一文件夹下创建emuera.config文件。 | `docs/Emuera/config.zh.md` |
| `config_files` | 配置设置的强制设定 |  | 当Emuera检测到csv文件夹内存在名为_fixed.config和/或_default.config的文件时，将会读取这些文件。 | `docs/Emuera/config_files.zh.md` |
| `debug` | 调试模式 |  | 调试模式是在ver 1.750中新增的模式。 | `docs/Emuera/debug.zh.md` |
| `debugCom` | 调试命令 |  | ※默认情况下无法使用调试命令。 | `docs/Emuera/debugCom.zh.md` |
| `differences_of_Emuera_and_eramaker` | 与eramaker的差异点 |  | 在eramaker中，如果数组的最后一个元素不是0，加载时数据会被破坏。 | `docs/Emuera/differences_of_Emuera_and_eramaker.zh.md` |
| `expression` | Emuera中新增的语法 |  | A = B ;将B赋值给A | `docs/Emuera/expression.zh.md` |
| `function` | 函数·预处理器 |  | 数据加载完成后立即调用。 | `docs/Emuera/function.zh.md` |
| `glossary` | 术语表 |  | 这是本Wiki中术语的汇总。 | `docs/Emuera/glossary.zh.md` |
| `in_expression_function` | 表达式中可使用的函数 |  | 本页面解释的语法不是必需的。 | `docs/Emuera/in_expression_function.zh.md` |
| `operand` | 运算 |  | ~ 按位取反(按位NOT) 一元运算符（优先级最高） | `docs/Emuera/operand.zh.md` |
| `replace` | _replace.csv |  | 通过在csv文件夹中放置名为_replace.csv的文件，可以进行与显示相关的设置。 | `docs/Emuera/replace.zh.md` |
| `resources` | 资源文件（历史文档） |  | 本页描述的是原版 Emuera 的资源设置方法。Skia 版已全面重构图像资源管理（懒加载索引、SharedBitmapCache、AnimSpriteCache），资源设置说明已迁移至 [资源设置 — 图像资源的准备方法](../tutorial/resources.zh.md)。 | `docs/Emuera/resources.zh.md` |
| `shortcut` | 快捷键 |  | Emuera可以通过快捷键执行几种操作。 | `docs/Emuera/shortcut.zh.md` |
| `system_flow` | 流程图 |  | 流程图使用DiagramDesigner制作。 | `docs/Emuera/system_flow.zh.md` |
| `usage` | Emuera使用方法 |  | 需要.NET Framework 4.5环境。(EM+EE需要7.0) | `docs/Emuera/usage.zh.md` |
| `user_defined_in_expression_function` | 用户定义的表达式函数 |  | 除了内置函数外，还可以在表达式中调用用@～～定义的函数作为"表达式中可使用的函数"。 | `docs/Emuera/user_defined_in_expression_function.zh.md` |
| `user_defined_variables` | 用户定义的变量 |  | 通过使用#DIM和#DIMS可以定义自己喜欢的变量。 | `docs/Emuera/user_defined_variables.zh.md` |
| `variables` | 变量的规格和一览 |  | 结合EmueraEM+EE的规格补充内容 | `docs/Emuera/variables.zh.md` |

## Emuera EM+EE（2 篇）

| 名称 | 标题 | 签名 | 摘要 | 路径 |
|---|---|---|---|---|
| `CHANGELOG` | 更新日志 |  | 新增功能：[PluginAvailableWarn](../EMEE/EMEE_Summary.zh.md#pluginavailablewarn) 配置项。控制外部插件功能启用时是否显示警告。 | `docs/EMEE/CHANGELOG.zh.md` |
| `EMEE_Summary` | Emuera EM+EE 功能概览 |  | 在程序运行过程中，不再持续占用资源（Resource）文件夹中的图像文件。 | `docs/EMEE/EMEE_Summary.zh.md` |

## Skia 图形（2 篇）

| 名称 | 标题 | 签名 | 摘要 | 路径 |
|---|---|---|---|---|
| `CHANGELOG` | Changelog |  | 共享 SKFont 被提前释放导致 use-after-free（原生访问冲突根因）：GraphicsImage.GDispose() 曾对 GSETFONT 传入、由 FontFactory.GetFont 缓存共享的 SKFont 实例调用 Dispose()，其余持有者访问已释放的原生句柄触发 0xc0000005。现 GDispose() 仅置空引用；FontFactory.ClearFont() 也不再 Dispose 共享 typeface，交由 GC/SkiaSharp 终结器回收。涉及 GraphicsImage.cs / FontFactory.cs | `docs/Skia/CHANGELOG.zh.md` |
| `Skia_Summary` |  |  |  | `docs/Skia/Skia_Summary.zh.md` |

## eramaker 原版（5 篇）

| 名称 | 标题 | 签名 | 摘要 | 路径 |
|---|---|---|---|---|
| `CSV_format` | eramaker的CSV书写格式 |  | 本页记载的是eramaker的相关信息。与现行Emuera的规格存在部分差异。 | `docs/eramaker/CSV_format.zh.md` |
| `ERB_format` | eramaker的ERB书写格式 |  | 本页记载的是eramaker的相关信息。与现行Emuera的规格存在部分差异。 | `docs/eramaker/ERB_format.zh.md` |
| `README` | eramaker 规格 |  | eramaker 规格说明汇总 | `docs/eramaker/README.zh.md` |
| `system_flow` | 游戏系统函数与流程 |  | 本页面记载的是 eramaker 的信息，与现行的 Emuera 规格存在部分差异。 | `docs/eramaker/system_flow.zh.md` |
| `variables` | eramaker 的变量列表 |  | Emuera 中变量的上限可以通过 VariableSize.csv 进行修改。 | `docs/eramaker/variables.zh.md` |

## 更新日志（1 篇）

| 名称 | 标题 | 签名 | 摘要 | 路径 |
|---|---|---|---|---|
| `README` | 更新日志 |  | 新增函数：[HTML_STRINGLINES](../Reference/HTML_STRINGLINES.zh.md)。 | `docs/Changelog/README.zh.md` |

---

共 387 篇。
