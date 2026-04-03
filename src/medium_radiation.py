import numpy as np
from source_spectrum import compute_Jz_kw


def kz_on_nondispersive_manifold(
    omega_grid: np.ndarray,
    theta: float,
    n_medium: float,
    c: float = 1.0,
) -> np.ndarray:
    """
    For a homogeneous nondispersive medium with refractive index n_medium,

        k_z = (n_medium * omega / c) * cos(theta)

    Parameters
    ----------
    omega_grid : np.ndarray
        Frequency grid.
    theta : float
        Polar angle in radians.
    n_medium : float
        Refractive index of the medium.
    c : float
        Speed of light.

    Returns
    -------
    kz_grid : np.ndarray
        kz values on the medium propagating manifold.
    """
    omega_grid = np.asarray(omega_grid, dtype=float)
    return (n_medium * omega_grid / c) * np.cos(theta)


def spectral_far_field_intensity_nondispersive_z_motion(
    t: np.ndarray,
    z: np.ndarray,
    vz: np.ndarray,
    omega_grid: np.ndarray,
    theta_grid: np.ndarray,
    n_medium: float,
    q: float = 1.0,
    c: float = 1.0,
    window: str = "hann",
    normalize: bool = True,
) -> np.ndarray:
    """
    Medium analogue of the spectral far-field observable for z-directed motion.

    Working observable:
        I_spec^(n)(omega, theta) ∝ omega^2 sin^2(theta)
                                   |J_z((n*omega/c) cos(theta), omega)|^2

    This is a first medium extension benchmark. It should be interpreted as a
    spectral observable / proxy, not yet as a final fully normalized medium
    power formula.

    Parameters
    ----------
    t, z, vz : np.ndarray
        Time, position, velocity arrays for z-directed motion.
    omega_grid : np.ndarray
        Frequency grid.
    theta_grid : np.ndarray
        Polar angle grid in radians.
    n_medium : float
        Constant refractive index of the nondispersive medium.
    q : float
        Charge prefactor.
    c : float
        Speed of light.
    window : str
        Time window type passed to the source-spectrum evaluation.
    normalize : bool
        Whether to normalize the source integral by window weight.

    Returns
    -------
    I : np.ndarray
        Array of shape (Ntheta, Nomega).
    """
    omega_grid = np.asarray(omega_grid, dtype=float)
    theta_grid = np.asarray(theta_grid, dtype=float)

    I = np.zeros((len(theta_grid), len(omega_grid)), dtype=float)

    for i, theta in enumerate(theta_grid):
        kz_grid = kz_on_nondispersive_manifold(
            omega_grid=omega_grid,
            theta=theta,
            n_medium=n_medium,
            c=c,
        )

        J_matrix = compute_Jz_kw(
            t=t,
            z=z,
            vz=vz,
            kz_grid=kz_grid,
            omega_grid=omega_grid,
            q=q,
            window=window,
            normalize=normalize,
        )

        J_diag = np.diag(J_matrix)
        I[i, :] = (omega_grid ** 2) * (np.sin(theta) ** 2) * (np.abs(J_diag) ** 2)

    return I