import os
import sys
import time
import numpy as np
import matplotlib.pyplot as plt

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_PATH = os.path.join(PROJECT_ROOT, "src")
if SRC_PATH not in sys.path:
    sys.path.append(SRC_PATH)

from jax_radiation import make_jax_grids, intensity_map_two_frequency_raw, trajectory_two_frequency_jax


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


def make_theta_sector_weights(theta_grid, theta_lo=1.0, theta_hi=2.1):
    w = trapz_weights_np(theta_grid)
    mask = ((theta_grid >= theta_lo) & (theta_grid <= theta_hi)).astype(float)
    return w * mask


def score_from_map(I_map, w_omega, w_theta):
    score_theta = np.sum(I_map * w_omega[None, :], axis=1)
    return float(np.sum(score_theta * w_theta))


def compute_map(grids, A2, ratio, phi, A1=1.0, omega1=1.0, c=1.0):
    return np.array(
        intensity_map_two_frequency_raw(
            A2=float(A2),
            ratio=float(ratio),
            phi=float(phi),
            t=grids["t"],
            theta_grid=grids["theta_grid"],
            omega_grid=grids["omega_grid"],
            w_t=grids["w_t"],
            A1=float(A1),
            omega1=float(omega1),
            c=float(c),
        )
    )


def main():
    print("Starting Task 10B JAX scan...", flush=True)

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

    omega_grid = np.array(grids["omega_grid"])
    theta_grid = np.array(grids["theta_grid"])
    t_grid = np.array(grids["t"])
    w_theta_full = np.array(grids["w_theta"])

    omega1 = 1.0
    omega_cut = 0.25
    theta_lo = 1.0
    theta_hi = 2.1

    w_omega_ff = make_ff_weights(omega_grid, omega_cut=omega_cut)
    w_theta_sector = make_theta_sector_weights(theta_grid, theta_lo=theta_lo, theta_hi=theta_hi)

    print("Computing baseline map...", flush=True)
    I_base = compute_map(grids, A2=0.0, ratio=2.0, phi=0.0, A1=1.0, omega1=omega1, c=1.0)
    Ssector_base = score_from_map(I_base, w_omega_ff, w_theta_sector)
    Sff_base = score_from_map(I_base, w_omega_ff, w_theta_full)

    print(f"Ssector(base) = {Ssector_base:.6e}", flush=True)
    print(f"Sff(base)     = {Sff_base:.6e}", flush=True)
    print(f"Angular window = [{theta_lo:.3f}, {theta_hi:.3f}] rad", flush=True)

    ratio_list = [2.0, 3.0]
    amp2_vals = np.linspace(0.0, 1.0, 9)
    phi_vals = np.linspace(0.0, 2 * np.pi, 24, endpoint=False)

    all_cases = []
    t0 = time.time()

    for ratio in ratio_list:
        print(f"Scanning ratio = {ratio:.1f} ...", flush=True)
        Rtheta_grid = np.zeros((len(amp2_vals), len(phi_vals)))
        Rff_grid = np.zeros((len(amp2_vals), len(phi_vals)))

        for i, A2 in enumerate(amp2_vals):
            for j, phi in enumerate(phi_vals):
                I = compute_map(grids, A2=A2, ratio=ratio, phi=phi, A1=1.0, omega1=omega1, c=1.0)

                Ssector = score_from_map(I, w_omega_ff, w_theta_sector)
                Sff = score_from_map(I, w_omega_ff, w_theta_full)

                Rtheta = Ssector / Ssector_base
                Rff = Sff / Sff_base

                Rtheta_grid[i, j] = Rtheta
                Rff_grid[i, j] = Rff

                all_cases.append({
                    "ratio": float(ratio),
                    "A2": float(A2),
                    "phi": float(phi),
                    "Ssector": float(Ssector),
                    "Sff": float(Sff),
                    "Rtheta": float(Rtheta),
                    "Rff": float(Rff),
                })

        extent = [phi_vals[0], phi_vals[-1], amp2_vals[0], amp2_vals[-1]]

        # sector suppression shown as 1 - Rtheta
        sector_supp = 1.0 - Rtheta_grid
        vmax = max(0.02, float(np.max(sector_supp)))

        plt.figure(figsize=(10, 5))
        plt.imshow(
            sector_supp,
            extent=extent,
            origin="lower",
            aspect="auto",
            vmin=0.0,
            vmax=vmax,
        )
        plt.colorbar(label=r"$1 - R_\Theta$")
        plt.xlabel(r"$\phi$")
        plt.ylabel(r"$A_2$")
        plt.title(fr"Task 10B: Angular-sector suppression for $\omega_2/\omega_1={ratio:.1f}$")
        plt.tight_layout()
        out = os.path.join(fig_dir, f"task10B_sector_suppression_ratio_{ratio:.1f}.png")
        plt.savefig(out, dpi=220)
        plt.close()
        print(f"[Saved] {out}", flush=True)

        plt.figure(figsize=(10, 5))
        plt.imshow(
            Rff_grid,
            extent=extent,
            origin="lower",
            aspect="auto",
        )
        plt.colorbar(label=r"$R_{\rm ff}=S_{\rm ff}/S_{\rm ff}^{\rm base}$")
        plt.xlabel(r"$\phi$")
        plt.ylabel(r"$A_2$")
        plt.title(fr"Task 10B: Total-radiation ratio for $\omega_2/\omega_1={ratio:.1f}$")
        plt.tight_layout()
        out = os.path.join(fig_dir, f"task10B_total_ratio_ratio_{ratio:.1f}.png")
        plt.savefig(out, dpi=220)
        plt.close()
        print(f"[Saved] {out}", flush=True)

    t1 = time.time()
    print(f"Total scan time: {t1 - t0:.2f} s", flush=True)

    all_cases = sorted(all_cases, key=lambda d: d["Rtheta"])
    top = all_cases[:10]

    print("\nTop 10 candidates by angular-sector suppression:", flush=True)
    for k, case in enumerate(top, start=1):
        print(
            f"{k}. ratio={case['ratio']:.1f}, "
            f"A2={case['A2']:.3f}, "
            f"phi={case['phi']:.3f}, "
            f"Ssector={case['Ssector']:.6e}, "
            f"Rtheta={case['Rtheta']:.6e}, "
            f"(1-Rtheta)={1.0 - case['Rtheta']:.6e}, "
            f"Sff={case['Sff']:.6e}, "
            f"Rff={case['Rff']:.6e}",
            flush=True
        )

    best = top[0]
    print("\nComputing best-candidate outputs...", flush=True)
    I_best = compute_map(grids, A2=best["A2"], ratio=best["ratio"], phi=best["phi"], A1=1.0, omega1=omega1, c=1.0)

    z_base, _ = trajectory_two_frequency_jax(grids["t"], 1.0, omega1, 0.0, 2.0, 0.0)
    z_best, _ = trajectory_two_frequency_jax(grids["t"], 1.0, omega1, best["A2"], best["ratio"], best["phi"])

    z_base = np.array(z_base)
    z_best = np.array(z_best)

    extent = [omega_grid[0], omega_grid[-1], theta_grid[0], theta_grid[-1]]

    plt.figure(figsize=(10, 5))
    plt.imshow(I_base, extent=extent, origin="lower", aspect="auto")
    plt.colorbar(label=r"$I(\omega,\theta)$")
    plt.xlabel(r"$\omega$")
    plt.ylabel(r"$\theta$")
    plt.title("Task 10B: Baseline map")
    plt.tight_layout()
    out = os.path.join(fig_dir, "task10B_baseline_map.png")
    plt.savefig(out, dpi=220)
    plt.close()
    print(f"[Saved] {out}", flush=True)

    plt.figure(figsize=(10, 5))
    plt.imshow(I_best, extent=extent, origin="lower", aspect="auto")
    plt.colorbar(label=r"$I(\omega,\theta)$")
    plt.xlabel(r"$\omega$")
    plt.ylabel(r"$\theta$")
    plt.title("Task 10B: Best candidate map")
    plt.tight_layout()
    out = os.path.join(fig_dir, "task10B_best_candidate_map.png")
    plt.savefig(out, dpi=220)
    plt.close()
    print(f"[Saved] {out}", flush=True)

    plt.figure(figsize=(10, 5))
    plt.plot(t_grid, z_base, label="Baseline sinusoid")
    plt.plot(t_grid, z_best, label="Best candidate")
    plt.xlabel("t")
    plt.ylabel("z(t)")
    plt.title("Task 10B: Trajectory comparison")
    plt.legend()
    plt.tight_layout()
    out = os.path.join(fig_dir, "task10B_trajectory_comparison.png")
    plt.savefig(out, dpi=220)
    plt.close()
    print(f"[Saved] {out}", flush=True)

    Ibase_sector = np.sum(I_base * w_omega_ff[None, :], axis=1)
    Ibest_sector = np.sum(I_best * w_omega_ff[None, :], axis=1)

    plt.figure(figsize=(8, 5))
    plt.plot(theta_grid, Ibase_sector, label="Baseline angular profile")
    plt.plot(theta_grid, Ibest_sector, label="Best candidate angular profile")
    plt.axvspan(theta_lo, theta_hi, alpha=0.15, label="sector")
    plt.xlabel(r"$\theta$")
    plt.ylabel("Finite-frequency angular intensity")
    plt.title("Task 10B: Angular-profile comparison")
    plt.legend()
    plt.tight_layout()
    out = os.path.join(fig_dir, "task10B_sector_profile_comparison.png")
    plt.savefig(out, dpi=220)
    plt.close()
    print(f"[Saved] {out}", flush=True)

    print("\nTask 10B complete.", flush=True)


if __name__ == "__main__":
    main()