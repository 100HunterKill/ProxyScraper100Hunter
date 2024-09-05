import argparse
import asyncio
import httpx
import time
from typing import List

# Importar las clases de scrapers
from scrapers import SpysMeScraper, ProxyScrapeScraper, GeoNodeScraper, ProxyListDownloadScraper, GeneralTableScraper, GeneralDivScraper, GitHubScraper

# Lista de scrapers disponibles
def get_scrapers(protocol: str):
    scrapers = []
    if protocol == "http":
        scrapers.extend([
            SpysMeScraper("http"),
            ProxyScrapeScraper("http"),
            GeoNodeScraper("http"),
            ProxyListDownloadScraper("http", "elite"),
            ProxyListDownloadScraper("http", "transparent"),
            ProxyListDownloadScraper("http", "anonymous"),
            GeneralTableScraper("http", "http://sslproxies.org"),
            GeneralTableScraper("http", "http://free-proxy-list.net"),
            GeneralTableScraper("http", "http://us-proxy.org"),
            GitHubScraper("http", "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/all/data.txt"),
            GitHubScraper("http", "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/all.txt"),
            GitHubScraper("http", "https://raw.githubusercontent.com/zloi-user/hideip.me/main/http.txt")
        ])
    elif protocol == "socks4":
        scrapers.extend([
            ProxyScrapeScraper("socks4"),
            GeoNodeScraper("socks4"),
            ProxyListDownloadScraper("socks", "elite"),
            GeneralTableScraper("socks", "http://socks-proxy.net"),
            GitHubScraper("socks4", "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/all/data.txt"),
            GitHubScraper("socks4", "https://raw.githubusercontent.com/zloi-user/hideip.me/main/socks4.txt")
        ])
    elif protocol == "socks5":
        scrapers.extend([
            ProxyScrapeScraper("socks5"),
            GeoNodeScraper("socks5"),
            ProxyListDownloadScraper("socks", "elite"),
            GeneralTableScraper("socks", "http://socks-proxy.net"),
            GitHubScraper("socks5", "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/all/data.txt"),
            GitHubScraper("socks5", "https://raw.githubusercontent.com/zloi-user/hideip.me/main/socks5.txt")
        ])
    return scrapers

async def scrape(output: str, protocol: str, verbose: bool):
    now = time.time()
    verbose_print(verbose, "Scraping proxies...")
    proxies = []

    tasks = []
    client = httpx.AsyncClient(follow_redirects=True)

    scrapers = get_scrapers(protocol)

    async def scrape_scraper(scraper):
        try:
            proxies.extend(await scraper.scrape(client))
        except Exception as e:
            verbose_print(verbose, f"Error while scraping {scraper.get_url()}: {e}")

    for scraper in scrapers:
        tasks.append(asyncio.ensure_future(scrape_scraper(scraper)))

    await asyncio.gather(*tasks)
    await client.aclose()

    proxies = set(proxies)
    verbose_print(verbose, f"Writing {len(proxies)} proxies to file...")
    with open(output, "w") as f:
        f.write("\n".join(proxies))
    verbose_print(verbose, "Done!")
    verbose_print(verbose, f"Took {time.time() - now} seconds")

def verbose_print(verbose: bool, message: str):
    if verbose:
        print(message)

def main():
    parser = argparse.ArgumentParser(description="Proxy Scraper")
    parser.add_argument(
        "-p",
        "--protocol",
        help="Protocol to scrape (http, socks4, socks5)",
        choices=["http", "socks4", "socks5"],
        required=True
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Output file name to save .txt file",
        default="output.txt",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="Increase output verbosity",
        action="store_true",
    )
    args = parser.parse_args()

    asyncio.run(scrape(args.output, args.protocol, args.verbose))

if __name__ == "__main__":
    main()
