# 产品资料（宣传稿唯一素材来源）

> 规则：这里没写的功能，稿子里一律不能出现。每个功能都要能指到真实截图或可复现的操作。
> 状态：**2026-11-11 已确认先发布到资料库。未实测、安装版、截图及其他待确认项仍保留原标记，不能作为确定事实宣传。**
> 核对日期：2026-11-11（北京时间）。
> “代码确认 / 代码可证”表示已读到实现，不表示本轮已运行软件、实测通过或用户安装版已包含该功能。截图路径均为建议位置，目前没有新增截图。
> 问题场景由现有实现归纳，不是用户访谈、作者个人经历、客户反馈或效果数据。个人动机、开发时长、所用 AI 工具、用户数量及节省时间等，仍须本人提供。
> 两个产品仓库为私有，content-agent 为公开。本页的功能细节、源码文件依据和开发记录已获确认先公开；私有源码链接仍仅对有仓库权限的人可访问。截图目前尚未提供，后续补图须先脱敏。

## 核对基准

- 模板：[content-agent/products.md](https://github.com/RookieToExpert/content-agent/blob/24c0ebcc90783004adbf960b81270d4f5f787526/products.md)。已读该版本的 AGENTS.md、content-draft skill、定位草案及红线。
- todoulist：main `97603373e9f2cd711f21b873b5bc4b7647adc563`（2026-11-05）。最新发行 1.10.0 / build 11000（2026-11-02）。本次主分支相对该发行仅多出工作流改动，仍需核对用户安装版。
- 网站监控：RookieToExpert/wangzhanjainkong，main `213064766af09c4a564dbd2285d81b55a0934be6`（2026-11-05）。源码最新状态不能代替安装包/部署状态。

## todoulist

- 平台：macOS14+ 原生 SwiftUI。[Package.swift L6–10](https://github.com/RookieToExpert/todoulist/blob/97603373e9f2cd711f21b873b5bc4b7647adc563/Package.swift#L6-L10)。当前发行说明标 Apple Silicon，不宣传 Windows、iPhone、Android、网页版。
- 版本：1.10.0 / 11000。[源码元数据 L1–6](https://github.com/RookieToExpert/todoulist/blob/97603373e9f2cd711f21b873b5bc4b7647adc563/Sources/TudouListAppShellFeature/TudouListReleaseMetadata.swift#L1-L6) 与[最新发行](https://github.com/RookieToExpert/todoulist/releases/tag/v1.10.0)一致；用户安装版待“关于”截图。
- 获取：私有仓库 Release 有 DMG、App ZIP、SHA256SUMS；local-ad-hoc 签名，未经 Apple 公证。公开下载地址、公开发行范围、App Store 状态待确认，不能把私有下载当公开获客入口。
- 价格：待确认。没有依据写免费、买断或订阅。
- 同步：不列为已有卖点。README将 CloudKit、iCloud、iPhone 放在后续方向；已确认本地存储和本地备份不等于云同步。
- 语言和外观：存在中英资源及主题选择；是否主推英文、全部英文布局质量待截图。E16 L169–201 证实主题设置。
- 不承诺不丢数据、自动备份零失败、所有操作均可撤销等绝对结果。

### 解决的真实问题（用户视角，一条一个）

| 问题场景 | 怎么解决（实现与边界） | 截图（待用户提供） | 证据 | 状态 |
|---|---|---|---|---|
| 工作、学习、生活事项混在一张清单里，难以分开管理 | 多计划表可新建、改名，设置图标和颜色；计划表各自管理任务 | 侧栏创建三个合成计划表，选中一个显示任务列表；`assets/products/todoulist/todoulist-plans.png` | E1 createPlanMutation / updatePlanMutation | 代码确认，安装版及截图待确认 |
| 目标很大，不知道下一步怎么拆 | 多层子任务，可调整父级、整棵子树移到另一计划表；禁止跨计划表父级、自身父级及循环关系 | 计划表内展开至少三级任务，右侧打开子任务详情；`assets/products/todoulist/todoulist-task-tree.png` | E2 L203–280、315–401；E3 makePlanningTaskTree | 代码确认，交互待确认 |
| 同一件事属于多个主题，单一分类不够 | 每个任务独立多选全局标签；子任务不继承；计划表多标签筛选为 OR，标签页跨计划表聚合 | 任务详情选择两个标签，再从侧栏进入标签页；`assets/products/todoulist/todoulist-multi-tags.png` | E2 L403–425；E3 L258–375 | 代码确认，README 旧说法不可用 |
| 清单列了很多，却没安排到今天具体时间 | 今日看板按全天、上午、下午、晚上与已过期组织；安排进时段寻找可用时间，默认半小时，保留已有有效时长；有满时段/重叠处理 | 进入今日重点，放入合成任务，展示全天、三个时段和已过期；补拖入前后图；`assets/products/todoulist/todoulist-today-board.png` | E4 L326–411，scheduledDuration L1284；调用 ActionScheduleAllocator.availableSchedule | 代码确认，不是仅分类 |
| 看不出一周是否挤在一起，改时间费劲 | 周/月时间线，全天栏及时间块；周视图有拖动、缩放改期。不宣传月视图同样支持所有拖拽缩放 | 时间线切到周和月各截一张；拖动/缩放补短录屏；`assets/products/todoulist/todoulist-timeline-week.png`、`assets/products/todoulist/todoulist-timeline-month.png` | E6 L16–21、564–636、1054–1090，resize / scheduleDroppedAction | 代码确认，真实交互待确认 |
| 到时间容易忘记做任务 | 本地提醒要求先设任务时间；普通任务以结束时间减提前量，全天以当地09:00减提前量；需系统通知权限，不是邮件/短信/远程推送 | 任务详情设置时间再选择提醒，截选项及系统实际通知；`assets/products/todoulist/todoulist-reminder-settings.png`、`assets/products/todoulist/todoulist-reminder-notification.png` | E7 L9–67；E8 L116–149 | 代码确认，权限和通知实测待确认 |
| 重复事项每次都要重新建 | 顶层任务按日、周、月、完成后间隔循环，支持全天/指定时刻/未安排、暂停恢复；完成当前后才生成下一份，未完成不堆积，错过周期顺延，关闭期间到下次打开补查 | 顶层任务详情“设置循环”，展示规则及旧/新实例；`assets/products/todoulist/todoulist-recurring-task.png` | E9 L202–272；E10 L163–258、290–294 | 代码确认，仅顶层任务 |
| 一组相似任务要重复使用，但不必定期循环 | 复制任务树，新 UUID，副本追加“（副本）”；不是独立模板库 | 任务菜单复制后并排展示原树和副本；`assets/products/todoulist/todoulist-duplicate-tree.png` | E9 duplicateTask L185–199、clone L95–122 | 代码确认，入口截图待确认 |
| 计划越多，长期目标推进越难看清 | 目标地图按计划表/标签展示任务树、完成进展、关注状态，支持未完成范围筛选；状态为规则计算，不是 AI 诊断 | 总览进入目标地图，展示两个计划表和不同状态；`assets/products/todoulist/todoulist-goal-map.png` | E3 L378–653、821–860、1423–1436 | 代码确认 |
| 记得关键词，却忘记放在哪 | 搜索任务、计划表和标签并定位；任务标题/备注参与匹配，最多50项，不含回收站 | 主窗口搜索输入合成关键词，显示三类结果；`assets/products/todoulist/todoulist-search.png` | E11 L254–398；E12 L871–892 | 代码确认 |
| 忙了一周，说不清完成了什么 | 完成洞察含总量、当月、近七天、连续活跃等；历史按标题、计划表、标签、时间筛选并按完成日期查看；不等同工时或生产力评估 | “已完成”页面洞察/热力图及筛选历史各一张；`assets/products/todoulist/todoulist-completion-insights.png`、`assets/products/todoulist/todoulist-completion-history.png` | E13 L494–681 | 代码确认 |
| 误删任务后想找回 | 删除任务整棵子树进入回收站保留七天，可恢复；另有永久删除/到期清理。不泛称所有删除可恢复，计划表删除需单独说明 | 回收站展开合成任务树，显示恢复入口；`assets/products/todoulist/todoulist-trash-restore.png` | E13 L254–439；E14 L4、30–31 | 代码确认 |
| 误操作后想回到上一步 | 会话内最多50步撤销/重做，连续输入可合并；不跨启动保存；维护及备份恢复不是普通可撤销操作 | 做一次合成改名后打开编辑菜单，展示撤销/重做；`assets/products/todoulist/todoulist-undo-redo.png` | E15 L1–26、43–134；E16 L212–222 | 代码确认 |
| 担心本地资料丢失，想保留副本 | JSON导出、校验后整体恢复；本地自动备份默认开启/七份，可调整保留数；恢复替换全部数据；不是云备份，空数据与异常文件有保护 | 设置→数据与存储，显示导出/恢复/自动备份，不上传备份内容；`assets/products/todoulist/todoulist-backup-settings.png` | E16 L225–313、327–413；E17 L11–36、82–159；E18 L187–257 | 代码确认 |

### 本机 AI 客户端接入（依赖配置，单独审核）

| 场景 | 现有实现及边界 | 截图（待用户提供） | 证据 | 状态 |
|---|---|---|---|---|
| 已在本机 AI 客户端规划任务，不想手工逐条录入 | 默认关闭的本机 MCP，13个工具查询、搜索、创建修改、标签归属、完成、排期与截止日期；由 App 校验及保存。需 App 运行、Python3.9+、本机 stdio 客户端；云端 HTTP 客户端不能直接连接。同一登录用户下的进程访问，无法区分同用户不同客户端。 | 设置→通用→AI与自动化，开启后截图监听状态；依 Docs/MCP.md 配客户端，用合成任务展示一次调用及 App 结果；`assets/products/todoulist/todoulist-local-mcp.png`、`assets/products/todoulist/todoulist-mcp-result.png` | E19 L37–195；E20 L3–63；E16 L139–165 | 生产代码确认；不是调试专用。完整客户端联调待确认，不能写已真机验收 |

MCP 写结果单独报告 persisted；超时/断连可能结果不确定，不自动重试。最新 Release 明确仍待完整 App 客户端联调、保存重开、真实拖放、通知、VoiceOver、英文长文本等人工验收。本次没有执行这些检查。

### 开发故事素材

以下仅为可查证的迭代事实，是否公开及个人经历部分待确认。

1. 从单标签到任务独立多标签：变更记录 CONTRACT-2026-018 描述全局目录、无继承、OR筛选、移动保留关系；当前代码吻合。可以写具体改动，不能杜撰客户呼声或人数。[变更记录 L336–350](https://github.com/RookieToExpert/todoulist/blob/97603373e9f2cd711f21b873b5bc4b7647adc563/Docs/CapabilityChangeLog.md#L336-L350)。
2. 循环任务选择“完成后下一份、跳到当前周期”，而非无限补积压：E9 processRecurrences 与 E10 帮助文案支持。不能杜撰作者因拖延/焦虑而开发的个人经历。
3. AI入口不直接写数据库：E19/E20 支持由运行中的 App 执行业务校验、撤销、保存及 persisted 检查。可讲实现取舍，不能写云端全自动托管。
4. 桌面布局持续迭代：1.9.1记录统一计划表列表、标签详情融入主窗口、备注完整高度、今日看板宽窄适配、时间线全天区域可读性。[v1.9.1](https://github.com/RookieToExpert/todoulist/releases/tag/v1.9.1)。不是外部认可或增长成果证据。
5. 发行记录含自动化检查数量与通过说明，但本次未重跑，引用时明确“发行记录记载”，不能声称本次已验证。

## 网站监控

- Mac：Apple Silicon、macOS14+，内置运行时和浏览器。临时签名预览版，未完成正式Developer ID签名/公证；暂无一键迁移、自动更新。[native/README.md#3-L39](https://github.com/RookieToExpert/wangzhanjainkong/blob/213064766af09c4a564dbd2285d81b55a0934be6/native/README.md#L3-L39)
- Windows：11 x64商业预览；缺WebView2时安装器联网补齐。未完成Windows真机验收/Authenticode签名；不承诺Win10/ARM/Server。[native/windows/RELEASE_CHECKLIST.md#1-L18](https://github.com/RookieToExpert/wangzhanjainkong/blob/213064766af09c4a564dbd2285d81b55a0934be6/native/windows/RELEASE_CHECKLIST.md#L1-L18)
- 容器与原生数据独立，本地电脑关机、休眠、断网不能正常检查，不是云端24小时服务。
- 版本：以上是main源码，不是已发行版本号。10月10日、29日、30日验收记录明确部分功能未重新打包/部署/替换安装包。不能说用户已有这些能力。[ACCEPTANCE.md#1291-L1322](https://github.com/RookieToExpert/wangzhanjainkong/blob/213064766af09c4a564dbd2285d81b55a0934be6/ACCEPTANCE.md#L1291-L1322)
- 获取：只核实到开发构建说明；当前正式版本号、对外下载/购买链接、用户安装包与SHA对应关系待确认。
- 价格：待确认。售价、授权期、设备数量政策、售后/试用条款须由用户提供，不写免费、买断或具体订阅价格。
- 补图：`assets/products/website-monitor/monitor-about.png`（关于/版本）；若宣传Windows须提供Windows真机运行截图；激活页应隐藏设备码及激活码。

### 解决的真实问题

| 问题场景 | 怎么解决（实现与边界） | 截图（待用户提供） | 文件依据 | 状态 |
|---|---|---|---|---|
|反复刷新商品、职位或公告网页|预览中点选/框选文字，试运行后按频率检查。框选比较元素文本，不是像素截图；首次建基线，后续变化才通知；网页改版可能须重选。|`assets/products/website-monitor/monitor-select.png`：蓝框、命名关注项与试读输出；`assets/products/website-monitor/monitor-frequency.png`：确认页频率|[session-browser/app/main.py#L1914-L2016](https://github.com/RookieToExpert/wangzhanjainkong/blob/213064766af09c4a564dbd2285d81b55a0934be6/session-browser/app/main.py#L1914-L2016)；[changedetection/upstream/changedetectionio/blueprint/simple/__init__.py#L640-L722](https://github.com/RookieToExpert/wangzhanjainkong/blob/213064766af09c4a564dbd2285d81b55a0934be6/changedetection/upstream/changedetectionio/blueprint/simple/__init__.py#L640-L722)；[changedetection/upstream/changedetectionio/worker.py#L571-L635](https://github.com/RookieToExpert/wangzhanjainkong/blob/213064766af09c4a564dbd2285d81b55a0934be6/changedetection/upstream/changedetectionio/worker.py#L571-L635)|代码可证；安装版与截图待确认|
|同一页要关注多个位置，或者列表排序后目标换位置|每条监控最多12项，支持字段选择、固定结构位置与按稳定名称跟随。歧义、名称缺失或结构变化会报错，不能承诺任意改版仍可用。|`assets/products/website-monitor/monitor-multi-fields.png`：至少两项与字段；`assets/products/website-monitor/monitor-follow.png`：跟随名称设置|[session-browser/app/main.py#L945-L952](https://github.com/RookieToExpert/wangzhanjainkong/blob/213064766af09c4a564dbd2285d81b55a0934be6/session-browser/app/main.py#L945-L952)；[session-browser/app/focus.py#L288-L378](https://github.com/RookieToExpert/wangzhanjainkong/blob/213064766af09c4a564dbd2285d81b55a0934be6/session-browser/app/focus.py#L288-L378)|代码可证；安装版与截图待确认|
|只想等目标价、上新、指定文字或恢复可选|支持低于/高于数值、列表新增、文字由无到有、明确不可选到可选。首次只记录，持续满足不重复提醒；列表只检查当前已加载且非空部分，不是跨页全站扫描；灰色本身不算库存状态。|`assets/products/website-monitor/monitor-rules.png`：关注规则与阈值；`assets/products/website-monitor/monitor-keyword.png`：指定文字；`assets/products/website-monitor/monitor-available.png`：可选状态|[changedetection/upstream/changedetectionio/focus_rules.py#L11-L77](https://github.com/RookieToExpert/wangzhanjainkong/blob/213064766af09c4a564dbd2285d81b55a0934be6/changedetection/upstream/changedetectionio/focus_rules.py#L11-L77)；[session-browser/app/focus.py#L365-L395](https://github.com/RookieToExpert/wangzhanjainkong/blob/213064766af09c4a564dbd2285d81b55a0934be6/session-browser/app/focus.py#L365-L395)|代码可证；安装版与截图待确认|
|酒店房型已列出但无房，关键词无法判断是否可订|携程专项读取保留房型身份、入住条件，验证价格与预订状态；需手动设置日期/人数，读取失败不当作有房。不能泛化成所有酒店平台。|`assets/products/website-monitor/monitor-hotel.png`：保留的日期人数、房型名与恢复可预订规则|[session-browser/app/hotel_rooms.py#L107-L128](https://github.com/RookieToExpert/wangzhanjainkong/blob/213064766af09c4a564dbd2285d81b55a0934be6/session-browser/app/hotel_rooms.py#L107-L128)；[session-browser/app/main.py#L2132-L2143](https://github.com/RookieToExpert/wangzhanjainkong/blob/213064766af09c4a564dbd2285d81b55a0934be6/session-browser/app/main.py#L2132-L2143)|代码可证；安装版与截图待确认|
|要登录、选城市或查询条件后网页才有内容|专用浏览器保存本地登录资料；用户手动登录。查询/筛选操作可记录并在检查时重放核对。不是验证码服务；不承诺任意站点、多窗口、跨站或iframe流程。|`assets/products/website-monitor/monitor-profile.png`：凭证卡及关联监控；`assets/products/website-monitor/monitor-recipe.png`：保留页面条件/操作步骤，隐去账号|[session-browser/app/main.py#L1098-L1185](https://github.com/RookieToExpert/wangzhanjainkong/blob/213064766af09c4a564dbd2285d81b55a0934be6/session-browser/app/main.py#L1098-L1185)；[session-browser/app/browser_recipe.py#L36-L59](https://github.com/RookieToExpert/wangzhanjainkong/blob/213064766af09c4a564dbd2285d81b55a0934be6/session-browser/app/browser_recipe.py#L36-L59)；[session-browser/app/main.py#L2130-L2143](https://github.com/RookieToExpert/wangzhanjainkong/blob/213064766af09c4a564dbd2285d81b55a0934be6/session-browser/app/main.py#L2130-L2143)|代码可证；安装版与截图待确认|
|收到变化但不知道改了什么|详情按历史版本显示修改前后和时间；重选在原监控更新，保留历史和通知配置。重选前后范围不同不能当成网页真实变化。|`assets/products/website-monitor/monitor-diff.png`：时间、前后对比和历史选择|[changedetection/upstream/changedetectionio/blueprint/simple/__init__.py#L338-L374](https://github.com/RookieToExpert/wangzhanjainkong/blob/213064766af09c4a564dbd2285d81b55a0934be6/changedetection/upstream/changedetectionio/blueprint/simple/__init__.py#L338-L374)；[changedetection/upstream/changedetectionio/blueprint/simple/__init__.py#L640-L663](https://github.com/RookieToExpert/wangzhanjainkong/blob/213064766af09c4a564dbd2285d81b55a0934be6/changedetection/upstream/changedetectionio/blueprint/simple/__init__.py#L640-L663)|代码可证；安装版与截图待确认|
|想知道价格走势与最近便宜了多少|历史变化点生成走势图，首页显示数值差额与百分比。非数字、缺字段和单位改变断线；趋势最多取最近200份历史，不是每次检查采样或金融级任意精度行情。|`assets/products/website-monitor/monitor-trend.png`：图、悬停、数据表；`assets/products/website-monitor/monitor-price-badge.png`：首页涨跌；`assets/products/website-monitor/monitor-trend-gap.png`：暂无报价断线|[changedetection/upstream/changedetectionio/product.py#L318-L410](https://github.com/RookieToExpert/wangzhanjainkong/blob/213064766af09c4a564dbd2285d81b55a0934be6/changedetection/upstream/changedetectionio/product.py#L318-L410)；[changedetection/upstream/changedetectionio/blueprint/simple/__init__.py#L375-L388](https://github.com/RookieToExpert/wangzhanjainkong/blob/213064766af09c4a564dbd2285d81b55a0934be6/changedetection/upstream/changedetectionio/blueprint/simple/__init__.py#L375-L388)|代码可证；安装版与截图待确认|
|普通价格波动提醒太多，只关心更低价|提醒正文有前后价格/涨跌与30天或有记录以来极值；可选历史新低提醒。过滤用完整同币种历史；无法判断照常提醒，手动重试不受过滤。不是全网比价。|`assets/products/website-monitor/monitor-new-low.png`：规则；`assets/products/website-monitor/monitor-price-message.png`：真实消息脱敏|[changedetection/upstream/changedetectionio/product.py#L453-L551](https://github.com/RookieToExpert/wangzhanjainkong/blob/213064766af09c4a564dbd2285d81b55a0934be6/changedetection/upstream/changedetectionio/product.py#L453-L551)；[changedetection/upstream/changedetectionio/notification_service.py#L363-L378](https://github.com/RookieToExpert/wangzhanjainkong/blob/213064766af09c4a564dbd2285d81b55a0934be6/changedetection/upstream/changedetectionio/notification_service.py#L363-L378)；[changedetection/upstream/changedetectionio/notification_service.py#L485-L501](https://github.com/RookieToExpert/wangzhanjainkong/blob/213064766af09c4a564dbd2285d81b55a0934be6/changedetection/upstream/changedetectionio/notification_service.py#L485-L501)|代码可证；安装版与截图待确认|
|不想盯软件，要在常用渠道接收提醒|飞书、SMTP邮件、企微群机器人、PushPlus个人微信、本地Mac/Windows系统通知。需用户配置；PushPlus接受异步请求不保证收件；系统通知须原生应用运行。|`assets/products/website-monitor/monitor-channels.png`：渠道选择/已配置状态；`assets/products/website-monitor/monitor-notification.png`：真实脱敏提醒，不展示Webhook/Token|[relay/app/channels.py#L15-L50](https://github.com/RookieToExpert/wangzhanjainkong/blob/213064766af09c4a564dbd2285d81b55a0934be6/relay/app/channels.py#L15-L50)；[relay/app/channels.py#L137-L184](https://github.com/RookieToExpert/wangzhanjainkong/blob/213064766af09c4a564dbd2285d81b55a0934be6/relay/app/channels.py#L137-L184)；[changedetection/upstream/changedetectionio/blueprint/simple/__init__.py#L724-L757](https://github.com/RookieToExpert/wangzhanjainkong/blob/213064766af09c4a564dbd2285d81b55a0934be6/changedetection/upstream/changedetectionio/blueprint/simple/__init__.py#L724-L757)|代码可证；安装版与截图待确认|
|短暂波动误报，或提醒投递失败|连续2/3次一致再确认；失败通知按原历史版本、当前渠道重试。会延迟提醒，不适合瞬时库存；多渠道重试可能重复发送，接受不等于已读。|`assets/products/website-monitor/monitor-confirm.png`：连续确认；`assets/products/website-monitor/monitor-delivery.png`：失败记录与重试|[changedetection/upstream/changedetectionio/product.py#L184-L224](https://github.com/RookieToExpert/wangzhanjainkong/blob/213064766af09c4a564dbd2285d81b55a0934be6/changedetection/upstream/changedetectionio/product.py#L184-L224)；[changedetection/upstream/changedetectionio/worker.py#L443-L454](https://github.com/RookieToExpert/wangzhanjainkong/blob/213064766af09c4a564dbd2285d81b55a0934be6/changedetection/upstream/changedetectionio/worker.py#L443-L454)；[changedetection/upstream/changedetectionio/blueprint/simple/__init__.py#L416-L437](https://github.com/RookieToExpert/wangzhanjainkong/blob/213064766af09c4a564dbd2285d81b55a0934be6/changedetection/upstream/changedetectionio/blueprint/simple/__init__.py#L416-L437)|代码可证；安装版与截图待确认|
|监控多了难找难暂停，异常要逐个重试|搜索、状态/标签筛选、批量暂停/继续、全部检查和重试异常；排队/检查中去重，批量检查跳过暂停，保留历史和规则。|`assets/products/website-monitor/monitor-dashboard.png`：首页过滤与异常；`assets/products/website-monitor/monitor-bulk.png`：多选暂停/继续|[changedetection/upstream/changedetectionio/static/simple/app.js#495-L592](https://github.com/RookieToExpert/wangzhanjainkong/blob/213064766af09c4a564dbd2285d81b55a0934be6/changedetection/upstream/changedetectionio/static/simple/app.js#L495-L592)；[changedetection/upstream/changedetectionio/blueprint/simple/__init__.py#L441-L500](https://github.com/RookieToExpert/wangzhanjainkong/blob/213064766af09c4a564dbd2285d81b55a0934be6/changedetection/upstream/changedetectionio/blueprint/simple/__init__.py#L441-L500)|代码可证；安装版与截图待确认|
|选一半刷新丢工作，后台检查占用浏览器|同标签页草稿保存一天，恢复后重新预览/试读；编辑和人工操作时后台让路。不是跨设备同步，关标签/清会话可能丢草稿。|`assets/products/website-monitor/monitor-draft.png`：继续上次编辑；`assets/products/website-monitor/monitor-queue.png`：等待状态|[changedetection/upstream/changedetectionio/static/simple/app.js#1085-L1115](https://github.com/RookieToExpert/wangzhanjainkong/blob/213064766af09c4a564dbd2285d81b55a0934be6/changedetection/upstream/changedetectionio/static/simple/app.js#L1085-L1115)；[session-browser/app/main.py#L1551-L1564](https://github.com/RookieToExpert/wangzhanjainkong/blob/213064766af09c4a564dbd2285d81b55a0934be6/session-browser/app/main.py#L1551-L1564)；[session-browser/app/main.py#L2099-L2112](https://github.com/RookieToExpert/wangzhanjainkong/blob/213064766af09c4a564dbd2285d81b55a0934be6/session-browser/app/main.py#L2099-L2112)|代码可证；安装版与截图待确认|
|网站需要代理，分不清是代理还是网页的问题|测试当前代理/直连与保存分开；仅保存才生效。作用于会话预览/手动操作/后台检查，不保证其他后端和通知走代理，不绕过网站访问限制。|`assets/products/website-monitor/monitor-network.png`：已保存状态、开关与测试结果，遮敏感地址和认证信息|[session-browser/app/main.py#L985-L1095](https://github.com/RookieToExpert/wangzhanjainkong/blob/213064766af09c4a564dbd2285d81b55a0934be6/session-browser/app/main.py#L985-L1095)；[session-browser/app/main.py#L368-L396](https://github.com/RookieToExpert/wangzhanjainkong/blob/213064766af09c4a564dbd2285d81b55a0934be6/session-browser/app/main.py#L368-L396)|代码可证；安装版与截图待确认|

### 开发故事素材

以下仅为代码或验收记录里的迭代事实，未在本轮重跑，也不能据此声称用户安装包已经包含修复。

1. 极小金额曾被两位小数抹成0；0.8→0.5因二进制浮点导致首页−37%、通知−38%，修复为精确十进制比值统一舍入。[ACCEPTANCE.md#1305-L1313](https://github.com/RookieToExpert/wangzhanjainkong/blob/213064766af09c4a564dbd2285d81b55a0934be6/ACCEPTANCE.md#L1305-L1313)。配图monitor-decimal.png，不能说本轮实测或已安装版有修复。
2. 新低规则曾只看200条历史，202条记录的复现漏掉早期¥1而把¥9误判最低，修正完整历史比较。[ACCEPTANCE.md#1297-L1303](https://github.com/RookieToExpert/wangzhanjainkong/blob/213064766af09c4a564dbd2285d81b55a0934be6/ACCEPTANCE.md#L1297-L1303)。配图monitor-low-history.png，注明测试数据，不能虚构真实成交。
3. 暂无报价/换币种不应被画成连续同币种价格线，当前代码保留断点。[changedetection/upstream/changedetectionio/product.py#L318-L378](https://github.com/RookieToExpert/wangzhanjainkong/blob/213064766af09c4a564dbd2285d81b55a0934be6/changedetection/upstream/changedetectionio/product.py#L318-L378)。配图monitor-trend-gap.png。

## 转化追踪口令

本次没有起草帖子，也没有分配新口令。保留原表，待具体帖子确定后填写。

| 口令 | 帖子 | 产品 | 用途 |
|---|---|---|---|

## 后续补充清单

- [ ] 核对两个产品当前实际安装版本。提供“关于 / 版本”截图；网站监控需明确要宣传 Mac、Windows，还是仅其中一端。
- [ ] 确认产品对外名称、获取方式、价格/授权政策及可公开范围。私有 Release 不直接作为公开下载入口。
- [ ] 按各功能行补真实界面截图。建议先补 todoulist 的计划表/任务树、今日看板、周时间线、多标签、循环任务；网站监控的选取与试读、规则设置、变化对比、价格走势、实际通知。
- [ ] 通知、循环生成、拖放/缩放、MCP、登录条件重放等行为，用前后截图或短录屏补充；静态截图不替代这些行为的实测。
- [ ] 提供愿意公开的开发动机、实际使用经历及结果。没有素材的部分保留待确认，不生成个人故事或效果数字。
- [x] 已确认先将本版资料和源码依据发布到公开 content-agent；后续新增素材仍按真实性与脱敏要求审核。

截图请优先用专门的示例数据，不把合成示例说成真实客户案例。涉及账号、任务备注、客户/公司、内部网址、主机、个人信息、浏览器标签/地址栏、代理认证、Webhook、通知 Token、设备码/激活码等，必须遮盖。不要提供备份文件内容、Cookie 或登录资料。

## 审核附录：todoulist 文件依据

下列索引对应功能表中的 E 编号；函数名和行号用于复核。链接固定到本次核对的提交。

- E1：[Sources/TudouListPlanningCore/PlanningCoreService.swift L1143-L1358](https://github.com/RookieToExpert/todoulist/blob/97603373e9f2cd711f21b873b5bc4b7647adc563/Sources/TudouListPlanningCore/PlanningCoreService.swift#L1143-L1358)
- E2：[Sources/TudouListTaskCore/TaskCoreService.swift L203-L444](https://github.com/RookieToExpert/todoulist/blob/97603373e9f2cd711f21b873b5bc4b7647adc563/Sources/TudouListTaskCore/TaskCoreService.swift#L203-L444)
- E3：[Sources/TudouListPlanningCore/PlanningCoreService.swift](https://github.com/RookieToExpert/todoulist/blob/97603373e9f2cd711f21b873b5bc4b7647adc563/Sources/TudouListPlanningCore/PlanningCoreService.swift)
- E4：[Sources/TudouListTodayCore/TodayCoreService.swift L326-L411](https://github.com/RookieToExpert/todoulist/blob/97603373e9f2cd711f21b873b5bc4b7647adc563/Sources/TudouListTodayCore/TodayCoreService.swift#L326-L411)
- E6：[Sources/TudouListTodayFeature/TimelineCalendarView.swift](https://github.com/RookieToExpert/todoulist/blob/97603373e9f2cd711f21b873b5bc4b7647adc563/Sources/TudouListTodayFeature/TimelineCalendarView.swift)
- E7：[Sources/TudouListTodayCore/TodayCoreService+Reminders.swift L9-L67](https://github.com/RookieToExpert/todoulist/blob/97603373e9f2cd711f21b873b5bc4b7647adc563/Sources/TudouListTodayCore/TodayCoreService%2BReminders.swift#L9-L67)
- E8：[Sources/TudouListAppShellFeature/AppShellReminderSession.swift L116-L149](https://github.com/RookieToExpert/todoulist/blob/97603373e9f2cd711f21b873b5bc4b7647adc563/Sources/TudouListAppShellFeature/AppShellReminderSession.swift#L116-L149)
- E9：[Sources/TudouListState/TaskRecurrenceEngine.swift L185-L272](https://github.com/RookieToExpert/todoulist/blob/97603373e9f2cd711f21b873b5bc4b7647adc563/Sources/TudouListState/TaskRecurrenceEngine.swift#L185-L272)
- E10：[Sources/TudouListTaskFeature/TaskRecurrenceViews.swift L163-L294](https://github.com/RookieToExpert/todoulist/blob/97603373e9f2cd711f21b873b5bc4b7647adc563/Sources/TudouListTaskFeature/TaskRecurrenceViews.swift#L163-L294)
- E11：[Sources/TudouListAppShellCore/AppShellCoreService.swift L254-L398](https://github.com/RookieToExpert/todoulist/blob/97603373e9f2cd711f21b873b5bc4b7647adc563/Sources/TudouListAppShellCore/AppShellCoreService.swift#L254-L398)
- E12：[Sources/TudouListAppShellFeature/ContentView.swift L871-L892](https://github.com/RookieToExpert/todoulist/blob/97603373e9f2cd711f21b873b5bc4b7647adc563/Sources/TudouListAppShellFeature/ContentView.swift#L871-L892)
- E13：[Sources/TudouListLifecycleCore/LifecycleCoreService.swift](https://github.com/RookieToExpert/todoulist/blob/97603373e9f2cd711f21b873b5bc4b7647adc563/Sources/TudouListLifecycleCore/LifecycleCoreService.swift)
- E14：[Sources/TudouListDomain/TrashedTaskGroup.swift L1-L32](https://github.com/RookieToExpert/todoulist/blob/97603373e9f2cd711f21b873b5bc4b7647adc563/Sources/TudouListDomain/TrashedTaskGroup.swift#L1-L32)
- E15：[Sources/TudouListState/PlanningUndoHistory.swift L1-L134](https://github.com/RookieToExpert/todoulist/blob/97603373e9f2cd711f21b873b5bc4b7647adc563/Sources/TudouListState/PlanningUndoHistory.swift#L1-L134)
- E16：[Sources/TudouListAppShellFeature/TudouListSettingsView.swift](https://github.com/RookieToExpert/todoulist/blob/97603373e9f2cd711f21b873b5bc4b7647adc563/Sources/TudouListAppShellFeature/TudouListSettingsView.swift)
- E17：[Sources/TudouListPersistenceCoordinator/AutomaticBackups.swift L11-L159](https://github.com/RookieToExpert/todoulist/blob/97603373e9f2cd711f21b873b5bc4b7647adc563/Sources/TudouListPersistenceCoordinator/AutomaticBackups.swift#L11-L159)
- E18：[Sources/TudouListPersistenceCoordinator/TudouListStorePersistence.swift L187-L257](https://github.com/RookieToExpert/todoulist/blob/97603373e9f2cd711f21b873b5bc4b7647adc563/Sources/TudouListPersistenceCoordinator/TudouListStorePersistence.swift#L187-L257)
- E19：[Sources/TudouListAutomation/MCPCommandHandler.swift L37-L195](https://github.com/RookieToExpert/todoulist/blob/97603373e9f2cd711f21b873b5bc4b7647adc563/Sources/TudouListAutomation/MCPCommandHandler.swift#L37-L195)
- E20：[Docs/MCP.md L3-L63](https://github.com/RookieToExpert/todoulist/blob/97603373e9f2cd711f21b873b5bc4b7647adc563/Docs/MCP.md#L3-L63)


## 审核附录：README 与代码/交付记录差异

### todoulist

[README固定版本](https://github.com/RookieToExpert/todoulist/blob/97603373e9f2cd711f21b873b5bc4b7647adc563/README.md)。

- L20–21：仍说每棵树零/一个标签及子任务继承；代码已是独立多标签。
- L25：仍说跨计划表移动解除标签；moveTaskMutation保留标签，移动根的父级清空。
- L17、36：仍说时段仅分类不自动时间化；assignToToday会分配时间，默认半小时。
- L16、38：以“无具体时间的今日任务”解释全天已不充分；当前有全天排期、跨日安排、全天循环，不能照抄。
- L32：只跟随系统的说法不完整，设置中已有主题选择。
- 后续方向仍列搜索、提醒，但生产代码已有实现。
- README版本示例1.4.2/1.5.0、SwiftData V5、JSON v13/v16不能当当前事实；最新发行是1.10.0、SwiftData V7、JSON v18。
- README 尚未同步修正；本页按已核对代码记录功能。

### 网站监控

- README的频率举例不完整：界面另有30分钟、12小时、3天、每周、自定义；后端允许3秒至10年，但实际加载/队列不保证秒级实时。[changedetection/upstream/changedetectionio/static/simple/app.js#675-L689](https://github.com/RookieToExpert/wangzhanjainkong/blob/213064766af09c4a564dbd2285d81b55a0934be6/changedetection/upstream/changedetectionio/static/simple/app.js#L675-L689)；[changedetection/upstream/changedetectionio/product.py#L210-L222](https://github.com/RookieToExpert/wangzhanjainkong/blob/213064766af09c4a564dbd2285d81b55a0934be6/changedetection/upstream/changedetectionio/product.py#L210-L222)
- 趋势只取最近200份历史；新低过滤用完整历史。不可混为一个时间窗口。
- 根README功能列表不证明旧Mac/Windows包已含全部功能；10月最新验收明确未打包部署。
- Windows README现为文档入口，应保留RELEASE_CHECKLIST的预览、未签名和未真机验收限制。
- 个别招聘站点排查文档中的“按岗位编号识别新增”等属于建议，不是已完成跨页功能；不列入功能宣传。
- 正式售价、下载、版本、安装态和截图仍待用户确认。本轮仅静态核对，不将历史夹具通过写成当前产品实测通过。
