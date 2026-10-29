# Phase 2.2 — 报告契约、限定授权与注入隔离加固

**结论：已完成授权范围内的离线工程；阶段总状态 PARTIAL。** 当前官方静态检查、历史回归和新确定性检查通过。新模型验证、独立人审、Uliya/NAS 运行均为 NOT_RUN，因此没有当前候选完整报告可靠性或真实平台成功的声明。Phase 3 只准备 DRAFT，不生成正式 PDF/ZIP，不提交。

## 基线与授权

首次实际检查：`main`，HEAD `1098e3ee6655c34977436806108b479af27c9c0d`，`git status --porcelain=v1` 为空。当前 HEAD 未变。原有 248 个跟踪文件的 SHA-256 已记录；允许修改的旧文件只有 `.gitattributes` 和三个 Skill Markdown 文件。其余 **244/244** 文件字节保持不变，包括历史模型记录、预期、夹具、报告和评分工具。33 个历史 `validation/fixtures/` 文件均保持原字节。[基线](../validation/results/phase2-2/baseline.json)、[保护检查](../validation/results/phase2-2/protected-history.json)。

基线收据生成前添加了两个新验证脚本，因此收据的“生成时状态”列有未跟踪新文件；`initial_status_at_first_inspection=CLEAN` 记录真正首次检查。没有覆盖用户改动或复位操作。此次没有 Phase 2.2 付费授权，也没有 commit/push、发布、可见性变更、外部联系或正式提交授权。

## 原因与实际修正

Phase 2.1 最终 v2 已有简短的 changed-input-only、路径/状态分离和拒绝裸保证说明，但该 v2 没有外部重测。此次将其扩展为可审阅的明确契约及独立版本的本地验证基础设施，而不是把已有说明宣称为新模型成功。

| 层面 | 旧契约/观察中的问题 | 本次候选行为 |
| --- | --- | --- |
| Input Delta | v1 外部回答 6/12 精确满足契约；状态不确定被误写成输入改变 | 逐一比较实际 A/B 值，只列真正不同的项，每项一次；资产/party 在本工作流固定。另行定义的可变 party 对照只存在本地测试，不扩大产品范围。 |
| Evidence Status Delta | 旧 `compare_effective` 只遍历变动输入，无法呈现未变输入维度的间接状态改变 | 新本地 `report_contract.py` 覆盖“输入变化维度 ∪ 状态变化维度”；两个变化标记独立。历史模块保持原样。 |
| Proof Delta | 只看最终标签容易丢失同标签下输入变化或依赖变化 | 同一维度集合逐项给出 A/B 状态、实际支持/反证、限定条件与缺失证据；没有可用引文就保留缺失。 |
| Scope Receipt | 七个历史严格失败，包括在路径附注状态、scenario 嵌入维度、外部路径污染 | 明确分离 selected、actually read、unavailable selected、状态、完整性、错误、限制、修订、依赖与不可信引用；不清洗错误答案后再评分。 |
| Qualified grant | H21-K 对 purpose 冲突后的另外三个 use terms 有投影分歧 | 明确独立维度条款与共享限定条件；不拆解耦合授权，不拼接不兼容 grant；真实含混保持可见。 |
| 人工修复问题 | B/D 回答允许“用户保证没有别的限制”替代文书证据 | 每问说明缺失、受阻 asset/scenario/dimension、所需可核查文书，以及补证后仍 Unknown 的事项；人类批准不等于来源完整。 |

新的 Skill 仍为四个 Markdown 文件：入口和三个直接链接的 references。只改了入口及两个规则引用；delegation example 原字节未变。没有添加 Agent、Action、参数、返回字段保证、CLI 执行器、Docker、web app 或 NAS API。保存仍 **DISABLED**。

## H21-K 原始调查

[原始调查与内容哈希](../validation/results/phase2-2/H21-K-investigation.json)直接读取冻结来源和实际最终回答，保留原 Scope Receipt、源文本、预期和模型状态。历史回答在 `unavailable` 中写入 `synthetic/private/other-contract.txt` 并附加解释，尽管其正文明确承认该路径未授权、未提供、未读取。因此这是**报告污染**；原代理没有实际工具调用或保存操作，不能称为已发生越权读取，也不能称为真实运行时注入防护通过。

原 G1 将 news commentary 与 site/Ireland/date 一起表述。冻结预期将后三项独立投影为 CONSISTENT_EVIDENCE；模型把它们视为 news-only 整体授权，给出三个 GAP_IN_CHECKED_SCOPE。三个保守不匹配完整保留，**没有修改或弱化 H21-K 预期**。该原文的投影解释仍需真实人审，不能用新明确措辞的用例“裁决”旧分歧。

新版本澄清：P22-Q01 文本明确维度独立；P22-Q02 文本明确四个 use 条件共同成立；P22-Q03 只有 channel 输入变化，却使其他 use 维度状态随耦合条件改变。这些新用例不计入旧模型成绩。历史严格成绩仍为 **3/12**；与不同、更宽松基准的 7/12 不是受控模型质量比较。

## 注入隔离与证据保留

六种新来源文本攻击：fake system、fake expert、私有路径、网络目的地、伪造用户授权、伪造批准/保存。全部仅作为合成来源数据使用，没有访问任何被提及路径或目的地。有效的授权集合来自用户，实际读取事实来自专家观察，二者不能由文档改写。攻击短引文及其包含来源保留在单独不可信 ledger；既不能新增 selected/unavailable，也不能制造新 dependency 或 approval。

评分控制拒绝污染原样，不删除后缀或替换 scenario-qualified 维度来提高成绩。若真实专家返回越界数据，候选要求拒绝依赖使用、披露边界问题并停止受影响工作。**以上是 Markdown 规则与离线拒绝控制，不是真实 Uliya 执行强制机制。**

## 保留的证据安全架构

Observed Evidence 保留实际可见名称、准确文本、独立禁止条款与来源限制；Effective Assessment 先检查可用性/完整性、关联、适用性、实质引文支持、修订权限/优先关系、跨维度依赖和总体一致性。潜在跨维度不完整来源阻断全部六维，包括身份/party；只有来源支持的排除/限缩证据才能保留不受影响的正面状态。独立 R1 禁令不会被另一个 grant 的部分修订消除。真实冲突观察不会因为最终 UNASSESSED 而丢失。

本地 oracle 复用冻结历史 policy，对新短文本提供人工策划的、内容/路径哈希绑定的解释前提。它不是任意自然语言蕴含器，更不是平台返回结构或真实法律权威；新 JSON 结构全部只是开发期报告契约。[代码](../validation/report_contract.py)、[新冻结用例](../validation/fixtures/phase2-2/deterministic-v1.json)、[冻结收据](../validation/fixtures/phase2-2/freeze.json)。

## 当前官方能力与来源

在修改前已读完整当前 [Starter Kit](https://ai.ugreen.com/pages/hackathon-starter-kit) 第 1–8 节、当前工具 SKILL/Standard 和要求的 orchestration/runtime/usage/safety/completion/check/format/capability-query 引用。重新下载 0.7.3 归档，SHA-256 为 `cf557e5a022e4297892f39768132855154232efdedeb726b2845450ccd70e1b3`；catalog 2.0.0 与已记录工具逐字节一致。所有八个既有已审计 Action 定义也与新 catalog 完全相同。[本轮工具记录](../validation/results/phase2-2/toolchain.json)。

| 当前启用能力 | 唯一登记 owner | 参数、权限和响应依据 |
| --- | --- | --- |
| ug-filesystem find | file-agent | 必需 path；完整可选列表、类型/范围、read/none 和未知响应布局见下列逐字定义。 |
| ug-filesystem stat | file-agent | 必需 string path，read/none；真实 identity/稳定性仍 Unknown。 |
| ug-filesystem sha256sum（仅可选完整性） | file-agent | 必需 string path，read/none；hash 不是权利证明。 |
| ug-document qa | document-agent | 必需 query；file 等完整参数/枚举/默认值、read/none 见逐字定义；没有保证的 nested quote/path/page schema。 |

精确参数/类型/required/repeatable/范围/approval/returnSummary/completionEvidence 已在[能力矩阵](10-capability-audit.md)和[逐字 catalog selection](../validation/official/capability-selection.json)中保存，本轮验证其与新归档一致。旧审计中可选 save 的讨论是历史设计，当前版本明确不启用；不能据旧审计开启保存。permissions/prerequisites/errorCodes/stability、OCR、覆盖完整性、路径约束和模型路由保持 Unknown。父 Skill 只委派业务指令，专家拥有 Action 选择与真实权限处理。

## 文件和下一阶段

已有文件仅四项窄改：`.gitattributes`、`rightsgap-media-reuse/SKILL.md`、`references/evidence-rules.md`、`references/report-and-recheck.md`。新代码为 `phase22_common.py`、`prepare_phase22_baseline.py`、`phase22_cases.py`、`report_contract.py`、`run_phase22.py`、`evaluate_phase22.py`、`test_phase22_evaluator.py`、`validate_phase22.py`、`prepare_phase22_materials.py`、`record_phase22_sources.py`，以及本轮审计/打包工具；全部位于实际 Skill 目录之外。新增结果、夹具、docs/19–22 与 review README/manifest 同样在目录外。

离线核心通过后，已按授权准备英文十问草稿和准备检查表；**仅供 owner 审阅，不代表 G3–G7 已通过或正式参赛包已就绪**。推荐 CONDITIONAL_GO：先处理真正人审、可选另行授权的冻结外部验证和 owner 最终选择；如获 Round 2 访问再验证真实源引文与权限。若真实平台不能返回可靠来源上下文，缩小为证据定位器及人工问题，不维持无依据正面判定。详细命令、限制和门禁见[验证报告](20-phase2-2-validation-report.md)。
