/* ============================================================
   InfoNest — site.js
   Shared navigation, footer injection, dark mode, animations
   ============================================================ */

(function () {
  'use strict';

  /* ── Helpers ── */
  const $ = (sel, ctx = document) => ctx.querySelector(sel);
  const $$ = (sel, ctx = document) => [...ctx.querySelectorAll(sel)];
  const currentPath = window.location.pathname;

  /* ── Current year for footer ── */
  const YEAR = new Date().getFullYear();

  /* ── Navigation HTML ── */
  const navCategories = [
    { label: 'Technology',   href: '/technology/'    },
    { label: 'AI',           href: '/ai/'            },
    { label: 'Programming',  href: '/programming/'   },
    { label: 'Finance',      href: '/finance/'       },
    { label: 'Health',       href: '/health-wellness/' },
    { label: 'Education',    href: '/education/'     },
    { label: 'Career',       href: '/career/'        },
    { label: 'Business',     href: '/business/'      },
    { label: 'Productivity', href: '/productivity/'  },
    { label: 'Travel',       href: '/travel/'        },
    { label: 'Lifestyle',    href: '/lifestyle/'     },
  ];

  function isActive(href) {
    if (href === '/' && currentPath === '/') return true;
    if (href !== '/' && currentPath.startsWith(href)) return true;
    return false;
  }

  function buildNav() {
    const navLinksHTML = navCategories.map(c =>
      `<a href="${c.href}" class="nav-link${isActive(c.href) ? ' active' : ''}">${c.label}</a>`
    ).join('');

    const drawerLinksHTML = navCategories.map(c =>
      `<a href="${c.href}" class="nav-drawer-link${isActive(c.href) ? ' active' : ''}">${c.label}</a>`
    ).join('');

    return `
<nav class="site-nav" aria-label="Main navigation">
  <div class="container nav-inner">
    <a href="/" class="nav-logo" aria-label="InfoNest Home">
      <svg viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
        <rect width="40" height="40" rx="10" fill="#14B8A6" opacity="0.15"/>
        <path d="M20 6L34 14V26L20 34L6 26V14L20 6Z" stroke="#14B8A6" stroke-width="2" fill="none"/>
        <circle cx="20" cy="20" r="4" fill="#14B8A6"/>
        <line x1="20" y1="10" x2="20" y2="16" stroke="#14B8A6" stroke-width="1.5" stroke-linecap="round"/>
        <line x1="20" y1="24" x2="20" y2="30" stroke="#14B8A6" stroke-width="1.5" stroke-linecap="round"/>
        <line x1="10" y1="20" x2="16" y2="20" stroke="#14B8A6" stroke-width="1.5" stroke-linecap="round"/>
        <line x1="24" y1="20" x2="30" y2="20" stroke="#14B8A6" stroke-width="1.5" stroke-linecap="round"/>
      </svg>
      <span class="nav-logo-text">Info<span>Nest</span></span>
    </a>

    <div class="nav-menu" role="list">
      ${navLinksHTML}
    </div>

    <div class="nav-actions">
      <button class="theme-toggle" id="themeToggle" aria-label="Toggle dark mode" title="Toggle dark/light mode">
        <span class="theme-icon">🌙</span>
      </button>
      <button class="nav-hamburger" id="navHamburger" aria-label="Open menu" aria-expanded="false">
        <span></span><span></span><span></span>
      </button>
    </div>
  </div>
</nav>

<div class="nav-drawer" id="navDrawer" role="dialog" aria-label="Mobile navigation">
  ${drawerLinksHTML}
  <a href="/about/"            class="nav-drawer-link">About Us</a>
  <a href="/contact/"          class="nav-drawer-link">Contact</a>
  <a href="/editorial-policy/" class="nav-drawer-link">Editorial Policy</a>
</div>
    `.trim();
  }

  /* ── Footer HTML ── */
  function buildFooter() {
    return `
<footer class="site-footer">
  <div class="container">
    <!-- AD SLOT: Footer -->
    <div class="ad-slot ad-slot-footer" aria-label="Advertisement">Advertisement</div>

    <div class="footer-grid">
      <div class="footer-brand">
        <a href="/" class="nav-logo" style="margin-bottom:16px; display:inline-flex;">
          <span class="nav-logo-text">Info<span>Nest</span></span>
        </a>
        <p class="footer-tagline">Your go-to hub for trusted, well-researched content across technology, finance, health, career, and more. Knowledge, curated.</p>
      </div>

      <div>
        <h3 class="footer-col-title">Categories</h3>
        <nav class="footer-links" aria-label="Category links">
          <a href="/technology/"    class="footer-link">Technology</a>
          <a href="/ai/"            class="footer-link">Artificial Intelligence</a>
          <a href="/programming/"   class="footer-link">Programming</a>
          <a href="/finance/"       class="footer-link">Finance</a>
          <a href="/health-wellness/" class="footer-link">Health &amp; Wellness</a>
          <a href="/education/"     class="footer-link">Education</a>
        </nav>
      </div>

      <div>
        <h3 class="footer-col-title">More Topics</h3>
        <nav class="footer-links" aria-label="More topic links">
          <a href="/career/"        class="footer-link">Career</a>
          <a href="/business/"      class="footer-link">Business</a>
          <a href="/productivity/"  class="footer-link">Productivity</a>
          <a href="/travel/"        class="footer-link">Travel</a>
          <a href="/lifestyle/"     class="footer-link">Lifestyle</a>
        </nav>
      </div>

      <div>
        <h3 class="footer-col-title">Company</h3>
        <nav class="footer-links" aria-label="Company links">
          <a href="/about/"             class="footer-link">About Us</a>
          <a href="/contact/"           class="footer-link">Contact</a>
          <a href="/author/alex-morgan/" class="footer-link">Our Team</a>
          <a href="/editorial-policy/"  class="footer-link">Editorial Policy</a>
          <a href="/sitemap-page/"      class="footer-link">Sitemap</a>
        </nav>
      </div>
    </div>

    <div class="footer-bottom">
      <span>&copy; ${YEAR} InfoNest. All rights reserved. Hosted at <a href="https://infonest.page" class="footer-bottom-link">infonest.page</a></span>
      <div class="footer-bottom-links">
        <a href="/privacy-policy/" class="footer-bottom-link">Privacy Policy</a>
        <a href="/terms/"          class="footer-bottom-link">Terms of Service</a>
        <a href="/disclaimer/"     class="footer-bottom-link">Disclaimer</a>
      </div>
    </div>
  </div>
</footer>
    `.trim();
  }

  /* ── Inject nav & footer ── */
  function injectShared() {
    // Nav
    const navPlaceholder = $('#site-nav-placeholder');
    if (navPlaceholder) {
      navPlaceholder.outerHTML = buildNav();
    } else {
      // Insert at the beginning of body if no placeholder
      document.body.insertAdjacentHTML('afterbegin', buildNav());
    }

    // Footer
    const footerPlaceholder = $('#site-footer-placeholder');
    if (footerPlaceholder) {
      footerPlaceholder.outerHTML = buildFooter();
    } else {
      document.body.insertAdjacentHTML('beforeend', buildFooter());
    }
  }

  /* ── Dark Mode ── */
  function initTheme() {
    const saved = localStorage.getItem('infonest-theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const theme = saved || (prefersDark ? 'dark' : 'light');
    applyTheme(theme);
  }

  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('infonest-theme', theme);
    const icon = $('.theme-icon');
    if (icon) icon.textContent = theme === 'dark' ? '☀️' : '🌙';
  }

  function setupThemeToggle() {
    document.addEventListener('click', function (e) {
      if (e.target.closest('#themeToggle')) {
        const current = document.documentElement.getAttribute('data-theme') || 'light';
        applyTheme(current === 'dark' ? 'light' : 'dark');
      }
    });
  }

  /* ── Mobile Menu ── */
  function setupMobileMenu() {
    const hamburger = $('#navHamburger');
    const drawer    = $('#navDrawer');
    if (!hamburger || !drawer) return;

    hamburger.addEventListener('click', function () {
      const isOpen = drawer.classList.contains('open');
      drawer.classList.toggle('open');
      hamburger.classList.toggle('open');
      hamburger.setAttribute('aria-expanded', String(!isOpen));
      document.body.style.overflow = isOpen ? '' : 'hidden';
    });

    // Close on drawer link click
    $$('.nav-drawer-link', drawer).forEach(link => {
      link.addEventListener('click', () => {
        drawer.classList.remove('open');
        hamburger.classList.remove('open');
        hamburger.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = '';
      });
    });

    // Close on ESC
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && drawer.classList.contains('open')) {
        drawer.classList.remove('open');
        hamburger.classList.remove('open');
        hamburger.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = '';
        hamburger.focus();
      }
    });
  }

  /* ── Scroll to Top ── */
  function initScrollTop() {
    const btn = document.createElement('button');
    btn.className = 'scroll-top';
    btn.setAttribute('aria-label', 'Scroll to top');
    btn.innerHTML = '↑';
    document.body.appendChild(btn);

    window.addEventListener('scroll', function () {
      btn.classList.toggle('visible', window.scrollY > 400);
    }, { passive: true });

    btn.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  /* ── Reading Progress Bar (article pages) ── */
  function initReadingProgress() {
    if (!document.querySelector('.article-body')) return;

    const bar = document.createElement('div');
    bar.className = 'reading-progress';
    bar.setAttribute('role', 'progressbar');
    bar.setAttribute('aria-label', 'Reading progress');
    document.body.appendChild(bar);

    window.addEventListener('scroll', function () {
      const docHeight   = document.documentElement.scrollHeight - window.innerHeight;
      const progress    = docHeight > 0 ? (window.scrollY / docHeight) * 100 : 0;
      bar.style.width   = Math.min(100, progress) + '%';
      bar.setAttribute('aria-valuenow', Math.round(progress));
    }, { passive: true });
  }

  /* ── Intersection Observer Animations ── */
  function initAnimations() {
    const elements = $$('[data-animate]');
    if (!elements.length) return;

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('in-view');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

    elements.forEach((el, i) => {
      el.style.transitionDelay = (i * 60) + 'ms';
      observer.observe(el);
    });
  }

  /* ── Estimated Reading Time ── */
  function setReadingTime() {
    const body = $('.article-body');
    const display = $$('.reading-time-display');
    if (!body || !display.length) return;

    const words = body.textContent.trim().split(/\s+/).length;
    const minutes = Math.max(1, Math.ceil(words / 200));
    const label = `${minutes} min read`;
    display.forEach(el => { el.textContent = label; });
  }

  /* ── Unique Category Article Images & Clickable Cards ── */
  const uniqueImages = {
    "/technology/how-cloud-computing-works/": "https://images.unsplash.com/photo-1544197150-b99a580bb7a8?auto=format&fit=crop&w=800&q=80",
    "/technology/top-emerging-tech-trends/": "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=800&q=80",
    "/technology/cybersecurity-basics/": "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=800&q=80",
    "/ai/what-is-artificial-intelligence/": "/assets/images/ai_hero.png",
    "/ai/ai-tools-changing-productivity/": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=800&q=80",
    "/ai/ml-deep-learning-ai-differences/": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=800&q=80",
    "/programming/best-programming-languages-2026/": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=800&q=80",
    "/programming/beginners-roadmap-software-developer/": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?auto=format&fit=crop&w=800&q=80",
    "/programming/clean-code-principles/": "https://images.unsplash.com/photo-1607799279861-4dd421887fb3?auto=format&fit=crop&w=800&q=80",
    "/finance/personal-budgeting-101/": "https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?auto=format&fit=crop&w=800&q=80",
    "/finance/understanding-compound-interest/": "https://images.unsplash.com/photo-1559526324-4b87b5e36e44?auto=format&fit=crop&w=800&q=80",
    "/finance/beginners-guide-to-investing/": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?auto=format&fit=crop&w=800&q=80",
    "/health-wellness/daily-habits-improve-long-term-health/": "https://images.unsplash.com/photo-1506126613408-eca07ce68773?auto=format&fit=crop&w=800&q=80",
    "/health-wellness/understanding-sleep-cycles/": "https://images.unsplash.com/photo-1511295742364-92767fc06295?auto=format&fit=crop&w=800&q=80",
    "/health-wellness/nutrition-basics-balanced-diet/": "https://images.unsplash.com/photo-1498837167922-ddd27525d352?auto=format&fit=crop&w=800&q=80",
    "/education/effective-study-techniques/": "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?auto=format&fit=crop&w=800&q=80",
    "/education/how-to-choose-degree-program/": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?auto=format&fit=crop&w=800&q=80",
    "/education/free-online-learning-resources/": "https://images.unsplash.com/photo-1501504905252-473c47e087f8?auto=format&fit=crop&w=800&q=80",
    "/career/how-to-write-resume/": "https://images.unsplash.com/photo-1586281380349-632531db7ed4?auto=format&fit=crop&w=800&q=80",
    "/career/negotiating-your-salary/": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=800&q=80",
    "/career/switching-careers-step-by-step/": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=800&q=80",
    "/business/how-to-start-small-business/": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?auto=format&fit=crop&w=800&q=80",
    "/business/understanding-business-models/": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=800&q=80",
    "/business/marketing-on-a-budget/": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=800&q=80",
    "/productivity/time-management-techniques/": "https://images.unsplash.com/photo-1508962914676-134849a727f0?auto=format&fit=crop&w=800&q=80",
    "/productivity/how-to-build-habits-that-stick/": "https://images.unsplash.com/photo-1476480862126-209bfaa8edc8?auto=format&fit=crop&w=800&q=80",
    "/productivity/pomodoro-technique-explained/": "https://images.unsplash.com/photo-1484480974693-6ca0a78fb36b?auto=format&fit=crop&w=800&q=80",
    "/travel/budget-travel-tips-for-beginners/": "https://images.unsplash.com/photo-1488646953014-85cb44e25828?auto=format&fit=crop&w=800&q=80",
    "/travel/how-to-plan-a-trip/": "https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?auto=format&fit=crop&w=800&q=80",
    "/travel/essential-packing-checklist/": "https://images.unsplash.com/photo-1527853787696-f7be74f2e39a?auto=format&fit=crop&w=800&q=80",
    "/lifestyle/building-a-morning-routine/": "https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=800&q=80",
    "/lifestyle/minimalism-101/": "https://images.unsplash.com/photo-1513519245088-0e12902e5a38?auto=format&fit=crop&w=800&q=80",
    "/lifestyle/sustainable-living-small-changes/": "https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?auto=format&fit=crop&w=800&q=80",
    "/lifestyle/digital-detox-guide/": "https://images.unsplash.com/photo-1526304640581-d334cdbbf45e?auto=format&fit=crop&w=800&q=80"
  };

  function setupUniqueImagesAndClickableCards() {
    // 1. Process standard cards
    const cards = $$('.card');
    cards.forEach(card => {
      const link = $('a', card);
      if (link) {
        const href = link.getAttribute('href');
        if (uniqueImages[href]) {
          const placeholder = $('.card-img-placeholder', card) || $('.featured-card-img-placeholder', card);
          if (placeholder) {
            placeholder.style.setProperty('background-image', `url('${uniqueImages[href]}')`, 'important');
            placeholder.style.fontSize = '0';
            placeholder.style.color = 'transparent';
            placeholder.style.backgroundSize = 'cover';
            placeholder.style.backgroundPosition = 'center';
            placeholder.style.backgroundRepeat = 'no-repeat';
          }
        }
        
        // Click action for entire card
        card.style.cursor = 'pointer';
        card.addEventListener('click', (e) => {
          if (e.target.tagName === 'A' || e.target.closest('a')) return;
          link.click();
        });
      }
    });

    // 2. Process featured card on homepage
    const featuredCards = $$('.featured-card');
    featuredCards.forEach(fCard => {
      const link = $('a', fCard) || fCard;
      const href = fCard.getAttribute('href') || (link !== fCard ? link.getAttribute('href') : null);
      
      if (href && uniqueImages[href]) {
        const placeholder = $('.featured-card-img-placeholder', fCard);
        if (placeholder) {
          placeholder.style.setProperty('background-image', `url('${uniqueImages[href]}')`, 'important');
          placeholder.style.fontSize = '0';
          placeholder.style.color = 'transparent';
          placeholder.style.backgroundSize = 'cover';
          placeholder.style.backgroundPosition = 'center';
          placeholder.style.backgroundRepeat = 'no-repeat';
        }
      }

      if (link && link !== fCard) {
        fCard.style.cursor = 'pointer';
        fCard.addEventListener('click', (e) => {
          if (e.target.tagName === 'A' || e.target.closest('a')) return;
          link.click();
        });
      }
    });

    // 3. Process current article page main hero image
    const path = window.location.pathname;
    if (uniqueImages[path]) {
      const heroPlaceholder = $('.article-hero-placeholder');
      if (heroPlaceholder) {
        heroPlaceholder.style.setProperty('background-image', `url('${uniqueImages[path]}')`, 'important');
        heroPlaceholder.style.fontSize = '0';
        heroPlaceholder.style.color = 'transparent';
        heroPlaceholder.style.backgroundSize = 'cover';
        heroPlaceholder.style.backgroundPosition = 'center';
        heroPlaceholder.style.backgroundRepeat = 'no-repeat';
      }
    }
  }

  /* ── Sidebar Category Icons SVG Mapping ── */
  const sidebarCategoryIcons = {
    "technology": `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>`,
    "ai": `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><line x1="9" y1="1" x2="9" y2="4"/><line x1="15" y1="1" x2="15" y2="4"/><line x1="9" y1="20" x2="9" y2="23"/><line x1="15" y1="20" x2="15" y2="23"/><line x1="20" y1="9" x2="23" y2="9"/><line x1="20" y1="15" x2="23" y2="15"/><line x1="1" y1="9" x2="4" y2="9"/><line x1="1" y1="15" x2="4" y2="15"/></svg>`,
    "programming": `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>`,
    "finance": `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>`,
    "health": `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>`,
    "education": `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>`,
    "career": `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>`,
    "business": `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg>`,
    "productivity": `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>`,
    "travel": `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/></svg>`,
    "lifestyle": `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.24 12.24a6 6 0 0 0-8.49-8.49L5 10.5V19h8.5z"/><line x1="16" y1="8" x2="2" y2="22"/><line x1="17.5" y1="15" x2="9" y2="15"/></svg>`
  };

  function setupSidebarIcons() {
    const sidebarLinks = $$('.sidebar-cat-link');
    sidebarLinks.forEach(link => {
      const href = link.getAttribute('href');
      let catKey = "";
      if (href.includes('/technology/')) catKey = "technology";
      else if (href.includes('/ai/')) catKey = "ai";
      else if (href.includes('/programming/')) catKey = "programming";
      else if (href.includes('/finance/')) catKey = "finance";
      else if (href.includes('/health-wellness/')) catKey = "health";
      else if (href.includes('/education/')) catKey = "education";
      else if (href.includes('/career/')) catKey = "career";
      else if (href.includes('/business/')) catKey = "business";
      else if (href.includes('/productivity/')) catKey = "productivity";
      else if (href.includes('/travel/')) catKey = "travel";
      else if (href.includes('/lifestyle/')) catKey = "lifestyle";

      if (catKey && sidebarCategoryIcons[catKey]) {
        const countSpan = $('.sidebar-cat-count', link);
        const countHTML = countSpan ? countSpan.outerHTML : '';
        
        let cleanText = link.textContent;
        // Strip emojis
        cleanText = cleanText.replace(/[\uE000-\uF8FF]|\uD83C[\uDC00-\uDFFF]|\uD83D[\uDC00-\uDFFF]|[\u2011-\u26FF]|\uD83E[\uDC00-\uDFFF]/g, '');
        if (countSpan) {
          cleanText = cleanText.replace(countSpan.textContent, '');
        }
        cleanText = cleanText.trim();

        link.innerHTML = `${sidebarCategoryIcons[catKey]} <span class="sidebar-cat-name">${cleanText}</span> ${countHTML}`;
      }
    });

    // Clean up emojis in category-header and page-header labels (e.g. "💰 Category" -> "Category")
    const pageLabels = $$('.page-header .section-label, .category-header .section-label');
    pageLabels.forEach(label => {
      let text = label.textContent;
      text = text.replace(/[\uE000-\uF8FF]|\uD83C[\uDC00-\uDFFF]|\uD83D[\uDC00-\uDFFF]|[\u2011-\u26FF]|\uD83E[\uDC00-\uDFFF]/g, '');
      label.textContent = text.trim();
    });
  }

  /* ── Initialize ── */
  function init() {
    injectShared();
    initTheme();
    setupThemeToggle();
    setupMobileMenu();
    initScrollTop();
    initReadingProgress();
    initAnimations();
    setReadingTime();
    setupUniqueImagesAndClickableCards();
    setupSidebarIcons();

    // Dynamically inject Google AdSense script
    const adScript = document.createElement('script');
    adScript.async = true;
    adScript.src = "https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2344063334800709";
    adScript.setAttribute('crossorigin', 'anonymous');
    document.head.appendChild(adScript);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();

