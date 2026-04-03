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


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def nearest_index(xgrid: np.ndarray, x: float) -> int:
    return int(np.argmin(np.abs(xgrid - x)))


def normalized(arr: np.ndarray) -> np.ndarray:
    arr = np.asarray(arr, dtype=float)
    m = np.max(arr)
    if m <= 0:
        return arr.copy()
    return arr / m


def symmetry_error(theta_grid: np.ndarray, profile: np.ndarray) -> float:
    mirrored = np.interp(np.pi - theta_grid, theta_grid, profile)
    return float(np.max(np.abs(profile - mirrored)))


def main():
    fig_dir = os.path.join(PROJECT_ROOT, "figures")
    ensure_dir(fig_dir)

    # Small-amplitude dipole-limit parameters
    q = 1.0
    c = 1.0
    omega0 = 1.5
    d = 0.05   # small enough that omega0*d/c << 1
    a = omega0 * d / c

    T = 80.0 * (2.0 * np.pi / omega0)
    Nt = 5000
    t = np.linspace(-T / 2, T / 2, Nt)

    z, vz = trajectory_sinusoidal(t, d=d, omega0=omega0)

    omega_grid = np.linspace(-5.0 * omega0, 5.0 * omega0, 801)
    theta_grid = np.linspace(0.0, np.pi, 181)

    I_spec = spectral_far_field_intensity_for_z_motion(
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

    # ----------------------------
    # 1. Full map
    # ----------------------------
    plt.figure(figsize=(9, 6))
    extent = [omega_grid[0] / omega0, omega_grid[-1] / omega0, theta_grid[0], theta_grid[-1]]
    plt.imshow(I_spec, extent=extent, origin="lower", aspect="auto")
    plt.colorbar(label=r"$I_{\rm spec}(\omega,\theta)$")
    plt.xlabel(r"$\omega/\omega_0$")
    plt.ylabel(r"$\theta$ [rad]")
    plt.title(fr"Task 5: Dipole-Limit Spectral Map ($\omega_0 d/c = {a:.3f}$)")
    plt.tight_layout()
    out1 = os.path.join(fig_dir, "task5_dipole_limit_map.png")
    plt.savefig(out1, dpi=200)
    plt.close()
    print(f"[Saved] {out1}")

    # ----------------------------
    # 2. Harmonic strengths at theta ~ pi/2
    # ----------------------------
    idx_theta = np.argmin(np.abs(theta_grid - np.pi / 2))
    line_mid = I_spec[idx_theta]

    harmonic_indices = np.array([1, 2, 3, 4], dtype=int)
    harmonic_strengths = []

    for n in harmonic_indices:
        idx = nearest_index(omega_grid, n * omega0)
        harmonic_strengths.append(line_mid[idx])

    harmonic_strengths = np.array(harmonic_strengths, dtype=float)
    harmonic_strengths_norm = normalized(harmonic_strengths)

    plt.figure(figsize=(8, 5))
    plt.plot(harmonic_indices, harmonic_strengths_norm, "o-", label="Numerical harmonic strengths")
    plt.xlabel("Harmonic index n")
    plt.ylabel("Normalized strength")
    plt.title("Task 5: Harmonic Content at $\\theta\\approx\\pi/2$")
    plt.legend()
    plt.tight_layout()
    out2 = os.path.join(fig_dir, "task5_harmonic_content.png")
    plt.savefig(out2, dpi=200)
    plt.close()
    print(f"[Saved] {out2}")

    # ----------------------------
    # 3. Angular profile at omega0 vs sin^2(theta)
    # ----------------------------
    idx_omega1 = nearest_index(omega_grid, omega0)
    profile_num = I_spec[:, idx_omega1]
    profile_num_norm = normalized(profile_num)

    profile_dipole = np.sin(theta_grid) ** 2
    profile_dipole_norm = normalized(profile_dipole)

    plt.figure(figsize=(9, 6))
    plt.plot(theta_grid, profile_num_norm, label=r"Numerical profile at $\omega=\omega_0$")
    plt.plot(theta_grid, profile_dipole_norm, "--", label=r"Dipole-limit $\sin^2\theta$")
    plt.xlabel(r"$\theta$ [rad]")
    plt.ylabel("Normalized profile")
    plt.title("Task 5: Fundamental Angular Profile vs Dipole Prediction")
    plt.legend()
    plt.tight_layout()
    out3 = os.path.join(fig_dir, "task5_fundamental_vs_sin2theta.png")
    plt.savefig(out3, dpi=200)
    plt.close()
    print(f"[Saved] {out3}")

    # ----------------------------
    # 4. Quantitative diagnostics
    # ----------------------------
    on_axis_max = max(profile_num[0], profile_num[-1])
    off_axis_max = np.max(profile_num)
    sym_err = symmetry_error(theta_grid, profile_num_norm)
    dipole_err = float(np.max(np.abs(profile_num_norm - profile_dipole_norm)))

    print("\nTask 5 diagnostics:")
    print(f"Small-amplitude parameter omega0*d/c = {a:.6e}")
    print(f"Fundamental on-axis max:             {on_axis_max:.6e}")
    print(f"Fundamental off-axis max:            {off_axis_max:.6e}")
    print(f"Fundamental on/off ratio:            {on_axis_max / off_axis_max:.6e}")
    print(f"Fundamental symmetry error:          {sym_err:.6e}")
    print(f"Fundamental vs sin^2(theta) max err: {dipole_err:.6e}")

    print("\nHarmonic strengths at theta ~ pi/2:")
    for n, s in zip(harmonic_indices, harmonic_strengths_norm):
        print(f"  n = {n}: {s:.6e}")

    if harmonic_strengths_norm[0] > 0:
        for n in harmonic_indices[1:]:
            ratio = harmonic_strengths_norm[n - 1] / harmonic_strengths_norm[0]
            print(f"  ratio I(n={n}) / I(n=1): {ratio:.6e}")

    print("\nTask 5 pass condition:")
    print("1. The fundamental dominates the higher harmonics")
    print("2. The angular profile at omega0 matches sin^2(theta) closely")
    print("3. On-axis suppression and symmetry remain intact")


if __name__ == "__main__":
    main()