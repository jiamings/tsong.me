---
layout: post
title: Paper Reading (Nov. 8 - Nov. 14)
author: Jiaming Song
tags:
- reading
---

## On the Quantitative Analysis of Decoder-Based Generative Models

### Annealed Importance Sampling

The objective is to obtain the marginal likelihood $$p(x)$$ when the posterior distribution $$p(z\lvert x)$$ is intractable. One simple approach would be likelihood weighing, which is a form of importance sampling:

$$
p(x) = \sum_z \frac{p(x, z)}{p(z)}p(z) = \mathbb{E}_{z \sim p(z)} [\frac{p(x, z)}{p(z)}]
$$

However, in high dimension regions, $$p(z)$$ may be very different from $$p(z\lvert x)$$, so instead of sampling from the distribution directly, a set of intermediate distributions are considered, such as the geometric averages of $$p(z)$$ and $$p(x, z)$$.

The AIS produces a unbiased estimate of $$p(x)$$ as follows: 

1. Sample a random $$z_1$$ from $$p_1$$ and set the initial weight $$w_1 = 1$$. 

2. For every stage $$t \geq 2$$ update $$w_t$$ and $$z_t$$, according to
   
$$

   w_t \leftarrow w_{t-1}\frac{f_t(z_{t-1})}{f_{t-1}(z_{t-1})} \quad z_t \sim \mathcal{T}_t(z\lvert z_{t-1})
   
$$

   ​

### Bidirectional Monte Carlo

To estimate $$p(x)$$ in the log space, we notice that the logarithm of a nonnegative unbiased estimate is the *statistical lower bound* of the log estimate. Therefore, the log of the estimated AIS $$\log p(\tilde{x})$$ is a lower bound for the true $$\log p(x)$$.

If AIS is run in reverse starting from $$p(x, z)$$ and to $$p(x)$$, this essentially gives us an estimate of $$1/p(x)$$, whose negative logartithm is a statistical upper bound of $$\log p(x)$$. Therefore, we can run bidirectional monte carlo to obtain a precise pinpoint value.



## Variational Lossy Autoencoder

In autoregressive structures, it is easy for the model to ignore the latent code by just using the prior distribution, and put the representation burden on the model $$p(x\lvert z)$$, while $$q(z\lvert x)$$ carries few information.

### Understanding VAE from Bits-Back Coding Perspective

VAE can be seen as a way to encode data in a two-part code: $$p(z)$$ and $$p(x\lvert z)$$. 

This gives us the naive encoding length:

$$

\mathcal{C}_{naive}(x) = \mathbb{E}_{x\sim p(x), z\sim q(z\lvert x)}[-\log p(z) - \log p(x\lvert z)]

$$

The Bits-Back Coding improves by noticing that the encoder distribution $$q(z\lvert x)$$ can be used to transmit additional information, up to $$H(q(z\lvert x))$$ expected nats.

$$

\mathcal{C}_{BB}(x) = \mathbb{E}_{x\sim p(x), z\sim q(z\lvert x)}[\log q(z\lvert x) -\log p(z) - \log p(x\lvert z)] = \mathbb{E}_{x\sim p(x)}[-\mathcal{L}(x)]

$$

This view of VAE as a efficient coding scheme allows us to reason *when* the latent code $$z$$ will be used: only when the two-part code is an efficient code. Therefore

$$

\begin{array}\\
\mathcal{C}_{BB}(x) & = \mathbb{E}_{x\sim p(x), z\sim q(z\lvert x)}[\log q(z\lvert x) -\log p(z) - \log p(x\lvert z)] \\
 & = \mathbb{E}_{x\sim p(x)} [-\log p(x) + \mathcal{D}_{KL}(q(z\lvert x) \rVert p(z\lvert x))] \\
 & \geq \mathbb{E}_{x\sim p(x)} [-\log p_{data}(x) + \mathcal{D}_{KL}(q(z\lvert x) \rVert p(z\lvert x))] \\
 & = \mathcal{H}(p(x)) +  \mathbb{E}_{x\sim p(x)} [\mathcal{D}_{KL}(q(z\lvert x) \rVert p(z\lvert x))]
\end{array}

$$

Since the second term is always larger than zero, we know that using the KL term derived from VAE suffers at least an extra code length. If the $$p(x\lvert z)$$ can model $$p(x)$$ without using the information from $$z$$, then the latent code $$z$$ is not used, which causes the true posterior to be simply the prior $$p(z)$$. Hence, information that can be modeled locally by decoding distribution $$p(x\lvert z)$$ without access to $$z$$ will be encoded locally and only the remainder will be encoded in $$z$$.

### Variational Lossy Autoencoder

There are two ways to utilize this information:

1. Use **explicit information placement** to restrict the reception of the autoregressive model, thereby forcing the model to use the latent code $$z$$ which is globally provided.
2. **Parametrize the prior distribution with a autoregressive model** showing that a type of autoregressive latent code can reduce inefficiency in Bits-Back coding.

## Zoneout: Regularizing RNNs by Randomly Preserving Hidden Activations

Zoneout randomly preserves the hidden unit of the previous state, instead of setting the value to zero in dropout.



## Calibrating Energy-Based Generative Adversarial Networks

### Optimization Dynamics Near Convergence of GANs

When the generator dstribution matches the data distribution, the training signal w.r.t. the discriminator vanishes, which pushes the generator that appears more real to the discriminator. Hence, the generator distribution will diverge from the data distrubution. In order to keep generator stationary as the data distribution, the discriminator must assign exactly same (flat) density to all samples at the optimal.

To tackle this problem, one needs to consider providing an additional training signal to the generator, such that the additional signal can

1. Balance the discriminator at optimum.
2. Cooperate with the discriminator to ensure the generator converges to the data distribution

### A New Formulation of GAN

The following adversarial learning formulation is proposed:

$$

\max_c \min_{p_g \sim \mathcal{P}} \mathbb{E}_{x\sim p_g}[c(x)] - \mathbb{E}_{x\sim p_d}[c(x)] + K(p_g)

$$

Define $$L(p_g, c) = \mathbb{E}_{x\sim p_g}[c(x)] - \mathbb{E}_{x\sim p_d}[c(x)] + K(p_g)$$, then $$L(p_g, c)$$ is the Lagrange dual function of the following optimization problem:

$$

\begin{array}\\
\min_{p_g \in \mathcal{P}} & K(p_g) \\
\mathrm{s.t.} & p_g(x) - p_d(x) = 0, \forall x \in \mathcal{X}
\end{array}

$$

We add the contraints for $$p_g(x)$$, and then by the KKT conditions, the optimal generator distribution $$p_g^*$$ matches the true data distribution, and the discriminator has the following form:

$$

c^*(x) = -\frac{\partial K(p_g)}{\partial x} \lvert _{p_g = p_d} - \lambda^* + \mu^*(x), \forall x \in \mathcal{X}

$$

where $$\mu^*(x)$$ is zero when $$p_d(x) > 0$$ and $$u_x$$ otherwise. This is called the *weak support discriminator*, which provides all the discrimination information in the original GAN formulation.

### Forms of $$K(p_g)$$

There are several forms of $$K(p_g)$$.

1. Entropy $$-H(p_g)$$
2. $$\ell_2$$ regularization on $$p_g$$
3. Constant

## Variational Inference with Normalizing Flows

A *normalizing flow* describes the transformation of a probability density through a sequence of invertible mappings.

Consider a smooth, invertible mapping $$f: \mathbb{R}^d \rightarrow \mathbb{R}^d$$ with inverse $$f^{-1} = g$$. If we use this mapping to transform a random variable $$z$$ with distribution $$q(z)$$, the resulting random variable $$z^\prime = f(z)$$ has a distribution

$$

q(z^\prime) = q(z) \lvert \mathrm{det}\frac{\partial f}{\partial z}\mid^{-1}

$$

Any expectation under $$q_K$$ can be written as an expectation under $$q_0$$ as

$$

\mathbb{E}_{q_K}[h(z_K)] = \mathbb{E}_{q_0}[h(f_k \circ \ldots \circ f_1 (z_0))]

$$

which does not require computation of the logged-Jacobian terms when $$h(z)$$ does not depend on $$q_K$$.



## Improving Variational Inference with Inverse Autoregressive Flow

Basically, find a type of normalizing flow that is both powerful and computationally cheap.

Consider an autoregressive Gaussian generative model

$$

\begin{array}\\
y_0 = \mu_0 + \sigma_0 \cdot z_0 \\
y_i = \mu_i(y_{1:i-1}) + \sigma_i(y_{1:i-1}) \cdot z_i \\
z_i \sim \mathcal{N}(0, 1) \quad \forall i
\end{array}

$$

$$z_i$$ can be reverted using

$$

z_i = \frac{y_i - \mu_i (y_{1:i-1})}{\sigma_i (y_{1:i-1})}

$$

which can be computed in parallel because of the independence between $$z_i$$s.

Given that insight, inverse autoregressive flow basically uses the inverse of the autoregressive Gaussian generative model.



## Unrolled Generative Advesarial Networks

GAN has the following minimax objective

$$

\theta_G^* = \arg\min_{\theta_G} f(\theta_G, \theta_D^*)

$$

A local optimum of discriminator update parameters $$\theta^*_D$$ can be expressed as the fixed point of an iterative optimization procedure,

$$

\theta_D^0 = \theta_D \\
\theta_D^{k+1} = \theta_{D}^{k} + \eta^{k} \frac{\mathrm{d} f(\theta_G, \theta_D^k)}{\mathrm{d} \theta_D^{k}}

$$

By unrolling for $$K$$ steps, a surrogate objective is created for the update of the generator.

Without the rolling, the generator tends to focus on the mode where the discriminator assigns highest probability value. One issue with the evaluation of generative models by looking at the images is that humans fail to notice missing modes; in fact, GAN can be better at producing visually appealling images by assigning most of its representation power to a few modes.



## Operator Variational Inference

Approximate Bayesian inference seeks to approximate the posterior distribution $$p(z\lvert x)$$. One commonly used notion is the Evidence Lower BOund (ELBO):

$$

\mathbb{E}_{q(z)}[\log p(x, z) - \log q(z)]

$$

Maximizing the ELBO is equivalent to minimizing the KL divergence to the posterior.

### Operator Variational Objectives

- Operator $$O^{p,q}$$ that depends on $$p(z\lvert x)$$ and $$q(z)$$. It is required to be written in terms of $$p(x, z)$$ and $$q(z)$$.
- Family of test functions $$\mathcal{F}$$, where each $$\mathcal{F}$$ maps latent variables to real vectors.
- A distance function $$t(a) : \mathbb{R} \rightarrow [0, \infty]$$

The operator variational objective is therefore:

$$

\mathcal{L}(q; O^{p, q}, \mathcal{F}, t) = \sup_{f\in \mathcal{F}} t(\mathbb{E}_{q(z)}[(O^{p, q}f)(z)])

$$

which is the worst case expected value among all the functions in $$\mathcal{F}$$.

For positive valued operators, one can choose KL divergence, $$\alpha$$-divergence, $$\chi$$-divergence.

For real valued operators, the operators leads to Stein divergence as:

$$

D_{\mathrm{stein}}(p, q) = \sup_{f} \lvert \mathbb{E}_{q(z)}[f(z)] - \mathbb{E}_{p(z\lvert x)}[f(z)]\lvert 

$$

The authors apply the Langevin-Stein operator 

$$

\mathcal{L}(q; O^{p, q}_{LS}, \mathcal{F}) = \sup_{f\in \mathcal{F}} (\mathbb{E}_{q(z)}[\nabla_z \log p(x, z)^\top f(z) + \nabla^\top f])^2

$$

Interestingly, the LS operator does not require the analytical form of $$q(z)$$ - only samples are needed. (which is an issue in energy based models)

### Operator Variational Inference

OPVI seeks to solve a minimax problem:

$$

\lambda^* = \inf_{\lambda}\sup_{\theta} t(\mathbb{E}_\lambda[(O^{p, q}f_\theta)(z)])

$$

which looks strikingly similar to the objective for energy based GAN, in terms of the order of min and max.



## Strategic Attentive Writer for Learning Macro-Actions

Assumption for the problem: one observation reveals enough information for further actions.

Latent representation $$z_t$$. Action plan: $$A_t$$, Commitment plan $$c_t$$, attention parameters $$\psi_t^A$$, state of action plan $$\beta_t$$, intermediate representation $$\xi_t$$.

$$

\psi_t^A = f^\psi(z_t) \\
\beta_t = read(A_{t-1}, \psi_t^A) \\
\xi_t = h([\beta_t, z_t]) \\
A_t = \rho(A_{t-1}) + g_t \cdot write(f^A({\xi_t}), \psi_t^A)

$$

Refer to the DRAW paper for attention models.

The training loss is defined as:

1. Domain specific loss defined over the network output.
2. $$1_{g_t} \alpha KL(Q(z_t \lvert  \phi(x_t)) \lVert P(z_t))$$, which defines a structured exploration.
3. $$\lambda c_t[t]$$ which encourages commitment.

## Learning to Draw Samples: With Application to Amortized MLE for Generative Adversarial Modeling

### Stein Variational Gradient Descent

SVGD initalizes the particles by sampling from som simple distribution $$q_0$$ and updates the particles iteratively by 

$$

x_i \leftarrow x_i + \epsilon \phi(x_i)

$$

$$\phi(x)$$ is a "particle gradient direction function" chosen to maximumly decrease the KL divergence between the distribution of particles and the target distribution.

$$

\phi = \arg \max_{\phi \in \mathcal{F}} \{- \frac{d}{d\epsilon} KL(q_[\epsilon \phi] \lVert p) \lvert _ {\epsilon=0} \}

$$

$$\mathcal{F}$$ is chosen as the unit ball of a vector-valued RKHS.

The Kernelized Stein discrepancy is:

$$

\mathbb{D}(q \lVert p) = \max_{\phi \in \mathcal{H}^D} \{ \mathbb{E}q[\mathcal{T}_p\phi(x)] \  \ \lvert  \ \ \lVert \phi \lVert_{\mathcal{H}^d} \leq 1 \}

$$

where $$\mathcal{T}_p \phi(x) = \nabla_x \log p(x)^\top \phi(x) + \nabla_x \phi(x)$$, and the optimal solution of this is

$$

\phi^*(x') \propto \mathbb{E}_{x \sim q}[\nabla_x \log p(x)k(x, x') + \nabla_x k(x, x')]

$$

By approximating the expectation under $$q$$ with the empirical average of the current particles, SVGD admits a sample form of update:

$$

x_i \leftarrow x_i + \epsilon \Delta x_i

$$

where $$\Delta x_i = \mathbb{E}_{x\in\{x_i\}_{i=1}^n}[\nabla_x \log p(x) k(x, x_i) + \nabla_x k(x, x_i)]$$

The first term drives the particles toward high probability regions, and the second term serve as a repulsive force to encourage diversity.

Notice when $$n=1$$, this reduces to maximizing $$\log p(x)$$.

### Amortized SVGD

SVGD may be inefficient, so on way to do this is to train a neural network $$f(\eta; \xi)$$ to mimic the SVGD dynamics, where $$\eta$$ is the network parameters, and $$\xi$$ is the input.

Each iteration, a batch of input is drawn and calculated. The Stein variational gradient $$\Delta x$$ would ensure that $$x_i^\prime = x_i + \epsilon \Delta x_i$$ forms a better approximation of the target distribution p. Therefore, $$\eta$$ shoudl be adjusted to match $$x_i^\prime$$ by minimizing the L2 loss. In practice this can be performed over only one gradient step

$$

\eta^{t+1} \leftarrow \eta^t + \epsilon \sum_{i=1}^{m} \partial_\eta f(\eta^t, \xi_i) \Delta x_i

$$

This is also related to the reparametrization trick.

### Amortized MLE for GAN

Energy based model as discriminator $$p(x\lvert \theta)$$, $$f(\eta; \xi)$$ is a generator that tries to fit the generative process of discriminative model.



## RL^2: Fast Reinforcement Learning via Slow Reinforcement Learning

Set the reward as the objective of a reinforcement learning objective.



## Value Iteration Network



## Hierarchical Deep Reinforcement Learning: Integrating Temporal Abstraction and Intrinsic Movivation

Introduces a meta controller, which provides a policy over goals. The meta controller interacts with the extrinsic reward.

The controller produce a policy over actions, which tries to minimize the intrinsic reward (given by the meta controller).

