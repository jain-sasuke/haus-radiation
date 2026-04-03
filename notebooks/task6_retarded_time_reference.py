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


def normalized(arr: np.ndarray) -> np.ndarray:
    arr = np.asarray(arr, dtype=float)
    m = np.max(arr)
    if m <= 0:
        return arr.copy()
    return arr / m


def nearest_index(xgrid: np.ndarray, x: float) -> int:
    return int(np.argmin(np.abs(xgrid - x)))


def symmetry_error(theta_grid: np.ndarray, profile: np.ndarray) -> float:
    mirrored = np.interp(np.pi - theta_grid, theta_grid, profile)
    return float(np.max(np.abs(profile - mirrored)))


def reference_spectral_map_from_acceleration(
    t: np.ndarray,
    zddot: np.ndarray,
    omega_grid: np.ndarray,
    theta_grid: np.ndarray,
    window: str = "hann",
) -> np.ndarray:
    """
    Build a nonrelativistic time-domain far-field reference:

        E_ref(t, theta) ∝ sin(theta) * zddot(t)

    Then Fourier transform in time and form

        I_ref(omega, theta) ∝ |E_ref_tilde|^2

    This compares spectral shape, not absolute normalization.
    """
    t = np.asarray(t, dtype=float)
    zddot = np.asarray(zddot, dtype=float)
    omega_grid = np.asarray(omega_grid, dtype=float)
    theta_grid = np.asarray(theta_grid, dtype=float)

    if window == "hann":
        w = np.hanning(len(t))
    else:
        w = np.ones_like(t)

    # common time-frequency kernel
    exp_omega_t = np.exp(1j * omega_grid[:, None] * t[None, :])

    I_ref = np.zeros((len(theta_grid), len(omega_grid)), dtype=float)

    for i, theta in enumerate(theta_grid):
        E_t = np.sin(theta) * zddot * w
        E_w = np.trapezoid(exp_omega_t * E_t[None, :], t, axis=1)
        I_ref[i, :] = np.abs(E_w) ** 2

    return I_ref


def plot_map(omega_grid, theta_grid, intensity, title, outpath, omega0=None):
    plt.figure(figsize=(9, 6))
    if omega0 is None:
        x0, x1 = omega_grid[0], omega_grid[-1]
        xlabel = r"$\omega$"
    else:
        x0, x1 = omega_grid[0] / omega0, omega_grid[-1] / omega0
        xlabel = r"$\omega/\omega_0$"

    extent = [x0, x1, theta_grid[0], theta_grid[-1]]
    plt.imshow(intensity, extent=extent, origin="lower", aspect="auto")
    plt.colorbar(label=r"$I(\omega,\theta)$")
    plt.xlabel(xlabel)
    plt.ylabel(r"$\theta$ [rad]")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(outpath, dpi=200)
    plt.close()
    print(f"[Saved] {outpath}")


def main():
    fig_dir = os.path.join(PROJECT_ROOT, "figures")
    ensure_dir(fig_dir)

    # Keep this clearly nonrelativistic
    q = 1.0
    c = 1.0
    omega0 = 1.5
    d = 0.2
    eps = omega0 * d / c

    T = 80.0 * (2.0 * np.pi / omega0)
    Nt = 4000
    t = np.linspace(-T / 2, T / 2, Nt)

    z, vz = trajectory_sinusoidal(t, d=d, omega0=omega0)
    zddot = -d * (omega0 ** 2) * np.sin(omega0 * t)

    omega_grid = np.linspace(-5.0 * omega0, 5.0 * omega0, 801)
    theta_grid = np.linspace(0.0, np.pi, 181)

    # Fourier-domain solver
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

    # Time-domain reference from transverse acceleration
    I_ref = reference_spectral_map_from_acceleration(
        t=t,
        zddot=zddot,
        omega_grid=omega_grid,
        theta_grid=theta_grid,
        window="hann",
    )

    # Save spectral maps
    plot_map(
        omega_grid,
        theta_grid,
        I_spec,
        title=fr"Task 6: Fourier-Domain Solver Map ($\omega_0 d/c = {eps:.3f}$)",
        outpath=os.path.join(fig_dir, "task6_solver_map.png"),
        omega0=omega0,
    )

    plot_map(
        omega_grid,
        theta_grid,
        I_ref,
        title=fr"Task 6: Time-Domain Reference Map ($\omega_0 d/c = {eps:.3f}$)",
        outpath=os.path.join(fig_dir, "task6_reference_map.png"),
        omega0=omega0,
    )

    # Compare fundamental angular profile
    idx_omega1 = nearest_index(omega_grid, omega0)
    prof_spec = normalized(I_spec[:, idx_omega1])
    prof_ref = normalized(I_ref[:, idx_omega1])

    plt.figure(figsize=(9, 6))
    plt.plot(theta_grid, prof_spec, label=r"Fourier-domain solver")
    plt.plot(theta_grid, prof_ref, "--", label=r"Time-domain reference")
    plt.xlabel(r"$\theta$ [rad]")
    plt.ylabel("Normalized profile")
    plt.title("Task 6: Fundamental Angular Profile Comparison")
    plt.legend()
    plt.tight_layout()
    out3 = os.path.join(fig_dir, "task6_fundamental_profile_comparison.png")
    plt.savefig(out3, dpi=200)
    plt.close()
    print(f"[Saved] {out3}")

    # Compare fixed-angle spectra at theta ~ pi/2
    idx_mid = np.argmin(np.abs(theta_grid - np.pi / 2))
    line_spec = normalized(I_spec[idx_mid])
    line_ref = normalized(I_ref[idx_mid])

    plt.figure(figsize=(9, 6))
    plt.plot(omega_grid / omega0, line_spec, label="Fourier-domain solver")
    plt.plot(omega_grid / omega0, line_ref, "--", label="Time-domain reference")
    for n in range(-5, 6):
        plt.axvline(n, linestyle="--", linewidth=0.8, alpha=0.2)
    plt.xlabel(r"$\omega/\omega_0$")
    plt.ylabel("Normalized spectrum")
    plt.title(r"Task 6: Fixed-Angle Spectral Comparison at $\theta \approx \pi/2$")
    plt.legend()
    plt.tight_layout()
    out4 = os.path.join(fig_dir, "task6_fixed_angle_spectrum_comparison.png")
    plt.savefig(out4, dpi=200)
    plt.close()
    print(f"[Saved] {out4}")

    # Diagnostics
    sym_spec = symmetry_error(theta_grid, prof_spec)
    sym_ref = symmetry_error(theta_grid, prof_ref)
    prof_err = float(np.max(np.abs(prof_spec - prof_ref)))

    print("\nTask 6 diagnostics:")
    print(f"Nonrelativistic parameter omega0*d/c = {eps:.6e}")
    print(f"Fundamental profile symmetry error (solver):    {sym_spec:.6e}")
    print(f"Fundamental profile symmetry error (reference): {sym_ref:.6e}")
    print(f"Max normalized profile difference:              {prof_err:.6e}")

    # harmonic comparison at theta ~ pi/2
    print("\nFixed-angle harmonic content at theta ~ pi/2:")
    for n in [1, 2, 3, 4]:
        idx = nearest_index(omega_grid, n * omega0)
        print(f"  n = {n}: solver = {line_spec[idx]:.6e}, reference = {line_ref[idx]:.6e}")

    print("\nTask 6 pass condition:")
    print("1. Solver and reference agree on the dominant harmonic structure")
    print("2. Fundamental angular profiles match closely after normalization")
    print("3. Symmetry and on-axis suppression agree")
    print("4. Remaining differences are consistent with finite-window and normalization effects")


if __name__ == "__main__":
    main()