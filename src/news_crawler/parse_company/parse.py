from collections.abc import Generator, Iterable
from typing import Literal

from pyquery import PyQuery as pq
from requests import Response
from typing_extensions import NamedTuple, TypedDict

COMPANY_MARKET = Literal["公開發行", "上市", "上櫃"]


class Company(TypedDict):
    name: str
    english_name: str
    short_name: str
    market: COMPANY_MARKET
    code: str


class CompanyName(NamedTuple):
    name: str
    english_name: str
    short_name: str


def fetch_url(
    url: str,
    headers: dict[str, str],
    params: dict[str, str],
    timeout: int = 10,
) -> Response:
    """
    fetch_url

    Args:
        url (str): 網址
        headers (dict[str, str]): 標頭
        params (dict[str, str]): 參數
        timeout (int, optional): 超時時間. Defaults to 10.

    Returns:
        Response: 回傳的 Response
    """
    from requests import get

    return get(url, headers=headers, params=params, timeout=timeout)


def parse_company_list(
    html: str, filter_company_name: Iterable[str] = {"公開發行", "上市", "上櫃"}
) -> Generator[Company, None, None]:
    """
    解析公司列表HTML並生成符合條件的公司信息。

    Args:
        html (str): 包含公司列表的HTML字符串。
        filter_company_name (Iterable[str], optional): 用於篩選公司市場類型的集合。
            默認為 {"公開發行", "上市", "上櫃"}。

    Yields:
        Generator[Company, None, None]: 生成器，每次產生一個符合篩選條件的Company對象。

    說明:
        此函數解析給定的HTML，提取公司信息，並根據指定的市場類型進行篩選。
        只有市場類型在filter_company_name中的公司才會被生成。
    """

    doc = pq(html)

    for tr in doc("table.table-striped tbody tr").items():
        company = parse_company(tr)
        if company["market"] in filter_company_name:
            yield company


def process_company_name(company_name_text: str) -> CompanyName:
    """
    process_company_name

    Args:
        company_name_text (str): 公司名稱所在的 text

    Returns:
        CompanyName: 公司名稱、英文名稱、簡稱
    """
    from re import match

    pattern = r"^(.*?)\((.*?)\)$"

    short_name_and_english_name, company_name = company_name_text.split("\n")
    match_result = match(pattern, short_name_and_english_name)

    if match_result:
        return CompanyName(
            name=company_name,
            english_name=match_result.group(2),
            short_name=match_result.group(1),
        )
    else:
        return CompanyName(company_name, "", "")


def parse_company(tr: pq) -> Company:
    """
    parse_company

    Args:
        tr (pq): 公司 tr

    Returns:
        Company: 公司
    """

    company_name_group = process_company_name(tr("td:nth-child(3)").text().__str__())

    return Company(
        name=company_name_group.name,
        english_name=company_name_group.english_name,
        short_name=company_name_group.short_name,
        market=tr("td:nth-child(1)").text().__str__(),  # type: ignore
        code=tr("td:nth-child(2)").text().__str__(),
    )


def main() -> Generator[Company, None, None]:
    """
    main

    Returns:
        Generator[Company, None, None]: 生成器，每次產生一個符合篩選條件的Company對象。
    """
    response = fetch_url(
        url="https://p.twincn.com/lm.aspx",
        headers={
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "priority": "u=0, i",
            "referer": "https://p.twincn.com/",
            "sec-ch-ua": '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Android"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Linux; Android) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.109 Safari/537.36 CrKey/1.54.248666",
        },
        params={"q": "股份有限公司"},
    )

    if response.status_code != 200:
        raise ValueError(f"Failed to fetch URL: {response.status_code}")

    yield from parse_company_list(
        html=response.text, filter_company_name=["上市", "上櫃"]
    )


if __name__ == "__main__":
    for index, company in enumerate(main(), 1):
        print(f"{index}. {company}")
