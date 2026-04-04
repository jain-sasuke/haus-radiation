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


def normalized(arr: np.ndarray) -> np.ndarray:
    arr = np.asarray(arr, dtype=float)
    m = np.max(arr)
    if m <= 0:
        return arr.copy()
    return arr / m


def cherenkov_angle(n_medium: float, beta: float):
    """
    Return the Cherenkov angle in radians if n*beta > 1, else None.
    """
    x = n_medium * beta
    if x <= 1.0:
        return None
    return float(np.arccos(1.0 / x))


def integrated_nonzero_frequency_strength(
    intensity_map: np.ndarray,
    omega_grid: np.ndarray,
    omega_cut: float,
) -> np.ndarray:
    """
    Integrate over |omega| > omega_cut.
    """
    omega_grid = np.asarray(omega_grid, dtype=float)
    mask = np.abs(omega_grid) > omega_cut
    if not np.any(mask):
        raise ValueError("omega_cut removed all frequencies.")
    return np.trapezoid(intensity_map[:, mask], omega_grid[mask], axis=1)


def nearest_theta_index(theta_grid: np.ndarray, theta: float) -> int:
    return int(np.argmin(np.abs(theta_grid - theta)))


def main():
    fig_dir = os.path.join(PROJECT_ROOT, "figures")
    ensure_dir(fig_dir)

    c = 1.0
    q = 1.0
    n_medium = 1.5

    # Below, near, and above threshold choices
    # threshold is beta = 1/n = 0.666...
    beta_list = [0.60, 0.68, 0.80]

    # Finite-time window for constant-velocity benchmark
    T = 120.0
    Nt = 4000
    t = np.linspace(-T / 2, T / 2, Nt)

    theta_grid = np.linspace(0.0, np.pi / 2, 241)
    omega_grid = np.linspace(-6.0, 6.0, 601)

    # remove a low-frequency band to avoid trivial DC contamination
    omega_cut = 0.30

    profiles = {}
    peak_report = []

    # Keep one above-threshold full map for visual confirmation
    map_beta = 0.80
    saved_map = None

    for beta in beta_list:
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

        profiles[beta] = S_theta

        theta_pred = cherenkov_angle(n_medium=n_medium, beta=beta)
        theta_num = float(theta_grid[np.argmax(S_theta)])

        if theta_pred is None:
            peak_report.append((beta, None, theta_num))
        else:
            peak_report.append((beta, theta_pred, theta_num))

        if abs(beta - map_beta) < 1e-12:
            saved_map = I_med.copy()

    # -------------------------------------------------
    # Plot integrated angular strengths
    # -------------------------------------------------
    plt.figure(figsize=(9, 6))
    for beta in beta_list:
        label = fr"$\beta={beta:.2f}$"
        plt.plot(theta_grid, normalized(profiles[beta]), label=label)

        theta_pred = cherenkov_angle(n_medium=n_medium, beta=beta)
        if theta_pred is not None:
            plt.axvline(theta_pred, linestyle="--", linewidth=1.0, alpha=0.6)

    plt.xlabel(r"$\theta$ [rad]")
    plt.ylabel(r"Normalized $S(\theta)$")
    plt.title(fr"Task 8: Threshold-Style Angular Strength in Medium ($n={n_medium}$)")
    plt.legend()
    plt.tight_layout()
    out1 = os.path.join(fig_dir, "task8_threshold_angular_profiles.png")
    plt.savefig(out1, dpi=200)
    plt.close()
    print(f"[Saved] {out1}")

    # -------------------------------------------------
    # Plot one above-threshold spectral map
    # -------------------------------------------------
    if saved_map is not None:
        plt.figure(figsize=(9, 6))
        extent = [omega_grid[0], omega_grid[-1], theta_grid[0], theta_grid[-1]]
        plt.imshow(saved_map, extent=extent, origin="lower", aspect="auto")
        plt.colorbar(label=r"$I_{\rm spec}^{(n)}(\omega,\theta)$")
        theta_pred = cherenkov_angle(n_medium=n_medium, beta=map_beta)
        if theta_pred is not None:
            plt.axhline(theta_pred, linestyle="--", linewidth=1.2, alpha=0.8,
                        label=fr"predicted $\theta_C$ for $\beta={map_beta:.2f}$")
            plt.legend()
        plt.xlabel(r"$\omega$")
        plt.ylabel(r"$\theta$ [rad]")
        plt.title(fr"Task 8: Above-Threshold Medium Map ($n={n_medium}$, $\beta={map_beta:.2f}$)")
        plt.tight_layout()
        out2 = os.path.join(fig_dir, "task8_above_threshold_map.png")
        plt.savefig(out2, dpi=200)
        plt.close()
        print(f"[Saved] {out2}")

    # -------------------------------------------------
    # Diagnostics
    # -------------------------------------------------
    print("\nTask 8 diagnostics:")
    print(f"Medium refractive index n = {n_medium:.3f}")
    print(f"Threshold beta = 1/n = {1.0 / n_medium:.6f}")
    print(f"Low-frequency cut omega_cut = {omega_cut:.3f}")

    for beta, theta_pred, theta_num in peak_report:
        x = n_medium * beta
        print(f"\nBeta = {beta:.3f}, n*beta = {x:.6f}")
        if theta_pred is None:
            print("  predicted Cherenkov angle: none (below threshold)")
            print(f"  numerical peak angle:      {theta_num:.6f} rad")
        else:
            err = abs(theta_num - theta_pred)
            print(f"  predicted Cherenkov angle: {theta_pred:.6f} rad")
            print(f"  numerical peak angle:      {theta_num:.6f} rad")
            print(f"  absolute angle error:      {err:.6e} rad")

    print("\nTask 8 pass condition:")
    print("1. Below-threshold case shows no sharp Cherenkov-like finite-frequency peak")
    print("2. Above-threshold cases show a clear angular enhancement")
    print("3. Above-threshold peak location is close to predicted theta_C")
    print("4. The above-threshold map visually supports the same geometry")


if __name__ == "__main__":
    main()