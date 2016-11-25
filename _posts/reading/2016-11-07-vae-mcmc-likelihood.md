---
layout: post
title: On the Quantitative Analysis of Decoder-Based Generative Models
author: Jiaming Song
tags:
- reading
---

### On the Quantitative Analysis of Decoder-Based Generative Models

#### Annealed Importance Sampling

The objective is to obtain the marginal likelihood $$p(x)$$ when the posterior distribution $$p(z\lvert x)$$ is intractable. One simple approach would be likelihood weighing, which is a form of importance sampling:

$$
p(x) = \sum_z \frac{p(x, z)}{p(z)}p(z) = \mathbb{E}_{z \sim p(z)} [\frac{p(x, z)}{p(z)}]
$$

However, in high dimension regions, $$p(z)$$ may be very different from $$p(z\lvert x)$$, so instead of sampling from the distribution directly, a set of intermediate distributions are considered, such as the geometric averages of $$p(z)$$ and $$p(x, z)$$.

The AIS produces a unbiased estimate of $$p(x)$$ as follows: 

1. Sample a random $$z_1$$ from $$p_1$$ and set the initial weight $$w_1 = 1$$. 

2. For every stage $$t \geq 2$$ update $$w_t$$ and $$z_t$$, according to

$$
w_t \leftarrow w_{t-1}\frac{f_t(z_{t-1})}{f_{t-1}(z_{t-1})} \quad z_t \sim \mathcal{T}_t(z|z_{t-1})
$$

#### Bidirectional Monte Carlo

To estimate $$p(x)$$ in the log space, we notice that the logarithm of a nonnegative unbiased estimate is the *statistical lower bound* of the log estimate. Therefore, the log of the estimated AIS $$\log p(\tilde{x})$$ is a lower bound for the true $$\log p(x)$$.

If AIS is run in reverse starting from $$p(x, z)$$ and to $$p(x)$$, this essentially gives us an estimate of $$1/p(x)$$, whose negative logartithm is a statistical upper bound of $$\log p(x)$$. Therefore, we can run bidirectional monte carlo to obtain a precise pinpoint value.

