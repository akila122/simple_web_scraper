import argparse
import sys
import requests
from bs4 import BeautifulSoup
from table_miner import mine
import json


def fetch_doc(url):
    resp = requests.get(url, headers={'User-Agent': 'Custom'})
    if resp.status_code != 200:
        print("GET request failed for ", url)
        sys.exit(2)
    else:
        return BeautifulSoup(resp.text, "html.parser")


def table_rec(url, args):
    doc = fetch_doc(url)
    tables = doc.find_all("table")
    if not tables:
        iframes = doc.find_all("iframe")
        for iframe in iframes:
            src = iframe['src'] if iframe['src'][0:2] != '//' \
                else "http:"+iframe['src']
            ret = table_rec(src, args)
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

    print("Searching {} for {} ".format(args.url, args.sport))

    if args.element_name and args.element_id is None \
       and args.element_index is None and args.element_class is None:
        print('--element_name requires additional arguments')
        sys.exit(1)

    tables = table_rec(args.url, args)

    if not tables:
        print("Source for scraping not found")
        sys.exit(0)

    # Filtering tables by index
    elif args.element_index and args.element_name == "table":
        if len(tables) <= int(args.element_index) \
           or int(args.element_index) < 0:
            print(
                "Invalid --element_index {} passed for {} tables"
                .format(args.element_index, len(tables)))
            sys.exit(3)

    print("Total {} tables found in source URL with given options"
          .format(len(tables)))

    data = mine(tables, args)
    results = json.dumps(data, indent=4)

    with open('../results.json', 'w') as out:
        out.write(results)

    print('Total {} results found. Results written to results.json.'
          .format(len(data)))
    print(results)

    sys.exit(0)


if __name__ == "__main__":
    main()
