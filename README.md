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
2. **Overview** — what changed and how
3. **Fresh Look** — *Digital Cards Before*, *Digital Card Fresh Look* and *Old vs New*
4. **Web Experience**
5. **Performance** — *Phase 1 · Pre-2025: Security* and *Phase 2 · Post-2025: Growth and Revamp*
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
| `stack` | small slots down the left, one large screen right | `items`, `hero` |
| `cards` | a numbered grid of cards | `cards: [{ t, d }]` |
| `columns` | three standing boxes, icon + heading + points | `columns: [{ icon, t, points }]` |
| `metrics` | metric tiles over a chart area | `metrics`, `box` |
| `chart` | a monthly bar chart above metric tiles | `series`, `bands`, `marks`, `legend`, `metrics` |

Any slide can also carry `sticky:'…'` — a note pinned over the corner, for
saying who still owes the slide its content.

For `chart`, `series` is `[{ m:'Nov 23', v:1422.6 }]` with `v` in thousands;
add `pre:true` to grey a bar out. `bands` shades a range by series index
(`{ from, to, kind:'red'|'green', lab }`) and `marks` labels one bar
(`{ at, lab }`). Set `fmt:'pct'` for a percentage axis, and give a point a
`tone` of `hot`, `warm` or `good` to colour that bar.

A `chart` can carry three more things when one slide has to make a whole
argument:

| Field | What it adds |
| --- | --- |
| `line` + `lineMax` | a second series on a right-hand percentage axis, one value per month, `null` where there is no reading |
| `baselines` | a dashed run-rate drawn across the months it covers — `{ from, to, v, lab }` |
| `funnel` | a panel of uplift bars beside the chart — `{ t, rows:[{ k, v }] }`, `v:0` renders as *flat* |

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
