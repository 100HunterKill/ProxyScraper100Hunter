import argparse
import asyncio
import aiohttp

async def check_proxy(session, proxy, timeout):
    try:
        async with session.get('http://httpbin.org/ip', proxy=f'socks5://{proxy}', timeout=timeout) as response:
            if response.status == 200:
                return proxy
    except Exception as e:
        pass
    return None

async def main(list_file, output_file, protocol, timeout, verbose):
    timeout = aiohttp.ClientTimeout(total=timeout)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        with open(list_file, 'r') as f:
            proxies = f.read().splitlines()

        tasks = []
        for proxy in proxies:
            tasks.append(check_proxy(session, proxy, timeout))

        valid_proxies = await asyncio.gather(*tasks)
        valid_proxies = [proxy for proxy in valid_proxies if proxy is not None]

        if verbose:
            print(f"Valid proxies: {len(valid_proxies)}")

        with open(output_file, 'w') as f:
            f.write('\n'.join(valid_proxies))

        print(f"Proxies have been written to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Proxy Checker")
    parser.add_argument(
        "-l", "--list",
        help="Input file containing list of proxies",
        required=True
    )
    parser.add_argument(
        "-o", "--output",
        help="Output file to save valid proxies",
        required=True
    )
    parser.add_argument(
        "-p", "--protocol",
        help="Protocol of proxies (http, socks4, socks5)",
        choices=["http", "socks4", "socks5"],
        required=True
    )
    parser.add_argument(
        "-t", "--timeout",
        help="Timeout in seconds for each request",
        type=int,
        default=10
    )
    parser.add_argument(
        "-v", "--verbose",
        help="Increase output verbosity",
        action="store_true"
    )

    args = parser.parse_args()

    asyncio.run(main(args.list, args.output, args.protocol, args.timeout, args.verbose))
