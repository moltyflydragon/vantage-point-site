# Vantage Point — Aerial Data Website

RTK-enabled drone data capture service website. Built with Astro + Tailwind CSS.

## Quick Start (Static Preview)

The `dist/` folder contains a ready-to-view static version of the site. Just open `dist/index.html` in your browser — no build step needed.

Or serve it locally:
```bash
npx serve dist
```

## Development Setup (Astro)

The source files in `src/` use Astro for development and production builds.

```bash
# Install dependencies
npm install

# Start dev server (http://localhost:4321)
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Deploy to Cloudflare Pages

1. Push this repo to GitHub
2. Go to Cloudflare Pages → Create a project
3. Connect your GitHub repo
4. Build settings:
   - Build command: `npm run build`
   - Build output directory: `dist`
   - Framework preset: Astro
5. Deploy

Alternative: Deploy the `dist/` folder directly via Wrangler CLI:
```bash
npx wrangler pages deploy dist
```

## HubSpot Form Integration

The contact form submits to HubSpot's Forms API.

### Setup:
1. Create a form in HubSpot (Marketing → Forms)
2. Copy `.env.example` to `.env`
3. Add your Portal ID and Form GUID
4. In the Astro version, these are read from environment variables
5. In the static HTML version, update the `data-portal-id` and `data-form-guid` attributes on the form element in `contact.html`

If HubSpot credentials aren't configured, the form automatically falls back to a mailto: link.

## Project Structure

```
vantage-point-site/
├── dist/                    # Static HTML site (ready to view/deploy)
│   ├── index.html           # Homepage
│   ├── services.html        # Services
│   ├── deliverables.html    # Deliverables gallery
│   ├── industries.html      # Industry verticals
│   ├── about.html           # About page
│   └── contact.html         # Contact form + FAQ
├── src/                     # Astro source (for development)
│   ├── pages/               # Page templates
│   ├── components/          # Shared components
│   ├── layouts/             # Page layouts
│   └── styles/              # Global styles
├── public/                  # Static assets
├── package.json
├── astro.config.mjs
├── tailwind.config.mjs
└── .env.example             # Environment variables template
```

## Design System

- **Aesthetic**: Industrial/rugged, dark tones
- **Primary Background**: #09090b
- **Surface**: #18181b
- **Accent**: Amber (#f59e0b)
- **Typography**: Inter, bold uppercase headers
- **Framework**: Tailwind CSS

## Pages

| Page | Description |
|------|-------------|
| Home | Hero, benefits, deliverables preview, industries grid, CTA |
| Services | 7 service cards, output formats, 4-step process |
| Deliverables | Gallery with placeholder samples, data format grid |
| Industries | 7 industry verticals with use cases |
| About | Pilot bio, equipment specs, certifications |
| Contact | Lead form with HubSpot integration, FAQ |

## Content Status

All images are placeholders (dashed amber borders). Replace with real drone footage as available.

## Tech Stack

- [Astro](https://astro.build) — Static-first web framework
- [Tailwind CSS](https://tailwindcss.com) — Utility-first CSS
- [Cloudflare Pages](https://pages.cloudflare.com) — Hosting (free tier)
- [HubSpot](https://hubspot.com) — CRM + form handling (free tier)

---

Domain: hithisisdan.com
