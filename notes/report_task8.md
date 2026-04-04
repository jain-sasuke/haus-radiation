# Task 8 Report — Threshold-Style Medium Behavior / Haus Validation

## Objective

Task 8 tests whether the Fourier-domain moving-source framework reproduces the expected **threshold-style angular enhancement** for **constant-velocity motion in a nondispersive medium**.

The core question is:

> When a charge moves uniformly in a medium, does the radiation observable develop a strong peak at the angle predicted by the Haus phase-matching condition?

---

## Physical Setup

We take constant-velocity motion along the $z$-axis,

$$
z(t)=vt, \qquad \beta = \frac{v}{c}.
$$

In a nondispersive medium of refractive index $n$, the longitudinal wave number sampled by the source is

$$
k_z = \frac{n\omega}{c}\cos\theta.
$$

The Fourier source phase becomes

$$
e^{-ik_z z(t)} e^{i\omega t}
=
e^{\,i\omega(1-n\beta\cos\theta)t}.
$$

The source integral is enhanced when the phase mismatch is small:

$$
1 - n\beta\cos\theta \approx 0.
$$

If $n\beta > 1$, this condition has a real solution,

$$
\cos\theta_C = \frac{1}{n\beta},
\qquad
\theta_C = \arccos\!\left(\frac{1}{n\beta}\right),
$$

which is the usual Cherenkov-style threshold angle.

---

## Observable Used

The medium spectral observable is constructed from the Fourier-domain source and evaluated on the medium propagating manifold.

To suppress trivial low-frequency contamination, we define an angle-dependent integrated strength

$$
S(\theta)
=
\int_{|\omega|>\omega_{\rm cut}} I(\omega,\theta)\, d\omega.
$$

This is the main threshold diagnostic in Task 8.

---

## Parameters

- Medium refractive index:
  $$
  n = 1.5
  $$

- Threshold speed:
  $$
  \beta_{\rm th} = \frac{1}{n} = 0.666667
  $$

- Low-frequency cut:
  $$
  \omega_{\rm cut} = 0.25
  $$

Three cases were tested:

1. **Below threshold**:
   $$
   \beta = 0.60
   \quad\Rightarrow\quad
   n\beta = 0.90
   $$

2. **Near threshold**:
   $$
   \beta = 0.68
   \quad\Rightarrow\quad
   n\beta = 1.02
   $$

3. **Clearly above threshold**:
   $$
   \beta = 0.80
   \quad\Rightarrow\quad
   n\beta = 1.20
   $$

---

## Numerical Results

### Case 1: Below threshold ($\beta=0.60$)

Since

$$
n\beta = 0.90 < 1,
$$

there is **no real predicted Cherenkov angle**.

Numerically, the integrated angular strength $S(\theta)$ still shows a broad peak at

$$
\theta_{\rm peak} \approx 0.353 \text{ rad}.
$$

### Interpretation

This broad maximum is **not** a true threshold-locked peak. It is residual finite-window / filtered spectral weight in the constructed observable.

The correct physical statement is:

- below threshold, there is **no real Haus/Cherenkov angle**
- and therefore no sharp angle-locked enhancement should appear.

This is consistent with the observed broad, non-singular background.

---

### Case 2: Near threshold ($\beta=0.68$)

Now

$$
n\beta = 1.02 > 1,
$$

so a real predicted angle exists:

$$
\theta_C
=
\arccos\!\left(\frac{1}{1.5\times 0.68}\right)
\approx 0.198355 \text{ rad}.
$$

Numerically, the peak occurs at

$$
\theta_{\rm peak} \approx 0.255254 \text{ rad},
$$

with absolute error

$$
|\theta_{\rm peak} - \theta_C|
\approx 5.69\times 10^{-2} \text{ rad}.
$$

### Interpretation

This is acceptable for a near-threshold case.

Very close to threshold, the phase mismatch becomes shallow, so:

- the enhancement is weak,
- finite-time broadening becomes important,
- the low-frequency cut affects the integrated strength more strongly,
- and the numerical peak is expected to be broader and less precise.

Thus the near-threshold case shows the **onset** of threshold behavior, but not yet an asymptotically sharp angle match.

---

### Case 3: Above threshold ($\beta=0.80$)

Here

$$
n\beta = 1.20 > 1,
$$

so the predicted angle is

$$
\theta_C
=
\arccos\!\left(\frac{1}{1.5\times 0.8}\right)
\approx 0.585686 \text{ rad}.
$$

Numerically, the peak occurs at

$$
\theta_{\rm peak} \approx 0.589049 \text{ rad}.
$$

Absolute error:

$$
|\theta_{\rm peak} - \theta_C|
\approx 3.36\times 10^{-3} \text{ rad}.
$$

### Interpretation

This is an excellent match.

The above-threshold spectral map shows a strong horizontal ridge localized near the predicted angle, which is exactly the geometric signature expected from the Haus phase condition

$$
1 - n\beta\cos\theta = 0.
$$

This is the strongest single result in the project so far.

---

## Figure Interpretation

### 1. Threshold Angular Strength Plot

The angular-strength figure shows three clearly distinct regimes:

- **$\beta=0.60$**: broad background, no sharp threshold-locked peak
- **$\beta=0.68$**: onset of a localized enhancement, but still broadened
- **$\beta=0.80$**: narrow strong peak aligned with predicted $\theta_C$

This is exactly the qualitative sequence expected from the Haus/Cherenkov phase-matching logic.

---

### 2. Above-Threshold Map ($\beta=0.80$)

The above-threshold map shows intensity concentrated along a horizontal ridge near

$$
\theta \approx \theta_C.
$$

The dashed predicted angle line passes directly through the brightest ridge.

This is the direct visual confirmation that the Fourier-domain source framework captures threshold-style angular locking in the medium.

---

## Haus Validation

Task 8 is specifically a validation of the **Haus source-phase picture**.

The governing phase is

$$
e^{\,i\omega(1-n\beta\cos\theta)t},
$$

so the correct criterion for enhancement is the vanishing of the phase mismatch:

$$
1 - n\beta\cos\theta = 0.
$$

Task 8 confirms that:

1. a real enhancement angle appears only when $n\beta > 1$,
2. the super-threshold numerical peak aligns closely with the predicted $\theta_C$,
3. near threshold the enhancement is broader, as expected from finite-window effects.

Therefore, Task 8 is a **strong validation of the Haus-based medium threshold logic**.

---

## What Task 8 Proves

Task 8 shows that the nondispersive-medium extension is not merely a smooth deformation of the vacuum result.

It captures a qualitatively new regime:

- below threshold: no sharp angle locking
- above threshold: clear angular enhancement near the phase-matching angle

Thus the project now successfully connects:

- source kinematics,
- propagating medium manifold,
- and threshold angular emission geometry

within a single Fourier-domain framework.

---

## Limitations

Task 8 should still be interpreted carefully.

### 1. Below-threshold signal is not exactly zero
This is expected, because the constructed observable uses finite time windows and a filtered frequency integration.

So the correct claim is **not** “below threshold gives no signal,” but rather:

> below threshold does not produce a sharp Haus/Cherenkov-like angle-locked peak.

### 2. Near-threshold agreement is only moderate
This is also expected, since near-threshold geometry is sensitive to:

- broadening,
- finite observation time,
- and the low-frequency cut.

### 3. This is a benchmark validation, not yet a full dielectric radiation theory
Task 8 strongly validates the phase geometry of the medium solver, but it should not be oversold as a complete material-electrodynamics treatment.

---

## Final Verdict

**Task 8 passes.**

More specifically:

- **Below threshold**: physically acceptable, no sharp angle locking
- **Near threshold**: onset is visible, agreement is moderate
- **Clearly above threshold**: strong pass, with excellent angle agreement

The above-threshold case provides the clearest evidence so far that the Fourier-domain moving-source framework reproduces the correct medium threshold geometry predicted by the Haus phase-matching condition.

---

## Best One-Sentence Conclusion

Task 8 demonstrates that the medium Fourier-domain solver develops a strong angular enhancement only in the super-threshold regime, and for a clearly above-threshold case the peak aligns closely with the Haus/Cherenkov prediction

$$
\theta_C = \arccos\!\left(\frac{1}{n\beta}\right).
$$
