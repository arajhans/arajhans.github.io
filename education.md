---
layout: default
title: Education
---

{%- assign entries = site.data.education.entries | sort: "start" | reverse -%}

<style>
  .edu-list {
    list-style: none;
    margin: 0;
    padding: 0;
  }
  .edu-list > li {
    padding: .8rem 0;
    border-top: 1px solid #eaeef2;
  }
  .edu-list > li:first-child {
    border-top: none;
  }
  .edu-degree {
    font-size: 1rem;
    font-weight: 600;
    color: #18212b;
  }
  .edu-meta,
  .edu-detail {
    margin-top: .15rem;
    color: #556270;
  }
  .edu-coursework {
    margin: .45rem 0 0 1rem;
  }
  .fgroup {
    margin-top: 1.25rem;
  }
  .fgroup > h2 {
    font-size: 1rem;
    margin: 0 0 .2rem;
    padding-bottom: .15rem;
    border-bottom: 1px solid #eaeef2;
  }
</style>

# Education

<noscript>
  <p><em>Filtering needs JavaScript. The complete list is below, grouped by degree.</em></p>
</noscript>

<div class="fbrowse">

  <aside class="fbrowse-nav" aria-label="Filter education entries">

    <div class="facet" data-facet="type">
      <button type="button" class="facet-header" aria-expanded="true">Type</button>
      <ul class="facet-options">
        {%- for category in site.data.education.categories -%}
        <li><label>
          <input type="checkbox" data-facet="type" value="{{ category.slug }}">
          <span class="facet-label">{{ category.name }}</span>
          <span class="facet-count" data-facet="type" data-value="{{ category.slug }}"></span>
        </label></li>
        {%- endfor -%}
      </ul>
    </div>

  </aside>

  <div class="fbrowse-main">

    <div class="fbrowse-bar">
      <div class="fbrowse-search">
        <input type="search" id="fbrowse-search" aria-label="Search education entries"
               placeholder="Search institution, field, thesis...">
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
      Try removing a degree filter or broadening the search.
    </div>

    {%- for category in site.data.education.categories -%}
    {%- assign in_category = entries | where: "category", category.slug -%}
    <section class="fgroup">
      <h2>{{ category.name }}</h2>
      <ul class="edu-list">
        {%- for entry in in_category -%}
        {%- assign search_text = entry.degree | append: " " | append: entry.field | append: " " | append: entry.institution | append: " " | append: entry.location | append: " " | append: entry.thesis_title | append: " " | append: entry.advisor -%}
        {%- for item in entry.coursework -%}
          {%- assign search_text = search_text | append: " " | append: item -%}
        {%- endfor -%}
        <li class="fitem"
            data-facet-type="{{ entry.category }}"
            data-search="{{ search_text | strip_newlines | downcase | escape }}">
          <div class="edu-degree">{{ entry.degree }}, {{ entry.field }}</div>
          <div class="edu-meta">{{ entry.institution }}{% if entry.location %}, {{ entry.location }}{% endif %} | {{ entry.start }}&ndash;{{ entry.end }}</div>
          {%- if entry.thesis_title %}<div class="edu-detail"><strong>Thesis:</strong> {{ entry.thesis_title }}</div>{% endif -%}
          {%- if entry.advisor %}<div class="edu-detail"><strong>Advisor:</strong> {{ entry.advisor }}</div>{% endif -%}
          {%- if entry.committee %}<div class="edu-detail"><strong>Committee:</strong> {{ entry.committee | join: ", " }}</div>{% endif -%}
          {%- if entry.coursework %}<ul class="edu-coursework">
            {%- for item in entry.coursework -%}
            <li>{{ item }}</li>
            {%- endfor -%}
          </ul>{% endif -%}
        </li>
        {%- endfor -%}
      </ul>
    </section>
    {%- endfor -%}

  </div>
</div>

{% include facet-ui.html %}
