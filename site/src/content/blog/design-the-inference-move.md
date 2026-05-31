---
title: Design the Inference Move First
description: Why autoregressive and diffusion models are less opposed than they look, and why future generative algorithms should start from the sampler.
pubDate: 2026-05-31
tags: ["generative models", "inference-time scaling", "diffusion"]
draft: true
---

There is a familiar story about modern generative models:

- language models are autoregressive;
- image and video models are diffusion-based;
- discrete things want next-token prediction;
- continuous things want denoising.

This story is useful historically, but I think it hides the more interesting
algorithmic question.

The real question is not whether a model is "autoregressive" or "diffusion."
The real question is:

> What kind of inference move is the model being asked to make?

Once you ask the question this way, a lot of otherwise separate ideas start to
look connected.

## Two ways to spend more compute

At inference time, a generative model can usually spend extra compute in one of
two ways.

The first way is **sequence expansion**: make the object longer. A language
model writes more tokens. A reasoning model writes a longer chain of thought. A
visual model may generate tokens, patches, frames, or blocks one piece at a
time.

The second way is **state refinement**: keep the object the same size, but revise
it. A diffusion model starts from noise and repeatedly improves the current
sample. A masked language model fills in missing pieces. A denoising video model
may keep revising the same latent sequence until it becomes coherent.

Autoregressive models are the most familiar example of sequence expansion.
Diffusion models are the most familiar example of state refinement. But those
are examples, not laws of nature.

A model can expand sequences. It can refine states. It can also do both.

## The false dichotomy

People often talk as if autoregressive models and diffusion models are two
opposing paradigms. I think this is the wrong abstraction.

Autoregression is an inference procedure: sample a conditional distribution,
append a variable, and repeat. This procedure is useful because each new token is
sampled from a normalized distribution conditioned on the prefix so far.

Diffusion is a refinement procedure: start from a corrupted state and repeatedly
update it toward something data-like. This procedure is useful because many
parts of the object can be revised in parallel.

These two ideas are not mutually exclusive. You can generate blocks
autoregressively and refine inside each block. You can denoise a whole sequence
while still using an ordering. You can even ask whether language models should
learn more state-refinement behavior, or whether visual models should use more
sequence-expansion behavior.

The more meaningful contrast is usually this:

- discrete tokens trained with cross-entropy;
- continuous tokens or states trained with diffusion-style objectives.

That is a difference in representation and objective, not a hard boundary
between possible inference algorithms.

## Why inference should come before training

Here is the principle I find most useful:

> Before designing the training objective, check whether the inference procedure
> can represent the move you want the model to make.

This sounds obvious, but it is easy to violate.

If the sampler omits an input it needs, no clever loss function can fully fix the
problem. If the sampler assumes two variables are independent when they are not,
training can only learn around the misspecification. The limitation lives in the
inference map, not merely in the objective.

Two examples make this concrete.

## Example 1: a missing argument in DDIM-style sampling

In a DDIM-style sampler, we often want to jump from a current noise level or time
`t` to a target time `s`. The usual velocity or denoising network sees the
current state and the current time. But in many formulations, it does not
directly see the target time.

That creates a strange situation: the sampler is being asked to land at `s`, but
the network producing the update is not told which `s` it is aiming for.

For small solver steps, this can be acceptable. For one-step or few-step
generation, it becomes a capacity issue. A model cannot learn arbitrary long
jumps to different target times if the target time is not part of the input.

The fix is conceptually simple: expose the target time to the model. Instead of
learning only a local velocity field, learn a two-time map: where should this
state at time `t` go if the target is time `s`?

This is one way to understand why recent flow-map, shortcut, consistency, and
few-step distillation methods feel like they are moving in the same direction.
They are trying to make long inference moves belong to the model class, rather
than hoping that a model trained for local moves will magically become a good
few-step sampler.

## Example 2: multi-token prediction is not automatically joint prediction

Multi-token prediction is attractive because it promises lower latency. Instead
of predicting one token at a time, predict several future tokens in parallel.

But there is a trap: predicting the marginal distribution of each future token is
not the same as predicting their joint distribution.

Imagine the prompt:

> Examples of two-word poker hands include: ...

Valid completions include "high card," "two pair," "full house," and "straight
flush." The first word and the second word are correlated. If a model samples the
two positions independently, it might produce something like "high house."

Each word looked plausible on its own. The pair was invalid.

This is the multi-token version of the same inference-first lesson. If the
inference procedure samples positions independently, it has assumed away the
dependency structure that matters. The training objective can improve the
marginals, but it cannot turn an independent sampler into a fully expressive
joint sampler by wishful thinking.

To make parallel decoding work well, the inference algorithm has to account for
dependencies among the tokens being decoded together. That can happen through
verification, rejection, iterative refinement, dependency prediction, or a better
joint parameterization. But the dependency problem has to appear somewhere in the
inference design.

## The emerging pattern

Many recent generative modeling ideas can be read as attempts to make inference
moves more explicit.

Flow maps learn long-range transport maps instead of only local vector fields.
Shortcut models condition on the desired step size. Mean-flow and few-step
distillation methods try to make large jumps directly learnable. Blockwise and
hybrid language/image models combine sequence expansion with local refinement.
Diffusion language models explore whether text generation can benefit from more
state revision rather than pure left-to-right expansion.

These methods differ in training objective, architecture, and domain. But they
share a common shape: they are not merely asking, "What loss should we train
with?" They are asking, "What update should the model be able to perform at
inference time?"

That is the right question.

## A useful design checklist

For a new generative pre-training algorithm, I would start with three questions.

First: does inference scale by making the object longer, by refining the current
object, or by doing both?

Second: if we reduce the number of inference steps, is the model still asked to
make a move that belongs to its parameterization?

Third: does the sampler represent the dependencies it needs to represent, or has
it silently factorized them away?

Only after these questions are answered does it make sense to argue about the
training objective.

## The punchline

The next generation of generative algorithms may not fit cleanly into the old
categories of "autoregressive" and "diffusion." That is probably a good thing.

Autoregression gave us a reliable way to scale by expanding sequences. Diffusion
gave us a reliable way to scale by refining states. Future systems may need both
abilities, and they may need them in forms that look different from today's
standard recipes.

The important thing is to design the inference move first.

Training should teach the model to make that move well. It should not be asked
to compensate for an inference procedure that was missing the move in the first
place.
