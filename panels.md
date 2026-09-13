---
layout: default
title: Panels
---

<!--
  Rendered entirely from _data/panels.yml + _data/topics.yml.

  This is the first post-service/publications migration of a legacy page into the
  new data model. Panels are the smallest slice: flat list, no role taxonomy, and
  just one controlled facet (`topics`) plus free-text search over the panel title,
  venue and note.
-->

{%- assign entries = site.data.panels.entries | sort: "start" | reverse -%}

<style>
  .panel-list { list-style: none; margin: 0; padding: 0; }
  .panel-list > li {
    padding: .5rem 0; border-top: 1px solid #eaeef2;
    display: grid; grid-template-columns: 1fr auto; gap: 0 .75rem; align-items: baseline;
  }
  .panel-list > li:first-child { border-top: none; }
  .panel-title { font-size: .95rem; font-weight: 600; line-height: 1.3; }
  .panel-year {
    font-size: .8rem; color: #57606a; font-variant-numeric: tabular-nums;
    white-space: nowrap; text-align: right;
  }
  .panel-meta {
    grid-column: 1 / -1; font-size: .82rem; color: #57606a; line-height: 1.4;
    margin-top: .1rem;
  }
  .panel-foot {
    grid-column: 1 / -1; margin-top: .25rem;
    display: flex; flex-wrap: wrap; gap: .3rem; align-items: center;
  }
  .panel-tag {
    font-size: .72rem; padding: .05rem .45rem; border-radius: 2em;
    background: #ddf4ff; color: #0550ae;
  }
  .panel-links { font-size: .75rem; }
  .panel-links a { text-decoration: none; }
  .panel-links a:hover { text-decoration: underline; }
  .panel-note { font-size: .75rem; color: #57606a; font-style: italic; }
</style>

# Panels

<p><em>Panels are also listed on the broader <a href="talks.html">Talks and Panels</a>
page. This page is the panel-only slice.</em></p>

<noscript>
  <p><em>Filtering needs JavaScript. The complete list is below, newest first.</em></p>
</noscript>

<div class="fbrowse">

  <aside class="fbrowse-nav" aria-label="Filter panels">

    <div class="facet" data-facet="topic">
      <button type="button" class="facet-header" aria-expanded="true">Topics</button>
      <ul class="facet-options">
        {%- for topic in site.data.topics -%}
        {%- assign hits = entries | where_exp: "e", "e.topics contains topic.slug" -%}
        {%- if hits.size > 0 -%}
        <li><label title="{{ topic.blurb | strip_newlines | strip | escape }}">
          <input type="checkbox" data-facet="topic" value="{{ topic.slug }}">
          <span class="facet-label">{{ topic.name }}</span>
          <span class="facet-count" data-facet="topic" data-value="{{ topic.slug }}"></span>
        </label></li>
        {%- endif -%}
        {%- endfor -%}
      </ul>
    </div>

  </aside>

  <div class="fbrowse-main">

    <div class="fbrowse-bar">
      <div class="fbrowse-search">
        <input type="search" id="fbrowse-search" aria-label="Search panels"
               placeholder="Search panel title, venue, note&hellip;">
      </div>
      <span class="fbrowse-count" id="fbrowse-count" aria-live="polite"></span>
    </div>

    <div class="fbrowse-active" id="fbrowse-active">
      <span class="label">Filtered by:</span>
      <span id="fbrowse-chips"></span>
      <button type="button" class="fclear" id="fbrowse-clear">Clear all</button>
    </div>

    <div class="fbrowse-empty" id="fbrowse-empty">
      <strong>Nothing matches every filter.</strong>
      Try removing a topic filter or broadening the search.
    </div>

    <ul class="panel-list">
      {%- for entry in entries -%}
      {%- assign facet_text = "" -%}
      {%- for slug in entry.topics -%}
        {%- assign t = site.data.topics | where: "slug", slug | first -%}
        {%- assign facet_text = facet_text | append: " " | append: t.name -%}
      {%- endfor -%}
      {%- assign searchable = entry.what | append: " " | append: entry.venue | append: " " | append: entry.note | append: " " | append: facet_text -%}
      <li class="fitem"
          id="{{ entry.id }}"
          data-facet-topic="{{ entry.topics | join: ' ' }}"
          data-search="{{ searchable | strip_newlines | downcase | escape }}">
        <span class="panel-title">{{ entry.what }}</span>
        <span class="panel-year">{{ entry.start }}</span>
        <span class="panel-meta">{{ entry.venue }}</span>
        <span class="panel-foot">
          {%- for slug in entry.topics -%}
            {%- assign topic = site.data.topics | where: "slug", slug | first -%}
          <span class="panel-tag">{{ topic.name | default: slug }}</span>
          {%- endfor -%}
          {%- if entry.links -%}
          <span class="panel-links">
            {%- for link in entry.links -%}<a href="{{ link.url }}">[{{ link.label }}]</a>{% endfor -%}
          </span>
          {%- endif -%}
          {%- if entry.note -%}
          <span class="panel-note">{{ entry.note }}</span>
          {%- endif -%}
        </span>
      </li>
      {%- endfor -%}
    </ul>

  </div>
</div>

{% include facet-ui.html %}
