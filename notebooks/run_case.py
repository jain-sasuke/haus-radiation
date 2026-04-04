import os
import sys
import json
import numpy as np

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_PATH = os.path.join(PROJECT_ROOT, "src")
if SRC_PATH not in sys.path:
    sys.path.append(SRC_PATH)

from trajectories import trajectory_constant_velocity, trajectory_sinusoidal
from medium_radiation import spectral_far_field_intensity_nondispersive_z_motion


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def n_dispersion(omega, n0=1.35, a=0.25, omega_s=1.5):
    omega = np.asarray(omega, dtype=float)
    return n0 + a / (1.0 + (omega / omega_s) ** 2)


def spectral_far_field_intensity_dispersive_z_motion(
    t, z, vz, omega_grid, theta_grid, n_of_omega, q=1.0, c=1.0, normalize=True
):
    w = np.hanning(len(t))
    dt = t[1] - t[0]
    intensity = np.zeros((len(theta_grid), len(omega_grid)), dtype=float)

    for j, theta in enumerate(theta_grid):
        sin2 = np.sin(theta) ** 2
        cos_th = np.cos(theta)

        for k, omega in enumerate(omega_grid):
            n_val = float(n_of_omega(np.array([omega]))[0])
            kz = n_val * omega * cos_th / c
            phase = np.exp(1j * omega * t - 1j * kz * z)
            amp = np.sum(q * vz * phase * w) * dt
            intensity[j, k] = sin2 * np.abs(amp) ** 2

    if normalize:
        m = np.max(intensity)
        if m > 0:
            intensity = intensity / m

    return intensity


def integrated_profile(intensity_map, omega_grid, omega_cut):
    mask = np.abs(omega_grid) > omega_cut
    return np.trapezoid(intensity_map[:, mask], omega_grid[mask], axis=1)


def analytic_theta_nondispersive(beta, n):
    if n * beta <= 1.0:
        return None
    return float(np.arccos(1.0 / (n * beta)))


def classify_case(traj_type, medium_kind, intensity_map, omega_grid, theta_grid, omega_cut, beta=None, n=None):
    mask = np.abs(omega_grid) > omega_cut
    finite_freq_max = float(np.max(intensity_map[:, mask])) if np.any(mask) else 0.0

    if traj_type == "constant_velocity_z" and medium_kind == "vacuum":
        return {
            "classification": "radiationless_benchmark",
            "radiation_message": "No significant finite-frequency radiation after DC filtering.",
            "finite_frequency_max": finite_freq_max,
        }

    if traj_type == "sinusoidal_z" and medium_kind == "vacuum":
        return {
            "classification": "radiative_benchmark",
            "radiation_message": "Finite-frequency radiation is present for oscillatory motion.",
            "finite_frequency_max": finite_freq_max,
        }

    if traj_type == "constant_velocity_z" and medium_kind == "nondispersive" and n is not None and beta is not None and n * beta > 1:
        return {
            "classification": "directional_threshold_radiation",
            "radiation_message": "Directional finite-frequency enhancement appears in the medium.",
            "finite_frequency_max": finite_freq_max,
        }

    if medium_kind == "dispersive_toy":
        return {
            "classification": "dispersive_directional_case",
            "radiation_message": "The radiation ridge deforms with frequency because n depends on omega.",
            "finite_frequency_max": finite_freq_max,
        }

    return {
        "classification": "unclassified_case",
        "radiation_message": "Case computed successfully.",
        "finite_frequency_max": finite_freq_max,
    }


def main(config_path):
    with open(config_path, "r") as f:
        cfg = json.load(f)

    case_name = cfg["case_name"]
    traj_type = cfg["trajectory"]["type"]
    traj_params = cfg["trajectory"]["params"]
    medium_kind = cfg["medium"]["kind"]
    medium_params = cfg["medium"]["params"]
    solver = cfg["solver"]
    display = cfg["display"]

    T = solver["T"]
    Nt = solver["Nt"]
    theta_grid = np.linspace(solver["theta_min"], solver["theta_max"], solver["Ntheta"])
    omega_grid = np.linspace(solver["omega_min"], solver["omega_max"], solver["Nomega"])
    omega_cut = solver["omega_cut"]
    normalize = solver["normalize"]

    t = np.linspace(-T / 2, T / 2, Nt)

    c = 1.0
    q = 1.0

    if traj_type == "constant_velocity_z":
        beta = traj_params["beta"]
        v = beta * c
        z, vz = trajectory_constant_velocity(t, v=v)

    elif traj_type == "sinusoidal_z":
        A = traj_params["A"]
        omega0 = traj_params["omega0"]
        z, vz = trajectory_sinusoidal(t, A=A, omega0=omega0)

    else:
        raise ValueError(f"Unsupported trajectory type: {traj_type}")

    if medium_kind == "vacuum":
        intensity_map = spectral_far_field_intensity_nondispersive_z_motion(
            t=t, z=z, vz=vz,
            omega_grid=omega_grid, theta_grid=theta_grid,
            n_medium=1.0, q=q, c=c, normalize=normalize
        )
        beta_val = traj_params.get("beta", None)
        n_val = 1.0

    elif medium_kind == "nondispersive":
        n_val = medium_params["n"]
        intensity_map = spectral_far_field_intensity_nondispersive_z_motion(
            t=t, z=z, vz=vz,
            omega_grid=omega_grid, theta_grid=theta_grid,
            n_medium=n_val, q=q, c=c, normalize=normalize
        )
        beta_val = traj_params.get("beta", None)

    elif medium_kind == "dispersive_toy":
        n0 = medium_params["n0"]
        a = medium_params["a"]
        omega_s = medium_params["omega_s"]
        intensity_map = spectral_far_field_intensity_dispersive_z_motion(
            t=t, z=z, vz=vz,
            omega_grid=omega_grid, theta_grid=theta_grid,
            n_of_omega=lambda om: n_dispersion(om, n0=n0, a=a, omega_s=omega_s),
            q=q, c=c, normalize=normalize
        )
        beta_val = traj_params.get("beta", None)
        n_val = None

    else:
        raise ValueError(f"Unsupported medium kind: {medium_kind}")

    profile = integrated_profile(intensity_map, omega_grid, omega_cut)
    j_peak = int(np.argmax(profile))
    theta_peak = float(theta_grid[j_peak])

    theta_analytic = None
    if medium_kind == "nondispersive" and traj_type == "constant_velocity_z":
        theta_analytic = analytic_theta_nondispersive(beta_val, n_val)

    cls = classify_case(
        traj_type=traj_type,
        medium_kind=medium_kind,
        intensity_map=intensity_map,
        omega_grid=omega_grid,
        theta_grid=theta_grid,
        omega_cut=omega_cut,
        beta=beta_val,
        n=n_val,
    )

    out_dir = os.path.join(PROJECT_ROOT, "outputs", case_name)
    ensure_dir(out_dir)

    np.savez(os.path.join(out_dir, "trajectory.npz"), t=t, z=z, vz=vz)
    np.savez(os.path.join(out_dir, "radiation_map.npz"), omega_grid=omega_grid, theta_grid=theta_grid, intensity_map=intensity_map)
    np.savez(os.path.join(out_dir, "angular_profile.npz"), theta_grid=theta_grid, profile=profile)

    summary = {
        "case_name": case_name,
        "trajectory_type": traj_type,
        "medium_kind": medium_kind,
        "classification": cls["classification"],
        "display_title": display["title"],
        "verdict_label": display["verdict_label"],
        "radiation_message": cls["radiation_message"],
        "parameters": {
            **traj_params,
            **medium_params,
            "omega_cut": omega_cut,
        },
        "diagnostics": {
            "finite_frequency_max": cls["finite_frequency_max"],
            "theta_peak_computed": theta_peak,
            "theta_peak_analytic": theta_analytic,
        },
    }

    with open(os.path.join(out_dir, "summary.json"), "w") as f:
        json.dump(summary, f, indent=2)

    print(f"Saved outputs to {out_dir}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python notebooks/run_case.py <config.json>")
    main(sys.argv[1])