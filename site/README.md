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

## Content model

Content is markdown-first and organized into collections:

- `src/content/projects`
- `src/content/talks`
- `src/content/podcasts`
- `src/content/blog`

Collection schemas are defined in `src/content.config.ts`.

## Migration notes

This Astro site was bootstrapped in a separate `site/` folder so the legacy Jekyll site can remain untouched while you iterate on design and content.
