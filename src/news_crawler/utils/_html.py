from scrapy import Selector


def get_text(
    html_string: str,
    element: str,
) -> str:
    return "".join(
        Selector(text=html_string.replace("&lt;", "<").replace("&gt;", ">"))
        .css(f"{element}::text")
        .getall()
    )
