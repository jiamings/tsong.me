---
layout: post
title: Towards Deeper Understanding of Variational Autoendoding Models
author: Jiaming Song and Shengjia Zhao
tags:

---



> TLDR: We propose a new way of viewing variational autoencoders, that allows us to explain many existing problems in VAE, such as fuzzy generation and low usage of latent code. Based on these observations, we are able to propose new models that are simple yet highly effective.



Variational Autoencoders (VAEs) {% cite kingma2013auto %} is a interesting family of generative models, and has received much attention since its emergence [^vae]. However, with the advent of the "violent" Generative Adversarial Networks (GANs) {% cite goodfellow2014generative %} [^ gun], VAEs seems to fall out of favor for a bit [^gan]. 

Intuitively, GAN seems to generate sharper samples than VAE does, and although GANs are hard to train, advances such as DCGAN {% cite radford2015unsupervised %} and WGAN {% cite arjovsky2017wasserstein %} has improved the quality of GANs significantly. 



#### References

{% bibliography --cited %}



#### Footnotes

[^ gun]: A recent inspiring work titled "Generative Unadversarial Networks" (GUNs) provides a thoughtful discussion on the violence of GANs.
[^vae]: As of Pi day 2017, VAE receives 637 citations.
[^gan]: Since 2017, VAE has received 68 citations while GAN has received 93 citations.

