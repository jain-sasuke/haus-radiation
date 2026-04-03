# Task 1.5 — Analytic harmonic validation for sinusoidal motion

## Goal

Validate the numerical sinusoidal source spectrum against the analytic harmonic structure implied by the Haus formulation.

This task still concerns the **source spectrum**, not yet the radiated field.

---

## Starting point

For 1D sinusoidal motion,

\[
z(t)=d\sin(\omega_0 t),
\qquad
v(t)=d\omega_0\cos(\omega_0 t),
\]

the source spectrum is

\[
J_z(k_z,\omega)=q\int dt\,d\omega_0\cos(\omega_0 t)\,e^{-ik_z d\sin(\omega_0 t)}e^{i\omega t}.
\]

Define

\[
a=k_z d.
\]

Then

\[
J_z(k_z,\omega)=q d\omega_0 \int dt\,\cos(\omega_0 t)\,e^{-ia\sin(\omega_0 t)}e^{i\omega t}.
\]

---

## Jacobi–Anger expansion

Use

\[
e^{-ia\sin(\omega_0 t)}=\sum_{m=-\infty}^{\infty} J_m(a)e^{-im\omega_0 t}.
\]

Also,

\[
\cos(\omega_0 t)=\frac{1}{2}\left(e^{i\omega_0 t}+e^{-i\omega_0 t}\right).
\]

So

\[
\cos(\omega_0 t)e^{-ia\sin(\omega_0 t)}
=
\frac{1}{2}\sum_{m=-\infty}^{\infty}
J_m(a)\left(
e^{-i(m-1)\omega_0 t}
+
e^{-i(m+1)\omega_0 t}
\right).
\]

Multiplying by \(e^{i\omega t}\) and integrating over time shows that the spectrum is concentrated at discrete harmonics

\[
\omega = n\omega_0.
\]

---

## Harmonic coefficient

Collecting terms at harmonic index \(n\), the coefficient is proportional to

\[
A_n(a)\propto J_{n+1}(a)+J_{n-1}(a).
\]

Using the Bessel recurrence,

\[
J_{n-1}(a)+J_{n+1}(a)=\frac{2n}{a}J_n(a),
\]

so equivalently

\[
A_n(a)\propto \frac{n}{a}J_n(a).
\]

These formulas determine the **relative harmonic weights** of the source spectrum.

---

## What should be tested numerically

For a chosen \(k_z\), \(d\), and \(\omega_0\):

1. Compute the numerical source spectrum \(J_z(k_z,\omega)\).
2. Sample the numerical magnitude at \(\omega=n\omega_0\).
3. Compute the analytic weights
   \[
   |A_n(a)| = \left|J_{n+1}(a)+J_{n-1}(a)\right|
   \]
   up to an arbitrary common normalization.
4. Compare the numerical and analytic relative harmonic heights.

---

## What counts as success

Task 1.5 is successful if:

- numerical harmonic locations occur at \(n\omega_0\),
- numerical relative peak heights follow the Bessel-weight trend,
- remaining differences are attributable to finite-time windowing and normalization.

---

## What this proves

This task upgrades the sinusoidal benchmark from a qualitative visual check to a physics-based analytic validation.

It still does **not** compute radiation.
It validates the oscillatory **source spectrum** before we move to propagating-mode restriction and transverse projection.