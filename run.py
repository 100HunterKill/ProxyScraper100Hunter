import argparse
import subprocess

def run_scraper_and_checker(protocol):
    # Construye el comando para ejecutar proxy_scraper.py
    scraper_command = [
        'python3', 'proxy_scraper.py', '-p', protocol, '-o', f'proxies-{protocol}.txt', '-v'
    ]
    
    # Ejecuta el comando del scraper
    subprocess.run(scraper_command, check=True)

    # Construye el comando para ejecutar proxy_checker.py
    checker_command = [
        'python3', 'proxy_checker.py', '-p', protocol, '-l', f'proxies-{protocol}.txt', '-o', f'list-{protocol}.txt', '-v'
    ]

    # Ejecuta el comando del checker
    subprocess.run(checker_command, check=True)

def main():
    parser = argparse.ArgumentParser(description="Run proxy scraper and checker")
    parser.add_argument(
        '-p', '--protocol',
        help="Protocol to use for proxies (http, socks4, socks5)",
        choices=['http', 'socks4', 'socks5'],
        required=True
    )
    
    args = parser.parse_args()
    
    print(f"Running proxy scraper and checker for protocol: {args.protocol}")
    run_scraper_and_checker(args.protocol)

if __name__ == "__main__":
    main()
