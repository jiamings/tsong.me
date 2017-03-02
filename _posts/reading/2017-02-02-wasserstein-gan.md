---
layout: post
title: Wasserstein GAN
author: Jiaming Song
tags:
- reading
---

## Wasserstein GAN

Paper: [http://arxiv.org/abs/1701.07875](http://arxiv.org/abs/1701.07875)



The regular GAN during the discriminator to approximate the Jenson-Shannon divergence, which has gradient vanishing problem when the generator reaches regions that are clearly defined by the discriminator.

In this paper, the authors proposed to use the discriminator to approximate the Earth-Mover distance (or Wasserstein-1). The EM distance has nicer properties than JS divergence, in that the gradient will not vanish when the generator reaches a region that the discriminator has high conficence over. Therefore, it is suitable for the discriminator to be trained more, without having to worry about the balancing between generator and discriminator.

![]({{site.baseurl}}/public/img/reading/w-gan.png)



The disadvantages is that more iteration is required on the discriminator, as it will be slower to be trained on, making the advantages over original GAN not so obvious. But the point is "eventually" the model will converge to a generator better than the original GAN.



Tensorflow implementation can be found here: [https://github.com/jiamings/wgan](https://github.com/jiamings/wgan)