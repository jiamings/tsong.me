---
layout: post
title: numpy.std()
author: 
tags:
- blog
---

> TL;DR: Always use higher precision when using `numpy.std()`.



I was working on rewriting my code and found some problems with numpy when using the std function, where the result with `dtype=np.float32` is drastically different from `dtype=np.float64`. (Double precision float gives the correct result while single precision does not)



See the following example:

```python
import numpy as np
a = np.random.normal(0.0, 500.0, [10000000, 2])
print('float64: {}'.format(np.std(a, axis=0)))
print('float32: {}'.format(np.std(a, axis=0, dtype=np.float32)))
```

```
float64: [ 500.17523373  500.04088655]
float32: [ 496.34017944  496.21456909]
```



Here we can see that even if the standard deviation should be 500, it was 496 when using float32. Numpy actually knows this (in [their docs](https://docs.scipy.org/doc/numpy-1.12.0/reference/generated/numpy.std.html)):

> For floating-point input, the *std* is computed using the same precision the input has. Depending on the input data, this can cause the results to be inaccurate, especially for float32 (see example below). Specifying a higher-accuracy accumulator using the [`dtype`](https://docs.scipy.org/doc/numpy-1.12.0/reference/generated/numpy.dtype.html#numpy.dtype) keyword can alleviate this issue.



Weirdly enough, if we use a data with shape [10000000 * 2] instead of [10000000, 2], then this will not have issues:

```python
a = np.random.normal(0.0, 500.0, [10000000 * 2])
print('float64: {}'.format(np.std(a)))
print('float32: {}'.format(np.std(a, dtype=np.float32)))
```

```
float64: 499.9830404637898
float32: 499.9829406738281
```





If we calculate std on each axis manually, no issues occur as well:

```python
print('float64: [{}, {}]'.format(np.std(a[:, 0], axis=0), np.std(a[:, 1], axis=0)))
print('float32: [{}, {}]'.format(np.std(a[:, 0], axis=0, dtype=np.float32), np.std(a[:, 1], axis=0, dtype=np.float32)))
```

```
float64: [500.1752337287789, 500.04088654730464]
float32: [500.1752624511719, 500.04095458984375]
```



So there is really no reason why std for float32 in the first case fails. Nevertheless, this happens and **we should use float64 in all cases**.