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

  Once reviewed, this becomes service.md and the filename disappears.
-->

<style>
  .topic-filter { margin: 1.5em 0; padding: 0; list-style: none; }
  .topic-filter li { display: inline-block; margin: 0 .4em .5em 0; }
  .topic-chip {
    display: inline-block; padding: .3em .85em; border-radius: 2em;
    border: 1px solid #d0d7de; background: #f6f8fa; color: #24292f;
    font-size: .85em; cursor: pointer; text-decoration: none; line-height: 1.6;
  }
  .topic-chip:hover { background: #eaeef2; text-decoration: none; }
  .topic-chip[aria-pressed="true"] { background: #0969da; border-color: #0969da; color: #fff; }
  .topic-chip .count { opacity: .65; margin-left: .35em; font-variant-numeric: tabular-nums; }
  .service-group { margin-top: 2em; }
  .service-group h2 { font-size: 1.25em; padding-bottom: .2em; border-bottom: 1px solid #eaeef2; }
  .service-list { padding-left: 1.2em; }
  .service-list li { margin: .45em 0; }
  .service-list .role { font-style: italic; }
  .service-list .dates { color: #57606a; white-space: nowrap; }
  .service-list .note { color: #57606a; font-size: .92em; display: block; }
  .service-list .links { font-size: .88em; white-space: nowrap; }
  .service-list .links a { text-decoration: none; }
  .service-list .links a:hover { text-decoration: underline; }
  .service-list .tags { font-size: .8em; color: #57606a; }
  [hidden] { display: none !important; }
  .filter-status { color: #57606a; font-size: .9em; }
</style>

# Professional Service

{% assign entries = site.data.service.entries %}

<noscript>
  <p class="filter-status">Topic filtering needs JavaScript; the full list is below.</p>
</noscript>

<ul class="topic-filter" id="topic-filter">
  <li><button class="topic-chip" data-topic="all" aria-pressed="true">All<span class="count">{{ entries | size }}</span></button></li>
  {%- for topic in site.data.topics -%}
    {%- assign matches = entries | where_exp: "e", "e.topics contains topic.slug" -%}
    {%- if matches.size > 0 -%}
  <li><button class="topic-chip" data-topic="{{ topic.slug }}" aria-pressed="false" title="{{ topic.blurb | strip_newlines | strip }}">{{ topic.name }}<span class="count">{{ matches.size }}</span></button></li>
    {%- endif -%}
  {%- endfor -%}
</ul>

{% for category in site.data.service.categories %}
  {%- assign in_category = entries | where: "category", category.slug -%}
  {%- if in_category.size > 0 %}
<section class="service-group" data-category="{{ category.slug }}">
  <h2>{{ category.name }}</h2>
  <ul class="service-list">
    {%- for entry in in_category %}
    <li data-topics="{{ entry.topics | join: ' ' }}">
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
  {%- endif -%}
{% endfor %}

<script>
  (function () {
    var filter = document.getElementById('topic-filter');
    if (!filter) return;
    var chips = filter.querySelectorAll('.topic-chip');
    var items = document.querySelectorAll('.service-list li');
    var groups = document.querySelectorAll('.service-group');

    function apply(topic) {
      items.forEach(function (item) {
        var topics = (item.getAttribute('data-topics') || '').split(' ');
        item.hidden = !(topic === 'all' || topics.indexOf(topic) !== -1);
      });
      // A category with nothing left to show is noise, so hide its heading too.
      groups.forEach(function (group) {
        var visible = group.querySelectorAll('.service-list li:not([hidden])');
        group.hidden = visible.length === 0;
      });
      chips.forEach(function (chip) {
        chip.setAttribute('aria-pressed', chip.dataset.topic === topic ? 'true' : 'false');
      });
    }

    chips.forEach(function (chip) {
      chip.addEventListener('click', function () {
        var topic = chip.dataset.topic;
        // Reflected in the hash so a filtered view is shareable and survives reload.
        history.replaceState(null, '', topic === 'all' ? location.pathname : '#' + topic);
        apply(topic);
      });
    });

    var initial = (location.hash || '').replace('#', '');
    var known = Array.prototype.map.call(chips, function (c) { return c.dataset.topic; });
    apply(known.indexOf(initial) !== -1 ? initial : 'all');
  })();
</script>
