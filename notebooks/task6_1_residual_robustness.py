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
    m = np.max(np.abs(arr))
    if m <= 0:
        return arr.copy()
    return arr / m


def symmetry_error(theta_grid: np.ndarray, profile: np.ndarray) -> float:
    mirrored = np.interp(np.pi - theta_grid, theta_grid, profile)
    return float(np.max(np.abs(profile - mirrored)))


def solver_profile_single_frequency(
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
    prof = np.zeros_like(theta_grid, dtype=float)

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
        prof[i] = (omega ** 2) * (np.sin(theta) ** 2) * (np.abs(J) ** 2)

    return prof


def reference_profile_single_frequency(
    t: np.ndarray,
    zddot: np.ndarray,
    omega: float,
    theta_grid: np.ndarray,
    window: str = "hann",
) -> np.ndarray:
    if window == "hann":
        w = np.hanning(len(t))
    else:
        w = np.ones_like(t)

    kernel = np.exp(1j * omega * t)
    prof = np.zeros_like(theta_grid, dtype=float)

    for i, theta in enumerate(theta_grid):
        E_t = np.sin(theta) * zddot * w
        E_w = np.trapezoid(E_t * kernel, t)
        prof[i] = np.abs(E_w) ** 2

    return prof


def solver_spectrum_fixed_angle(
    t: np.ndarray,
    z: np.ndarray,
    vz: np.ndarray,
    omega_grid: np.ndarray,
    theta: float,
    q: float = 1.0,
    c: float = 1.0,
    window: str = "hann",
    normalize_source: bool = True,
) -> np.ndarray:
    kz_grid = (omega_grid / c) * np.cos(theta)
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


def reference_spectrum_fixed_angle(
    t: np.ndarray,
    zddot: np.ndarray,
    omega_grid: np.ndarray,
    theta: float,
    window: str = "hann",
) -> np.ndarray:
    if window == "hann":
        w = np.hanning(len(t))
    else:
        w = np.ones_like(t)

    E_t = np.sin(theta) * zddot * w
    kernel = np.exp(1j * omega_grid[:, None] * t[None, :])
    Ew = np.trapezoid(kernel * E_t[None, :], t, axis=1)
    return np.abs(Ew) ** 2


def run_case(fig_dir: str, omega0: float, d: float, c: float = 1.0):
    eps = omega0 * d / c

    T = 80.0 * (2.0 * np.pi / omega0)
    Nt = 3000
    t = np.linspace(-T / 2, T / 2, Nt)

    z, vz = trajectory_sinusoidal(t, d=d, omega0=omega0)
    zddot = -d * (omega0 ** 2) * np.sin(omega0 * t)

    theta_grid = np.linspace(0.0, np.pi, 121)
    omega_grid = np.linspace(-5.0 * omega0, 5.0 * omega0, 601)

    # Fundamental angular profile
    prof_solver = solver_profile_single_frequency(
        t=t, z=z, vz=vz, omega=omega0, theta_grid=theta_grid,
        c=c, window="hann", normalize_source=True
    )
    prof_ref = reference_profile_single_frequency(
        t=t, zddot=zddot, omega=omega0, theta_grid=theta_grid, window="hann"
    )

    prof_solver_n = normalized(prof_solver)
    prof_ref_n = normalized(prof_ref)
    residual = prof_solver_n - prof_ref_n

    plt.figure(figsize=(9, 6))
    plt.plot(theta_grid, prof_solver_n, label="Solver")
    plt.plot(theta_grid, prof_ref_n, "--", label="Reference")
    plt.xlabel(r"$\theta$ [rad]")
    plt.ylabel("Normalized profile")
    plt.title(fr"Task 6.1: Fundamental Profile Comparison ($\omega_0 d/c={eps:.3f}$)")
    plt.legend()
    plt.tight_layout()
    out1 = os.path.join(fig_dir, f"task6_1_profile_compare_eps_{eps:.3f}.png")
    plt.savefig(out1, dpi=200)
    plt.close()
    print(f"[Saved] {out1}")

    plt.figure(figsize=(9, 4.5))
    plt.plot(theta_grid, residual)
    plt.axhline(0.0, linestyle="--", linewidth=1.0)
    plt.xlabel(r"$\theta$ [rad]")
    plt.ylabel("Solver - Reference")
    plt.title(fr"Task 6.1: Fundamental Profile Residual ($\omega_0 d/c={eps:.3f}$)")
    plt.tight_layout()
    out2 = os.path.join(fig_dir, f"task6_1_profile_residual_eps_{eps:.3f}.png")
    plt.savefig(out2, dpi=200)
    plt.close()
    print(f"[Saved] {out2}")

    # Off-axis spectra at several angles
    angle_list = [np.pi / 6, np.pi / 4, np.pi / 3]

    for theta0 in angle_list:
        spec_solver = solver_spectrum_fixed_angle(
            t=t, z=z, vz=vz, omega_grid=omega_grid, theta=theta0,
            c=c, window="hann", normalize_source=True
        )
        spec_ref = reference_spectrum_fixed_angle(
            t=t, zddot=zddot, omega_grid=omega_grid, theta=theta0, window="hann"
        )

        # separate normalization
        spec_solver_n = normalized(spec_solver)
        spec_ref_n = normalized(spec_ref)

        plt.figure(figsize=(9, 6))
        plt.plot(omega_grid / omega0, spec_solver_n, label="Solver")
        plt.plot(omega_grid / omega0, spec_ref_n, "--", label="Reference")
        for n in range(-5, 6):
            plt.axvline(n, linestyle="--", linewidth=0.8, alpha=0.2)
        plt.xlabel(r"$\omega/\omega_0$")
        plt.ylabel("Normalized spectrum")
        plt.title(fr"Task 6.1: Spectrum at $\theta={theta0:.3f}$, $\omega_0 d/c={eps:.3f}$")
        plt.legend()
        plt.tight_layout()
        out3 = os.path.join(fig_dir, f"task6_1_spectrum_norm_theta_{theta0:.3f}_eps_{eps:.3f}.png")
        plt.savefig(out3, dpi=200)
        plt.close()
        print(f"[Saved] {out3}")

        # joint scaling
        joint_scale = max(np.max(spec_solver), np.max(spec_ref), 1e-30)
        plt.figure(figsize=(9, 6))
        plt.plot(omega_grid / omega0, spec_solver / joint_scale, label="Solver")
        plt.plot(omega_grid / omega0, spec_ref / joint_scale, "--", label="Reference")
        for n in range(-5, 6):
            plt.axvline(n, linestyle="--", linewidth=0.8, alpha=0.2)
        plt.xlabel(r"$\omega/\omega_0$")
        plt.ylabel("Jointly scaled spectrum")
        plt.title(fr"Task 6.1: Joint-Scale Spectrum at $\theta={theta0:.3f}$, $\omega_0 d/c={eps:.3f}$")
        plt.legend()
        plt.tight_layout()
        out4 = os.path.join(fig_dir, f"task6_1_spectrum_joint_theta_{theta0:.3f}_eps_{eps:.3f}.png")
        plt.savefig(out4, dpi=200)
        plt.close()
        print(f"[Saved] {out4}")

        # diagnostics for harmonics
        print(fr"\nAngle theta = {theta0:.6f}, eps = {eps:.3f}")
        for n in [1, 2, 3, 4]:
            idx = int(np.argmin(np.abs(omega_grid - n * omega0)))
            print(
                f"  n = {n}: "
                f"solver(norm) = {spec_solver_n[idx]:.6e}, "
                f"reference(norm) = {spec_ref_n[idx]:.6e}, "
                f"solver(joint) = {(spec_solver[idx]/joint_scale):.6e}, "
                f"reference(joint) = {(spec_ref[idx]/joint_scale):.6e}"
            )

    # diagnostics for profile
    prof_err = float(np.max(np.abs(residual)))
    print(f"\nTask 6.1 diagnostics for eps = {eps:.3f}:")
    print(f"  profile max residual: {prof_err:.6e}")
    print(f"  solver symmetry error: {symmetry_error(theta_grid, prof_solver_n):.6e}")
    print(f"  reference symmetry error: {symmetry_error(theta_grid, prof_ref_n):.6e}")


def main():
    fig_dir = os.path.join(PROJECT_ROOT, "figures")
    ensure_dir(fig_dir)

    omega0 = 1.5

    # two amplitudes: moderate and harder
    d_values = [0.2, 1.0 / 3.0]  # eps = 0.3 and 0.5 for c=1

    for d in d_values:
        run_case(fig_dir, omega0=omega0, d=d, c=1.0)

    print("\nTask 6.1 pass condition:")
    print("1. Residuals stay small and structured")
    print("2. Agreement persists at several off-axis angles")
    print("3. Differences grow sensibly as amplitude increases")
    print("4. No unphysical asymmetry or instability appears")


if __name__ == "__main__":
    main()