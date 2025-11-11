
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

def main():
    """Main function to run the analysis."""
    print("--- DEBUG RUN ---")
    theta0_rad = np.deg2rad(60.0)
    
    n = INTEGRAL_STEPS
    a = 0.0
    b = theta0_rad
    h = (b - a) / n

    def f(theta):
        cos_diff = np.cos(theta) - np.cos(theta0_rad)
        return 1.0 / np.sqrt(2 * np.maximum(cos_diff, EPSILON))

    # --- Simpson's Rule Calculation ---
    s = f(a) + f(b)
    print(f"f(a) where a=0: {f(a):.4f}")
    print(f"f(b) where b=theta0: {f(b):.4f}")

    s1 = 0
    for i in range(1, n, 2):
        s1 += f(a + i * h)
    
    s2 = 0
    for i in range(2, n, 2):
        s2 += f(a + i * h)

    print(f"Sum of f(odd steps) before multiplying by 4: {s1:.4f}")
    print(f"Sum of f(even steps) before multiplying by 2: {s2:.4f}")

    total_s = f(a) + f(b) + 4*s1 + 2*s2
    print(f"Total weighted sum of ordinates (s): {total_s:.4f}")
    
    integral = total_s * h / 3.0
    print(f"Calculated integral value (s * h / 3): {integral:.4f}")

    # --- Final Calculation ---
    t_num = 4 * np.sqrt(L / g) * integral
    print(f"sqrt(L/g): {np.sqrt(L/g):.4f}")
    print(f"Final T_num (4 * sqrt(L/g) * integral): {t_num:.4f}")

    # --- For Comparison ---
    t0_scalar = 2 * np.pi * np.sqrt(L / g)
    theta0_sq = theta0_rad**2
    theta0_qu = theta0_rad**4
    t_series = t0_scalar * (1 + theta0_sq / 16 + 11 * theta0_qu / 3072)
    print(f"T_series for comparison: {t_series:.4f}")
    print("Expected T_num should be very close to T_series.")


if __name__ == "__main__":
    main()
