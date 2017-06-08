---
layout: post
title: Learning Hierarchical Features from Generative Models
author: 
tags:
- blog
---

> TLDR: Current ways of stacking variational autoencoders may not always provide meaningful structured features. In fact, we showed in a recent ICML paper that a simple ladder architecture is enough for us to learn structured, distentangled features from variational autoencoders.

Variational Autoencoders (VAE) {% cite kingma2013auto %} has been one of the most popular frameworks for deep generative models. It defines a model $$p(x \lvert z)$$ that generates data $$x$$ given the latent variables $$z$$, where we can treat $$z$$ as some sort of "feature" and perform semi-supervised learning {% cite kingma2014semi %}. 



### Deeper is not Always Better for Hierarchical VAEs

For some time, researchers have proposed to use "hierarchical VAEs":




$$
p(x \lvert z) = p(x|z_1)\prod_{\ell = 1}^{L-1} p(z_\ell | z_{\ell+1})
$$


There are two potential advantages to using such hierarchical VAEs:

1. It could improve the ELBO bounds and decrease reconstruction error in most cases, which would look nicely in a paper. 
2. The stack of latent variables $$z_\ell$$ might learn a "feature hierarchy", similar to what convolutional neural networks learned.

The first has been validated by many recent works and hierarchical VAEs would help improving ELBO bounds on paper [^likelihood]. The second argument, however, has not been clearly demonstrated[^hierarchy]. In fact, it is difficult to learn a meaningful hierarchy when there are many layers of $$z$$, and some have considered that as an inference problem {% cite sonderby2016ladder %}. 

### A Simple yet Effective Method for Learning Hierarchical Features

We show in our recent ICML paper, [Learning Hierarchical Features from Generative Models](https://arxiv.org/abs/1702.08396), that if the purpose is to learn structured, hierarchical features, using an hierarchical VAE has its problems. Instead, we can use a very simple approach, which we call Variational Ladder Autoencoder (VLAE) [^vlae]. 

The basic idea is simple: *if there is a hiearchy of features, some complex and some simple, they should be expressed by neural networks of different capacity*. Hence, we should use shallow networks to express low-level, simple features and deep networks to express high-level, complex features. One way to do this is to use an implicit generative model [^implicit], where we inject Gaussian noise at different levels of the network:

<div class="row">

<div class="col-lg-4 col-lg-offset-4">

<img src="{{ site.baseurl }}/public/img/blog/vlae.png">

</div>

</div>



Training is essentially the same for 1 layer VAE with $$L_2$$ reconstruction error. We show some results from SVHN and CelebA: the models have 4 layers of $$z$$ and in each block we display the generation results when we change the $$z$$ in one layer and fix that in other layers (from left to right, lower layers to higher layers):

![]({{ site.baseurl }}/public/img/blog/vlae_svhn.png)

![]({{ site.baseurl }}/public/img/blog/vlae_celeba.png)

We can see that lower layers learned simpler features such as the image color, while higher layers learned more complex attributes such as the overall structure. This clearly demonstrates that this VLAE is able to learn hierarchical features, similar to what InfoGAN {% cite chen2016infogan %} does.



Code is available at: [https://github.com/ermongroup/Variational-Ladder-Autoencoder](https://github.com/ermongroup/Variational-Ladder-Autoencoder).



### Conclusion

In terms of learning hierarchical features, deep is not always good for VAEs; if we use a ladder architecture that serves as an inductive bias for the complexity of features, then we can learn structured features at ease.







#### References

{% bibliography --cited %}

#### Footnotes

[^likelihood]: Although ELBO bounds and log-likelihood in general are not necessarily good measurements for generative models {% cite theis2015note %}.
[^hierarchy]: Except for in {% cite gulrajani2016pixelvae %}, where PixelCNN is used to model $$p$$.
[^vlae]: Coming up with a good name for this model is so difficult, because of existing works.
[^implicit]: {% cite tran2017deep %} has mentioned a model with similar architecture, but the motivation is different from ours (they focus on learning and inference with GANs while we focus on learning hierarchical features).

