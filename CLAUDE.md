# LazyTradie assets: working memory

Marketing assets for **LazyTradie** (lazytradie.com.au): an AI admin team for Australian tradies.
The owner sends references and briefs in short, casual messages ("lets cook", "do it fast").
Build to a "$50k ad campaign" standard.

## Product facts (only claim what's real)
- **AI Receptionist** ("Ruby"): answers calls, SMS and web enquiries, checks live free slots and books
  jobs straight into the calendar. Don't say "24/7" unless confirmed.
- **Admin Copilot**: runs the business by voice. It handles quotes, invoices (with Stripe card pay links),
  bookings, scheduling, job notes and finding jobs and customers. Nothing reaches a customer until the tradie taps confirm.
  It can't email customers beyond sending quotes and invoices, and payment reminders aren't live yet.
- **Job tiers**: `T1 · Auto-book` (green), `T2 · Confirm` (amber, $1,000+ or unsure), `T3 · Emergency` (red).
  Details are in `Tiers/README.md`.
- **Customer portal**: shows the customer their job status live, under the tradie's logo and branding.
- **Integrations** (live only): Xero, ServiceM8, Fergus, Stripe.
- Free to get started, no hidden charges. Don't claim "no card needed" unless confirmed.
- Tagline: **"Stress about work, not bookings."**
- Demo account in renders: Turner Electrical, Melbourne (fictional).
- Real UI comes from the `MEGARDX/lazytradie-backend` repo (`dashboard.html`, `public/js/orb.js`).
  Attach it with add_repo when rendering real UI.

## Brand look
- Palette: deep navy `#0D1B2A`, marigold amber `#F5A623`, warm off-white, a touch of sky blue.
- Type in posts: Inter Tight (clean modern sans), set large and readable on a phone.
- The main reference style is ElevenLabs / ElevenCreative carousels: copy their layouts closely.
- No food or drinks in images. LazyTradie isn't a café.

## The campaign girl (use in every campaign unless told otherwise)
Reference photo: `26 oct/Cover hero.jpg`. Attach it as the reference image and paste this:
> the same young woman as the reference image: 22-year-old Australian model, glowing sun-kissed skin,
> light freckles, glossy voluminous curly brown hair in a loose high bun with face-framing curls,
> natural dewy makeup, glossy lips, gold hoop earrings

(The 29 Oct cover used a one-off Asian model. The owner wants the Aussie girl.)

## Workflow
1. Owner sends reference images, and I study the layout system.
2. I write image prompts (4:5 unless stated). Each ends with a shared style block and says
   `No text except "LazyTradie" exactly as written`.
3. Owner generates them and uploads the raw photos to `main` in `<date>/` or `<date>/non edited/`.
4. I build the posts in code: HTML/CSS rendered with Playwright to 1080×1350 PNGs, plus a
   contact-sheet `overview.png`. Output goes in `campaign/<dd>-oct/`. Never touch the originals.
   Remove generator watermarks. Add the real wordmark instead of trusting generated text.
   **Commit the build source too** (in `campaign/<dd>-oct/src/`). The 26 and 29 Oct source was lost with the old container.
5. Write captions on request: Instagram, Facebook and LinkedIn versions, hashtags as one comma-separated string,
   and alt text. LinkedIn carousels are posted as a PDF document.

## Done so far (24–29 Oct)
- `explainer/`: 60 s onboarding explainer (16:9 + 9:16, onboarding and brand cuts, VTT).
- `Tiers/`: 41 s Job Tiers tutorial.
- `copilot/`: 1:43 Admin Copilot film (white/navy, voice + SFX).
- `launch-film/`: parked.
- `campaign/26-oct/`: 18 Instagram posts.
- `campaign/29-oct/`: Admin Copilot carousel (cover + 4 slides) and a LinkedIn PDF.
- All films are voice + SFX only, with no music. The music rule is in each README.
- Earlier work is in PR MEGARDX/lazytradie-asstes#1 (branch `claude/peaceful-newton-lf4aj0`).
