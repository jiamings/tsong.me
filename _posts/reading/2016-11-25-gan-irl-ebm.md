---
layout: post
title: A Connection Between GAN, IRL, and EBM
author: Jiaming Song
tags:
- reading
---

## A Connection Between Generative Adversarial Networks, Inverse Reinforcement Learning, and Energy-Based Models

> By Finn et al. [https://arxiv.org/pdf/1611.03852v3.pdf](https://arxiv.org/pdf/1611.03852v3.pdf)
>
>  A sampled based algorithm for maximum entropy IRL and a GAN in which the generator's density can be evaluated and is provided as an additional input to the discriminator. Interestingly, maximum entropy IRL is a special case of an energy-based model.

### Inverse Reinforcement Learning

The goal is to infer the cost function underlying demonstrated behavior.

#### Maximum Entropy IRL

Maximum Entropy RL models the demonstrations using a Boltzmann distribution, where the energy is given by the cost fuction:


$$
p_\theta(\tau) = \frac{1}{Z} \exp(-c_\theta(\tau))
$$


The optimal trajectories have the highest likelihood, and the expert can generate suboptimal paths with a probability that decreases exponentially.

#### Guided Cost Learning

The algorithm estimates $$Z$$ by training a new sampling distribution $$q(\tau)$$ and using importance sampling. 


$$
\mathcal{L}_{cost} (\theta) = \mathbb{E}_{\tau \sim p}[-\log p_\theta(\tau)] = \mathbb{E}_{\tau \sim p}[c_\theta(\tau)] + \log Z \\
= \mathbb{E}_{\tau \sim p}[c_\theta(\tau)] + \log (\mathbb{E}_{\tau \sim q}[\frac{\exp(-c_\theta (\tau))}{q(\tau)}])
$$


The importance sampling estimate can have very high variance if the sampling distribution $$q$$ fails to cover some trajectories $$\tau$$ with high values of $$\exp (-c_\theta (\tau))$$. One way to address this is to mix sampling data and demonstrations $$\mu = \frac{1}{2} p + \frac{1}{2} q$$.


$$
\mathcal{L}_{cost} (\theta) = \mathbb{E}_{\tau \sim p}[-\log p_\theta(\tau)] = \mathbb{E}_{\tau \sim p}[c_\theta(\tau)] + \log Z \\
= \mathbb{E}_{\tau \sim p}[c_\theta(\tau)] + \log (\mathbb{E}_{\tau \sim \mu}[\frac{\exp(-c_\theta (\tau))}{\mu(\tau)}])
$$

### GAN = MaxInt IRL

For GAN the log loss for discriminator is equal to:


$$
\mathcal{L} (D_\theta) = \mathbb{E}_{\tau \sim p}[-\log D_\theta (\tau)] + \mathbb{E}_{\tau \sim q} [-\log (1 - D_\theta(\tau))]
$$


where $$ D_\theta(t) = \frac{\frac{1}{Z}\exp(-c_{\theta}(\tau))}{\frac{1}{Z}\exp(-c_{\theta}(\tau)) + q(\tau)} $$

There are three facts that imply that GANs optimize precisely the MaxEnt IRL problem

1. The value of $$Z$$ which minimizes the discriminator's loss is an importance-sampling estimator for the partition function.n (Compute $$\frac{\partial \mathcal{L}(D_\theta)}{\partial Z}$$)
2. For this value of $$Z$$, the derivative of the discriminator's loss wrt. $$\theta$$ is equal to the derivative for the MaxEnt IRL objective. (Compute $$\frac{\partial \mathcal{L}(D_\theta)}{\partial \theta}$$ and $$\frac{\partial \mathcal{L}_{cost}(\theta)}{\partial \theta}$$)
3. The generator's loss is exactly equal to the cost $$c_\theta$$ minus the entropy of $$q(\tau)$$.