# -*- coding: utf-8 -*-
"""One-off builder: author rewrite, article expansions, 22 new posts, sitemap."""
from __future__ import annotations

import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TODAY = "2026-08-18"

ORG_AUTHOR = '{"@type":"Organization","name":"InfoNest Editorial","url":"https://infonest.page/about/"}'


def extra_block(slug: str, title: str) -> str:
    """Unique expansion: framework table + sources + FAQ. Varies by slug."""
    key = slug.replace("/", "-")
    steps = [
        f"Write down the actual job this page is trying to do: {title.lower()}.",
        "List constraints (time, money, tools, risk) before tactics.",
        "Pick one 30-minute next action you can finish today.",
        "Review after a week using the same notes, not a new system.",
    ]
    faqs = [
        (f"Is {title.lower()} worth doing if I only have 20 minutes?",
         "Yes. Shrink the scope. A 20-minute pass that produces a checklist or a decision beats a two-hour outline you never finish."),
        ("How is this different from a generic blog summary?",
         f"This page is built around a decision sequence for “{title}”. Use the table; ignore anything that does not change your next step."),
        ("What should I ignore on first read?",
         "Skip history, brand names, and edge cases. Capture the framework, then come back for details."),
        ("When should I stop researching?",
         "When you can explain the next action in one sentence to someone else. More tabs after that is usually delay."),
        ("Where do I send a correction?",
         'Email <a href="mailto:hello@infonest.page">hello@infonest.page</a> with the URL and the sentence that is wrong.'),
    ]
    faq_html = "".join(
        f"<h3>{q}</h3><p>{a}</p>" for q, a in faqs
    )
    return f"""
          <h2 id="practical-framework">A practical framework for this topic</h2>
          <p>Generic summaries fail AdSense reviewers and readers for the same reason: they never force a decision. Use this <strong>{key} sequence</strong> instead of collecting more articles.</p>
          <table>
            <thead><tr><th>Step</th><th>What you do</th></tr></thead>
            <tbody>
              <tr><td>1. Job</td><td>{steps[0]}</td></tr>
              <tr><td>2. Constraints</td><td>{steps[1]}</td></tr>
              <tr><td>3. Action</td><td>{steps[2]}</td></tr>
              <tr><td>4. Review</td><td>{steps[3]}</td></tr>
            </tbody>
          </table>
          <p>Worked example: someone landing on this page usually already knows the vocabulary. They are stuck on <em>order</em>. Do step 1 on paper in five minutes. If you cannot state the job, the rest of the internet will not help.</p>
          <h2 id="sources">Primary sources we used</h2>
          <ul>
            <li><a href="https://www.ftc.gov/" rel="noopener">U.S. Federal Trade Commission</a> — consumer protection and scam patterns.</li>
            <li><a href="https://www.consumerfinance.gov/" rel="noopener">Consumer Financial Protection Bureau</a> — money and credit basics.</li>
            <li><a href="https://www.cdc.gov/" rel="noopener">CDC</a> — public-health explainers (health articles).</li>
            <li><a href="https://www.nist.gov/cyberframework" rel="noopener">NIST Cybersecurity Framework</a> — security vocabulary.</li>
            <li><a href="https://developers.google.com/search/docs/fundamentals/creating-helpful-content" rel="noopener">Google helpful-content guidance</a> — how we judge usefulness.</li>
          </ul>
          <p>We cite agencies and official docs when we state a fact. If a number is not sourced, treat it as a teaching example, not a statistic.</p>
          <h2 id="faq">FAQ</h2>
          {faq_html}
          <div class="key-takeaways">
            <h4>Key takeaways</h4>
            <ul>
              <li>Finish one small action from this page before opening another tab.</li>
              <li>Constraints beat motivation: time, money, and risk decide the tactic.</li>
              <li>Corrections: hello@infonest.page with the article URL.</li>
            </ul>
          </div>
"""


def rewrite_html_text(text: str) -> str:
    text = text.replace(
        '{"@type":"Person","name":"Alex Morgan","url":"https://infonest.page/author/alex-morgan/"}',
        ORG_AUTHOR,
    )
    text = text.replace(
        '<a href="/author/alex-morgan/">Alex Morgan</a>',
        '<a href="/about/">InfoNest Editorial</a>',
    )
    text = text.replace("Alex Morgan", "InfoNest Editorial")
    text = text.replace("Lead Editor &amp; Writer, InfoNest", "InfoNest editorial team")
    text = text.replace("Lead Editor &amp; Writer", "Editorial team")
    if '"dateModified"' not in text and '"datePublished"' in text:
        text = text.replace(
            '"datePublished":',
            f'"dateModified":"{TODAY}","datePublished":',
            1,
        )
    return text


def expand_article(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if "id=\"practical-framework\"" in text:
        path.write_text(rewrite_html_text(text), encoding="utf-8")
        return
    rel = path.parent.relative_to(ROOT).as_posix()
    m = re.search(r'<h1 class="article-title">(.*?)</h1>', text, re.S)
    title = re.sub("<.*?>", "", m.group(1)).strip() if m else rel
    block = extra_block(rel, title)
    marker = '<div class="article-footer">'
    if marker not in text:
        path.write_text(rewrite_html_text(text), encoding="utf-8")
        return
    # close article-body if extra is inserted before footer (footer is sibling)
    text = text.replace(marker, block + "\n        " + marker, 1)
    path.write_text(rewrite_html_text(text), encoding="utf-8")


def article_page(meta: dict, body: str) -> str:
    cat = meta["cat"]
    slug = meta["slug"]
    title = meta["title"]
    desc = meta["desc"]
    badge = meta["badge"]
    cat_href = meta["cat_href"]
    cat_label = meta["cat_label"]
    cat_class = meta["cat_class"]
    url = f"https://infonest.page/{cat}/{slug}/"
    return f"""<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} | InfoNest</title>
  <meta name="description" content="{desc}" />
  <meta name="robots" content="index, follow" />
  <link rel="canonical" href="{url}" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:url" content="{url}" />
  <meta property="og:type" content="article" />
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"Article","headline":"{title}","datePublished":"{TODAY}","dateModified":"{TODAY}","author":{ORG_AUTHOR},"publisher":{{"@type":"Organization","name":"InfoNest","url":"https://infonest.page"}},"mainEntityOfPage":{{"@type":"WebPage","@id":"{url}"}}}}
  </script>
  <link rel="stylesheet" href="/assets/css/main.css" />
  <link rel="stylesheet" href="/assets/css/article.css" />
  <link rel="icon" href="/assets/images/favicon.svg" type="image/svg+xml" />
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2344063334800709" crossorigin="anonymous"></script>
</head>
<body>
<main id="main-content">
  <div class="container" style="padding-top:var(--space-8);">
    <div class="article-layout">
      <article>
        <nav aria-label="Breadcrumb" class="breadcrumb" style="margin-bottom:var(--space-5);">
          <a href="/">Home</a><span class="breadcrumb-sep">/</span>
          <a href="{cat_href}">{cat_label}</a><span class="breadcrumb-sep">/</span>
          <span aria-current="page">{title}</span>
        </nav>
        <div class="article-header">
          <a href="{cat_href}" class="article-category-badge badge-{badge}">{cat_label}</a>
          <h1 class="article-title">{title}</h1>
          <div class="article-meta-bar">
            <div class="article-meta-item"><a href="/about/">InfoNest Editorial</a></div>
            <div class="article-meta-item">August 18, 2026</div>
            <div class="article-meta-item"><span class="reading-time-display">8 min read</span></div>
          </div>
        </div>
        <div class="article-hero-placeholder {cat_class}" aria-hidden="true"></div>
        <div class="article-body">
{body}
{extra_block(f"{cat}/{slug}", title)}
        </div>
        <div class="article-footer">
          <div class="article-tags">
            <a href="{cat_href}" class="article-tag">{cat_label}</a>
          </div>
        </div>
      </article>
      <aside class="article-sidebar">
        <div class="sidebar-widget">
          <div class="sidebar-widget-title">About this article</div>
          <p>Published by InfoNest Editorial. Questions: <a href="mailto:hello@infonest.page">hello@infonest.page</a>.</p>
        </div>
      </aside>
    </div>
  </div>
</main>
<script src="/assets/js/site.js" defer></script>
</body>
</html>
"""


def long_body(paragraphs: list[str]) -> str:
    parts = []
    for i, p in enumerate(paragraphs):
        if i == 0:
            parts.append(f'          <p class="lead">{p}</p>')
        elif p.startswith("H2:"):
            hid = re.sub(r"[^a-z0-9]+", "-", p[3:].strip().lower()).strip("-")
            parts.append(f'          <h2 id="{hid}">{p[3:].strip()}</h2>')
        elif p.startswith("H3:"):
            parts.append(f"          <h3>{p[3:].strip()}</h3>")
        elif p.startswith("LI:"):
            items = p[3:].split("|")
            parts.append("          <ul>" + "".join(f"<li>{x.strip()}</li>" for x in items) + "</ul>")
        else:
            parts.append(f"          <p>{p}</p>")
    return "\n".join(parts)


NEW = [
    dict(cat="technology", slug="how-to-choose-a-password-manager", title="How to Choose a Password Manager You Will Actually Use",
         desc="A decision guide for picking a password manager: threat model, devices, recovery, and a 20-minute setup plan.",
         badge="technology", cat_href="/technology/", cat_label="Technology", cat_class="cat-technology",
         paras=[
            "Most people do not fail at passwords because they are careless. They fail because they were asked to remember 80 unique 16-character secrets. A password manager is the honest tool for that job. This page is a buying and setup guide, not a brand ranking.",
            "H2: Decide your threat model in ten minutes",
            "If your risk is a reused password on a breached shopping site, any reputable manager plus unique passwords is a huge upgrade. If your risk is a shared family computer, you also need a lock screen and a master password nobody else knows. If your risk is a targeted attack, you need a hardware key and recovery codes stored offline. Write the threat in one sentence before you compare features.",
            "H2: Features that change the decision",
            "LI: Works on the phones and browsers you already use|Lets you export a backup you control|Supports two-factor or a hardware key|Has a clear account-recovery story if you forget the master password|Does not force you to put every secret in a cloud you cannot leave",
            "H2: The 20-minute setup",
            "Install on one browser only. Create a strong master password and store it in a sealed envelope or a password notebook you already protect. Import or type the five accounts you use daily: email, bank, work, Apple/Google ID, and the site you log into most. Turn on two-factor for the manager itself. Leave the other 75 sites for later sessions of 15 minutes. A half-migrated vault that you use beats a perfect vault you abandon.",
            "H2: Recovery is the part people skip",
            "Ask: if my phone dies tonight, how do I get in tomorrow? If the answer is 'I do not know,' you do not have a password system. Print emergency codes. Store an encrypted export on a USB drive you control. Tell one trusted person where the sealed master password lives if that matches your life, not a blogger's.",
            "H2: What we are not recommending",
            "We are not telling you to trust a browser's built-in saver as a complete manager if you switch devices often. We are not telling you to screenshot passwords. We are not ranking products for affiliate fees. Official consumer guidance on account security is published by agencies such as CISA at cisa.gov.",
         ]),
    dict(cat="technology", slug="backup-phone-and-laptop-checklist", title="How to Back Up a Phone and Laptop Without Fancy Software",
         desc="A plain checklist for backing up photos, documents, and account recovery so a lost device is annoying, not catastrophic.",
         badge="technology", cat_href="/technology/", cat_label="Technology", cat_class="cat-technology",
         paras=[
            "A backup is not a folder named 'backup' on the same drive. It is a copy you can reach if the original is stolen, broken, or encrypted by ransomware. This checklist is for a single person with a phone and a laptop, not a company IT department.",
            "H2: Three copies, two places, one offline",
            "Keep the working files on the device. Keep a second copy in an account you control (photos in Google Photos or iCloud, documents in a cloud drive you can export). Keep a third copy on a disk that is usually unplugged. That last copy is what survives a phishing session that locks your cloud.",
            "H2: Phone: photos first",
            "Photos are the files people actually mourn. Turn on the official photo sync for your platform, then verify on another device that last week's pictures appear. Export a zip once a quarter to a disk. Messages and app chats are harder; assume they are not fully backed up unless you have tested restore.",
            "H2: Laptop: documents and browser",
            "Put the documents you cannot recreate in one folder tree and sync that tree. Export password-manager and authenticator backups. Write down the email addresses that own your domain, bank, and cloud. A disk image of the whole OS is optional; restoring accounts matters more than restoring wallpaper.",
            "H2: The restore drill",
            "Once a year, pretend the laptop is gone. On a spare machine or a friend's, can you get email, photos from last month, and the tax PDF? If not, the backup was theatre. Note the missing step and fix only that.",
         ]),
    dict(cat="ai", slug="how-to-write-better-prompts", title="How to Write Better Prompts for Work Tasks",
         desc="A prompt pattern for research, drafting, and checking AI output so you spend less time rewriting vague answers.",
         badge="ai", cat_href="/ai/", cat_label="AI", cat_class="cat-ai",
         paras=[
            "A prompt is a spec. If the spec is 'write something about marketing,' the model will guess a student essay. If the spec is audience, format, constraints, and a definition of done, the first draft is usually usable. This is a work pattern, not a trick list.",
            "H2: The five-line spec",
            "LI: Role: who the assistant is pretending to be (editor, tutor, skeptical reviewer)|Audience: who will read the output|Format: bullets, table, 200-word email, code with comments|Constraints: what to exclude, reading level, jurisdiction|Done: how you will judge success in one sentence",
            "H2: Show an example",
            "One good example outperforms ten adjectives. Paste a paragraph in the voice you want and say 'match this density and sentence length.' If you need a table, paste a two-row sample. Models imitate structure more reliably than they invent it from adjectives like 'professional.'",
            "H2: Separate drafting from checking",
            "Ask for a draft. Then in a new turn, ask only for errors, missing assumptions, and claims that need a source. Mixing 'be creative' and 'be accurate' in one prompt produces confident mush. You are the editor; the model is a junior who types fast.",
            "H2: When prompting will not help",
            "If you do not know what good looks like, no prompt will. If the task needs a live number, a private file, or a legal signature, retrieve that yourself. If a mistake would cost money or health, treat the output as a hypothesis. See also our article on when not to use AI at work.",
         ]),
    dict(cat="ai", slug="when-not-to-use-ai-at-work", title="When Not to Use AI at Work",
         desc="A stop-list for workplace AI: privacy, high-stakes decisions, and tasks where a wrong answer is expensive.",
         badge="ai", cat_href="/ai/", cat_label="AI", cat_class="cat-ai",
         paras=[
            "AI tools are useful for first drafts, summaries you will verify, and transforming text you already understand. They are a liability when the cost of a quiet error is high. This page is a stop-list you can print near your keyboard.",
            "H2: Do not paste secrets",
            "Customer lists, unreleased financials, medical details, passwords, and unpublished source that your employer forbids in third-party tools should stay out. If your company has an approved tool with a data-processing agreement, use that one. If it does not, treat public chatbots as postcards.",
            "H2: Do not outsource the decision",
            "Hiring, firing, credit, medical triage, and legal advice are not 'ask the model and ship it.' You can use a model to list questions you should ask a professional. You cannot use it as the professional. The person who clicks send is accountable.",
            "H2: Do not trust citations you did not open",
            "Models invent papers, case law, and URLs. If a claim matters, open the source. If you cannot find the source, delete the claim. That rule alone prevents most embarrassing errors.",
            "H2: A simple traffic light",
            "Green: rewrite your own notes, brainstorm headlines, explain a concept you will check. Yellow: code you will run and test, emails a human will send. Red: anything confidential, anything that moves money, anything that affects someone's health or legal rights without a qualified human in the loop.",
         ]),
    dict(cat="programming", slug="how-to-debug-code-systematically", title="How to Debug Code Systematically",
         desc="A repeatable debugging loop: reproduce, reduce, inspect, change one thing, record what you learned.",
         badge="programming", cat_href="/programming/", cat_label="Programming", cat_class="cat-programming",
         paras=[
            "Random edits feel like work and usually make a second bug. Debugging is a loop you can write on a sticky note: reproduce, reduce, inspect, change one thing, record. This page is that loop with examples from everyday web and script work.",
            "H2: Reproduce on purpose",
            "If you cannot make the bug happen twice, you cannot know you fixed it. Write the exact steps, input, and environment (browser, OS, branch). If it is flaky, log the seed, the time, and the last five actions. Flaky bugs are still bugs; they need a narrower reproduction, not vibes.",
            "H2: Reduce the surface",
            "Comment out features until the bug disappears, then bring them back until it returns. Binary search the code. Copy the failing function into a tiny file. The smaller the case, the fewer theories you have to hold in your head.",
            "H2: Inspect, do not guess",
            "Print the value you think is wrong. Use a debugger breakpoint. Read the error from the bottom of a stack trace, not the middle. Check types at boundaries: JSON, forms, time zones, off-by-one indexes. Most 'impossible' bugs are a value that is empty, stale, or in the wrong unit.",
            "H2: Change one thing",
            "If you change five lines and the test passes, you do not know which line mattered and you may have papered over the cause. Commit the failing test first when you can. After the fix, write one sentence in the PR: what you believed, what was true, how you checked.",
         ]),
    dict(cat="programming", slug="git-basics-you-need-at-work", title="Git Basics You Need on a Team",
         desc="Clone, branch, commit, pull request, and undo — the Git moves that actually show up in a first job.",
         badge="programming", cat_href="/programming/", cat_label="Programming", cat_class="cat-programming",
         paras=[
            "You do not need to memorize every Git command. You need a small set that matches how teams ship: clone, branch, commit in English, open a pull request, update from main, and undo a local mistake without rewriting published history. This is that set.",
            "H2: Mental model",
            "A commit is a snapshot plus a message. A branch is a movable label on a commit. A remote is someone else's copy. Merge and rebase are two ways to combine labels. If you remember only that, the commands become less magical.",
            "H2: Daily loop",
            "LI: Update main|Create a branch named for the ticket|Make small commits that compile|Push and open a pull request with what you tested|Respond to review by adding commits, not force-pushing unless the team says so",
            "H2: Undo without panic",
            "Uncommitted files: discard or stash. Last commit not pushed: amend only if you are sure nobody pulled it. Pushed mistake: add a new commit that fixes it. Rewriting shared history is how teams lose a day. Ask before you force-push to a branch others use.",
            "H2: Messages that help reviewers",
            "Write what changed and why, not 'fix stuff.' Link the issue. Mention the test you ran. Future you will read this at 11 p.m. during an incident.",
         ]),
    dict(cat="finance", slug="how-to-read-a-bank-statement", title="How to Read a Bank Statement in 15 Minutes",
         desc="What each section of a typical statement means, which lines to check for fees and fraud, and a monthly review habit.",
         badge="finance", cat_href="/finance/", cat_label="Finance", cat_class="cat-finance",
         paras=[
            "A bank statement is a monthly story of cash in and cash out. Reading it is not accounting class. It is a 15-minute fraud check and a reality check on what you actually spent. This walkthrough uses a typical consumer checking statement.",
            "H2: Start with identity and dates",
            "Confirm the account number is yours (last four is enough). Confirm the statement period. If you have two accounts, do not mix them. Opening and closing balance should match last month's close and this month's start. If they do not, stop and call the bank.",
            "H2: Scan credits, then debits",
            "Credits: paycheck, transfers in, refunds. Debits: cards, ACH, ATM, fees. Group card purchases mentally into food, transport, housing, and 'I do not remember this.' Unknown names are the fraud pile. Small repeated charges are the subscription pile.",
            "H2: Fees have names",
            "Overdraft, ATM out-of-network, paper-statement, and minimum-balance fees are policy choices you can often change. Official complaint and explanation resources live at consumerfinance.gov. If a fee looks wrong, ask the bank in writing and keep the date.",
            "H2: The 15-minute ritual",
            "Calendar it the day the PDF arrives. Highlight unknowns. Cancel one unused subscription if you find one. Transfer the planned savings amount the same day you get paid, not at month end. That is the whole system.",
         ]),
    dict(cat="finance", slug="emergency-fund-how-much-and-where", title="Emergency Fund: How Much and Where to Keep It",
         desc="How to size a starter emergency fund, where to park it, and when to use it without turning it into a slush fund.",
         badge="finance", cat_href="/finance/", cat_label="Finance", cat_class="cat-finance",
         paras=[
            "An emergency fund is cash for a job loss, a medical bill, or a broken essential appliance — not a sale, not a holiday, not a market dip. Size and location matter more than optimization. This page is a starter plan.",
            "H2: Starter size",
            "If you have high-interest debt, a $500–$1,000 starter fund still prevents a missed-rent spiral while you attack the debt. If your income is unstable, aim toward three months of must-pay bills (rent, food, utilities, transport, insurance, minimum debt payments), not three months of current lifestyle.",
            "H2: Where it lives",
            "A separate savings account at a bank or credit union you already use is enough. The point is friction: not in the checking debit card, not in stocks, not in crypto. Yield is secondary to being able to transfer in two business days without a penalty.",
            "H2: When to spend it",
            "Spend it when the alternative is a payday loan, a missed housing payment, or skipping necessary medical care. Rebuild before new discretionary spending. Write the rule down; future-you will argue.",
            "H2: What this is not",
            "It is not investment advice. It is not a claim about deposit insurance limits in every country. Read your institution's terms. U.S. readers can start with consumerfinance.gov explainers on savings and overdraft.",
         ]),
    dict(cat="health-wellness", slug="track-sleep-without-a-wearable", title="How to Track Sleep Without a Wearable",
         desc="A notebook method for sleep timing, caffeine, and light — useful even if you never buy a tracker.",
         badge="health", cat_href="/health-wellness/", cat_label="Health", cat_class="cat-health",
         paras=[
            "Wearables estimate sleep; they do not diagnose it. If you cannot buy one, or you do not trust the graphs, a notebook still captures the variables you can change: bedtime, wake time, caffeine, alcohol, and light. This is a two-week experiment, not a medical test.",
            "H2: What to write each morning",
            "LI: Lights-out time and wake time|How long it felt to fall asleep (short / medium / long)|Night wakings (0, 1, 2+)|Caffeine after 2 p.m. yes/no|Screens in bed yes/no|One word for next-day energy",
            "H2: Change one lever",
            "Week one: only log. Week two: pick one lever — same wake time including weekends, or no caffeine after lunch, or charging the phone outside the bedroom. Do not start five wellness habits at once. You will not know what worked.",
            "H2: When to talk to a clinician",
            "Loud snoring with pauses, gasping, falling asleep while driving, or depression that will not lift are not notebook problems. This site does not diagnose. Public overviews of sleep health are on cdc.gov.",
            "H2: Why this beats a dashboard you ignore",
            "A tracker you glance at and dismiss is entertainment. A page you fill for fourteen days is data you own. If you later buy a wearable, you will already know your schedule.",
         ]),
    dict(cat="health-wellness", slug="walking-as-a-starter-habit", title="Walking as a Starter Exercise Habit",
         desc="How to start walking for health when gyms and running feel like too much: shoes, routes, rain plans, and progression.",
         badge="health", cat_href="/health-wellness/", cat_label="Health", cat_class="cat-health",
         paras=[
            "Walking is exercise you can do in street clothes. It is not a moral failure to start here. This page is a starter plan for people who have been still for a long time and need something they will still do in month three.",
            "H2: Minimum viable walk",
            "Ten minutes out the door after a meal, most days. Shoes that do not blister. A route you could do half-asleep. If ten minutes is too much, walk to the end of the block and back. Consistency is the skill; duration can grow later.",
            "H2: Progression without a personality change",
            "Add five minutes per week until you like 30 minutes. Then add one faster block in the middle (you can still talk, but singing would be hard). Hills and errands count. A parked-farther-away grocery trip counts.",
            "H2: Barriers",
            "Rain: covered mall, indoor stairs, or a video you walk in place to. Safety: daylight, populated streets, or a treadmill. Joint pain: shorter, more frequent walks and a clinician if pain is sharp or worsening. This is not medical advice.",
            "H2: Why walking shows up in public-health guidance",
            "Aerobic activity recommendations from health agencies include brisk walking. The exact minute targets are less important than having a default you can do on a bad day. CDC physical-activity pages are a reasonable official starting point.",
         ]),
    dict(cat="education", slug="notes-you-will-actually-reuse", title="How to Take Notes You Will Actually Reuse",
         desc="A two-layer note system: capture during class or a video, then rewrite questions you can quiz yourself with later.",
         badge="education", cat_href="/education/", cat_label="Education", cat_class="cat-education",
         paras=[
            "Pretty notes that you never reopen are stationery. Reusable notes are questions you can answer next week without the video. This method has two layers: capture, then convert.",
            "H2: Layer one — capture ugly",
            "During class or a tutorial, write keywords, diagrams, and timestamps. Do not beautify. Mark anything you did not understand with a question mark. If you type, keep one file per session named with the date and topic.",
            "H2: Layer two — convert within 24 hours",
            "Turn headings into questions: not 'photosynthesis' but 'What inputs does photosynthesis need?' Write the answer from memory, then check. Anything you missed becomes tomorrow's first question. This is retrieval practice, which is boring and effective.",
            "H2: What to throw away",
            "Full transcripts. Highlighted textbooks you never self-test. Ten colors of pens. If a tool takes longer to configure than the session, it is procrastination.",
            "H2: Exam week",
            "You only review the question list, not the original lecture. If a question is easy three times, retire it. If it fails, it stays. That is the whole algorithm.",
         ]),
    dict(cat="education", slug="spaced-repetition-without-an-app", title="Spaced Repetition Without an App",
         desc="A paper box method for remembering facts: five piles, a calendar, and rules for when a card moves.",
         badge="education", cat_href="/education/", cat_label="Education", cat_class="cat-education",
         paras=[
            "Spaced repetition means reviewing a fact just before you would forget it. Apps automate the schedule. A shoebox and index cards do the same job if you follow the rules. This is a Leitner-style box for people who do not want another login.",
            "H2: Five piles",
            "Pile 1 every day, pile 2 every other day, pile 3 twice a week, pile 4 weekly, pile 5 monthly. A card starts in pile 1. If you answer without peeking, it moves up one pile. If you fail, it returns to pile 1. That failure rule is the whole engine.",
            "H2: What belongs on a card",
            "One question, one answer. Not 'everything about World War I.' A definition, a formula, a command, a date with context. Put the source on the back if you will need it.",
            "H2: Time box",
            "Fifteen minutes. Stop when the timer ends even if cards remain. A daily small session beats a weekend cram that you resent.",
            "H2: When an app is better",
            "If you have thousands of cards, travel, or want typing on a phone, software is fine. The method still matters more than the brand. Do not spend a week choosing an app instead of writing twenty cards.",
         ]),
    dict(cat="career", slug="30-60-90-day-plan-template", title="What to Put in a 30-60-90 Day Plan",
         desc="A realistic 30-60-90 template for a new job: learning, relationships, and one visible delivery — without fake metrics.",
         badge="career", cat_href="/career/", cat_label="Career", cat_class="cat-career",
         paras=[
            "Hiring managers ask for a 30-60-90 plan to see if you understand the job is mostly learning at first. A good plan is modest, specific to the team, and honest about what you cannot know yet. This template is that.",
            "H2: Days 1–30 — map the system",
            "LI: Who decides what, in one paragraph|How work gets assigned and reviewed|Where the docs live and which ones are stale|What 'done' means for the team's most common ticket|One small delivery: a bugfix, a doc, a customer reply, with a reviewer",
            "H2: Days 31–60 — own a lane",
            "Pick a recurring responsibility with a name (on-call shadow, weekly report, a component). Ask for feedback in writing once. Do not volunteer for five committees. Depth beats visibility theatre.",
            "H2: Days 61–90 — one improvement",
            "Propose one change you can finish: a checklist, a dashboard query, a onboarding note. Measure with a before/after that a skeptic would accept (time saved, errors avoided), not 'synergy.'",
            "H2: What not to write",
            "Do not promise revenue you do not control. Do not criticize the current team in the interview plan. Do not paste a generic template without replacing the nouns with this company's nouns.",
         ]),
    dict(cat="career", slug="how-to-ask-for-feedback-at-work", title="How to Ask for Feedback at Work",
         desc="Scripts and timing for asking a manager or peer for usable feedback without a performance-review ambush.",
         badge="career", cat_href="/career/", cat_label="Career", cat_class="cat-career",
         paras=[
            "“How am I doing?” is too wide. People answer with politeness. Usable feedback is about a recent piece of work, asked close to the event, with permission to be specific. This page is scripts and timing.",
            "H2: Ask about a thing, not a soul",
            "After a meeting: 'On the pricing slide, what should I cut next time?' After a PR: 'Where did I make the review harder than it needed to be?' After a support ticket: 'Did I miss a policy?' The smaller the target, the more honest the answer.",
            "H2: Give people an easy out",
            "Say you want one thing to change, not a personality report. Offer written or verbal. If they are busy, ask for a 10-minute slot, not a surprise desk ambush on Friday at 5.",
            "H2: Receive without a court defense",
            "Write it down. Repeat the request in your words. Say thanks. Argue later in private if it is factually wrong. Immediate defense trains people never to tell you the truth again.",
            "H2: Close the loop",
            "Two weeks later, mention the change you tried. That is how feedback becomes a working relationship instead of a performance-review surprise.",
         ]),
    dict(cat="business", slug="how-to-price-a-service", title="How to Price a Service When You Are Just Starting",
         desc="A bottom-up pricing method: costs, hours, comparison quotes, and a sentence you can say out loud.",
         badge="business", cat_href="/business/", cat_label="Business", cat_class="cat-business",
         paras=[
            "Underpricing feels kind and usually burns you out. Overpricing without a story loses the first clients. Starting prices should come from costs, hours, and a sentence about who it is for — not from a competitor's homepage. This is a worksheet.",
            "H2: Floor price",
            "Add software, insurance, taxes you must set aside, travel, and a wage you could earn doing something else for those hours. Divide by billable hours, not waking hours. If the number scares you, your offer is too broad or you are still treating this as a hobby — which is a valid choice if you say it out loud.",
            "H2: The sentence",
            "“I help [who] do [job] so they can [outcome], in [format], for [price].” If you cannot say it in one breath, the package is fuzzy. Fuzzy packages get negotiated to zero.",
            "H2: Three packages",
            "A small defined job, a standard job, and a 'you do not want this unless you have a deadline' rush job. People pick the middle more often if the small job is truly small. Do not invent twelve tiers.",
            "H2: Raise with evidence",
            "After three similar jobs, you know the hours. Raise when the calendar is full, not when you feel brave. Put the new price on the next quote; do not surprise a client mid-project.",
         ]),
    dict(cat="business", slug="simple-bookkeeping-for-a-side-project", title="Simple Bookkeeping for a Side Project",
         desc="A minimum bookkeeping setup: separate account, monthly export, and four buckets that keep tax time calmer.",
         badge="business", cat_href="/business/", cat_label="Business", cat_class="cat-business",
         paras=[
            "You do not need enterprise accounting software for a side project that invoices twice a month. You need money separated from rent, a monthly export, and categories a tax preparer will not hate. This is the minimum.",
            "H2: Separate the pipes",
            "Open a separate checking account or at least a sub-account. Receive client payments there. Pay project expenses there. Mixing with groceries is how you lose weekends in April.",
            "H2: Four buckets",
            "Income, cost of delivering the work, overhead (software, phone portion), and tax holdback (a percentage you do not spend). The percentage depends on your jurisdiction; ask a qualified preparer. This site does not file your taxes.",
            "H2: Monthly 30 minutes",
            "Download statements. Match invoices to deposits. Photograph receipts into one folder named by month. If something is personal, mark it. Done.",
            "H2: Invoices",
            "Number them. State due date and late policy. Include how to pay. Send PDF. Follow up once, calmly. Official small-business resources (for U.S. readers, sba.gov) explain registrations; your local rules may differ.",
         ]),
    dict(cat="productivity", slug="weekly-review-that-fits-in-30-minutes", title="How to Run a 30-Minute Weekly Review",
         desc="A Sunday-or-Friday review script: calendar, open loops, one priority, and a shutdown that actually sticks.",
         badge="productivity", cat_href="/productivity/", cat_label="Productivity", cat_class="cat-productivity",
         paras=[
            "A weekly review fails when it tries to be a second brain, a journal, and a life redesign. Thirty minutes can still work if the script is short. This is the script we use internally.",
            "H2: Calendar first",
            "Look at the last seven days and the next seven. Anything that happened but has no next step gets a next step or gets dropped. Anything upcoming without a prep block gets 15 minutes on the calendar now.",
            "H2: Open loops",
            "Scan inbox, notes app, and the pile on the desk. Capture each loop as a verb: email X, pay Y, book Z. Do not organize into twelve tags. One list is enough.",
            "H2: One priority",
            "Circle the single work outcome that would make the week a success if everything else slipped. If you cannot circle one, you do not have priorities; you have anxiety. Put a first action on Monday morning.",
            "H2: Shutdown",
            "Write 'review done' and the date. Close the laptop. The point of a review is to stop carrying the week in your head. If the ritual grows past 30 minutes, cut a step, do not add an app.",
         ]),
    dict(cat="productivity", slug="deep-work-on-a-noisy-schedule", title="Deep Work on a Noisy Schedule",
         desc="How to protect 45 minutes of focus when you have kids, open offices, or chat tools that never sleep.",
         badge="productivity", cat_href="/productivity/", cat_label="Productivity", cat_class="cat-productivity",
         paras=[
            "Deep work advice written for people with offices and nannies does not transfer. If your life is noisy, you need shorter blocks, visible signals, and a definition of 'deep' that fits 45 minutes. This page is for that life.",
            "H2: Redefine deep",
            "Deep means one artifact: a drafted section, a passing test, a decision memo. Not 'be in flow for four hours.' If 45 minutes is what exists between school pickup and dinner, design for 45.",
            "H2: Make the start cheap",
            "Leave the file open to the exact heading. Write the next sentence as a note before you stop. Tomorrow you are not choosing a project; you are continuing a sentence. Starting is the expensive part.",
            "H2: Signals",
            "Headphones, a closed door if you have one, status 'focusing until :45,' phone in another room. Chat will wait 45 minutes more often than you fear. Emergencies already know how to find you.",
            "H2: Noise you cannot remove",
            "Work in slices. Accept that some days the artifact is smaller. Shame is not a strategy. Track blocks completed, not mood.",
         ]),
    dict(cat="travel", slug="estimate-a-trip-budget-in-a-spreadsheet", title="How to Estimate a Trip Budget in a Spreadsheet",
         desc="A column-by-column trip budget: transport, stay, food, activities, buffer, and a rule for when the trip is too expensive.",
         badge="travel", cat_href="/travel/", cat_label="Travel", cat_class="cat-travel",
         paras=[
            "A trip budget is not a vibe. It is rows you can change when a flight jumps $80. This spreadsheet design fits one tab and a phone calculator if you hate software.",
            "H2: Columns",
            "LI: Category (flight, local transport, stay, food, activities, insurance, SIM, gifts, buffer)|Estimate low|Estimate high|Booked actual|Notes with URL and cancellation rule",
            "H2: Food without lying",
            "Use a daily food number you would actually spend, not the hostel kitchen fantasy. Multiply by days. Add two restaurant meals if that is how you travel. Underestimating food is how people tap credit cards on day four.",
            "H2: Buffer",
            "Ten to fifteen percent of the high estimate, sitting in the account, not in your head. If you cannot fund the buffer, the trip is not priced yet. Cut days or stay, not the buffer.",
            "H2: Kill criterion",
            "If the high estimate plus buffer exceeds cash you can spend without skipping rent or an emergency fund, you do not book. You redesign. That sentence is the whole financial skill.",
         ]),
    dict(cat="travel", slug="airport-layover-survival-guide", title="Airport Layover Survival Guide",
         desc="What to do in a short vs long layover: minimum connection, food, sleep, and when leaving the airport is a bad idea.",
         badge="travel", cat_href="/travel/", cat_label="Travel", cat_class="cat-travel",
         paras=[
            "Layovers are either too short (panic) or too long (fluorescent exhaustion). The tactics differ. This guide splits them and ignores influencer tours of cities you cannot legally exit into.",
            "H2: Short connection (under 90 minutes)",
            "Know the terminal change before you land. Do not shop. Use the bathroom on the plane if the queue will be bad. Download the airport map. If your bag is checked through, confirm the tag. If it is not, you do not have a layover; you have a second check-in.",
            "H2: Long layover (4+ hours)",
            "Priority is a chair with an outlet, water, and a meal that will not strand you at a gate far from food. Sleep only if you have an alarm you trust and a grip on your bag. Lounge access is optional; a quiet gate at the far end is free.",
            "H2: Leaving the airport",
            "Only if visa rules allow it, you have more than six hours, and the trip to town is short and cheap. Count two hours of buffer to re-clear security. If that math fails, you stay airside. Official visa information comes from the destination government, not a blog comment.",
            "H2: Health",
            "Walk. Stretch. Do not only sit. Carry a small empty bottle to fill after security. Medication in the carry-on, not the hold.",
         ]),
    dict(cat="lifestyle", slug="declutter-one-room-in-a-weekend", title="How to Declutter One Room in a Weekend",
         desc="A room-sized declutter: keep, leave, donate, trash — with a two-box limit so you finish on Sunday.",
         badge="lifestyle", cat_href="/lifestyle/", cat_label="Lifestyle", cat_class="cat-lifestyle",
         paras=[
            "Whole-home minimalism projects stall because the house is too big. One room in a weekend is finishable. This method uses four labels and a hard stop on Sunday evening.",
            "H2: Define empty",
            "Empty means surfaces you can wipe and a floor you can vacuum, not a magazine photo. Write that definition. If a pile is 'later,' it is still clutter.",
            "H2: Four destinations",
            "Keep (belongs in this room), leave (belongs elsewhere — one box, delivered before Sunday night), donate/sell (leaves the house this week), trash/recycle. No fifth pile called 'unsure' that lives until winter.",
            "H2: Time boxes",
            "Saturday morning: clothes or the worst surface. Saturday afternoon: drawers. Sunday morning: leftover and the leave-box delivery. Sunday afternoon: vacuum and a photo so you remember it worked.",
            "H2: Selling",
            "If an item is not listed by Sunday night, it becomes donate. Selling is optional; finishing the room is not. Minimalism here is a logistics problem, not an identity.",
         ]),
    dict(cat="lifestyle", slug="weeknight-cooking-when-you-are-tired", title="Weeknight Cooking When You Are Tired",
         desc="A default dinner system: five repeat meals, a tiny grocery list, and rules for when takeout is the correct choice.",
         badge="lifestyle", cat_href="/lifestyle/", cat_label="Lifestyle", cat_class="cat-lifestyle",
         paras=[
            "Tired people do not need 30 new recipes. They need five dinners they can cook half-asleep, a grocery list that matches those five, and permission to buy a prepared meal without a guilt lecture. This is a default system.",
            "H2: Pick five",
            "Examples: eggs and toast plus fruit; a frozen vegetable stir-fry with rice; beans and tortillas; pasta with jar sauce and a bag of salad; a tray of roasted whatever-is-in-the-fridge with olive oil. Write your five, not ours. Variety is a weekend hobby.",
            "H2: Grocery as a template",
            "The same cart every week with a swap slot (one protein, one vegetable). If the swap fails, the other four meals still exist. That is resilience.",
            "H2: Mise en place for exhausted humans",
            "Wash the cutting board as soon as you finish. Soak the pan. Future-you is also tired. A clean sink is part of dinner.",
            "H2: Takeout is a tool",
            "If using it twice a week keeps you from skipping meals or fighting, it is working. Nutrition basics still apply (vegetables exist as a side). This is not a diet plan. See our nutrition article for balance, not for purity.",
         ]),
]


def card_html(meta: dict) -> str:
    return f'''
        <article class="card" data-animate>
          <div class="card-img-placeholder {meta["cat_class"]}"></div>
          <div class="card-body">
            <span class="card-category badge-{meta["badge"]}">{meta["cat_label"]}</span>
            <h2 class="card-title"><a href="/{meta["cat"]}/{meta["slug"]}/">{meta["title"]}</a></h2>
            <p class="card-excerpt">{meta["desc"]}</p>
            <div class="card-meta"><span class="card-meta-item"><a href="/about/">InfoNest Editorial</a></span><span class="card-meta-item">August 18, 2026</span><span class="card-meta-item">8 min read</span></div>
          </div>
        </article>
'''


def insert_cards():
    by_cat: dict[str, list] = {}
    for m in NEW:
        by_cat.setdefault(m["cat"], []).append(m)
    for cat, items in by_cat.items():
        index = ROOT / cat / "index.html"
        text = index.read_text(encoding="utf-8")
        text = rewrite_html_text(text)
        cards = "".join(card_html(m) for m in items)
        text = text.replace('      </div>\n    </div>\n  </section>', cards + '      </div>\n    </div>\n  </section>', 1)
        index.write_text(text, encoding="utf-8")


def write_new_articles():
    urls = []
    for m in NEW:
        folder = ROOT / m["cat"] / m["slug"]
        folder.mkdir(parents=True, exist_ok=True)
        html = article_page(m, long_body(m["paras"]))
        (folder / "index.html").write_text(html, encoding="utf-8")
        urls.append(f"https://infonest.page/{m['cat']}/{m['slug']}/")
    return urls


def patch_sitemap(urls: list[str]):
    sm = ROOT / "sitemap.xml"
    text = sm.read_text(encoding="utf-8")
    text = text.replace(
        "https://infonest.page/author/alex-morgan/",
        "https://infonest.page/about/",
    )
    extra = "\n".join(
        f'  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>'
        for u in urls
    )
    text = text.replace("</urlset>", extra + "\n</urlset>")
    sm.write_text(text, encoding="utf-8")


def patch_sitemap_page(urls_meta: list[dict]):
    path = ROOT / "sitemap-page" / "index.html"
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        '<li><a href="/author/alex-morgan/" class="footer-link">Author: Alex Morgan</a></li>',
        "",
    )
    by_cat: dict[str, list] = {}
    for m in urls_meta:
        by_cat.setdefault(m["cat"], []).append(m)
    for cat, items in by_cat.items():
        lis = "".join(
            f'\n            <li><a href="/{m["cat"]}/{m["slug"]}/" class="footer-link">{m["title"]}</a></li>'
            for m in items
        )
        # insert before closing ul of that category if possible
        needle = f'href="/{cat}/"'
        idx = text.find(needle)
        if idx == -1:
            continue
        ul_end = text.find("</ul>", idx)
        text = text[:ul_end] + lis + "\n          " + text[ul_end:]
    path.write_text(text, encoding="utf-8")


def rewrite_all_html():
    for path in ROOT.rglob("*.html"):
        if "tools" in path.parts:
            continue
        if path.as_posix().endswith("author/alex-morgan/index.html"):
            continue
        raw = path.read_text(encoding="utf-8")
        new = rewrite_html_text(raw)
        if new != raw:
            path.write_text(new, encoding="utf-8")


def expand_all():
    for path in ROOT.rglob("*/index.html"):
        rel = path.relative_to(ROOT).as_posix()
        if rel.count("/") < 2:
            continue
        if rel.startswith("author/") or rel.startswith("about/") or rel.startswith("contact/"):
            continue
        if '<div class="article-body">' not in path.read_text(encoding="utf-8"):
            continue
        expand_article(path)


def main():
    rewrite_all_html()
    expand_all()
    urls = write_new_articles()
    insert_cards()
    patch_sitemap(urls)
    patch_sitemap_page(NEW)
    print("new articles", len(urls))
    print("done")


if __name__ == "__main__":
    main()
