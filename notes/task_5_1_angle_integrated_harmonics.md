# Task 5.1 — Angle-integrated dipole-limit harmonic benchmark

## Goal

Strengthen the dipole-limit benchmark by comparing harmonic strengths after angular integration, rather than only at the special slice $\theta=\pi/2$.

---

## Why Task 5 needed refinement

In Task 5, harmonic strengths were sampled at $\theta=\pi/2$. At that angle,

$$
k_z = \frac{\omega}{c}\cos\theta = 0,
$$

so the oscillatory phase factor simplifies strongly, and higher harmonics vanish almost exactly. That is correct, but it is a special geometric slice.

To test the dipole limit more generally, harmonic strengths should be compared using angle-integrated power-like quantities.

---

## Working observable

Using the upgraded spectral far-field observable,

$$
I_{\rm spec}(\omega,\theta)
\propto
\omega^2 \sin^2\theta
\left|
J_z\!\left(\frac{\omega}{c}\cos\theta,\omega\right)
\right|^2,
$$

define the angle-integrated harmonic strength

$$
S_n = \int_0^\pi I_{\rm spec}(n\omega_0,\theta)\,\sin\theta\,d\theta.
$$

The factor $\sin\theta$ is the axisymmetric solid-angle weight.

---

## Dipole-limit expectation

For small amplitude

$$
\frac{\omega_0 d}{c}\ll 1,
$$

the motion should reduce to a dipole source, so:

1. the fundamental $n=1$ should dominate,
2. higher harmonics $n\ge 2$ should be strongly suppressed,
3. the suppression should improve as $d$ is reduced.

---

## What should be tested

1. Compute the angular profile $I_{\rm spec}(n\omega_0,\theta)$ for $n=1,2,3,4$.
2. Integrate over angle to obtain $S_n$.
3. Normalize by the fundamental:
   $$
   \tilde S_n = S_n / S_1.
   $$
4. Confirm that $\tilde S_1 = 1$ and $\tilde S_{n\ge 2}\ll 1$.

---

## What success means

Task 5.1 is successful if:

- the angle-integrated fundamental dominates strongly,
- higher harmonics are suppressed by large factors,
- and the result supports the interpretation that the solver reduces to dipole radiation in the small-amplitude limit.

This closes the harmonic-suppression benchmark in a more general and defensible way than the $\theta=\pi/2$ slice alone.
