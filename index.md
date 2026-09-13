---
layout: default
title: Akshay Rajhans
---

{%- assign profile = site.data.profile -%}

<style>
  :root {
    --ink: #18212b;
    --muted: #556270;
    --line: #d9e2ea;
    --panel: #f7fafc;
    --accent: #0b6b8a;
    --accent-soft: #d9eef5;
  }
  .home {
    margin-top: 1.5rem;
    display: grid;
    gap: 1.5rem;
  }
  .hero {
    display: grid;
    grid-template-columns: 220px 1fr;
    gap: 1.5rem;
    align-items: start;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid var(--line);
  }
  .hero img {
    width: 100%;
    border-radius: 10px;
    display: block;
  }
  .eyebrow {
    margin: 0 0 .3rem;
    font-size: .78rem;
    font-weight: 700;
    letter-spacing: .08em;
    text-transform: uppercase;
    color: var(--accent);
  }
  .hero h1 {
    margin: 0;
    font-size: 2.1rem;
    line-height: 1.05;
    color: var(--ink);
  }
  .hero .role {
    margin: .45rem 0 0;
    font-size: 1.02rem;
    line-height: 1.35;
    color: var(--muted);
    max-width: 46rem;
  }
  .hero .tagline {
    margin: .85rem 0 0;
    font-size: 1rem;
    line-height: 1.5;
    color: var(--ink);
    max-width: 48rem;
  }
  .linkrow {
    display: flex;
    flex-wrap: wrap;
    gap: .45rem;
    margin-top: 1rem;
  }
  .linkrow a {
    text-decoration: none;
    color: var(--accent);
    border: 1px solid var(--line);
    background: #fff;
    border-radius: 999px;
    padding: .28rem .72rem;
    font-size: .86rem;
  }
  .linkrow a:hover {
    background: var(--accent-soft);
  }
  .home-grid {
    display: grid;
    grid-template-columns: 1.2fr .8fr;
    gap: 1.5rem;
  }
  .section h2 {
    margin: 0 0 .65rem;
    font-size: 1.08rem;
    color: var(--ink);
  }
  .summary p {
    margin: 0 0 .9rem;
    line-height: 1.65;
    color: var(--ink);
  }
  .summary p:last-child {
    margin-bottom: 0;
  }
  .stack {
    display: grid;
    gap: 1rem;
  }
  .card {
    padding: 1rem 1.05rem;
    border: 1px solid var(--line);
    border-radius: 10px;
    background: var(--panel);
  }
  .card h3 {
    margin: 0 0 .4rem;
    font-size: .98rem;
    color: var(--ink);
  }
  .card p {
    margin: 0;
    line-height: 1.5;
    color: var(--muted);
    font-size: .92rem;
  }
  .card a {
    color: var(--accent);
    text-decoration: none;
  }
  .card a:hover {
    text-decoration: underline;
  }
  .tags {
    display: flex;
    flex-wrap: wrap;
    gap: .45rem;
  }
  .tag {
    padding: .24rem .58rem;
    border-radius: 999px;
    background: var(--accent-soft);
    color: var(--accent);
    font-size: .82rem;
  }
  .contact {
    font-size: .93rem;
    color: var(--muted);
  }
  .contact strong {
    color: var(--ink);
  }
  @media (max-width: 860px) {
    .hero,
    .home-grid {
      grid-template-columns: 1fr;
    }
    .hero {
      gap: 1rem;
    }
    .hero img {
      max-width: 240px;
    }
  }
</style>

<div class="home">
  <section class="hero">
    <div>
      <img src="{{ profile.portrait }}" alt="{{ profile.name }}">
    </div>
    <div>
      <p class="eyebrow">{{ profile.organization }}</p>
      <h1>{{ profile.name }}</h1>
      <p class="role">{{ profile.title }}</p>
      <p class="tagline">{{ profile.tagline }}</p>
      <div class="linkrow">
        {%- for link in profile.external_links -%}
        <a href="{{ link.url }}">{{ link.label }}</a>
        {%- endfor -%}
      </div>
    </div>
  </section>

  <div class="home-grid">
    <section class="section summary">
      <h2>Overview</h2>
      <p>{{ profile.home_intro }}</p>
    </section>

    <div class="stack">
      <section class="section">
        <h2>Contact</h2>
        <div class="card contact">
          <strong>{{ profile.name }}, {{ profile.degrees }}</strong><br>
          {{ profile.title }}<br>
          {{ profile.organization }}<br>
          {{ profile.email_obfuscated }}
        </div>
      </section>

      <section class="section">
        <h2>Focus Areas</h2>
        <div class="tags">
          {%- for area in profile.focus_areas -%}
          <span class="tag">{{ area }}</span>
          {%- endfor -%}
        </div>
      </section>
    </div>
  </div>

  <section class="section">
    <h2>Programs and Initiatives</h2>
    <div class="stack">
      {%- for item in profile.programs -%}
      <div class="card">
        <h3><a href="{{ item.url }}">{{ item.title }}</a></h3>
        <p>{{ item.note }}</p>
      </div>
      {%- endfor -%}
    </div>
  </section>

  <section class="section">
    <h2>Explore the Site</h2>
    <div class="stack">
      {%- for item in profile.site_links -%}
      <div class="card">
        <h3><a href="{{ item.url }}">{{ item.label }}</a></h3>
        <p>{{ item.note }}</p>
      </div>
      {%- endfor -%}
    </div>
  </section>
</div>
