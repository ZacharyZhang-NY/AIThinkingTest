# Objective
严格执行一个小型但完整的物理数学项目：
“非线性单摆周期误差分析：小角近似 vs 改进级数近似 vs 数值积分真值”。

必须完成：
1）生成一组初始摆角 θ0 ∈ [θ_low, θ_high]（度），共 sample_count 个点；
2）将角度转为弧度；
3）计算单摆小角近似周期 T0 = 2π√(L/g)；
4）计算改进级数近似：
   T_series(θ0) = T0 * (1 + θ0^2/16 + 11θ0^4/3072)；
5）使用 Simpson 数值积分计算“真值周期”：
   T_num(θ0) = 4√(L/g) * ∫0→θ0 [ dθ / √(2(cosθ - cosθ0)) ]；
6）对每个 θ0，计算两个相对误差：
   err_small = |T0 - T_num| / T_num
   err_series = |T_series - T_num| / T_num
7）输出一个清晰结构化的 data.json（列表形式）
8）生成 analysis_report.md（≤ 2 页 A4）：
   - 单摆背景（简短）
   - 各方法公式
   - 数值积分方法和稳定性处理
   - 表格（θ0, T0, T_series, T_num, err_small, err_series）
   - 结果分析与结论
   - 适用范围、局限性、如何复现

不允许外部访问，不允许使用 Playwright，所有图形以 ASCII 描述或清晰文字解释。

# Inputs (fixed values)
L = 1.0
g = 9.80665
theta_low_deg = 5
theta_high_deg = 60
sample_count = 12
integral_steps = 2000
epsilon = 1e-10

# Mandatory Behaviors
- 使用 Sequential Thinking：分步骤推理、验证稳定性、控制误差。
- 使用 Task Manager：明确任务子步骤及依赖。
- 所有推理过程内部进行，不直接输出推理链条。
- 所有输出内容必须简洁、精确、专业。

# Task Manager Task Graph
tasks:
  - validate_inputs:
      check that integral_steps is even;
      check degrees range;
      check sample_count≥4;

  - generate_theta_grid:
      create evenly spaced θ0(弧度)，长度=sample_count

  - compute_T0:
      compute T0 = 2π√(L/g)

  - compute_T_series:
      for each θ0 use T0*(1 + θ0^2/16 + 11θ0^4/3072)

  - compute_T_num:
      numeric Simpson integration:
      integral = Σ f(θ_i) weighted by Simpson method
      f(θ)=1/√(2(max(cosθ−cosθ0, epsilon)))
      T_num = 4√(L/g)*integral

  - compute_errors:
      err_small = |T0−T_num|/T_num
      err_series = |T_series−T_num|/T_num

  - assemble_json:
      produce data.json containing:
      {
        "theta0_deg": [...],
        "theta0_rad": [...],
        "T0": [...],
        "T_series": [...],
        "T_num": [...],
        "err_small": [...],
        "err_series": [...]
      }

  - write_report:
      produce analysis_report.md with:
        - 背景
        - 数学公式
        - 数值积分说明
        - 表格
        - 结果解读：误差随角度增大趋势
        - 结论：小角近似在 θ0≤~20° 内可靠；级数近似到 45° 左右仍可接受
        - 局限性: 截断误差、边界奇异点处理
        - 如何复现: step-by-step 简述

  - output_artifacts:
      return:
        - data.json
        - analysis_report.md
        - summary JSON block

# Output Format
1) summary JSON:
{
  "status": "success",
  "theta_range_deg": [theta_low_deg, theta_high_deg],
  "max_err_small": max(err_small),
  "max_err_series": max(err_series),
  "largest_error_at_deg": θ0
}

2) data.json (as object)

3) analysis_report.md (≤2页)

# Constraints
- 单次运行全部完成
- 不输出内部推理文本
- 所有内容自洽、可复现、数学严谨
- 尽量避免超长文本
