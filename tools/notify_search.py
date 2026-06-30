#!/usr/bin/env python3
"""검색엔진 색인 통보 자동화 — 배포 직후 실행하면 색인 속도를 크게 높여준다.

하는 일
  1. IndexNow  — 색인 대상 전체 URL을 일괄 제출. 네이버·빙·얀덱스가 즉시 수신
                 (네이버는 2022년부터 IndexNow 공식 참여). 키 파일은 사이트
                 루트의 {KEY}.txt 로 이미 배포되어 있어야 한다.
  2. 구글 Indexing API — 서비스 계정 JSON이 있으면 URL_UPDATED 통보.
                 (구글은 IndexNow 미참여. 공식적으로는 구인공고·라이브방송
                 페이지 대상 API이므로, 일반 페이지는 Search Console
                 사이트맵 제출 + URL 검사 '색인 생성 요청'이 정석이다.)
  3. 사이트맵 핑 — 구글·빙의 GET 핑 엔드포인트는 2023년 폐지되어 호출하지
                 않는다. 대신 sitemap.xml lastmod 갱신 + IndexNow 로 대체.

사용법
  python3 tools/notify_search.py                     # IndexNow 만
  python3 tools/notify_search.py --google sa.json    # + 구글 Indexing API
  python3 tools/notify_search.py --urls https://... # 특정 URL만 통보

구글 Indexing API 사전 준비 (1회)
  1. Google Cloud 콘솔에서 프로젝트 생성 → "Web Search Indexing API" 사용 설정
  2. 서비스 계정 생성 → JSON 키 다운로드
  3. Search Console 속성(bundang-massage.netlify.app)에 서비스 계정 이메일을
     '소유자'로 추가
  의존성: pip install google-auth requests
"""
import argparse
import glob
import json
import os
import re
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from content.site import BASE_URL  # noqa: E402

HOST = BASE_URL.split("//", 1)[1].rstrip("/")
INDEXNOW_ENDPOINT = "https://api.indexnow.org/indexnow"  # 모든 참여 엔진에 전파됨
GOOGLE_ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"


def find_key() -> str:
    for path in glob.glob(os.path.join(ROOT, "*.txt")):
        name = os.path.basename(path)[:-4]
        if re.fullmatch(r"[0-9a-f]{32}", name):
            return name
    sys.exit("IndexNow 키 파일({32자리 hex}.txt)이 사이트 루트에 없습니다.")


def sitemap_urls() -> list:
    src = open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()
    return re.findall(r"<loc>(.*?)</loc>", src)


def ping_indexnow(urls: list) -> None:
    key = find_key()
    payload = json.dumps({
        "host": HOST,
        "key": key,
        "keyLocation": f"{BASE_URL.rstrip('/')}/{key}.txt",
        "urlList": urls,
    }).encode()
    req = urllib.request.Request(
        INDEXNOW_ENDPOINT, data=payload,
        headers={"Content-Type": "application/json; charset=utf-8"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as res:
            print(f"IndexNow: HTTP {res.status} — {len(urls)}개 URL 제출 완료"
                  " (네이버·빙·얀덱스 전파)")
    except Exception as e:  # noqa: BLE001
        print(f"IndexNow 실패: {e}")


def ping_google(urls: list, sa_json: str) -> None:
    try:
        import requests
        from google.auth.transport.requests import AuthorizedSession
        from google.oauth2 import service_account
    except ImportError:
        sys.exit("pip install google-auth requests 후 다시 실행하세요.")
    creds = service_account.Credentials.from_service_account_file(
        sa_json, scopes=["https://www.googleapis.com/auth/indexing"])
    session = AuthorizedSession(creds)
    ok = fail = 0
    for url in urls:
        res = session.post(GOOGLE_ENDPOINT,
                           json={"url": url, "type": "URL_UPDATED"})
        if res.status_code == 200:
            ok += 1
        else:
            fail += 1
            print(f"  구글 거절({res.status_code}): {url} — {res.text[:120]}")
    print(f"구글 Indexing API: 성공 {ok} / 실패 {fail}"
          " (일일 기본 할당량 200건 주의)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--google", metavar="SA_JSON",
                    help="구글 서비스 계정 JSON 경로 (Indexing API 통보)")
    ap.add_argument("--urls", nargs="*",
                    help="특정 URL만 통보 (기본: sitemap.xml 전체)")
    args = ap.parse_args()

    urls = args.urls or sitemap_urls()
    print(f"대상 URL {len(urls)}개 (host: {HOST})")
    ping_indexnow(urls)
    if args.google:
        ping_google(urls, args.google)


if __name__ == "__main__":
    main()
