---
title: Inference-Time Scaling for Generative Pre-Training
description: A short note on the false dichotomy between autoregression and diffusion, why flow maps help, and what this might mean for language models.
pubDate: 2026-05-31
tags: ["generative models", "inference-time scaling", "diffusion"]
draft: true
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
refining an existing state. Many useful systems can do both. Diffusion Forcing,
for example, can generate a sequence over time while also denoising parts of the
sequence. Block Diffusion generates blocks autoregressively but refines tokens
inside each block. Diffusion via Autoregressive Models recasts a visual
diffusion process into a next-token prediction problem.

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

This exposes a simple mismatch in DDIM-style samplers. The sampler may be trying
to move from a current time `t` to a target time `s`, but the network producing
the update may only see the current state and current time. It is being asked to
land at `s` without being told which `s` it is aiming for.

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

That is why flow maps, shortcut models, consistency-style methods, mean flows,
and few-step distillation methods feel connected even when their losses and
training recipes differ. They all move in the same direction: make long-range
updates belong to the model class, instead of hoping that a model trained for
local updates will automatically become a good few-step sampler.

There is still a tradeoff. A flow map is harder to learn than a local direction.
It has to represent a larger move. But that difficulty is at least placed in the
right part of the problem. If the product we want at inference time is a large
move, then training should expose and supervise that large move directly.

This is the broader lesson: before designing the training objective, check
whether the inference procedure is well specified. Does the sampler see the
variables it needs? Does its parameterization contain the update it will be
asked to perform? If not, training is being asked to compensate for a missing
piece of the algorithm.

## Why consider this for LLMs

The language-modeling version of this issue shows up in a different form.

Multi-token prediction is attractive because left-to-right decoding is slow. If
a model could predict several future tokens at once, we might get lower latency
and better use of parallel hardware.

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

This is not a failure of vocabulary. It is a failure of inference design. The
sampler removed a dependency that the output needed.

There are many ways to repair this: verification, rejection, iterative
refinement, dependency prediction, blockwise sampling, or a more direct joint
parameterization. The important point is that the dependency has to live
somewhere in the inference procedure. It cannot be wished into existence by
calling the objective "multi-token."

This is also why I think diffusion and flow-style ideas for language should be
taken seriously, but carefully. The point is not that text should simply copy
image diffusion. The point is that language generation might also benefit from
inference procedures that refine, revise, or move several variables together.

Continuous-domain language models are especially useful for thinking through the
false dichotomy. They separate the question of language from the question of
discrete left-to-right decoding. If a language model lives in a continuous state
space, then ideas from diffusion and flow matching become available in a more
direct way. The hard part is then to preserve the dependencies that make
language coherent while gaining the parallelism or refinement behavior that
continuous methods make possible.

That is the interesting possibility: not replacing autoregressive LLMs because
they are "old," but asking whether some parts of language generation could use a
different inference axis.

## What to check first

The practical takeaway is simple: look at the sampler before arguing about the
loss.

For a new generative pre-training algorithm, I would ask:

- Does inference scale by making the object longer, refining the current object,
  or both?
- If the sampler takes a large step, does the model get the variables needed to
  specify where that step should land?
- If several variables are generated together, does the sampler represent their
  dependencies?
- If the method uses a continuous state for language, what structure keeps the
  result coherent after refinement or parallel decoding?

These questions do not replace scaling laws, architectures, or empirical
validation. They are a sanity check. A training objective can make a model good
at an inference procedure. It cannot fully repair an inference procedure that is
missing the move it is supposed to make.

The old categories will probably keep being useful shorthand. But the more
important design question is becoming clearer: what inference behavior do we
want, and have we actually given the model a way to learn it?

## Related reading

Sander Dieleman's posts on diffusion are good examples of writing that starts
from a conceptual mismatch and slowly sharpens it into a model. In particular,
["Perspectives on diffusion"](https://sander.ai/2023/07/20/perspectives.html),
["Diffusion language models"](https://sander.ai/2023/01/09/diffusion-language.html),
and ["Flow maps"](https://sander.ai/2026/05/06/flow-maps.html) are useful
background for the diffusion side of this discussion.

For a broader research context around multimodal generative modeling, Ruiqi
Gao's [research page](https://ruiqigao.github.io/) and diffusion-related work
are also useful reference points.
