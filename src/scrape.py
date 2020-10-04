import argparse
import sys
import requests
from bs4 import BeautifulSoup
from table_miner import mine


def fetch_doc(url):
    resp = requests.get(url, headers={'User-Agent': 'Custom'})
    if resp.status_code != 200:
        print("GET request failed for ", url)
        sys.exit(2)
    else:
        return BeautifulSoup(resp.text, "html.parser")


def table_rec(url):
    doc = fetch_doc(url)
    tables = doc.find_all("table")
    if not tables:
        iframes = doc.find_all("iframe")
        for iframe in iframes:
            src = iframe['src'] if iframe['src'][0:2] != '//' else "http:"+iframe['src']
            ret = table_rec(src)
            if ret:
                tables.extend(ret)
    return tables


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("url")
    parser.add_argument("sport")
    parser.add_argument("--element_name", choices=['tr', 'table'])

    excl = parser.add_mutually_exclusive_group()
    excl.add_argument('--element_id')
    excl.add_argument('--element_index')
    excl.add_argument('--element_class')

    args = parser.parse_args(sys.argv[1:])

    if args.element_name and args.element_id is None and args.element_index is None and args.element_class is None:
        print('--element_name requires additional arguments')
        sys.exit(1)

    tables = table_rec(args.url)

    if not tables:
        print("Source for scraping not found")
        sys.exit(0)


    print(repr(mine(tables,args)))


if __name__ == "__main__":
    main()
