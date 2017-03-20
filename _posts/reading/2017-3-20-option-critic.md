---
layout: post
title: The Option-Critic Architecture
author: Jiaming Song
tags:
- reading
---

## The Option-Critic Architecture 

Paper: [https://arxiv.org/abs/1609.05140](https://arxiv.org/abs/1609.05140)

A Markovian option $$\omega \in \Omega$$ is a triple $$(\mathcal{I}_\omega, \pi_\omega \beta_\omega)$$ in which $$\mathcal{I} \in \mathcal{S}$$ is an initiation set, $$\pi_\omega$$ is an *intra-option* policy, and $$\beta_\omega$$ is a termination function.

The option-value function can be written as:


$$
Q_\Omega(s, \omega) = \sum_a \pi_{\omega, \theta}(a | s) Q_U(s, \omega, a)
$$
where


$$
Q_U(s, \omega, a) = r(s, a) + \gamma \sum_{s^\prime} P(s^\prime | s, a) U(\omega, s^\prime)
$$
$$U(\omega, s)$$ is called the option-value function *upon arrival*. The value of executing $$\omega$$ upon entering a state $$s^\prime$$ is given by:


$$
U(\omega, s^\prime) = (1 - \beta_{\omega, \vartheta}(s^\prime)) Q_\omega(s^\prime, \omega) + \beta_{\omega, \vartheta}(s^\prime) V_\omega (s^\prime)
$$


Note that each option have its individual $$\theta$$ and $$\vartheta$$ parameters. 

**Intra-Option Policy Gradient Theorem** Given a set of Markov options with stochastic intra-option policies differentiable in their parameters $$\theta$$, the gradient of the expected discounted return with respect to $$\theta$$ and initial condition $$(s_0, \omega_0)$$ is:


$$
\sum_{s, \omega} \sum_{t=0}^{\infty} \gamma^t P(s_t = s, \omega_t = \omega | s_0, \omega_0) \sum_a \frac{\partial \pi_{\omega, \theta}(a | s)}{\partial \theta}Q_U(s, \omega, a)
$$
**Termination Gradient Theorem** Given a set of set of Markov options with stochastic termination function differentiable in their parameters $$\vartheta$$, the gradient of the expected discounted return objective with respect to $$\vartheta$$ and the initial condition $$(s_1, \omega_0)$$ is


$$
-\sum_{s^\prime, \omega} \sum_{t=0}^{\infty}\gamma^t P(s_{t+1} = s^\prime, \omega_t = \omega | s_1, \omega_0) \frac{\partial \beta_{\omega, \vartheta}(s^\prime)}{\partial \vartheta}A_{\Omega}(s^\prime, \omega)
$$
where $$A_\Omega(s, \omega)$$ is the advantage function over options. 



The optimization process is over the $$Q$$ values, and option parameters $$\theta$$ and $$\vartheta$$. The values are learned at a *fast* scale (through Q-learning) and the option parameters at a *slow scale* (through policy gradient).