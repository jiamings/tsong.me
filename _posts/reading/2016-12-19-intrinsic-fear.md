---
layout: post
title: Combating Deep Reinforcement Learning's Sisyphean Curse with Intrinsic Fear
author: Jiaming Song
tags:
- reading
---

## Combating Deep Reinforcement Learning's Sisyphean Curse with Intrinsic Fear

Deep reinforcement learning with function approximations may forget about catastrophic outcomes. This is because of the following failure:

1. Training under distribution $$\mathcal{D}$$, our agent produces a safe policy $$\pi_s$$ that avoids catastophes
2. Collecting data generated under $$\pi_s$$ yields a distribution $$\mathcal{D}^\prime$$
3. Training under $$\mathcal{D}^\prime$$, the agent produces $$\pi_d$$, a policy that once again experiences catastrophes.



### Safe Reinforcement Learning

*Fatality* is defined as a return below some threshold $$\tau$$. In this view, the $$\hat{Q}$$ learning objective seeks to minimize the worst case scenario


$$
\hat{Q} = \min (\hat{Q}(s_t, a_t), r_{t+1} + \gamma \max_{a_{t+1} \in \mathcal{A}} \hat{Q}(s_{t+1}, a_{t+1}))
$$
Other objective penalize policies for returns with high variance, and in the extreme cases, the policy search is confined to policies that are *safe*.

In this paper, a new safety problem called *danger* is proposed. The agent is instructed to avoid catastrophic zones in the future, and try to avoid one when that happens.



### Intrinsic Fear

In this approach, both a DQN and a separate, supervised *danger model* is provided. The *danger model* provides an auxillary source of reward, penalizing the learner for entering dangerous states.

The model is encouraged to update $$Q(s_t, a_t; \theta_Q)$$ towards 


$$
r_t + \max{a^\prime} Q(s{t+1}, a^\prime; \theta_Q) - \lambda \cdot d(s_{t+1}; \theta_d)
$$
where $$d$$ is the danger model.