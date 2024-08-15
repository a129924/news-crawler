from datetime import datetime, timedelta
from pathlib import Path
from typing import Literal, Union

from typing_extensions import TypeAlias, TypedDict

CrawlWebsite: TypeAlias = Literal["cynes"]


class WebsiteCrawlState(TypedDict):
    name: CrawlWebsite
    last_start_time: Union[datetime, str]
    processed_items: set[str]  # set[{news_title}{news_date}]


class CrawlStateProcesser:
    def __init__(self, base_filepath: Union[str, Path], name: CrawlWebsite) -> None:
        self.website_name: CrawlWebsite = name

        base_path = Path(base_filepath)
        self.state_fullpath = base_path / "states" / f"{name}.crawler.state"

        self.state = self.load_state()

    def load_state(self) -> WebsiteCrawlState:
        """
        load_state 讀取state, 如果該路徑沒有找到 就會回傳預設的狀態
            last_start_time = datetime.now()

        Returns:
            WebsiteCrawlState: _description_
        """
        from ..utils._json import load_json_file

        try:
            state = load_json_file(self.state_fullpath.__str__())
            state["last_start_time"] = datetime.fromisoformat(state["last_start_time"])
            state["processed_items"] = set(state["processed_items"])

            return state
        except (FileNotFoundError, KeyError):
            return WebsiteCrawlState(
                name=self.website_name,
                last_start_time=datetime.now() - timedelta(days=1),
                processed_items=set(),
            )

    @staticmethod
    def generate_item_key(title: str, date: Union[str, datetime]) -> str:
        return f"{title}{date}"

    def mark_item_processed(self, item_key: str):
        """
        mark_item_processed 新增以爬取成功的新聞

        Args:
            item_key (str): 爬取成功的key({news_title}{news_date})
        """
        self.state["processed_items"].add(item_key)

    def is_item_processed(self, item_key: str) -> bool:
        """
        is_item_processed item_key是否在processed_items存在

        Args:
            item_key (str): 爬取成功的key({news_title}{news_date})

        Returns:
            bool: 是否存在
        """
        return item_key in self.state["processed_items"]

    def write_state(self, is_success: bool, success_or_error_time: datetime) -> None:
        """
        write_state 輸出新的結果到state file

        Args:
            is_success (bool): 是否完成
            success_or_error_time (datetime): 輸出的datetime
        """

        from ..utils._json import write_json_file

        self.state["last_start_time"] = success_or_error_time.isoformat()

        if is_success:
            self.state["processed_items"] = set()

        write_json_file(
            self.state_fullpath.__str__(),
            obj=self.state,
        )
