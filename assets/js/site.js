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
<a class="skip-link" href="#main-content">Skip to content</a>
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

    <div class="nav-menu">
      ${navLinksHTML}
      <a href="/about/" class="nav-link${isActive('/about/') ? ' active' : ''}">About</a>
      <a href="/contact/" class="nav-link${isActive('/contact/') ? ' active' : ''}">Contact</a>
    </div>

    <div class="nav-actions">
      <button class="theme-toggle" id="themeToggle" aria-label="Toggle dark mode" title="Toggle dark/light mode">
        <span class="theme-icon">🌙</span>
      </button>
      <button class="nav-hamburger" id="navHamburger" aria-label="Open menu" aria-expanded="false" aria-controls="navDrawer">
        <span></span><span></span><span></span>
      </button>
    </div>
  </div>
</nav>

<div class="nav-drawer" id="navDrawer" hidden role="dialog" aria-label="Mobile navigation" aria-hidden="true">
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
    <div class="footer-grid">
      <div class="footer-brand">
        <a href="/" class="nav-logo" style="margin-bottom:16px; display:inline-flex;">
          <span class="nav-logo-text">Info<span>Nest</span></span>
        </a>
        <p class="footer-tagline">Practical, original explainers for work and life. Published by the InfoNest editorial team. Contact: hello@infonest.page</p>
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
          <a href="/editorial-policy/"  class="footer-link">Editorial Policy</a>
          <a href="/sitemap-page/"      class="footer-link">Sitemap</a>
        </nav>
      </div>
    </div>

    <p class="cookie-note">Theme preference is stored on this device. After ads are approved, Google AdSense may set advertising cookies. See the <a href="/privacy-policy/">Privacy Policy</a>.</p>
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

    function setDrawer(open) {
      drawer.classList.toggle('open', open);
      hamburger.classList.toggle('open', open);
      hamburger.setAttribute('aria-expanded', String(open));
      drawer.hidden = !open;
      drawer.setAttribute('aria-hidden', open ? 'false' : 'true');
      document.body.style.overflow = open ? 'hidden' : '';
    }

    hamburger.addEventListener('click', function () {
      setDrawer(!drawer.classList.contains('open'));
    });

    $$('.nav-drawer-link', drawer).forEach(link => {
      link.addEventListener('click', () => setDrawer(false));
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && drawer.classList.contains('open')) {
        setDrawer(false);
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

  /* ── Clickable cards (heroes are original CSS/SVG) ── */
  function setupUniqueImagesAndClickableCards() {
    $$('.article-hero-placeholder, .card-img-placeholder, .featured-card-img-placeholder').forEach((el) => {
      el.style.fontSize = '0';
      el.style.color = 'transparent';
    });

    const cards = $$('.card');
    cards.forEach(card => {
      const link = $('a', card);
      if (link) {
        card.style.cursor = 'pointer';
        card.addEventListener('click', (e) => {
          if (e.target.tagName === 'A' || e.target.closest('a')) return;
          link.click();
        });
      }
    });

    const featuredCards = $$('.featured-card');
    featuredCards.forEach(fCard => {
      const link = $('a', fCard) || fCard;
      if (link && link !== fCard) {
        fCard.style.cursor = 'pointer';
        fCard.addEventListener('click', (e) => {
          if (e.target.tagName === 'A' || e.target.closest('a')) return;
          link.click();
        });
      }
    });
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
        const counts = {
          technology: 8, ai: 5, programming: 5, finance: 6, health: 6,
          education: 5, career: 6, business: 5, productivity: 5, travel: 5, lifestyle: 6
        };
        const countSpan = $('.sidebar-cat-count', link);
        if (countSpan && counts[catKey]) countSpan.textContent = String(counts[catKey]);
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

  function setupContactForm() {
    const form = $('#contact-form');
    if (!form) return;

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      const name = ($('#contact-name', form) || {}).value || '';
      const email = ($('#contact-email', form) || {}).value || '';
      const subject = ($('#contact-subject', form) || {}).value || 'InfoNest contact';
      const message = ($('#contact-message', form) || {}).value || '';
      const body = encodeURIComponent(`From: ${name} <${email}>\n\n${message}`);
      const mailto = `mailto:hello@infonest.page?subject=${encodeURIComponent(subject)}&body=${body}`;
      window.location.href = mailto;
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
    setupContactForm();
  }

  window.addEventListener('load', function () {
    setTimeout(function () {
      if (document.querySelector('script[src*="adsbygoogle"]')) return;
      var s = document.createElement('script');
      s.async = true;
      s.src = 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2344063334800709';
      s.setAttribute('crossorigin', 'anonymous');
      document.head.appendChild(s);
    }, 4000);
  });

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();

