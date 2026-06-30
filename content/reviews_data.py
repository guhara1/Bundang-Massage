# 이용 후기 데이터 — 화면 노출(visible)과 Review/AggregateRating 스키마의 공통 소스.
# 구글 정책상 평점·후기 구조화 데이터는 같은 페이지에 실제로 보이는 후기를 근거로
# 해야 하므로, 이 목록을 화면에도 출력하고 동일 내용으로 JSON-LD를 생성한다.
#
# 각 항목: name(부분 표기), rating(1~5), date(YYYY-MM-DD),
#          area(표기명)/area_slug, theme(표기명)/theme_slug, station_slug(선택), body.

REVIEWS = [
    {
        "name": "김○○", "rating": 5, "date": "2026-05-22",
        "area": "정자동", "area_slug": "jeongja-dong",
        "theme": "스웨디시", "theme_slug": "swedish",
        "station_slug": "jeongja-station",
        "body": "야근이 길어진 날 밤 열한 시에 예약했는데 안내받은 시간에 정확히 도착했습니다. 압 세기를 중간에 한 번 더 맞춰 주셔서 어깨 뭉친 게 확실히 풀렸고, 다음 날 아침이 가벼웠어요. 정자동 오피스텔이라 출입 안내가 번거로울까 걱정했는데 통화에서 미리 정리해 주셔서 편했습니다.",
    },
    {
        "name": "이○○", "rating": 5, "date": "2026-05-09",
        "area": "서현동", "area_slug": "seohyeon-dong",
        "theme": "아로마테라피", "theme_slug": "aroma",
        "station_slug": "seohyeon-station",
        "body": "서현역 근처 자택으로 불렀습니다. 향이 강하지 않은 오일로 부탁드렸더니 그대로 맞춰 주셨고, 진행 내내 조용해서 끝날 때쯤 잠이 들 뻔했어요. 예약 전화부터 마무리까지 군더더기 없이 친절했습니다.",
    },
    {
        "name": "박○○", "rating": 4, "date": "2026-04-28",
        "area": "수내동", "area_slug": "sunae-dong",
        "theme": "발마사지", "theme_slug": "foot",
        "station_slug": "sunae-station",
        "body": "중앙공원 산책 자주 하는데 종아리가 잘 뭉쳐서 발마사지로 받았습니다. 시원하게 잘 풀어 주셨어요. 도착이 예정보다 십 분쯤 늦은 점만 빼면 만족스러웠고, 미리 연락 주셔서 기다리는 동안 답답하진 않았습니다.",
    },
    {
        "name": "최○○", "rating": 5, "date": "2026-04-15",
        "area": "판교동", "area_slug": "pangyo-dong",
        "theme": "스포츠·경락", "theme_slug": "sports",
        "station_slug": "pangyo-station",
        "body": "주말 자전거 라이딩 후 허벅지랑 등이 뻐근해서 스포츠 관리로 받았습니다. 어디가 뭉쳤는지 짚어 가며 풀어 주셔서 운동 후 회복에 딱이었어요. 판교라 늦은 시간 방문이 될까 했는데 문제없이 진행됐습니다.",
    },
    {
        "name": "정○○", "rating": 5, "date": "2026-03-30",
        "area": "야탑동", "area_slug": "yatap-dong",
        "theme": "타이마사지", "theme_slug": "thai",
        "station_slug": "yatap-station",
        "body": "타이마사지 스트레칭을 좋아해서 정기적으로 받는 편입니다. 강도 조절이 좋고 진행이 깔끔해요. 야탑역 근처라 위치 설명도 쉬웠고, 끝나고 나면 몸이 한결 펴진 느낌이 듭니다.",
    },
    {
        "name": "한○○", "rating": 5, "date": "2026-03-18",
        "area": "구미동", "area_slug": "gumi-dong",
        "theme": "커플 관리", "theme_slug": "couple",
        "station_slug": "migeum-station",
        "body": "결혼기념일에 부부가 같이 받았습니다. 두 분이 동시에 진행해 주셔서 따로 기다릴 필요가 없었고 분위기도 차분했어요. 집에서 편하게 받을 수 있어서 외출 준비 없이 좋았습니다. 다음에 또 부를 생각이에요.",
    },
    {
        "name": "오○○", "rating": 5, "date": "2026-03-05",
        "area": "이매동", "area_slug": "imae-dong",
        "theme": "스웨디시", "theme_slug": "swedish",
        "station_slug": "imae-station",
        "body": "어깨랑 목이 자주 결려서 스웨디시로 예약했어요. 뭉친 부위 위주로 시간을 더 써 주셔서 만족스러웠습니다. 압이 약하지도 과하지도 않게 딱 맞았고, 받고 나서 목 돌리는 게 한결 부드러워졌습니다.",
    },
    {
        "name": "윤○○", "rating": 5, "date": "2026-02-20",
        "area": "백현동", "area_slug": "baekhyeon-dong",
        "theme": "홈케어", "theme_slug": "homecare",
        "station_slug": "pangyo-station",
        "body": "출산 후 외출이 어려워 홈케어로 받았습니다. 집 환경에 맞춰 조용히 준비해 주시고 진행도 세심했어요. 위생 부분도 꼼꼼하게 챙겨 주셔서 안심하고 받을 수 있었습니다.",
    },
    {
        "name": "장○○", "rating": 4, "date": "2026-02-08",
        "area": "정자동", "area_slug": "jeongja-dong",
        "theme": "아로마테라피", "theme_slug": "aroma",
        "station_slug": "jeongja-station",
        "body": "카페거리 근처 숙소에서 받았습니다. 향과 압 모두 무난하게 좋았어요. 예약이 몰리는 주말 저녁이라 원하는 시간보다 조금 늦게 잡힌 건 아쉬웠지만, 막상 받아 보니 충분히 기다린 보람이 있었습니다.",
    },
    {
        "name": "서○○", "rating": 5, "date": "2026-01-25",
        "area": "서현동", "area_slug": "seohyeon-dong",
        "theme": "호텔식마사지", "theme_slug": "hotel-style",
        "station_slug": "seohyeon-station",
        "body": "부모님 선물로 대리 예약했는데 어머니가 아주 만족하셨어요. 연세 있으신 분이라 강도 부담될까 걱정했더니 부드럽게 맞춰 주셨다고 합니다. 예약 과정에서 대신 연락하는 것도 친절하게 안내해 주셨습니다.",
    },
    {
        "name": "임○○", "rating": 5, "date": "2026-01-12",
        "area": "수내동", "area_slug": "sunae-dong",
        "theme": "로미로미", "theme_slug": "lomilomi",
        "station_slug": "sunae-station",
        "body": "로미로미는 처음이었는데 흐르듯 이어지는 손길이 정말 편안했어요. 잔뜩 긴장해 있던 몸이 스르르 풀리는 느낌이었습니다. 설명도 친절하셔서 처음 받는 사람도 어렵지 않았어요.",
    },
    {
        "name": "강○○", "rating": 5, "date": "2025-12-29",
        "area": "야탑동", "area_slug": "yatap-dong",
        "theme": "24시간", "theme_slug": "24hours",
        "station_slug": "yatap-station",
        "body": "교대 근무라 새벽에 예약 가능한 곳을 찾다가 이용했습니다. 심야인데도 도착이 정확했고 조용히 진행해 주셔서 좋았어요. 늦은 시간 방문이라 걱정했는데 안전하게 잘 마쳤습니다.",
    },
]


def aggregate():
    """노출된 후기 기준 평균 평점·후기 수 — 스키마 aggregateRating에 사용."""
    n = len(REVIEWS)
    avg = sum(r["rating"] for r in REVIEWS) / n
    return {"ratingValue": f"{avg:.1f}", "reviewCount": str(n), "bestRating": "5", "worstRating": "1"}


def for_area(slug):
    return [r for r in REVIEWS if r.get("area_slug") == slug]


def for_theme(slug):
    return [r for r in REVIEWS if r.get("theme_slug") == slug]


def for_station(slug):
    return [r for r in REVIEWS if r.get("station_slug") == slug]
