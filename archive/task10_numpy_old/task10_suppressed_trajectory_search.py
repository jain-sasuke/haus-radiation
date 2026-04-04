import os
import sys
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


def normalized(arr):
    arr = np.asarray(arr, dtype=float)
    m = np.max(arr)
    if m <= 0:
        return arr.copy()
    return arr / m


def main():
    fig_dir = os.path.join(PROJECT_ROOT, "figures")
    ensure_dir(fig_dir)

    # Solver settings
    T = 80.0
    Nt = 2200
    t = np.linspace(-T / 2, T / 2, Nt)

    theta_grid = np.linspace(0.0, np.pi, 121)
    omega_grid = np.linspace(-6.0, 6.0, 241)
    omega_cut = 0.25

    # Baseline
    A1 = 1.0
    omega1 = 1.0

    z_base, vz_base = trajectory_two_frequency(
        t=t, A1=A1, omega1=omega1, A2=0.0, omega2=2.0, phi=0.0
    )

    I_base = spectral_far_field_intensity_for_z_motion(
        t=t,
        z=z_base,
        vz=vz_base,
        omega_grid=omega_grid,
        theta_grid=theta_grid,
        q=1.0,
        c=1.0,
        window="hann",
        normalize=True,
    )

    S_base = finite_frequency_score(I_base, omega_grid, theta_grid, omega_cut)

    print("Task 10 baseline:")
    print(f"  S_ff(base) = {S_base:.6e}")

    # Search space
    amp2_vals = np.linspace(0.0, 1.0, 11)
    ratio_list = [1.0, 2.0, 3.0]
    phi_vals = np.linspace(0.0, 2 * np.pi, 25, endpoint=False)

    best_cases = []

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

                S_ff = finite_frequency_score(I, omega_grid, theta_grid, omega_cut)
                R = S_ff / S_base
                suppression_grid[i, j] = R

                best_cases.append(
                    {
                        "ratio": ratio,
                        "A2": A2,
                        "phi": phi,
                        "score": S_ff,
                        "suppression": R,
                    }
                )

        # Heatmap for this ratio
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
        plt.title(fr"Task 10: Suppression Heatmap for $\omega_2/\omega_1={ratio:.1f}$")
        plt.tight_layout()
        out = os.path.join(fig_dir, f"task10_heatmap_ratio_{ratio:.1f}.png")
        plt.savefig(out, dpi=200)
        plt.close()
        print(f"[Saved] {out}")

    # Sort best cases
    best_cases = sorted(best_cases, key=lambda x: x["suppression"])
    top = best_cases[:5]

    print("\nTop 5 suppressed cases:")
    for k, case in enumerate(top, start=1):
        print(
            f"{k}. ratio={case['ratio']:.1f}, "
            f"A2={case['A2']:.3f}, "
            f"phi={case['phi']:.3f}, "
            f"S_ff={case['score']:.6e}, "
            f"R={case['suppression']:.6e}"
        )

    # Recompute best case for detailed plots
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

    I_best = spectral_far_field_intensity_for_z_motion(
        t=t,
        z=z_best,
        vz=vz_best,
        omega_grid=omega_grid,
        theta_grid=theta_grid,
        q=1.0,
        c=1.0,
        window="hann",
        normalize=True,
    )

    # Figure: baseline vs best trajectory
    plt.figure(figsize=(10, 5))
    plt.plot(t, z_base, label="Baseline sinusoid")
    plt.plot(t, z_best, label="Best suppressed candidate")
    plt.xlabel("t")
    plt.ylabel("z(t)")
    plt.title("Task 10: Trajectory Comparison")
    plt.legend()
    plt.tight_layout()
    out1 = os.path.join(fig_dir, "task10_best_trajectory_vs_baseline.png")
    plt.savefig(out1, dpi=200)
    plt.close()
    print(f"[Saved] {out1}")

    # Figure: best map
    plt.figure(figsize=(10, 5))
    extent = [omega_grid[0], omega_grid[-1], theta_grid[0], theta_grid[-1]]
    plt.imshow(I_best, extent=extent, origin="lower", aspect="auto")
    plt.colorbar(label=r"$I(\omega,\theta)$")
    plt.xlabel(r"$\omega$")
    plt.ylabel(r"$\theta$")
    plt.title("Task 10: Best Suppressed Candidate Map")
    plt.tight_layout()
    out2 = os.path.join(fig_dir, "task10_best_candidate_map.png")
    plt.savefig(out2, dpi=200)
    plt.close()
    print(f"[Saved] {out2}")

    # Figure: baseline map
    plt.figure(figsize=(10, 5))
    plt.imshow(I_base, extent=extent, origin="lower", aspect="auto")
    plt.colorbar(label=r"$I(\omega,\theta)$")
    plt.xlabel(r"$\omega$")
    plt.ylabel(r"$\theta$")
    plt.title("Task 10: Baseline Sinusoid Map")
    plt.tight_layout()
    out3 = os.path.join(fig_dir, "task10_baseline_map.png")
    plt.savefig(out3, dpi=200)
    plt.close()
    print(f"[Saved] {out3}")

    print("\nTask 10 pass condition:")
    print("1. A nontrivial trajectory gives substantial suppression relative to baseline")
    print("2. The suppression is visible in both the scalar score and the map")
    print("3. The best candidate is physically interpretable and worth robustness testing")


if __name__ == "__main__":
    main()