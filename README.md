# InfoNest — Deployment Guide

## Overview

InfoNest is a fully static HTML/CSS/JS content site covering 11 categories and 33+ articles, ready for GitHub Pages hosting at **infonest.page**.

---

## GitHub Pages Deployment

### Step 1: Create the GitHub Repository

1. Go to [github.com](https://github.com) and sign in
2. Click **"New repository"**
3. Name it: `infonest` (or any name you prefer)
4. Set visibility to **Public**
5. Do NOT initialize with a README (you already have one)
6. Click **"Create repository"**

### Step 2: Push Your Files to GitHub

Open PowerShell in your project folder (`C:\Users\farze\Desktop\infoNest`) and run:

```powershell
git init
git add .
git commit -m "Initial commit: Full InfoNest site"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/infonest.git
git push -u origin main
```

> Replace `YOUR_USERNAME` with your actual GitHub username.

### Step 3: Enable GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings** → **Pages** (left sidebar)
3. Under **"Source"**, select **"Deploy from a branch"**
4. Select branch: **main**, folder: **/ (root)**
5. Click **Save**

GitHub will deploy your site within 1–2 minutes. The URL will be:
`https://YOUR_USERNAME.github.io/infonest/`

---

## Custom Domain Setup (infonest.page)

### Step 4: Add the CNAME File

The `CNAME` file is already created in your project root containing `infonest.page`.

Verify it exists:
```
C:\Users\farze\Desktop\infoNest\CNAME
```

Contents should be:
```
infonest.page
```

### Step 5: Configure DNS at Your Domain Registrar

Log in to wherever you purchased **infonest.page** and add these DNS records:

**For the apex domain (`infonest.page`):**

| Type | Name | Value |
|------|------|-------|
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |

**For the www subdomain (optional but recommended):**

| Type | Name | Value |
|------|------|-------|
| CNAME | www | YOUR_USERNAME.github.io |

### Step 6: Set Custom Domain in GitHub Pages

1. Go back to **Settings → Pages**
2. Under **"Custom domain"**, enter: `infonest.page`
3. Click **Save**
4. Check **"Enforce HTTPS"** (wait a few minutes after DNS propagates)

DNS changes can take up to 24–48 hours to propagate globally, though often faster.

---

## Google AdSense Setup

### Prerequisites for AdSense Approval

Before applying, ensure:
- [ ] The site is live at your custom domain
- [ ] At least 20–30 unique, quality articles are published
- [ ] Privacy Policy page is live: `/privacy-policy/`
- [ ] Terms of Service page is live: `/terms/`
- [ ] Contact page is live: `/contact/`
- [ ] About page is live: `/about/`
- [ ] `ads.txt` file is present at the root: `/ads.txt`
- [ ] Site has been indexed by Google (check Google Search Console)

### Apply for AdSense

1. Go to [google.com/adsense](https://www.google.com/adsense/)
2. Sign in with your Google account
3. Click **"Get started"** and enter your site URL
4. Add the AdSense verification code to your site (place in the `<head>` section of all pages, or add it to `assets/js/site.js` as a script)
5. Submit for review — AdSense review typically takes 1–14 days

### Ad Placement

Ad slots are already marked in every page with the class `ad-slot`:
- `ad-slot-header` — above the fold banner
- `ad-slot-inarticle` — mid-article placement
- `ad-slot-sidebar` — right sidebar

After AdSense approval, replace the `<div class="ad-slot ...">Advertisement</div>` placeholders with actual AdSense ad unit code.

---

## Google Search Console Setup

1. Go to [search.google.com/search-console](https://search.google.com/search-console)
2. Add property → **URL prefix** → enter `https://infonest.page`
3. Verify ownership (download the HTML verification file and place it in the root of your project)
4. Submit your sitemap: `https://infonest.page/sitemap.xml`

---

## File Structure

```
infoNest/
├── index.html                          # Homepage
├── 404.html                            # Custom 404 page
├── sitemap.xml                         # XML sitemap for search engines
├── ads.txt                             # AdSense verification
├── CNAME                               # Custom domain for GitHub Pages
├── README.md                           # This file
├── assets/
│   ├── css/
│   │   ├── main.css                    # Global styles and design system
│   │   └── article.css                 # Article-specific styles
│   └── js/
│       └── site.js                     # Shared components (nav, footer, theme)
├── about/index.html
├── contact/index.html
├── privacy-policy/index.html
├── terms/index.html
├── disclaimer/index.html
├── editorial-policy/index.html
├── sitemap-page/index.html
├── author/
│   └── alex-morgan/index.html
├── technology/                         # 3 articles
│   ├── index.html
│   ├── how-cloud-computing-works/
│   ├── top-emerging-tech-trends/
│   └── cybersecurity-basics/
├── ai/                                 # 3 articles
│   ├── index.html
│   ├── what-is-artificial-intelligence/
│   ├── ai-tools-changing-productivity/
│   └── ml-deep-learning-ai-differences/
├── programming/                        # 3 articles
│   ├── index.html
│   ├── best-programming-languages-2026/
│   ├── beginners-roadmap-software-developer/
│   └── clean-code-principles/
├── finance/                            # 3 articles
│   ├── index.html
│   ├── personal-budgeting-101/
│   ├── understanding-compound-interest/
│   └── beginners-guide-to-investing/
├── health-wellness/                    # 3 articles
│   ├── index.html
│   ├── daily-habits-improve-long-term-health/
│   ├── understanding-sleep-cycles/
│   └── nutrition-basics-balanced-diet/
├── education/                          # 3 articles
│   ├── index.html
│   ├── effective-study-techniques/
│   ├── how-to-choose-degree-program/
│   └── free-online-learning-resources/
├── career/                             # 3 articles
│   ├── index.html
│   ├── how-to-write-resume/
│   ├── negotiating-your-salary/
│   └── switching-careers-step-by-step/
├── business/                           # 3 articles
│   ├── index.html
│   ├── how-to-start-small-business/
│   ├── understanding-business-models/
│   └── marketing-on-a-budget/
├── productivity/                       # 3 articles
│   ├── index.html
│   ├── time-management-techniques/
│   ├── how-to-build-habits-that-stick/
│   └── pomodoro-technique-explained/
├── travel/                             # 3 articles
│   ├── index.html
│   ├── budget-travel-tips-for-beginners/
│   ├── how-to-plan-a-trip/
│   └── essential-packing-checklist/
└── lifestyle/                          # 3 articles
    ├── index.html
    ├── building-a-morning-routine/
    ├── minimalism-101/
    └── digital-detox-guide/
```

---

## Maintenance

### Adding New Articles

1. Create a new folder inside the relevant category: `/category/article-slug/`
2. Create `index.html` using the existing article template as reference
3. Update the category landing page (`/category/index.html`) to include the new article card
4. Update `sitemap.xml` with the new URL
5. Commit and push to GitHub

### Updating the Sitemap

The `sitemap.xml` in the root is manually maintained. Add new article URLs with their `<lastmod>` dates as content is added.

---

## Performance Notes

- All CSS and JS are served from `/assets/` — no external dependencies except Google Fonts
- Images are replaced with CSS emoji placeholders (lightweight, no external requests)
- Dark/light theme implemented via CSS variables on `data-theme` attribute — zero JavaScript paint blocking
- All pages are fully static — no server-side processing required

---

## Contact

Built by InfoNest editorial team. For questions about deployment, contact via the [Contact page](/contact/).
