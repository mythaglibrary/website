---
# Complete repository-only source example; this file is not published.
title: GDoll
description: Builds and new-player guidance for the Chaos Awakener GDoll.
template: awakeners/awakener.html
awakener:
  tagline: Boss-Destroying Aliemus Battery
  roles:
    - Aliemus
    - DMG Amp.
    - HP % Damage
    - Poison
    - Weakness
    - Vulnerable
    - Heals
  ranks:
    dps:
      - tier: D
        note: Meme
      - tier: B
        note: against bosses
    support:
      - tier: A
        note: Great
  stopping_points:
    - E1
    - E2
    - E3
    - OE
  builds:
    - name: Example Build
      covenants:
        - dream-of-medicine
        - burial-grounds-sighs
      wheels:
        early_game:
          - id: elevated-focus
            note: Any aliemus
          - id: gluttony
            note: Any support
        astral_reign:
          - id: manikin-of-oblivion
            note: Any aliemus
          - id: elevated-focus
            note: Any aliemus
  suggested_posses:
    - id: plague-of-illusions
    - id: tiny-wish
      note: Early game
  works_well_with:
    - lily
    - xu
    - nymphaea
    - '24'
---

A versatile aliemus battery who brings big [DMG amplification](/handbook/team#dmg-amplification-base-dmg) buffs and access to both weakness and vulnerable at E1.
She shines in poison teams, but works as an aliemus support anywhere.

Her true strength is in boss fights, where she deletes 25–30% of a boss's HP bar
and gives your team a massive boost in Finale Form.

At OE, she can carry boss fights by herself.

```team
name: Xu Poison
context: Astral Reign - Story
summary: A team that applies poison and triggers it to deal damage.
posse: plague-of-illusions
members:
  - awakener: xu
    archetype: dps
    role: Poison / DPS
    note: Applies and triggers poison
    covenant: steppenwolf
    wheels: [gift-of-decay, cursed-binding]
  - awakener: nymphaea
    archetype: support
    role: Poison / Support
    note: Keyflare, triggers poison
    covenant: life-drain
    wheels: [merciful-nurturing, moment-of-reunion]
  - awakener: gdoll
    archetype: support
    role: Poison / Support
    note: Aliemus, applies poison
    covenant: dream-of-medicine
    wheels: [manikin-of-oblivion, elevated-focus]
  - awakener: faint
    archetype: tank
    role: Tank
    note: Death resistance, weakness
    covenant: burial-grounds-sighs
    wheels: [dusk-and-dawn, cloaked-in-the-night]
```
