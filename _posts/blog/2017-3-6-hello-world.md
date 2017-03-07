---
layout: post
title: Hello World!
author: Jiaming Song
tags:
- blog
---

Finally I decide to open a blog here. I will write mostly about research stuff - some recent works will come out shortly - but in this post I just wanted to talk about the blog itself.

It is a long journey to start with [Jekyll](https://jekyllrb.com) from scratch[^medium] - I have always wanted more customization options, but I really know little about web developing.

It all started when I was writing a website for grad school applications. I started off by using the [Bootstrap Material Design](http://fezvrasta.github.io/bootstrap-material-design/) template, which I used during a [course project](http://tsong.me/projects/biopedia/). It was a great template, but I just did not like Google's Roboto font in paragraphs. So after I got to Stanford, I changed to the [Paper template @ Bootswatch](https://bootswatch.com/paper/). Material Design rocks!

But the font problem persists. Then I took inspiration from [Typora](https://typora.io), a fantastic Markdown editor. I love how beautiful the rendering in a WYSIWYG style, and I though it would be pleasing to see this style in the blog posts, so I can basically type in Typora and publish directly without worring about the style in the browser. This can be done easily since Typora (and most other Markdown editors) use CSS templates for rendering; so I took it. I really have no idea how adding a file replaces the Roboto font, but it worked, so I never bothered to know why [^phd].

However, the process was not entirely smooth, and I list some of the problems that I encountered and their solutions:

1. Math does not render properly in the browser but it works perfectly in Typora. **Solution**: All math in Kramdown are enclosed in double dollar signs. Luckily, Typora supports this, so the problem is solved.
2. Disqus just does not work. **Solution**: I found the documentation in the official website very confusing. [This blog post](http://www.perfectlyrandom.org/2014/06/29/adding-disqus-to-your-jekyll-powered-github-pages/) is a much better guide.
3. I need citations. **Solution:** Use [Jekyll Scholar](https://github.com/inukshuk/jekyll-scholar). 
4. Images do not appear where I want it to. **Solution**: Use Kramdown IAL, such as `{:.center}`, and some CSS hacks will get you there. Or use plain Photoshop.



<br/>

Here is a comparison between brower and Typora:

**Browser:**[^mathjax]

![]({{site.baseurl}}/public/img/blog/browser.png)

**Typora**:

![]({{site.baseurl}}/public/img/blog/typora.png)

So basically, WYSIWYG!



<br/>

The code for this blog is fully available [on Github](https://github.com/jiamings/jiamings.github.io). Feel free to use the code - I will be grateful if you include a link to [tsong.me](http://tsong.me) in the footer of your blog.

Certain style details of the blog are inspired by [Otoro](http://blog.otoro.net/) and [Dustin Tran's Blog](http://dustintran.com/blog/).

<hr/>

#### Footnotes

[^medium]: Medium does not support math, and Ghost is expensive (and I didn't really need it by the time I encountered it).
[^mathjax]: Math is not pretty. Use Common HTML in MathJax fix this.
[^phd]: I am a machine learning Ph.D, not a front-end developer.

 