---
layout: post
title: Operator Variational Inference
author: Jiaming Song
tags:
- reading
---
## Operator Variational Inference

Approximate Bayesian inference seeks to approximate the posterior distribution $$p(z\lvert x)$$. One commonly used notion is the Evidence Lower BOund (ELBO):

$$

\mathbb{E}_{q(z)}[\log p(x, z) - \log q(z)]

$$

Maximizing the ELBO is equivalent to minimizing the KL divergence to the posterior.

### Operator Variational Objectives

- Operator $$O^{p,q}$$ that depends on $$p(z\lvert x)$$ and $$q(z)$$. It is required to be written in terms of $$p(x, z)$$ and $$q(z)$$.
- Family of test functions $$\mathcal{F}$$, where each $$\mathcal{F}$$ maps latent variables to real vectors.
- A distance function $$t(a) : \mathbb{R} \rightarrow [0, \infty]$$

The operator variational objective is therefore:

$$

\mathcal{L}(q; O^{p, q}, \mathcal{F}, t) = \sup_{f\in \mathcal{F}} t(\mathbb{E}_{q(z)}[(O^{p, q}f)(z)])

$$

which is the worst case expected value among all the functions in $$\mathcal{F}$$.

For positive valued operators, one can choose KL divergence, $$\alpha$$-divergence, $$\chi$$-divergence.

For real valued operators, the operators leads to Stein divergence as:

$$

D_{\mathrm{stein}}(p, q) = \sup_{f} \lvert \mathbb{E}_{q(z)}[f(z)] - \mathbb{E}_{p(z\lvert x)}[f(z)]\lvert

$$

The authors apply the Langevin-Stein operator

$$

\mathcal{L}(q; O^{p, q}_{LS}, \mathcal{F}) = \sup_{f\in \mathcal{F}} (\mathbb{E}_{q(z)}[\nabla_z \log p(x, z)^\top f(z) + \nabla^\top f])^2

$$

Interestingly, the LS operator does not require the analytical form of $$q(z)$$ - only samples are needed. (which is an issue in energy based models)

### Operator Variational Inference

OPVI seeks to solve a minimax problem:

$$

\lambda^* = \inf_{\lambda}\sup_{\theta} t(\mathbb{E}_\lambda[(O^{p, q}f_\theta)(z)])

$$

which looks strikingly similar to the objective for energy based GAN, in terms of the order of min and max.
