---
layout: default
title: Talks, Panels, and Tutorials
---

<!--
  The user-facing speaking page is one place: keynotes, invited talks, panels,
  and tutorials.
  Panels remain a distinct source file (`panels.yml`) because the data shape and
  curation path are different, not because they need to be a separate destination.
-->

{%- assign talks = site.data.talks.entries | sort: "start" | reverse -%}
{%- assign panels = site.data.panels.entries | sort: "start" | reverse -%}

<style>
  .talk-list { list-style: none; margin: 0; padding: 0; }
  .talk-list > li {
    padding: .5rem 0; border-top: 1px solid #eaeef2;
    display: grid; grid-template-columns: 1fr auto; gap: 0 .75rem; align-items: baseline;
  }
  .talk-list > li:first-child { border-top: none; }
  .talk-title { font-size: .95rem; font-weight: 600; line-height: 1.3; }
  .talk-year {
    font-size: .8rem; color: #57606a; font-variant-numeric: tabular-nums;
    white-space: nowrap; text-align: right;
  }
  .talk-meta {
    grid-column: 1 / -1; font-size: .82rem; color: #57606a; line-height: 1.4;
    margin-top: .1rem;
  }
  .talk-foot {
    grid-column: 1 / -1; margin-top: .25rem;
    display: flex; flex-wrap: wrap; gap: .3rem; align-items: center;
  }
  .talk-type {
    font-size: .7rem; padding: .05rem .45rem; border-radius: 2em;
    border: 1px solid #d0d7de; background: #f6f8fa; color: #57606a;
    text-transform: uppercase; letter-spacing: .03em;
  }
  .talk-tag {
    font-size: .72rem; padding: .05rem .45rem; border-radius: 2em;
    background: #ddf4ff; color: #0550ae;
  }
  .talk-links { font-size: .75rem; }
  .talk-links a { text-decoration: none; }
  .talk-links a:hover { text-decoration: underline; }
  .talk-note { font-size: .75rem; color: #57606a; font-style: italic; }
  .fgroup { margin-top: 1.25rem; }
  .fgroup > h2 {
    font-size: 1rem; margin: 0 0 .2rem; padding-bottom: .15rem;
    border-bottom: 1px solid #eaeef2;
  }
</style>

# Talks, Panels, and Tutorials

<noscript>
  <p><em>Filtering needs JavaScript. The complete list is below, grouped by type.</em></p>
</noscript>

<div class="fbrowse">

  <aside class="fbrowse-nav" aria-label="Filter talks, panels, and tutorials">

    <div class="facet" data-facet="type">
      <button type="button" class="facet-header" aria-expanded="true">Type</button>
      <ul class="facet-options">
        <li><label>
          <input type="checkbox" data-facet="type" value="keynote">
          <span class="facet-label">Keynote Talks</span>
          <span class="facet-count" data-facet="type" data-value="keynote"></span>
        </label></li>
        <li><label>
          <input type="checkbox" data-facet="type" value="invited">
          <span class="facet-label">Invited Talks</span>
          <span class="facet-count" data-facet="type" data-value="invited"></span>
        </label></li>
        <li><label>
          <input type="checkbox" data-facet="type" value="panel">
          <span class="facet-label">Panels</span>
          <span class="facet-count" data-facet="type" data-value="panel"></span>
        </label></li>
        <li><label>
          <input type="checkbox" data-facet="type" value="tutorial">
          <span class="facet-label">Tutorials</span>
          <span class="facet-count" data-facet="type" data-value="tutorial"></span>
        </label></li>
      </ul>
    </div>

    <div class="facet" data-facet="topic">
      <button type="button" class="facet-header" aria-expanded="true">Topics</button>
      <ul class="facet-options">
        {%- for topic in site.data.topics -%}
        {%- assign talk_hits = talks | where_exp: "e", "e.topics contains topic.slug" -%}
        {%- assign panel_hits = panels | where_exp: "e", "e.topics contains topic.slug" -%}
        {%- assign total_hits = talk_hits.size | plus: panel_hits.size -%}
        {%- if total_hits > 0 -%}
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
        <input type="search" id="fbrowse-search" aria-label="Search talks, panels, and tutorials"
               placeholder="Search title, venue, note&hellip;">
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
      Try removing a type/topic filter or broadening the search.
    </div>

    {%- for category in site.data.talks.categories -%}
    {%- assign in_category = talks | where: "category", category.slug -%}
    <section class="fgroup">
      <h2>{{ category.name }}</h2>
      <ul class="talk-list">
        {%- for entry in in_category -%}
        {%- assign facet_text = "" -%}
        {%- for slug in entry.topics -%}
          {%- assign t = site.data.topics | where: "slug", slug | first -%}
          {%- assign facet_text = facet_text | append: " " | append: t.name -%}
        {%- endfor -%}
        {%- assign searchable = entry.what | append: " " | append: entry.venue | append: " " | append: entry.note | append: " " | append: facet_text -%}
        <li class="fitem"
            id="{{ entry.id }}"
            data-facet-type="{{ entry.category }}"
            data-facet-topic="{{ entry.topics | join: ' ' }}"
            data-search="{{ searchable | strip_newlines | downcase | escape }}">
          <span class="talk-title">{{ entry.what }}</span>
          <span class="talk-year">{{ entry.start }}</span>
          <span class="talk-meta">{{ entry.venue }}</span>
          <span class="talk-foot">
            <span class="talk-type">{{ category.name }}</span>
            {%- for slug in entry.topics -%}
              {%- assign topic = site.data.topics | where: "slug", slug | first -%}
            <span class="talk-tag">{{ topic.name | default: slug }}</span>
            {%- endfor -%}
            {%- if entry.links -%}
            <span class="talk-links">
              {%- for link in entry.links -%}<a href="{{ link.url }}">[{{ link.label }}]</a>{% endfor -%}
            </span>
            {%- endif -%}
            {%- if entry.note -%}
            <span class="talk-note">{{ entry.note }}</span>
            {%- endif -%}
          </span>
        </li>
        {%- endfor -%}
      </ul>
    </section>
    {%- endfor -%}

    <section class="fgroup">
      <h2>Panels</h2>
      <ul class="talk-list">
        {%- for entry in panels -%}
        {%- assign facet_text = "" -%}
        {%- for slug in entry.topics -%}
          {%- assign t = site.data.topics | where: "slug", slug | first -%}
          {%- assign facet_text = facet_text | append: " " | append: t.name -%}
        {%- endfor -%}
        {%- assign searchable = entry.what | append: " " | append: entry.venue | append: " " | append: entry.note | append: " " | append: facet_text -%}
        <li class="fitem"
            id="{{ entry.id }}"
            data-facet-type="panel"
            data-facet-topic="{{ entry.topics | join: ' ' }}"
            data-search="{{ searchable | strip_newlines | downcase | escape }}">
          <span class="talk-title">{{ entry.what }}</span>
          <span class="talk-year">{{ entry.start }}</span>
          <span class="talk-meta">{{ entry.venue }}</span>
          <span class="talk-foot">
            <span class="talk-type">Panels</span>
            {%- for slug in entry.topics -%}
              {%- assign topic = site.data.topics | where: "slug", slug | first -%}
            <span class="talk-tag">{{ topic.name | default: slug }}</span>
            {%- endfor -%}
            {%- if entry.links -%}
            <span class="talk-links">
              {%- for link in entry.links -%}<a href="{{ link.url }}">[{{ link.label }}]</a>{% endfor -%}
            </span>
            {%- endif -%}
            {%- if entry.note -%}
            <span class="talk-note">{{ entry.note }}</span>
            {%- endif -%}
          </span>
        </li>
        {%- endfor -%}
      </ul>
    </section>

  </div>
</div>

{% include facet-ui.html %}
