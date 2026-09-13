---
layout: default
title: Professional Societies
---

{%- assign entries = site.data.societies.entries | sort: "class_year" | reverse -%}

<style>
  .societies {
    max-width: 44rem;
    margin-top: 1.5rem;
  }
  .society-list {
    list-style: none;
    margin: 1rem 0 0;
    padding: 0;
  }
  .society-list li {
    padding: .75rem 0;
    border-top: 1px solid #eaeef2;
  }
  .society-list li:first-child {
    border-top: none;
  }
  .society-level {
    display: block;
    font-weight: 600;
    color: #18212b;
  }
  .society-org {
    display: block;
    margin-top: .1rem;
    color: #556270;
  }
  .society-meta {
    display: block;
    margin-top: .15rem;
    font-size: .88rem;
    color: #57606a;
  }
</style>

<div class="societies">
  <h1>Professional Societies</h1>
  <p>Memberships recorded in the CV as professional affiliations rather than service appointments.</p>

  <ul class="society-list">
    {%- for entry in entries -%}
    <li>
      <span class="society-level">{{ entry.level }}</span>
      <span class="society-org">{{ entry.organization }}</span>
      <span class="society-meta">Class of {{ entry.class_year }}{% if entry.end == "ongoing" %}; current{% endif %}</span>
    </li>
    {%- endfor -%}
  </ul>
</div>
