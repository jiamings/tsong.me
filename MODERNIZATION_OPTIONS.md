# Modernization Options

This branch is for exploring a post-Jekyll version of `tsong.me`, especially if
the site later grows a blog with math-heavy technical posts.

## Current constraints

- The live site is published from `main` + `/docs` on GitHub Pages.
- The current source is Jekyll/al-folio-derived Ruby code.
- Local Jekyll builds are currently brittle because the machine has Ruby 2.6,
  while current dependency resolution pulls gems requiring Ruby 3+.
- The site is mostly static: homepage, project/research links, old PDFs, and a
  possible future blog.

## Option A: Astro in `site/`

Astro is the strongest fit.

Why:

- Static-first by default, so it works naturally with GitHub Pages.
- Markdown and MDX are first-class enough for blog posts.
- Content collections provide a typed frontmatter/content model for posts.
- It can stay almost zero-JavaScript for a personal site, but still allows
  interactive components later.
- There is already an old `origin/revamp/astro-site` branch with a `site/`
  prototype and a GitHub Pages workflow.

Suggested structure:

```text
site/
  public/
    CNAME
    assets/
  src/
    content/
      blog/
        2026-xx-xx-example.md
    layouts/
      Base.astro
      Post.astro
    pages/
      index.astro
      blog/
        index.astro
        [...slug].astro
    styles/
      global.css
```

Blog experience:

- Write posts in `src/content/blog/*.md` or `*.mdx`.
- Use frontmatter for title, date, description, tags, and draft status.
- Add KaTeX/remark plugins for math.
- Add RSS later without changing the content model.

Deployment:

- Keep GitHub Pages, but switch Pages back to GitHub Actions deployment.
- Build `site/` with Node and deploy `site/dist`.
- Keep `docs/` around temporarily until the Astro site fully replaces it.

Migration effort:

- Low-to-medium. The current homepage is simple and can be ported quickly.
- Best path is to create a fresh Astro site rather than trying to rescue all
  al-folio/Jekyll conventions.

## Option B: Eleventy

Eleventy is the simplest modern static-site-generator option.

Why:

- Markdown-first and close to the current static HTML mental model.
- Less framework ceremony than Astro or Next.js.
- Very good if the site should stay mostly text, essays, and links.
- Easy to output plain static HTML for GitHub Pages.

Tradeoffs:

- Less typed/content-model structure than Astro unless we add conventions.
- MDX/component-style writing is possible, but Astro is smoother there.
- More manual assembly for things like RSS, tag pages, post schemas, and math.

Best for:

- A minimal personal site plus blog where simplicity matters more than future UI
  flexibility.

## Option C: Next.js static export

Next.js is viable but probably too heavy for this site.

Why it could work:

- Static export can generate deployable HTML/CSS/JS.
- MDX support is mature.
- Good if future posts need React components or interactive demos.

Why I would not start here:

- More moving pieces than needed for a personal homepage/blog.
- GitHub Pages static export has more edge cases than Astro/Eleventy.
- The output usually carries more JavaScript than this site needs.

Best for:

- If the blog becomes an interactive research notebook with React demos,
  visualizations, and client-side components.

## Option D: Keep Jekyll, modernize minimally

This is the smallest change, but not the best long-term direction.

What we could do:

- Pin Ruby and gems properly.
- Remove most al-folio baggage.
- Add a cleaner `_posts/` blog with KaTeX.

Why not:

- The current template has a lot of academic-site legacy.
- Ruby dependency drift has already caused local build friction.
- It is harder to make the site feel like a modern personal/research site
  without fighting the old theme.

## Recommendation

Use Astro.

Practical plan:

1. Create a fresh `site/` Astro app on this branch.
2. Port the current homepage exactly first.
3. Add `src/content/blog/` with one draft/sample post using Markdown + math.
4. Add a GitHub Pages workflow that builds `site/dist`.
5. Preview on this branch; when ready, switch Pages deployment from `/docs` to
   the workflow.

This keeps the site markdown-first and GitHub-hosted while avoiding the Jekyll
dependency problems. It also leaves room for technical blog posts with math,
MDX components, RSS, and richer project pages later.
