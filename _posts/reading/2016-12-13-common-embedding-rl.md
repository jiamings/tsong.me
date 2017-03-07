---
layout: post
title: Learning Invariant Feature Spaces to Transfer Skills with Reinforcement Learning
author: Jiaming Song
tags:
- reading
---

## Learning Invariant Feature Spaces to Transfer Skills with Reinforcement Learning

### Common Feature Spaces

The common feature space assumes that for two state distribution of the optimal policy $$\pi_S$$ and $$\pi_T$$, it is possible to learn two function $$f$$ and $$g$$, such that $$p(f(s_S)) = p(g(s_T)$$.

### Learning Common Feature Spaces from A Proxy Task

Basically there are two autoencoders, which tries to autoencode the states, and a regularizer that tries to minimize the distance between the common feature space embedding.


$$
\mathcal{L} = \mathcal{L}_{sim} + \mathcal{L}_{AE_S} + \mathcal{L}_{AE_T}
$$


### Using the Common Embedding for Knowledge Transfer

Instead of attempting direct policy transfer, the distribution of optimal trajectories are matched across the domains. Therefore, apart from the target reward objective, an additional term is included


$$
r_{t}(s_{T}) = \alpha \lVert f(s_S) - g(s_T) \rVert_2
$$
Hnece the additional incentive guides the target policy to match the original policy in the common embedding space.