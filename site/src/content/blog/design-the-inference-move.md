---
title: Inference-Time Scaling for Generative Pre-Training
description: A short note on sequence expansion, state refinement, and why the inference procedure should shape the training objective.
pubDate: 2026-05-31
tags: ["generative models", "inference-time scaling", "diffusion"]
draft: true
---

A common way to describe modern generative models is to split them into two
families: autoregressive models for language, and diffusion models for images
and videos.

I think this is a false dichotomy. It treats "autoregressive" and "diffusion" as
if they name two opposing model families, when they are mixing together several
different choices: the data representation, the training objective, and the
procedure used at inference time.

Autoregression is primarily a way to sample: draw from a conditional
distribution, append a new variable, and repeat. Diffusion is primarily a way to
refine: start from a corrupted or simple state, then repeatedly revise it toward
data.

So the question I find more useful is:

> What inference move is the model allowed to make?

This sounds small, but it changes the way I look at a lot of recent work.

## Two kinds of motion

At inference time, extra compute usually buys one of two things.

The first is that the object gets longer. A language model samples a token,
appends it, and repeats. A video model might extend a clip. A reasoning model
might write down more intermediate steps. I will call this sequence expansion.

The second is that the object stays roughly the same size, but the state changes.
A diffusion model starts from noise and revises the whole sample many times. A
masked model fills in or repairs parts of a sequence. A video model might keep
the same latent grid and make it more coherent. I will call this state
refinement.

Autoregressive models are the canonical example of sequence expansion.
Diffusion models are the canonical example of state refinement. But those are
just the familiar cases. There is nothing sacred about the boundary. A model can
expand for a while, refine locally, expand again, verify, revise, and so on.

Once you look at it this way, the familiar AR/diffusion split becomes less like
a boundary between tribes and more like two common inference motions. Those
motions often travel with particular objectives and representations because
history made them travel together. They do not have to.

## The sampler has opinions

It is tempting to think of inference as the boring part that happens after
training. We choose a loss, train a large model, and then the sampler is just how
we run it.

I think this gets the order backwards.

The sampler already contains a set of assumptions. It decides which variables are
available to the model, which dependencies are represented explicitly, which
updates are local, and which updates are supposed to be learned as a single
move. The training objective can make the model good at the move. It cannot
fully rescue an inference procedure that never had the move in its vocabulary.

This is easiest to see in cases where the missing ingredient is almost
embarrassingly concrete.

## A small example from fast diffusion sampling

In a DDIM-style sampler, we often move from a current time `t` to a target time
`s`. For many small steps, it is natural to think in terms of a local velocity or
denoising direction. The network sees the current state and the current time,
and the numerical solver takes care of stepping forward.

But if we want to make very large jumps, or even a single jump, a small mismatch
appears. The sampler is trying to land at `s`, but the network may not be told
which `s` it is aiming for.

For local steps, this can be fine. The target is close enough that the direction
is mostly determined by where you are. For long jumps, it becomes a real
restriction. A model that only sees `(x_t, t)` is being asked to produce updates
for many possible destinations without being told the destination.

One natural fix is to put the destination into the model class. Instead of only
learning a local vector field, learn a two-time map: from this state at time `t`,
where should I go if the target time is `s`?

This is one way to read the recent interest in flow maps, shortcut models,
consistency-style methods, and few-step distillation. They are not just better
losses for the same old sampler. They make larger inference moves explicit.

## A small example from parallel decoding

There is a related issue on the language side.

Multi-token prediction is appealing because one-token-at-a-time decoding is
slow. If a model could predict several future tokens at once, we might get lower
latency and better use of parallel hardware.

But predicting several marginal distributions is not the same as predicting a
joint distribution.

Suppose the prompt asks for examples of two-word poker hands. "High card," "two
pair," "full house," and "straight flush" are valid. If the first position and
second position are sampled independently, each word can look plausible on its
own while the pair is invalid. You can get something like "high house."

The problem is not that the model failed to know English. The problem is that the
inference procedure quietly removed the dependency it needed.

There are many possible repairs: verification, rejection, iterative refinement,
dependency modeling, blockwise sampling with an internal ordering, or some more
direct joint parameterization. The important point is that the dependency has to
live somewhere in the inference algorithm. It cannot be wished into existence by
calling the objective "multi-token."

## What this suggests

I do not think the future of generative modeling is going to be a clean victory
for one historical family over another.

Autoregressive models gave us a robust way to scale by making sequences longer.
Diffusion models gave us a robust way to scale by revising many parts of a state
in parallel. Frontier systems probably need both kinds of motion, and they will
probably use them in combinations that look awkward if we insist on the old
taxonomy.

So when I look at a new pretraining or inference-time scaling idea, I try to ask
a few questions before looking too closely at the loss:

- What variables does the model get to condition on when it makes an update?
- Does extra compute make the sample longer, make the current sample better, or
  both?
- If we reduce the number of steps, is the model still being asked to make a
  move that belongs to its parameterization?
- If several variables are generated together, where is their dependence
  represented?

These questions are not a replacement for likelihoods, architectures, or scaling
laws. They are more like a sanity check. Before training a model to make a move,
make sure the move is actually available.

That is the main point I want to preserve from this note: design the inference
move first. Then train the model to make that move well.

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
