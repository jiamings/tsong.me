import { defineCollection, z } from "astro:content";

const projects = defineCollection({
  schema: z.object({
    title: z.string(),
    summary: z.string(),
    date: z.date(),
    tags: z.array(z.string()).default([]),
    projectUrl: z.string().url().optional(),
    repoUrl: z.string().url().optional(),
    featured: z.boolean().default(false)
  })
});

const talks = defineCollection({
  schema: z.object({
    title: z.string(),
    event: z.string(),
    date: z.date(),
    location: z.string().optional(),
    slidesUrl: z.string().url().optional(),
    videoUrl: z.string().url().optional(),
    summary: z.string()
  })
});

const podcasts = defineCollection({
  schema: z.object({
    title: z.string(),
    show: z.string(),
    date: z.date(),
    episodeUrl: z.string().url(),
    summary: z.string()
  })
});

const blog = defineCollection({
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.date(),
    tags: z.array(z.string()).default([]),
    draft: z.boolean().default(false)
  })
});

export const collections = { projects, talks, podcasts, blog };
