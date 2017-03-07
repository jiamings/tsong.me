---
layout: post
title: Deep Unsupervised Learning Using Nonequilibrium Thermodynamics
author: Jiaming Song
tags:
- reading
---

## Deep Unsupervised Learning Using Nonequilibrium Thermodynamics

> Sohl-Dickstein et al. 2015. [https://arxiv.org/pdf/1503.03585v8.pdf](https://arxiv.org/pdf/1503.03585v8.pdf)

### Model

The goal is to define a forward difussion process which converts any complex data distribution into a simple tractable distribution, and then learn a finite-time reversal of this diffusion process which defines the generative model distribution.
$$
\pi(y) = \int dy^\prime T_\pi (y \lvert y^\prime; \beta) \pi (y^\prime)
$$

$$
q(x^{(t)} \lvert x^{(t-1)}) = T_\pi (x^{(t)} \lvert x^{(t-1)}; \beta_t)
$$

The forward trajectory is thus:


$$
q(x^{(0 \ldots T)}) = q(x^{(0)}) \prod_{t=1}^{T} q(x^{(t)} \lvert x^{(t-1)})
$$


The reverse trajectory is:


$$
p(x^{(0 \ldots T)}) = p(x^{(T)}) \prod_{t=1}^{T} p(x^{(t-1)} \lvert x^{(t)})
$$


The probability the generative model assigns to the data is 


$$
p(x^{(0)}) = \int dx^{(1\ldots T)} q(x^{(1\ldots T)} \lvert x^{(0)}) \cdot p(x^{(T)}) \prod_{t=1}^{T} \frac{p(x^{(t-1)} \lvert x^{(t)} )}{q(x^{(t)} \lvert x^{(t-1)})}
$$


### Training

Training amounts to maximizing the model log-likelihood


$$
L = \int dx^{(0)} q(x^{(0)}) \log p(x^{(0)}) \geq \int dx^{(0 \ldots T)} q(x^{(0 \ldots T)}) \log [p(x^{(T)} \prod_{t=1}^{T} \frac{p(x^{(t-1)} \lvert x^{(t)})}{q(x^{(t)} \lvert x^{(t-1)})})]
$$


Which gives us 


$$
L \geq K \\
K  = -\sum_{t=2}^{T} \int dx^{(0)} dx^{(t)} q(x^{(0)}, x^{(t)}) \cdot D_{KL} (q(x^{(t-1)} \lvert x^{(t)}, x^{(0)}) \lVert p(x^{(t-1)} \lvert x^{(t)})) \\ + H_q(X^{(T)} \lvert X^{(0)}) - H_q(X^{(1)} \lvert X^{(0)}) - H_p (X^{(T)})
$$


The training objective would then be $$\arg \max K$$.

### Modifying Distributions

Some tasks would require one to compute a distribution which requires a $$\tilde{p}(x^{(0)}) \propto p(x^{(0)}) r(x^{(0)})$$. To derive the kernel, two steps are needed:

- Introduce normalizing constant $$\tilde{Z}_{t}$$

- Satisfy the equilibrium condition. $$\tilde{p}(x^{(t)} \lvert x^{(t+1)}) = \frac{1}{\tilde{Z}_t (x^{(t+1)})} p(x^{(t)} \lvert x^{(t+1)}) r(x^{(t)})$$

  ​