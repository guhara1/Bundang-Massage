# 바로GO — 분당 출장마사지·홈타이 안내 사이트

분당구 전지역 방문 관리(출장마사지·홈타이) 안내용 정적 사이트입니다.
예약전화: **0508-202-4719**

## 구조

- 정적 HTML 사이트 — 어느 호스팅(GitHub Pages, Netlify, 일반 웹서버)에서든 그대로 서빙 가능
- `build.py` + `content/` 패키지에서 페이지를 생성하는 빌드 방식
- 생성물(각 디렉터리의 `index.html`, `sitemap.xml`, `robots.txt`)도 저장소에 포함

```
build.py            # 빌드 스크립트 (레이아웃·글자수 검사·sitemap 생성)
content/
  site.py           # 상호·전화·BASE_URL·메뉴 구조
  main.py           # 메인 페이지 (+ LocalBusiness/FAQPage JSON-LD)
  areas.py          # 지역별: 분당구 허브 + 대표 동 9개 (분당·수내·정자·서현·이매·야탑·구미·금곡·궁내)
  areas2.py         # 지역별: 대표 동 9개 (동원·백현·삼평·판교·운중·대장·석운·율·하산운)
  stations.py       # 지하철역별: 허브 + 9개 역 (수인분당선·신분당선·경강선·GTX-A)
  themes.py         # 테마별: 허브 + 14개 테마
  info.py           # 출장마사지 안내·코스·예약·가이드·후기·고객센터·약관
  magazine.py       # 매거진 허브 + 아티클 (Article JSON-LD)
  about.py          # 운영자 소개 (E-E-A-T)
  pricing.py        # 공용 요금 블록
assets/             # CSS, 모바일 내비 JS, 파비콘, OG 이미지
tools/
  charcheck.py      # 모듈 단위 본문 글자수 검사
  make_icons.py     # 파비콘·OG 이미지 생성 (Pillow 필요)
```

## 빌드

```bash
python3 build.py
```

빌드 시 페이지별 본문 글자수 리포트가 출력됩니다.

## SEO 운영 원칙 (빌드에 강제됨)

- 본문 **2,000자 미만 페이지는 자동 `noindex`** 처리되고 sitemap에서 제외
- 지역은 분당구 **법정동 18개 대표 동만** — 숫자 행정동(수내1동, 정자3동 등) 페이지 없음
- 역은 역 1개당 페이지 1개 — 환승역(정자·미금·판교·이매·성남)도 URL 하나, 출구별 페이지 없음
- **지역+역+테마 조합 페이지 없음** (도어웨이 방지) — 테마는 독립 페이지로만 운영
- 상단/하위 메뉴와 푸터에 키워드·지역명·역명 대량 나열 없음
- 모든 페이지 본문은 페이지별 고유 작성 (지역명만 바꾼 복붙 없음)

## 색인 (네이버·구글 빠른 색인)

도메인: **https://bundang-massage.netlify.app** (`content/site.py`의 `BASE_URL`)

빌드 시 자동 생성되는 색인 파일:

- `sitemap.xml` — 색인 59페이지, `lastmod`(매거진은 발행일)·`changefreq`·`priority` 포함
- `rss.xml` — RSS 2.0 피드 (네이버 서치어드바이저 RSS 제출용, 전 페이지 head에 자동탐색 링크)
- `robots.txt` — Sitemap 경로 고지
- `{32자리}.txt` — IndexNow 키 파일 (네이버·빙 즉시 색인 통보용)

배포 직후 실행:

```bash
python3 tools/notify_search.py                      # IndexNow — 네이버·빙·얀덱스 즉시 통보
python3 tools/notify_search.py --google sa.json     # + 구글 Indexing API (서비스 계정 필요)
```

1회 수동 등록:

1. **네이버 서치어드바이저** — 소유확인(메인페이지 메타태그 등록됨) 후
   `요청 > 사이트맵 제출`에 `https://bundang-massage.netlify.app/sitemap.xml`,
   `요청 > RSS 제출`에 `https://bundang-massage.netlify.app/rss.xml` 제출.
   급한 페이지는 `요청 > 웹 페이지 수집`으로 개별 요청
2. **Google Search Console** — 속성 등록 후 `Sitemaps`에 `sitemap.xml` 제출.
   주요 페이지는 `URL 검사 > 색인 생성 요청`. (구글은 IndexNow 미참여,
   사이트맵 핑 엔드포인트는 2023년 폐지되어 lastmod 갱신이 최신성 신호)
3. 구글 Indexing API를 쓰려면 `tools/notify_search.py` 상단 주석의
   서비스 계정 발급·Search Console 소유자 추가 절차 참고
