---
layout: frontpage
title: Publications
---

<div class="page-publications">
  <div class="page-hero">
    <div class="page-hero-copy">
      <h2><i class="fa-solid fa-book-open"></i> Publications</h2>
      <p class="page-subtitle">
        Peer-reviewed papers, articles, and scholarly outputs from the Radiant Systems Lab.
      </p>
      <p class="scholar-line">
        You can also browse our
        <a href="https://scholar.google.com/citations?hl=en&user=ZvYwdsUAAAAJ" target="_blank">Google Scholar profile</a>.
      </p>
    </div>
  </div>

  {%- comment -%}
  Collect all publications with dates, newest first.
  {%- endcomment -%}
  {% assign pubs = site.data.single_data_source
    | where_exp: "i", "i.Publication"
    | where_exp: "i", "i.Publication.date"
    | sort: "Publication.date"
    | reverse %}

  {%- comment -%}
  Extract unique year buckets.
  {%- endcomment -%}
  {% assign years = "" | split: "" %}
  {% for item in pubs %}
    {% assign y = item.Publication.date | date: "%Y" %}
    {% assign years = years | push: y %}
  {% endfor %}
  {% assign years = years | uniq | sort | reverse %}

  <section class="pub-controls-panel">
    <div class="pub-controls-label">
      <i class="fa-solid fa-filter"></i> Filter by
    </div>

    <div class="pub-controls-grid">
      <div class="pub-filter-group">
        <label class="pub-filter-label" for="pubTypeTrigger">Type</label>
        <input type="hidden" id="pubTypeFilter" value="all">
        <div class="pub-select" data-input-id="pubTypeFilter">
          <button type="button"
                  class="pub-select-trigger"
                  id="pubTypeTrigger"
                  aria-haspopup="listbox"
                  aria-expanded="false"
                  aria-controls="pubTypeMenu">All</button>
          <ul class="pub-select-menu" id="pubTypeMenu" role="listbox" aria-labelledby="pubTypeTrigger">
            <li><button type="button" class="pub-select-option is-active" data-value="all" role="option" aria-selected="true">All</button></li>
            <li><button type="button" class="pub-select-option" data-value="article" role="option" aria-selected="false">Articles</button></li>
            <li><button type="button" class="pub-select-option" data-value="chapter" role="option" aria-selected="false">Chapters</button></li>
            <li><button type="button" class="pub-select-option" data-value="dissertation" role="option" aria-selected="false">Dissertations</button></li>
            <li><button type="button" class="pub-select-option" data-value="editorial" role="option" aria-selected="false">Editorials</button></li>
            <li><button type="button" class="pub-select-option" data-value="other" role="option" aria-selected="false">Others</button></li>
          </ul>
        </div>
      </div>

      <div class="pub-filter-group">
        <label class="pub-filter-label" for="pubYearTrigger">Year</label>
        <input type="hidden" id="pubYearFilter" value="all">
        <div class="pub-select" data-input-id="pubYearFilter">
          <button type="button"
                  class="pub-select-trigger"
                  id="pubYearTrigger"
                  aria-haspopup="listbox"
                  aria-expanded="false"
                  aria-controls="pubYearMenu">All</button>
          <ul class="pub-select-menu" id="pubYearMenu" role="listbox" aria-labelledby="pubYearTrigger">
            <li><button type="button" class="pub-select-option is-active" data-value="all" role="option" aria-selected="true">All</button></li>
            {% for y in years %}
              <li><button type="button" class="pub-select-option" data-value="{{ y }}" role="option" aria-selected="false">{{ y }}</button></li>
            {% endfor %}
          </ul>
        </div>
      </div>
    </div>
  </section>

  <div id="pub-list" class="pub-year-groups">
    {% for y in years %}
      <section class="pub-year-group">
        <h3 class="pubyear">{{ y }}</h3>
        <ol class="pub-year-list">
          {% for item in pubs %}
            {% assign p = item.Publication %}
            {% assign pub_year = p.date | date: "%Y" %}

            {% if pub_year == y %}
              {% assign raw_type = p.pubType | default: "other" | downcase %}
              {% assign type = raw_type %}
              {% assign allowed_types = "article,chapter,dissertation,editorial,other" | split: "," %}
              {% unless allowed_types contains type %}
                {% assign type = "other" %}
              {% endunless %}

              {% assign uid = item.id %}
              {% unless uid %}
                {% capture uid %}{{ y }}-{{ forloop.index }}{% endcapture %}
              {% endunless %}

              {% assign bib_type = p.pubType | downcase | default: "article" %}
              {% assign bib_key = p.citationKey | default: uid %}
              {% assign bib_year = p.year | default: pub_year %}

              <li class="pub-entry" data-type="{{ type }}" data-year="{{ pub_year }}">
                <article class="pub-card">
                  <div class="pub-top-row">
                    <h4 class="pub-title">{{ p.title }}</h4>
                    <span class="pub-type-pill">{{ type | capitalize }}</span>
                  </div>

                  {% if p.authors %}
                    <div class="pub-authors">{{ p.authors }}</div>
                  {% endif %}

                  <div class="pub-venue-row">
                    {% if p.journal %}
                      <span class="pub-venue"><em>{{ p.journal }}</em></span>
                    {% endif %}
                    <span class="pub-date">
                      <i class="fa-regular fa-calendar"></i> {{ p.date | date: "%B %Y" }}
                    </span>
                  </div>

                  <div class="pub-icons">
                    {% if p.abstract %}
                      <button class="pub-action"
                              type="button"
                              onclick="toggleSection('abs-{{ uid }}', this)"
                              title="Abstract"
                              aria-controls="abs-{{ uid }}"
                              aria-expanded="false">
                        <i class="fas fa-file-alt"></i>
                      </button>
                    {% endif %}

                    <button class="pub-action"
                            type="button"
                            onclick="toggleSection('bib-{{ uid }}', this)"
                            title="BibTeX"
                            aria-controls="bib-{{ uid }}"
                            aria-expanded="false">
                      <i class="fas fa-code"></i>
                    </button>

                    {% if p.links and p.links.PDF %}
                      <a href="{{ p.links.PDF.url }}"
                         class="pub-action"
                         target="_blank"
                         title="{{ p.links.PDF.text }}">
                        <i class="fas fa-file-pdf"></i>
                      </a>
                    {% endif %}
                  </div>

                  {% if p.abstract %}
                    <div id="abs-{{ uid }}" class="pub-section pub-abstract" hidden>
                      <p>{{ p.abstract }}</p>
                    </div>
                  {% endif %}

                  <div id="bib-{{ uid }}" class="pub-section pub-bibtex" hidden>
<pre>@{{ bib_type }}{ {{ bib_key }},
  title     = { {{ p.title }} },
  author    = { {{ p.authors }} },
{% if p.journal %}  journal   = { {{ p.journal }} },
{% endif %}{% if p.Publisher %}  publisher = { {{ p.Publisher }} },
{% endif %}  year      = {{ bib_year }},
}</pre>
                  </div>
                </article>
              </li>
            {% endif %}
          {% endfor %}
        </ol>
      </section>
    {% endfor %}
    <div id="pub-no-results" class="pub-no-results" role="status" aria-live="polite" hidden>
      No publications match the selected filters.
    </div>
  </div>
</div>

<script>
let publicationBaselineHeight = 0;

function applyPublicationFilters() {
  const typeFilter = document.getElementById("pubTypeFilter");
  const yearFilter = document.getElementById("pubYearFilter");
  const noResultsEl = document.getElementById("pub-no-results");
  const selectedType = typeFilter ? typeFilter.value : "all";
  const selectedYear = yearFilter ? yearFilter.value : "all";

  const entries = document.querySelectorAll(".page-publications .pub-entry");
  entries.forEach((entry) => {
    const typeMatch = selectedType === "all" || entry.dataset.type === selectedType;
    const yearMatch = selectedYear === "all" || entry.dataset.year === selectedYear;
    const visible = typeMatch && yearMatch;
    entry.classList.toggle("is-hidden", !visible);
  });

  document.querySelectorAll(".page-publications .pub-year-group").forEach((group) => {
    const hasVisible = group.querySelector(".pub-entry:not(.is-hidden)");
    group.classList.toggle("is-hidden", !hasVisible);
  });

  const visibleCount = document.querySelectorAll(".page-publications .pub-entry:not(.is-hidden)").length;
  if (noResultsEl) {
    if (visibleCount === 0) {
      noResultsEl.removeAttribute("hidden");
    } else {
      noResultsEl.setAttribute("hidden", "hidden");
    }
  }

  lockPublicationResultsHeight();
}

function closeAllCustomFilters(exceptSelect) {
  document.querySelectorAll(".page-publications .pub-select").forEach((selectEl) => {
    if (exceptSelect && selectEl === exceptSelect) return;
    selectEl.classList.remove("open");
    const trigger = selectEl.querySelector(".pub-select-trigger");
    if (trigger) trigger.setAttribute("aria-expanded", "false");
  });
}

function setFilterValue(selectEl, value, label) {
  if (!selectEl) return;
  const inputId = selectEl.dataset.inputId;
  const hiddenInput = inputId ? document.getElementById(inputId) : null;
  const trigger = selectEl.querySelector(".pub-select-trigger");
  const options = Array.from(selectEl.querySelectorAll(".pub-select-option"));

  if (hiddenInput) hiddenInput.value = value;
  if (trigger) trigger.textContent = label;

  options.forEach((optionEl) => {
    const isActive = optionEl.dataset.value === value;
    optionEl.classList.toggle("is-active", isActive);
    optionEl.setAttribute("aria-selected", isActive ? "true" : "false");
  });
}

function setEqualCustomFilterWidth() {
  const selectEls = Array.from(document.querySelectorAll(".page-publications .pub-select"));
  if (!selectEls.length) return;

  const canvas = document.createElement("canvas");
  const ctx = canvas.getContext("2d");
  if (!ctx) return;

  const computedWidths = selectEls.map((selectEl) => {
    const trigger = selectEl.querySelector(".pub-select-trigger");
    const options = Array.from(selectEl.querySelectorAll(".pub-select-option"));
    if (!trigger || !options.length) return 0;

    const style = window.getComputedStyle(trigger);
    const font = `${style.fontStyle} ${style.fontVariant} ${style.fontWeight} ${style.fontSize} ${style.fontFamily}`;
    ctx.font = font;

    const longestTextPx = options.reduce((maxPx, optionEl) => {
      const text = (optionEl.textContent || "").trim();
      const textPx = ctx.measureText(text).width;
      return Math.max(maxPx, textPx);
    }, 0);

    const padLeft = parseFloat(style.paddingLeft) || 12;
    const padRight = parseFloat(style.paddingRight) || 36;
    const borderLeft = parseFloat(style.borderLeftWidth) || 1;
    const borderRight = parseFloat(style.borderRightWidth) || 1;
    const buffer = 12;

    return Math.ceil(longestTextPx + padLeft + padRight + borderLeft + borderRight + buffer);
  });

  const targetWidth = Math.max(...computedWidths, 110);
  selectEls.forEach((selectEl) => {
    selectEl.style.setProperty("--pub-select-width", `${targetWidth}px`);
  });
}

function initializeCustomFilters() {
  const selectEls = Array.from(document.querySelectorAll(".page-publications .pub-select"));
  if (!selectEls.length) return;

  selectEls.forEach((selectEl) => {
    const inputId = selectEl.dataset.inputId;
    const hiddenInput = inputId ? document.getElementById(inputId) : null;
    const trigger = selectEl.querySelector(".pub-select-trigger");
    const options = Array.from(selectEl.querySelectorAll(".pub-select-option"));
    if (!hiddenInput || !trigger || !options.length) return;

    const initial = options.find((opt) => opt.dataset.value === hiddenInput.value) || options[0];
    setFilterValue(selectEl, initial.dataset.value, (initial.textContent || "").trim());

    trigger.addEventListener("click", () => {
      const isOpen = selectEl.classList.contains("open");
      closeAllCustomFilters(selectEl);
      if (!isOpen) {
        selectEl.classList.add("open");
        trigger.setAttribute("aria-expanded", "true");
      }
    });

    options.forEach((optionEl) => {
      optionEl.addEventListener("click", () => {
        const value = optionEl.dataset.value || "all";
        const label = (optionEl.textContent || "").trim() || "All";
        setFilterValue(selectEl, value, label);
        closeAllCustomFilters();
        applyPublicationFilters();
      });
    });
  });

  document.addEventListener("click", (event) => {
    if (!event.target.closest(".page-publications .pub-select")) {
      closeAllCustomFilters();
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      closeAllCustomFilters();
    }
  });

  setEqualCustomFilterWidth();

  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(setEqualCustomFilterWidth);
  }

  window.addEventListener("resize", setEqualCustomFilterWidth);
}

function lockPublicationResultsHeight() {
  const listEl = document.getElementById("pub-list");
  const typeFilter = document.getElementById("pubTypeFilter");
  const yearFilter = document.getElementById("pubYearFilter");
  if (!listEl || !typeFilter || !yearFilter) return;

  const isDefaultView = typeFilter.value === "all" && yearFilter.value === "all";
  if (!isDefaultView && publicationBaselineHeight > 0) {
    listEl.style.minHeight = `${publicationBaselineHeight}px`;
    return;
  }

  const measuredHeight = listEl.scrollHeight;
  if (measuredHeight > publicationBaselineHeight) {
    publicationBaselineHeight = measuredHeight;
  }

  if (publicationBaselineHeight > 0) {
    listEl.style.minHeight = `${publicationBaselineHeight}px`;
  }
}

function toggleSection(id, triggerEl) {
  const el = document.getElementById(id);
  if (!el) return;

  const willOpen = el.hasAttribute("hidden");
  if (willOpen) {
    el.removeAttribute("hidden");
  } else {
    el.setAttribute("hidden", "hidden");
  }

  if (triggerEl) {
    triggerEl.classList.toggle("active", willOpen);
    triggerEl.setAttribute("aria-expanded", willOpen ? "true" : "false");
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const typeFilter = document.getElementById("pubTypeFilter");
  const yearFilter = document.getElementById("pubYearFilter");
  if (!typeFilter || !yearFilter) return;

  initializeCustomFilters();
  applyPublicationFilters();

  requestAnimationFrame(lockPublicationResultsHeight);
  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(lockPublicationResultsHeight);
  }
  window.addEventListener("load", lockPublicationResultsHeight);
  window.addEventListener("resize", lockPublicationResultsHeight);
});
</script>
