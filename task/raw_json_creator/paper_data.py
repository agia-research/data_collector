import re


def get_tags(tag_str):
    tags = []
    raw_tags = tag_str[1:-1].split(',')
    for t in raw_tags:
        if t.startswith("\""):
            result = re.search('"(.*)"', t)
            tags.append(result.group(1).strip())
        else:
            tags.append(t.strip())
    return tags


def create_map(paper, sections):
    obj = {}
    obj['id'] = paper[0]
    obj['title'] = paper[1]
    obj['tags'] = get_tags(paper[2])
    obj['submission_date'] = paper[3].isoformat()

    section_names = []
    generalized_section_names = []
    section_map = {}
    abstract = None
    for i in range(len(sections)):
        s = sections[i]
        if i != 0:
            section_names.append(s[0])
            generalized_section_names.append(s[1])
            section_map[s[0]] = s[2]
        else:
            abstract = s[2]
    obj['abstract'] = abstract
    obj['article'] = section_map
    obj['section_names'] = section_names
    obj['generalized_section_names'] = generalized_section_names
    return obj
