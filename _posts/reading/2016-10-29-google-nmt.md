---
layout: post
title: Google's Neural Machine Translation System
author: Jiaming Song
tags:
- reading
---

## Google's Neural Machine Translation System

Neural Machine Translation is an end-to-end approach for automated translation, with the hope of overcoming many of the weaknesses of conventional phrase-based translation systems. 

The Phrase-Based Machine Translation (PBMT) methods try to break an input sentence into words and phrases to be translated largely independently, whereas Neural Machine Translation (NMT) considers the entire input sentence as a unit of translation. This paper discusses Google's recent work on Neural Machine Translation, which utilizes state-of-the-art training techniques to improve the Google Translation system.

### Architecture

The Google Neural Machine Translation uses Recurrent Neural Networks to directly learn the mapping between sentence in one language to sentence in another language. The overall architecture of the model uses an "encoder - attention - decoder" structure.


![Image]({{ site.baseurl }}/public/img/reading/google-nmt-lstm.png){:.center}

#### Preliminaries

Here are some resources for you to help understand some of the terms.

- [Autoencoders](http://ufldl.stanford.edu/tutorial/unsupervised/Autoencoders/)
- [Recurrent Neural Networks and Long Short-Term Memory](http://colah.github.io/posts/2015-08-Understanding-LSTMs/)
- [Residual Networks](http://kaiminghe.com/icml16tutorial/icml2016_tutorial_deep_residual_networks_kaiminghe.pdf)
- [Neural Attention and Memory](http://www.wildml.com/2016/01/attention-and-memory-in-deep-learning-and-nlp/)

#### Overall Architecture

The overall architecture adopts an "encoder-attention-decoder" architecture. 

- The encoder module encodes the input sequence of length M to M encoding vectors. 
- The decoding module produces a hidden state for the next symbol to be predicted (given the previous symbol and the encoding vectors), which then goes through a softmax layer to generate a probability distribution over candidate output symbols.
- The attention module is responsible for selecting the weights for summation of the encoding vectors at different time steps, such that the encoding vector fed into the decoding module is different at each time step, with the aim of prioritizing attention.

![]({{ site.baseurl }}/public/img/reading/nmt-model-fast.gif){:.center}

#### Encoder

The encoder is an LSTM-RNN of 8 layers with residual connections between layers, but Google did some tweaks to the architecture for better performance (both accuracy and speed).

##### Bidirectional LSTM in the First Layer

The first two layers are bi-directional, which takes both forwards and backwards context into consideration. The only reason why Google did not use bidirectional LSTMs on all the layers is to save computation time using parallelism; we will explain this in detail later.


![]({{ site.baseurl }}/public/img/reading/google-nmt-lstm-bidirectional.png){:.center}

##### Residual Connections Across Layers

Due to the gradient exploing / vanishing problems, simply stacking layers in deep nets are difficult to train. The residual connection targets this problem by transforming the output to the input plus a "residual", which the network learns. In particular, if the input for layer $$i$$ is $$x_{i}$$, then the residual tries to model $$x_{i+1}$$ by

$$
x_{i+1} = x_{i} + f(x_i)
$$

where $$f(x_i)$$ contains the model parameters. This effectively solves the gradient explode / vanish problems because of the "shortcut connection" between the input and output.

![]({{ site.baseurl }}/public/img/reading/google-nmt-res.png){:.center}

#### Decoder

The decoder is also an LSTM-RNN with 8 layers, where the input for each time step is the output for the previous time step (bottom layer) and the attention-weighted encoding vectors. The deocder does not have bidirectional LSTMs among the layers.

### Optimization

Neural Machine Translation methods ususally have the following problems:

**Slow training and inference speed.** This is naturally caused by the large model and large number of parameters. The model has multiple time step and multiple layers, so computing for even one sentence is very expensive.

**Lacks robustness in translating rare words.** Rare words are either not translated or not translated correctly, since the words have low frequency in the training set, and probably have few sentences to train on, resulting to overfitting the limited amount of sentences.

**Fail to completely "cover" the input**. Since there are not direct restrictions posed on completely covering the input, NMT has the tendency to do so.

Google addresses these following problems by the methods discussed below.

#### Data Paralleism and Model Paralleism

Using data parallelsim and model parallelism, the model training and inference speed can be effectively increased.

Data parallelism is straightfoward: the $$n$$ model replicas are trained concurrently using a Downpour SGD algorithm.

Model parallelism takes advantage of the structure of the model - for deep LSTM with a single direction, the $$i$$-th layer can compute with the $$(i+1)$$th layer in parallel, with only a time step ahead. This would be most effective if the input sequence is very long.

However, model paralleism does not directly apply to the decoding structure, since reasonably one need to obtain the prediction at time step $$t$$ to get the input of time step $$t+1$$. The Google people here adopted this hack - use the **bottom layer** of the decoder at step $$t, combined with the encoding vector with attention as the input for LSTM.

#### Quantizable Model and Quantized Inference

Quantizing the model allows for efficient inference, allowing for low latency translation.

To reduce quantization error, the accumulator values are restricted to be between $$[-\delta, \delta]$$, such that quantization can be utilized later.

The weight matrices $$W$$ are represented as a 8-bit integer matrix $$WQ$$. The accumulator values are represented as 16-bit integers representing the range $$[-\delta, \delta]$$.

The softmax logits are restricted between the range $$[-\gamma, \gamma]$$. 

The matrix multiplication are done using 8-bit integer arithmetic, and the summation are done using 16-bit integer arithmetic. Therefore, the quantized solution is quite efficient.

The quantized model does not have degraded performance compared to the original model. In fact the performance gets better, possibly due to the regularization imposed to the network.

#### Beam Search For Maximum Likelihood

Beam search is used to find the sequence $$Y$$ that maximizes a score function $$s(Y, X)$$ given a trained model. Two important refinements can be introduced.

**Length normalization**: With length normalization, the hypothesis of different lengths are taken into account.

- Normalize by length directly
- Normalize by length over the power of $$\alpha$$.
- Use a scoring function $$s(Y, X)$$ with two parameters $$\alpha$$ and $$\beta$$.

There is a work from Facebook that tries to attach softmax. There method is called [Adaptive Softmax](https://research.facebook.com/blog/building-an-efficient-neural-language-model-over-a-billion-words/).


