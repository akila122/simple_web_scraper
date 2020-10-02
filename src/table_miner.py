
import sys
import re

# Add support for <tr>


def filter_tables(_tables, args):
    if args.element_name == "table":
        if args.element_index:
            if len(_tables) <= int(args.element_index):
                print("Table index is under range")
                return None
            else:
                return [_tables[int(args.element_index)]]
        elif args.element_id:
            return _tables.find_all(id=args.element_id)
        elif args.element_class:
            return _tables.find_all(class_=args.element_class)


def find_sport(table, sport):
    single = False
    start = None
    end = None
    for tr in table.find_all("tr"):
        if len(tr.find_all(re.compile("^t[dh]"))) == 1:
            single = True
            break
    if single:
        for tr in table.find_all("tr"):
            cols = tr.find_all(re.compile("^t[dh]"))
            if len(cols) == 1 and next(cols[0].stripped_strings).lower() == sport.lower():
                start = tr
                for sibling in tr.find_next_siblings():
                    if len(sibling.find_all(re.compile("^t[dh]"))) == 1:
                        end = sibling
                        break
                return {'start': start, 'end': end}
    else:
        marker = table.find("tr")['class'][0]
        for tr in table.find_all("tr",class_=marker):
            if tr.find('td').string.lower() == sport.lower():
                start = tr
                end = tr.find_next_sibling("tr",class_=marker)
                return {'start': start, 'end': end}


def mine(tables, args):
    # tables = filter_tables(tables)
    delim = find_sport(tables[0], args.sport)
    print(repr(delim['start']))
    print(repr(delim['end']))
