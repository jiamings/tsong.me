---
layout: post
title: Learning to Generate Samples from Noise Through Infusion Training
author: Jiaming Song
tags:
- reading
---

## Learning to Generate Samples from Noise Through Infusion Training

### Sampling through Markov Chain

The generative model is defined through the following procedure:

1. Using a simple factorial distribution $$p^{(0)}(z^{(0)})$$ draw an initial sample $$z^{(0)} \sim p^{(0)}$$, where $$z^{(0)}$$ has the same  dimension as the data.
2. Repeatedly apply T times a stochastic transition operator $$p^{(t)}(z^{(t)}\lvert z^{(t-1)})$$, which provides a more "denoised" sample $$z^{(t)}$$.
3. Obtain $$z^{(T)}$$ as the final sample.

Thus the generative model is $$p(z^{(t)}) = p^{(0)}(z^{(0)}) (\prod_{t=1}^T p^{(t)}(z^{(t)} \lvert z^{(t-1)}))$$.

### Infusion Training Procedure

Let $$\theta^{(t)}$$ be the prarmeters for $$p^{(t)}$$. We can share the parameters of $$t > 0$$ across time.

One procedure would be the greedy layerwise procedure - use greedy layerwize maximum likelihood training on each layer. This intuitive way of training, however, makes no sense - for $$ t > 1 $$ the objective becomes essentially the same as training the first objective. To see this, we show that $$p^{(1)}(x \lvert z^{(0)}) = p^{(1)}(x)$$, since $$z^{(0)}$$ and $$x$$ are drawn independently.

One way to solve this is to introduce some dependency on $x$. Formally, one can introduce a infused transition as $$q_i^{(t)}(z_i^{(t)}\lvert z_i^{(t-1)}, x) = (1 - \omega) p_i^{(t)}(z_i^{(t)}\lvert z_i^{(t-1)}) + \omega \delta_{x_i} (z_i^{(t)})$$ 

The procedure can be explained as follows. For each $$x$$ in training data:

- Sample the infusion chain
- Perform a gradient step so that $$p$$ learns to "denoise" every $$z^{(t)}$$ into $$x$$.

$$
\theta^{(t)} \leftarrow \theta^{(t)} + \eta \frac{\partial \log p^{(t)}(x \lvert z^{(t-1)}; \theta^{(t)})}{\partial \theta^{(t)}}
$$



