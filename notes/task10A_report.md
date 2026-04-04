# Task 10A Report — Band-Limited Suppression Search

## Aim

Test whether a simple nontrivial trajectory can reduce radiation in a chosen frequency band relative to the baseline sinusoid.

The old Task 10 asked for reduction of total finite-frequency radiation. That failed: the baseline sinusoid was always best. So Task 10A changed the question to a more realistic one:

**Can structured motion suppress radiation in the fundamental band, even if it radiates more elsewhere?**

---

## Trajectory family

We scanned

$$
z(t) = A_1 \sin(\omega_1 t) + A_2 \sin(\omega_2 t + \phi),
$$

with baseline

$$
z_{\text{base}}(t) = A_1 \sin(\omega_1 t).
$$

The scan used:

- $\omega_2 / \omega_1 = 2, 3$
- $A_2 \in [0,1]$
- $\phi \in [0,2\pi)$

---

## Scores used

### Primary score: radiation in the fundamental band

$$
S_1 = \int_0^\pi d\theta \int_{B_1} I(\omega,\theta)\, d\omega,
$$

with

$$
B_1 = \left\{ \omega : 0.8\omega_1 \le |\omega| \le 1.2\omega_1 \right\}.
$$

Reported as the ratio

$$
R_1 = \frac{S_1}{S_1^{\rm base}}.
$$

### Secondary score: total finite-frequency radiation

$$
S_{\rm ff} = \int_0^\pi d\theta \int_{|\omega| > \omega_{\rm cut}} I(\omega,\theta)\, d\omega,
$$

reported as

$$
R_{\rm ff} = \frac{S_{\rm ff}}{S_{\rm ff}^{\rm base}}.
$$

This second score tells us whether the effect is true suppression or just redistribution.

---

## Baseline values

From the run:

- $S_1^{\rm base} = 1.046267 \times 10^2$
- $S_{\rm ff}^{\rm base} = 3.828664 \times 10^2$

---

## Main result

Best candidate found:

- $\omega_2 / \omega_1 = 3$
- $A_2 = 1.0$
- $\phi \approx \pi$

Numerical values:

- $S_1 = 8.821783 \times 10^1$
- $R_1 = 0.8431674$
- $S_{\rm ff} = 7.568712 \times 10^3$
- $R_{\rm ff} = 19.76855$

---

## Interpretation

This means:

$$
1 - 0.843 \approx 0.157,
$$

so the radiation in the chosen fundamental band is reduced by about **16%**.

But at the same time, the total finite-frequency radiation becomes about **20 times larger** than the baseline.

So the effect is **not** overall suppression.

It is **spectral redistribution**:

- less radiation near the fundamental,
- much more radiation at other frequencies.

---

## Figure-based reading

### 1. Fundamental-band suppression heatmaps

For $\omega_2/\omega_1 = 2$, suppression is weak and almost phase-independent.

For $\omega_2/\omega_1 = 3$, suppression is real and strongest near $A_2 \to 1$ and $\phi \approx \pi$.

This shows that the third harmonic is much more effective than the second harmonic for reshaping the spectrum near the fundamental.

### 2. Total-radiation heatmaps

Both ratio-2 and ratio-3 cases show strong growth in total radiation with increasing $A_2$.

So the band suppression is achieved by making the motion much more radiative elsewhere.

### 3. Baseline vs. best-candidate maps

The best candidate map is much stronger overall, but weaker in the selected fundamental band. This agrees with the scalar metrics.

### 4. Band-profile comparison

The best candidate band-integrated angular profile lies below the baseline over much of the angular range, so the reduction is genuine and not confined to one tiny angle.

### 5. Trajectory comparison

The best candidate waveform is much more structured than the baseline sinusoid. That richer waveform feeds stronger higher-frequency radiation.

---

## Physics verdict

Task 10A is a success, but only in the following sense:

**Nontrivial structured motion can suppress radiation in a selected frequency band.**

Task 10A is **not** evidence for:

- radiationless motion,
- overall radiation suppression,
- hydrogen-like stationary motion,
- orbit without radiation.

The correct conclusion is:

> The best scanned two-frequency trajectories show modest suppression in the fundamental band, but this comes from redistribution into other radiative channels, not from becoming globally quieter.

---

## Harsh conclusion

Old Task 10 failed as a search for overall suppression.

Task 10A succeeded as a search for channel suppression.

The mechanism is **redistribution**, not disappearance of radiation.

That is a real result and worth keeping.