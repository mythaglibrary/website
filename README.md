# Mythag Library

A living collection of everything related to Morimens, continuously updated and curated by a dedicated team.

If you have feedback or suggestions, feel free to create an [Issue](https://github.com/mythaglibrary/website/issues), a [Discussion](https://github.com/mythaglibrary/website/discussions) or a [Pull Request](https://github.com/mythaglibrary/website/pulls).

# Installation and preview

1. [Install uv](https://docs.astral.sh/uv/getting-started/installation/).
2. Run `uv sync --locked` from the repository root to install the locked
   project dependencies.
3. Run `uv run mythag-serve` to preview the website locally.

The preview shows ordinary content, template, and CSS changes in real time (you
might need to reload the page occasionally). Restart the preview after adding,
renaming, moving, or removing an Awakener guide, editing a content catalog, or
adding or removing structured covenant, wheel, posse, or related-Awakener IDs.
Those changes refresh generated navigation and asset lookups only at startup.
This is a fast authoring preview: AVIF URL rewriting, production abbreviation
expansion, and redundant-PNG pruning run only during `mythag-build`.

Run `uv run mythag-check` for a quick content and asset validation without a
full production build.

For a production build, run `uv run mythag-build`. This builds the site,
generates one AVIF delivery asset for every PNG in `lib/images`, and updates the
built HTML to serve AVIF images with intrinsic dimensions. Wheel delivery
assets are capped at a 640-pixel edge; other images retain their source
dimensions. Maintainers should continue adding and referencing ordinary PNG
source assets; no manual conversion or AVIF filenames are needed. Unchanged
conversions are reused from the ignored `.avif-cache` directory. The completed
artifact is checked for surviving references before redundant built PNG copies
are removed; the logo PNG is retained for favicon compatibility.

To inspect the exact production output locally, build it and then run
`uv run python -m http.server 8000 --directory site`.

The hosting provider must use `uv run --locked mythag-build` as its production
build command. On Cloudflare Pages, where uv is not preinstalled, use
`python -m pip install uv && uv run --locked mythag-build`. Keep `site` as the
build output directory. Running `zensical build` directly skips AVIF generation
and HTML rewriting as well as Awakener validation and generated navigation.

## Adding an Awakener guide

1. Copy `templates/awakener.md` into the appropriate realm folder under
   `lib/handbook/awakeners/` and name it after the Awakener, such as
   `lib/handbook/awakeners/chaos/gdoll.md`.
2. Fill in the YAML header and write the guide below it using ordinary
   Markdown. Do not add HTML, CSS classes, or Jinja template calls.
3. Reference covenants, wheels, and posses by their kebab-case IDs from
   the matching YAML file under `content/`. When introducing a new item, add
   its ID and display label to that catalog; the ID must match its PNG filename.
4. Add the ordinary game PNG assets under `lib/images/`; the production build
   handles the web delivery format.
5. Run `uv run mythag-check`, then preview with `uv run mythag-serve`.

Fields such as `builds`, `suggested_posses`, and `works_well_with` can be
removed when a guide does not need those sections.

The guide `title` must match its filename's label in `content/awakeners.yaml`.
Use Awakener IDs from that same catalog in `works_well_with`.

The shared Awakener layout is defined in
`overrides/awakeners/awakener.html`, and its presentation is defined in
`lib/styles/awakeners.css`. Editing those files updates every standalone
Awakener guide.

To add example teams to an Awakener guide, place one or more top-level
`team` fences in the guide source. The guide template automatically moves
those teams into an optional **Example Teams** section after the build and
recommendation sections; no extra YAML switch is needed.
The section is omitted when the guide has no team fence. The fences still use
the shared team schema described below.

## Adding a team to a guide

Place a `team` block as a standalone top-level Markdown block with its opener
starting in column zero. It may be surrounded by ordinary Markdown, but it
must not be nested inside a table, list, blockquote, admonition, or tabbed
content:

````markdown
```team
name: Xu Poison
context: Astral Reign - Story
summary: A team that applies poison and triggers it to deal damage.
posse: plague-of-illusions
members:
  - awakener: xu
    archetype: dps
    covenant: steppenwolf
    wheels: [gift-of-decay, cursed-binding]
  - awakener: nymphaea
    archetype: support
    covenant: life-drain
    wheels: [merciful-nurturing, moment-of-reunion]
  - awakener: gdoll
    archetype: support
    covenant: dream-of-medicine
    wheels: [manikin-of-oblivion, elevated-focus]
  - awakener: faint
    archetype: tank
    covenant: burial-grounds-sighs
    wheels: [dusk-and-dawn, cloaked-in-the-night]
```
````

Use the kebab-case IDs from the four YAML catalogs under `content/`. A team has
one posse and exactly four members; each member has one covenant, two wheels,
and an explicit `archetype` (`dps`, `support`, or `tank`). Keep that archetype
separate from any authored role text. `context`, `summary`, `role`, and `note`
are optional authored presentation fields. `uv run mythag-check` reports the
source line and suggests the closest known ID when it finds a typo.

The shared team fragment is defined in `overrides/teams/team.html`, and its
presentation is defined in `lib/styles/teams.css`.

## Reference examples and templates

The repository keeps complete, copyable source examples separately from the
published `lib/` tree. See [`examples/README.md`](examples/README.md) for a
filled Awakener guide, a full team fence, and links to both scaffolds. These
reference files are not website pages.

# How to

1. [Create a GitHub account](https://docs.github.com/en/get-started/start-your-journey/creating-an-account-on-github)
2. [Clone the repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository)

## If you don't know what Git is

1. [Set up Git](https://docs.github.com/en/get-started/git-basics/set-up-git)
2. [Learn Git](https://github.com/git-guides)

## If you want to make a few quick edits and you are a collaborator

1. How to [make changes directly on GitHub](https://docs.github.com/en/get-started/using-github/github-flow?search-overlay-input=branch#make-changes)

## If you are a collaborator and you know what you are doing

1. Open the cloned repository in your preferred text editor. [Zed](https://zed.dev/) is recommended
2. Use your preferred Git client to [pull the latest repository changes](https://docs.github.com/en/get-started/using-git/getting-changes-from-a-remote-repository), e.g. [Zed Git panel](https://zed.dev/docs/git) or [Git Bash](https://git-scm.com/)
3. Make necessary changes (update files, create new ones, etc.)
4. [Commit](https://github.com/git-guides/git-commit) your changes to Git
5. Once again, [pull the latest repository changes](https://docs.github.com/en/get-started/using-git/getting-changes-from-a-remote-repository)
5. If no conflicts, [push](https://docs.github.com/en/get-started/using-git/pushing-commits-to-a-remote-repository) your changes to the repository. If there are conflicts, you **must** [resolve](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/addressing-merge-conflicts/resolving-a-merge-conflict-using-the-command-line) them before pushing

## If you are not a collaborator or just want to be safe

Follow a [Git workflow](https://docs.github.com/en/get-started/using-github/github-flow).

1. Open the cloned repository in your preferred text editor. [Zed](https://zed.dev/) is recommended
2. Use your preferred Git client to [pull the latest repository changes](https://docs.github.com/en/get-started/using-git/getting-changes-from-a-remote-repository), e.g. [Zed Git panel](https://zed.dev/docs/git) or [Git Bash](https://git-scm.com/)
3. [Create a new branch](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-and-deleting-branches-within-your-repository)
4. Move (`git checkout <your-branch-name>`) to the newly created branch, if you aren't moved there automatically
5. Make necessary changes (update files, create new ones, etc.)
6. [Commit](https://github.com/git-guides/git-commit) your changes to Git
7. Once again, [pull the latest repository changes](https://docs.github.com/en/get-started/using-git/getting-changes-from-a-remote-repository). You need to pull changes from the default repository branch, usually named `main`
8. Create a [pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request)
9. Wait for the pull request to be reviewed by one of the collaborators
10. Address review comments, if any
11. Repeat Step 7
12. [Merge](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/merging-a-pull-request)
13. [Delete the branch](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-branches-in-your-repository/deleting-and-restoring-branches-in-a-pull-request)

# Licensing

- Code in this repository is released under the Unlicense
- Non-code content is licensed under CC BY-SA 4.0 unless otherwise noted
- Game names, logos, characters, and other trademarks remain the property of their respective owners and are not licensed by this repository

See:
- [UNLICENSE](./UNLICENSE)
- [CONTENT_LICENSE.md](./CONTENT_LICENSE.md)
- [TRADEMARKS.md](./TRADEMARKS.md)

---

&copy; 2026 Mythag Library
