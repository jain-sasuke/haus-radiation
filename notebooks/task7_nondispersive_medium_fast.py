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


def max_profile_difference(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.max(np.abs(np.asarray(a) - np.asarray(b))))


def spectral_profile_single_frequency(
    t: np.ndarray,
    z: np.ndarray,
    vz: np.ndarray,
    omega: float,
    theta_grid: np.ndarray,
    n_medium: float = 1.0,
    q: float = 1.0,
    c: float = 1.0,
    window: str = "hann",
    normalize_source: bool = True,
) -> np.ndarray:
    """
    Spectral observable at one frequency in vacuum or a nondispersive medium:

        I_spec^(n)(omega, theta) ∝ omega^2 sin^2(theta)
                                   |J_z((n*omega/c) cos(theta), omega)|^2
    """
    prof = np.zeros_like(theta_grid, dtype=float)

    for i, theta in enumerate(theta_grid):
        kz = (n_medium * omega / c) * np.cos(theta)

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

        prof[i] = (omega ** 2) * (np.sin(theta) ** 2) * (np.abs(J) ** 2)

    return prof


def spectral_slice_fixed_angle(
    t: np.ndarray,
    z: np.ndarray,
    vz: np.ndarray,
    omega_grid: np.ndarray,
    theta: float,
    n_medium: float = 1.0,
    q: float = 1.0,
    c: float = 1.0,
    window: str = "hann",
    normalize_source: bool = True,
) -> np.ndarray:
    """
    Spectral observable at one fixed angle for vacuum or medium.
    """
    kz_grid = (n_medium * omega_grid / c) * np.cos(theta)

    Jmat = compute_Jz_kw(
        t=t,
        z=z,
        vz=vz,
        kz_grid=kz_grid,
        omega_grid=omega_grid,
        q=q,
        window=window,
        normalize=normalize_source,
    )

    Jdiag = np.diag(Jmat)
    return (omega_grid ** 2) * (np.sin(theta) ** 2) * (np.abs(Jdiag) ** 2)


def main():
    fig_dir = os.path.join(PROJECT_ROOT, "figures")
    ensure_dir(fig_dir)

    q = 1.0
    c = 1.0
    omega0 = 1.5
    d = 0.2

    n_medium = 1.5
    n_close = 1.05

    T = 80.0 * (2.0 * np.pi / omega0)
    Nt = 3000
    t = np.linspace(-T / 2, T / 2, Nt)

    z, vz = trajectory_sinusoidal(t, d=d, omega0=omega0)

    theta_grid = np.linspace(0.0, np.pi, 121)
    omega_grid = np.linspace(-5.0 * omega0, 5.0 * omega0, 601)

    # -------------------------------------------------
    # 1. Fundamental angular profiles
    # -------------------------------------------------
    prof_vac = spectral_profile_single_frequency(
        t=t, z=z, vz=vz, omega=omega0, theta_grid=theta_grid,
        n_medium=1.0, q=q, c=c, window="hann", normalize_source=True
    )

    prof_med = spectral_profile_single_frequency(
        t=t, z=z, vz=vz, omega=omega0, theta_grid=theta_grid,
        n_medium=n_medium, q=q, c=c, window="hann", normalize_source=True
    )

    prof_close = spectral_profile_single_frequency(
        t=t, z=z, vz=vz, omega=omega0, theta_grid=theta_grid,
        n_medium=n_close, q=q, c=c, window="hann", normalize_source=True
    )

    prof_vac_n = normalized(prof_vac)
    prof_med_n = normalized(prof_med)
    prof_close_n = normalized(prof_close)

    plt.figure(figsize=(9, 6))
    plt.plot(theta_grid, prof_vac_n, label="Vacuum")
    plt.plot(theta_grid, prof_med_n, "--", label=fr"Medium, n={n_medium}")
    plt.plot(theta_grid, prof_close_n, ":", label=fr"Near vacuum, n={n_close}")
    plt.xlabel(r"$\theta$ [rad]")
    plt.ylabel("Normalized profile")
    plt.title("Task 7 (fast): Fundamental Angular Profile — Vacuum vs Medium")
    plt.legend()
    plt.tight_layout()
    out1 = os.path.join(fig_dir, "task7_fast_fundamental_profile_comparison.png")
    plt.savefig(out1, dpi=200)
    plt.close()
    print(f"[Saved] {out1}")

    # -------------------------------------------------
    # 2. Off-axis fixed-angle spectrum
    # -------------------------------------------------
    theta0 = np.pi / 3

    spec_vac = spectral_slice_fixed_angle(
        t=t, z=z, vz=vz, omega_grid=omega_grid, theta=theta0,
        n_medium=1.0, q=q, c=c, window="hann", normalize_source=True
    )
    spec_med = spectral_slice_fixed_angle(
        t=t, z=z, vz=vz, omega_grid=omega_grid, theta=theta0,
        n_medium=n_medium, q=q, c=c, window="hann", normalize_source=True
    )
    spec_close = spectral_slice_fixed_angle(
        t=t, z=z, vz=vz, omega_grid=omega_grid, theta=theta0,
        n_medium=n_close, q=q, c=c, window="hann", normalize_source=True
    )

    spec_vac_n = normalized(spec_vac)
    spec_med_n = normalized(spec_med)
    spec_close_n = normalized(spec_close)

    plt.figure(figsize=(9, 6))
    plt.plot(omega_grid / omega0, spec_vac_n, label="Vacuum")
    plt.plot(omega_grid / omega0, spec_med_n, "--", label=fr"Medium, n={n_medium}")
    plt.plot(omega_grid / omega0, spec_close_n, ":", label=fr"Near vacuum, n={n_close}")
    for n in range(-5, 6):
        plt.axvline(n, linestyle="--", linewidth=0.8, alpha=0.2)
    plt.xlabel(r"$\omega/\omega_0$")
    plt.ylabel("Normalized spectrum")
    plt.title(r"Task 7 (fast): Off-Axis Spectrum — Vacuum vs Medium at $\theta\approx\pi/3$")
    plt.legend()
    plt.tight_layout()
    out2 = os.path.join(fig_dir, "task7_fast_off_axis_spectrum_comparison.png")
    plt.savefig(out2, dpi=200)
    plt.close()
    print(f"[Saved] {out2}")

    # -------------------------------------------------
    # Diagnostics
    # -------------------------------------------------
    profile_diff_main = max_profile_difference(prof_med_n, prof_vac_n)
    profile_diff_close = max_profile_difference(prof_close_n, prof_vac_n)

    spectrum_diff_main = max_profile_difference(spec_med_n, spec_vac_n)
    spectrum_diff_close = max_profile_difference(spec_close_n, spec_vac_n)

    print("\nTask 7 (fast) diagnostics:")
    print(f"Main medium refractive index n = {n_medium:.3f}")
    print(f"Near-vacuum refractive index n = {n_close:.2f}")
    print(f"Off-axis comparison angle theta0 = {theta0:.6f} rad")

    print(f"\nFundamental angular profile:")
    print(f"  max diff (medium vs vacuum):     {profile_diff_main:.6e}")
    print(f"  max diff (n={n_close:.2f} vs vacuum): {profile_diff_close:.6e}")

    print(f"\nOff-axis spectrum:")
    print(f"  max diff (medium vs vacuum):     {spectrum_diff_main:.6e}")
    print(f"  max diff (n={n_close:.2f} vs vacuum): {spectrum_diff_close:.6e}")

    print("\nTask 7 (fast) pass condition:")
    print("1. Medium result differs from vacuum in structured, sensible ways")
    print("2. n -> 1 result moves continuously toward vacuum")
    print("3. Angular and spectral patterns remain well behaved")


if __name__ == "__main__":
    main()