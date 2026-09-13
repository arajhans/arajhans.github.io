---
layout: default
title: Professional Experience
---

{%- assign entries = site.data.experience.entries | sort: "start" | reverse -%}

<style>
  .exp-list {
    list-style: none;
    margin: 0;
    padding: 0;
  }
  .exp-list > li {
    padding: .8rem 0;
    border-top: 1px solid #eaeef2;
  }
  .exp-list > li:first-child {
    border-top: none;
  }
  .exp-head {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    gap: .35rem .75rem;
    align-items: baseline;
  }
  .exp-org {
    font-size: 1rem;
    font-weight: 600;
    color: #18212b;
  }
  .exp-years {
    color: #57606a;
    font-size: .86rem;
    font-variant-numeric: tabular-nums;
    white-space: nowrap;
  }
  .exp-location {
    margin-top: .12rem;
    color: #556270;
    font-size: .88rem;
  }
  .exp-roles,
  .exp-summary {
    margin: .45rem 0 0 1rem;
  }
  .exp-roles li,
  .exp-summary li {
    margin: .2rem 0;
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

# Professional Experience

<noscript>
  <p><em>Filtering needs JavaScript. The complete list is below, grouped by sector.</em></p>
</noscript>

<div class="fbrowse">

  <aside class="fbrowse-nav" aria-label="Filter experience entries">

    <div class="facet" data-facet="type">
      <button type="button" class="facet-header" aria-expanded="true">Type</button>
      <ul class="facet-options">
        {%- for category in site.data.experience.categories -%}
        <li><label>
          <input type="checkbox" data-facet="type" value="{{ category.slug }}">
          <span class="facet-label">{{ category.name }}</span>
          <span class="facet-count" data-facet="type" data-value="{{ category.slug }}"></span>
        </label></li>
        {%- endfor -%}
      </ul>
    </div>

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
        <input type="search" id="fbrowse-search" aria-label="Search experience entries"
               placeholder="Search organizations, roles, summary...">
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

    {%- for category in site.data.experience.categories -%}
    {%- assign in_category = entries | where: "category", category.slug -%}
    <section class="fgroup">
      <h2>{{ category.name }}</h2>
      <ul class="exp-list">
        {%- for entry in in_category -%}
        {%- assign search_text = entry.organization | append: " " | append: entry.location -%}
        {%- for role in entry.roles -%}
          {%- assign search_text = search_text | append: " " | append: role.title -%}
        {%- endfor -%}
        {%- for line in entry.summary -%}
          {%- assign search_text = search_text | append: " " | append: line -%}
        {%- endfor -%}
        {%- for slug in entry.topics -%}
          {%- assign topic = site.data.topics | where: "slug", slug | first -%}
          {%- assign search_text = search_text | append: " " | append: topic.name -%}
        {%- endfor -%}
        <li class="fitem"
            data-facet-type="{{ entry.category }}"
            data-facet-topic="{{ entry.topics | join: ' ' }}"
            data-search="{{ search_text | strip_newlines | downcase | escape }}">
          <div class="exp-head">
            <span class="exp-org">{{ entry.organization }}</span>
            <span class="exp-years">
              {%- if entry.end == "ongoing" -%}
                {{ entry.start }}&ndash;
              {%- elsif entry.end == entry.start -%}
                {{ entry.start }}
              {%- else -%}
                {{ entry.start }}&ndash;{{ entry.end }}
              {%- endif -%}
            </span>
          </div>
          {%- if entry.location %}<div class="exp-location">{{ entry.location }}</div>{% endif -%}
          {%- if entry.roles %}<ul class="exp-roles">
            {%- for role in entry.roles -%}
            <li>{{ role.title }}{% if role.start %}, {{ role.start }}{% if role.end == "ongoing" %}&ndash;{% elsif role.end != role.start %}&ndash;{{ role.end }}{% endif %}{% endif %}</li>
            {%- endfor -%}
          </ul>{% endif -%}
          {%- if entry.summary %}<ul class="exp-summary">
            {%- for line in entry.summary -%}
            <li>{{ line }}</li>
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
