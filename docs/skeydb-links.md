# SKeyDB links

`content/skeydb.yaml` stores optional destination slugs under `awakeners`,
`wheels`, and `posses`, keyed by the existing Mythag content IDs. Keep those IDs
unchanged: the value is the SKeyDB slug, which may differ from the local ID.
Maintainers can add or correct mappings in this file without changing code.
An omitted mapping leaves the corresponding item unlinked.

For example:

```yaml
awakeners:
  gdoll: doll-inferno
wheels:
  celestial-beast: celestial-beast
posses:
  tiny-wish: tiny-wish
```

Destinations use `https://skeydb.com/database/<category>/<slug>`. Use a verified
destination from SKeyDB, not a slug guessed from the Mythag label.

## Initial mapping provenance

Verified on 2026-09-05 against the read-only local MomenTB checkout at commit
`fd018ae5a3f513a54ffaa113d79e98d94d9b0fd5` (clean working tree).
The source was `src/data/public-v3/catalogs/{awakeners,wheels,posses}.json`:
each stored value is a record's explicit `route.slug`, and its
`route.canonicalPath` was checked against the category and slug.
The route prefixes are also defined in
`src/domain/database-entity-definitions.ts`; detail paths are assembled by
`src/domain/database-entity-paths.ts`.

All 60 Awakener, 58 wheel, and 29 posse labels in Mythag's content registries
matched one source record. Matching ignored case and punctuation and treated
`&` as `and` (Mythag's `Dusk & Dawn` is SKeyDB's `Dusk and Dawn`). No unresolved
entries remain in this initial set. This verifies the local source routes;
it is not a claim that every destination was checked against a live deployment.

The five alternate Awakener IDs were resolved from the source catalog's
explicit aliases, not by assuming that a `g` prefix identifies a particular form:

| Mythag ID | Source alias | Source name / destination slug |
| --- | --- | --- |
| `gdoll` | `g-doll` | Doll: Inferno / `doll-inferno` |
| `ghelot` | `g-helot` | Helot: Catena / `helot-catena` |
| `gmurphy` | `g-murphy` | Murphy: Fauxborn / `murphy-fauxborn` |
| `glotan` | `glotan` | Lotan: Cetarchon / `lotan-cetarchon` |
| `gramona` | `g-ramona` | Ramona: Timeworn / `ramona-timeworn` |

Builds read the checked-in mappings and do not need the MomenTB checkout.
Future entries can be maintained here independently; leave uncertain matches
absent until their destination is known.

## Upstream content update

After rebasing onto Mythag `6d20fa8`, added six wheel mappings: `birth-of-a-soul`, `lullaby-devoured`, `queens-edict`, `rota-fortunae`, `shrouded-birth`, `the-gaze-of-isarawu`.
Verified each name and explicit route against local MomenTB `91069ba58976901a0be796c8bda9151119581744`.
Coverage is now 60 awakeners, 64 wheels, and 29 posses.
