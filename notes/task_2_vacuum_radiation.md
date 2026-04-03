# Task 2 — First radiation observable in vacuum

## Goal

Move from the source-spectrum object

\[
\mathbf J(\mathbf k,\omega)
\]

to a first radiation-level observable in vacuum.

This is still a structural radiation calculation, not yet a fully normalized energy-flux formula.

---

## Physical idea

Haus’s Fourier-domain interpretation says that radiation is associated with those source Fourier components that match propagating electromagnetic modes.

In vacuum, propagating waves satisfy

\[
k=\omega/c.
\]

So for observation direction \(\hat{\mathbf n}\), the source must be evaluated on

\[
\mathbf k_{\rm rad}=\frac{\omega}{c}\hat{\mathbf n}.
\]

But not every component of the current contributes to radiation. The far-field radiation is transverse, so we must keep only the transverse part of the source:

\[
\mathbf J_\perp
=
\hat{\mathbf n}\times(\hat{\mathbf n}\times \mathbf J).
\]

---

## First numerical radiation observable

For this stage, define the structural vacuum radiation observable

\[
I(\omega,\hat{\mathbf n}) \propto |\mathbf J_\perp(\mathbf k_{\rm rad},\omega)|^2.
\]

This is enough to test the core physical distinction:

- constant velocity in vacuum should not radiate,
- oscillatory motion should radiate.

---

## Why the 1D benchmark is not enough for radiation

For Task 1, 1D motion along \(z\) was fine because we were only testing the source spectrum.

For radiation, however, if we keep the motion exactly collinear with the observation direction and only track \(J_z\), the transverse projection can become degenerate or misleading.

So for Task 2 we should use a simple 3D benchmark trajectory.

The cleanest choice is oscillatory motion along \(z\), but we observe at varying polar angle \(\theta\). Then

\[
\hat{\mathbf n}=(\sin\theta,0,\cos\theta).
\]

The source current is still along \(\hat z\), but the transverse projection is nonzero except along the axis.

---

## 3D source current for z-directed motion

For motion

\[
\mathbf r_0(t)=z(t)\hat z,
\qquad
\mathbf v(t)=v(t)\hat z,
\]

the vector source is

\[
\mathbf J(\mathbf k,\omega)=\hat z\,J_z(k_z,\omega),
\]

with

\[
k_z = \mathbf k\cdot\hat z.
\]

On the vacuum propagating manifold,

\[
\mathbf k = \frac{\omega}{c}\hat{\mathbf n},
\]

so

\[
k_z = \frac{\omega}{c}\cos\theta.
\]

Therefore, for z-directed motion, the radiation observable can be built from

\[
J_z\!\left(\frac{\omega}{c}\cos\theta,\omega\right).
\]

---

## Transverse projection for z-directed current

Let

\[
\mathbf J = J_z \hat z.
\]

Then

\[
\mathbf J_\perp
=
\hat{\mathbf n}\times(\hat{\mathbf n}\times \hat z\,J_z).
\]

Its magnitude is

\[
|\mathbf J_\perp| = |J_z|\,\sin\theta.
\]

So the first vacuum radiation observable becomes

\[
I(\omega,\theta)\propto \sin^2\theta\;
\left|
J_z\!\left(\frac{\omega}{c}\cos\theta,\omega\right)
\right|^2.
\]

This is the working formula for Task 2.

---

## Expected physics checks

### Constant velocity in vacuum

For uniform motion, the source support is on

\[
\omega = k_z v.
\]

But on the propagating manifold,

\[
k_z=\frac{\omega}{c}\cos\theta.
\]

So radiation would require

\[
\omega=\frac{\omega}{c}v\cos\theta.
\]

For subluminal motion \(v<c\), this cannot hold for ordinary nonzero \(\omega\), except trivially at zero frequency. Therefore the vacuum radiation observable should be negligible.

### Oscillatory motion in vacuum

The oscillatory source contains harmonics at

\[
\omega = n\omega_0,
\]

and those harmonics can contribute on the vacuum propagating manifold. The angular factor \(\sin^2\theta\) also implies:

- no radiation on axis (\(\theta=0,\pi\)),
- strongest radiation away from the axis.

---

## What Task 2 should produce

1. Vacuum radiation map \(I(\omega,\theta)\) for sinusoidal z-motion.
2. Vacuum radiation map \(I(\omega,\theta)\) for constant velocity.
3. A comparison plot showing:
   - constant velocity gives negligible signal,
   - oscillatory motion gives nonzero signal concentrated at harmonics and away from the axis.

---

## What success means

Task 2 is successful if:

- the constant-velocity vacuum radiation observable is negligible,
- the sinusoidal-motion vacuum radiation observable is nonzero,
- the oscillatory case vanishes on-axis because of the transverse factor,
- harmonic structure is visible in frequency.

This closes the first radiation-level step in vacuum.