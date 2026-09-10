#!/usr/bin/env python3
"""Validate _data/*.yml against the controlled vocabularies in _data/.

Runs in CI and fails the build on a problem. The point is to make tag rot
impossible: without this, `cps` / `CPS` / `cyber-physical` coexist and filtering
silently returns partial results, which is worse than an error because nobody
notices. The same argument applies to institution names, where the CV already
shows the failure mode ("University of Bergamo" written out by hand each time).

Vocabularies (each a flat list of {slug, name}):
  topics.yml         what work is about        referenced by `topics:`
  orgs.yml           external institutions     referenced by `orgs:`
  distinctions.yml   kinds of award/honour     referenced by `distinctions[].kind`

Entry files declare their own contract with a top-level `required:` list, so a new
data file with a different shape needs no change here. Publications require
title/authors/venue/year; service requires what/start/end.

Checks:
  * every facet value resolves to a slug declared in the matching vocabulary
  * vocabularies have no duplicate or malformed slugs, and all have display names
  * every entry has its file's required fields and a declared category
  * start/end/year are a 4-digit year, `ongoing`, or `unknown`; end >= start
  * distinctions carry {kind, name, status} with status in won/finalist/selected
  * every `mentored` name also appears in `authors`, so the two cannot drift
  * links are a list of {label, url}, non-duplicated, either absolute http(s) or
    site-relative ('/files/...'), and a site-relative one must exist on disk
  * `id` is unique across all data files, so entries can be cross-referenced
  * `also_appeared` entries carry venue/year/track - the same work at a second venue
  * `related` targets resolve to a real id, are not self-referential, and use a
    declared relation kind
  * a declared slug that nothing uses is reported (warning, not failure)

ONE WORK OR TWO? The two mechanisms above answer different questions and must not
be confused, because they count differently. The discriminator is the DOI:

  A SEPARATE DOI IN A SEPARATE VENUE IS A SEPARATE ARTIFACT.

  `related`        Distinct DOIs. SEPARATE entries, each counted, cross-linked so a
                   reader can see they are the same line of work. The L-CSS paper
                   and its ACC proceedings version have their own DOIs and are two
                   citable artifacts; so are a conference paper and its later
                   rewritten journal version.

  `also_appeared`  No second DOI. ONE entry, counted ONCE, with the additional
                   appearance recorded. A journal-first *presentation* is a talk
                   slot, not a proceedings entry - nothing new was published, so
                   counting it again would inflate the list.

This is deliberately mechanical rather than a judgement call: "does it have its own
DOI" can be checked, whereas "is it really the same paper" invites the two
maintained copies of a CV to answer differently. Where a DOI does not exist at all
(older workshop papers, reports), fall back to whether the venue issues separate
proceedings.

Usage:  python scripts/check_data.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml
except ModuleNotFoundError:
    sys.exit("error: PyYAML is required (pip install pyyaml)")

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "_data"

SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SENTINELS = {"ongoing", "unknown"}

# filename -> the entry field that references it
VOCABULARIES = {
    "topics.yml": "topics",
    "orgs.yml": "orgs",
    "distinctions.yml": "distinctions",
}

# Facets that are a plain list of slugs. `distinctions` is deliberately not here:
# it needs a per-entry name and won/finalist status, so it is a list of mappings.
SLUG_FACETS = ("topics", "orgs")

DISTINCTION_STATUSES = {"won", "finalist", "selected"}
DEFAULT_REQUIRED = ("category", "what", "start", "end", "topics")
YEAR_FIELDS = ("start", "end", "year")

# How one entry relates to another, and the inverse the renderer shows on the far
# side. Relations are authored in ONE direction only - writing both would be two
# facts to keep in step, and they would drift exactly like the CV and the site did.
# The renderer derives the reverse from this table, so it is the single definition.
RELATION_INVERSES = {
    "revises": "revised-as",        # later rewrite of the same result for a new audience
    "extends": "extended-by",       # later, longer development of an earlier paper
    "presented-as": "presented-at",  # same result, second archival venue with its own DOI
    "companion": "companion",       # symmetric: different artifact types, same venue
}
RELATION_KINDS = set(RELATION_INVERSES) | set(RELATION_INVERSES.values())

# Why a work appears somewhere a second time WITHOUT a second DOI. If a track issues
# its own proceedings entry it is not one of these - it is a separate entry.
APPEARANCE_TRACKS = {"journal-first", "presentation", "reprint"}

errors: list[str] = []
warnings: list[str] = []
ids: dict[str, str] = {}                        # id -> label that declared it
relations: list[tuple[str, str, str]] = []      # (label, target id, how)


def load(path: Path):
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def load_vocabulary(filename: str) -> set[str]:
    path = DATA / filename
    if not path.exists():
        errors.append(f"_data/{filename} is missing; it defines a vocabulary")
        return set()

    entries = load(path) or []
    if not isinstance(entries, list):
        errors.append(f"{filename}: expected a top-level list of slug entries")
        return set()

    slugs: set[str] = set()
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict) or "slug" not in entry:
            errors.append(f"{filename} entry {index} has no slug")
            continue
        slug = entry["slug"]
        if not SLUG_RE.match(str(slug)):
            errors.append(f"{filename} slug {slug!r} is not lower-case-kebab")
        if slug in slugs:
            errors.append(f"{filename} declares {slug!r} more than once")
        if not entry.get("name"):
            errors.append(f"{filename} slug {slug!r} has no display name")
        slugs.add(slug)
    return slugs


def check_year(value, label: str) -> None:
    if isinstance(value, str) and value in SENTINELS:
        return
    if isinstance(value, int) and 1900 <= value <= 2100:
        return
    errors.append(f"{label}: {value!r} is not a 4-digit year, 'ongoing' or 'unknown'")


def check_links(entry, label: str) -> None:
    """Links are a list of {label, url}, never a bare string.

    A single `url:` field cannot express "the announcement AND the artifact", which
    is a real distinction (a news post about a report is not the report). Entries
    therefore carry a list, and this enforces its shape so the renderer can assume it.
    """
    if "url" in entry:
        errors.append(
            f"{label}: bare 'url' field is not supported; use "
            f"'links: [{{label: ..., url: ...}}]'"
        )

    links = entry.get("links")
    if links is None:
        return
    if not isinstance(links, list):
        errors.append(f"{label}: links must be a list")
        return

    seen: set[str] = set()
    for position, link in enumerate(links):
        where = f"{label} links[{position}]"
        if not isinstance(link, dict):
            errors.append(f"{where}: must be a mapping with label and url")
            continue
        extra = set(link) - {"label", "url"}
        if extra:
            errors.append(f"{where}: unexpected key(s) {sorted(extra)}")
        if not link.get("label"):
            errors.append(f"{where}: missing label - readers need to know what they get")
        url = str(link.get("url", ""))
        if url.startswith("/"):
            # A repo-local asset, e.g. /files/papers/Foo18.pdf. Writing these as
            # site-relative rather than https://arajhans.github.io/... keeps them
            # working if the domain ever changes, and lets the gate do what it
            # cannot do for an external URL: confirm the file is actually there.
            # A silently missing PDF is the exact failure this project is about.
            if not (ROOT / url.lstrip("/")).is_file():
                errors.append(f"{where}: local file {url!r} does not exist")
        elif not url.startswith(("http://", "https://")):
            errors.append(
                f"{where}: url {url!r} must be absolute (http/https) or "
                f"site-relative starting with '/'"
            )
        if url in seen:
            errors.append(f"{where}: duplicate url within the same entry")
        seen.add(url)


def check_slug_facet(entry, field: str, label: str, vocabulary: set[str],
                     used: set[str]) -> None:
    values = entry.get(field)
    if values is None:
        return
    if isinstance(values, str):
        errors.append(f"{label}: {field} must be a list, not a bare string")
        return
    if not isinstance(values, list):
        errors.append(f"{label}: {field} must be a list")
        return

    for value in values:
        used.add(value)
        if value not in vocabulary:
            errors.append(
                f"{label}: unknown {field[:-1]} {value!r} - add it to "
                f"_data/{field}.yml or fix the spelling"
            )
    if len(set(values)) != len(values):
        errors.append(f"{label}: repeats a value in {field}")


def check_distinctions(entry, label: str, vocabulary: set[str],
                       used: set[str]) -> None:
    """Awards are {kind, name, status}, because they are not interchangeable.

    A repeatability *finalist* is not a win, and a CACM Research Highlight is a
    selection rather than an award at all. `status` is required so that no
    rendering can quietly promote a finalist to a winner.
    """
    if "awards" in entry:
        errors.append(
            f"{label}: use 'distinctions' rather than 'awards'; a Research "
            f"Highlight is not an award and a finalist is not a win"
        )

    values = entry.get("distinctions")
    if values is None:
        return
    if not isinstance(values, list):
        errors.append(f"{label}: distinctions must be a list of mappings")
        return

    for position, item in enumerate(values):
        where = f"{label} distinctions[{position}]"
        if not isinstance(item, dict):
            errors.append(f"{where}: must be a mapping with kind, name and status")
            continue
        extra = set(item) - {"kind", "name", "status"}
        if extra:
            errors.append(f"{where}: unexpected key(s) {sorted(extra)}")

        kind = item.get("kind")
        if not kind:
            errors.append(f"{where}: missing kind")
        else:
            used.add(kind)
            if kind not in vocabulary:
                errors.append(
                    f"{where}: unknown kind {kind!r} - add it to "
                    f"_data/distinctions.yml or fix the spelling"
                )

        if not item.get("name"):
            errors.append(
                f"{where}: missing name - the exact wording is the citable part"
            )

        status = item.get("status")
        if status not in DISTINCTION_STATUSES:
            errors.append(
                f"{where}: status {status!r} must be one of "
                f"{sorted(DISTINCTION_STATUSES)}"
            )


def check_appearances(entry, label: str) -> int:
    """`also_appeared` records a second appearance that produced no second DOI.

    Returns how many were declared, so the summary can report works separately from
    appearances - the whole point being that these do NOT add to the publication
    count. A journal-first slot at a conference is a talk about a paper that already
    exists; listing it as a publication is how a CV quietly inflates.
    """
    values = entry.get("also_appeared")
    if values is None:
        return 0
    if not isinstance(values, list):
        errors.append(f"{label}: also_appeared must be a list of mappings")
        return 0

    for position, item in enumerate(values):
        where = f"{label} also_appeared[{position}]"
        if not isinstance(item, dict):
            errors.append(f"{where}: must be a mapping with venue, year and track")
            continue
        extra = set(item) - {"venue", "year", "track", "links", "note"}
        if extra:
            errors.append(f"{where}: unexpected key(s) {sorted(extra)}")
        if not item.get("venue"):
            errors.append(f"{where}: missing venue")
        if "year" in item:
            check_year(item["year"], f"{where} year")
        else:
            errors.append(f"{where}: missing year")

        track = item.get("track")
        if track not in APPEARANCE_TRACKS:
            errors.append(
                f"{where}: track {track!r} must be one of "
                f"{sorted(APPEARANCE_TRACKS)}; if this venue issued its own DOI it "
                f"is a separate entry linked with 'related', not an appearance"
            )
        check_links(item, where)
    return len(values)


def check_related(entry, label: str) -> None:
    """`related` cross-links DISTINCT works; targets are resolved after every file."""
    values = entry.get("related")
    if values is None:
        return
    if not isinstance(values, list):
        errors.append(f"{label}: related must be a list of mappings")
        return

    own_id = entry.get("id")
    seen: set[str] = set()
    for position, item in enumerate(values):
        where = f"{label} related[{position}]"
        if not isinstance(item, dict):
            errors.append(f"{where}: must be a mapping with id and how")
            continue
        extra = set(item) - {"id", "how", "note"}
        if extra:
            errors.append(f"{where}: unexpected key(s) {sorted(extra)}")

        target = item.get("id")
        if not target:
            errors.append(f"{where}: missing id of the related entry")
        else:
            if target == own_id:
                errors.append(f"{where}: entry is related to itself")
            if target in seen:
                errors.append(f"{where}: names {target!r} more than once")
            seen.add(target)

        how = item.get("how")
        if how not in RELATION_KINDS:
            errors.append(
                f"{where}: how {how!r} must be one of {sorted(RELATION_KINDS)}"
            )
        if target and how:
            relations.append((where, str(own_id or label), str(target), str(how)))


def check_id(entry, label: str) -> None:
    """Ids are the only stable way to name an entry.

    The CV's P-numbers cannot do it: they are positional, so they differ between the
    CV (tops out at P28) and index.md (P29), and publications.md skips P7 outright.
    "P6" therefore does not identify a paper. Relations and permalinks need a name
    that does not move when something is added above it.
    """
    value = entry.get("id")
    if value is None:
        return
    if not SLUG_RE.match(str(value)):
        errors.append(f"{label}: id {value!r} is not lower-case-kebab")
        return
    if value in ids:
        errors.append(f"{label}: id {value!r} is already used by {ids[value]}")
        return
    ids[value] = label


def check_mentored(entry, label: str) -> None:
    """`mentored` must be a subset of `authors`, so the two cannot drift apart.

    The CV encodes this as a $^*$ on the author's name, which keeps them together
    by construction. Splitting them into two fields loses that guarantee unless it
    is enforced here.
    """
    mentored = entry.get("mentored")
    if mentored is None:
        return
    if not isinstance(mentored, list):
        errors.append(f"{label}: mentored must be a list of author names")
        return

    authors = entry.get("authors")
    if not isinstance(authors, list):
        errors.append(f"{label}: mentored is set but authors is not a list")
        return

    for name in mentored:
        if name not in authors:
            errors.append(
                f"{label}: mentored name {name!r} is not in authors - "
                f"the two lists have drifted"
            )


def check_entry(entry, label: str, required, categories: set[str],
                vocabularies: dict[str, set[str]],
                used: dict[str, set[str]]) -> int:
    if not isinstance(entry, dict):
        errors.append(f"{label} is not a mapping")
        return 0

    for field in required:
        if field not in entry or entry[field] in (None, "", []):
            errors.append(f"{label}: missing required field {field!r}")

    category = entry.get("category")
    if category is not None and categories and category not in categories:
        errors.append(
            f"{label}: category {category!r} is not declared in the file's "
            f"categories list"
        )

    for field in YEAR_FIELDS:
        if field in entry:
            check_year(entry[field], f"{label} {field}")

    start, end = entry.get("start"), entry.get("end")
    if isinstance(start, int) and isinstance(end, int) and end < start:
        errors.append(f"{label}: end {end} is before start {start}")

    check_id(entry, label)
    check_links(entry, label)
    check_mentored(entry, label)
    check_related(entry, label)
    appearances = check_appearances(entry, label)

    for field in SLUG_FACETS:
        check_slug_facet(entry, field, label, vocabularies.get(field, set()),
                         used.setdefault(field, set()))

    check_distinctions(entry, label, vocabularies.get("distinctions", set()),
                       used.setdefault("distinctions", set()))
    return appearances


def normalize_title(value) -> str:
    return re.sub(r"[^a-z0-9]+", " ", str(value).lower()).strip()


def check_shared_titles(by_title: dict[str, list[tuple[str, dict]]]) -> None:
    """Two entries with the same title must agree on their facets.

    This is the "P6 and P11" case: distinct works, identical titles and author
    lists. Keeping them as separate entries is correct, but it creates a new way to
    drift - one copy gets a topic or an institution and the other does not, and
    because the titles match nobody spots it. If they are genuinely the same work
    described twice, the facets should match; if a facet really does differ, the
    entries should say why in a note.
    """
    for title, group in sorted(by_title.items()):
        if len(group) < 2:
            continue
        first_label, first = group[0]
        for other_label, other in group[1:]:
            for field in ("authors", "orgs", "topics"):
                a, b = first.get(field) or [], other.get(field) or []
                if sorted(map(str, a)) != sorted(map(str, b)):
                    warnings.append(
                        f"{other_label}: shares a title with {first_label} but "
                        f"{field} differs ({sorted(map(str, a))} vs "
                        f"{sorted(map(str, b))}) - out of sync, or add a note"
                    )
            # A `related` link to some third entry does not help a reader tell
            # THESE two apart, so the link has to name the twin.
            if not (_links_to(first, other) or _links_to(other, first)):
                warnings.append(
                    f"{other_label}: shares a title with {first_label} but neither "
                    f"declares a 'related' link to the other, so a reader cannot "
                    f"tell them apart"
                )


def _links_to(entry, target) -> bool:
    """Does `entry` declare a `related` link naming `target`'s id?"""
    target_id = target.get("id")
    if not target_id:
        return False
    related = entry.get("related")
    if not isinstance(related, list):
        return False
    return any(
        isinstance(item, dict) and item.get("id") == target_id for item in related
    )


def main() -> int:
    if not DATA.is_dir():
        sys.exit("error: no _data directory found")

    vocabularies = {
        field: load_vocabulary(filename)
        for filename, field in VOCABULARIES.items()
    }
    used: dict[str, set[str]] = {field: set() for field in vocabularies}
    entry_count = 0
    appearance_count = 0
    by_title: dict[str, list[tuple[str, dict]]] = {}

    for path in sorted(DATA.glob("*.yml")):
        if path.name in VOCABULARIES:
            continue

        document = load(path)
        if document is None:
            warnings.append(f"{path.name} is empty")
            continue

        categories: set[str] = set()
        required = DEFAULT_REQUIRED
        if isinstance(document, dict):
            if isinstance(document.get("categories"), list):
                for category in document["categories"]:
                    if isinstance(category, dict) and "slug" in category:
                        categories.add(category["slug"])
            if isinstance(document.get("required"), list):
                required = document["required"]
            entries = document.get("entries") or []
        elif isinstance(document, list):
            entries = document
        else:
            errors.append(f"{path.name}: unexpected top-level type")
            continue

        for index, entry in enumerate(entries):
            entry_count += 1
            label = f"{path.name}[{index}]"
            if isinstance(entry, dict):
                what = entry.get("what") or entry.get("title")
                if what:
                    label += f" ({str(what).strip()[:48]})"
            appearance_count += check_entry(
                entry, label, required, categories, vocabularies, used
            )
            if isinstance(entry, dict) and entry.get("title"):
                by_title.setdefault(
                    normalize_title(entry["title"]), []
                ).append((label, entry))

    check_shared_titles(by_title)

    for where, _source, target, how in relations:
        if target not in ids:
            errors.append(
                f"{where}: related id {target!r} does not exist - add the entry or "
                f"fix the id"
            )
        elif how not in RELATION_INVERSES and how not in RELATION_INVERSES.values():
            errors.append(f"{where}: relation {how!r} has no defined inverse")

    # Enforce the one-direction rule the RELATION_INVERSES comment states. Writing
    # both halves is the failure mode this whole data model exists to prevent: two
    # copies of one fact, free to disagree. The renderer derives the far side.
    declared = {(source, target) for _, source, target, _ in relations}
    for source, target in sorted(declared):
        if (target, source) in declared and source < target:
            errors.append(
                f"relation between {source!r} and {target!r} is declared from both "
                f"sides - author it once and let the renderer show the inverse"
            )

    for field, vocabulary in sorted(vocabularies.items()):
        for slug in sorted(vocabulary - used[field]):
            warnings.append(f"{field}: {slug!r} is declared but unused")

    for warning in warnings:
        print(f"warning: {warning}")
    for error in errors:
        print(f"error: {error}")

    if errors:
        print(f"\nFAILED: {len(errors)} error(s)")
        return 1

    summary = ", ".join(
        f"{len(used[field])}/{len(vocabulary)} {field}"
        for field, vocabulary in sorted(vocabularies.items())
    )
    # Appearances are reported separately and never folded into the entry count -
    # that separation is the whole point of the also_appeared / related split.
    extra = f", {appearance_count} extra appearance(s)" if appearance_count else ""
    print(
        f"OK: {entry_count} entries{extra}; {len(ids)} with stable ids; "
        f"{len(relations)} relation(s); {summary} in use; {len(warnings)} warning(s)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
