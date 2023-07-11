---
layout: about
title: About
permalink: /
description:


news: true
social: true
years: [2023, 2022, 2021, 2020, 2019, 2018, 2017, 2016]
---

Ph.D., Computer Science <br/>
Research Scientist, Luma AI <br/>
<a href="assets/pdf/jiaming_cv.pdf" target="_blank"><b>Curriculum Vitae (outdated)</b></a>

---- 

I am a research scientist in [Luma AI](https://lumalabs.ai/), where I am working on foundation models for 3D. 

Before that, I was:
- A research scientist in the Deep Imagination Research (DIR) group of NVIDIA Research. I worked on NVIDIA AI Foundations, specifically the [Picasso project](https://www.nvidia.com/en-us/gpu-cloud/picasso/). 
- A research scientist in the Learning and Perception Research (LPR) group of NVIDIA Research. I was the first author of an ICLR 2023 and an ICML 2023 paper and also collaborated on various other papers.
- A postdoc in Computer Science in Stanford University working with [Stefano Ermon](http://cs.stanford.edu/~ermon). 
- [Ph.D.](assets/pdf/jiaming_thesis.pdf) in Computer Science at Stanford University advised by Stefano as well.
- Undergrad in the Department of Computer Science and Technology, Tsinghua University, where I worked with [Jun Zhu](http://ml.cs.tsinghua.edu.cn/~jun/index.shtml) and [Lawrence Carin](http://people.ee.duke.edu/~lcarin).


My "generative AI" qualifications:
- I created DDIM, the earliest [accelerated algorithm for diffusion models](https://arxiv.org/abs/2010.02502). DDIM is widely used in recent generative AI systems including [DALL-E 2](https://cdn.openai.com/papers/dall-e-2.pdf), [Imagen](https://imagen.research.google/paper.pdf), [Stable Diffusion](https://en.wikipedia.org/wiki/Stable_Diffusion), and [ERNIE-ViLG 2.0](https://arxiv.org/abs/2210.15257). 
- I co-authored [the paper](https://arxiv.org/abs/2108.01073) that is the foundation of [Stable Diffusion's img2img method](https://github.com/CompVis/stable-diffusion/blob/main/README.md#image-modification-with-stable-diffusion). 
- I also [democratized the use of diffusion models for general applications](https://arxiv.org/abs/2201.11793), such as super-resolution, inpainting, and [JPEG restoration](https://arxiv.org/abs/2209.11888). 

**Email**: jiaming [dot] tsong [atgmaildotcom]


----

##### News

- Organized the [CVPR 2023 diffusion model tutorial](https://cvpr2023-tutorial-diffusion-models.github.io/). Slides are available. 
- Organizing the SIGGRAPH 2023 Course on Diffusion Models.
- Talks at University of Edinburgh, DeepMind, Imperial College London, and Oxford. [[slides](assets/slides/2023-01-26-workshop.pdf)]


----

##### Publications

<div class="publications-front">

{% for y in page.years %}
  <h3 class="year">{{y}}</h3>
  {% bibliography -f papers -q @*[year={{y}}]* %}
{% endfor %}

</div>
---

##### Professional Services

**Journal reviewer**: IEEE TPAMI, JAIR, IEEE TIT, ACM TIST, JMLR

**Conference reviewer / Program committee**: ICML (2019, 2020, 2021), NeurIPS (2019, 2020, 2021), ICLR (2018, 2019, 2020, 2021), COLT (2019), UAI (2019, 2020, 2021), CVPR (2020, 2021), ECCV (2020), ICCV (2019, 2021), AAAI (2021), ACML (2018, 2019), WACV (2020)

**Workshop organization**:
- [NeurIPS 2019 Workshop on Information Theory and Machine Learning](https://sites.google.com/view/itml19/home) (chair)
- [DALI 2018 Workshop on Generative Models and Reinforcement Learning](http://dalimeeting.org/dali2018//program) (chair)

----

##### Awards and Fellowships

- ICLR 2022 Outstanding Paper Award
- [Qualcomm Innovation Fellowship](https://www.qualcomm.com/invention/research/university-relations/innovation-fellowship/winners) (QInF 2018, 4.6%)
- Stanford School of Engineering Fellowship (2016)
- Google Excellence Scholarship (2015)
- Outstanding Undergraduate, China Computer Federation (2015)
- Outstanding Winner, Interdisciplinary Contest in Modeling (2015, 0.4%)
- Zhong Shimo Scholarship (2013, 0.75%)

----


##### Teaching

- [CS228](cs228.stanford.edu), Probablistic Graphical Models (Winter 2020, Head TA)
- [CS236](cs236.stanford.edu), Deep Generative Models (Fall 2018, TA)

----

**Acknowledgements**: based on the [al-folio](https://github.com/alshedivat/al-folio) template by [Maruan Al-Shedivat](https://www.cs.cmu.edu/~mshediva/).