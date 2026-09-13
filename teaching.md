---
layout: default
title: Mentoring and Teaching
---

{%- assign allowed = "mentoring|teaching|competition|outreach" | split: "|" -%}

<style>
  .teach-list {
    list-style: none;
    margin: 0;
    padding: 0;
  }
  .teach-list > li {
    padding: .45rem 0;
    border-top: 1px solid #f0f2f4;
    font-size: .88rem;
    line-height: 1.45;
  }
  .teach-list > li:first-child {
    border-top: none;
  }
  .teach-role {
    font-style: italic;
  }
  .teach-note {
    display: block;
    color: #57606a;
    font-size: .92em;
  }
  .teach-links {
    font-size: .85em;
    white-space: nowrap;
  }
  .teach-links a {
    text-decoration: none;
  }
  .teach-links a:hover {
    text-decoration: underline;
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

# Mentoring and Teaching

<noscript>
  <p><em>Filtering needs JavaScript. The complete list is below, grouped by kind.</em></p>
</noscript>

<div class="fbrowse">

  <aside class="fbrowse-nav" aria-label="Filter mentoring and teaching entries">

    <div class="facet" data-facet="type">
      <button type="button" class="facet-header" aria-expanded="true">Type</button>
      <ul class="facet-options">
        {%- for category in site.data.service.categories -%}
        {%- if allowed contains category.slug -%}
        <li><label>
          <input type="checkbox" data-facet="type" value="{{ category.slug }}">
          <span class="facet-label">{{ category.name }}</span>
          <span class="facet-count" data-facet="type" data-value="{{ category.slug }}"></span>
        </label></li>
        {%- endif -%}
        {%- endfor -%}
      </ul>
    </div>

  </aside>

  <div class="fbrowse-main">

    <div class="fbrowse-bar">
      <div class="fbrowse-search">
        <input type="search" id="fbrowse-search" aria-label="Search mentoring and teaching entries"
               placeholder="Search roles, institutions, notes...">
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
      Try removing a filter or broadening the search.
    </div>

    {%- for category in site.data.service.categories -%}
    {%- if allowed contains category.slug -%}
    {%- assign in_category = site.data.service.entries | where: "category", category.slug -%}
    <section class="fgroup">
      <h2>{{ category.name }}</h2>
      <ul class="teach-list">
        {%- for entry in in_category -%}
        {%- assign search_text = entry.role | append: " " | append: entry.what | append: " " | append: entry.note -%}
        <li class="fitem"
            data-facet-type="{{ entry.category }}"
            data-search="{{ search_text | strip_newlines | downcase | escape }}">
          {%- if entry.role %}<span class="teach-role">{{ entry.role }}</span>, {% endif -%}
          {{ entry.what }}
          {%- if entry.start != "unknown" %}, {{ entry.start }}{% if entry.end == "ongoing" %}&ndash;{% elsif entry.end != entry.start %}&ndash;{{ entry.end }}{% endif %}{% endif -%}
          {%- if entry.links %}<span class="teach-links">
            {%- for link in entry.links %} <a href="{{ link.url }}">[{{ link.label }}]</a>{% endfor -%}
          </span>{% endif -%}
          {%- if entry.note %}<span class="teach-note">{{ entry.note }}</span>{% endif -%}
        </li>
        {%- endfor -%}
      </ul>
    </section>
    {%- endif -%}
    {%- endfor -%}

  </div>
</div>

{% include facet-ui.html %}
