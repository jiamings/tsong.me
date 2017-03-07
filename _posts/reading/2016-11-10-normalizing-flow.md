---
layout: post
title: Variational Inference with Normalizing Flows
author: Jiaming Song
tags:
- reading
---

## Variational Inference with Normalizing Flows

A *normalizing flow* describes the transformation of a probability density through a sequence of invertible mappings.

Consider a smooth, invertible mapping $$f: \mathbb{R}^d \rightarrow \mathbb{R}^d$$ with inverse $$f^{-1} = g$$. If we use this mapping to transform a random variable $$z$$ with distribution $$q(z)$$, the resulting random variable $$z^\prime = f(z)$$ has a distribution

$$

q(z^\prime) = q(z) \lvert \mathrm{det}\frac{\partial f}{\partial z}\mid^{-1}

$$

Any expectation under $$q_K$$ can be written as an expectation under $$q_0$$ as

$$

\mathbb{E}_{q_K}[h(z_K)] = \mathbb{E}_{q_0}[h(f_k \circ \ldots \circ f_1 (z_0))]

$$

which does not require computation of the logged-Jacobian terms when $$h(z)$$ does not depend on $$q_K$$.
