import os
import sys
import numpy as np
import matplotlib.pyplot as plt

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_PATH = os.path.join(PROJECT_ROOT, "src")
if SRC_PATH not in sys.path:
    sys.path.append(SRC_PATH)

from trajectories import trajectory_sinusoidal
from source_spectrum import compute_Jz_kw


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def normalized(arr: np.ndarray) -> np.ndarray:
    arr = np.asarray(arr, dtype=float)
    m = np.max(arr)
    if m <= 0:
        return arr.copy()
    return arr / m


def symmetry_error(theta_grid: np.ndarray, profile: np.ndarray) -> float:
    mirrored = np.interp(np.pi - theta_grid, theta_grid, profile)
    return float(np.max(np.abs(profile - mirrored)))


def spectral_intensity_single_frequency(
    t: np.ndarray,
    z: np.ndarray,
    vz: np.ndarray,
    omega: float,
    theta_grid: np.ndarray,
    q: float = 1.0,
    c: float = 1.0,
    window: str = "hann",
    normalize_source: bool = True,
) -> np.ndarray:
    """
    Fast evaluation of the spectral far-field observable at a single frequency.

    For z-directed motion:
        I_spec(omega, theta) ∝ omega^2 sin^2(theta) |J_z(kz_rad, omega)|^2
    where
        kz_rad = (omega/c) cos(theta)

    This avoids building a full (theta, omega) map.
    """
    theta_grid = np.asarray(theta_grid, dtype=float)
    intensity = np.zeros_like(theta_grid, dtype=float)

    for i, theta in enumerate(theta_grid):
        kz = (omega / c) * np.cos(theta)

        J = compute_Jz_kw(
            t=t,
            z=z,
            vz=vz,
            kz_grid=np.array([kz]),
            omega_grid=np.array([omega]),
            q=q,
            window=window,
            normalize=normalize_source,
        )[0, 0]

        intensity[i] = (omega ** 2) * (np.sin(theta) ** 2) * (np.abs(J) ** 2)

    return intensity


def main():
    fig_dir = os.path.join(PROJECT_ROOT, "figures")
    ensure_dir(fig_dir)

    # Dipole-limit parameters
    q = 1.0
    c = 1.0
    omega0 = 1.5
    d = 0.05   # small amplitude: omega0*d/c << 1
    eps = omega0 * d / c

    T = 80.0 * (2.0 * np.pi / omega0)
    Nt = 3000
    t = np.linspace(-T / 2, T / 2, Nt)
    z, vz = trajectory_sinusoidal(t, d=d, omega0=omega0)

    theta_grid = np.linspace(0.0, np.pi, 121)

    # Only evaluate the harmonics we actually need
    harmonic_indices = np.array([1, 2, 3, 4], dtype=int)
    omega_targets = harmonic_indices * omega0

    profiles = []
    harmonic_strengths = []

    for omega in omega_targets:
        prof = spectral_intensity_single_frequency(
            t=t,
            z=z,
            vz=vz,
            omega=omega,
            theta_grid=theta_grid,
            q=q,
            c=c,
            window="hann",
            normalize_source=True,
        )
        profiles.append(prof)
        # benchmark harmonic strength at theta ~ pi/2
        idx_mid = np.argmin(np.abs(theta_grid - np.pi / 2))
        harmonic_strengths.append(prof[idx_mid])

    profiles = np.array(profiles)
    harmonic_strengths = np.array(harmonic_strengths, dtype=float)
    harmonic_strengths_norm = normalized(harmonic_strengths)

    # Figure 1: harmonic angular profiles
    plt.figure(figsize=(9, 6))
    for n, prof in zip(harmonic_indices, profiles):
        plt.plot(theta_grid, normalized(prof), label=fr"$\omega={n}\omega_0$")
    plt.xlabel(r"$\theta$ [rad]")
    plt.ylabel("Normalized profile")
    plt.title(fr"Task 5 (fast): Angular Profiles in Dipole Limit ($\omega_0 d/c = {eps:.3f}$)")
    plt.legend()
    plt.tight_layout()
    out1 = os.path.join(fig_dir, "task5_fast_harmonic_profiles.png")
    plt.savefig(out1, dpi=200)
    plt.close()
    print(f"[Saved] {out1}")

    # Figure 2: harmonic-content plot
    plt.figure(figsize=(8, 5))
    plt.plot(harmonic_indices, harmonic_strengths_norm, "o-", label="Numerical")
    plt.xlabel("Harmonic index n")
    plt.ylabel("Normalized strength at $\\theta\\approx\\pi/2$")
    plt.title("Task 5 (fast): Harmonic Content in Dipole Limit")
    plt.legend()
    plt.tight_layout()
    out2 = os.path.join(fig_dir, "task5_fast_harmonic_content.png")
    plt.savefig(out2, dpi=200)
    plt.close()
    print(f"[Saved] {out2}")

    # Figure 3: fundamental vs sin^2(theta)
    prof1 = profiles[0]
    prof1_norm = normalized(prof1)
    dipole_profile = normalized(np.sin(theta_grid) ** 2)

    plt.figure(figsize=(9, 6))
    plt.plot(theta_grid, prof1_norm, label=r"Numerical at $\omega=\omega_0$")
    plt.plot(theta_grid, dipole_profile, "--", label=r"$\sin^2\theta$")
    plt.xlabel(r"$\theta$ [rad]")
    plt.ylabel("Normalized profile")
    plt.title("Task 5 (fast): Fundamental Angular Profile vs Dipole Prediction")
    plt.legend()
    plt.tight_layout()
    out3 = os.path.join(fig_dir, "task5_fast_fundamental_vs_sin2theta.png")
    plt.savefig(out3, dpi=200)
    plt.close()
    print(f"[Saved] {out3}")

    # Diagnostics
    on_axis_max = max(prof1[0], prof1[-1])
    off_axis_max = np.max(prof1)
    sym_err = symmetry_error(theta_grid, prof1_norm)
    dipole_err = float(np.max(np.abs(prof1_norm - dipole_profile)))

    print("\nTask 5 (fast) diagnostics:")
    print(f"Small-amplitude parameter omega0*d/c = {eps:.6e}")
    print(f"Fundamental on-axis max:             {on_axis_max:.6e}")
    print(f"Fundamental off-axis max:            {off_axis_max:.6e}")
    print(f"Fundamental on/off ratio:            {on_axis_max / off_axis_max:.6e}")
    print(f"Fundamental symmetry error:          {sym_err:.6e}")
    print(f"Fundamental vs sin^2(theta) max err: {dipole_err:.6e}")

    print("\nHarmonic strengths at theta ~ pi/2:")
    for n, s in zip(harmonic_indices, harmonic_strengths_norm):
        print(f"  n = {n}: {s:.6e}")

    if harmonic_strengths_norm[0] > 0:
        for idx, n in enumerate(harmonic_indices[1:], start=1):
            ratio = harmonic_strengths_norm[idx] / harmonic_strengths_norm[0]
            print(f"  ratio I(n={n}) / I(n=1): {ratio:.6e}")

    print("\nTask 5 pass condition:")
    print("1. The fundamental dominates the higher harmonics")
    print("2. The fundamental angular profile matches sin^2(theta) closely")
    print("3. On-axis suppression and symmetry remain intact")


if __name__ == "__main__":
    main()