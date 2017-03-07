---
layout: post
title: Calibrating Energy-Based Generative Adversarial Networks
author: Jiaming Song
tags:
- reading
---

## Calibrating Energy-Based Generative Adversarial Networks

### Optimization Dynamics Near Convergence of GANs

When the generator dstribution matches the data distribution, the training signal w.r.t. the discriminator vanishes, which pushes the generator that appears more real to the discriminator. Hence, the generator distribution will diverge from the data distrubution. In order to keep generator stationary as the data distribution, the discriminator must assign exactly same (flat) density to all samples at the optimal.

To tackle this problem, one needs to consider providing an additional training signal to the generator, such that the additional signal can

1. Balance the discriminator at optimum.
2. Cooperate with the discriminator to ensure the generator converges to the data distribution

### A New Formulation of GAN

The following adversarial learning formulation is proposed:

$$

\max_c \min_{p_g \sim \mathcal{P}} \mathbb{E}_{x\sim p_g}[c(x)] - \mathbb{E}_{x\sim p_d}[c(x)] + K(p_g)

$$

Define $$L(p_g, c) = \mathbb{E}_{x\sim p_g}[c(x)] - \mathbb{E}_{x\sim p_d}[c(x)] + K(p_g)$$, then $$L(p_g, c)$$ is the Lagrange dual function of the following optimization problem:

$$

\begin{array}\\
\min_{p_g \in \mathcal{P}} & K(p_g) \\
\mathrm{s.t.} & p_g(x) - p_d(x) = 0, \forall x \in \mathcal{X}
\end{array}

$$

We add the contraints for $$p_g(x)$$, and then by the KKT conditions, the optimal generator distribution $$p_g^*$$ matches the true data distribution, and the discriminator has the following form:

$$

c^*(x) = -\frac{\partial K(p_g)}{\partial x} \lvert _{p_g = p_d} - \lambda^* + \mu^*(x), \forall x \in \mathcal{X}

$$

where $$\mu^*(x)$$ is zero when $$p_d(x) > 0$$ and $$u_x$$ otherwise. This is called the *weak support discriminator*, which provides all the discrimination information in the original GAN formulation.

### Forms of $$K(p_g)$$

There are several forms of $$K(p_g)$$.

1. Entropy $$-H(p_g)$$
2. $$\ell_2$$ regularization on $$p_g$$
3. Constant
