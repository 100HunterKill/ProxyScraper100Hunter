import re
from bs4 import BeautifulSoup
import httpx
from typing import List

class Scraper:
    def __init__(self, method: str, _url: str):
        self.method = method
        self._url = _url

    def get_url(self, **kwargs) -> str:
        return self._url.format(**kwargs, method=self.method)

    async def get_response(self, client: httpx.AsyncClient) -> httpx.Response:
        return await client.get(self.get_url())

    async def handle(self, response: httpx.Response) -> str:
        return response.text

    async def scrape(self, client: httpx.AsyncClient) -> List[str]:
        response = await self.get_response(client)
        proxies = await self.handle(response)
        pattern = re.compile(r"\d{1,3}(?:\.\d{1,3}){3}(?::\d{1,5})?")
        return re.findall(pattern, proxies)


class SpysMeScraper(Scraper):
    def __init__(self, method: str):
        super().__init__(method, "https://spys.me/{mode}.txt")

    def get_url(self, **kwargs) -> str:
        if self.method == "http":
            mode = "proxy"
        elif self.method == "socks":
            mode = "socks"
        else:
            raise NotImplementedError(f"Protocol {self.method} is not supported for SpysMeScraper")
        return super().get_url(mode=mode, **kwargs)


class ProxyScrapeScraper(Scraper):
    def __init__(self, method: str, timeout: int = 1000, country: str = "All"):
        self.timeout = timeout
        self.country = country
        super().__init__(method,
                         "https://api.proxyscrape.com/?request=getproxies"
                         "&proxytype={method}"
                         "&timeout={timeout}"
                         "&country={country}")

    def get_url(self, **kwargs) -> str:
        return super().get_url(timeout=self.timeout, country=self.country, **kwargs)


class GeoNodeScraper(Scraper):
    def __init__(self, method: str, limit: str = "1000", page: str = "1", sort_by: str = "lastChecked", sort_type: str = "desc"):
        self.limit = limit
        self.page = page
        self.sort_by = sort_by
        self.sort_type = sort_type
        super().__init__(method,
                         "https://proxylist.geonode.com/api/proxy-list?"
                         "&limit={limit}"
                         "&page={page}"
                         "&sort_by={sort_by}"
                         "&sort_type={sort_type}")

    def get_url(self, **kwargs) -> str:
        return super().get_url(limit=self.limit, page=self.page, sort_by=self.sort_by, sort_type=self.sort_type, **kwargs)


class ProxyListDownloadScraper(Scraper):
    def __init__(self, method: str, anon: str):
        self.anon = anon
        super().__init__(method, "https://www.proxy-list.download/api/v1/get?type={method}&anon={anon}")

    def get_url(self, **kwargs) -> str:
        return super().get_url(anon=self.anon, **kwargs)


class GeneralTableScraper(Scraper):
    async def handle(self, response: httpx.Response) -> str:
        soup = BeautifulSoup(response.text, "html.parser")
        proxies = set()
        table = soup.find("table", attrs={"class": "table table-striped table-bordered"})
        for row in table.findAll("tr"):
            count = 0
            proxy = ""
            for cell in row.findAll("td"):
                if count == 1:
                    proxy += ":" + cell.text.replace("&nbsp;", "")
                    proxies.add(proxy)
                    break
                proxy += cell.text.replace("&nbsp;", "")
                count += 1
        return "\n".join(proxies)


class GeneralDivScraper(Scraper):
    async def handle(self, response: httpx.Response) -> str:
        soup = BeautifulSoup(response.text, "html.parser")
        proxies = set()
        table = soup.find("div", attrs={"class": "list"})
        for row in table.findAll("div"):
            count = 0
            proxy = ""
            for cell in row.findAll("div", attrs={"class": "td"}):
                if count == 2:
                    break
                proxy += cell.text + ":"
                count += 1
            proxy = proxy.rstrip(":")
            proxies.add(proxy)
        return "\n".join(proxies)


class GitHubScraper(Scraper):
    async def handle(self, response: httpx.Response) -> str:
        tempproxies = response.text.split("\n")
        proxies = set()
        for prxy in tempproxies:
            if self.method in prxy:
                proxies.add(prxy.split("//")[-1])
        return "\n".join(proxies)
