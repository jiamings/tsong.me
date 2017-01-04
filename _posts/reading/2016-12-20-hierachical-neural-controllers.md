---
layout: post
title: Communicating Hierarchical Neural Controllers for Learning Zero-shot Task Generalization
author: Jiaming Song
tags:
- reading
---



## Communicating Hierarchical Neural Controllers for Learning Zero-shot Task Generalization

[https://openreview.net/pdf?id=SJttqw5ge](https://openreview.net/pdf?id=SJttqw5ge)



The model consists of two modules, which is popular in the current hierarchical RL literature:

1. A meta controller that reads instructions and repeatedly communicates subtasks to a subtask controller 


2. The subtask controller that in turn learns to perform such subtasks

### Subtask Controller

The subtask controller takes an input $$x$$ and subtask arguments $$g$$ and provides an output $$y$$ through a layer, either convolutional or fully connected:



$$
y = \phi(g) * x + b \quad \mbox{or} \quad y = W^\prime \mbox{diag}(\phi(g)) Wx + b
$$

Given the observation $$s_t$$ and subtask $$g$$, the controller is defined as



$$
\pi(a_t \lvert s_t, g) \propto \exp(\phi^\pi (\mbox{CNN}(s_t; g))) \\
\beta(b_t \lvert s_t, g) \propto \sigma (\phi^\beta (\mbox{CNN}(s_t; g)))
$$


where $$\phi^\pi$$ and $$\phi_\beta$$ are MLPs.

### Meta Contoller

Given the sentence embedding $$r_{t-1}$$ received at the previous time-step, the previously selected subtask $$g_{t-1}$$ and the subtask termination $$b_t$$, the meta-controller computes the context vector $$h_t$$ through $$h_t = \mbox{CNN}(s_t; r_{t-1}, g_{t-1}, b_t)$$.

The context vector is used to determine the next instruction and the subtask to communicate.

### Subtask Updater

The subtask updater constructs a memory structure form the list of instructions, retrieves an instruction by maintaining a pointer into the memory and computes the subtask arguments.

Memory: $$M = [\phi^w(m_1), \ldots, \phi^w(m_k)]$$, retrieval $$r_t = Mp_t$$

Location based Addressing: $$p_t = I_t * p_{t-1}$$ where $$I_t \sim Softmax(\phi^{shift}(h_t))$$

Subtask arguments:



$$
\pi(g_t \lvert h_t, r_t) = \prod_i \pi(g_t^{(i)} \lvert h_t, r_t), \mbox{where} \ \pi(g_t^{(i)} \lvert h_t, r_t) \propto \exp(\phi_i^{goal}(h_t, r_t))
$$


The architechure is as follows:

![]({{site.baseurl}}/public/img/reading/hnc.png)



### Learning

The subtask controller is trained through *policy distillation*, and then fine tuned through actor-critic method. The meta controller is updated through actor-critic method and generalized advantage estimation.

### Analogy Making Regularization

Basically this forces the embedding to make analogies in a word2vec-like style, and is made based on the contrastive loss:



$$
\mathcal{L}_{sim} = \mathbb{E}[\lVert \phi(g_A) - \phi(g_B) - \phi(g_C) + \phi(g_D) \rVert^2] \\
\mathcal{L}_{dis} = \mathbb{E}[\max(0, \tau_{dis} - \lVert \phi(g_A) - \phi(g_B) - \phi(g_C) + \phi(g_D) \rVert)^2] \\
\mathcal{L}_{diff} = \mathbb{E}[\max(0, \tau_{diff} - \lVert \phi(g_A) - \phi(g_B) \rVert)^2]
$$
