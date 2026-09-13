---
layout: default
title: Patents
---

{%- assign patents = site.data.patents.entries | sort: "start" | reverse -%}

<style>
  .patents {
    max-width: 52rem;
    margin-top: 1.5rem;
  }
  .patent-list {
    list-style: none;
    margin: 0;
    padding: 0;
  }
  .patent-list > li {
    padding: .9rem 0;
    border-top: 1px solid #eaeef2;
    display: grid;
    grid-template-columns: 1fr auto;
    gap: 0 .75rem;
    align-items: baseline;
  }
  .patent-list > li:first-child {
    border-top: none;
  }
  .patent-title {
    font-size: 1rem;
    font-weight: 600;
    line-height: 1.35;
  }
  .patent-year {
    font-size: .82rem;
    color: #57606a;
    white-space: nowrap;
    font-variant-numeric: tabular-nums;
  }
  .patent-meta,
  .patent-foot {
    grid-column: 1 / -1;
  }
  .patent-meta {
    margin-top: .15rem;
    font-size: .9rem;
    line-height: 1.55;
    color: #24292f;
  }
  .patent-foot {
    margin-top: .45rem;
    display: flex;
    flex-wrap: wrap;
    gap: .35rem .5rem;
    align-items: center;
  }
  .patent-tag {
    font-size: .74rem;
    padding: .05rem .45rem;
    border-radius: 2em;
    background: #ddf4ff;
    color: #0550ae;
  }
  .patent-links {
    font-size: .78rem;
  }
  .patent-links a {
    text-decoration: none;
  }
  .patent-links a:hover {
    text-decoration: underline;
  }
  .patent-note {
    font-size: .78rem;
    color: #57606a;
    font-style: italic;
  }
</style>

<div class="patents">
  <h1>Patents</h1>
  <p>Patent material is kept separate from publications. It is still a professional
  output, but not the same kind of artifact as a paper, report, or thesis.</p>

  <ul class="patent-list">
    {%- for entry in patents -%}
    <li class="fitem" id="{{ entry.id }}">
      <span class="patent-title">{{ entry.what }}</span>
      <span class="patent-year">{{ entry.start }}</span>
      <span class="patent-meta">
        {{ entry.inventors | join: ", " }}.
        Patent No. {{ entry.patent_number }}.
      </span>
      <span class="patent-foot">
        {%- for slug in entry.topics -%}
          {%- assign topic = site.data.topics | where: "slug", slug | first -%}
        <span class="patent-tag">{{ topic.name | default: slug }}</span>
        {%- endfor -%}
        <span class="patent-links">
          {%- for link in entry.links -%}<a href="{{ link.url }}">[{{ link.label }}]</a>{% endfor -%}
        </span>
        {%- if entry.note -%}
        <span class="patent-note">{{ entry.note }}</span>
        {%- endif -%}
      </span>
    </li>
    {%- endfor -%}
  </ul>
</div>
