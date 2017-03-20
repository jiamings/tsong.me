---
layout: post
title: Evolutional Strategies as a Scalable Alternative to Reinforcement Learning
author: Jiaming Song
tags:
- reading
---

## Evolutional Strategies as a Scalable Alternative to Reinforcement Learning

Paper: [https://arxiv.org/abs/1703.03864](https://arxiv.org/abs/1703.03864)



Evolutional Strategies for reinforcement learning (ES) is a type of reparametrization trick for smoothing in reinforcement learning. Traditionally in score function approximation of gradients:


$$
\nabla \mathbb{E}_{\theta \sim p(\theta)}[f(\theta)] = \mathbb{E}_{\theta \sim p(\theta)}[f(\theta) \nabla_\theta \log p(\theta)]
$$


In traditional policy gradient, $$p(\theta)$$ is introduced in the policy level, therefore it requires backpropagation through $$p(\theta)$$. In ES, the authors propose to use a Gaussian as $$p(\theta)$$, which does not require backpropagation to compute the gradient, since the gradient of log-Gaussian is simple.



To me, ES is analogous to the "implicit models" in the generative modeling literature. I am not familiar with the ES literature, and wonder why this name is selected (or even mentioning ES is necessary).



The advantages of the reprametraizations are:

1. No need to compute and send gradients (for the network)
2. Faster parallelism
3. Better than PG for long episodes with long steps
4. Do not require smoothing as in PG does.



The disadvantages of ES are:

1. For larger networks, Gaussian noise might not be a great exploration strategy.
2. Gaussian noise might not work well for convolutional settings.



#### References

{% bibliography --cited %}