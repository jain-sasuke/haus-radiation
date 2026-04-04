# Task 10B — Angular-sector suppression search

## Goal

Search for a simple nontrivial trajectory family that suppresses radiation into a chosen angular sector relative to a baseline sinusoid.

This task does **not** aim to suppress all radiation. The goal is to see whether structured motion can make the source quieter in a selected directional channel while possibly redistributing radiation elsewhere.

---

## Physical idea

In the Haus-style source picture, radiation is distributed across angular and spectral channels.

A trajectory may fail to reduce total radiation, but it may still reduce radiation seen in a detector window at selected angles. That is the question of Task 10B.

---

## Trajectory family

Use the same two-frequency trajectory as in Task 10A:

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

## Primary score: angular-sector radiation

Choose an angular window

$$
\Theta_{\rm win}=[\theta_1,\theta_2].
$$

Define the angular-sector score

$$
S_\Theta=\int_{\theta_1}^{\theta_2} d\theta \int_{|\omega|>\omega_{\rm cut}} I(\omega,\theta)\,d\omega.
$$

This is the main suppression metric.

The corresponding suppression factor is

$$
R_\Theta=\frac{S_\Theta}{S_\Theta^{\rm base}}.
$$

Values $R_\Theta<1$ indicate suppression of radiation in the chosen angular sector relative to the baseline sinusoid.

---

## Secondary score: total finite-frequency radiation

To monitor redistribution, also compute

$$
S_{\rm ff}=\int_0^\pi d\theta \int_{|\omega|>\omega_{\rm cut}} I(\omega,\theta)\,d\omega.
$$

This is only a side diagnostic.

A trajectory may reduce $S_\Theta$ while increasing $S_{\rm ff}$, which would mean directional quieting through redistribution rather than overall suppression.

---

## What success means

Task 10B is successful if:

1. a nontrivial trajectory gives $R_\Theta<1$,
2. the reduction is visible in the angular-sector profile or radiation map,
3. the result is not just numerical noise,
4. the side diagnostic $S_{\rm ff}$ shows whether the effect is local suppression or redistribution.

---

## What should be reported

For the best candidate, report:

- $(A_2,\omega_2/\omega_1,\phi)$,
- the chosen angular window $[\theta_1,\theta_2]$,
- baseline and candidate values of $S_\Theta$,
- baseline and candidate values of $S_{\rm ff}$,
- suppression factor $R_\Theta$,
- total-radiation ratio $S_{\rm ff}/S_{\rm ff}^{\rm base}$,
- baseline and candidate maps,
- baseline and candidate angular profiles.

This gives a physically honest directional-suppression result.