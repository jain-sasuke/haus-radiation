import os
import sys
import numpy as np
import matplotlib.pyplot as plt

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_PATH = os.path.join(PROJECT_ROOT, "src")
if SRC_PATH not in sys.path:
    sys.path.append(SRC_PATH)

from trajectories import trajectory_sinusoidal
from vacuum_radiation import spectral_far_field_intensity_for_z_motion
from medium_radiation import spectral_far_field_intensity_nondispersive_z_motion


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def normalized(arr: np.ndarray) -> np.ndarray:
    arr = np.asarray(arr, dtype=float)
    m = np.max(arr)
    if m <= 0:
        return arr.copy()
    return arr / m


def nearest_index(xgrid: np.ndarray, x: float) -> int:
    return int(np.argmin(np.abs(xgrid - x)))


def plot_map(omega_grid, theta_grid, intensity, title, outpath, omega0=None):
    plt.figure(figsize=(9, 6))
    if omega0 is None:
        extent = [omega_grid[0], omega_grid[-1], theta_grid[0], theta_grid[-1]]
        xlabel = r"$\omega$"
    else:
        extent = [omega_grid[0] / omega0, omega_grid[-1] / omega0, theta_grid[0], theta_grid[-1]]
        xlabel = r"$\omega/\omega_0$"

    plt.imshow(intensity, extent=extent, origin="lower", aspect="auto")
    plt.colorbar(label=r"$I(\omega,\theta)$")
    plt.xlabel(xlabel)
    plt.ylabel(r"$\theta$ [rad]")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(outpath, dpi=200)
    plt.close()
    print(f"[Saved] {outpath}")


def max_profile_difference(profile_a: np.ndarray, profile_b: np.ndarray) -> float:
    return float(np.max(np.abs(profile_a - profile_b)))


def main():
    fig_dir = os.path.join(PROJECT_ROOT, "figures")
    ensure_dir(fig_dir)

    q = 1.0
    c = 1.0
    omega0 = 1.5
    d = 0.2

    # Medium refractive index for the main benchmark
    n_medium = 1.5

    T = 80.0 * (2.0 * np.pi / omega0)
    Nt = 3500
    t = np.linspace(-T / 2, T / 2, Nt)

    z, vz = trajectory_sinusoidal(t, d=d, omega0=omega0)

    omega_grid = np.linspace(-5.0 * omega0, 5.0 * omega0, 601)
    theta_grid = np.linspace(0.0, np.pi, 181)

    # -----------------------------
    # Vacuum result
    # -----------------------------
    I_vac = spectral_far_field_intensity_for_z_motion(
        t=t,
        z=z,
        vz=vz,
        omega_grid=omega_grid,
        theta_grid=theta_grid,
        q=q,
        c=c,
        window="hann",
        normalize=True,
    )

    # -----------------------------
    # Medium result
    # -----------------------------
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

    # Save spectral maps
    plot_map(
        omega_grid,
        theta_grid,
        I_vac,
        title="Task 7: Vacuum Spectral Map",
        outpath=os.path.join(fig_dir, "task7_vacuum_map.png"),
        omega0=omega0,
    )

    plot_map(
        omega_grid,
        theta_grid,
        I_med,
        title=fr"Task 7: Nondispersive Medium Spectral Map (n = {n_medium})",
        outpath=os.path.join(fig_dir, "task7_medium_map.png"),
        omega0=omega0,
    )

    # -----------------------------
    # Fundamental angular profile comparison
    # -----------------------------
    idx_w1 = nearest_index(omega_grid, omega0)
    prof_vac = normalized(I_vac[:, idx_w1])
    prof_med = normalized(I_med[:, idx_w1])

    plt.figure(figsize=(9, 6))
    plt.plot(theta_grid, prof_vac, label="Vacuum")
    plt.plot(theta_grid, prof_med, "--", label=fr"Medium, n={n_medium}")
    plt.xlabel(r"$\theta$ [rad]")
    plt.ylabel("Normalized profile")
    plt.title("Task 7: Fundamental Angular Profile — Vacuum vs Medium")
    plt.legend()
    plt.tight_layout()
    out3 = os.path.join(fig_dir, "task7_fundamental_profile_comparison.png")
    plt.savefig(out3, dpi=200)
    plt.close()
    print(f"[Saved] {out3}")

    # -----------------------------
    # Off-axis fixed-angle spectrum comparison
    # IMPORTANT: do NOT use theta ~ pi/2 here
    # because cos(theta)=0 there and medium effects are muted.
    # -----------------------------
    theta0 = np.pi / 3
    idx_theta0 = np.argmin(np.abs(theta_grid - theta0))

    spec_vac = normalized(I_vac[idx_theta0])
    spec_med = normalized(I_med[idx_theta0])

    plt.figure(figsize=(9, 6))
    plt.plot(omega_grid / omega0, spec_vac, label="Vacuum")
    plt.plot(omega_grid / omega0, spec_med, "--", label=fr"Medium, n={n_medium}")
    for n in range(-5, 6):
        plt.axvline(n, linestyle="--", linewidth=0.8, alpha=0.2)
    plt.xlabel(r"$\omega/\omega_0$")
    plt.ylabel("Normalized spectrum")
    plt.title(r"Task 7: Off-Axis Spectrum — Vacuum vs Medium at $\theta\approx\pi/3$")
    plt.legend()
    plt.tight_layout()
    out4 = os.path.join(fig_dir, "task7_off_axis_spectrum_comparison.png")
    plt.savefig(out4, dpi=200)
    plt.close()
    print(f"[Saved] {out4}")

    # -----------------------------
    # Continuity check as n -> 1
    # -----------------------------
    n_close = 1.05
    I_close = spectral_far_field_intensity_nondispersive_z_motion(
        t=t,
        z=z,
        vz=vz,
        omega_grid=omega_grid,
        theta_grid=theta_grid,
        n_medium=n_close,
        q=q,
        c=c,
        window="hann",
        normalize=True,
    )

    prof_close = normalized(I_close[:, idx_w1])
    continuity_err_profile = max_profile_difference(prof_close, prof_vac)

    spec_close = normalized(I_close[idx_theta0])
    continuity_err_spectrum = max_profile_difference(spec_close, spec_vac)

    # -----------------------------
    # Diagnostics
    # -----------------------------
    fundamental_profile_diff = max_profile_difference(prof_med, prof_vac)
    off_axis_spectrum_diff = max_profile_difference(spec_med, spec_vac)

    print("\nTask 7 diagnostics:")
    print(f"Main medium refractive index n = {n_medium:.3f}")
    print(f"Off-axis comparison angle theta0 = {theta0:.6f} rad")
    print(f"Max normalized difference in fundamental angular profile (vac vs med): {fundamental_profile_diff:.6e}")
    print(f"Max normalized difference in off-axis spectrum (vac vs med):          {off_axis_spectrum_diff:.6e}")

    print(f"\nContinuity check near n -> 1 using n = {n_close:.2f}:")
    print(f"  max profile difference from vacuum:  {continuity_err_profile:.6e}")
    print(f"  max spectrum difference from vacuum: {continuity_err_spectrum:.6e}")

    print("\nTask 7 pass condition:")
    print("1. Medium result differs from vacuum in structured, sensible ways")
    print("2. Medium -> vacuum continuously as n -> 1")
    print("3. Angular and spectral patterns remain well behaved")


if __name__ == "__main__":
    main()