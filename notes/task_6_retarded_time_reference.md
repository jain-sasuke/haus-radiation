# Task 6 — Nonrelativistic retarded-time far-field benchmark

## Goal

Compare the Fourier-domain radiation solver against a standard nonrelativistic time-domain far-field reference for z-directed oscillatory motion.

This is the first direct comparison against an external radiation construction, rather than only internal checks or asymptotic dipole-limit expectations.

---

## Physical setup

For nonrelativistic motion along the z-axis,

$$
\mathbf r_0(t)=z(t)\hat z,
$$

the far-field electric field in the observation direction $\hat{\mathbf n}$ is proportional to the transverse part of the acceleration evaluated at retarded time.

For polar angle $\theta$,

$$
E_{\rm far}(t,\theta)\propto \sin\theta\,\ddot z(t_r),
\qquad
t_r=t-\frac{R}{c}.
$$

The retarded-time shift changes only the phase in frequency space, so for spectral-shape comparisons one may use the simpler reference signal

$$
E_{\rm ref}(t,\theta)\propto \sin\theta\,\ddot z(t).
$$

---

## Reference spectral observable

Define the time-domain reference spectrum by Fourier transforming the far-field signal:

$$
\tilde E_{\rm ref}(\omega,\theta)=\int dt\,E_{\rm ref}(t,\theta)e^{i\omega t}.
$$

Then define the reference spectral intensity

$$
I_{\rm ref}(\omega,\theta)\propto |\tilde E_{\rm ref}(\omega,\theta)|^2.
$$

This should be compared against the Fourier-domain solver observable

$$
I_{\rm spec}(\omega,\theta)
\propto
\omega^2\sin^2\theta
\left|
J_z\!\left(\frac{\omega}{c}\cos\theta,\omega\right)
\right|^2.
$$

---

## What should agree

For the same trajectory and in the nonrelativistic regime, the two approaches should agree on:

1. harmonic locations,
2. angular symmetry,
3. on-axis suppression,
4. dominant harmonic structure,
5. relative angular profile shape at the fundamental.

Absolute normalization need not match, because the project solver currently omits some overall constants and geometric prefactors.

---

## Benchmark trajectory

Use sinusoidal motion

$$
z(t)=d\sin(\omega_0 t),
\qquad
\ddot z(t)=-d\omega_0^2\sin(\omega_0 t).
$$

This trajectory gives a clean comparison between:
- Fourier-domain source-based radiation,
- and time-domain acceleration-based far-field radiation.

---

## What Task 6 should compute

1. The Fourier-domain solver spectral map $I_{\rm spec}(\omega,\theta)$.
2. The time-domain reference spectral map $I_{\rm ref}(\omega,\theta)$.
3. A comparison at selected angles.
4. A comparison of the angular profile at the fundamental frequency.

---

## What success means

Task 6 is successful if:

- the reference and solver agree on the main harmonic structure,
- the fundamental angular profiles match closely after normalization,
- on-axis suppression and symmetry agree,
- and remaining differences are attributable mainly to normalization and finite-window effects.

This would show that the solver agrees with a standard nonrelativistic far-field construction, not just with its own internal logic.
