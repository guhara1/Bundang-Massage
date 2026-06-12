# 메인 페이지 — 분당 허브. 키워드를 한곳에 몰지 않고 지역·역·테마 상세 페이지로 연결한다.
from .site import BASE_URL, BRAND, PHONE, PHONE_DISPLAY
from .pricing import PRICING

_JSONLD = f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "HealthAndBeautyBusiness",
  "name": "{BRAND}",
  "telephone": "{PHONE}",
  "url": "{BASE_URL}/",
  "image": "{BASE_URL}/assets/og-image.png",
  "description": "분당구 전지역 방문 출장마사지·홈타이 예약 안내",
  "areaServed": {{
    "@type": "AdministrativeArea",
    "name": "경기도 성남시 분당구"
  }},
  "openingHours": "Mo-Su 00:00-24:00",
  "priceRange": "₩90,000 - ₩180,000"
}}
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {{
      "@type": "Question",
      "name": "분당구 전지역 방문이 가능한가요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "정자동, 서현동, 야탑동부터 판교 일대와 율동 같은 외곽까지 18개 법정동 기준으로 안내하며, 실제 가능 여부는 예약 시간과 위치에 따라 상담에서 확정됩니다."
      }}
    }},
    {{
      "@type": "Question",
      "name": "서현역이나 판교역 근처 숙소도 가능한가요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "주요 역세권 9곳은 역 상세 페이지에서 안내합니다. 역 이름과 건물명을 알려주시면 가능 여부를 바로 확인해 드립니다."
      }}
    }},
    {{
      "@type": "Question",
      "name": "수내1동 같은 행정동 페이지는 왜 없나요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "숫자 행정동은 같은 생활권을 나눈 단위라서 수내동, 정자동 등 법정동 대표 페이지에서 통합해 안내합니다."
      }}
    }},
    {{
      "@type": "Question",
      "name": "당일 예약도 가능한가요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "배정 여유가 있으면 진행됩니다. 저녁과 주말에는 문의가 몰리니 한두 시간 이상 여유를 두시길 권장합니다."
      }}
    }},
    {{
      "@type": "Question",
      "name": "테마는 어떻게 고르면 되나요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "테마별 안내에서 14개 테마의 특징과 추천 대상을 비교할 수 있고, 고르기 어려우면 전화로 컨디션을 말씀해 주세요."
      }}
    }}
  ]
}}
</script>
"""

_HERO = f"""<section class="hero">
  <div class="hero-inner">
    <p class="hero-badge">PREMIUM VISITING SPA · 분당구 전지역</p>
    <h1>분당 출장마사지·홈타이<br>예약 안내</h1>
    <p class="hero-lead">정자동에서 판교까지, 계신 곳으로 찾아가는 프리미엄 방문 관리.<br>자택·오피스텔·숙소 어디든 전화 한 통으로 예약이 마무리됩니다.</p>
    <div class="hero-actions">
      <a class="hero-btn primary" href="tel:{PHONE}">📞 {PHONE_DISPLAY}</a>
      <a class="hero-btn" href="/courses/">코스 안내 보기</a>
    </div>
    <ul class="hero-stats">
      <li><strong>18개</strong><span>대표 지역</span></li>
      <li><strong>9개</strong><span>역세권 안내</span></li>
      <li><strong>14개</strong><span>관리 테마</span></li>
      <li><strong>24시간</strong><span>예약 상담</span></li>
    </ul>
  </div>
</section>
"""

_BODY = f"""
<section id="service">
<h2>분당 출장마사지·홈타이 서비스 안내</h2>
<p>이 페이지는 성남시 분당구에서 방문 마사지와 홈타이를 찾는 분들을 위한 허브입니다. 어느 동까지 방문이 되는지, 역세권 숙소나 오피스텔은 어떻게 안내되는지, 코스와 테마는 무엇을 기준으로 고르는지를 한눈에 정리하고, 자세한 내용은 하위 페이지로 연결해 드립니다. {BRAND}는 전화 상담으로 위치와 시간을 확인한 뒤 방문을 확정하는 절차를 지키므로 처음 이용하셔도 어렵지 않습니다.</p>
</section>

<section id="coverage">
<h2>분당구 전지역 방문 가능 안내</h2>
<p>분당구는 1기 신도시로 계획된 수내·서현·정자 일대와 그 뒤 조성된 판교신도시, 율동·석운동 같은 외곽 권역이 함께 있는 지역입니다. 지역 안내는 법정동 18개를 대표 페이지로 운영하며, 수내1동이나 정자1동처럼 숫자로 나뉜 행정동은 별도 페이지 없이 해당 법정동 페이지에서 통합해 설명합니다. 같은 생활권을 쪼개 비슷한 글을 반복하기보다 동 단위로 묶어 안내하는 편이 정확하기 때문입니다.</p>
</section>

<section id="areas">
<h2>지역별 안내</h2>
<p>탄천을 따라 늘어선 신도시 중심부, 판교테크노밸리 일대, 구미동·금곡동 같은 남부 주거권까지 동마다 생활권 성격이 다릅니다. 각 페이지에서 해당 동의 특징, 가까운 역, 방문 형태, 예약 팁을 고유한 내용으로 다루니 거주하시거나 머무시는 동을 골라 주세요.</p>
<ul class="card-grid">
<li><a href="/bundang/bundang-dong/">분당동</a></li>
<li><a href="/bundang/sunae-dong/">수내동</a></li>
<li><a href="/bundang/jeongja-dong/">정자동</a></li>
<li><a href="/bundang/seohyeon-dong/">서현동</a></li>
<li><a href="/bundang/imae-dong/">이매동</a></li>
<li><a href="/bundang/yatap-dong/">야탑동</a></li>
<li><a href="/bundang/gumi-dong/">구미동</a></li>
<li><a href="/bundang/geumgok-dong/">금곡동</a></li>
<li><a href="/bundang/gungnae-dong/">궁내동</a></li>
<li><a href="/bundang/dongwon-dong/">동원동</a></li>
<li><a href="/bundang/baekhyeon-dong/">백현동</a></li>
<li><a href="/bundang/sampyeong-dong/">삼평동</a></li>
<li><a href="/bundang/pangyo-dong/">판교동</a></li>
<li><a href="/bundang/unjung-dong/">운중동</a></li>
<li><a href="/bundang/daejang-dong/">대장동</a></li>
<li><a href="/bundang/seogun-dong/">석운동</a></li>
<li><a href="/bundang/yul-dong/">율동</a></li>
<li><a href="/bundang/hasanun-dong/">하산운동</a></li>
</ul>
<p>분당구 전체 구조는 <a href="/bundang/">지역 전체 안내</a>에서 한 번에 볼 수 있습니다.</p>
</section>

<section id="stations">
<h2>지하철역 인근 안내</h2>
<p>분당구는 수인분당선과 신분당선이 남북으로 지나고, 판교역에는 경강선, 성남역에는 GTX-A가 더해진 지역입니다. 역 안내는 아홉 개 주요 역 기준이며, 두 노선이 만나는 환승역도 페이지는 하나만 운영합니다. 출구별 페이지는 만들지 않고, 정확한 위치는 예약 통화에서 건물 기준으로 확인합니다.</p>
<ul class="card-grid">
<li><a href="/bundang/stations/yatap-station/">야탑역</a></li>
<li><a href="/bundang/stations/imae-station/">이매역</a></li>
<li><a href="/bundang/stations/seohyeon-station/">서현역</a></li>
<li><a href="/bundang/stations/sunae-station/">수내역</a></li>
<li><a href="/bundang/stations/jeongja-station/">정자역</a></li>
<li><a href="/bundang/stations/migeum-station/">미금역</a></li>
<li><a href="/bundang/stations/ori-station/">오리역</a></li>
<li><a href="/bundang/stations/pangyo-station/">판교역</a></li>
<li><a href="/bundang/stations/seongnam-station/">성남역</a></li>
</ul>
</section>

<section id="themes">
<h2>테마별 관리 안내</h2>
<p>관리 테마는 14개 독립 페이지에서 기법의 특징과 추천 대상, 받기 전 확인사항을 설명합니다. 동이나 역과 테마를 묶은 조합 페이지는 운영하지 않는데, 어느 위치든 같은 테마라면 진행 방식이 같아 내용만 중복되기 때문입니다. 테마를 먼저 정하고 위치는 예약 시 알려주시면 충분합니다.</p>
<ul class="card-grid">
<li><a href="/themes/swedish/">스웨디시</a></li>
<li><a href="/themes/lomilomi/">로미로미</a></li>
<li><a href="/themes/thai/">타이마사지</a></li>
<li><a href="/themes/chinese/">중국마사지</a></li>
<li><a href="/themes/aroma/">아로마테라피</a></li>
<li><a href="/themes/homecare/">홈케어</a></li>
<li><a href="/themes/hotel-style/">호텔식마사지</a></li>
<li><a href="/themes/foot/">발마사지</a></li>
<li><a href="/themes/sports/">스포츠·경락</a></li>
<li><a href="/themes/skincare/">스킨케어</a></li>
<li><a href="/themes/waxing/">왁싱</a></li>
<li><a href="/themes/couple/">커플 관리</a></li>
<li><a href="/themes/24hours/">24시간</a></li>
<li><a href="/themes/overnight/">수면 가능</a></li>
</ul>
</section>

<section id="course">
<h2>코스 선택 안내</h2>
<p>코스는 60분, 90분, 120분 중 그날의 목적과 컨디션에 맞춰 고르시면 됩니다. 야근이 이어진 뒤의 짧은 회복, 주말 휴식을 겸한 여유 있는 관리, 탄천 러닝이나 운동 뒤 근육 이완, 커플 일정 등 상황별 기준은 <a href="/courses/">코스안내</a>에서 다룹니다. 애매하면 전화에서 상태를 말씀해 주세요.</p>
</section>

<section id="how">
<h2>예약 진행 방식</h2>
<p>예약은 다섯 단계로 진행됩니다. 먼저 방문할 동이나 역 인근 위치를 알려주시고, 희망 시간을 맞춰본 뒤, 코스와 인원을 정합니다. 이어서 해당 시간대 방문 가능 여부를 안내받고, 마지막으로 예약을 확정하면 끝입니다. 전체 통화는 보통 몇 분이면 충분하며, 절차 세부 내용은 <a href="/reservation/">예약안내</a>에 정리되어 있습니다.</p>
</section>

<section id="check">
<h2>이용 전 확인사항</h2>
<p>방문 전에 정확한 주소와 동·호수, 아파트 단지나 오피스텔의 공동현관 출입 방법, 주차 가능 여부를 미리 확인해 주시면 도착이 빨라집니다. 관리받을 공간은 조용하고 바닥이나 침대 주변이 정리된 상태면 충분하며, 숙소 방문이라면 예약자 이름과 객실 연락 방법을 함께 알려주세요. 준비 항목 전체는 <a href="/guide/">이용가이드</a>에서 확인할 수 있습니다.</p>
</section>

<section id="safety">
<h2>위생 및 안전 안내</h2>
<p>모든 방문 관리는 건전한 서비스 범위 안에서만 진행됩니다. 관리사 위생 수칙과 용품 관리 기준을 지키고, 예약 시 받은 주소와 연락처는 방문 확인 외의 목적으로 사용하지 않습니다. 불법적인 요청이나 서비스 범위를 벗어난 요구는 어떤 경우에도 거절하며, 현장에서 발생하면 즉시 중단합니다. 안심하고 이용하실 수 있는 기준을 먼저 지키겠습니다.</p>
</section>

<section id="faq">
<h2>자주 묻는 질문</h2>
<div class="faq-item">
<h3>분당구 전지역 방문이 가능한가요?</h3>
<p>정자동, 서현동, 야탑동부터 판교 일대와 율동 같은 외곽까지 18개 법정동 기준으로 안내하며, 실제 가능 여부는 예약 시간과 위치에 따라 상담에서 확정됩니다.</p>
</div>
<div class="faq-item">
<h3>서현역이나 판교역 근처 숙소도 가능한가요?</h3>
<p>주요 역세권 9곳은 역 상세 페이지에서 안내합니다. 역 이름과 건물명을 알려주시면 가능 여부를 바로 확인해 드립니다.</p>
</div>
<div class="faq-item">
<h3>수내1동 같은 행정동 페이지는 왜 없나요?</h3>
<p>숫자 행정동은 같은 생활권을 나눈 단위라서 수내동, 정자동 등 법정동 대표 페이지에서 통합해 안내합니다.</p>
</div>
<div class="faq-item">
<h3>당일 예약도 가능한가요?</h3>
<p>배정 여유가 있으면 진행됩니다. 저녁과 주말에는 문의가 몰리니 한두 시간 이상 여유를 두시길 권장합니다.</p>
</div>
<div class="faq-item">
<h3>테마는 어떻게 고르면 되나요?</h3>
<p>테마별 안내에서 14개 테마의 특징과 추천 대상을 비교할 수 있고, 고르기 어려우면 전화로 컨디션을 말씀해 주세요.</p>
</div>
</section>

{PRICING}
<section id="contact" class="cta">
<h2>예약문의</h2>
<p>분당구 방문 관리 상담과 예약은 전화가 가장 빠릅니다. 위치와 희망 시간, 원하시는 코스를 알려주시면 가능 여부를 그 자리에서 확인해 드립니다.</p>
<a class="cta-phone" href="tel:{PHONE}">{PHONE_DISPLAY}</a>
</section>
"""

PAGE = {
    "path": "",
    "title": "분당 출장마사지·홈타이 | 분당구 전지역 방문 마사지 예약 안내",
    "desc": "분당 출장마사지·홈타이 안내 페이지입니다. 정자동, 서현동, 수내동, 야탑동, 판교동과 분당구 주요 지하철역 인근, 테마별 관리, 예약 전 확인사항을 확인해보세요.",
    "h1": "분당 출장마사지·홈타이 예약 안내",
    "body": _BODY,
    "extra_head": _JSONLD,
    "breadcrumb": [],
    "hero": _HERO,
}
