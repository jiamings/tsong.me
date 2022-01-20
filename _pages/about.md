---
layout: about
title: About
permalink: /
description:


news: true
social: true
years: [2022, 2021, 2020, 2019, 2018, 2017, 2016]
---

Ph.D. Candidate, Computer Science <br/>
[Stanford Artificial Intelligence Laboratory](ai.stanford.edu) <br/>
[Statistical Machine Learning Group](statsml.stanford.edu) <br/>
<a href="assets/pdf/jiaming_cv.pdf" target="_blank"><b>Curriculum Vitae</b></a>

---- 

I am a postdoc in Computer Science in Stanford University working with [Stefano Ermon](http://cs.stanford.edu/~ermon). I completed my [Ph.D.](assets/pdf/jiaming_thesis.pdf) in Computer Science at Stanford University advised by Stefano as well.

I did my undergrad in the Department of Computer Science and Technology, Tsinghua University, where I worked with [Jun Zhu](http://ml.cs.tsinghua.edu.cn/~jun/index.shtml) and [Lawrence Carin](http://people.ee.duke.edu/~lcarin).

My research is centered on deep unsupervised learning, with various applications on deep generative modeling, representation learning and (inverse) reinforcement learning. Recently, I am interested in the following topics:

- Information-theoretic approaches to machine learning and representation learning 
[[1](https://arxiv.org/abs/2007.09852), [2](https://arxiv.org/abs/1910.06222), [3](https://arxiv.org/abs/2002.10689), [4](https://arxiv.org/abs/1812.04218)]
- Improvements to generative modeling and statistical inference [[1](https://arxiv.org/abs/1910.09779), [2](https://arxiv.org/abs/1906.09531), [3](https://arxiv.org/abs/1706.07561), [4](https://arxiv.org/abs/2010.02502)]
- Learning complex behaviors and intentions from demonstrations [[1](https://arxiv.org/abs/1807.09936), [2](https://arxiv.org/abs/1703.08840), [3](https://arxiv.org/abs/1907.13220), [4](http://www.ifaamas.org/Proceedings/aamas2020/pdfs/p1855.pdf)]
- Societal issues in machine learning, such as fairness and calibration [[1](https://arxiv.org/abs/1812.04218), [2](https://arxiv.org/abs/1906.08312), [3](https://arxiv.org/abs/2008.09643)]

**Email**: tsong [at] cs [dot] stanford [dot] edu

----



##### Teaching

- [CS228](cs228.stanford.edu), Probablistic Graphical Models (Winter 2020, Head TA)
- [CS236](cs236.stanford.edu), Deep Generative Models (Fall 2018, TA)


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

- [Qualcomm Innovation Fellowship](https://www.qualcomm.com/invention/research/university-relations/innovation-fellowship/winners) (QInF 2018, 4.6%)
- Stanford School of Engineering Fellowship (2016)
- Google Excellence Scholarship (2015)
- Outstanding Undergraduate, China Computer Federation (2015)
- Outstanding Winner, Interdisciplinary Contest in Modeling (2015, 0.4%)
- Zhong Shimo Scholarship (2013, 0.75%)

----

**Acknowledgements**: based on the [al-folio](https://github.com/alshedivat/al-folio) template by [Maruan Al-Shedivat](https://www.cs.cmu.edu/~mshediva/).