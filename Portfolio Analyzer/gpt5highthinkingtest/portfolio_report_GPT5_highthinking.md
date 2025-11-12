# 组合分析与重构建议（12M，USD，moderate）

生成时间（America/New_York）：2025-11-11T18:57:44-05:00  数据新鲜度：prices=OK，news=PARTIAL  stale:false

信息仅供研究参考，不构成投资建议。

## 概览
- 组合规模：8 支资产；权重已校验，总和=1.00
- 关键KPI（模型估计，截面近似）：
  - 预期收益（12M）：6.84%
  - 年化波动：20.7%
  - 夏普比（Rf=3M T-Bill≈3.92%）：0.14
  - 股息收益率（已得：AAPL前瞻0.39%加权近似）：0.07%
  - 集中度 HHI：0.1368（等效成分数≈7.3）

| Ticker | Type   | Wt  | Price | d% | 备注 |
|---|---|---:|---:|---:|---|
| AAPL | equity | 0.18 | 275.25 | +2.16 | 52W: 169.21–277.32；Forward Yield≈0.39% |
| NVDA | equity | 0.15 | 193.16 | -2.96 |  |
| MSFT | equity | 0.12 | 508.68 | +0.53 |  |
| AMZN | equity | 0.10 | 249.10 | +0.28 |  |
| SOXX | etf    | 0.15 | 295.15 | -2.27 | 半导体ETF |
| JEPI | etf    | 0.15 | 57.11  | +0.69 | 股息增强（备兑+主动） |
| JEPQ | etf    | 0.10 | 58.72  | -0.09 | NASDAQ 权益溢价 |
| SGOV | etf    | 0.05 | 100.48 | +0.01 | 0–3M 美债短久期现金替代 |

证据快照（首屏）示例：
- screenshots/AAPL_above.png；screenshots/NVDA_above.png；screenshots/SOXX_above.png；screenshots/JEPI_above.png

## 现状体检
- 收益/波动/Sharpe（模型）：组合 6.84% / 20.7% / 0.14。
- 集中度：单票最高 18%（AAPL）< 20% 约束；行业科技权重高（含 SOXX/JEPQ/NVDA/MSFT）。
- 分红：AAPL 前瞻0.39%；JEPI/JEPQ 为分配型ETF（未在本轮页面稳定抓取到TTM/SEC Yield，报告中作为缺口记录）。
- 费用拖累：JEPI/JEPQ/SOXX/SGOV 费用率未从官方页稳定抓取，本轮以“未知”标记。

## 风险与洞察
- 相关性挤压：大盘科技与半导体（NVDA、MSFT、SOXX、JEPQ）相关性假设偏高（0.6–0.8），波动共振时回撤可能放大。
- 单票与主题集中：前四大科技+半导体累计>0.60 权重。
- 分红错配：组合收益更多来自价格贝塔，现金流贡献偏低；在“利率仍具黏性”环境下，股息/短债头寸可改善夏普。
- 费用与跟踪误差：增强/备兑策略（JEPI/JEPQ）在高波动期可能出现溢价/折价与分红时点偏移。

相关性热力（假设近似）与主要风险源详见 data/covariance.csv；证据截图见 screenshots/*.png。

## 情景与弹性（12M近似）
- 基线：历史常识/截面假设 E[R] 同上，σ 同上。
- 压力：
  - 科技回撤：纳指 −15% 对应（AAPL/NVDA/MSFT/JEPQ/SOXX）贝塔冲击，组合回撤约 8–12%（近似）。
  - 利率上行：10Y +50bp → 估值压缩与分红折现影响，权益 −3% 左右；SGOV 轻微受益。
  - 波动上升：VIX +10 → 备兑ETF（JEPI/JEPQ）分配可阶段性上升但净值承压。
- 防守：临时将 2–5% 权重移入 SGOV，可将组合波动下压约 0.5–1.0pct，同时维持现金流。

假设与局限：本轮未成功稳定获取完整历史CSV，协方差基于波动假设与经验相关矩阵，作为“截面近似”。

## 调整方案
约束：max_single_name_weight≤0.20；min_cash_like≥0.05；目标 Sharpe 提升；turnover 见下。

方案A（稳健，最小变动，总权重变动≈0.08）
- 新权重：AAPL 0.17 / NVDA 0.13 / MSFT 0.12 / AMZN 0.10 / SOXX 0.14 / JEPI 0.17 / JEPQ 0.12 / SGOV 0.05
- 预期：E[R]≈{data/summary.json}中的 Plan A；vol 下降、Sharpe 提升（模型）。
- 理由：
  - 适度从高波动（NVDA、SOXX）向 JEPI/JEPQ 倾斜；
  - 保持 SGOV≥5%；单票不超 20%。

方案B（进取，主题强化，总权重变动≈0.10）
- 新权重：AAPL 0.18 / NVDA 0.15 / MSFT 0.11 / AMZN 0.09 / SOXX 0.18 / JEPI 0.12 / JEPQ 0.12 / SGOV 0.05
- 预期：提高半导体与NASDAQ 权益溢价暴露，E[R] 上行、σ 上升，Sharpe 轻度改善。
- 理由：在风险预算“moderate”下，向成长与半导体主题增配，同时保留现金与收益增强因子。

变更前后对比与推导见：data/weights_before_after.csv、data/covariance.csv、data/features.csv。

## 附录
- 数据源与证据（主要）：
  - Yahoo Finance：quote 页（见 screenshots/*）；AAPL Key Statistics 获取 Forward Dividend。
  - FRED：DGS3MO（3M T-Bill）：页面最新值≈3.92%。
  - SEC EDGAR：自动化访问受限（403），已记录为降级策略。
- 抓取与降级记录：见 data/fetch_log.json、data/news.jsonl。
- 失败与影响：
  - 未能稳定抓取全部ETF官方“Holdings/Fees”表格 → 用Yahoo近似与经验值；
  - 历史CSV下载未执行 → 协方差采用截面近似（对角正则+经验相关）。

脚注：市场数据来自公开网页抓取，可能延迟或含误差；本内容不构成投资建议。

