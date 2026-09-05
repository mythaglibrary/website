# Inline symbols

Write `:skey:`, `:weak:`, or `:vuln:` in Markdown prose to insert a small icon.
The full list lives in `content/symbols.yaml`. Authors can add names there without
changing Python or maintaining a separate allowlist:

```yaml
my-symbol:
  label: Accessible name
  icon: /images/icons/effects/weakness.png
  description: Optional plain-text explanation shown on hover.
```

Names use lowercase letters, numbers, underscores or hyphens and start with a
letter. Names already used by built-in emoji are reserved; choose a different
name for those icons. `label` and `icon` are required. `light_icon` optionally supplies a second
image for light mode; with both images, `icon` is the dark-mode image. Paths must
reference existing files under `lib/images/`. Descriptions are optional: omit
them when no verified explanation is available.

Unknown shortcuts produce an error naming the shortcut and suggesting a close
match when possible. Existing emoji names remain valid. Use backticks when
showing a literal shortcut, such as `:future-symbol:`. Code blocks, links, URLs
and raw HTML are preserved. Keep shortcuts in ordinary Markdown prose, outside
raw HTML tags.

In guide YAML, quote text containing shortcuts, for example
`tagline: "Support with :skey: regeneration"`, because colons have meaning in YAML.
