---
layout: default
title: Publications (faceted preview)
---

<!--
  PREVIEW PAGE - not linked from anywhere, does not replace publications.md yet.

  Rendered entirely from _data/publications.yml + topics.yml + orgs.yml +
  distinctions.yml + venues.yml. No titles, venues, years, authors or tags are
  written here.

  This page exercises every facet at once, which service.yml cannot: service entries
  carry category, topics and series, while publication entries add orgs, mentored,
  distinctions and authors. All nine sections in the left nav are therefore real here,
  not mocked up.

  Four of the nine are DERIVED, never stored:
    Collaboration - external when `orgs` is non-empty. There is no `external: true`
                    field, because "external" is relative to where the author was at
                    the time (Penn, then CMU, then MathWorks) and a boolean frozen at
                    entry time would quietly rot.
    Mentorship    - present when `mentored` is non-empty; `mentored` is itself checked
                    to be a subset of `authors`, so it cannot drift.
    Outcome       - read off each distinction's `status`, which is what keeps a
                    finalist from rendering as a win.
    Coauthors     - the union of `authors` minus the site owner, restricted to people
                    with more than one shared work. No coauthor list is maintained
                    anywhere; check_data.py instead warns when one person is written
                    two ways, since "P. J. Mosterman" and "Pieter J. Mosterman" would
                    otherwise render as two people with one paper each.

  Venue is the one addition that is NOT derived and could not be: `venue:` is prose
  about one instance ("21st ... (HSCC)", "... co-located with CAV, Snowbird, UT"), so
  entries carry `series: hscc` beside it. That slug is shared with service.yml, which
  is the point - HSCC here is one paper, an Awards Chair term, a Demo and Poster Chair
  term and a PC seat, four facts that previously lived in two files with nothing
  connecting them.
-->

{%- assign entries = site.data.publications.entries -%}
{%- assign undated = entries | where: "year", "unknown" -%}
{%- assign dated = entries | where_exp: "e", "e.year != 'unknown'" | sort: "year" | reverse -%}

<style>
  /* Compact rows. The earlier preview used a wide chip bar above a bulleted list,
     which pushed content down the page and wasted the horizontal space a left nav
     puts to work. One entry is a hairline-separated block of at most three lines. */
  .pub-list { list-style: none; margin: 0; padding: 0; }
  .pub-list > li {
    padding: .5rem 0; border-top: 1px solid #eaeef2;
    display: grid; grid-template-columns: 1fr auto; gap: 0 .75rem; align-items: baseline;
  }
  .pub-list > li:first-child { border-top: none; }
  .pub-title { font-size: .95rem; font-weight: 600; line-height: 1.3; }
  .pub-year {
    font-size: .8rem; color: #57606a; font-variant-numeric: tabular-nums;
    white-space: nowrap; text-align: right;
  }
  .pub-meta {
    grid-column: 1 / -1; font-size: .82rem; color: #57606a; line-height: 1.4;
    margin-top: .1rem;
  }
  .pub-meta .me { font-weight: 600; color: #24292f; }
  .pub-venue { font-style: italic; }
  .pub-foot {
    grid-column: 1 / -1; margin-top: .25rem;
    display: flex; flex-wrap: wrap; gap: .3rem; align-items: center;
  }
  .pub-badge {
    font-size: .7rem; padding: .05rem .45rem; border-radius: 2em;
    border: 1px solid #d0d7de; background: #f6f8fa; color: #57606a;
    text-transform: uppercase; letter-spacing: .03em;
  }
  .pub-tag {
    font-size: .72rem; padding: .05rem .45rem; border-radius: 2em;
    background: #ddf4ff; color: #0550ae;
  }
  .pub-award {
    font-size: .72rem; padding: .05rem .45rem; border-radius: 2em;
    background: #fff8c5; color: #7d4e00;
  }
  .pub-award[data-status="finalist"], .pub-award[data-status="selected"] {
    background: #fff; border: 1px solid #d4a72c; color: #7d4e00;
  }
  .pub-links { font-size: .75rem; }
  .pub-links a { text-decoration: none; }
  .pub-links a:hover { text-decoration: underline; }
  .pub-rel { font-size: .75rem; color: #57606a; font-style: italic; }
</style>

# Publications

<noscript>
  <p><em>Filtering needs JavaScript. The complete list is below, newest first.</em></p>
</noscript>

<div class="fbrowse">

  <aside class="fbrowse-nav" aria-label="Filter publications">

    <div class="facet" data-facet="type">
      <button type="button" class="facet-header" aria-expanded="true">Type</button>
      <ul class="facet-options">
        {%- for category in site.data.publications.categories %}
        <li><label>
          <input type="checkbox" data-facet="type" value="{{ category.slug }}">
          <span class="facet-label">{{ category.name }}</span>
          <span class="facet-count" data-facet="type" data-value="{{ category.slug }}"></span>
        </label></li>
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

    <div class="facet" data-facet="collab">
      <button type="button" class="facet-header" aria-expanded="true">Collaboration</button>
      <ul class="facet-options">
        <li><label title="At least one coauthor from outside MathWorks, derived from a non-empty orgs list.">
          <input type="checkbox" data-facet="collab" value="external">
          <span class="facet-label">External coauthors</span>
          <span class="facet-count" data-facet="collab" data-value="external"></span>
        </label></li>
        <li><label title="Every coauthor was at MathWorks; nothing is set to false to say so.">
          <input type="checkbox" data-facet="collab" value="internal">
          <span class="facet-label">MathWorks only</span>
          <span class="facet-count" data-facet="collab" data-value="internal"></span>
        </label></li>
      </ul>
    </div>

    <div class="facet" data-facet="mentored">
      <button type="button" class="facet-header" aria-expanded="true">Mentorship</button>
      <ul class="facet-options">
        <li><label title="Includes a student or intern coauthor listed in `mentored`.">
          <input type="checkbox" data-facet="mentored" value="yes">
          <span class="facet-label">Mentored coauthor</span>
          <span class="facet-count" data-facet="mentored" data-value="yes"></span>
        </label></li>
      </ul>
    </div>

    <div class="facet" data-facet="award">
      <button type="button" class="facet-header" aria-expanded="true">Recognition</button>
      <ul class="facet-options">
        {%- for kind in site.data.distinctions %}
        <li><label title="{{ kind.blurb | strip_newlines | strip | escape }}">
          <input type="checkbox" data-facet="award" value="{{ kind.slug }}">
          <span class="facet-label">{{ kind.name }}</span>
          <span class="facet-count" data-facet="award" data-value="{{ kind.slug }}"></span>
        </label></li>
        {%- endfor %}
      </ul>
    </div>

    <div class="facet" data-facet="outcome">
      <button type="button" class="facet-header" aria-expanded="true">Outcome</button>
      <ul class="facet-options">
        {%- assign outcomes = "won,finalist,selected" | split: "," %}
        {%- for status in outcomes %}
        <li><label>
          <input type="checkbox" data-facet="outcome" value="{{ status }}">
          <span class="facet-label">{{ status | capitalize }}</span>
          <span class="facet-count" data-facet="outcome" data-value="{{ status }}"></span>
        </label></li>
        {%- endfor %}
      </ul>
    </div>

    <!-- Venue series, in venues.yml order so conferences, workshops and journals stay
         grouped. `series` is a single slug beside the prose `venue:` string, because
         the prose is about one instance - the ordinal, the co-location and the city
         are worth printing and differ every time, so it cannot also be the key. -->
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

    {%- comment -%}
      Coauthors, most-shared-work first. Two things are going on here.

      FLATTENING. `map: "authors"` gives a list of lists; joining it produces one flat
      delimited string because Ruby's Array#join recurses into nested arrays. That is
      the only way Liquid can flatten, and the build check asserts a known slug is
      present so this silently returning nothing would fail CI rather than quietly
      emptying the section.

      ORDERING. Liquid cannot sort by a computed number, so each name is prefixed with
      a zero-padded 99-minus-count. Ascending string sort then means descending count,
      and alphabetical within a count. The prefix is sliced back off to get the name.

      ONLY RECURRING COAUTHORS. 88 of the 102 names appear exactly once, most of them
      cosignatories of a single 25-author workshop report. 102 checkboxes with 88
      reading "1" is a wall, not a filter; one-off coauthors stay findable by search,
      which already indexes every author name.
    {%- endcomment -%}
    {%- assign all_authors = entries | map: "authors" | join: "|" | split: "|" -%}
    {%- assign distinct_authors = all_authors | uniq -%}
    {%- assign ranked = "" -%}
    {%- for name in distinct_authors -%}
      {%- unless name == "Akshay Rajhans" -%}
        {%- assign n = 0 -%}
        {%- for other in all_authors -%}
          {%- if other == name %}{% assign n = n | plus: 1 %}{% endif -%}
        {%- endfor -%}
        {%- if n > 1 -%}
          {%- assign key = 99 | minus: n | prepend: "0" | slice: -2, 2 -%}
          {%- assign ranked = ranked | append: "|" | append: key | append: name -%}
        {%- endif -%}
      {%- endunless -%}
    {%- endfor -%}
    {%- assign ranked = ranked | remove_first: "|" | split: "|" | sort -%}

    <div class="facet" data-facet="coauthor" data-collapsed="true">
      <button type="button" class="facet-header" aria-expanded="false">Coauthors</button>
      <ul class="facet-options">
        {%- for pair in ranked %}
        {%- assign name = pair | slice: 2, 200 %}
        <li><label>
          <input type="checkbox" data-facet="coauthor" value="{{ name | slugify }}">
          <span class="facet-label">{{ name }}</span>
          <span class="facet-count" data-facet="coauthor" data-value="{{ name | slugify }}"></span>
        </label></li>
        {%- endfor %}
        <li class="facet-note">Coauthors on a single work are not listed; the search
          box finds them by name.</li>
      </ul>
    </div>

    <!-- Collapsed by default: it is the longest section and the least often wanted,
         but it is also the one thing the CV's "more than a dozen coauthor
         affiliations" could never actually answer. -->
    <div class="facet" data-facet="org" data-collapsed="true">
      <button type="button" class="facet-header" aria-expanded="false">Institutions</button>
      <ul class="facet-options">
        {%- for org in site.data.orgs %}
        {%- assign hits = entries | where_exp: "e", "e.orgs contains org.slug" %}
        {%- if hits.size > 0 %}
        <li><label>
          <input type="checkbox" data-facet="org" value="{{ org.slug }}">
          <span class="facet-label">{{ org.name }}</span>
          <span class="facet-count" data-facet="org" data-value="{{ org.slug }}"></span>
        </label></li>
        {%- endif %}
        {%- endfor %}
      </ul>
    </div>

  </aside>

  <div class="fbrowse-main">

    <div class="fbrowse-bar">
      <div class="fbrowse-search">
        <input type="search" id="fbrowse-search" aria-label="Search publications"
               placeholder="Search title, author, venue&hellip;">
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

    <ul class="pub-list">
      {%- assign ordered = undated | concat: dated -%}
      {%- for entry in ordered %}

      {%- comment -%} Derived facet values, computed here and nowhere else. {%- endcomment -%}
      {%- if entry.orgs and entry.orgs != empty %}{% assign collab = "external" %}
      {%- else %}{% assign collab = "internal" %}{% endif -%}
      {%- if entry.mentored and entry.mentored != empty %}{% assign mentored = "yes" %}
      {%- else %}{% assign mentored = "" %}{% endif -%}
      {%- assign award_kinds = "" -%}
      {%- assign award_status = "" -%}
      {%- for d in entry.distinctions -%}
        {%- assign award_kinds = award_kinds | append: d.kind | append: " " -%}
        {%- assign award_status = award_status | append: d.status | append: " " -%}
      {%- endfor -%}
      {%- comment -%}
        Built as its own variable first: piping `append: entry.authors` would append an
        ARRAY, and Liquid stringifies that by running the elements together, so
        "Yi DengAkshay Rajhans" would be searchable but "Yi Deng" would not.
      {%- endcomment -%}
      {%- assign authors_text = entry.authors | join: ", " -%}
      {%- comment -%}
        Search covers the FACET LABELS too, not just the bibliographic fields. Typing
        "formal" should find the formal-methods work and "McMaster" should find the
        McMaster collaborations, even though neither string appears in any title. The
        slug is useless to a human typing, so the display names are what get indexed.
      {%- endcomment -%}
      {%- assign facet_text = "" -%}
      {%- for slug in entry.topics -%}
        {%- assign t = site.data.topics | where: "slug", slug | first -%}
        {%- assign facet_text = facet_text | append: " " | append: t.name -%}
      {%- endfor -%}
      {%- for slug in entry.orgs -%}
        {%- assign o = site.data.orgs | where: "slug", slug | first -%}
        {%- assign facet_text = facet_text | append: " " | append: o.name -%}
      {%- endfor -%}
      {%- for d in entry.distinctions -%}
        {%- assign facet_text = facet_text | append: " " | append: d.name -%}
      {%- endfor -%}
      {%- comment -%}
        Both venue forms are indexed, because neither is reliably in the prose. The
        Winter Simulation Conference paper never writes "WSC", and the CSM paper
        never writes "Control Systems Magazine" as an acronym - so searching either
        way has to work.
      {%- endcomment -%}
      {%- if entry.series -%}
        {%- assign v = site.data.venues | where: "slug", entry.series | first -%}
        {%- assign facet_text = facet_text | append: " " | append: v.name | append: " " | append: v.acronym -%}
      {%- endif -%}
      {%- comment -%}
        Coauthor slugs must be generated the same way in the item and in the nav, so
        both sides use `slugify` on the name and nothing else does the conversion.
      {%- endcomment -%}
      {%- assign coauthor_slugs = "" -%}
      {%- for author in entry.authors -%}
        {%- unless author == "Akshay Rajhans" -%}
          {%- comment -%} Slugify the name ALONE. Piping the accumulated string
            through slugify would collapse the separating spaces into hyphens and
            fuse every coauthor into one meaningless slug. {%- endcomment -%}
          {%- assign one = author | slugify -%}
          {%- assign coauthor_slugs = coauthor_slugs | append: " " | append: one -%}
        {%- endunless -%}
      {%- endfor -%}
      {%- assign searchable = entry.title | append: " " | append: authors_text | append: " " | append: entry.venue | append: " " | append: entry.year | append: " " | append: facet_text -%}

      <li class="fitem"
          id="{{ entry.id }}"
          data-facet-type="{{ entry.category }}"
          data-facet-topic="{{ entry.topics | join: ' ' }}"
          data-facet-collab="{{ collab }}"
          data-facet-mentored="{{ mentored }}"
          data-facet-award="{{ award_kinds | strip }}"
          data-facet-outcome="{{ award_status | strip }}"
          data-facet-org="{{ entry.orgs | join: ' ' }}"
          data-facet-venue="{{ entry.series }}"
          data-facet-coauthor="{{ coauthor_slugs | strip }}"
          data-search="{{ searchable | downcase | escape }}">
        <span class="pub-title">{{ entry.title }}</span>
        <span class="pub-year">{% if entry.year == "unknown" %}&mdash;{% else %}{{ entry.year }}{% endif %}</span>
        <span class="pub-meta">
          {%- for author in entry.authors -%}
            {%- if author == "Akshay Rajhans" -%}<span class="me">{{ author }}</span>
            {%- else -%}{{ author }}{%- endif -%}
            {%- unless forloop.last %}, {% endunless -%}
          {%- endfor %}.
          <span class="pub-venue">{{ entry.venue }}</span>
        </span>
        <span class="pub-foot">
          {%- assign cat = site.data.publications.categories | where: "slug", entry.category | first -%}
          <span class="pub-badge">{{ cat.name | default: entry.category }}</span>
          {%- for slug in entry.topics -%}
            {%- assign topic = site.data.topics | where: "slug", slug | first %}
          <span class="pub-tag">{{ topic.name | default: slug }}</span>
          {%- endfor -%}
          {%- for d in entry.distinctions %}
          <span class="pub-award" data-status="{{ d.status }}">{{ d.name }}{% unless d.status == "won" %} ({{ d.status }}){% endunless %}</span>
          {%- endfor -%}
          {%- if entry.links %}
          <span class="pub-links">
            {%- for link in entry.links %}<a href="{{ link.url }}">[{{ link.label }}]</a>{% endfor -%}
          </span>
          {%- endif -%}
          {%- for rel in entry.related %}
            {%- assign target = entries | where: "id", rel.id | first %}
          <span class="pub-rel">{{ rel.how | replace: "-", " " }} <a href="#{{ rel.id }}">{{ target.venue | default: rel.id | truncate: 40 }}</a></span>
          {%- endfor -%}
          {%- for extra in entry.also_appeared %}
          <span class="pub-rel">also presented: {{ extra.venue | truncate: 60 }} ({{ extra.year }})</span>
          {%- endfor -%}
        </span>
      </li>
      {%- endfor %}
    </ul>

  </div>
</div>

{% include facet-ui.html %}
