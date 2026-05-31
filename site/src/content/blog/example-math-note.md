---
title: Example Math Note
description: A draft post that demonstrates Markdown and math support.
pubDate: 2026-05-31
tags: ["example", "math"]
draft: true
---

This is a draft placeholder for testing the blog pipeline.

Inline math should work, for example $x_t = \alpha_t x_0 + \sigma_t \epsilon$.

Block math should work too:

$$
\nabla_\theta \mathbb{E}_{x \sim p_\theta} [f(x)]
  = \mathbb{E}_{x \sim p_\theta} [f(x) \nabla_\theta \log p_\theta(x)].
$$

Because this post is marked `draft: true`, it will not appear on the public blog
index or build a public route.
