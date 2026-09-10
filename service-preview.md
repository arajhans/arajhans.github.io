---
layout: default
title: Professional Service (data-driven preview)
---

<!--
  PREVIEW PAGE - not linked from anywhere, deliberately not replacing service.md yet.

  Everything below is rendered from _data/service.yml + _data/topics.yml. There is no
  hand-written content in this file: no list of conferences, no dates, no topic
  headings. That is the whole point. Adding a PC membership means one entry in the
  YAML, and it appears here, under every topic it carries, with no chance of the
  index.md-vs-service.md divergence that this replaces.

  Three facets here, because service entries carry `category`, `topics` and `series`.
  publications-preview.md exercises all nine. The left nav, search, chips, counts and
  URL state all come from the shared _includes/facet-ui.html, so the two pages cannot
  drift in behaviour - the previous version of this page had its own copy of the
  filter script, which is how it ended up single-select while nothing else was.

  Groups are kept even though Type is a filter: 57 entries in one flat list is hard to
  scan, and the category headings carry meaning ("Editorial", "Program Committees").
  Publications go the other way - flat and newest-first - because there the year is
  the thing you scan by.

  Once reviewed, this becomes service.md and the filename disappears.
-->

{%- assign entries = site.data.service.entries -%}

<style>
  .service-list { list-style: none; margin: 0; padding: 0; }
  .service-list > li {
    padding: .35rem 0; border-top: 1px solid #f0f2f4; font-size: .88rem; line-height: 1.4;
  }
  .service-list > li:first-child { border-top: none; }
  .fgroup { margin-top: 1.25rem; }
  .fgroup > h2 {
    font-size: 1rem; margin: 0 0 .2rem; padding-bottom: .15rem;
    border-bottom: 1px solid #eaeef2;
  }
  .service-list .role { font-style: italic; }
  .service-list .dates { color: #57606a; white-space: nowrap; font-variant-numeric: tabular-nums; }
  .service-list .note { color: #57606a; font-size: .92em; display: block; }
  .service-list .links { font-size: .85em; white-space: nowrap; }
  .service-list .links a { text-decoration: none; }
  .service-list .links a:hover { text-decoration: underline; }
</style>

# Professional Service

<noscript>
  <p><em>Filtering needs JavaScript. The complete list is below, grouped by kind.</em></p>
</noscript>

<div class="fbrowse">

  <aside class="fbrowse-nav" aria-label="Filter service entries">

    <div class="facet" data-facet="type">
      <button type="button" class="facet-header" aria-expanded="true">Type</button>
      <ul class="facet-options">
        {%- for category in site.data.service.categories %}
        {%- assign hits = entries | where: "category", category.slug %}
        {%- if hits.size > 0 %}
        <li><label>
          <input type="checkbox" data-facet="type" value="{{ category.slug }}">
          <span class="facet-label">{{ category.name }}</span>
          <span class="facet-count" data-facet="type" data-value="{{ category.slug }}"></span>
        </label></li>
        {%- endif %}
        {%- endfor %}
      </ul>
    </div>

    <div class="facet" data-facet="topic">
      <button type="button" class="facet-header" aria-expanded="true">Topics</button>
      <ul class="facet-options">
        {%- for topic in site.data.topics %}
        {%- assign hits = entries | where_exp: "e", "e.topics contains topic.slug" %}
        {%- if hits.size > 0 %}
        <li><label title="{{ topic.blurb | strip_newlines | strip | escape }}">
          <input type="checkbox" data-facet="topic" value="{{ topic.slug }}">
          <span class="facet-label">{{ topic.name }}</span>
          <span class="facet-count" data-facet="topic" data-value="{{ topic.slug }}"></span>
        </label></li>
        {%- endif %}
        {%- endfor %}
      </ul>
    </div>

    <!-- Venue series, shared with publications.yml through _data/venues.yml. This is
         the facet that makes the two lists add up: 27 service entries carry a
         `series`, and HSCC alone is a PC seat, an Awards Chair term and a Demo and
         Poster Chair term here plus one paper there. Entries with no venue - the
         mentoring, teaching and outreach - simply drop out when one is selected. -->
    <div class="facet" data-facet="venue" data-collapsed="true">
      <button type="button" class="facet-header" aria-expanded="false">Venue</button>
      <ul class="facet-options">
        {%- for venue in site.data.venues %}
        {%- assign hits = entries | where: "series", venue.slug %}
        {%- if hits.size > 0 %}
        <li><label title="{{ venue.name | escape }}">
          <input type="checkbox" data-facet="venue" value="{{ venue.slug }}">
          <span class="facet-label">{{ venue.acronym | default: venue.name }}</span>
          <span class="facet-count" data-facet="venue" data-value="{{ venue.slug }}"></span>
        </label></li>
        {%- endif %}
        {%- endfor %}
      </ul>
    </div>

  </aside>

  <div class="fbrowse-main">

    <div class="fbrowse-bar">
      <div class="fbrowse-search">
        <input type="search" id="fbrowse-search" aria-label="Search service entries"
               placeholder="Search role, venue, note&hellip;">
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
      Filters combine as OR inside a section and AND across sections, so adding a
      section narrows the result. Try removing one chip above.
    </div>

    {%- for category in site.data.service.categories %}
    {%- assign in_category = entries | where: "category", category.slug %}
    {%- if in_category.size > 0 %}
    <section class="fgroup" data-category="{{ category.slug }}">
      <h2>{{ category.name }}</h2>
      <ul class="service-list">
        {%- for entry in in_category %}
        {%- comment -%} Topic display names are indexed too, so "formal" finds the
          formal-methods service even where the words are not in the entry text. {%- endcomment -%}
        {%- assign facet_text = "" -%}
        {%- for slug in entry.topics -%}
          {%- assign t = site.data.topics | where: "slug", slug | first -%}
          {%- assign facet_text = facet_text | append: " " | append: t.name -%}
        {%- endfor -%}
        {%- if entry.series -%}
          {%- assign v = site.data.venues | where: "slug", entry.series | first -%}
          {%- assign facet_text = facet_text | append: " " | append: v.name | append: " " | append: v.acronym -%}
        {%- endif -%}
        {%- assign searchable = entry.role | append: " " | append: entry.what | append: " " | append: entry.note | append: " " | append: facet_text -%}
        <li class="fitem"
            data-facet-type="{{ entry.category }}"
            data-facet-topic="{{ entry.topics | join: ' ' }}"
            data-facet-venue="{{ entry.series }}"
            data-search="{{ searchable | strip_newlines | downcase | escape }}">
          {%- if entry.role %}<span class="role">{{ entry.role }}</span>, {% endif -%}
          {{ entry.what | strip_newlines | strip }}
          {%- if entry.start != "unknown" %}
          <span class="dates">
          {%- if entry.end == "ongoing" -%}
            {{ entry.start }}&ndash;
          {%- elsif entry.end == entry.start -%}
            {{ entry.start }}
          {%- else -%}
            {{ entry.start }}&ndash;{{ entry.end }}
          {%- endif -%}
          </span>
          {%- endif -%}
          {%- if entry.links %}
          <span class="links">
            {%- for link in entry.links %} <a href="{{ link.url }}">[{{ link.label }}]</a>{% endfor -%}
          </span>
          {%- endif -%}
          {%- if entry.note %}<span class="note">{{ entry.note | strip_newlines | strip }}</span>{% endif %}
        </li>
        {%- endfor %}
      </ul>
    </section>
    {%- endif %}
    {%- endfor %}

  </div>
</div>

{% include facet-ui.html %}
