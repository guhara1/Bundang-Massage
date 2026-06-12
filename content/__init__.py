# 전체 페이지 목록 집계
from . import main, areas, areas2, stations, themes, info, magazine, about

PAGES = (
    [main.PAGE]
    + areas.PAGES
    + areas2.PAGES
    + stations.PAGES
    + themes.PAGES
    + info.PAGES
    + magazine.PAGES
    + [about.PAGE]
)
