import re


def form_message(res):
    p = ""
    str = ""
    for r in res:

        if r['preview'] != "":
            p = r['preview'] + '\n'
        str += '{}\n{}{}\n{}\n{}\n\n'.format(r['title'], p, re.sub(r'\s+', ' ', r['location']), r['time'], r['ref'])
    return str