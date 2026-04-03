import os
import sys
import numpy as np
import matplotlib.pyplot as plt

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_PATH = os.path.join(PROJECT_ROOT, "src")
if SRC_PATH not in sys.path:
    sys.path.append(SRC_PATH)

from trajectories import trajectory_constant_velocity, trajectory_sinusoidal
from vacuum_radiation import structural_vacuum_intensity_for_z_motion


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def plot_intensity_map(omega_grid, theta_grid, intensity, title, outpath):
    plt.figure(figsize=(9, 6))
    extent = [omega_grid[0], omega_grid[-1], theta_grid[0], theta_grid[-1]]
    plt.imshow(
        intensity,
        extent=extent,
        origin="lower",
        aspect="auto",
    )
    plt.colorbar(label=r"$I(\omega,\theta)$")
    plt.xlabel(r"$\omega$")
    plt.ylabel(r"$\theta$ [rad]")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(outpath, dpi=200)
    plt.close()
    print(f"[Saved] {outpath}")


def run_constant_velocity(fig_dir: str):
    q = 1.0
    c = 1.0
    v = 0.8

    T = 100.0
    Nt = 2500
    t = np.linspace(-T / 2, T / 2, Nt)
    z, vz = trajectory_constant_velocity(t, v=v)

    omega_grid = np.linspace(-10.0, 10.0, 301)
    theta_grid = np.linspace(0.0, np.pi, 181)

    I = structural_vacuum_intensity_for_z_motion(
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

    outpath = os.path.join(fig_dir, "task2_constant_velocity_vacuum_map.png")
    plot_intensity_map(
        omega_grid,
        theta_grid,
        I,
        title="Task 2: Vacuum Radiation Observable — Constant Velocity",
        outpath=outpath,
    )

    print(f"Max constant-velocity vacuum intensity: {np.max(I):.6e}")
    return omega_grid, theta_grid, I


def run_sinusoidal(fig_dir: str):
    q = 1.0
    c = 1.0
    d = 1.0
    omega0 = 1.5

    T = 50.0 * (2.0 * np.pi / omega0)
    Nt = 4000
    t = np.linspace(-T / 2, T / 2, Nt)
    z, vz = trajectory_sinusoidal(t, d=d, omega0=omega0)

    omega_grid = np.linspace(-10.0 * omega0, 10.0 * omega0, 401)
    theta_grid = np.linspace(0.0, np.pi, 181)

    I = structural_vacuum_intensity_for_z_motion(
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

    outpath = os.path.join(fig_dir, "task2_sinusoidal_vacuum_map.png")
    plot_intensity_map(
        omega_grid,
        theta_grid,
        I,
        title="Task 2: Vacuum Radiation Observable — Sinusoidal Motion",
        outpath=outpath,
    )

    print(f"Max sinusoidal vacuum intensity: {np.max(I):.6e}")
    return omega_grid, theta_grid, I, omega0


def compare_fixed_angle(fig_dir: str, omega_cv, I_cv, omega_sin, I_sin, theta_grid, omega0):
    theta_target = np.pi / 2
    idx = np.argmin(np.abs(theta_grid - theta_target))

    plt.figure(figsize=(9, 6))
    plt.plot(omega_cv, I_cv[idx], label=r"Constant velocity, $\theta\approx\pi/2$")
    plt.plot(omega_sin / omega0, I_sin[idx], label=r"Sinusoidal, $\theta\approx\pi/2$")
    for n in range(-8, 9):
        plt.axvline(n, linestyle="--", linewidth=0.8, alpha=0.25)
    plt.xlabel(r"$\omega$ (constant-velocity curve) / $\omega/\omega_0$ (sinusoidal curve)")
    plt.ylabel(r"$I$")
    plt.title("Task 2: Fixed-Angle Comparison")
    plt.legend()
    plt.tight_layout()

    outpath = os.path.join(fig_dir, "task2_fixed_angle_comparison.png")
    plt.savefig(outpath, dpi=200)
    plt.close()
    print(f"[Saved] {outpath}")


def main():
    fig_dir = os.path.join(PROJECT_ROOT, "figures")
    ensure_dir(fig_dir)

    omega_cv, theta_grid, I_cv = run_constant_velocity(fig_dir)
    omega_sin, theta_grid2, I_sin, omega0 = run_sinusoidal(fig_dir)

    compare_fixed_angle(
        fig_dir=fig_dir,
        omega_cv=omega_cv,
        I_cv=I_cv,
        omega_sin=omega_sin,
        I_sin=I_sin,
        theta_grid=theta_grid,
        omega0=omega0,
    )

    print("\nTask 2 pass condition:")
    print("1. Constant velocity in vacuum gives negligible intensity")
    print("2. Sinusoidal motion gives nonzero intensity")
    print("3. Sinusoidal intensity vanishes near theta = 0 and pi")
    print("4. Harmonic structure appears in frequency")


if __name__ == "__main__":
    main()