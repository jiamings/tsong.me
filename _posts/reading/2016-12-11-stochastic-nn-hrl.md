---
layout: post
title: Stochastic Neural Networks for Hierarchical Reinforcement Learning
author: Jiaming Song
tags:
- reading
---



## Stochastic Neural Networks for Hierarchical Reinforcement Learning

Currently, deep RL employ naive exploration strategies, and work poorly in tasks with sparse rewards. To tackle these challenges, two popular approaches are used

1. design hand crafted hierarchy over the actions
2. utilize domain agnostic intrinsic rewards to guide exploration

In the paper a general framework for learning useful skills in a pre-training environment, whihc can be used in downstream tasks by training a high-level policy over these skills.



**The main interest** is in solving a collection of downstream tasks, specified via a collection of MDPs $$\mathcal{M}$$.

**The pre-training environment** is where the agent can freely interact with the environment in minimal setup. Rather than specifying goals, an intrinsic reward is used as the only signal to guide skill learning, which should encourage locally optimal solutions.

**The stochastic neural network** is basically a fancy way of saying deep generative model. It serves the purpose of defining a flexible weight sharing scheme among different policies.

**The information theoretic optimization** prevents the generator to collapse to a single mode.

**The high level policy** is learned using a span of skills learned from the pre training task and the sparse reward signal. The high level policy receive a full state as input and outputs a sample of the skill. The high level policy operates slower than the SNN policy by a factor of $$\tau$$. The weights of SNN are freezed during this phase of training. 

