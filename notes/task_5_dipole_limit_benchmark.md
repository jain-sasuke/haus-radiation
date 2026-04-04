# Task 5 — Dipole-limit benchmark for small-amplitude oscillation

## Goal

Validate the Fourier-domain spectral far-field observable against the standard dipole-radiation limit for small-amplitude sinusoidal motion.

This is the first external physics benchmark beyond internal consistency checks.

---

## Physical regime

Consider the sinusoidal trajectory

$$
z(t)=d\sin(\omega_0 t).
$$

In the small-amplitude regime

$$
\frac{\omega_0 d}{c}\ll 1,
$$

the source behaves like an oscillating electric dipole oriented along $z$.

This is the long-wavelength / dipole approximation.

---

## Standard dipole prediction

For a dipole moment

$$
p_z(t)=q z(t)=q d\sin(\omega_0 t),
$$

the far-field radiation in vacuum is determined by the second time derivative:

$$
\ddot p_z(t)= - q d \omega_0^2 \sin(\omega_0 t).
$$

Therefore:

1. radiation occurs only at the fundamental frequency $\omega_0$,
2. higher harmonics should be absent in the strict dipole limit,
3. the angular intensity should satisfy

$$
I(\theta)\propto \sin^2\theta.
$$

---

## What the Fourier-domain solver should do in this limit

Using the upgraded spectral observable

$$
I_{\rm spec}(\omega,\theta)
\propto
\omega^2 \sin^2\theta
\left|
J_z\!\left(\frac{\omega}{c}\cos\theta,\omega\right)
\right|^2,
$$

the small-amplitude oscillatory case should satisfy:

- strong signal at $\omega=\omega_0$,
- strong suppression of $\omega=2\omega_0,3\omega_0,\ldots$,
- angular profile at $\omega_0$ close to $\sin^2\theta$.

---

## What should be tested numerically

Choose a small amplitude $d$ such that

$$
a=\frac{\omega_0 d}{c}\ll 1.
$$

Then test:

1. harmonic content:
   - compare the first few harmonic strengths,
   - confirm that the fundamental dominates,

2. angular shape at the fundamental:
   - compare the numerical profile at $\omega_0$ against $\sin^2\theta$,

3. symmetry:
   - confirm the profile remains symmetric under $\theta\to\pi-\theta$.

---

## What success means

Task 5 is successful if:

- the fundamental dominates strongly over higher harmonics,
- the angular profile at $\omega_0$ matches $\sin^2\theta$ closely after normalization,
- deviations are small and decrease as $d$ is reduced.

This would show that the Fourier-domain solver correctly reduces to the standard dipole-radiation limit.
