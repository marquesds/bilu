from bilu.browser.duckduckgo import DuckDuckGoBrowser


async def get_results(query: str) -> str:
    browser = DuckDuckGoBrowser(query=query)
    return browser.results()


async def get_result_page(query: str, choice: str) -> str:
    browser = DuckDuckGoBrowser(query=query)
    return browser.result_page(choice=choice)
