import os
import sys
import time
import numpy as np
import matplotlib.pyplot as plt

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_PATH = os.path.join(PROJECT_ROOT, "src")
if SRC_PATH not in sys.path:
    sys.path.append(SRC_PATH)

from jax_radiation import make_jax_grids, intensity_map_two_frequency_raw


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def trapz_weights_np(x):
    x = np.asarray(x, dtype=float)
    dx = np.diff(x)
    w = np.zeros_like(x)
    w[0] = dx[0] / 2.0
    w[-1] = dx[-1] / 2.0
    if len(x) > 2:
        w[1:-1] = 0.5 * (dx[:-1] + dx[1:])
    return w


def make_ff_weights(omega_grid, omega_cut=0.25):
    w = trapz_weights_np(omega_grid)
    mask = (np.abs(omega_grid) > omega_cut).astype(float)
    return w * mask


def make_theta_sector_weights(theta_grid, theta_lo=0.55, theta_hi=0.80):
    w = trapz_weights_np(theta_grid)
    mask = ((theta_grid >= theta_lo) & (theta_grid <= theta_hi)).astype(float)
    return w * mask


def score_from_map(I_map, w_omega, w_theta):
    score_theta = np.sum(I_map * w_omega[None, :], axis=1)
    return float(np.sum(score_theta * w_theta))


def rms(x):
    return float(np.sqrt(np.mean(np.asarray(x) ** 2)))


def constrained_two_harmonic_trajectory(t, r, phi, omega1=1.0, vrms_target=None):
    """
    Raw ansatz:
        z_raw = sin(omega t) + r sin(2 omega t + phi)

    Then rescale whole trajectory by alpha so that
        RMS(v) = vrms_target

    If vrms_target is None, returns the unscaled raw trajectory.
    """
    t = np.asarray(t, dtype=float)
    omega2 = 2.0 * omega1

    z_raw = np.sin(omega1 * t) + r * np.sin(omega2 * t + phi)
    v_raw = omega1 * np.cos(omega1 * t) + r * omega2 * np.cos(omega2 * t + phi)

    if vrms_target is None:
        return z_raw, v_raw, 1.0

    vrms_raw = rms(v_raw)
    if vrms_raw <= 1e-14:
        alpha = 0.0
    else:
        alpha = vrms_target / vrms_raw

    z = alpha * z_raw
    v = alpha * v_raw
    return z, v, alpha


def compute_map_from_zv(grids, z, v, c=1.0):
    """
    Same radiation kernel, but directly from supplied z(t), v(t).
    """
    t = np.array(grids["t"])
    theta_grid = np.array(grids["theta_grid"])
    omega_grid = np.array(grids["omega_grid"])
    w_t = np.array(grids["w_t"])

    amps = np.zeros((len(theta_grid), len(omega_grid)), dtype=np.complex128)

    for i, theta in enumerate(theta_grid):
        tau = t - np.cos(theta) * z / c
        phase = np.exp(1j * omega_grid[:, None] * tau[None, :])
        amps[i, :] = np.sum((v * w_t)[None, :] * phase, axis=1)

    I = (
        (omega_grid[None, :] ** 2)
        * (np.sin(theta_grid)[:, None] ** 2)
        * (np.abs(amps) ** 2)
    )
    return I


def main():
    print("Starting Task 11A constrained optimization...", flush=True)

    fig_dir = os.path.join(PROJECT_ROOT, "figures")
    ensure_dir(fig_dir)

    grids = make_jax_grids(
        T=60.0,
        Nt=1200,
        theta_min=0.0,
        theta_max=np.pi,
        Ntheta=61,
        omega_min=-5.0,
        omega_max=5.0,
        Nomega=121,
        omega_cut=0.25,
    )

    t_grid = np.array(grids["t"])
    theta_grid = np.array(grids["theta_grid"])
    omega_grid = np.array(grids["omega_grid"])
    w_theta_full = np.array(grids["w_theta"])

    omega1 = 1.0
    omega_cut = 0.25
    theta_lo = 0.55
    theta_hi = 0.80

    w_omega_ff = make_ff_weights(omega_grid, omega_cut=omega_cut)
    w_theta_sector = make_theta_sector_weights(theta_grid, theta_lo=theta_lo, theta_hi=theta_hi)

    # Baseline with fixed RMS velocity target
    z_base_raw = np.sin(omega1 * t_grid)
    v_base_raw = omega1 * np.cos(omega1 * t_grid)
    vrms_target = rms(v_base_raw)

    z_base, v_base, alpha_base = constrained_two_harmonic_trajectory(
        t_grid, r=0.0, phi=0.0, omega1=omega1, vrms_target=vrms_target
    )
    I_base = compute_map_from_zv(grids, z_base, v_base, c=1.0)

    Ssector_base = score_from_map(I_base, w_omega_ff, w_theta_sector)
    Sff_base = score_from_map(I_base, w_omega_ff, w_theta_full)

    print(f"vrms target     = {vrms_target:.6e}", flush=True)
    print(f"Ssector(base)   = {Ssector_base:.6e}", flush=True)
    print(f"Sff(base)       = {Sff_base:.6e}", flush=True)
    print(f"Narrow sector   = [{theta_lo:.3f}, {theta_hi:.3f}] rad", flush=True)

    # Search over amplitude ratio r and phase phi
    r_vals = np.linspace(0.0, 1.0, 17)
    phi_vals = np.linspace(0.0, 2 * np.pi, 36, endpoint=False)

    Rtheta_grid = np.zeros((len(r_vals), len(phi_vals)))
    Rff_grid = np.zeros((len(r_vals), len(phi_vals)))
    alpha_grid = np.zeros((len(r_vals), len(phi_vals)))

    all_cases = []

    t0 = time.time()

    for i, r in enumerate(r_vals):
        for j, phi in enumerate(phi_vals):
            z, v, alpha = constrained_two_harmonic_trajectory(
                t_grid, r=r, phi=phi, omega1=omega1, vrms_target=vrms_target
            )

            I = compute_map_from_zv(grids, z, v, c=1.0)

            Ssector = score_from_map(I, w_omega_ff, w_theta_sector)
            Sff = score_from_map(I, w_omega_ff, w_theta_full)

            Rtheta = Ssector / Ssector_base
            Rff = Sff / Sff_base

            Rtheta_grid[i, j] = Rtheta
            Rff_grid[i, j] = Rff
            alpha_grid[i, j] = alpha

            all_cases.append({
                "r": float(r),
                "phi": float(phi),
                "alpha": float(alpha),
                "Ssector": float(Ssector),
                "Sff": float(Sff),
                "Rtheta": float(Rtheta),
                "Rff": float(Rff),
            })

    t1 = time.time()
    print(f"Total optimization scan time: {t1 - t0:.2f} s", flush=True)

    all_cases = sorted(all_cases, key=lambda d: d["Rtheta"])
    top = all_cases[:10]

    print("\nTop 10 constrained candidates by narrow-sector suppression:", flush=True)
    for k, case in enumerate(top, start=1):
        print(
            f"{k}. r={case['r']:.3f}, "
            f"phi={case['phi']:.3f}, "
            f"alpha={case['alpha']:.6f}, "
            f"Ssector={case['Ssector']:.6e}, "
            f"Rtheta={case['Rtheta']:.6e}, "
            f"(1-Rtheta)={1.0 - case['Rtheta']:.6e}, "
            f"Sff={case['Sff']:.6e}, "
            f"Rff={case['Rff']:.6e}",
            flush=True
        )

    best = top[0]
    z_best, v_best, alpha_best = constrained_two_harmonic_trajectory(
        t_grid, r=best["r"], phi=best["phi"], omega1=omega1, vrms_target=vrms_target
    )
    I_best = compute_map_from_zv(grids, z_best, v_best, c=1.0)

    extent = [omega_grid[0], omega_grid[-1], theta_grid[0], theta_grid[-1]]

    # Heatmap: directional suppression
    sector_supp = 1.0 - Rtheta_grid
    vmax = max(0.01, float(np.max(sector_supp)))

    plt.figure(figsize=(10, 5))
    plt.imshow(
        sector_supp,
        extent=[phi_vals[0], phi_vals[-1], r_vals[0], r_vals[-1]],
        origin="lower",
        aspect="auto",
        vmin=0.0,
        vmax=vmax,
    )
    plt.colorbar(label=r"$1 - R_\Theta$")
    plt.xlabel(r"$\phi$")
    plt.ylabel(r"$r = a_2/a_1$")
    plt.title("Task 11A: Constrained narrow-sector suppression")
    plt.tight_layout()
    out = os.path.join(fig_dir, "task11A_constrained_sector_suppression.png")
    plt.savefig(out, dpi=220)
    plt.close()
    print(f"[Saved] {out}", flush=True)

    # Heatmap: total radiation ratio
    plt.figure(figsize=(10, 5))
    plt.imshow(
        Rff_grid,
        extent=[phi_vals[0], phi_vals[-1], r_vals[0], r_vals[-1]],
        origin="lower",
        aspect="auto",
    )
    plt.colorbar(label=r"$R_{\rm ff}=S_{\rm ff}/S_{\rm ff}^{\rm base}$")
    plt.xlabel(r"$\phi$")
    plt.ylabel(r"$r = a_2/a_1$")
    plt.title("Task 11A: Constrained total-radiation ratio")
    plt.tight_layout()
    out = os.path.join(fig_dir, "task11A_constrained_total_ratio.png")
    plt.savefig(out, dpi=220)
    plt.close()
    print(f"[Saved] {out}", flush=True)

    # Baseline map
    plt.figure(figsize=(10, 5))
    plt.imshow(I_base, extent=extent, origin="lower", aspect="auto")
    plt.colorbar(label=r"$I(\omega,\theta)$")
    plt.xlabel(r"$\omega$")
    plt.ylabel(r"$\theta$")
    plt.title("Task 11A: Constrained baseline map")
    plt.tight_layout()
    out = os.path.join(fig_dir, "task11A_constrained_baseline_map.png")
    plt.savefig(out, dpi=220)
    plt.close()
    print(f"[Saved] {out}", flush=True)

    # Best map
    plt.figure(figsize=(10, 5))
    plt.imshow(I_best, extent=extent, origin="lower", aspect="auto")
    plt.colorbar(label=r"$I(\omega,\theta)$")
    plt.xlabel(r"$\omega$")
    plt.ylabel(r"$\theta$")
    plt.title("Task 11A: Constrained best-candidate map")
    plt.tight_layout()
    out = os.path.join(fig_dir, "task11A_constrained_best_candidate_map.png")
    plt.savefig(out, dpi=220)
    plt.close()
    print(f"[Saved] {out}", flush=True)

    # Angular profile comparison
    Ibase_profile = np.sum(I_base * w_omega_ff[None, :], axis=1)
    Ibest_profile = np.sum(I_best * w_omega_ff[None, :], axis=1)

    plt.figure(figsize=(8, 5))
    plt.plot(theta_grid, Ibase_profile, label="Baseline angular profile")
    plt.plot(theta_grid, Ibest_profile, label="Best constrained candidate")
    plt.axvspan(theta_lo, theta_hi, alpha=0.15, label="narrow sector")
    plt.xlabel(r"$\theta$")
    plt.ylabel("Finite-frequency angular intensity")
    plt.title("Task 11A: Constrained angular-profile comparison")
    plt.legend()
    plt.tight_layout()
    out = os.path.join(fig_dir, "task11A_constrained_sector_profile_comparison.png")
    plt.savefig(out, dpi=220)
    plt.close()
    print(f"[Saved] {out}", flush=True)

    # Trajectory comparison
    plt.figure(figsize=(10, 5))
    plt.plot(t_grid, z_base, label="Baseline sinusoid")
    plt.plot(t_grid, z_best, label="Best constrained candidate")
    plt.xlabel("t")
    plt.ylabel("z(t)")
    plt.title("Task 11A: Constrained trajectory comparison")
    plt.legend()
    plt.tight_layout()
    out = os.path.join(fig_dir, "task11A_constrained_trajectory_comparison.png")
    plt.savefig(out, dpi=220)
    plt.close()
    print(f"[Saved] {out}", flush=True)

    print("\nTask 11A complete.", flush=True)


if __name__ == "__main__":
    main()