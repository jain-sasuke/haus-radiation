# Task 10 — Search for radiation-suppressed trajectories

## Goal

Search for a simple nontrivial trajectory family whose finite-frequency radiation is strongly suppressed relative to a standard oscillatory baseline.

This task does **not** aim to prove exact nonradiation. The goal is to identify trajectories that are unusually weakly radiative in the present Fourier-domain benchmark observable.

---

## Physical idea

In the Haus-style source formulation, radiation depends on how the source spectrum overlaps the propagating manifold.

So the natural question is:

> Can a structured trajectory reshape its source spectrum so that the overlap with radiative channels becomes unusually small?

This is the guiding idea of Task 10.

---

## Trajectory family

Use a two-frequency trajectory:

$$
z(t)=A_1\sin(\omega_1 t)+A_2\sin(\omega_2 t+\phi).
$$

This is the first nontrivial search family because it is still simple, but has enough structure to allow interference and partial cancellation.

The baseline comparison is the ordinary single-frequency sinusoid:

$$
z_{\rm base}(t)=A_1\sin(\omega_1 t).
$$

---

## Suppression score

For each trajectory, define the finite-frequency radiation score

$$
S_{\rm ff}=\int d\theta \int_{|\omega|>\omega_{\rm cut}} I(\omega,\theta)\, d\omega.
$$

This is the main suppression metric.

A smaller value of $S_{\rm ff}$ means weaker finite-frequency radiation in the benchmark observable.

To compare with the baseline, define the suppression factor

$$
\mathcal{R}=\frac{S_{\rm ff}}{S_{\rm ff}^{\rm base}}.
$$

Values $\mathcal{R}\ll 1$ indicate strong suppression relative to the baseline sinusoid.

---

## Parameters to scan

A practical first scan is:

- fix $A_1=1$
- scan $A_2 \in [0,1]$
- scan frequency ratio $\omega_2/\omega_1 \in \{1,2,3\}$
- scan phase $\phi \in [0,2\pi)$

This is enough to search for suppression pockets without making the computation too expensive.

---

## What should be tested

1. Compute $S_{\rm ff}$ over the parameter grid.
2. Compare each result to the single-sinusoid baseline.
3. Identify the best-suppressed candidates.
4. Check whether the best candidate remains suppressed under small perturbations.

---

## What success means

Task 10 is successful if:

1. at least one nontrivial parameter region gives substantial suppression relative to the baseline,
2. the suppression is visible in both the scalar score and the radiation map,
3. the best candidate survives small parameter perturbations.

This would give the project its first real radiation-suppressed trajectory result.