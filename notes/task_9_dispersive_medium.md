# Task 9 — Dispersive medium benchmark

## Goal

Extend the nondispersive-medium benchmark to a simple dispersive medium with frequency-dependent refractive index $n(\omega)$.

The main question is:

> How does the threshold-style angular enhancement deform when the medium is dispersive?

---

## Physical basis

In the nondispersive case, the phase mismatch is

$$
1 - n\beta\cos\theta.
$$

In a dispersive medium, this becomes

$$
1 - n(\omega)\beta\cos\theta.
$$

So the preferred angle can depend on frequency:

$$
\cos\theta_C(\omega)=\frac{1}{n(\omega)\beta},
$$

whenever the right-hand side is physically allowed.

This means the simple nondispersive threshold picture may deform into a frequency-dependent angular ridge.

---

## Strategy

Use a simple toy dispersion law, for example

$$
n(\omega)=n_0+\frac{a}{1+(\omega/\omega_s)^2}.
$$

This is not meant to model a specific real material precisely. It is a controlled benchmark to test whether the solver behaves sensibly once the refractive index depends on frequency.

---

## What to compute

For one fixed super-threshold velocity $\beta$, compare:

- vacuum,
- nondispersive medium with constant $n=n_0$,
- dispersive medium with $n(\omega)$.

Make:

1. a spectral map $I(\omega,\theta)$ for the dispersive case,
2. a comparison map between nondispersive and dispersive cases,
3. an off-axis spectrum at one fixed angle,
4. an overlay of the predicted angle band $\theta_C(\omega)$ on the dispersive map.

---

## What success means

Task 9 is successful if:

1. the dispersive result reduces smoothly toward the nondispersive result when dispersion is weak,
2. the angular enhancement deforms in a smooth and interpretable way,
3. the deformation is broadly consistent with the frequency-dependent phase-matching condition.

This would show that the framework is not limited to constant-$n$ media and can track frequency-dependent radiation geometry.