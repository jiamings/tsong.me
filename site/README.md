# tsong.me (Astro Revamp)

This directory contains the new Astro-based site focused on industry-facing content:

- Projects
- Talks
- Podcasts
- Blog

## Local development

From this directory:

```sh
npm install
npm run dev
```

## Build

```sh
npm run build
```

## Deploy to GitHub Pages

This repo includes `.github/workflows/deploy-astro-pages.yml`:

- Pull requests to `main` build the Astro site for validation.
- Pushes to `main` build and deploy `site/dist` to GitHub Pages.

Custom domain is preserved by `public/CNAME` (`tsong.me`).

## Content model

Content is markdown-first and organized into collections:

- `src/content/projects`
- `src/content/talks`
- `src/content/podcasts`
- `src/content/blog`

Collection schemas are defined in `src/content.config.ts`.

## Migration notes

This Astro site was bootstrapped in a separate `site/` folder so the legacy Jekyll site can remain untouched while you iterate on design and content.
