# Task 6.1 — Residual and robustness check for the time-domain reference benchmark

## Goal

Stress-test the apparent agreement between the Fourier-domain solver and the time-domain far-field reference.

The earlier comparison looked visually very clean. This task checks whether that agreement remains credible when examined through residuals, multiple off-axis angles, and a less trivial amplitude.

---

## Why this is needed

Overlayed normalized curves can look deceptively perfect, especially for simple symmetric trajectories.

To test whether the agreement is robust rather than cosmetic, we must inspect:
- profile residuals directly,
- angle dependence away from special slices,
- sensitivity to amplitude,
- and spectra without hiding all differences through separate normalization.

---

## What should be tested

### 1. Residual in the fundamental angular profile

For the normalized profiles at \(\omega=\omega_0\),

\[
\Delta(\theta)=P_{\rm solver}(\theta)-P_{\rm ref}(\theta).
\]

This reveals differences that are invisible in a simple overlay plot.

### 2. Off-axis spectral comparison at several angles

Use several fixed angles, for example:

\[
\theta=\pi/6,\quad \pi/4,\quad \pi/3.
\]

This avoids over-reliance on a single special geometry.

### 3. More than one amplitude

Compare at two nonrelativistic amplitudes:
- a moderate case with \(\omega_0 d/c = 0.3\),
- a harder case with \(\omega_0 d/c = 0.5\).

The larger amplitude should still be nonrelativistic, but it should expose more visible deviations from the strict dipole picture.

### 4. Jointly scaled spectra

When comparing fixed-angle spectra, do not always normalize each curve independently to 1. Also compare them using a common scale so that real amplitude redistribution remains visible.

---

## What success means

Task 6.1 is successful if:

- the residuals remain small and structured,
- off-axis spectra still agree on the dominant harmonic structure,
- differences grow in a sensible way as amplitude increases,
- and no unphysical asymmetry or instability appears.

This would show that the earlier excellent agreement was not just an artifact of an easy benchmark.