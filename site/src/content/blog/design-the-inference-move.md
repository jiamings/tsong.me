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

This note is about three points.

First, the usual split is a false dichotomy. Autoregressive and diffusion
methods can coexist in the same generative system, because the labels mix
together several different choices: representation, training objective, and
inference procedure.

Second, flow maps point to a better way to build fast continuous-domain
generators. If the sampler needs to make a large jump, the model should be given
the information needed to learn that jump directly.

Third, the same idea may matter for language models. Rather than assuming LLMs
must stay in the usual discrete-token, left-to-right form, we should ask whether
continuous states, refinement steps, or flow-like updates can give language
models a useful form of inference-time scaling.

## Two kinds of motion

The false dichotomy becomes easier to see from a simple observation: at
inference time, extra compute usually buys one of two things.

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

## Well-specified inference

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

## Why flow maps are good

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

Flow maps are the clean version of this idea. Instead of asking a model to learn
only an infinitesimal direction and then hoping that numerical integration will
make it fast, a flow-map model is asked to learn a finite move between two
times. If the goal is few-step generation, that is a better match between the
thing we train and the thing we ask the model to do at inference time.

This is the second point in concrete form. Before training, ask whether the
sampler has the right arguments. If a model is expected to jump to a target time,
then the target time should be part of the inference map. Otherwise the training
objective is trying to repair a sampler that was underspecified from the start.

## Why consider this for LLMs

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

This also changes how I think about diffusion and flow methods for language.
They should not be dismissed just because language is usually represented with
discrete tokens, and they should not be accepted just because they carry the word
"diffusion." The question is more specific: what is the state space, and what
parallel or refinement move is the sampler actually allowed to make?

Masked diffusion language models, block diffusion models, continuous diffusion
over categorical data, and flow-map language models answer that question in
different ways. Some operate over discrete masked tokens. Some generate blocks
autoregressively and refine inside each block. Some move the language problem
into a continuous space and learn refinement or flow-like updates there. These
are not the same algorithm with different branding. But they share a common
inference design problem: how to get the latency benefits of parallelism or
few-step refinement without silently dropping the dependencies that make
language coherent.

Continuous-domain language models are especially interesting from this angle
because they make the false dichotomy harder to maintain. A language model can
use continuous states. A diffusion or flow model can be applied to text-like
objects. But the important part is not the label. It is whether the chosen state
space and update map make the intended inference procedure well specified.

## What this suggests

I do not think the future of generative modeling is going to be a clean victory
for one historical family over another.

Autoregressive models gave us a robust way to scale by making sequences longer.
Diffusion models gave us a robust way to scale by revising many parts of a state
in parallel. Frontier systems probably need both kinds of motion, and they will
probably use them in combinations that look awkward if we insist on the old
taxonomy.

Flow maps make the continuous-domain implication clear: if we want fewer, larger
refinement steps, we should train objects that can represent fewer, larger
refinement steps. Continuous-domain language models pose the same question in a
different state space: if we want text generation to benefit from refinement or
parallel updates, we have to specify the dependencies those updates must
preserve.

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
