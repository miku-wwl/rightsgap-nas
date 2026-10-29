# Phase 2.2 — 验证记录与门禁

**PHASE22_ENGINEERING_STATUS=PARTIAL；OFFLINE_ENGINEERING=PASS；FINAL_RECOMMENDATION=CONDITIONAL_GO。** 授权范围内离线工作已完成；外部安全、完整模型报告和独立人审未运行。不得把以下依赖断言数量当成独立文档数量、泛化准确率或 Uliya/NAS 运行结果。

基线/当前 HEAD：`1098e3ee6655c34977436806108b479af27c9c0d`，分支 `main`，初始干净。没有 commit/push、release、visibility change、外部联系或 Devpost 提交。保存 DISABLED，正式 PDF/ZIP 未创建。

## 实际命令及结果

全部从 `D:\workshop\oct\rightsgap-nas` 执行。历史 runner 实际 cwd 为收据中记录的独立临时目录；当前工作区的历史输出没有被重写。[逐命令参数、UTC 时间、stdout/stderr、退出码](../validation/results/phase2-2/execution.json)。子进程仅接收 OS 路径等允许列表环境，不转发 API 凭证；没有查询或记录凭证值。

| 命令 | 退出码 | 结果 / 证据边界 |
| --- | --- | --- |
| `python -B validation/prepare_phase22_baseline.py` | 0 | 248 个跟踪文件初始哈希、初始改动记录、四文件 Skill 快照；当前官方工具比对。仅首次运行，拒绝覆盖。 |
| `python -B validation/phase22_cases.py` | 0 | 17 个新确定性用例和 12 个新外部留出用例先冻结，再执行候选检查；无付费请求。 |
| `python -B validation/validate_phase22.py`（首次） | 1 | 保留两个历史运行环境/哈希门禁失败，见下节；未隐瞒、未跳过。 |
| `python -B validation/validate_phase22.py`（修正后） | 0 | 所有要求的历史/新 suites 和实际官方静态检查完成。 |
| `python -B validation/run_offline.py`（隔离副本） | 0 | 257/257。 |
| `python -B validation/run_hardening.py`（隔离副本） | 0 | 481/481。 |
| `python -B validation/run_phase13.py`（隔离副本） | 0 | 69/69，包括既有 evaluator 对抗控制。 |
| `python -B validation/run_phase2.py`（历史 gated Skill 副本） | 0 | 379/379 模拟 workflow 断言。没有执行当前 Markdown。 |
| `python -B validation/replay_phase21_history.py`（先运行的未改写副本） | 0 | 独立重放原四套历史基线 1,186/1,186。该重放与上面四套是重复验证，不重复累计总数。 |
| `python -B validation/run_phase21.py`（隔离副本） | 0 | 581/581 既有证据完整性断言。 |
| `python -B validation/test_phase21_evaluator.py`（隔离副本） | 0 | 9/9 既有评分器对抗控制。 |
| `python -B validation/check_phase21_clarifications.py`（隔离副本） | 0 | 6/6 既有事后澄清诊断，单列，不改旧 external 分数。 |
| `python -B validation/run_phase22.py` | 0 | 657/657，新 17 个冻结案例、Delta/receipt 对比、状态/拒绝/问题控制。 |
| `python -B validation/test_phase22_evaluator.py` | 0 | 34/34 手工构造的接收/拒绝控制；不是 34 次模型观察。 |
| `node D:\Ollama\Temp\rightsgap-phase22-toolchain-9404a59dcd2e4207ae764d77db25112f\extracted\uliya-skill-kit\scripts\check-skill.mjs D:\workshop\oct\rightsgap-nas\rightsgap-media-reuse` | 0 | 当前四个 Markdown 文件；0 errors / 0 warnings / 0 info。 |
| `python -B validation/prepare_phase22_materials.py` | 0 | 新未付费计划/候选/评分器冻结、人审工作表和 H21-K 原始调查。 |
| `python -B validation/evaluate_phase22.py` | 0 | 记录 EXTERNAL=NOT_RUN，0 请求、0 新费用；无 API 执行入口。 |
| `python -B validation/record_phase22_sources.py`（首次/改进记录后） | 1 / 0 | 首次 optional 本地获取遇 HTTP 403；现保存两个本地阻断和两个成功哈希。四个官方页面已通过本轮 live web 工具读到；没有把本地 403 说成页面未查或哈希成功。 |
| `python -B validation/audit_phase22.py` | 0 | 26/26 内部制品一致性检查，重新核对全部冻结哈希、2,473 唯一历史/新断言 ID、无新增模型观察、草稿词数和 Git 边界。审计项不重复加入回归断言分母。 |

现有 suites 共 **1,782/1,782**：原 1,186 + Phase 2.1 的 590 + 另列 6。新 suites 共 **691/691**：657 oracle/contract + 34 evaluator。合计 2,473 个全局唯一断言 ID；这不是 2,473 个独立样本。[历史重放](../validation/results/phase2-2/historical-regression.json)、[新断言](../validation/results/phase2-2/deterministic.json)、[新评分器控制](../validation/results/phase2-2/evaluator-controls.json)。

## 保留的失败与修正

[首次命令记录](../validation/results/phase2-2/initial-execution-1.json)和[首次回归汇总](../validation/results/phase2-2/initial-execution-1-regression.json)记录：旧 Phase 2 runner 报 `Gated implementation changed; revalidate Phase 1.3 before continuing`，因为它有意绑定旧 Skill 字节。另一个原始基线重放在已经重写临时测试结果的副本中启动，拒绝变化的 `validation/results/phase1-3/targeted-tests.json`。两者退出均为 1。

修正只涉及新的执行组织：先在尚未重写的独立目录重放原始历史基线；Phase 2 workflow runner 使用它真正绑定的历史 Skill 快照。没有改旧 gate、case、expected、policy 或当前工作区历史文件，也没有声称旧 runner 在新 Markdown 上执行成功。新候选由当前静态 checker 和新规则/本地 oracle 对照单独检查。静态与模拟基础设施仍不能证明模型遵循 Markdown。

补充公开来源获取曾因 Devpost 本地 HTTP 403 退出 1；[来源收据](../validation/results/phase2-2/official-sources.json)保留其命令/错误，分开记录 live web 已核对和本地 body hash 不可得。这不是付费 API 尝试。

## 冻结与保护

新确定性 fixture SHA-256：`3ac6cb9560b24b644bc961a5f3592f4556f37a3e536d1141d4f40ab11c57479d`。

新 holdout SHA-256：`5e89740c8035bb7ef0f10ca89c0f4d2acebae310614131dc79694dd8d0588b10`。

[用例 freeze](../validation/fixtures/phase2-2/freeze.json)先于候选测试；[未付费 study freeze](../validation/results/phase2-2/llm-freeze.json)进一步绑定实际完整四文件候选、payload、评分器与测试工具。当前没有任何外部观察，不能声称 holdout 成功，也不能事后改变预期来改善成绩。17 个 oracle 用例包括八个基础/不完整/修订/引文/变化用例、三个限定授权对照和六种注入。攻击控制保持原始文本，不进行真实越权访问。

历史 244/244 受保护文件、33/33 历史夹具原字节一致。没有重写 H21-K 预期或旧 3/12 成绩；原始 API 观察也没有变。当前 oracle 的 semantic/scope annotations 是策划的测试前提；准确引用的字面包含仍不等于实质支持。

## 当前候选与实际官方 checker

[实际 checker 输出](../validation/results/phase2-2/official-static.json)、[命令及当前文件哈希](../validation/results/phase2-2/official-static-execution.json)。检查目录仅四个 Markdown，references 全部从入口直接链接。归档、catalog、checker 指纹与当前官方 0.7.3 下载一致；没有借用旧 PASS 冒充当前候选 PASS。没有上传、安装或真实 NAS 检查。

## 未执行的外部验证与预算

拟 **12** 个全新、单次、合成 `deepseek-flash` 请求；每个输出最多 8,000 tokens，输入使用 UTF-8 byte 上界加 2,048 protocol-token 预留。按本轮查询的[官方峰值费率](https://api-docs.deepseek.com/quick_start/pricing/)：cache miss USD 0.30/百万输入、USD 1.20/百万输出，不使用缓存或非高峰折扣。保守最大估算 **USD 0.2998599**，计划预算帽 **USD 0.30**；没有独立对账的账单/税/汇率结论。需在未来授权执行前重新核对费率、候选和 payload 指纹；输出截断算失败，不重试。

**实际本轮请求数 0，估算新增费用 USD 0.00。** 没有 Phase 2.2 付费授权，未查找/读取 API 凭证，未联系模型 API、未查余额。没有重采样、重试、fallback 或私有文档发送。网页公开文档 GET 不是模型请求。记录的 provider alias 不等于独立验证的 backend revision；当前没有 returned model ID。[计划](../validation/results/phase2-2/llm-plan.json)、[NOT_RUN 分项指标](../validation/results/phase2-2/external-status.json)。

九个完整报告分项均为外部 NOT_RUN：Input Delta、Evidence Status Delta、Proof Delta、Scope Receipt、citation semantics、qualified grant、repair questions、overall status、effective dimensions。外部 unsafe-positive、unsupported accepted citation、unauthorized selected-source contamination 同样 **NOT_RUN，不能填 0**。历史零 unsafe positives 不能移植给新候选。旧 3/12 与 7/12 不构成受控比较。

## 人审、平台与门禁

[人审工作表](../validation/results/phase2-2/human-review-worksheet.md)含八个代表新案例，覆盖完整证据、跨维度不完整、部分修订、独立限制、耦合授权、注入、未知 authority 和限缩来源；提供实际合成场景、精确源片段、预期、NOT_RUN 模型状态、citation-to-claim/scope 检查点与具体修复问题。原 H21-K 三项分歧另附原模型状态和原文。没有任何人签字或作出审阅决定。

AUTOMATED_REVIEW 仅指实现 agent 的结构化交叉检查、人工策划 oracle 和评分器控制；**没有另一个独立审阅者，也没有独立法律/人工确认**。语义审阅模板用 null 保留未完成项，评分器不接受缺失、null、自报或不绑定内容哈希的审阅。

| Gate | 决策 | 依据与限制 |
| --- | --- | --- |
| G0 official static | PASS | 当前官方 checker exit 0、零错误/警告。 |
| G1 historical regression | PASS | 1,782/1,782 既有断言，包含原四套 1,186、P21 590、澄清 6；保护历史字节。 |
| G2 new deterministic correctness | PASS | 新冻结 oracle/contract 657 + evaluator controls 34 = 691/691。 |
| G3 external safety | NOT_RUN | 未授权任何本阶段付费请求；没有当前候选安全样本。 |
| G4 full report contract | NOT_RUN | 九分项全部待新的实际 frozen holdout 观察；不能由离线通过替代。 |
| G5 human review | NOT_RUN | 工作表准备完毕，实际人审/签字缺失。 |
| G6 Uliya runtime | NOT_RUN | 没有真实 instance/task/expert trace。 |
| G7 NAS runtime | NOT_RUN | 没有获准设备访问；没有合成日志/视频冒充。 |

## Phase 3 DRAFT 与后续

已核对本轮当前 [Rules](https://ugreenhackathon.devpost.com/rules)、[Resources](https://ugreenhackathon.devpost.com/resources)、[Starter Kit](https://ai.ugreen.com/pages/hackathon-starter-kit)，英文十问草稿只作审阅。实质回答按 whitespace **381 words**，保守计入标题为 **428 words**；另有 lexical 计数供审计，均低于 500。正式 PDF 尚未创建，正式 competition ZIP 尚未创建；`rightsgap-phase2-2-review.zip` 仅为工程复核包，严禁当成正式包上传。

下一步依次为：实际人审并记录争议；若 owner 另行授权，则按冻结计划和当前价格执行至多 12 次、预算至多 USD 0.30 的外部推理代理并逐项报告失败；owner 确认项目/track、原创性/资格、成员声明、AI 工具与第三方披露及最终措辞；仅获最终制作授权后生成并检查 PDF/独立 Skill ZIP；仅获提交授权后操作 Devpost。若入围再使用真正指定的 NAS 测试日，不把 Round 1 不要求 NAS 运行解释为平台已验证。

Verified：本地文件/哈希、冻结时间记录、实际子进程结果及当前静态检查。Assumed：合成文书的 curated applicability/semantic premises。Unknown：任意新文本的正确理解、真实法定权限、OCR、源覆盖/稳定身份、权限执行和模型路由。Not Run：当前候选外部、独立人审、Uliya/NAS 和运行时批准拒绝测试。

## 工程复核包

工程复核入口为 [PHASE22_REVIEW.md](../PHASE22_REVIEW.md)。`python -B validation/package_phase22_review.py` 只创建工程 ZIP，不上传；运行后的外置 `rightsgap-phase2-2-review-verification.json` 记录实际退出结果对应的 CRC、逐条字节/清单哈希、安全相对路径、无重复名、凭证常见模式检查以及 ZIP SHA-256。清单和 SHA256SUMS 排除自身递归哈希。旧工程 ZIP 和两个历史 private-reasoning 原始 payload 不入包，省略项及原哈希明确记录；已有脱敏历史最终回答仍按原来源标注，不是新模型结果。

复核包可以在独立目录运行新 691 项检查；历史 1,186 项重放必须在尚未被其他 runner 改写的副本先运行。完整工作区 244 文件的保护检查依赖原仓库，不能在缺少已声明省略文件的 ZIP 上伪称已复验全部原字节。正式 PDF、正式 Skill ZIP、Devpost 提交和 owner 最终审批仍未发生。
