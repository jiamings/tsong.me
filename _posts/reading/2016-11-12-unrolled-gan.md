---
layout: post
title: Unrolled Generative Advesarial Networks
author: Jiaming Song
tags:
- reading
---

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

