import os
import sys
import numpy as np
import matplotlib.pyplot as plt

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_PATH = os.path.join(PROJECT_ROOT, "src")
if SRC_PATH not in sys.path:
    sys.path.append(SRC_PATH)

from trajectories import trajectory_constant_velocity


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def hann_window(t: np.ndarray) -> np.ndarray:
    n = len(t)
    return np.hanning(n)


def n_dispersion(omega: np.ndarray, n0: float = 1.35, a: float = 0.25, omega_s: float = 1.5) -> np.ndarray:
    """
    Simple toy dispersion law:
        n(omega) = n0 + a / (1 + (omega/omega_s)^2)

    Positive, smooth, and easy to interpret.
    """
    omega = np.asarray(omega, dtype=float)
    return n0 + a / (1.0 + (omega / omega_s) ** 2)


def spectral_far_field_intensity_dispersive_z_motion(
    t: np.ndarray,
    z: np.ndarray,
    vz: np.ndarray,
    omega_grid: np.ndarray,
    theta_grid: np.ndarray,
    n_of_omega,
    q: float = 1.0,
    c: float = 1.0,
    normalize: bool = True,
):
    """
    Toy dispersive-medium analog of the z-motion Fourier observable.

    The source phase uses
        kz(omega,theta) = n(omega) * omega * cos(theta) / c

    and the transverse factor uses sin(theta)^2.
    """
    t = np.asarray(t, dtype=float)
    z = np.asarray(z, dtype=float)
    vz = np.asarray(vz, dtype=float)
    omega_grid = np.asarray(omega_grid, dtype=float)
    theta_grid = np.asarray(theta_grid, dtype=float)

    w = hann_window(t)
    dt = t[1] - t[0]

    intensity = np.zeros((len(theta_grid), len(omega_grid)), dtype=float)

    for j, theta in enumerate(theta_grid):
        sin2 = np.sin(theta) ** 2
        cos_th = np.cos(theta)

        amp = np.zeros(len(omega_grid), dtype=complex)

        for k, omega in enumerate(omega_grid):
            n_val = float(n_of_omega(np.array([omega]))[0])
            kz = n_val * omega * cos_th / c

            phase = np.exp(1j * omega * t - 1j * kz * z)
            # keep same structural source weighting style as earlier benchmarks
            integrand = q * vz * phase * w
            amp[k] = np.sum(integrand) * dt

        intensity[j, :] = sin2 * np.abs(amp) ** 2

    if normalize:
        m = np.max(intensity)
        if m > 0:
            intensity = intensity / m

    return intensity


def spectral_far_field_intensity_nondispersive_z_motion(
    t: np.ndarray,
    z: np.ndarray,
    vz: np.ndarray,
    omega_grid: np.ndarray,
    theta_grid: np.ndarray,
    n_medium: float,
    q: float = 1.0,
    c: float = 1.0,
    normalize: bool = True,
):
    return spectral_far_field_intensity_dispersive_z_motion(
        t=t,
        z=z,
        vz=vz,
        omega_grid=omega_grid,
        theta_grid=theta_grid,
        n_of_omega=lambda om: np.full_like(om, fill_value=n_medium, dtype=float),
        q=q,
        c=c,
        normalize=normalize,
    )


def predicted_theta_band(omega_grid: np.ndarray, beta: float, n_of_omega):
    """
    Compute predicted angle curve from
        cos(theta_C(omega)) = 1 / (n(omega) * beta)
    when physically allowed.
    """
    th = np.full_like(omega_grid, np.nan, dtype=float)
    nvals = n_of_omega(omega_grid)

    for i, (om, nv) in enumerate(zip(omega_grid, nvals)):
        x = nv * beta
        if x > 1.0:
            arg = 1.0 / x
            if -1.0 <= arg <= 1.0:
                th[i] = np.arccos(arg)

    return th


def main():
    fig_dir = os.path.join(PROJECT_ROOT, "figures")
    ensure_dir(fig_dir)

    c = 1.0
    q = 1.0

    beta = 0.80
    v = beta * c

    T = 60.0
    Nt = 1800
    t = np.linspace(-T / 2, T / 2, Nt)

    theta_grid = np.linspace(0.0, np.pi / 2, 121)
    omega_grid = np.linspace(-6.0, 6.0, 301)

    theta0 = np.pi / 3

    z, vz = trajectory_constant_velocity(t, v=v)

    # vacuum = n=1
    I_vac = spectral_far_field_intensity_nondispersive_z_motion(
        t=t, z=z, vz=vz,
        omega_grid=omega_grid, theta_grid=theta_grid,
        n_medium=1.0, q=q, c=c, normalize=True
    )

    # nondispersive comparison medium
    n0 = 1.35
    I_nondisp = spectral_far_field_intensity_nondispersive_z_motion(
        t=t, z=z, vz=vz,
        omega_grid=omega_grid, theta_grid=theta_grid,
        n_medium=n0, q=q, c=c, normalize=True
    )

    # dispersive medium
    disp_fun = lambda om: n_dispersion(om, n0=n0, a=0.25, omega_s=1.5)
    I_disp = spectral_far_field_intensity_dispersive_z_motion(
        t=t, z=z, vz=vz,
        omega_grid=omega_grid, theta_grid=theta_grid,
        n_of_omega=disp_fun, q=q, c=c, normalize=True
    )

    theta_band = predicted_theta_band(omega_grid, beta=beta, n_of_omega=disp_fun)

    # nearest angle index for 1D cut
    j0 = int(np.argmin(np.abs(theta_grid - theta0)))
    theta_used = float(theta_grid[j0])

    # -------------------------------------------------
    # Figure 1: dispersive spectral map with predicted angle band
    # -------------------------------------------------
    plt.figure(figsize=(10, 6))
    plt.imshow(
        I_disp,
        extent=[omega_grid[0], omega_grid[-1], theta_grid[0], theta_grid[-1]],
        origin="lower",
        aspect="auto",
    )
    plt.plot(omega_grid, theta_band, "--", linewidth=2, label=r"analytic $\theta_C(\omega)$")
    plt.xlabel(r"$\omega$")
    plt.ylabel(r"$\theta$ [rad]")
    plt.title(r"Task 9: Dispersive Medium Spectral Map")
    plt.colorbar(label=r"$I_{\rm disp}(\omega,\theta)$")
    plt.legend()
    plt.tight_layout()
    out1 = os.path.join(fig_dir, "task9_dispersive_map.png")
    plt.savefig(out1, dpi=200)
    plt.close()
    print(f"[Saved] {out1}")

    # -------------------------------------------------
    # Figure 2: nondispersive vs dispersive map difference
    # -------------------------------------------------
    diff_map = I_disp - I_nondisp
    plt.figure(figsize=(10, 6))
    plt.imshow(
        diff_map,
        extent=[omega_grid[0], omega_grid[-1], theta_grid[0], theta_grid[-1]],
        origin="lower",
        aspect="auto",
    )
    plt.xlabel(r"$\omega$")
    plt.ylabel(r"$\theta$ [rad]")
    plt.title(r"Task 9: Dispersive Minus Nondispersive Map")
    plt.colorbar(label=r"$I_{\rm disp} - I_{\rm nondisp}$")
    plt.tight_layout()
    out2 = os.path.join(fig_dir, "task9_disp_minus_nondisp.png")
    plt.savefig(out2, dpi=200)
    plt.close()
    print(f"[Saved] {out2}")

    # -------------------------------------------------
    # Figure 3: off-axis spectrum comparison
    # -------------------------------------------------
    plt.figure(figsize=(10, 6))
    plt.plot(omega_grid, I_vac[j0, :], label="Vacuum")
    plt.plot(omega_grid, I_nondisp[j0, :], label=fr"Nondispersive, $n={n0}$")
    plt.plot(omega_grid, I_disp[j0, :], label="Dispersive medium")
    plt.xlabel(r"$\omega$")
    plt.ylabel("Normalized spectrum")
    plt.title(fr"Task 9: Off-Axis Spectrum at $\theta \approx {theta_used:.3f}$ rad")
    plt.legend()
    plt.tight_layout()
    out3 = os.path.join(fig_dir, "task9_offaxis_spectrum_comparison.png")
    plt.savefig(out3, dpi=200)
    plt.close()
    print(f"[Saved] {out3}")

    # -------------------------------------------------
    # Figure 4: refractive index model
    # -------------------------------------------------
    plt.figure(figsize=(10, 6))
    plt.plot(omega_grid, disp_fun(omega_grid))
    plt.xlabel(r"$\omega$")
    plt.ylabel(r"$n(\omega)$")
    plt.title(r"Task 9: Toy Dispersion Law")
    plt.tight_layout()
    out4 = os.path.join(fig_dir, "task9_dispersion_law.png")
    plt.savefig(out4, dpi=200)
    plt.close()
    print(f"[Saved] {out4}")

    # diagnostics
    print("\nTask 9 diagnostics:")
    print(f"beta = {beta:.3f}")
    print(f"nondispersive comparison index n0 = {n0:.3f}")
    print(f"off-axis comparison angle theta0 = {theta_used:.6f} rad")

    nmin = float(np.min(disp_fun(omega_grid)))
    nmax = float(np.max(disp_fun(omega_grid)))
    print(f"dispersion range: n(omega) in [{nmin:.6f}, {nmax:.6f}]")

    valid = np.isfinite(theta_band)
    if np.any(valid):
        print(f"predicted angle band exists for {np.sum(valid)} / {len(valid)} omega points")
        print(f"theta_C(omega) range: [{np.nanmin(theta_band):.6f}, {np.nanmax(theta_band):.6f}] rad")
    else:
        print("no real predicted theta_C(omega) in scanned omega range")

    print("\nTask 9 pass condition:")
    print("1. Dispersive result differs smoothly from nondispersive result")
    print("2. The deformation is consistent with frequency-dependent n(omega)")
    print("3. The predicted theta_C(omega) band gives a sensible guide to the ridge geometry")


if __name__ == "__main__":
    main()