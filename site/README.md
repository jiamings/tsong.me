# tsong.me Astro site

This directory contains the Astro version of `tsong.me`.

## Local development

This machine currently has Node but may not expose `npm` on `PATH`. If npm is
available:

```sh
npm install
npm run dev
```

Otherwise use any Node package manager that can install from `package-lock.json`.

## Build

```sh
npm run build
```

The production output is written to `dist/`.

## Content

- Homepage: `src/pages/index.astro`
- Homepage: `src/pages/index.astro`

A blog can be added later with Astro content collections and Markdown/MDX, but it
is intentionally not surfaced in the current site.

## Deployment

The repository includes `.github/workflows/deploy-astro-pages.yml`, which builds
this directory and deploys `site/dist` to GitHub Pages. When this replaces the
legacy `/docs` deployment, set Pages to use GitHub Actions.
