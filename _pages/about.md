---
layout: about
title: About
permalink: /
description:


news: true
social: true
years: [2022, 2021, 2020, 2019, 2018, 2017, 2016]
---

Ph.D., Computer Science <br/>
Research Scientist, NVIDIA <br/>
<a href="assets/pdf/jiaming_cv.pdf" target="_blank"><b>Curriculum Vitae</b></a>

---- 

I am a research scientist in the Learning and Perception Research (LPR) team of NVIDIA Research. I am interested in learning and inference algorithms for applications such as generative modeling, reinforcement learning, representation learning, simulation, and inverse problems. 


Prior to joining LPR, I was a postdoc in Computer Science in Stanford University working with [Stefano Ermon](http://cs.stanford.edu/~ermon). I completed my [Ph.D.](assets/pdf/jiaming_thesis.pdf) in Computer Science at Stanford University advised by Stefano as well.
I did my undergrad in the Department of Computer Science and Technology, Tsinghua University, where I worked with [Jun Zhu](http://ml.cs.tsinghua.edu.cn/~jun/index.shtml) and [Lawrence Carin](http://people.ee.duke.edu/~lcarin).

**Email**: jiaming [dot] tsong [atgmaildotcom]




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