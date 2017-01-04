---
layout: post
title: Learning to Play in a Day - Faster Deep Reinforcement Learning by Optimiality Tightening
author: Jiaming Song
tags:
- reading
---

## Learning to Play in a Day: Faster Deep Reinforcement Learning by Optimiality Tightening

[https://openreview.net/pdf?id=rJ8Je4clg](https://openreview.net/pdf?id=rJ8Je4clg)

Deep Q-Learning has high demand for computational resources. This work proposes to accelerate deep Q-learning by fast reward propagation by taking advantage of the longer sequences which are readily available in the "experience replay memory".

Note that the following holds for the optimal $$Q$$-function $$Q^\star$$.



$$
Q^\star(s_j, a_j) = r_j + \gamma \max_a Q^\star(s_{j+1}, a) = \ldots = r_j + \gamma \max_a [r_{j+1} + \gamma \max_{a^\prime} Q^\star(s_{j+1}, a^\prime)]
$$


Therefore



$$
Q^\star(s_j, a_j) = r_j + \gamma \max_a Q^\star(s_{j+1}, a) \geq \ldots \geq \sum_{i=0}^{k}\gamma^i r_{j+i} + \gamma^{k+1}\max_a Q^\star(s_{j+k+1}, a) = L^\star_{j, k}
$$


which is a lower bound for $$Q^\star(s_j, a_j)$$. We can also define upper bounds:



$$
U^\star_{j,k} = \gamma^{-k-1} Q^\star(s_{j-k-1}, a_{j-k-1}) - \sum_{i=0}^{k} \gamma^{i-k-1}r_{j-k-1+i} \geq Q^\star(s_j, a_j)
$$


And transform the objective to:



$$
\min_\theta \sum (Q_\theta(s_j, a_j) - y_j)^2 \quad \mbox{s.t.} \quad U_j^{\min} \geq Q_\theta(s_j, a_j) \geq L_j^{\max}
$$


This objective is highly non-convex in the constraints, so the program can be reformulated to



$$
\min_\theta \sum [(Q_\theta(s_j, a_j) - y_j)^2 + \lambda (L_j^\max - Q_\theta(s_j, a_j))_+^2 + \lambda (Q_\theta(s_j, a_j) - U_j^\min)_+^2]
$$



$$L^\max$$ and $$U^\min$$ can be computed in parallel, which allows for the speed up. If memory is not enough, the model can use a subset of the constraints, instead of all of them.