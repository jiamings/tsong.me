---
layout: post
title: Improving Variational Inference with Inverse Autoregressive Flow
author: Jiaming Song
tags:
- reading
---

## Improving Variational Inference with Inverse Autoregressive Flow

Basically, find a type of normalizing flow that is both powerful and computationally cheap.

Consider an autoregressive Gaussian generative model

$$

\begin{array}\\
y_0 = \mu_0 + \sigma_0 \cdot z_0 \\
y_i = \mu_i(y_{1:i-1}) + \sigma_i(y_{1:i-1}) \cdot z_i \\
z_i \sim \mathcal{N}(0, 1) \quad \forall i
\end{array}

$$

$$z_i$$ can be reverted using

$$

z_i = \frac{y_i - \mu_i (y_{1:i-1})}{\sigma_i (y_{1:i-1})}

$$

which can be computed in parallel because of the independence between $$z_i$$s.

Given that insight, inverse autoregressive flow basically uses the inverse of the autoregressive Gaussian generative model.
