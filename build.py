#!/usr/bin/env python3
"""바로GO — 분당 출장마사지·홈타이 정적 사이트 빌드 스크립트.

content/ 패키지의 페이지 정의를 읽어 정적 HTML을 생성한다.

규칙(자동 적용):
  - 본문 텍스트 2,000자 미만 페이지는 robots noindex 처리
  - sitemap.xml 에는 index 허용 페이지만 포함
  - 지역+역+테마 조합 경로는 생성 자체가 불가능한 구조
"""
import datetime
import html
import json
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from content import PAGES
from content.site import (BASE_URL, BRAND, BRAND_MARK, NAV, PHONE, PHONE_DISPLAY)
from content import reviews_data

ROOT = os.path.dirname(os.path.abspath(__file__))
MIN_INDEX_CHARS = 2000
BASE = BASE_URL.rstrip("/")
OPENING_HOURS = "Mo-Su 00:00-24:00"
PRICE_RANGE = "₩90,000 - ₩180,000"
AREA_PROVINCE = "경기도 성남시 분당구"

# 후기·평점 구조화 데이터를 함께 출력하는 페이지 유형
REVIEW_KINDS = {
    "home", "reviews", "area_hub", "area", "station_hub", "station",
    "theme_hub", "theme", "service_hub", "courses",
}


def page_kind(path: str) -> str:
    if path == "":
        return "home"
    if path == "reviews/":
        return "reviews"
    if path == "bundang/":
        return "area_hub"
    if path == "bundang/stations/":
        return "station_hub"
    if path.startswith("bundang/stations/"):
        return "station"
    if path.startswith("bundang/"):
        return "area"
    if path == "themes/":
        return "theme_hub"
    if path.startswith("themes/"):
        return "theme"
    if path == "massage/":
        return "service_hub"
    if path == "courses/":
        return "courses"
    return "other"


def reviews_for(kind: str, path: str):
    """페이지 유형에 맞는 후기 묶음 — 노출 HTML과 JSON-LD가 같은 묶음을 공유한다."""
    if kind == "reviews":
        return list(reviews_data.REVIEWS)
    sub = []
    parts = path.split("/")
    if kind == "area":
        sub = reviews_data.for_area(parts[1])
    elif kind == "station":
        sub = reviews_data.for_station(parts[2])
    elif kind == "theme":
        sub = reviews_data.for_theme(parts[1])
    return (sub or list(reviews_data.REVIEWS))[:3]


def _stars(n: int) -> str:
    return "★" * n + "☆" * (5 - n)


def render_reviews(subset, kind: str) -> str:
    agg = reviews_data.aggregate()
    score = agg["ratingValue"]
    summary = (
        '<div class="review-summary">'
        f'<span class="review-score">{score}</span>'
        f'<span class="review-stars review-stars-lg" aria-hidden="true">{_stars(round(float(score)))}</span>'
        f'<span class="review-count">이용자 평점 {score} / 5 · 후기 {agg["reviewCount"]}건</span>'
        "</div>"
    )
    cards = []
    for r in subset:
        cards.append(
            '<li class="review-card">'
            '<div class="review-head">'
            f'<span class="review-stars" aria-label="별점 {r["rating"]}점">{_stars(r["rating"])}</span>'
            f'<span class="review-name">{r["name"]}</span>'
            "</div>"
            f'<p class="review-body">{r["body"]}</p>'
            '<p class="review-meta">'
            f'<span>{r["area"]}</span><span>{r["theme"]}</span>'
            f'<time datetime="{r["date"]}">{r["date"].replace("-", ". ")}</time>'
            "</p>"
            "</li>"
        )
    more = (
        ""
        if kind == "reviews"
        else '<p class="review-more"><a href="/reviews/">전체 이용 후기 보기 →</a></p>'
    )
    return (
        '<section id="reviews-block" class="reviews-block">'
        "<h2>이용 후기</h2>"
        f"{summary}"
        f'<ul class="review-list">{"".join(cards)}</ul>'
        f"{more}"
        "</section>\n"
    )


def _plain(s: str) -> str:
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    return re.sub(r"\s+", " ", s).strip()


def _ld(obj) -> str:
    return (
        '<script type="application/ld+json">\n'
        + json.dumps(obj, ensure_ascii=False, indent=2)
        + "\n</script>\n"
    )


def _breadcrumb_obj(page, canonical):
    crumbs = page.get("breadcrumb") or []
    if not crumbs:
        return None
    items = [{"@type": "ListItem", "position": 1, "name": "홈", "item": BASE + "/"}]
    for i, (label, href) in enumerate(crumbs, start=2):
        items.append({
            "@type": "ListItem", "position": i, "name": label,
            "item": (BASE + href) if href else canonical,
        })
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}


def _faq_obj(body):
    pairs = re.findall(
        r'<div class="faq-item">\s*<h3>(.*?)</h3>\s*<p>(.*?)</p>', body, flags=re.S
    )
    if not pairs:
        return None
    ent = [
        {"@type": "Question", "name": _plain(q),
         "acceptedAnswer": {"@type": "Answer", "text": _plain(a)}}
        for q, a in pairs
    ]
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": ent}


def _agg_obj():
    agg = reviews_data.aggregate()
    return {
        "@type": "AggregateRating",
        "ratingValue": agg["ratingValue"],
        "reviewCount": agg["reviewCount"],
        "bestRating": "5",
        "worstRating": "1",
    }


def _review_objs(subset):
    out = []
    for r in subset:
        out.append({
            "@type": "Review",
            "author": {"@type": "Person", "name": r["name"]},
            "datePublished": r["date"],
            "reviewRating": {
                "@type": "Rating", "ratingValue": str(r["rating"]),
                "bestRating": "5", "worstRating": "1",
            },
            "reviewBody": r["body"],
        })
    return out


def _business_obj(page, kind, canonical, subset):
    crumbs = page.get("breadcrumb") or []
    label = crumbs[-1][0] if crumbs else ""
    if kind in ("theme", "theme_hub"):
        obj = {
            "@context": "https://schema.org",
            "@type": "Service",
            "serviceType": (f"{label} 출장마사지·홈타이" if kind == "theme" and label
                            else "분당 출장마사지·홈타이"),
            "name": (f"{label} 방문 관리" if kind == "theme" and label else "분당 방문 관리"),
            "provider": {
                "@type": "HealthAndBeautyBusiness", "name": BRAND,
                "telephone": PHONE, "url": BASE + "/",
            },
            "areaServed": {"@type": "AdministrativeArea", "name": AREA_PROVINCE},
            "url": canonical,
        }
    else:
        name = BRAND
        if kind in ("area", "station") and label:
            name = f"{BRAND} — {label} 방문 관리"
        served = AREA_PROVINCE
        if kind == "area" and label:
            served = f"{AREA_PROVINCE} {label}"
        obj = {
            "@context": "https://schema.org",
            "@type": "HealthAndBeautyBusiness",
            "name": name,
            "telephone": PHONE,
            "url": canonical,
            "image": BASE + "/assets/og-image.png",
            "description": page.get("desc", ""),
            "areaServed": {"@type": "AdministrativeArea", "name": served},
            "openingHours": OPENING_HOURS,
            "priceRange": PRICE_RANGE,
        }
    obj["aggregateRating"] = _agg_obj()
    obj["review"] = _review_objs(subset)
    return obj


def build_schema(page, kind, canonical, body, subset):
    blocks = []
    bc = _breadcrumb_obj(page, canonical)
    if bc:
        blocks.append(bc)
    faq = _faq_obj(body)
    if faq:
        blocks.append(faq)
    if kind in REVIEW_KINDS:
        blocks.append(_business_obj(page, kind, canonical, subset))
    if kind == "home":
        blocks.append({
            "@context": "https://schema.org", "@type": "WebSite",
            "name": BRAND, "url": BASE + "/",
        })
        blocks.append({
            "@context": "https://schema.org", "@type": "Organization",
            "name": BRAND, "url": BASE + "/",
            "logo": BASE + "/assets/icon-512.png",
            "telephone": PHONE,
        })
    return "".join(_ld(b) for b in blocks)


def text_length(body_html: str) -> int:
    """태그를 제거한 본문 글자수(공백 포함, 연속 공백은 1자).
    공통 요금 블록은 페이지 고유 본문이 아니므로 측정에서 제외한다."""
    text = re.sub(r'<section class="pricing">.*?</section>', " ", body_html, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return len(text)


def render_nav(current_path: str) -> str:
    items = []
    for label, href, children in NAV:
        active = " is-active" if href == "/" + current_path else ""
        if children:
            sub = "".join(
                f'<li><a href="{c_href}">{c_label}</a></li>'
                for c_label, c_href in children
            )
            items.append(
                f'<li class="nav-item has-sub{active}">'
                f'<a href="{href}">{label}</a>'
                f'<ul class="sub-menu">{sub}</ul></li>'
            )
        else:
            items.append(
                f'<li class="nav-item{active}"><a href="{href}">{label}</a></li>'
            )
    return "".join(items)


def render_breadcrumb(crumbs) -> str:
    if not crumbs:
        return ""
    parts = ['<nav class="breadcrumb" aria-label="현재 위치"><ol>']
    parts.append('<li><a href="/">홈</a></li>')
    for label, href in crumbs:
        if href:
            parts.append(f'<li><a href="{href}">{label}</a></li>')
        else:
            parts.append(f"<li><span>{label}</span></li>")
    parts.append("</ol></nav>")
    return "".join(parts)


def inject_toc(body: str):
    """본문 섹션(h2)에 id를 보장하고 좌측 목차 데이터를 만든다."""
    items = []
    counter = [0]

    def repl(m):
        attrs, title = m.group(1), m.group(2)
        idm = re.search(r'id="([^"]+)"', attrs)
        if idm:
            sid = idm.group(1)
            opening = f"<section{attrs}>"
        else:
            counter[0] += 1
            sid = f"sec-{counter[0]}"
            opening = f'<section id="{sid}"{attrs}>'
        label = re.sub(r"<[^>]+>", "", title).strip()
        items.append((sid, label))
        return f"{opening}<h2>{title}</h2>"

    body = re.sub(r"<section([^>]*)>\s*<h2>(.*?)</h2>", repl, body, flags=re.S)
    return body, items


def render_toc(items) -> str:
    if len(items) < 3:
        return ""
    links = "".join(
        f'<li><a href="#{sid}">{label}</a></li>' for sid, label in items
    )
    return (
        '<aside class="page-toc"><nav aria-label="페이지 목차">'
        '<p class="toc-title">목차</p>'
        f"<ul>{links}</ul></nav></aside>"
    )


def render_page(page: dict) -> str:
    path = page["path"]
    title = page["title"]
    desc = page["desc"]
    h1 = page["h1"]
    body = page["body"]
    crumbs = page.get("breadcrumb") or []
    extra_head = page.get("extra_head", "")
    hero = page.get("hero", "")

    chars = text_length(body)
    noindex = page.get("noindex", False) or chars < MIN_INDEX_CHARS
    robots = (
        '<meta name="robots" content="noindex,follow">'
        if noindex
        else '<meta name="robots" content="index,follow">'
    )
    canonical = BASE_URL.rstrip("/") + "/" + path

    # 구조화 데이터(JSON-LD)와 노출 후기는 같은 후기 묶음을 공유한다.
    kind = page_kind(path)
    subset = reviews_for(kind, path) if kind in REVIEW_KINDS else []
    schema_html = build_schema(page, kind, canonical, body, subset)

    # 평점·후기 블록을 예약 CTA 바로 앞에 끼워 넣는다(후기 노출 = 평점 스키마 근거).
    if subset:
        rv = render_reviews(subset, kind)
        for marker in ('<section id="contact" class="cta">', '<section class="cta">'):
            if marker in body:
                body = body.replace(marker, rv + marker, 1)
                break
        else:
            body += rv

    # 히어로가 있는 페이지(메인)는 H1을 히어로 안에서 출력한다.
    if hero:
        page_head = hero
    else:
        page_head = ""

    h1_html = "" if hero else f"<h1>{h1}</h1>"

    body, toc_items = inject_toc(body)
    toc_html = render_toc(toc_items)
    layout_cls = "page-layout has-toc" if toc_html else "page-layout"

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
{robots}
<link rel="canonical" href="{canonical}">
<link rel="alternate" type="application/rss+xml" title="{BRAND} RSS" href="{BASE_URL.rstrip('/')}/rss.xml">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:image" content="{BASE_URL.rstrip('/')}/assets/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{BASE_URL.rstrip('/')}/assets/og-image.png">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<meta name="theme-color" content="#0a1120">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&family=Noto+Serif+KR:wght@600;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/style.css">
{extra_head}{schema_html}</head>
<body>
<header class="site-header">
  <div class="header-accent" aria-hidden="true"></div>
  <div class="header-top">
    <div class="header-inner">
      <a class="brand" href="/"><span class="brand-mark">{BRAND_MARK}</span> <span class="brand-text">{BRAND}</span></a>
      <p class="header-tagline"><span class="tag-gem">◆</span> 분당구 전지역 방문 관리 <span class="tag-gem">◆</span> 24시간 상담</p>
      <a class="header-call" href="tel:{PHONE}"><span class="call-label">예약전화</span> {PHONE_DISPLAY}</a>
      <button class="nav-toggle" aria-label="메뉴 열기" aria-expanded="false"><span></span><span></span><span></span></button>
    </div>
  </div>
  <nav class="main-nav" aria-label="주 메뉴">
    <div class="nav-inner"><ul class="nav-list">{render_nav(path)}</ul></div>
  </nav>
</header>
{page_head}<main class="site-main">
  <div class="container {layout_cls}">
    {toc_html}
    <article class="page-content">
      {render_breadcrumb(crumbs)}
      {h1_html}
      {body}
    </article>
  </div>
</main>
<footer class="site-footer">
  <div class="container footer-grid">
    <div class="footer-col footer-about">
      <p class="footer-brand">{BRAND}</p>
      <p class="footer-desc">분당구 전지역 방문 출장마사지·홈타이 안내 사이트입니다. 모든 서비스는 안내된 관리 범위와 위생·안전 기준 안에서만 제공됩니다.</p>
      <address class="footer-contact">
        <span class="footer-contact-row"><span class="footer-label">예약전화</span> <a href="tel:{PHONE}">{PHONE_DISPLAY}</a></span>
        <span class="footer-contact-row"><span class="footer-label">상담시간</span> 연중무휴 24시간</span>
        <span class="footer-contact-row"><span class="footer-label">서비스 지역</span> 경기도 성남시 분당구 전지역</span>
      </address>
    </div>
    <nav class="footer-col" aria-label="서비스 안내">
      <p class="footer-title">서비스</p>
      <ul>
        <li><a href="/massage/">분당 출장마사지</a></li>
        <li><a href="/bundang/">지역별 안내</a></li>
        <li><a href="/bundang/stations/">지하철역별 안내</a></li>
        <li><a href="/themes/">테마별 안내</a></li>
        <li><a href="/courses/">코스안내</a></li>
      </ul>
    </nav>
    <nav class="footer-col" aria-label="이용 안내">
      <p class="footer-title">이용 안내</p>
      <ul>
        <li><a href="/reservation/">예약안내</a></li>
        <li><a href="/guide/">이용가이드</a></li>
        <li><a href="/reviews/">이용 후기</a></li>
        <li><a href="/support/">고객센터</a></li>
        <li><a href="/support/#faq">자주 묻는 질문</a></li>
      </ul>
    </nav>
    <nav class="footer-col" aria-label="정책 및 기준">
      <p class="footer-title">정책</p>
      <ul>
        <li><a href="/about/">운영자 소개</a></li>
        <li><a href="/support/privacy/">개인정보처리방침</a></li>
        <li><a href="/support/terms/">이용약관</a></li>
        <li><a href="/guide/#hygiene">위생·안전 기준</a></li>
        <li><a href="/guide/#prohibited">금지행위 안내</a></li>
        <li><a href="/support/#biz">제휴·기업 문의</a></li>
      </ul>
    </nav>
  </div>
  <div class="footer-bottom">
    <div class="container footer-bottom-inner">
      <p class="footer-copy">&copy; {BRAND}. All rights reserved.</p>
      <p class="footer-note">건전한 방문 관리 서비스를 운영하며, 불법적인 요청은 어떤 경우에도 응하지 않습니다.</p>
      <a class="footer-made" href="https://t.me/googleseolab" target="_blank" rel="noopener nofollow">웹사이트 제작문의 ↗</a>
    </div>
  </div>
</footer>
<a class="call-fab" href="tel:{PHONE}" aria-label="전화 예약 {PHONE_DISPLAY}">
  <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg>
  <span class="call-fab-label">예약 전화</span>
</a>
<script src="/assets/nav.js"></script>
</body>
</html>
"""


def _page_priority(path: str) -> str:
    """URL 깊이 기준 우선순위 — 메인 1.0, 허브 0.8, 상세 0.6."""
    if path == "":
        return "1.0"
    if path in ("bundang/", "bundang/stations/", "themes/", "massage/", "magazine/"):
        return "0.8"
    return "0.6"


def _rfc822(date_str: str) -> str:
    """YYYY-MM-DD → RFC 822 (RSS pubDate). KST 기준."""
    d = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    return d.strftime("%a, %d %b %Y 09:00:00 +0900")


def build() -> None:
    report = []
    sitemap_entries = []  # (url, lastmod, priority)
    rss_items = []        # (url, title, desc, date)
    today = datetime.date.today().isoformat()

    for page in PAGES:
        path = page["path"]  # "" 또는 "bundang/jeongja-dong/" 형태
        out_dir = os.path.join(ROOT, path)
        os.makedirs(out_dir, exist_ok=True)
        html_out = render_page(page)
        with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(html_out)

        chars = text_length(page["body"])
        noindex = page.get("noindex", False) or chars < MIN_INDEX_CHARS
        if not noindex:
            url = BASE_URL.rstrip("/") + "/" + path
            lastmod = page.get("date", today)
            sitemap_entries.append((url, lastmod, _page_priority(path)))
            rss_items.append((url, page["title"], page["desc"], lastmod))
        report.append((path or "/", chars, "noindex" if noindex else "index"))

    # sitemap.xml — lastmod·priority 포함 (네이버·구글 색인 최신성 신호)
    urls = "\n".join(
        "  <url>"
        f"<loc>{html.escape(u)}</loc>"
        f"<lastmod>{lm}</lastmod>"
        f"<changefreq>{'daily' if pr in ('1.0', '0.8') else 'weekly'}</changefreq>"
        f"<priority>{pr}</priority>"
        "</url>"
        for u, lm, pr in sitemap_entries
    )
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            f"{urls}\n</urlset>\n"
        )

    # rss.xml — 네이버 서치어드바이저 RSS 제출용 (매거진 글은 발행일, 그 외는 빌드일)
    base = BASE_URL.rstrip("/")
    rss_items.sort(key=lambda it: it[3], reverse=True)
    items = "\n".join(
        "    <item>\n"
        f"      <title>{html.escape(title)}</title>\n"
        f"      <link>{html.escape(url)}</link>\n"
        f"      <guid isPermaLink=\"true\">{html.escape(url)}</guid>\n"
        f"      <description>{html.escape(desc)}</description>\n"
        f"      <pubDate>{_rfc822(date)}</pubDate>\n"
        "    </item>"
        for url, title, desc, date in rss_items
    )
    with open(os.path.join(ROOT, "rss.xml"), "w", encoding="utf-8") as f:
        f.write(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n'
            "  <channel>\n"
            f"    <title>{html.escape(BRAND)} — 분당 출장마사지·홈타이 안내</title>\n"
            f"    <link>{base}/</link>\n"
            "    <description>분당구 전지역 방문 관리(출장마사지·홈타이) 안내와 지역·역세권·테마별 가이드, 매거진 콘텐츠를 제공합니다.</description>\n"
            "    <language>ko</language>\n"
            f"    <lastBuildDate>{_rfc822(today)}</lastBuildDate>\n"
            f'    <atom:link href="{base}/rss.xml" rel="self" type="application/rss+xml" />\n'
            f"{items}\n"
            "  </channel>\n"
            "</rss>\n"
        )

    # robots.txt
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(
            "User-agent: *\nAllow: /\n\n"
            f"Sitemap: {BASE_URL.rstrip('/')}/sitemap.xml\n"
        )

    # .nojekyll (GitHub Pages)
    open(os.path.join(ROOT, ".nojekyll"), "w").close()

    width = max(len(p) for p, _, _ in report)
    print(f"{'PATH'.ljust(width)}  CHARS  ROBOTS")
    for p, c, r in sorted(report):
        flag = "" if (r == "noindex" or MIN_INDEX_CHARS <= c <= 2500) else "  ⚠"
        print(f"{p.ljust(width)}  {str(c).rjust(5)}  {r}{flag}")
    print(f"\n{len(report)} pages built, {len(sitemap_entries)} in sitemap.")


if __name__ == "__main__":
    build()
