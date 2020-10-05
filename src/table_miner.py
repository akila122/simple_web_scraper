
import sys
import re


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
            if len(cols) == 1 and next(cols[0].stripped_strings).lower().replace(" ", "") == sport.lower().replace(" ", ""):
                start = tr
                for sibling in tr.find_next_siblings():
                    if len(sibling.find_all(re.compile("^t[dh]"))) == 1:
                        end = sibling
                        break
                return {'start': start, 'end': end}
    else:
        marker = table.find("tr")['class'][0]
        for s in table.find("tr").stripped_strings:
            if re.search("@", s):
                suff = s[1:]
                break

        for tr in table.find_all("tr", class_=marker):
            if tr.find('td').string.lower().replace(" ", "") == sport.lower().replace(" ", ""):
                start = tr
                end = start.find_next_sibling(class_=marker)
                return {'start': start, 'end': end, 'suff': suff}


def fetch_data(delim, args):
    sport = args.sport
    ret = []
    start = delim['start']
    end = delim['end']
    index = -1
    indexFound = False

    for tr in start.find_next_siblings():
        index = index + 1
        if tr == end:
            break

        # Filtering rows
        if args.element_name == "tr":
            if args.element_index:
                if index != int(args.element_index):
                    continue
                else:
                    indexFound = True
            if args.element_class:
                if not (tr.has_attr('class') and args.element_class in tr['class']):
                    continue
            if args.element_id:
                if not (tr.has_attr('id') and tr['id'] == args.element_class):
                    continue

        data = {"sport": sport.lower(), "name": "",
                "position": "", "phone": "", "email": ""}
        i = 0

        for val in tr.stripped_strings:
            if i == 0:
                data['name'] = val
            elif i == 1:
                data['position'] = val
            else:
                if re.search("\d+-\d+", val):
                    data['phone'] = val
                elif re.search("@", val):
                    data['email'] = val.lower() + \
                        (delim['suff'] if 'suff' in delim else '')

            i = i + 1
        ret.append(data)
        index = index + 1
        if indexFound:
            break
    return ret


def mine(tables, args):
    ret = []
    index = 0
    for table in tables:
        index = index + 1

        # Filtering tables
        if args.element_name == "table":
            if args.element_index:
                if index != int(args.element_idex):
                    continue
            if args.element_class:
                if not (table.has_attr('class') and args.element_class in table['class'] ):
                    continue
            if args.element_id:
                if not (table.has_attr('id') and table['id'][0] == args.element_id):
                    continue

        delim = None
        try:
            delim = find_sport(table, args.sport)
        except:
            delim = None
        if delim:
            ret.extend(fetch_data(delim, args))

    return ret
