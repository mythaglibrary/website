# Content examples

These files are repository-only references. They live outside `lib/`, the
configured Zensical `docs_dir`, so they are not published as website pages.

- [`awakener-guide.md`](awakener-guide.md) is a complete, filled Awakener
  guide source, including an inline example team.
- [`team-fence.md`](team-fence.md) is a standalone, complete `team` fence that
  can be copied into a guide after the prose.
- [`../templates/awakener.md`](../templates/awakener.md) is the copyable
  Awakener scaffold.
- [`../templates/team.md`](../templates/team.md) is the copyable team-fence
  scaffold.

The guide example uses real GDoll content; when adapting it for a page, rename
the file to the matching realm path (for example,
`lib/handbook/awakeners/chaos/gdoll.md`) and update its catalog-backed IDs.

When creating content, copy the relevant scaffold, replace every catalog ID,
and keep team fences as standalone top-level Markdown blocks. Run
`uv run mythag-check` before opening a preview; the validator checks the same
IDs and team shape used by the published templates.
