import dataclasses
import datetime
import functools
import html
import json
import typing

import requests


BASE_URL = "https://www.megabox.co.kr"
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0",
}

MSG_ON_SUCCESS = "정상적으로 조회되었습니다."


class bool_to_yn:
    def __new__(cls, value: bool) -> str:
        return "Y" if value else "N"


class yyyymmdd_to_date:
    def __new__(cls, value: str) -> datetime.date:
        y = value[0:4]
        m = value[4:6]
        d = value[6:8]
        return datetime.date(year=int(y), month=int(m), day=int(d))


@dataclasses.dataclass
class Movie:
    movieNo: str  # ex) "25008000"
    boxoRank: int  # ex) 1
    boxoAccmRank: int  # ex) 6
    megaScoreRank: int  # ex) 4
    boxoBokdRt: float  # ex) 37.5
    mxTheabAt: str  # ex) "Y"
    dbcTheabAt: str  # ex) "Y"
    mx4dTheabAt: str  # ex) "Y"
    boutqTheabAt: str  # ex) "Y"
    boxoKofTotAdncCnt: int  # ex) 642113
    movieNm: str  # ex) "\uC9C4\uACA9\uC758 \uAC70\uC778 \uC644\uACB0\uD3B8 \uB354 \uB77C\uC2A4\uD2B8 \uC5B4\uD0DD"
    rpstMovieNo: str  # ex) "25008000"
    filmAt: str  # ex) "N"
    classicAt: str  # ex) "N"
    disneyAt: str  # ex) "N"
    playTime: str  # ex) "144"
    admisClassCd: str  # ex) "AD03"
    movieStatCd: str  # ex) "MSC01"
    rfilmDe: str  # ex) "2025.03.13"
    rfilmYm: str  # ex) "2025.03"
    rfilmDeReal: str  # ex) "20250313"
    dday: int  # ex) 25
    bokdAbleAt: str  # ex) "Y"
    bokdAbleYn: str  # ex) "Y"
    rfilmAt: str  # ex) "Y"
    movieStatNm: str  # ex) "\uC0C1\uC601\uC911"
    admisClassNm: str  # ex) "15\uC138\uC774\uC0C1\uAD00\uB78C\uAC00"
    expeAt: str  # ex) "N"
    prevAt: str  # ex) "N"
    intrstCnt: int  # ex) 7828
    intrstAt: str  # ex) "N"
    totalSpoint: float  # ex) 10.8
    admisNSpoint: int  # ex) 0
    admisYSpoint: float  # ex) 9.6
    megaCubeAt: str  # ex) "Y"
    rowNum: int  # ex) 1
    totCnt: int  # ex) 1
    imgPathNm: str  # ex) "/SharedImg/2025/03/19/t1aws8JYeDCKaCbRntA8oalmQ2UW33ua.jpg"
    atchFileNo: int  # ex) 1
    movieImgKindCd: str  # ex) "MIK01"
    playDday: int  # ex) -30
    movieSynopCn: str  # ex) "\uC774\uAC83\uC774 \uCD5C\uD6C4\uC758 &quot;\uC9C4\uACA9&quot;---!\n\uAC70\uC778\uC758 \uC704\uD611\uC73C\uB85C\uBD80\uD130 \uBAB8\uC744 \uC9C0\uD0A4\uAE30 \uC704\uD574 \uAC70\uB300\uD55C \uBCBD\uC744 \uC313\uACE0 \uADF8 \uC548\uC5D0\uC11C \uC228\uC744 \uC8FD\uC774\uACE0 \uC0B4\uACE0 \uC788\uB294 \uC778\uB958.\n\uBC31 \uB144\uC758 \uD3C9\uD654\uB294 \uCD08\uB300\uD615 \uAC70\uC778\uC758 \uC2B5\uACA9\uC73C\uB85C \uD30C\uAD34\uB410\uACE0, \uC5B4\uBA38\uB2C8\uB97C \uC783\uC740 \uC18C\uB144 \uC5D8\uB7F0 \uC608\uAC70\uB294\n\uBAA8\uB4E0 \uAC70\uC778\uC744 \uC5C6\uC568 \uAC83\uC744 \uB9F9\uC138\uD558\uACE0 \uAC70\uC778\uACFC \uC2F8\uC6B0\uB294 \uC870\uC0AC\uBCD1\uB2E8\uC758 \uC77C\uC6D0\uC774 \uB418\uC5C8\uB2E4.\n\n\uAE00\uC790 \uADF8\uB300\uB85C \uBAA9\uC228\uC744 \uAC74 \uC2F8\uC6C0 \uC18D\uC5D0\uC11C \uC5D8\uB7F0 \uC608\uAC70\uB294 \uC790\uC2E0\uB3C4 \uAC70\uC778\uC774 \uB418\uB294 \uB2A5\uB825\uC744 \uC190\uC5D0 \uB123\uC5C8\uACE0\n\uC778\uB958\uC758 \uC2B9\uB9AC\uC5D0 \uACF5\uD5CC\uD558\uBA74\uC11C \uC870\uAE08\uC529 \uC138\uACC4\uC758 \uC9C4\uC2E4\uC5D0 \uAC00\uAE4C\uC6CC\uC9C0\uACE0 \uC788\uC5C8\uB2E4. \uC774\uC73D\uACE0 \uC2DC\uAC04\uC774 \uD758\uB7EC \uBCBD \uBC16\uC73C\uB85C \uB098\uAC04 \uC5D8\uB7F0\uC740\n\uC870\uC0AC\uBCD1\uB2E8\uC758 \uB3D9\uB8CC\uB4E4\uACFC \uAC08\uB77C\uC130\uACE0 \uC5B4\uB5A4 \uBB34\uC2DC\uBB34\uC2DC\uD55C \uACC4\uD68D\uC744 \uC2E4\uD589\uD55C\uB2E4.\n\n\uC218\uB9CE\uC740 \uAC70\uC778\uC744 \uC774\uB04C\uACE0, \uC774 \uC138\uACC4\uC758 \uC0B4\uC544\uC788\uB294 \uBAA8\uB4E0 \uAC83\uB4E4\uC744 \uC9D3\uBC1F\uB294 \u300C\uB545\uC6B8\uB9BC\u300D.\n\n\uBBF8\uCE74\uC0AC\uC640 \uC544\uB974\uBBFC\uC744 \uC2DC\uC791\uC73C\uB85C \uB0A8\uACA8\uC9C4 \uC790\uB4E4\uC740 \uC138\uACC4\uB97C \uBA78\uB9DD\uC2DC\uD0A4\uB824 \uD558\uB294 \uC5D8\uB7F0\uC744 \uB9C9\uAE30\n\uC704\uD574 \uCD5C\uD6C4\uC758 \uC2F8\uC6C0\uC5D0 \uB098\uC120\uB2E4.\n"
    specialType: None  # ex) null
    onairYn: str  # ex) "N"
    movienmSearchYn: str  # ex) "Y"
    festivalYn: str  # ex) "N"
    movieCttsNm: None  # ex) null
    filmAfAt: str  # ex) "N"
    singlPlayAt: str  # ex) "Y"
    megaOnlyAt: str  # ex) "N"
    atmosTheabIncAt: str  # ex) "N"
    dolbyTheabIncAt: str  # ex) "N"
    mx4dTheabIncAt: str  # ex) "Y"
    schdlYn: str  # ex) "Y"
    currentPage: int  # ex) 1
    recordCountPerPage: int  # ex) 20


class SelectBokdListResponse:
    def __init__(self, raw_data: dict):
        self._raw = raw_data

    @property
    def movie_form_list(self) -> typing.List['MovieForm']:
        return list(map(MovieForm, self._raw["movieFormList"]))

    @property
    def date_list(self) -> typing.List[datetime.date]:
        return [yyyymmdd_to_date(item["playDe"]) for item in self._raw['movieFormDeList']]


class MovieForm:
    def __init__(self, raw_data: dict):
        self._raw = raw_data

    @property
    def branch_id(self) -> int:
        return int(self._raw["brchNo"])

    @property
    def branch_name(self) -> str:
        return html.unescape(self._raw["brchNm"])

    @property
    def rest_seat_count(self) -> int:
        return self._raw["restSeatCnt"]

    @property
    def total_seat_count(self) -> int:
        return self._raw["totSeatCnt"]

    @property
    def play_start_time(self) -> str:
        return self._raw["playStartTime"]

    @property
    def play_end_time(self) -> str:
        return self._raw["playEndTime"]

    @property
    def play_date(self) -> datetime.date:
        return yyyymmdd_to_date(self._raw["playDe"])

    @property
    def play_kind_code(self) -> str:
        return self._raw["playKindCd"]

    @property
    def play_kind_name(self) -> str:
        return html.unescape(self._raw["playKindNm"])

    @property
    def is_2d_mx4d(self) -> bool:
        return self._raw["playKindCd"] == "MK32"

    @property
    def view_date(self) -> str:
        return html.unescape(self._raw["viewDe"])


def megabox_api(url: str, payload: str) -> dict:
    response = requests.post(
        url=BASE_URL+url,
        headers=DEFAULT_HEADERS,
        data=payload,
    )
    data = response.json()
    assert data['msg'] == MSG_ON_SUCCESS, data
    return data


def select_movie_list(
    currentPage: int = 1,
    recordCountPerPage: int = 20,
    ibxMovieNmSearch: str = "",
    onair: bool = False,
    special: bool = False,
) -> dict:
    request_url = "/on/oh/oha/Movie/selectMovieList.do"
    payload = json.dumps({
        "currentPage": str(currentPage),
        "recordCountPerPage": str(recordCountPerPage),
        "pageType": "ticketing",
        "ibxMovieNmSearch": ibxMovieNmSearch,
        "onairYn": bool_to_yn(onair),
        "specialType": "",
        "specialYn": bool_to_yn(special),
    })
    return megabox_api(url=request_url, payload=payload)


def select_bokd_list(
    movieNo: str,
    playDe: datetime.date,
) -> SelectBokdListResponse:
    request_url = "/on/oh/ohb/SimpleBooking/selectBokdList.do"
    payload = json.dumps({
        "arrMovieNo": movieNo,  # Required "25008000"
        "playDe": playDe.strftime("%Y%m%d"),  # ex "20250407",
        "brchNoListCnt": 3,
        "brchNo1": "1351",  # 코엑스
        "brchNo2": "4651",  # 하남스타필드
        "brchNo3": "0052",  # 수원ak플라자 (수원역)
        "brchNo4": "",
        "brchNo5": "",
        "areaCd1": "10",
        "areaCd2": "30",
        "areaCd3": "30",
        "areaCd2": "",
        "areaCd3": "",
        "areaCd4": "",
        "areaCd5": "",
        "spclbYn1": "N",
        "spclbYn2": "N",
        "spclbYn3": "N",
        "spclbYn4": "",
        "spclbYn5": "",
        "theabKindCd1": "10",
        "theabKindCd2": "30",
        "theabKindCd3": "30",
        "theabKindCd4": "",
        "theabKindCd5": "",
        "brchAll": "30",
        "brchSpcl": "",
        "movieNo1": movieNo,
        "movieNo2": "",
        "movieNo3": "",
        "sellChnlCd": "",
    })
    response = megabox_api(url=request_url, payload=payload)
    return SelectBokdListResponse(response)
