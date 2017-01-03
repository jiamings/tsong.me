---
layout: post
title: Surprised-Based Intrinsic Motivation for Deep Reinforcement Learning
author: Jiaming Song
tags:
- reading
---

## Surprised-Based Intrinsic Motivation for Deep Reinforcement Learning

Simple heuristic methods of exploring such as $$\epsilon$$-greedy action selection and Gaussian control noise are inadequate. One approach to encourage better exploration is via intrisic motivation, where the agent has a task-independent intrinsic reward function where it seeks to maximize in addition to the reward.

Examples include:

1. **Empowerment**, where the agent enjoys the level of control of the future
2. **Surprise**, where the agent is excited to see outcomes that run contrary to understanding the world
3. **Novelty**, where the agent is excited to see new states



To train an agent with surprised-based exploration, alternates are made between updating a dynamics model and updating a policy that maximizes a trade-off between policy performance and surprise measure.

The dynamics model step makes an update on


$$
\min_\phi - \frac{1}{\lvert D \lvert} \sum_{(s,a, s^\prime) \in D} \log P_\phi(s^\prime \lvert s, a) + \alpha f(\phi)
$$


The policy update makes an update on 


$$
\max_\pi L(\pi) + \eta \mathbb{E}_{(s, a) \sim \pi}[\mathrm{KL}(P \lVert P_\phi)[s, a]]
$$
The shaped reward looks like


$$
r^\prime(s, a, s^\prime) = r(s, a, s^\prime) + \eta \ (\log P(s^\prime \lvert s, a) - \log P_\phi(s^\prime \lvert s, a))
$$
However, since $$\log P$$ is unknown, approximations should be made.

