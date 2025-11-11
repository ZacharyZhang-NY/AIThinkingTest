#!/usr/bin/env python3
"""
Nonlinear pendulum period error analysis: small angle approximation vs improved series approximation vs numerical integration
"""

import numpy as np
import math
import json

def main():
    # Fixed input parameters
    L = 1.0
    g = 9.80665
    theta_low_deg = 5
    theta_high_deg = 60
    sample_count = 12
    integral_steps = 2000
    epsilon = 1e-10

    # Task 87: Generate theta grid
    theta0_deg = np.linspace(theta_low_deg, theta_high_deg, sample_count)
    theta0_rad = theta0_deg * np.pi / 180

    print("Theta grid (degrees):", theta0_deg)
    print("Theta grid (radians):", theta0_rad)

    # Task 88: Compute T0 (small angle approximation)
    T0 = 2 * np.pi * np.sqrt(L / g)
    T0_array = np.full(sample_count, T0)  # Same T0 for all theta values

    print(f"T0 = {T0:.6f} seconds (small angle approximation)")

    # Task 89: Compute T_series (improved series approximation)
    T_series = T0 * (1 + theta0_rad**2/16 + 11*theta0_rad**4/3072)

    print("T_series values (seconds):", np.round(T_series, 6))

    # Task 90: Compute T_num (numerical integration using Simpson's method)
    def compute_integral_simpson(theta0, steps):
        """Simpson's integration for T_num calculation"""
        h = theta0 / steps  # Step size
        integral = 0.0
        cos_theta0 = np.cos(theta0)

        # Simpson's rule: integral = (h/3) * [f(0) + 4f(h) + 2f(2h) + 4f(3h) + ... + f(theta0)]
        for i in range(steps + 1):
            theta = i * h
            cos_theta = np.cos(theta)

            # f(theta) = 1/sqrt(2*(cos(theta) - cos(theta0)))
            # Note: cos(theta) >= cos(theta0) for theta in [0, theta0]
            arg = 2.0 * (cos_theta - cos_theta0)

            # Handle the endpoint where cos(theta) = cos(theta0)
            if i == steps:  # theta = theta0
                f_theta = 0.0  # Avoid division by zero
            else:
                f_theta = 1.0 / np.sqrt(arg)

            # Simpson's weights: 1, 4, 2, 4, 2, ..., 4, 1
            if i == 0 or i == steps:
                weight = 1.0
            elif i % 2 == 1:
                weight = 4.0
            else:
                weight = 2.0

            integral += weight * f_theta

        integral *= h / 3.0
        return integral

    # Compute T_num for each theta0
    T_num = np.zeros(sample_count)
    for i, theta0 in enumerate(theta0_rad):
        integral = compute_integral_simpson(theta0, integral_steps)
        T_num[i] = 4 * np.sqrt(L / g) * integral
        print(f"T_num[{theta0_deg[i]:.0f}°] = {T_num[i]:.6f} seconds")

    # Task 91: Calculate relative errors
    err_small = np.abs(T0 - T_num) / T_num
    err_series = np.abs(T_series - T_num) / T_num

    print("Relative errors (small angle):", np.round(err_small * 100, 4), "%")
    print("Relative errors (series):", np.round(err_series * 100, 4), "%")

    # Task 92: Assemble JSON data
    data = {
        "theta0_deg": theta0_deg.tolist(),
        "theta0_rad": theta0_rad.tolist(),
        "T0": T0_array.tolist(),
        "T_series": T_series.tolist(),
        "T_num": T_num.tolist(),
        "err_small": err_small.tolist(),
        "err_series": err_series.tolist()
    }

    # Save to data.json
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=2)

    print("Data saved to data.json")

    # Store parameters for next tasks
    return L, g, theta0_deg, theta0_rad, integral_steps, epsilon, T0, T0_array, T_series, T_num, err_small, err_series

if __name__ == "__main__":
    main()