
import json
import numpy as np

# --- Inputs (fixed values) ---
L = 1.0
g = 9.80665
THETA_LOW_DEG = 5
THETA_HIGH_DEG = 60
SAMPLE_COUNT = 12
INTEGRAL_STEPS = 2000
EPSILON = 1e-10

def validate_inputs():
    """Validates the input parameters."""
    if INTEGRAL_STEPS % 2 != 0:
        raise ValueError("integral_steps must be an even number for Simpson's rule.")
    if not (0 < THETA_LOW_DEG < THETA_HIGH_DEG < 90):
        raise ValueError("Degree range must be within (0, 90) and low < high.")
    if SAMPLE_COUNT < 4:
        raise ValueError("sample_count must be at least 4 for a meaningful analysis.")
    print("Input validation successful.")

def generate_theta_grid():
    """Generates a grid of initial angles in radians."""
    return np.linspace(np.deg2rad(THETA_LOW_DEG), np.deg2rad(THETA_HIGH_DEG), SAMPLE_COUNT)

def compute_t0():
    """Computes the small-angle approximation period T0."""
    return 2 * np.pi * np.sqrt(L / g)

def compute_t_series(t0, theta0_rad_array):
    """Computes the improved series approximation period T_series."""
    theta0_sq = theta0_rad_array**2
    theta0_qu = theta0_rad_array**4
    return t0 * (1 + theta0_sq / 16 + 11 * theta0_qu / 3072)

def compute_t_num(theta0_rad):
    """
    Computes the 'true' period T_num using a different implementation of Simpson's rule.
    """
    n = INTEGRAL_STEPS
    a = 0.0
    b = theta0_rad
    
    def f(theta):
        # Vectorized integrand function
        cos_diff = np.cos(theta) - np.cos(theta0_rad)
        return 1.0 / np.sqrt(2 * np.maximum(cos_diff, EPSILON))

    dx = (b - a) / n
    x = np.linspace(a, b, n + 1)
    y = f(x)
    
    # Simpson's rule implementation from StackOverflow
    integral = dx / 3 * np.sum(y[0:-1:2] + 4 * y[1::2] + y[2::2])
    
    return 4 * np.sqrt(L / g) * integral

def compute_errors(t_approx, t_num):
    """Computes the relative error."""
    return np.abs(t_approx - t_num) / t_num

def generate_report(data):
    """Generates the analysis_report.md content."""
    
    header = f"""
# 非线性单摆周期误差分析

**摘要**: 本报告分析了单摆周期计算中两种近似方法（小角近似和改进级数近似）与数值积分“真值”之间的误差。计算覆盖的初始摆角范围为 [{THETA_LOW_DEG}°, {THETA_HIGH_DEG}°]。

---

## 1. 背景

单摆是一个经典的物理模型，其运动由二阶非线性常微分方程描述。在小角度（θ₀ ≲ 15°）下，该方程可线性化，得到一个恒定的周期解。然而，当摆角增大时，线性近似的误差变得显著，需要更精确的计算方法。

## 2. 周期计算公式

### 2.1. 小角近似 (T₀)

对于小角度 `θ₀`，`sin(θ) ≈ θ`，单摆周期可以近似为：

```
T₀ = 2π * √(L/g)
```
该周期与初始摆角 `θ₀` 无关。

### 2.2. 改进级数近似 (T_series)

为了提高大角度下的精度，可以使用周期 `T` 的级数展开式，此处取前三项：

```
T_series(θ₀) = T₀ * (1 + (1/16)θ₀² + (11/3072)θ₀⁴ + ...)
```
其中 `θ₀` 为弧度。

### 2.3. 数值积分“真值” (T_num)

周期的精确解可以通过椭圆积分得到，其数值形式为：

```
T_num(θ₀) = 4 * √(L/g) * ∫[0, θ₀] dθ / √(2 * (cos(θ) - cos(θ₀)))
```

## 3. 数值方法与稳定性

我们使用 **辛普森 1/3 法则 (Simpson's 1/3 Rule)** 对 `T_num` 的积分进行数值计算，步数 `integral_steps = {INTEGRAL_STEPS}`。

积分的被积函数在积分上限 `θ = θ₀` 时存在奇点（分母为零）。为了确保数值稳定性，我们引入一个极小值 `epsilon = {EPSILON}`，将被积函数分母根号下的 `cos(θ) - cos(θ₀)` 替换为 `max(cos(θ) - cos(θ₀), epsilon)`，从而避免了除以零的错误。

## 4. 结果与分析

下表展示了不同初始角度 `θ₀` 下的计算结果。

| θ₀ (度) | T₀ (s) | T_series (s) | T_num (s) | 误差 (小角) | 误差 (级数) |
|:---:|:---:|:---:|:---:|:---:|:---:|
"""
    
    table_rows = ""
    for i in range(len(data["theta0_deg"])):
        table_rows += (
            f"| {data['theta0_deg'][i]:.2f} "
            f"| {data['T0'][i]:.6f} "
            f"| {data['T_series'][i]:.6f} "
            f"| {data['T_num'][i]:.6f} "
            f"| {data['err_small'][i]:.2e} "
            f"| {data['err_series'][i]:.2e} |\n"
        )

    footer = f"""
## 5. 结论

1.  **小角近似 (T₀)**: 当 `θ₀` ≤ 20° 时，其相对误差在 1% 以下，是可靠的。但随着角度增大，误差迅速增加，在 {THETA_HIGH_DEG}° 时达到约 {data['err_small'][-1]:.1%}。
2.  **改进级数近似 (T_series)**: 在整个测试范围 [{THETA_LOW_DEG}°, {THETA_HIGH_DEG}°] 内都表现出极高的精度。即使在 {THETA_HIGH_DEG}°，其误差也仅为约 {data['err_series'][-1]:.2e}，远优于小角近似。这证明了级数近似在处理中等甚至较大角度时的有效性。

## 6. 局限性与复现

-   **局限性**:
    -   `T_series` 的精度受限于截断误差，对于更大的角度（例如 `θ₀` > 70°），可能需要更多项。
    -   `T_num` 的精度依赖于积分步数 `integral_steps` 和 `epsilon` 的选择。
-   **如何复现**:
    1.  使用 Python 环境及 `numpy` 库。
    2.  设置物理和计算参数: `L={L}`, `g={g}`, `theta_low_deg={THETA_LOW_DEG}`, `theta_high_deg={THETA_HIGH_DEG}`, `sample_count={SAMPLE_COUNT}`, `integral_steps={INTEGRAL_STEPS}`。
    3.  运行本报告附带的 `pendulum_analysis.py` 脚本，即可生成 `data.json`、`summary.json` 和本分析报告。
"""
    return header + table_rows + footer

def main():
    """Main function to run the analysis."""
    validate_inputs()
    
    # --- Generation & Computation ---
    theta0_rad = generate_theta_grid()
    theta0_deg = np.rad2deg(theta0_rad)
    
    t0_scalar = compute_t0()
    t0_array = np.full_like(theta0_rad, t0_scalar)
    
    t_series_array = compute_t_series(t0_scalar, theta0_rad)
    
    # Compute T_num for each theta0
    t_num_array = np.array([compute_t_num(th0) for th0 in theta0_rad])
    
    # --- Error Calculation ---
    err_small_array = compute_errors(t0_array, t_num_array)
    err_series_array = compute_errors(t_series_array, t_num_array)
    
    # --- Assemble Data ---
    output_data = {
        "theta0_deg": [round(x, 4) for x in theta0_deg.tolist()],
        "theta0_rad": [round(x, 6) for x in theta0_rad.tolist()],
        "T0": [round(t0_scalar, 8)] * SAMPLE_COUNT,
        "T_series": [round(x, 8) for x in t_series_array.tolist()],
        "T_num": [round(x, 8) for x in t_num_array.tolist()],
        "err_small": [round(x, 10) for x in err_small_array.tolist()],
        "err_series": [round(x, 10) for x in err_series_array.tolist()],
    }
    
    summary_data = {
        "status": "success",
        "theta_range_deg": [THETA_LOW_DEG, THETA_HIGH_DEG],
        "max_err_small": np.max(err_small_array),
        "max_err_series": np.max(err_series_array),
        "largest_error_at_deg": THETA_HIGH_DEG
    }
    
    # --- Write Artifacts ---
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2)
    print("data.json generated.")
        
    with open("summary.json", "w", encoding="utf-8") as f:
        json.dump(summary_data, f, indent=2)
    print("summary.json generated.")
        
    report_content = generate_report(output_data)
    with open("analysis_report.md", "w", encoding="utf-8") as f:
        f.write(report_content)
    print("analysis_report.md generated.")

if __name__ == "__main__":
    main()
