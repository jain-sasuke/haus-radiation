# Task 8 — Threshold-style medium behavior / Cherenkov logic

## Goal

Test whether the nondispersive-medium Fourier-domain solver shows the expected threshold-style onset for constant-velocity motion when \(n\beta\) crosses 1.

This is the first task where the medium extension is connected explicitly to Cherenkov-type kinematics.

---

## Physical setup

For constant velocity motion along z,

\[
z(t)=vt,
\qquad
\beta=\frac{v}{c}.
\]

In a homogeneous nondispersive medium,

\[
k_z=\frac{n\omega}{c}\cos\theta.
\]

The Fourier-domain source phase becomes

\[
e^{-ik_z z(t)}e^{i\omega t}
=
e^{i\omega(1-n\beta\cos\theta)t}.
\]

Thus the source integral is strongly enhanced when

\[
1-n\beta\cos\theta \approx 0.
\]

---

## Threshold condition

A real observation angle exists only if

\[
n\beta \ge 1.
\]

When \(n\beta>1\), the resonance angle is

\[
\cos\theta_C = \frac{1}{n\beta}.
\]

This is the usual Cherenkov-angle condition in a nondispersive medium.

---

## Working observable

Use the medium spectral observable already introduced:

\[
I_{\rm spec}^{(n)}(\omega,\theta)
\propto
\omega^2\sin^2\theta
\left|
J_z\!\left(\frac{n\omega}{c}\cos\theta,\omega\right)
\right|^2.
\]

To suppress trivial low-frequency contamination, define an angle-dependent integrated nonzero-frequency strength

\[
S(\theta)
=
\int_{|\omega|>\omega_{\rm cut}}
I_{\rm spec}^{(n)}(\omega,\theta)\,d\omega.
\]

This is the main threshold diagnostic.

---

## What should happen

### Below threshold: \(n\beta<1\)
No real Cherenkov angle exists. The finite-frequency angular profile should not show a sharp threshold peak.

### Near threshold: \(n\beta\approx 1\)
The enhancement should move toward small angles and become sensitive to finite-window broadening.

### Above threshold: \(n\beta>1\)
A clear angular enhancement should appear near

\[
\theta_C = \arccos\!\left(\frac{1}{n\beta}\right).
\]

---

## What Task 8 should compute

1. Integrated nonzero-frequency angular strength \(S(\theta)\) for several values of \(\beta\).
2. Comparison of predicted \(\theta_C\) with numerical peak location when \(n\beta>1\).
3. One medium spectral map in the above-threshold regime for visual confirmation.

---

## What success means

Task 8 is successful if:

- below-threshold cases do not show a Cherenkov-like finite-frequency peak,
- above-threshold cases do show an angular peak,
- and the peak location is close to the predicted

\[
\theta_C = \arccos\!\left(\frac{1}{n\beta}\right).
\]

This would show that the Fourier-domain medium solver captures the correct threshold-style kinematic geometry.