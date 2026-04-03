# Task 7 — Nondispersive medium benchmark

## Goal

Extend the vacuum Fourier-domain radiation solver to the simplest homogeneous nondispersive medium with constant refractive index \(n\).

This is the first medium benchmark after the vacuum stage has been validated.

---

## Vacuum vs medium propagating manifold

In vacuum, propagating modes satisfy

\[
k=\omega/c.
\]

For observation direction \(\hat{\mathbf n}\), the radiation manifold is

\[
\mathbf k_{\rm vac} = \frac{\omega}{c}\hat{\mathbf n}.
\]

In a nondispersive medium with refractive index \(n\),

\[
k=\frac{n\omega}{c},
\]

so the propagating manifold becomes

\[
\mathbf k_{\rm med} = \frac{n\omega}{c}\hat{\mathbf n}.
\]

For z-directed motion and polar angle \(\theta\),

\[
k_z = \frac{n\omega}{c}\cos\theta.
\]

---

## Working spectral observable in the medium

The same far-field spectral construction gives

\[
I_{\rm spec}^{(n)}(\omega,\theta)
\propto
\omega^2 \sin^2\theta
\left|
J_z\!\left(\frac{n\omega}{c}\cos\theta,\omega\right)
\right|^2.
\]

This differs from the vacuum case only through the replacement

\[
\frac{\omega}{c}\cos\theta
\;\to\;
\frac{n\omega}{c}\cos\theta.
\]

---

## What should change physically

Relative to vacuum:

1. the angular profiles can shift because the source is sampled at different \(k_z\),
2. harmonic intensities can be redistributed,
3. the vacuum and medium maps should agree continuously as \(n\to 1\).

At this stage we are not yet imposing or analyzing Cherenkov threshold logic in detail. We are only building the medium version of the solver and checking that it behaves sensibly.

---

## What Task 7 should compute

1. Vacuum spectral map for a benchmark trajectory.
2. Medium spectral map for the same trajectory.
3. A direct comparison of angular profiles at selected harmonics.
4. A continuity test showing that the medium result approaches the vacuum result as \(n\to 1\).

---

## What success means

Task 7 is successful if:

- the medium observable is implemented consistently,
- the medium and vacuum results differ in structured, physically sensible ways,
- and the medium result approaches the vacuum result as \(n\to 1\).

This prepares the next task, which will examine threshold-like medium behavior more explicitly.