对给定投资组合 {PORTFOLIO} 在 {HORIZON} 维度内做一次“自洽可复现”的分析与重构建议：

用 Playwright 访问权威站点抓取 最新价格、分红、权重、行业暴露、新闻事件与公告；

用 Sequential Thinking 拆解推理（收益/波动/相关性/集中度/情景压力测试）；

导出 Markdown 报告 + JSON/CSV 工件（含可追溯证据/时间戳/链接）；

全流程一次执行完成（不驻留后台），纽约时区时间戳。

运行输入（请替换）

PORTFOLIO（示例）：

[
  {"ticker":"AAPL","type":"equity","weight":0.18},
  {"ticker":"NVDA","type":"equity","weight":0.15},
  {"ticker":"MSFT","type":"equity","weight":0.12},
  {"ticker":"AMZN","type":"equity","weight":0.10},
  {"ticker":"SOXX","type":"etf","weight":0.15},
  {"ticker":"JEPI","type":"etf","weight":0.15},
  {"ticker":"JEPQ","type":"etf","weight":0.10},
  {"ticker":"SGOV","type":"etf","weight":0.05}
]


BASE_CCY: "USD"

HORIZON: "12M"（可选："6M"/"12M"/"36M"）

RISK_BUDGET: "moderate"（可选："conservative"/"moderate"/"aggressive"）

TARGETS: {"max_single_name_weight":0.20,"min_cash_like":0.05,"target_sharpe":">=1.0"}

EXCLUSIONS: 如需排除行业/国家/单票（例如：{"sectors":["Energy"],"countries":["CN"]}）

数据源（Playwright 抓取要求）

必须从多源交叉获取，并记录“来源-时间戳-URL”：

价格/分红/概览：Yahoo Finance、Google Finance、ETF 提供商官网（iShares/Vanguard/BlackRock/StateStreet）、公司 IR

行业/权重/持仓：ETF 官方页面“Holdings/Portfolio”

公告与监管：SEC EDGAR（10-K/10-Q/8-K）、公司新闻稿

宏观参考（可选）：FRED（3M/10Y 国债）、VIX 指数页面

若任一站点反爬/阻断，切换到备用站点；务必保存 first_contentful_paint 截图 与 最终 HTML 作为证据。

工具要求

MCP: Playwright

headless Chromium；viewport=1440x900；wait_until:"networkidle"；每站点 重试≤2（指数回退）。

需产出：screenshots/*.png（首屏/关键表格）、html_dumps/*.html、fetch_log.json（URL/时间/状态）。

MCP: Sequential Thinking

显式分步：数据校验→因子构建→相关与协方差→情景推演→权衡与结论；（内部思考不写入最终报告原文）。


串行依赖：t0_inputs → t1_fetch → t2_parse → t3_clean → t4_features → t5_reason → t6_opt → t7_report → t8_export

每任务 max_retries=2；失败记录输入快照与错误原因。

任务图（必须逐项执行）

t0_inputs

校验 PORTFOLIO 权重和为 1（±0.5% 容差）；ticker 去重与规范化（上市场所/货币）。

t1_fetch（Playwright）

对每个 ticker 抓取：最新价、当日变动、近 52W 区间、股息/分配（TTM、12M）、ETF 顶层持仓（若为 ETF）、费用率、AUM。

抓三条最新相关重大新闻标题与时间（24–72h 内优先）。

记录 source,url,timestamp,raw_html_path,screenshot_path。

t2_parse

统一单位与货币（BASE_CCY）；抽取数值字段；ETF 解析其“行业/国家/前十大持仓”。

t3_clean

缺失值/冲突处理：多源投票或最近时间优先；异常值 winsorize（1%/99%）。

t4_features

计算：组合当前权重、价格向量、股息收益率（股票/ETF）、费用率拖累。

历史收益序列：若页面可下载 CSV（Yahoo/ETF 官网），抓取最近 {HORIZON} 的 日度/周度 收益（若失败，降级为 月度）。

协方差矩阵、波动率、组合年化波动、组合收益估计（历史均值/加权分红 + 价格动量的保守混合）、夏普比（无风险利率用最新 3M T-Bill）。

集中度（Herfindahl-Hirschman Index）、单票暴露、行业/国家分布（含 ETF look-through：只对前十大持仓做近似展开）。

t5_reason（Sequential Thinking）

推理链：在 RISK_BUDGET 与 TARGETS 约束下，识别主要风险源（单票集中/行业过度/相关性挤压/红利错配/费用率拖累）。

情景测试：

基线：历史均值 ±1σ

压力：科技回撤（纳指 −15%）、利率上行（10Y+50bp）、波动上升（VIX +10）

防守：资金回撤入 SGOV 或等价短债提高现金流

t6_opt

生成两个再平衡方案：

方案A（稳健）：最小变动（权重差总和 ≤ 20%），目标 Sharpe 提升且单票 ≤ max_single_name_weight。

方案B（进取）：在满足 TARGETS 下，提升预期收益和分红；增加/替换分红 ETF（如 JEPI/JEPQ 类）或半导体敞口（SOXX/SMH）按约束扩展。

输出每方案的：新权重、预期收益/波动/Sharpe、行业/单票暴露变化、预估分红变化。

t7_report

生成 portfolio_report.md（≤4页A4），结构：

概览（组合快照、最新抓取时间、关键 KPI 表）

现状体检（收益/波动/Sharpe、集中度、行业分布、分红）

风险与洞察（相关性热力、主要风险源，附证据链接与截图标注）

情景与弹性（基线/压力/防守）

调整方案A/B（变更前后对比表 + 文字理由）

附录（数据源清单、时间戳、抓取失败与降级记录）

报告加注：“信息仅供研究参考，不构成投资建议。”

t8_export

导出：

portfolio_report.md

summary.json（核心KPI、两套方案、新旧差异、数据来源）

features.csv（逐票特征）

covariance.csv、weights_before_after.csv

fetch_log.json、screenshots/*.png、html_dumps/*.html

Playwright 细节（必须执行）

UA：桌面默认；超时 30s；遇到 Cookie/GDPR 弹窗尝试按钮集合：[Accept, I agree, Got it, Close]。

价格/概览页常用选择器提示（示例，失败则回退到文本检索）：

fin-streamer[data-field="regularMarketPrice"]（Yahoo）

section:has-text("Performance"), section:has-text("Holdings")（ETF Provider）

每支票至少保存：首屏截图 screenshots/{ticker}_above.png 与 html_dumps/{ticker}.html。

抓取新闻：只收录 时间戳可见 的前 3 条，存入 news.jsonl。

新鲜度约束：报告顶部写入生成时间（America/New_York）；若关键价格数据时间戳早于 T-1 交易日，标记 stale:true 并在报告中显著提示。

数学/统计要求

收益序列按对数收益；年化波动按 √(periods_per_year)；Sharpe = (E[R] - Rf)/σ；

Rf：抓取 3M T-Bill 最新收益率（FRED 或财经站快照）；

协方差矩阵使用样本协方差，最小正则化（对角 +1e-6）以避免病态；

组合暴露：ETF 按前十大持仓近似穿透（权重归一化）；

情景冲击用贝塔近似或历史回撤映射（保守系数）；注明假设与局限。

失败与降级策略

站点阻断→换源；连续失败→标注该票为 fetch_failed，保留其余流程并在报告列入“数据缺失与影响”。

历史 CSV 下载失败→退回到页面表格抓取或仅做“截面”分析（不做协方差更新）。

任意任务失败两次→记录 error_log.json，继续运行下游能运行的部分，报告中显著标注“部分降级”。

输出规范

顶部返回一个 summary JSON：

{
  "status":"success",
  "generated_at_tz":"America/New_York",
  "n_tickers": 8,
  "kpis":{
    "exp_return_12m": "...",
    "ann_vol":"...",
    "sharpe":"...",
    "dividend_yield":"...",
    "hhi":"..."
  },
  "proposals":[
    {"name":"Plan A - Minimal Move", "delta_turnover":"...","exp_return":"...","ann_vol":"...","sharpe":"..."},
    {"name":"Plan B - Offensive", "delta_turnover":"...","exp_return":"...","ann_vol":"...","sharpe":"..."}
  ],
  "data_freshness":{"prices":"OK|STALE", "news":"OK|STALE"}
}


其次输出 portfolio_report.md 正文（含表格与截图引用的文件名即可）。

最后列出所有工件文件相对路径清单。

# Constraints
- 单次运行全部完成
- 不输出内部推理文本
- 尽量避免超长文本

合规提示

全文添加脚注：“市场数据来自公开网页抓取，可能延迟或含误差；本内容不构成投资建议。”

不进行个股“保证收益”表述；对高风险资产附显著风险披露。