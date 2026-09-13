---
layout: default
title: Biography
---

{%- assign profile = site.data.profile -%}

<style>
  .bio {
    max-width: 48rem;
    margin-top: 1.5rem;
  }
  .bio h1 {
    margin-bottom: .35rem;
  }
  .bio .role {
    margin: 0 0 1rem;
    color: #556270;
    line-height: 1.4;
  }
  .bio p {
    line-height: 1.7;
    margin: 0 0 1rem;
  }
  .bio .links {
    display: flex;
    flex-wrap: wrap;
    gap: .5rem;
    margin-top: 1rem;
  }
  .bio .links a {
    text-decoration: none;
    color: #0b6b8a;
    border: 1px solid #d9e2ea;
    border-radius: 999px;
    padding: .26rem .7rem;
    font-size: .86rem;
  }
  .bio .links a:hover {
    background: #d9eef5;
  }
</style>

<div class="bio">
  <h1>{{ profile.name }}</h1>
  <p class="role">{{ profile.title }}, {{ profile.organization }}</p>

  {%- for para in profile.summary -%}
  <p>{{ para }}</p>
  {%- endfor -%}

  <div class="links">
    <a href="/index.html">Home</a>
    <a href="/experience.html">Experience</a>
    <a href="/education.html">Education</a>
    <a href="/teaching.html">Mentoring and Teaching</a>
    <a href="/talks.html">Talks, Panels, and Tutorials</a>
    <a href="/service-preview.html">Professional Service</a>
    <a href="/societies.html">Professional Societies</a>
    <a href="/publications-preview.html">Publications</a>
    <a href="/files/docs/AkshayRajhansCV.pdf">Curriculum Vitae (PDF)</a>
  </div>
</div>
