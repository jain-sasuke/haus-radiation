import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import jv

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_PATH = os.path.join(PROJECT_ROOT, "src")
if SRC_PATH not in sys.path:
    sys.path.append(SRC_PATH)

from trajectories import trajectory_sinusoidal
from source_spectrum import compute_Jz_kw


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def analytic_harmonic_weights(n_vals: np.ndarray, a: float) -> np.ndarray:
    """
    Relative analytic harmonic weights for the sinusoidal source spectrum.

    A_n(a) ∝ J_{n+1}(a) + J_{n-1}(a)

    Parameters
    ----------
    n_vals : np.ndarray
        Harmonic indices.
    a : float
        Dimensionless argument a = k_z * d.

    Returns
    -------
    weights : np.ndarray
        Absolute harmonic weights, normalized to max = 1.
    """
    weights = np.abs(jv(n_vals + 1, a) + jv(n_vals - 1, a))
    max_w = np.max(weights)
    if max_w > 0:
        weights = weights / max_w
    return weights


def nearest_index(xgrid: np.ndarray, x: float) -> int:
    return int(np.argmin(np.abs(xgrid - x)))


def run_bessel_validation(fig_dir: str) -> None:
    # Chosen parameters
    q = 1.0
    d = 1.0
    omega0 = 1.5
    kz = 2.0
    a = kz * d

    # Long enough window for sharp harmonics
    T = 60.0 * (2.0 * np.pi / omega0)
    Nt = 5000

    t = np.linspace(-T / 2, T / 2, Nt)
    z, vz = trajectory_sinusoidal(t, d=d, omega0=omega0)

    # Fine omega grid
    omega_grid = np.linspace(-12.0 * omega0, 12.0 * omega0, 3001)

    J = compute_Jz_kw(
        t=t,
        z=z,
        vz=vz,
        kz_grid=np.array([kz]),
        omega_grid=omega_grid,
        q=q,
        window="hann",
        normalize=True,
    )[0]

    J_abs = np.abs(J)

    # Harmonic indices to compare
    n_vals = np.arange(-8, 9, 1)

    # Numerical peak samples at omega = n * omega0
    numerical = []
    for n in n_vals:
        idx = nearest_index(omega_grid, n * omega0)
        numerical.append(J_abs[idx])
    numerical = np.array(numerical, dtype=float)

    if np.max(numerical) > 0:
        numerical = numerical / np.max(numerical)

    analytic = analytic_harmonic_weights(n_vals, a=a)

    # --- Figure 1: full spectrum with harmonic markers ---
    plt.figure(figsize=(10, 6))
    plt.plot(omega_grid / omega0, J_abs, label=fr"Numerical, $k_z={kz}$")
    for n in n_vals:
        plt.axvline(n, linestyle="--", linewidth=0.8, alpha=0.3)
    plt.xlabel(r"$\omega/\omega_0$")
    plt.ylabel(r"$|J_z(k_z,\omega)|$")
    plt.title("Task 1.5: Sinusoidal Source Spectrum with Harmonic Markers")
    plt.legend()
    plt.tight_layout()
    out1 = os.path.join(fig_dir, "task1_5_full_spectrum.png")
    plt.savefig(out1, dpi=200)
    plt.close()

    # --- Figure 2: numerical vs analytic harmonic weights ---
    plt.figure(figsize=(9, 6))
    plt.plot(n_vals, numerical, "o-", label="Numerical harmonic heights")
    plt.plot(n_vals, analytic, "s--", label=r"Analytic $|J_{n+1}(a)+J_{n-1}(a)|$")
    plt.xlabel("Harmonic index n")
    plt.ylabel("Normalized amplitude")
    plt.title(fr"Task 1.5: Harmonic Weight Comparison (a = $k_z d = {a:.2f}$)")
    plt.legend()
    plt.tight_layout()
    out2 = os.path.join(fig_dir, "task1_5_harmonic_weight_comparison.png")
    plt.savefig(out2, dpi=200)
    plt.close()

    print(f"[Saved] {out1}")
    print(f"[Saved] {out2}")

    print("\nHarmonic comparison table:")
    print(" n    numerical    analytic")
    for n, num, ana in zip(n_vals, numerical, analytic):
        print(f"{n:>2d}    {num:>8.4f}    {ana:>8.4f}")


def main() -> None:
    fig_dir = os.path.join(PROJECT_ROOT, "figures")
    ensure_dir(fig_dir)
    run_bessel_validation(fig_dir)

    print("\nTask 1.5 pass condition:")
    print("1. Harmonic locations occur at integer multiples of omega0")
    print("2. Relative peak heights follow the analytic Bessel-weight trend")
    print("3. Remaining differences are consistent with finite-window effects")


if __name__ == "__main__":
    main()