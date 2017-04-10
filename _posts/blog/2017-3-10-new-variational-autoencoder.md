---
layout: post
title: Towards Deeper Understanding of Variational Autoendoding Models
author: Jiaming Song and Shengjia Zhao
tags:

---



> TLDR: We propose a new way of viewing variational autoencoders, that allows us to explain many existing problems in VAE, such as fuzzy generation and low usage of latent code. Based on these observations, we are able to propose new models that are simple yet highly effective.



Variational Autoencoders (VAEs) {% cite kingma2013auto %} is a interesting family of generative models, and has received much attention since its emergence [^vae]. We recently submitted two papers on arXiv that discuss several interesting aspects of VAEs.

- We propose a novel interpretation of VAEs that explains several phenomenons, including 
  - generation of fuzzy images
  - improving sample quality through sequential generation
  - under utilization of latent codes
- We discuss problems with current hierarchical VAEs, and propose a simple yet effective alternative to learn structured, disentangled features using the VAE framework (Similar to InfoGAN!).

We use the common notation for VAEs. Suppose $$p(x)$$ is the underlying true data distribution, $$p(z)$$ is the prior of the latent code, the generative model is $$p_\theta(x\vert z)$$ and the recognition (or inference) model is $$q_\phi(z \vert x)$$.



### A Novel Interpretation of VAEs

As in representation learning, we assume that the latent variables $$z$$ represent certain features in $$x$$. For example, if we consider face data $$x$$ and glasses features $$z$$, then if $$x$$ is a face with glasses, then $$z$$ will represent "the existence of glasses" (we denote that as $$z_g$$, which is determined by the inference network $$q(z\lvert x)$$. Our observation comes from the following intuitive question:

Suppose we already have $$q(z\vert x)$$, which is a "glasses feature detector". What type of $$p(x\vert z)$$ should we choose to generate the set of "faces with glasses"?

To answer this question, recall that $$\mathbb{E}_{p(x)}\mathbb{E}_{q(z \vert x)}[p(x\lvert z)]$$ is the VAE ELBO bound without the KL divergence term. In the Bayesian framework, we are using $$q(z\vert x)$$ as a variational approximator to the true posterior. However, we can also consider the variational approximation the other way:


$$
\begin{align}\
q(x, z) &= p(x)q(z\lvert x) \\
q(z) &= \mathbb{E}_{x \sim p(x)}[q(z \lvert x)] \\
q(x \lvert z) &= \frac{q(x, z)}{q(z)}
\end{align}
$$
Namely, we are treating the generative network as a variational approximation to the true posterior $$q(x \lvert z)$$, where the likelihood is defined by the recognition network $$q(z \lvert x)$$.

Why is this interpretation necessary? If we consider the "glasses" example, the true posterior $$q(x \vert z = z_g)$$ is going to be the distribution of all the faces with glasses, which is a truly complex distribution, and requires a very complex $$p(x\vert z)$$ to approximate. 



#### Fuzzy Generation / Simple Generative Model

The most common $$p(x\vert z)$$ we see are factored Gaussians, which clearly cannot approximate this complex distribution. 

In fact, this explains the fuzzy generation of VAEs. Given a latent code, the generative network try to fit a subset of data with a Gaussian distribution, where the best fit for the mean is to calculate an average of the subset. If multiple $$x$$ map to the same $$z$$ (which is common since $$q(z \vert x)$$ is also a Gaussian), the Gaussian will try to learn an average of these $$x$$, which leads to fuzzy generation. Since $$p(x\vert z)$$ is an approximation of $$q(x\vert z)$$, we can calculate the variance of $$q(x\vert z)$$ for any $$z$$ to measure the "fuzziness" of the generated samples given that particular $$z$$.



For a weak $$p$$ there is only one solution to alleviate fuzziness - have a better $$q$$. In our paper, we demonstrated that injecting latent codes during iterative generation can result in latent code that have smaller variance, thus creating sharper samples. This is similar to the notion of "infusion training", where the injected latent code is just a subset of the pixels of the image.





#### Underutilization of Latent Code / Complex Generative Model

What if a complex distribution, such as PixelCNN is considered for $$p_\theta(x \vert z)$$?

Let us write the VAE ELBO:


$$
L = \mathbb{E}_{q(x, z)}[\log p(x \vert z)] - \mathbb{E}_{p(x)}[\text{KL}(q(z\vert x) \ \Vert \ p(z)))]
$$
This is equivalent to:


$$
L = -\text{KL}(p(x) \ \Vert p_\theta(x)) - \mathbb{E}_{p(x)}[\text{KL}(q(z\vert x) \ \lVert \ p_\theta(z|x))] \leq 0
$$
where $$p_\theta(x) = \mathbb{E}_{p(z)}[p_\theta(x\vert z)]$$, and $$p_\theta(z|x)$$ is the true posterior. If $$p_\theta(x\vert z)$$ can be arbitrarily complex, then a trivial solution will make $$L$$ equal to zero:

- For all $$z_i$$, $$p(x \vert z = z_i)$$ is the true data distribution $$p(x)$$.
- For all $$x_i$$, $$q(z|x = x_i) = p_\theta(z | x = x_i) = p(z)$$. Namely, $$z$$ and $$x$$ are independent for both $$p_\theta$$ and $$q$$. 

This is exactly the case discussed in the Variational Lossy Autoencoder paper. 



In order to make $$q(z \vert x)$$ meaningful, the 









However, with the advent of the "violent" Generative Adversarial Networks (GANs) {% cite goodfellow2014generative %} [^ gun], VAEs seems to fall out of favor for a bit [^gan]. 

One empirical motivation for GANs is that they to generate sharper samples than VAEs do. 

#### References

{% bibliography --cited %}



#### Footnotes

[^ gun]: A recent inspiring work titled "Generative Unadversarial Networks" (GUNs) provides a thoughtful discussion on the violence of GANs.
[^vae]: As of Pi day 2017, VAE receives 637 citations.
[^gan]: Since 2017, VAE has received 68 citations while GAN has received 93 citations.

