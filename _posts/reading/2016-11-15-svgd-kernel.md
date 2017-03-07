---
layout: post
title: Learning to Draw Samples - With Application to Amortized MLE for Generative Adversarial Modeling
author: Jiaming Song
tags:
- reading
---

## Learning to Draw Samples: With Application to Amortized MLE for Generative Adversarial Modeling

### Stein Variational Gradient Descent

SVGD initalizes the particles by sampling from som simple distribution $$q_0$$ and updates the particles iteratively by

$$

x_i \leftarrow x_i + \epsilon \phi(x_i)

$$

$$\phi(x)$$ is a "particle gradient direction function" chosen to maximumly decrease the KL divergence between the distribution of particles and the target distribution.

$$

\phi = \arg \max_{\phi \in \mathcal{F}} \{- \frac{d}{d\epsilon} KL(q_\epsilon[\phi] \lVert p) \lvert _ {\epsilon=0} \}

$$

$$\mathcal{F}$$ is chosen as the unit ball of a vector-valued RKHS.

The Kernelized Stein discrepancy is:

$$

\mathbb{D}(q \lVert p) = \max_{\phi \in \mathcal{H}^D} \{ \mathbb{E}q[\mathcal{T}_p\phi(x)] \  \ \lvert  \ \ \lVert \phi \lVert_{\mathcal{H}^d} \leq 1 \}

$$

where $$\mathcal{T}_p \phi(x) = \nabla_x \log p(x)^\top \phi(x) + \nabla_x \phi(x)$$, and the optimal solution of this is

$$

\phi^*(x') \propto \mathbb{E}_{x \sim q}[\nabla_x \log p(x)k(x, x') + \nabla_x k(x, x')]

$$

By approximating the expectation under $$q$$ with the empirical average of the current particles, SVGD admits a sample form of update:

$$

x_i \leftarrow x_i + \epsilon \Delta x_i

$$

where $$\Delta x_i = \mathbb{E}_{x\in\{x_i\}_{i=1}^n}[\nabla_x \log p(x) k(x, x_i) + \nabla_x k(x, x_i)]$$

The first term drives the particles toward high probability regions, and the second term serve as a repulsive force to encourage diversity.

Notice when $$n=1$$, this reduces to maximizing $$\log p(x)$$.

### Amortized SVGD

SVGD may be inefficient, so on way to do this is to train a neural network $$f(\eta; \xi)$$ to mimic the SVGD dynamics, where $$\eta$$ is the network parameters, and $$\xi$$ is the input.

Each iteration, a batch of input is drawn and calculated. The Stein variational gradient $$\Delta x$$ would ensure that $$x_i^\prime = x_i + \epsilon \Delta x_i$$ forms a better approximation of the target distribution p. Therefore, $$\eta$$ shoudl be adjusted to match $$x_i^\prime$$ by minimizing the L2 loss. In practice this can be performed over only one gradient step

$$

\eta^{t+1} \leftarrow \eta^t + \epsilon \sum_{i=1}^{m} \partial_\eta f(\eta^t, \xi_i) \Delta x_i

$$

This is also related to the reparametrization trick.

### Amortized MLE for GAN

Energy based model as discriminator $$p(x\lvert \theta)$$, $$f(\eta; \xi)$$ is a generator that tries to fit the generative process of discriminative model.
