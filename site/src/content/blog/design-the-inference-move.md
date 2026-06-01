---
title: Inference-Time Scaling for Generative Pre-Training
description: A short note on the false dichotomy between autoregression and diffusion, why flow maps help, and what this might mean for language models.
pubDate: 2026-05-31
tags: ["generative models", "inference-time scaling", "diffusion"]
---

A common way to describe modern generative models is to split them into two
families: autoregressive models for language, and diffusion models for images
and videos.

This note is about three points.

First, the usual split is a false dichotomy. Autoregressive and diffusion
methods can coexist in the same generative system. The split makes it sound as
if we are choosing between two fixed packages, when in practice the pieces can
be recombined.

Second, flow maps point to a better way to build fast continuous-domain
generators. If the sampler needs to make a large jump, the model should be given
the information needed to learn that jump directly.

Third, the same idea may matter for language models. Rather than assuming LLMs
must stay in the usual discrete-token, left-to-right form, we should ask whether
continuous states, refinement steps, or flow-like updates can give language
models a useful form of inference-time scaling.

This is a shorter, less technical version of the argument. For the longer
technical write-up, see
[Inference-Time Scaling for Generative Pre-Training](https://arxiv.org/abs/2503.07154).

## The false dichotomy

The autoregressive/diffusion split is useful historically, but it bundles
together things that do not have to stay bundled.

Autoregressive models are usually discussed in the context of discrete tokens
and next-token prediction. Diffusion models are usually discussed in the context
of continuous signals and denoising objectives. This pairing is so common that
it can start to look inevitable: language is autoregressive; images and videos
are diffusion.

I do not think that is the right abstraction. The sharper question is how a
method spends inference compute, not whether it belongs to the autoregressive or
diffusion tribe.

Some methods spend compute by expanding a sequence. Others spend compute by
refining an existing state. Many useful systems can do both.
[Diffusion Forcing](https://arxiv.org/abs/2407.01392), for example, can generate
a sequence over time while also denoising parts of the sequence.
[Block Diffusion](https://arxiv.org/abs/2503.09573) generates blocks
autoregressively but refines tokens inside each block.
[Diffusion via Autoregressive Models](https://arxiv.org/abs/2505.23660) recasts
a visual diffusion process into a next-token prediction problem.

These examples are hard to describe cleanly if "autoregressive" and "diffusion"
are treated as mutually exclusive families. They are easier to understand as
different ways of organizing inference compute: when to extend the object, when
to revise the current state, and how much work each step should do. That is
where flow maps become interesting.

## Why flow maps are good

Suppose a continuous generator is trained with a local view of time. At a current
time `t`, the model predicts a velocity or denoising direction, and a sampler
uses that direction to take a step. If the step is small, this is a natural
setup. The model only needs to know how to move locally.

But fast generation asks for something harder. If we want one-step or few-step
sampling, the model is no longer being asked for a small local correction. It is
being asked to make a large jump.

This exposes a simple mismatch in
[DDIM-style samplers](https://arxiv.org/abs/2010.02502). The sampler may be
trying to move from a current time `t` to a target time `s`, but the network
producing the update may only see the current state and current time. It is
being asked to land at `s` without being told which `s` it is aiming for.

For small steps, the missing target is not too damaging. For large jumps, it is a
real limitation. The inference map is under-specified: it omits an argument that
matters.

Flow maps are a clean way to remove that mismatch. Instead of learning only an
infinitesimal vector field, a flow-map model learns a two-time map: from this
state at time `t`, where should the sample go if the target is time `s`?

<figure class="imm-flow-figure">
  <div class="imm-flow-media-grid">
    <div class="imm-flow-panel">
      <video autoplay loop muted playsinline preload="metadata" src="https://static.cdn-luma.com/files/blog/imm/DDTI%20FINAL.mp4"></video>
      <figcaption>
        <strong>DDIM-style update.</strong> The sampler wants to jump from a
        current time to a target time, but the network is not directly
        conditioned on the target.
      </figcaption>
    </div>
    <div class="imm-flow-panel">
      <video autoplay loop muted playsinline preload="metadata" src="https://static.cdn-luma.com/files/site/home/IMM%20Exported.mp4"></video>
      <figcaption>
        <strong>Target-time-conditioned update.</strong> Exposing the target
        time gives the model the missing degree of freedom for a finite
        two-time move.
      </figcaption>
    </div>
  </div>
  <figcaption class="imm-flow-source">
    Animations from Luma AI's
    <a href="https://lumalabs.ai/news/inductive-moment-matching">Inductive Moment Matching</a>
    post.
  </figcaption>
</figure>

This is not just a trick for conditioning on one more scalar. It changes the
object being learned. A local velocity field is the right object if inference
will use many tiny steps. A two-time map is a more natural object if inference
needs a small number of large steps.

That is why [flow maps](https://arxiv.org/abs/2406.07507),
[shortcut models](https://arxiv.org/abs/2410.12557),
consistency-style methods, [mean flows](https://arxiv.org/abs/2505.13447), and
few-step distillation methods feel connected even when their losses and training
recipes differ. They all move in the same direction: make long-range updates
belong to the model class, instead of hoping that a model trained for local
updates will automatically become a good few-step sampler.

## Why consider this for LLMs

The language-modeling version of this issue shows up in a different form.

[Multi-token prediction](https://arxiv.org/abs/2404.19737) is attractive
because left-to-right decoding is slow. If a model could predict several future
tokens at once, we might get lower latency and better use of parallel hardware.

But predicting several token marginals is not the same as predicting their joint
distribution.

Suppose the prompt asks for examples of two-word poker hands. Valid answers
include "high card," "two pair," "full house," and "straight flush." The first
word and the second word are correlated. If a sampler predicts the two positions
independently, each word can look plausible on its own while the pair is invalid.
You can get something like "high house."

<figure class="blog-figure">
  <img
    src="/assets/blog/mtp-poker-gpt-image.png"
    alt="A comparison of a joint distribution over valid two-word poker hands and independent sampling heads that can produce invalid combinations such as high house."
  />
  <figcaption>
    A two-token poker-hand example. Valid two-word hands are correlated; sampling
    the two positions independently can mix good marginals into an invalid pair.
  </figcaption>
</figure>

The issue is the independence assumption in the inference process. Current
multi-token prediction methods often produce softmax distributions for multiple
future positions in parallel, and then sample from those positions independently.
This can be useful as part of a larger decoding system, but by itself it does
not represent the joint distribution over the tokens being decoded together.

Existing systems often work around this limitation with verification,
self-speculative decoding, rejection, or by falling back to ordinary next-token
prediction at inference time, as in the
[DeepSeek-V3 technical report](https://arxiv.org/abs/2412.19437). Those
workarounds can be practical, but they also make the capacity issue visible: the
inference procedure itself did not directly model the dependency among the
tokens.

Continuous-domain language models are especially useful for thinking through the
false dichotomy. They separate the question of language from the question of
discrete left-to-right decoding. If a language model lives in a continuous state
space, then ideas from diffusion and flow matching become available in a more
direct way.

Recent examples include
[Continuous Diffusion for Categorical Data](https://arxiv.org/abs/2211.15089),
[Flow Map Language Models](https://arxiv.org/abs/2602.16813),
[CoDAR](https://arxiv.org/abs/2603.02547),
[LangFlow](https://arxiv.org/abs/2604.11748),
[ELF](https://arxiv.org/abs/2605.10938), and
[FlowLM](https://arxiv.org/abs/2605.20199). Their inference procedures are quite
similar: they use continuous refinement before returning to discrete text. They
differ in where they place the continuous state, how they map back to tokens,
and whether they learn diffusion, flow matching, or a flow-map-like few-step
sampler. One of the remaining challenges is whether continuous refinement can
give a proper validation perplexity, not only a useful sampler.

## Related reading

- [Denoising Diffusion Implicit Models](https://arxiv.org/abs/2010.02502)
- [Diffusion Forcing](https://arxiv.org/abs/2407.01392)
- [Block Diffusion](https://arxiv.org/abs/2503.09573)
- [Diffusion via Autoregressive Models](https://arxiv.org/abs/2505.23660)
- [Flow Map Matching](https://arxiv.org/abs/2406.07507)
- [One Step Diffusion via Shortcut Models](https://arxiv.org/abs/2410.12557)
- [Mean Flows for One-Step Generative Modeling](https://arxiv.org/abs/2505.13447)
- [Better & Faster Large Language Models via Multi-token Prediction](https://arxiv.org/abs/2404.19737)
- [Continuous Diffusion for Categorical Data](https://arxiv.org/abs/2211.15089)
- [Flow Map Language Models](https://arxiv.org/abs/2602.16813)
- [CoDAR: Continuous Diffusion Language Models are More Powerful Than You Think](https://arxiv.org/abs/2603.02547)
- [LangFlow](https://arxiv.org/abs/2604.11748)
- [ELF: Embedded Language Flows](https://arxiv.org/abs/2605.10938)
- [FlowLM: Few-Step Language Modeling via Diffusion-to-Flow Adaptation](https://arxiv.org/abs/2605.20199)
- Sander Dieleman's ["Flow maps"](https://sander.ai/2026/05/06/flow-maps.html),
  ["Perspectives on diffusion"](https://sander.ai/2023/07/20/perspectives.html),
  and ["Diffusion language models"](https://sander.ai/2023/01/09/diffusion-language.html)
