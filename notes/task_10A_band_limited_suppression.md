# Task 10A — Band-limited suppression search

## Goal

Search for a simple nontrivial trajectory family that suppresses radiation in a **chosen frequency band** relative to a baseline sinusoid.

This task does **not** aim to eliminate all radiation. The goal is to test whether structured motion can reduce radiation in a selected channel while possibly redistributing it elsewhere.

---

## Why Task 10 was replaced

The original Task 10 used a fully integrated positive score over almost all finite-frequency radiation,

$$
S_{\rm ff}=\int d\theta \int_{|\omega|>\omega_{\rm cut}} I(\omega,\theta)\,d\omega.
$$

In the scanned two-frequency family, this score was minimized by the simplest baseline trajectory with no added second harmonic. This showed that the original score favored overall spectral simplicity and was not suitable for discovering nontrivial suppression.

So the problem has been reformulated.

---

## Physical idea of Task 10A

In the Haus-style source picture, radiation depends on how the source spectrum overlaps propagating channels.

A structured trajectory may not reduce radiation everywhere, but it may still **reduce radiation in a selected band** and move spectral weight elsewhere.

That is the question of Task 10A.

---

## Trajectory family

Use the two-frequency trajectory

$$
z(t)=A_1\sin(\omega_1 t)+A_2\sin(\omega_2 t+\phi),
$$

with baseline

$$
z_{\rm base}(t)=A_1\sin(\omega_1 t).
$$

The first scan focuses on

$$
\omega_2/\omega_1 \in \{2,3\}.
$$

---

## Primary score: fundamental-band radiation

Define a band around the fundamental frequency,

$$
\mathcal{B}_1=\{\omega:\ 0.8\omega_1 \le |\omega| \le 1.2\omega_1\}.
$$

Then define the band-limited score

$$
S_1=\int_0^\pi d\theta \int_{\omega\in\mathcal{B}_1} I(\omega,\theta)\,d\omega.
$$

This is the main suppression metric.

The corresponding suppression factor is

$$
\mathcal{R}_1=\frac{S_1}{S_1^{\rm base}}.
$$

Values $\mathcal{R}_1<1$ indicate suppression of radiation in the fundamental band relative to the baseline sinusoid.

---

## Secondary score: total finite-frequency radiation

To monitor redistribution, also compute

$$
S_{\rm ff}=\int_0^\pi d\theta \int_{|\omega|>\omega_{\rm cut}} I(\omega,\theta)\,d\omega.
$$

This is not the optimization target. It is a side diagnostic.

A candidate may reduce $S_1$ while increasing $S_{\rm ff}$, which would mean **redistribution rather than total suppression**.

---

## What success means

Task 10A is successful if:

1. a nontrivial trajectory gives $\mathcal{R}_1<1$,
2. the reduction is clearly visible in the radiation map,
3. the result is not just numerical noise,
4. the side diagnostic $S_{\rm ff}$ shows whether the effect is suppression or redistribution.

---

## What should be reported

For the best candidate, report:

- $(A_2,\omega_2/\omega_1,\phi)$,
- baseline and candidate values of $S_1$,
- baseline and candidate values of $S_{\rm ff}$,
- suppression factor $\mathcal{R}_1$,
- total-radiation ratio $S_{\rm ff}/S_{\rm ff}^{\rm base}$,
- baseline and candidate maps,
- baseline and candidate trajectories.

This gives a physically honest picture of what changed.