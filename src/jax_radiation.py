import numpy as np
import jax
import jax.numpy as jnp


def trapz_weights(x: np.ndarray) -> np.ndarray:
    """
    Trapezoidal integration weights for a 1D grid x.
    """
    x = np.asarray(x, dtype=float)
    if x.ndim != 1 or len(x) < 2:
        raise ValueError("x must be a 1D array with length >= 2")

    dx = np.diff(x)
    w = np.zeros_like(x)
    w[0] = dx[0] / 2.0
    w[-1] = dx[-1] / 2.0
    if len(x) > 2:
        w[1:-1] = 0.5 * (dx[:-1] + dx[1:])
    return w


def make_jax_grids(
    T: float = 60.0,
    Nt: int = 1200,
    theta_min: float = 0.0,
    theta_max: float = np.pi,
    Ntheta: int = 61,
    omega_min: float = -5.0,
    omega_max: float = 5.0,
    Nomega: int = 121,
    omega_cut: float = 0.25,
):
    """
    Build all fixed grids and quadrature weights once.
    """
    t = np.linspace(-T / 2.0, T / 2.0, Nt)
    theta_grid = np.linspace(theta_min, theta_max, Ntheta)
    omega_grid = np.linspace(omega_min, omega_max, Nomega)

    # Windowed time integration weights
    window = np.hanning(Nt)
    w_t = trapz_weights(t) * window

    # Finite-frequency integration weights
    w_omega = trapz_weights(omega_grid)
    ff_mask = (np.abs(omega_grid) > omega_cut).astype(float)
    w_omega_ff = w_omega * ff_mask

    # Angular integration weights
    w_theta = trapz_weights(theta_grid)

    return {
        "t": jnp.asarray(t),
        "theta_grid": jnp.asarray(theta_grid),
        "omega_grid": jnp.asarray(omega_grid),
        "w_t": jnp.asarray(w_t),
        "w_omega_ff": jnp.asarray(w_omega_ff),
        "w_theta": jnp.asarray(w_theta),
    }


@jax.jit
def trajectory_two_frequency_jax(
    t: jnp.ndarray,
    A1: float,
    omega1: float,
    A2: float,
    ratio: float,
    phi: float,
):
    """
    z(t) = A1 sin(omega1 t) + A2 sin(omega2 t + phi)
    with omega2 = ratio * omega1
    """
    omega2 = ratio * omega1
    z = A1 * jnp.sin(omega1 * t) + A2 * jnp.sin(omega2 * t + phi)
    vz = A1 * omega1 * jnp.cos(omega1 * t) + A2 * omega2 * jnp.cos(omega2 * t + phi)
    return z, vz


@jax.jit
def intensity_map_two_frequency_raw(
    A2: float,
    ratio: float,
    phi: float,
    t: jnp.ndarray,
    theta_grid: jnp.ndarray,
    omega_grid: jnp.ndarray,
    w_t: jnp.ndarray,
    A1: float = 1.0,
    omega1: float = 1.0,
    c: float = 1.0,
):
    """
    Raw (unnormalized) spectral map for z-directed motion in vacuum:
        I(omega, theta) ∝ omega^2 sin^2(theta) |J_z|^2

    This is the correct object for Task 10 score comparison.
    """
    z, vz = trajectory_two_frequency_jax(t, A1, omega1, A2, ratio, phi)

    def amps_for_theta(theta):
        # tau_theta(t) = t - cos(theta) z(t)/c
        tau = t - (jnp.cos(theta) / c) * z
        phase = jnp.exp(1j * omega_grid[:, None] * tau[None, :])
        amp = jnp.sum((vz * w_t)[None, :] * phase, axis=1)
        return amp

    amps = jax.vmap(amps_for_theta)(theta_grid)  # shape: (Ntheta, Nomega)

    intensity = (
        (omega_grid[None, :] ** 2)
        * (jnp.sin(theta_grid)[:, None] ** 2)
        * (jnp.abs(amps) ** 2)
    )
    return intensity


@jax.jit
def finite_frequency_score_two_frequency(
    A2: float,
    ratio: float,
    phi: float,
    t: jnp.ndarray,
    theta_grid: jnp.ndarray,
    omega_grid: jnp.ndarray,
    w_t: jnp.ndarray,
    w_omega_ff: jnp.ndarray,
    w_theta: jnp.ndarray,
    A1: float = 1.0,
    omega1: float = 1.0,
    c: float = 1.0,
):
    """
    Unnormalized finite-frequency score:
        S_ff = ∫ dtheta ∫_{|omega|>omega_cut} I(omega,theta) domega
    """
    intensity = intensity_map_two_frequency_raw(
        A2=A2,
        ratio=ratio,
        phi=phi,
        t=t,
        theta_grid=theta_grid,
        omega_grid=omega_grid,
        w_t=w_t,
        A1=A1,
        omega1=omega1,
        c=c,
    )

    score_theta = jnp.sum(intensity * w_omega_ff[None, :], axis=1)
    score = jnp.sum(score_theta * w_theta)
    return score


def build_score_function(grids, A1: float = 1.0, omega1: float = 1.0, c: float = 1.0):
    """
    Convenience wrapper that closes over the precomputed grids.
    """
    def score_fn(A2: float, ratio: float, phi: float):
        return finite_frequency_score_two_frequency(
            A2=A2,
            ratio=ratio,
            phi=phi,
            t=grids["t"],
            theta_grid=grids["theta_grid"],
            omega_grid=grids["omega_grid"],
            w_t=grids["w_t"],
            w_omega_ff=grids["w_omega_ff"],
            w_theta=grids["w_theta"],
            A1=A1,
            omega1=omega1,
            c=c,
        )

    return score_fn