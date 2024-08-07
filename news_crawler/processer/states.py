from datetime import datetime
from pathlib import Path
from typing import Literal, Optional, Union

from typing_extensions import TypeAlias, TypedDict

CrawlWebsite: TypeAlias = Literal["cynes"]


class WebsiteCrawlState(TypedDict):
    name: CrawlWebsite
    last_start_time: datetime


class CrawlStateProcesser:
    def __init__(self, base_filepath: Union[str, Path], name: CrawlWebsite) -> None:
        self.website_name: CrawlWebsite = name
        self.start_time = datetime.now()

        base_path = Path(base_filepath)
        self.state_fullpath = base_path / "states" / f"{name}.crawler.state"
        print(f"{self.state_fullpath = }")
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
            print(f"{state = }")

            return state
        except FileNotFoundError:
            return WebsiteCrawlState(
                name=self.website_name, last_start_time=datetime.now()
            )

    def write_state(self, start_time: Optional[datetime] = None) -> None:
        """
        write_state 輸出新的結果到state file
        """
        from ..utils._json import write_json_file

        write_json_file(
            self.state_fullpath.__str__(),
            obj={
                "name": self.website_name,
                "last_start_time": (start_time or self.start_time).isoformat(),
            },
        )
