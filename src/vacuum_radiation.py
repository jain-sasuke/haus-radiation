import numpy as np
from source_spectrum import compute_Jz_kw


def kz_on_vacuum_manifold(omega_grid: np.ndarray, theta: float, c: float = 1.0) -> np.ndarray:
    """
    For observation polar angle theta, compute k_z on the vacuum propagating manifold:

        k_z = (omega / c) cos(theta)

    Parameters
    ----------
    omega_grid : np.ndarray
        Frequency grid.
    theta : float
        Polar angle in radians.
    c : float
        Speed of light (normalized default c=1).

    Returns
    -------
    kz_grid : np.ndarray
        k_z values corresponding to each omega.
    """
    omega_grid = np.asarray(omega_grid, dtype=float)
    return (omega_grid / c) * np.cos(theta)


def structural_vacuum_intensity_for_z_motion(
    t: np.ndarray,
    z: np.ndarray,
    vz: np.ndarray,
    omega_grid: np.ndarray,
    theta_grid: np.ndarray,
    q: float = 1.0,
    c: float = 1.0,
    window: str = "hann",
    normalize: bool = True,
) -> np.ndarray:
    """
    Compute the first structural vacuum radiation observable for motion along z.

    For z-directed motion:
        J = J_z zhat

    On the vacuum propagating manifold:
        k_z = (omega/c) cos(theta)

    The transverse radiation observable is:
        I(omega, theta) ∝ sin^2(theta) * |J_z(k_z_rad, omega)|^2

    Parameters
    ----------
    t, z, vz : np.ndarray
        Time, position, velocity arrays for z-directed motion.
    omega_grid : np.ndarray
        Frequency grid, shape (Nw,).
    theta_grid : np.ndarray
        Polar angle grid in radians, shape (Nteta,).
    q : float
        Charge prefactor.
    c : float
        Speed of light.
    window : str
        Time window type passed to source_spectrum.
    normalize : bool
        Whether to normalize the source-spectrum integral by window weight.

    Returns
    -------
    I : np.ndarray
        Array of shape (Ntheta, Nw), the structural radiation observable.
    """
    omega_grid = np.asarray(omega_grid, dtype=float)
    theta_grid = np.asarray(theta_grid, dtype=float)

    I = np.zeros((len(theta_grid), len(omega_grid)), dtype=float)

    for i, theta in enumerate(theta_grid):
        kz_grid = kz_on_vacuum_manifold(omega_grid, theta=theta, c=c)

        # Need J_z(kz(omega), omega), one diagonal element per omega.
        # compute_Jz_kw returns a matrix over (Nk, Nw). Here Nk == Nw.
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

        # Extract diagonal because row i corresponds to kz_grid[i],
        # and column i corresponds to omega_grid[i].
        J_diag = np.diag(J_matrix)

        I[i, :] = (np.sin(theta) ** 2) * (np.abs(J_diag) ** 2)

    return I