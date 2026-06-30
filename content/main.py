# 메인 페이지 — 분당 허브. 키워드를 한곳에 몰지 않고 지역·역·테마 상세 페이지로 연결한다.
# LocalBusiness/FAQPage/AggregateRating 등 구조화 데이터는 build.py 에서 전 페이지 공통 생성한다.
from .site import BASE_URL, BRAND, PHONE, PHONE_DISPLAY
from .pricing import PRICING

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
<ul class="link-grid">
<li><a href="/bundang/bundang-dong/"><span class="lg-t">분당동 출장마사지</span><span class="lg-s">불곡산 자락 조용한 주거지 방문</span></a></li>
<li><a href="/bundang/sunae-dong/"><span class="lg-t">수내동 출장마사지</span><span class="lg-s">중앙공원·수내역 도보권 홈타이</span></a></li>
<li><a href="/bundang/jeongja-dong/"><span class="lg-t">정자동 출장마사지</span><span class="lg-s">카페거리·정자역 심야 방문</span></a></li>
<li><a href="/bundang/seohyeon-dong/"><span class="lg-t">서현동 출장마사지</span><span class="lg-s">서현역 상권 인근 자택·숙소</span></a></li>
<li><a href="/bundang/imae-dong/"><span class="lg-t">이매동 출장마사지</span><span class="lg-s">이매역 인근 아파트촌 방문</span></a></li>
<li><a href="/bundang/yatap-dong/"><span class="lg-t">야탑동 출장마사지</span><span class="lg-s">야탑역·터미널 24시간 권역</span></a></li>
<li><a href="/bundang/gumi-dong/"><span class="lg-t">구미동 출장마사지</span><span class="lg-s">미금역·오리역 남부 주거권</span></a></li>
<li><a href="/bundang/geumgok-dong/"><span class="lg-t">금곡동 출장마사지</span><span class="lg-s">정자권 인접 생활권 홈타이</span></a></li>
<li><a href="/bundang/gungnae-dong/"><span class="lg-t">궁내동 출장마사지</span><span class="lg-s">분당 남단 전원형 주거지</span></a></li>
<li><a href="/bundang/dongwon-dong/"><span class="lg-t">동원동 출장마사지</span><span class="lg-s">청계산 자락 저밀도 권역</span></a></li>
<li><a href="/bundang/baekhyeon-dong/"><span class="lg-t">백현동 출장마사지</span><span class="lg-s">판교 카페거리·아파트 방문</span></a></li>
<li><a href="/bundang/sampyeong-dong/"><span class="lg-t">삼평동 출장마사지</span><span class="lg-s">판교테크노밸리 오피스 인근</span></a></li>
<li><a href="/bundang/pangyo-dong/"><span class="lg-t">판교동 출장마사지</span><span class="lg-s">판교역 신도시 중심 홈타이</span></a></li>
<li><a href="/bundang/unjung-dong/"><span class="lg-t">운중동 출장마사지</span><span class="lg-s">운중천·판교 서편 주거권</span></a></li>
<li><a href="/bundang/daejang-dong/"><span class="lg-t">대장동 출장마사지</span><span class="lg-s">신규 택지 주거권 방문</span></a></li>
<li><a href="/bundang/seogun-dong/"><span class="lg-t">석운동 출장마사지</span><span class="lg-s">청계산 전원 주택 권역</span></a></li>
<li><a href="/bundang/yul-dong/"><span class="lg-t">율동 출장마사지</span><span class="lg-s">율동공원 인근 외곽 방문</span></a></li>
<li><a href="/bundang/hasanun-dong/"><span class="lg-t">하산운동 출장마사지</span><span class="lg-s">분당 남서단 전원 권역</span></a></li>
</ul>
<p>분당구 전체 구조는 <a href="/bundang/">지역 전체 안내</a>에서 한 번에 볼 수 있습니다.</p>
</section>

<section id="stations">
<h2>지하철역 인근 안내</h2>
<p>분당구는 수인분당선과 신분당선이 남북으로 지나고, 판교역에는 경강선, 성남역에는 GTX-A가 더해진 지역입니다. 역 안내는 아홉 개 주요 역 기준이며, 두 노선이 만나는 환승역도 페이지는 하나만 운영합니다. 출구별 페이지는 만들지 않고, 정확한 위치는 예약 통화에서 건물 기준으로 확인합니다.</p>
<ul class="link-grid">
<li><a href="/bundang/stations/yatap-station/"><span class="lg-t">야탑역 출장마사지</span><span class="lg-s">분당선·터미널 환승 거점 홈타이</span></a></li>
<li><a href="/bundang/stations/imae-station/"><span class="lg-t">이매역 출장마사지</span><span class="lg-s">분당선·경강선 환승 인근</span></a></li>
<li><a href="/bundang/stations/seohyeon-station/"><span class="lg-t">서현역 출장마사지</span><span class="lg-s">분당 최대 역세권 숙소·자택</span></a></li>
<li><a href="/bundang/stations/sunae-station/"><span class="lg-t">수내역 출장마사지</span><span class="lg-s">중앙공원·업무지구 홈타이</span></a></li>
<li><a href="/bundang/stations/jeongja-station/"><span class="lg-t">정자역 출장마사지</span><span class="lg-s">분당선·신분당 환승 카페거리</span></a></li>
<li><a href="/bundang/stations/migeum-station/"><span class="lg-t">미금역 출장마사지</span><span class="lg-s">분당선·신분당 환승 남부권</span></a></li>
<li><a href="/bundang/stations/ori-station/"><span class="lg-t">오리역 출장마사지</span><span class="lg-s">분당선 남단 종착 권역</span></a></li>
<li><a href="/bundang/stations/pangyo-station/"><span class="lg-t">판교역 출장마사지</span><span class="lg-s">신분당·경강 테크노밸리 인근</span></a></li>
<li><a href="/bundang/stations/seongnam-station/"><span class="lg-t">성남역 출장마사지</span><span class="lg-s">GTX-A·신분당 광역환승 거점</span></a></li>
</ul>
</section>

<section id="themes">
<h2>테마별 관리 안내</h2>
<p>관리 테마는 14개 독립 페이지에서 기법의 특징과 추천 대상, 받기 전 확인사항을 설명합니다. 동이나 역과 테마를 묶은 조합 페이지는 운영하지 않는데, 어느 위치든 같은 테마라면 진행 방식이 같아 내용만 중복되기 때문입니다. 테마를 먼저 정하고 위치는 예약 시 알려주시면 충분합니다.</p>
<ul class="link-grid">
<li><a href="/themes/swedish/"><span class="lg-t">스웨디시 마사지</span><span class="lg-s">부드러운 압·수면 개선</span></a></li>
<li><a href="/themes/lomilomi/"><span class="lg-t">로미로미 마사지</span><span class="lg-s">하와이안 오일 릴랙스</span></a></li>
<li><a href="/themes/thai/"><span class="lg-t">타이마사지</span><span class="lg-s">스트레칭·전신 이완</span></a></li>
<li><a href="/themes/chinese/"><span class="lg-t">중국마사지</span><span class="lg-s">경혈 지압·뭉침 케어</span></a></li>
<li><a href="/themes/aroma/"><span class="lg-t">아로마테라피</span><span class="lg-s">오일 향기 힐링 관리</span></a></li>
<li><a href="/themes/homecare/"><span class="lg-t">홈케어 마사지</span><span class="lg-s">집 환경 맞춤 방문 관리</span></a></li>
<li><a href="/themes/hotel-style/"><span class="lg-t">호텔식 마사지</span><span class="lg-s">정중한 프리미엄 진행</span></a></li>
<li><a href="/themes/foot/"><span class="lg-t">발마사지</span><span class="lg-s">다리 피로·부종 완화</span></a></li>
<li><a href="/themes/sports/"><span class="lg-t">스포츠·경락 마사지</span><span class="lg-s">운동 후 근육 회복</span></a></li>
<li><a href="/themes/skincare/"><span class="lg-t">스킨케어 방문 관리</span><span class="lg-s">피부 톤·컨디션 케어</span></a></li>
<li><a href="/themes/waxing/"><span class="lg-t">출장 왁싱</span><span class="lg-s">위생적 방문 제모 관리</span></a></li>
<li><a href="/themes/couple/"><span class="lg-t">커플 마사지</span><span class="lg-s">2인 동시 진행 방문</span></a></li>
<li><a href="/themes/24hours/"><span class="lg-t">24시간 출장마사지</span><span class="lg-s">새벽·심야 예약 가능</span></a></li>
<li><a href="/themes/overnight/"><span class="lg-t">수면 가능 마사지</span><span class="lg-s">숙박 동반 장시간 관리</span></a></li>
</ul>
</section>

<section id="topics">
<h2>자주 찾는 주제별 안내</h2>
<p>상황과 목적에 맞는 주제로도 바로 찾아보실 수 있습니다. 아래 링크는 지역·역·테마 안내와 매거진 가이드 중 관련 페이지로 연결됩니다.</p>
<ul class="topic-links">
<li><a href="/themes/24hours/">심야·새벽 출장마사지</a></li>
<li><a href="/themes/overnight/">숙소·호텔 홈타이</a></li>
<li><a href="/themes/couple/">커플 함께 받는 마사지</a></li>
<li><a href="/themes/sports/">운동 후 회복 마사지</a></li>
<li><a href="/magazine/post-workout-timing/">운동 후 마사지 타이밍</a></li>
<li><a href="/magazine/neck-shoulder-care/">어깨·목 결림 관리</a></li>
<li><a href="/magazine/sleep-and-massage/">불면·수면을 위한 마사지</a></li>
<li><a href="/magazine/parents-gift/">부모님 선물 마사지 예약</a></li>
<li><a href="/magazine/first-time-guide/">처음 받는 출장마사지 가이드</a></li>
<li><a href="/magazine/swedish-vs-thai/">스웨디시·타이 비교</a></li>
<li><a href="/bundang/stations/seohyeon-station/">서현역 근처 홈타이</a></li>
<li><a href="/bundang/stations/pangyo-station/">판교역 근처 출장마사지</a></li>
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
    "desc": "분당 출장마사지·홈타이 안내입니다. 정자동, 서현동, 야탑동, 판교동 등 지역·지하철역·테마별 관리와 예약 안내를 확인해보세요.",
    "h1": "분당 출장마사지·홈타이 예약 안내",
    "body": _BODY,
    "extra_head": '<meta name="naver-site-verification" content="b5385ebd6f88dae26a58f366236d68dd9bab9ba0" />\n',
    "breadcrumb": [],
    "hero": _HERO,
}
