# Task 13 — Extended-source benchmark

## Goal

Move beyond single point trajectories and test whether simple spatially extended source configurations can produce stronger radiative suppression than any point-trajectory model.

The purpose of this task is not to jump immediately to a full atomic model. It is to test the deeper hypothesis:

> genuine suppression may require spatial structure, not just trajectory shaping of a single point source.

---

## Why this task is needed

The point-trajectory branch has shown:

- no convincing global suppression,
- real channel suppression through redistribution,
- modest but meaningful directional quieting under constraints,
- likely limits of simple 1D harmonic shaping.

Even 3D point motion may still inherit a fundamental limitation: the source is still spatially localized.

Many better-known weak-radiation or nonradiating constructions in electromagnetism involve:

- extended current distributions,
- multiple emitters,
- spatial phase cancellation,
- multipole balance,
- anapole-like mechanisms.

So if the point-source branch saturates, the correct next physics move is to explore extended sources.

---

## Core question

The main question of Task 13 is:

> does spatial extension provide suppression mechanisms that are not available to single point trajectories?

A secondary question is:

> can simple extended sources already outperform the best constrained point-trajectory results?

---

## Benchmark hierarchy

Task 13 should proceed in a controlled sequence.

### Stage 1 — two-point source benchmark

Start with the simplest extended configuration:
two point emitters with controlled relative phase and separation.

This is the smallest step beyond a single point source.

### Stage 2 — small ring / loop current toy model

Then move to a continuous or discretized ring-like source.

This introduces distributed spatial phase and possible loop-current cancellation effects.

### Stage 3 — richer distributed source patterns

Only if the earlier stages are promising, move to:
- source patches,
- toroidal-like distributions,
- multipole-balanced toy models.

---

## Stage 1: two-point source benchmark

Let two emitters be located at positions

$$
\mathbf r_1(t), \qquad \mathbf r_2(t),
$$

with relative phase or relative driving parameters.

The total source is then the coherent sum of contributions from both emitters.

The simplest test cases are:

1. identical motion, fixed spatial separation,
2. identical motion, opposite phase,
3. slightly different amplitudes or phase offsets.

This benchmark asks whether simple pairwise spatial interference can reduce radiation in selected channels.

---

## Stage 2: ring / loop benchmark

A ring-like current is the next natural step because it introduces angular circulation and distributed phase structure.

A first toy model can use a discretized set of $N$ equally spaced emitters on a ring, each with prescribed phase relation.

This already allows testing whether collective geometry suppresses dipole-like far-field radiation more effectively than single-particle motion.

---

## Primary observables

Use the same style of observables as before so the comparison remains fair.

### Directional detector-window score

For a chosen angular detector window,

$$
S_\Theta=\int_{\theta_1}^{\theta_2} d\theta \int_{|\omega|>\omega_{\rm cut}} I(\omega,\theta)\,d\omega.
$$

### Total finite-frequency score

$$
S_{\rm ff}=\int_0^\pi d\theta \int_{|\omega|>\omega_{\rm cut}} I(\omega,\theta)\,d\omega.
$$

### Optional band-limited score

If the source has strong harmonic structure, it is also useful to track

$$
S_1
$$

or another selected frequency-band score, as in Task 10A.

---

## What should be compared

The extended-source benchmark should be compared against:

1. the baseline single sinusoidal point source,
2. the best constrained 1D trajectory from Task 11A,
3. the best constrained 3D point trajectory, if Task 12 succeeds.

This will reveal whether spatial structure genuinely adds a new suppression mechanism.

---

## Constraint philosophy

Comparisons must remain fair.

Possible fairness conditions include fixing one of the following:

- total RMS source strength,
- total RMS velocity budget across all emitters,
- total kinetic or driving norm,
- total integrated source amplitude.

The exact choice depends on the source model, but some normalization must be imposed so that suppression is not obtained by simply weakening the whole source.

---

## What success means

Task 13 is successful if an extended-source configuration:

1. achieves lower $R_\Theta$ than the best point-source result,
2. does so with a competitive or improved $R_{\rm ff}$,
3. exhibits a clear spatial cancellation mechanism,
4. reveals a genuinely new physical effect rather than just another redistribution trick.

---

## What failure would mean

If even simple extended sources fail to improve the tradeoff, that would suggest the present benchmark observable or source class still misses the relevant physics.

That would not kill the project. It would simply mean the search must be pushed toward richer multipole or field-structured models.

---

## Connection to the larger goal

This is the first branch that begins to point, cautiously, toward the deeper intuition behind bound nonradiating structure.

A stationary hydrogen orbital is **not** being modeled here directly. But the extended-source branch is a more appropriate semiclassical direction than single point trajectories if one wants to understand how structured charge/current configurations can avoid radiating like naive classical orbits.

So Task 13 is not a claim about hydrogen quantization. It is a better structural bridge toward the idea that spatial organization of source motion matters fundamentally for radiation.