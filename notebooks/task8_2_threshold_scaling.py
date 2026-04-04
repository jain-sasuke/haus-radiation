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


def fwhm(theta_grid: np.ndarray, profile: np.ndarray):
    """
    Estimate the full width at half maximum of the dominant peak.
    Returns np.nan if width cannot be estimated robustly.
    """
    theta_grid = np.asarray(theta_grid, dtype=float)
    profile = np.asarray(profile, dtype=float)

    if np.max(profile) <= 0:
        return np.nan

    idx_peak = int(np.argmax(profile))
    peak = profile[idx_peak]
    half = 0.5 * peak

    # search left crossing
    left_idx = None
    for i in range(idx_peak, 0, -1):
        if profile[i] >= half and profile[i - 1] < half:
            left_idx = i
            break

    # search right crossing
    right_idx = None
    for i in range(idx_peak, len(profile) - 1):
        if profile[i] >= half and profile[i + 1] < half:
            right_idx = i
            break

    if left_idx is None or right_idx is None:
        return np.nan

    # linear interpolation left
    x1, x2 = theta_grid[left_idx - 1], theta_grid[left_idx]
    y1, y2 = profile[left_idx - 1], profile[left_idx]
    if y2 == y1:
        theta_left = x2
    else:
        theta_left = x1 + (half - y1) * (x2 - x1) / (y2 - y1)

    # linear interpolation right
    x1, x2 = theta_grid[right_idx], theta_grid[right_idx + 1]
    y1, y2 = profile[right_idx], profile[right_idx + 1]
    if y2 == y1:
        theta_right = x1
    else:
        theta_right = x1 + (half - y1) * (x2 - x1) / (y2 - y1)

    return float(theta_right - theta_left)


def main():
    fig_dir = os.path.join(PROJECT_ROOT, "figures")
    ensure_dir(fig_dir)

    c = 1.0
    q = 1.0
    n_medium = 1.5

    beta_list = [0.68, 0.72, 0.76, 0.80, 0.85, 0.90]

    T = 60.0
    Nt = 1800
    t = np.linspace(-T / 2, T / 2, Nt)

    theta_grid = np.linspace(0.0, np.pi / 2, 121)
    omega_grid = np.linspace(-4.0, 4.0, 201)
    omega_cut = 0.25

    xvals = []
    theta_pred_list = []
    theta_num_list = []
    peak_height_list = []
    width_list = []

    print("Starting Task 8.2 threshold scaling...")
    print(f"n = {n_medium}, beta list = {beta_list}")

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

        theta_pred = cherenkov_angle(n_medium, beta)
        theta_num = float(theta_grid[np.argmax(S_theta)])
        height = float(np.max(S_theta))
        width = fwhm(theta_grid, S_theta)

        xvals.append(n_medium * beta - 1.0)
        theta_pred_list.append(theta_pred)
        theta_num_list.append(theta_num)
        peak_height_list.append(height)
        width_list.append(width)

        print(f"  n*beta - 1 = {n_medium * beta - 1.0:.6f}")
        print(f"  theta_C(pred) = {theta_pred:.6f} rad")
        print(f"  theta_peak(num) = {theta_num:.6f} rad")
        print(f"  peak height = {height:.6e}")
        print(f"  FWHM = {width:.6e} rad")

    xvals = np.array(xvals, dtype=float)
    theta_pred_list = np.array(theta_pred_list, dtype=float)
    theta_num_list = np.array(theta_num_list, dtype=float)
    peak_height_list = np.array(peak_height_list, dtype=float)
    width_list = np.array(width_list, dtype=float)

    # -------------------------------------------------
    # Figure 1: peak angle vs distance above threshold
    # -------------------------------------------------
    plt.figure(figsize=(9, 6))
    plt.plot(xvals, theta_pred_list, "o-", label=r"Predicted $\theta_C$")
    plt.plot(xvals, theta_num_list, "s--", label=r"Numerical $\theta_{\rm peak}$")
    plt.xlabel(r"$n\beta - 1$")
    plt.ylabel("Angle [rad]")
    plt.title(fr"Task 8.2: Peak Angle vs Distance Above Threshold ($n={n_medium}$)")
    plt.legend()
    plt.tight_layout()
    out1 = os.path.join(fig_dir, "task8_2_peak_angle_vs_distance.png")
    plt.savefig(out1, dpi=200)
    plt.close()
    print(f"\n[Saved] {out1}")

    # -------------------------------------------------
    # Figure 2: peak height vs distance above threshold
    # -------------------------------------------------
    plt.figure(figsize=(9, 6))
    plt.plot(xvals, peak_height_list, "o-")
    plt.xlabel(r"$n\beta - 1$")
    plt.ylabel(r"$S_{\max}$")
    plt.title(fr"Task 8.2: Peak Height vs Distance Above Threshold ($n={n_medium}$)")
    plt.tight_layout()
    out2 = os.path.join(fig_dir, "task8_2_peak_height_vs_distance.png")
    plt.savefig(out2, dpi=200)
    plt.close()
    print(f"[Saved] {out2}")

    # -------------------------------------------------
    # Figure 3: FWHM vs distance above threshold
    # -------------------------------------------------
    plt.figure(figsize=(9, 6))
    plt.plot(xvals, width_list, "o-")
    plt.xlabel(r"$n\beta - 1$")
    plt.ylabel("FWHM [rad]")
    plt.title(fr"Task 8.2: Peak Width vs Distance Above Threshold ($n={n_medium}$)")
    plt.tight_layout()
    out3 = os.path.join(fig_dir, "task8_2_fwhm_vs_distance.png")
    plt.savefig(out3, dpi=200)
    plt.close()
    print(f"[Saved] {out3}")

    # Diagnostics table
    print("\nTask 8.2 diagnostics:")
    print(f"Medium refractive index n = {n_medium:.3f}")
    print(f"Threshold beta = 1/n = {1.0 / n_medium:.6f}")
    print(f"Low-frequency cut omega_cut = {omega_cut:.3f}\n")

    print("beta   n*beta-1   theta_C(pred)   theta_peak(num)   peak_height   FWHM")
    for beta, x, tp, tn, h, w in zip(
        beta_list, xvals, theta_pred_list, theta_num_list, peak_height_list, width_list
    ):
        print(f"{beta:0.2f}   {x:0.6f}    {tp:0.6f}        {tn:0.6f}         {h:0.6e}   {w:0.6e}")

    print("\nTask 8.2 pass condition:")
    print("1. Peak angle remains close to the threshold law")
    print("2. Peak height grows sensibly above threshold")
    print("3. Peak width decreases sensibly away from threshold")


if __name__ == "__main__":
    main()