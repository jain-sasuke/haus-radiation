import os
import sys
import numpy as np
import matplotlib.pyplot as plt

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_PATH = os.path.join(PROJECT_ROOT, "src")
if SRC_PATH not in sys.path:
    sys.path.append(SRC_PATH)

from trajectories import trajectory_constant_velocity
from medium_radiation import spectral_far_field_intensity_nondispersive_z_motion


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def cherenkov_angle(n_medium: float, beta: float):
    x = n_medium * beta
    if x <= 1.0:
        return None
    return float(np.arccos(1.0 / x))


def integrated_nonzero_frequency_strength(
    intensity_map: np.ndarray,
    omega_grid: np.ndarray,
    omega_cut: float,
) -> np.ndarray:
    mask = np.abs(omega_grid) > omega_cut
    if not np.any(mask):
        raise ValueError("omega_cut removed all frequencies.")
    return np.trapezoid(intensity_map[:, mask], omega_grid[mask], axis=1)


def main():
    fig_dir = os.path.join(PROJECT_ROOT, "figures")
    ensure_dir(fig_dir)

    c = 1.0
    q = 1.0
    n_medium = 1.5

    # Above-threshold scan
    beta_list = [0.68, 0.72, 0.76, 0.80, 0.85, 0.90]

    # Keep this reasonably light
    T = 60.0
    Nt = 1800
    t = np.linspace(-T / 2, T / 2, Nt)

    theta_grid = np.linspace(0.0, np.pi / 2, 101)
    omega_grid = np.linspace(-4.0, 4.0, 201)
    omega_cut = 0.25

    predicted = []
    numerical = []
    errors = []

    print("Starting Task 8.1 threshold scan...")
    print(f"n = {n_medium}, beta list = {beta_list}")
    print(f"Nt = {Nt}, Ntheta = {len(theta_grid)}, Nomega = {len(omega_grid)}")

    for beta in beta_list:
        print(f"\nComputing beta = {beta:.2f} ...")
        v = beta * c
        z, vz = trajectory_constant_velocity(t, v=v)

        I_med = spectral_far_field_intensity_nondispersive_z_motion(
            t=t,
            z=z,
            vz=vz,
            omega_grid=omega_grid,
            theta_grid=theta_grid,
            n_medium=n_medium,
            q=q,
            c=c,
            window="hann",
            normalize=True,
        )

        S_theta = integrated_nonzero_frequency_strength(
            intensity_map=I_med,
            omega_grid=omega_grid,
            omega_cut=omega_cut,
        )

        theta_pred = cherenkov_angle(n_medium=n_medium, beta=beta)
        theta_num = float(theta_grid[np.argmax(S_theta)])

        predicted.append(theta_pred)
        numerical.append(theta_num)
        errors.append(abs(theta_num - theta_pred))

        print(f"Finished beta = {beta:.2f}")
        print(f"  predicted theta_C = {theta_pred:.6f} rad")
        print(f"  numerical theta_peak = {theta_num:.6f} rad")
        print(f"  absolute error = {abs(theta_num - theta_pred):.6e} rad")

    predicted = np.array(predicted, dtype=float)
    numerical = np.array(numerical, dtype=float)
    errors = np.array(errors, dtype=float)
    beta_arr = np.array(beta_list, dtype=float)

    # -------------------------------------------------
    # Figure 1: predicted vs numerical angle
    # -------------------------------------------------
    plt.figure(figsize=(9, 6))
    plt.plot(beta_arr, predicted, "o-", label=r"Predicted $\theta_C$")
    plt.plot(beta_arr, numerical, "s--", label=r"Numerical $\theta_{\rm peak}$")
    plt.xlabel(r"$\beta$")
    plt.ylabel(r"Angle [rad]")
    plt.title(fr"Task 8.1: Threshold Angle Scan ($n={n_medium}$)")
    plt.legend()
    plt.tight_layout()
    out1 = os.path.join(fig_dir, "task8_1_predicted_vs_numerical_angle.png")
    plt.savefig(out1, dpi=200)
    plt.close()
    print(f"\n[Saved] {out1}")

    # -------------------------------------------------
    # Figure 2: angle error vs beta
    # -------------------------------------------------
    plt.figure(figsize=(9, 6))
    plt.plot(beta_arr, errors, "o-")
    plt.xlabel(r"$\beta$")
    plt.ylabel(r"$|\theta_{\rm peak}-\theta_C|$ [rad]")
    plt.title(fr"Task 8.1: Threshold Angle Error Scan ($n={n_medium}$)")
    plt.tight_layout()
    out2 = os.path.join(fig_dir, "task8_1_angle_error_scan.png")
    plt.savefig(out2, dpi=200)
    plt.close()
    print(f"[Saved] {out2}")

    # -------------------------------------------------
    # Diagnostics table
    # -------------------------------------------------
    print("\nTask 8.1 diagnostics:")
    print(f"Medium refractive index n = {n_medium:.3f}")
    print(f"Threshold beta = 1/n = {1.0 / n_medium:.6f}")
    print(f"Low-frequency cut omega_cut = {omega_cut:.3f}\n")

    print("beta    n*beta    theta_C(pred)    theta_peak(num)    abs_error")
    for beta, tp, tn, err in zip(beta_arr, predicted, numerical, errors):
        print(f"{beta:0.2f}    {n_medium*beta:0.6f}    {tp:0.6f}         {tn:0.6f}          {err:0.6e}")

    print("\nTask 8.1 pass condition:")
    print("1. Numerical peak angle follows the predicted theta_C trend")
    print("2. Error is largest near threshold and decreases farther above threshold")
    print("3. Predicted and numerical angle curves lie close together")


if __name__ == "__main__":
    main()