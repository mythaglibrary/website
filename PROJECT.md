# Project Structure

The site is built with [Zensical](https://zensical.org). Content lives in `lib/`, builds to `site/` on deploy.

## `lib/` — main content directory

- **`.md` files** — each represents a page. The filename becomes part of the URL.
- **Folders** — represent the navigation structure. A folder with an `index.md` becomes a section with that page as the landing page.
- Subfolders can be nested arbitrarily to create deeper navigation hierarchies.

### Frontmatter

Every `.md` file must have YAML frontmatter at the top:

```yaml
---
title: Page Title
description: SEO description for search engines and social previews.
icon: lucide/book-open
---
```

- `title` — used as the `<title>` tag (formatted as `Page Title * Mythag Library`) and the page heading.
- `description` — used as the `<meta name="description">` tag for SEO and link previews.
- `icon` — optional [icon](https://zensical.org/docs/authoring/icons-emojis/) shown in the nav sidebar and page header.

### HTML in `.md` files

HTML markup is allowed (enabled by the `md_in_html` extension), but with a constraint: **any HTML block that contains Markdown must include the `markdown` (or `markdown="span"` for inline) attribute**, otherwise the Markdown inside won't be rendered. For example:

```html
<div markdown>
This **bold** text renders correctly.
</div>

<span markdown="span">This **bold** text renders correctly.</span>
```

Without the `markdown` attribute, any Markdown inside HTML tags will appear as raw text, breaking the visual output.

The formatting itself is also important, including spacings, new lines, etc., and can cause visual discrepancies, so make sure to follow the existing examples.

## `lib/images/` — image assets

All image files (PNG). Organised into subdirectories by category: `awakeners/`, `covenants/`, `emojis/`, `handbook/`, `icons/`, `posses/`, `realms/`, `wheels/`. Referenced in `.md` files with paths relative to `lib/`, e.g. `![](/images/logo.png)`.

## `lib/styles/` — custom CSS

Contains `extra.css` with project-specific styles. Defines:
- Custom fonts (Crimson Text, Libre Caslon Display)
- CSS custom properties for realm colors, tier colors, highlight colors, effect colors
- Utility classes for layout (`.flex-desktop`, `.grid`, `.text-center`, etc.)
- Responsive breakpoints and component overrides

These classes can be used in `.md` files via the `attr_list` extension (e.g. `{.text-center}`) or directly in HTML.

## `includes/` — site-wide includes

### `abbreviations.md`

Defines abbreviations in a specific format (`*[TERM]: Definition.`) that are automatically appended to every page via the `pymdownx.snippets` extension. When you add a term here, hovering over it on any page shows its definition as a tooltip.

## `overrides/` — theme template overrides

Contains Jinja2 templates that extend Zensical's default theme. Currently customises the `<title>` tag format to `Page Title * Mythag Library`.

## `zensical.toml` — site configuration

Contains:
- **SEO**: `site_name`, `site_description`, `site_author`, `site_url`
- **Navigation**: explicit `nav` structure defining the sidebar menu and page order
- **Theme**: fonts (Rubik), color palette (light/dark), logo, favicon, custom directory
- **Features**: toggles for instant navigation, search highlighting, footnote tooltips, code copy, etc.
- **Markdown extensions**: enabled extensions that extend the authoring syntax (admonitions, footnotes, emoji, superfences/mermaid, glightbox, etc.)
