# Task 8.1 — Threshold-angle scan above threshold

## Goal

Strengthen the threshold-style medium benchmark by scanning several above-threshold velocities and checking whether the numerical peak angle follows the predicted law

\[
\theta_C(\beta)=\arccos\!\left(\frac{1}{n\beta}\right).
\]

This task upgrades Task 8 from a few examples to a genuine parameter-law validation.

---

## Physical basis

For constant-velocity motion in a nondispersive medium,

\[
z(t)=vt, \qquad \beta=\frac{v}{c},
\]

the Fourier source phase becomes

\[
e^{i\omega(1-n\beta\cos\theta)t}.
\]

Enhancement occurs when the phase mismatch is small:

\[
1-n\beta\cos\theta \approx 0.
\]

If \(n\beta>1\), the predicted angle is

\[
\theta_C=\arccos\!\left(\frac{1}{n\beta}\right).
\]

---

## What should be tested

Choose a set of above-threshold velocities, for example

\[
\beta = 0.68,\ 0.72,\ 0.76,\ 0.80,\ 0.85,\ 0.90
\]

for \(n=1.5\).

For each case:

1. compute the angle-dependent integrated nonzero-frequency strength
   \[
   S(\theta)=\int_{|\omega|>\omega_{\rm cut}} I(\omega,\theta)\,d\omega
   \]
2. extract the numerical peak angle \(\theta_{\rm peak}\),
3. compare it with the predicted \(\theta_C\).

---

## What should happen

- Near threshold, the peak will be broader and the angle error may be larger.
- Farther above threshold, the numerical peak should align more closely with \(\theta_C\).

So the most important trend is not “zero error everywhere,” but:

- the numerical peak angle should move monotonically with \(\beta\),
- and agreement should improve as the system moves away from threshold.

---

## What success means

Task 8.1 is successful if:

1. the numerical peak angle follows the predicted trend,
2. the predicted and numerical angle curves lie close together,
3. the error decreases for more clearly above-threshold cases.

This would show that the medium solver captures not just one threshold example, but the threshold-angle law itself.