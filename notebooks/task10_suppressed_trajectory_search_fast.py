import os
import sys
import heapq
import numpy as np
import matplotlib.pyplot as plt

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_PATH = os.path.join(PROJECT_ROOT, "src")
if SRC_PATH not in sys.path:
    sys.path.append(SRC_PATH)

from vacuum_radiation import spectral_far_field_intensity_for_z_motion


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def trajectory_two_frequency(t, A1=1.0, omega1=1.0, A2=0.0, omega2=2.0, phi=0.0):
    z = A1 * np.sin(omega1 * t) + A2 * np.sin(omega2 * t + phi)
    vz = A1 * omega1 * np.cos(omega1 * t) + A2 * omega2 * np.cos(omega2 * t + phi)
    return z, vz


def finite_frequency_score(intensity_map, omega_grid, theta_grid, omega_cut):
    mask = np.abs(omega_grid) > omega_cut
    if not np.any(mask):
        raise ValueError("omega_cut removed all frequencies.")
    score_theta = np.trapezoid(intensity_map[:, mask], omega_grid[mask], axis=1)
    return float(np.trapezoid(score_theta, theta_grid))


def compute_score_only(t, z, vz, omega_grid, theta_grid, omega_cut):
    I = spectral_far_field_intensity_for_z_motion(
        t=t,
        z=z,
        vz=vz,
        omega_grid=omega_grid,
        theta_grid=theta_grid,
        q=1.0,
        c=1.0,
        window="hann",
        normalize=True,
    )
    return finite_frequency_score(I, omega_grid, theta_grid, omega_cut)


def compute_full_map(t, z, vz, omega_grid, theta_grid):
    return spectral_far_field_intensity_for_z_motion(
        t=t,
        z=z,
        vz=vz,
        omega_grid=omega_grid,
        theta_grid=theta_grid,
        q=1.0,
        c=1.0,
        window="hann",
        normalize=True,
    )


def main():
    fig_dir = os.path.join(PROJECT_ROOT, "figures")
    ensure_dir(fig_dir)

    # Keep scan reasonably light
    T = 60.0
    Nt = 1800
    t = np.linspace(-T / 2, T / 2, Nt)

    theta_grid = np.linspace(0.0, np.pi, 81)
    omega_grid = np.linspace(-5.0, 5.0, 161)
    omega_cut = 0.25

    A1 = 1.0
    omega1 = 1.0

    # Baseline score
    z_base, vz_base = trajectory_two_frequency(
        t=t, A1=A1, omega1=omega1, A2=0.0, omega2=2.0, phi=0.0
    )
    S_base = compute_score_only(t, z_base, vz_base, omega_grid, theta_grid, omega_cut)

    print("Task 10 fast baseline:")
    print(f"  S_ff(base) = {S_base:.6e}")

    # Coarse scan
    amp2_vals = np.linspace(0.0, 1.0, 9)
    ratio_list = [1.0, 2.0, 3.0]
    phi_vals = np.linspace(0.0, 2 * np.pi, 16, endpoint=False)

    best_heap = []  # keep smallest suppression values
    heatmaps = {}

    for ratio in ratio_list:
        omega2 = ratio * omega1
        suppression_grid = np.zeros((len(amp2_vals), len(phi_vals)))

        print(f"\nScanning omega2/omega1 = {ratio:.1f}")

        for i, A2 in enumerate(amp2_vals):
            for j, phi in enumerate(phi_vals):
                z, vz = trajectory_two_frequency(
                    t=t,
                    A1=A1,
                    omega1=omega1,
                    A2=A2,
                    omega2=omega2,
                    phi=phi,
                )

                S_ff = compute_score_only(t, z, vz, omega_grid, theta_grid, omega_cut)
                R = S_ff / S_base
                suppression_grid[i, j] = R

                item = (-R, {  # max heap trick for top smallest
                    "ratio": ratio,
                    "A2": float(A2),
                    "phi": float(phi),
                    "score": float(S_ff),
                    "suppression": float(R),
                })

                if len(best_heap) < 5:
                    heapq.heappush(best_heap, item)
                else:
                    if R < -best_heap[0][0]:
                        heapq.heapreplace(best_heap, item)

        heatmaps[ratio] = suppression_grid

        plt.figure(figsize=(10, 5))
        extent = [phi_vals[0], phi_vals[-1], amp2_vals[0], amp2_vals[-1]]
        plt.imshow(
            suppression_grid,
            extent=extent,
            origin="lower",
            aspect="auto",
        )
        plt.colorbar(label=r"$\mathcal{R}=S_{\rm ff}/S_{\rm ff}^{\rm base}$")
        plt.xlabel(r"$\phi$")
        plt.ylabel(r"$A_2$")
        plt.title(fr"Task 10 (fast): Suppression Heatmap for $\omega_2/\omega_1={ratio:.1f}$")
        plt.tight_layout()
        out = os.path.join(fig_dir, f"task10_fast_heatmap_ratio_{ratio:.1f}.png")
        plt.savefig(out, dpi=200)
        plt.close()
        print(f"[Saved] {out}")

    # Sort best cases properly
    top = sorted([x[1] for x in best_heap], key=lambda d: d["suppression"])

    print("\nTop 5 suppressed cases:")
    for k, case in enumerate(top, start=1):
        print(
            f"{k}. ratio={case['ratio']:.1f}, "
            f"A2={case['A2']:.3f}, "
            f"phi={case['phi']:.3f}, "
            f"S_ff={case['score']:.6e}, "
            f"R={case['suppression']:.6e}"
        )

    # Only now compute full maps for baseline and best case
    best = top[0]
    omega2_best = best["ratio"] * omega1

    z_best, vz_best = trajectory_two_frequency(
        t=t,
        A1=A1,
        omega1=omega1,
        A2=best["A2"],
        omega2=omega2_best,
        phi=best["phi"],
    )

    I_base = compute_full_map(t, z_base, vz_base, omega_grid, theta_grid)
    I_best = compute_full_map(t, z_best, vz_best, omega_grid, theta_grid)

    extent = [omega_grid[0], omega_grid[-1], theta_grid[0], theta_grid[-1]]

    plt.figure(figsize=(10, 5))
    plt.plot(t, z_base, label="Baseline sinusoid")
    plt.plot(t, z_best, label="Best suppressed candidate")
    plt.xlabel("t")
    plt.ylabel("z(t)")
    plt.title("Task 10 (fast): Trajectory Comparison")
    plt.legend()
    plt.tight_layout()
    out1 = os.path.join(fig_dir, "task10_fast_best_trajectory_vs_baseline.png")
    plt.savefig(out1, dpi=200)
    plt.close()
    print(f"[Saved] {out1}")

    plt.figure(figsize=(10, 5))
    plt.imshow(I_best, extent=extent, origin="lower", aspect="auto")
    plt.colorbar(label=r"$I(\omega,\theta)$")
    plt.xlabel(r"$\omega$")
    plt.ylabel(r"$\theta$")
    plt.title("Task 10 (fast): Best Suppressed Candidate Map")
    plt.tight_layout()
    out2 = os.path.join(fig_dir, "task10_fast_best_candidate_map.png")
    plt.savefig(out2, dpi=200)
    plt.close()
    print(f"[Saved] {out2}")

    plt.figure(figsize=(10, 5))
    plt.imshow(I_base, extent=extent, origin="lower", aspect="auto")
    plt.colorbar(label=r"$I(\omega,\theta)$")
    plt.xlabel(r"$\omega$")
    plt.ylabel(r"$\theta$")
    plt.title("Task 10 (fast): Baseline Sinusoid Map")
    plt.tight_layout()
    out3 = os.path.join(fig_dir, "task10_fast_baseline_map.png")
    plt.savefig(out3, dpi=200)
    plt.close()
    print(f"[Saved] {out3}")

    print("\nTask 10 (fast) pass condition:")
    print("1. A nontrivial trajectory gives substantial suppression relative to baseline")
    print("2. The suppression is visible in both the scalar score and the map")
    print("3. The best candidate is physically interpretable and worth robustness testing")


if __name__ == "__main__":
    main()