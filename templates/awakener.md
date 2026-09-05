---
title: Awakener Name
description: Builds and new-player guidance for Awakener Name.
template: awakeners/awakener.html
awakener:
  # Optional: overrides the shared content/skeydb.yaml mapping.
  # skeydb_slug: doll-inferno
  tagline: Short description of what this Awakener does
  roles:
    - Main role
    - Secondary role
  ranks:
    dps:
      - tier: B
        note: Decent
    support:
      - tier: A
        note: Great
  stopping_points:
    - E0
    - E3
  builds:
    - name: Example Build
      covenants:
        - covenant-id
      covenants_note: Optional guidance such as Any support
      wheels:
        early_game:
          - id: wheel-id
            note: Optional explanation
        astral_reign:
          - id: wheel-id
  suggested_posses:
    - id: posse-id
      note: Optional explanation
  suggested_posses_note: Optional note such as Any
  works_well_with:
    - other-awakener-id
  works_well_with_note: Optional note such as Anyone
---

Write the overview as ordinary Markdown here.

## How to Play

Optional: explain how to use this Awakener here. Remove this heading and text
if the section is not ready. Use ### headings for subsections.

Optional example teams can be added as standalone top-level `team` fences
below the prose. Awakener guides render them in a separate Example Teams
section; see `examples/awakener-guide.md` for a complete source example and
`templates/team.md` for a copyable fence scaffold.
