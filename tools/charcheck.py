#!/usr/bin/env python3
"""단일 콘텐츠 모듈의 본문 글자수 검사.

병렬 작성 중에는 content/__init__.py 가 다른(미완성) 모듈까지 import 하므로,
사이트 공통 모듈(site·pricing)과 검사 대상 모듈만 임시 패키지로 복사해 검사한다.

사용법: python3 tools/charcheck.py content/areas.py
"""
import html
import importlib
import os
import re
import shutil
import sys
import tempfile


def text_length(body_html: str) -> int:
    text = re.sub(r'<section class="pricing">.*?</section>', " ", body_html, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return len(text)


def main():
    target = sys.argv[1]
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    name = os.path.basename(target)[:-3]
    tmp = tempfile.mkdtemp(prefix="charcheck-")
    pkg = os.path.join(tmp, "content")
    os.makedirs(pkg)
    for fname in {"site.py", "pricing.py", os.path.basename(target)}:
        shutil.copy(os.path.join(root, "content", fname), pkg)
    open(os.path.join(pkg, "__init__.py"), "w").close()
    sys.path.insert(0, tmp)
    mod = importlib.import_module(f"content.{name}")

    pages = list(getattr(mod, "PAGES", []) or [])
    if hasattr(mod, "PAGE"):
        pages.append(mod.PAGE)

    bad = 0
    for p in pages:
        n = text_length(p["body"])
        if p.get("noindex"):
            status = "noindex"
        elif 2000 <= n <= 2500:
            status = "OK"
        else:
            status = "OUT-OF-RANGE"
            bad += 1
        print(f"{(p['path'] or '/').ljust(42)} {str(n).rjust(5)}  {status}")
    shutil.rmtree(tmp, ignore_errors=True)
    print(f"\n{len(pages)} pages, {bad} out of range (index 대상은 2,000~2,500자 필수)")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
