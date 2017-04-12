---
layout: post
title: Towards Deeper Understanding of Variational Autoendoding Models
author: Jiaming Song and Shengjia Zhao
tags:
---



> TLDR: We propose a new way of viewing variational autoencoders, that allows us to explain many existing problems in VAE, such as fuzzy generation and low usage of latent code.



Variational Autoencoders (VAEs) {% cite kingma2013auto %} is a interesting family of generative models, and has received much attention since its emergence. We recently submitted two papers on arXiv that discuss several interesting aspects of VAEs. In one of them ([https://arxiv.org/abs/1702.08658](https://arxiv.org/abs/1702.08658)), we propose a novel interpretation of VAEs that explains several phenomenons, including 

- generation of fuzzy images
- improving sample quality through sequential generation
- under utilization of latent codes

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

The most common $$p(x\vert z)$$ we see are factored Gaussians, which clearly cannot approximate this complex distribution. In fact, this explains the fuzzy generation of VAEs. Given a latent code, the generative network try to fit a subset of data with a Gaussian distribution, where the best fit for the mean is to calculate an average of the subset. If multiple $$x$$ map to the same $$z$$ (which is common since $$q(z \vert x)$$ is also a Gaussian), the Gaussian will try to learn an average of these $$x$$, which leads to fuzzy generation. 

Since $$p(x\vert z)$$ is an approximation of $$q(x\vert z)$$, we can calculate the variance of $$q(x\vert z)$$ for any $$z$$ to measure the "fuzziness" of the generated samples given that particular $$z$$. In the following image, the left digits are generated with low $$q(x\vert z)$$, and thus are sharp; the right digits, however, have high $$q(x\vert z)$$, and hence looks like some average between 5, 4, and 9.



![]({{site.baseurl}}/public/img/blog/fuzzy.png){:.center}



For a weak $$p$$ there is only one solution to alleviate fuzziness - have a better $$q$$. In our paper, we demonstrated that injecting latent codes during iterative generation can result in latent code that have smaller variance, thus creating sharper samples. This is a generalization of the notion of "infusion training" {% cite bordes2017learning %}, where the injected latent code is just a subset of the pixels of the image. Here, we show that we can generate sharp LSUN images using simple Gaussian VAEs.



![]({{site.baseurl}}/public/img/blog/seq_vae_lsun.png){:.center}



Our code for this experiment is available at [https://github.com/ermongroup/Sequential-Variational-Autoencoder](https://github.com/ermongroup/Sequential-Variational-Autoencoder).





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


where $$p_\theta(x) = \mathbb{E}_{p(z)}[p_\theta(x\vert z)]$$, and $$p_\theta(z \vert x)$$ is the true posterior. If $$p_\theta(x\vert z)$$ can be arbitrarily complex, then a trivial solution will make $$L$$ equal to zero:

- For all $$z_i$$, $$p(x \vert z = z_i)$$ is the true data distribution $$p(x)$$.
- For all $$x_i$$, $$q(z\lvert  = x_i) = p_\theta(z \lvert x = x_i) = p(z)$$. Namely, $$z$$ and $$x$$ are independent for both $$p_\theta$$ and $$q$$. 

This is exactly the case discussed in the Variational Lossy Autoencoder paper {% cite chen2016variational %}. 



However, if we are willing to give up the KL divergence term in the prior, the latent code will be utilized, and it is still possible to generate samples through a Markov chain. Here, we illustrate generating samples through a Markov chain, where highly complex models such as PixelCNN++ are utilized.

![]({{site.baseurl}}/public/img/blog/pixel_vae_cifar_mc_noreg.png){:.center}

Our code for this experiment is available at [https://github.com/ermongroup/Generalized-PixelVAE](https://github.com/ermongroup/Generalized-PixelVAE).

### Discussion

Through this work, we aim to promote the following argument: **Learning features should be at least equally important to generating samples in unsupervised learning.**

The view of VAE from the inference side allows us to realize that if we want our features $$z$$ to have some alignment with the real world, then the type of $$p(x \vert z)$$ we utilize should match our inductive bias over that distribution. Since both Gaussian and Recurrent distributions are far from perfect of encoding our inductive bias (as directed by features), this requires us to consider other types of distribution that could reflect that.

This also gives us another intuition. Instead of using a simple generator network and come-up with complex inference distributions (as in many prior works), we can take the opposite direction, where the generator is complex yet the inference is simple. 

Following this work, our second arXiv submission ([https://arxiv.org/abs/1702.08396](https://arxiv.org/abs/1702.08396)) discusses current limitations for hierarchical VAEs, and propose an architecture that is extremely simple yet effective at learning structured features. We will discuss that in another blog post.





#### References

{% bibliography --cited %}