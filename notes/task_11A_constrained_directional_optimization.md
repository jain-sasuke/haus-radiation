# Task 11A — Constrained directional optimization

## Goal

Find the best 2-harmonic trajectory for suppressing radiation in a chosen narrow angular detector window, under a fair motion constraint.

The earlier scans showed that directional suppression is possible, but raw amplitude scans are not fully fair because different trajectories can have different overall kinematic strength.

Task 11A fixes this by normalizing all candidate trajectories to the same RMS velocity.

---

## Trajectory family

Use the 2-harmonic trajectory

$$
z(t)=a_1\sin(\omega t)+a_2\sin(2\omega t+\phi).
$$

Rather than scanning unconstrained amplitudes directly, each candidate is rescaled so that the RMS velocity satisfies a fixed target value,

$$
\sqrt{\langle v^2\rangle} = v_{\rm rms,target}.
$$

This makes all comparisons kinematically fair.

---

## Primary objective

Minimize radiation into the narrow detector window

$$
\Theta_{\rm win}=[0.55,\ 0.80]\ \text{rad}.
$$

Define

$$
S_\Theta=\int_{\theta_1}^{\theta_2} d\theta \int_{|\omega|>\omega_{\rm cut}} I(\omega,\theta)\,d\omega.
$$

This is the optimization target.

The suppression factor is

$$
R_\Theta=\frac{S_\Theta}{S_\Theta^{\rm base}},
$$

where the baseline is a single-frequency sinusoid with the same RMS velocity.

---

## Secondary diagnostic

Also compute total finite-frequency radiation

$$
S_{\rm ff}=\int_0^\pi d\theta \int_{|\omega|>\omega_{\rm cut}} I(\omega,\theta)\,d\omega.
$$

This determines whether the optimized result is only directional quieting through redistribution, or whether it also improves global radiative behavior.

---

## What success means

Task 11A is successful if:

1. a constrained nontrivial trajectory gives $R_\Theta<1$,
2. it improves upon the best raw-scan result from Task 10B narrow,
3. the result is robust under small changes in parameters,
4. the total-radiation diagnostic clarifies the redistribution cost.

---

## Why this is better than raw scans

Raw scans answer: "which scanned waveform looks best?"

Task 11A answers: "within a fair class of equally strong motions, which waveform is best for directional quieting?"

That is the physically stronger question.