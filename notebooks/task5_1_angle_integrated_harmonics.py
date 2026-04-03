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
    Evaluate the spectral far-field observable at a single frequency:

        I_spec(omega, theta) ∝ omega^2 sin^2(theta) |J_z(kz_rad, omega)|^2
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


def angle_integrated_strength(theta_grid: np.ndarray, profile: np.ndarray) -> float:
    """
    Axisymmetric angular integration:
        S = ∫ I(theta) sin(theta) dtheta
    """
    theta_grid = np.asarray(theta_grid, dtype=float)
    profile = np.asarray(profile, dtype=float)
    return float(np.trapezoid(profile * np.sin(theta_grid), theta_grid))


def main():
    fig_dir = os.path.join(PROJECT_ROOT, "figures")
    ensure_dir(fig_dir)

    # Dipole-limit parameters
    q = 1.0
    c = 1.0
    omega0 = 1.5
    d = 0.05
    eps = omega0 * d / c

    T = 80.0 * (2.0 * np.pi / omega0)
    Nt = 3000
    t = np.linspace(-T / 2, T / 2, Nt)

    z, vz = trajectory_sinusoidal(t, d=d, omega0=omega0)

    theta_grid = np.linspace(0.0, np.pi, 181)

    harmonic_indices = np.array([1, 2, 3, 4], dtype=int)
    omega_targets = harmonic_indices * omega0

    profiles = []
    strengths = []

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
        strengths.append(angle_integrated_strength(theta_grid, prof))

    profiles = np.array(profiles)
    strengths = np.array(strengths, dtype=float)

    strengths_norm = strengths / strengths[0] if strengths[0] > 0 else strengths.copy()

    # Figure 1: absolute angular profiles
    plt.figure(figsize=(9, 6))
    for n, prof in zip(harmonic_indices, profiles):
        plt.plot(theta_grid, normalized(prof), label=fr"$\omega={n}\omega_0$")
    plt.xlabel(r"$\theta$ [rad]")
    plt.ylabel("Normalized profile")
    plt.title(fr"Task 5.1: Angular Profiles by Harmonic ($\omega_0 d/c = {eps:.3f}$)")
    plt.legend()
    plt.tight_layout()
    out1 = os.path.join(fig_dir, "task5_1_angular_profiles.png")
    plt.savefig(out1, dpi=200)
    plt.close()
    print(f"[Saved] {out1}")

    # Figure 2: angle-integrated harmonic strengths
    plt.figure(figsize=(8, 5))
    plt.plot(harmonic_indices, strengths_norm, "o-", label="Angle-integrated strength")
    plt.xlabel("Harmonic index n")
    plt.ylabel(r"Normalized $S_n/S_1$")
    plt.title("Task 5.1: Angle-Integrated Harmonic Suppression")
    plt.legend()
    plt.tight_layout()
    out2 = os.path.join(fig_dir, "task5_1_angle_integrated_strengths.png")
    plt.savefig(out2, dpi=200)
    plt.close()
    print(f"[Saved] {out2}")

    print("\nTask 5.1 diagnostics:")
    print(f"Small-amplitude parameter omega0*d/c = {eps:.6e}")

    print("\nAngle-integrated harmonic strengths:")
    for n, s, sn in zip(harmonic_indices, strengths, strengths_norm):
        print(f"  n = {n}: absolute = {s:.6e}, normalized = {sn:.6e}")

    if strengths[0] > 0:
        for idx, n in enumerate(harmonic_indices[1:], start=1):
            print(f"  ratio S(n={n}) / S(n=1): {strengths[idx] / strengths[0]:.6e}")

    print("\nTask 5.1 pass condition:")
    print("1. The angle-integrated fundamental dominates")
    print("2. Higher harmonics are strongly suppressed")
    print("3. This suppression supports the dipole-limit interpretation")


if __name__ == "__main__":
    main()