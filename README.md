# Digital Card Experience Revamp

A self-contained presentation deck — one HTML file, no build step, no server.
Open `index.html` in any browser.

## Getting around

| Action | How |
| --- | --- |
| Next / previous slide | `→` `←` (also `↑` `↓`, PageUp/PageDown, scroll, drag) |
| Jump to a chapter | dropdown at the bottom right |
| First / last slide | `Home` / `End` |
| View a screen full size | click it — `Esc` closes |

## Chapters

1. **Cover**
2. **Fresh Look** — *Digital Cards Before* and *Digital Card Fresh Look*
3. **Web Experience**
4. **Functional Optimisations**
5. **Performance**
6. **End**

## Editing the content

Everything the deck says lives in one block at the top of the `<script>` in
`index.html` — `COVER`, `PANELS` and `END`. No HTML editing needed to add a
slide or change copy.

Each chapter in `PANELS` is a list of slides, so a chapter can hold as many
slides as it needs. A slide picks a `layout`:

| `layout` | What it draws | Payload |
| --- | --- | --- |
| `screens` | a row of screens at their own proportions | `screens: [{ img, cap }]` |
| `beforeafter` | before → after pairs | `pairs: [{ t, before, after }]` |
| `split` | one large screen beside a list of points | `media`, `points` |
| `cards` | a numbered grid of cards | `cards: [{ t, d }]` |
| `metrics` | metric tiles over a chart area | `metrics`, `box` |

### Adding a screenshot

Drop the file in `assets/` and point a screen at it:

```js
{ img:'assets/after-5.png', cap:'Checkout' }
```

Leave `img` out and the slot renders as a labelled placeholder instead — that
is how the empty slots in the deck are marked. Videos work in the same field
(`.mp4`, `.webm`, `.mov`): they play inline and full-screen on click.

Screenshots are committed at full resolution so they stay sharp when opened
full size.
