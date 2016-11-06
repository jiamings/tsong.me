---
layout: post
title: Video Classification with Deep Features
author: Jiaming Song and Yankai Zhang
tags:
  - projects
permalink: /projects/decaf-video/
---

### Abstract

This project aims to do fast and scalable video sequence classification through feature extraction methods.

We extract features from image frames as well as audio information.

{: .row}
![-border]({{ site.baseurl }}/public/img/projects/decaf-video/overview.png){: .col-lg-5 .col-lg-offset-1}
![-border]({{ site.baseurl }}/public/img/projects/decaf-video/philosophy.png){: .col-lg-5 }

### Methods

The image features are extracted according to novel methods
from this paper
[DeCAF: A Deep Convolutional Activation Feature for Generic Visual Recognition](http://arxiv.org/pdf/1310.1531v1.pdf),
which uses a deep convolutional neural net trained on ImageNet dataset for feature extraction;
the audio features are extracted using MFCC/LPCC.

We extract visual features by configuring [Caffe](http://caffe.berkeleyvision.org/)
on a Thinkpad T430 laptop, use a pretrained
[AlexNet](http://www.cs.toronto.edu/~fritz/absps/imagenet.pdf), and extract a layer of
responses for each image.

{: .row}
![]({{ site.baseurl }}/public/img/projects/decaf-video/validation-test.png){: .col-lg-5 .col-lg-offset-1}
![]({{ site.baseurl }}/public/img/projects/decaf-video/add-audio.png){: .col-lg-5 }

### Results
We collect a dataset with 5 classes, and train the features with an linear SVM. We discover that:

- Features from neural networks provides better performance than traditional hand-crafted features.
- Combining audio and image features provides better performance than using image features alone.

For more details, please refer to [our slides]({{ site.baseurl }}/static/slides/decaf_video_slides.pdf).