import re

def biodata(html):
    div = html.find("div", class_="bio-info")

    regex = r"\w*>([\w*\s*\/]+)"
    matches = re.finditer(regex, str(div), re.MULTILINE)

    bio = []

    for matchNum, match in enumerate(matches, start=0):
        value = match.group(1)
        if value.strip() != "":
            bio.append(value.rstrip())
            #print(match.group(1))

    remove = [2, 4, 6, 8, 10]

    bio = [x for i,x in enumerate(bio) if i not in remove]

    return bio

def jadwal(html):
    table = html.find("tr", class_="textWhite")

    table = table.previous_element.previous_element

    regex = r"<[td\s*\w*\=\"]*>([\&\;\w*\s*\:*-\.]*)"
    matches = re.finditer(regex, str(table), re.MULTILINE)

    jdwl = []

    for matchNum, match in enumerate(matches, start=0):
        value = match.group(1)
        value = value.replace("&amp;", "&")
        if value.strip() != "":
            jdwl.append(value.strip())

    remove = [0, 1, 2, 3, 4, 5, 6, 7, 8]

    jdwl = [x for i,x in enumerate(jdwl) if i not in remove]

    return jdwl
