import numpy as np


def remove_newcommand_lines_and_comments(text):
    substring = '\\newcommand'
    lines = text.split('\n')
    updated_text = []

    for line in lines:
        if (substring not in line) and (line.strip().startswith('%')):
            updated_text.append(line)

    return '\n'.join(updated_text)


def get_indices(text, substring):
    indices = []
    start_index = 0
    while True:
        index = text.find(substring, start_index)
        if index == -1:
            break
        indices.append(index)
        start_index = index + len(substring)
    return indices


def get_table_indices(text):
    its = get_indices(text, "egin{table")
    its = list(np.array(its) - 2)

    ite = get_indices(text, "end{table")
    ite = list(np.array(ite) + 10)
    indexes = list(zip(its, ite))
    return indexes


def get_figure_indices(text):
    its = get_indices(text, "egin{figure")
    its = list(np.array(its) - 2)

    ite = get_indices(text, "end{figure")
    ite = list(np.array(ite) + 11)
    indexes = list(zip(its, ite))
    return indexes


def remove_text_by_indices(original_text, start_index, end_index):
    if start_index < 0 or end_index > len(original_text) or start_index > end_index:
        return original_text

    modified_text = original_text[:start_index] + original_text[end_index:]

    return modified_text, end_index - start_index


def remove_figures_and_tables(input_text):
    input_text = remove_newcommand_lines_and_comments(
        input_text)  # removing comments and new commands since it interefere with table and figure search

    indices = get_table_indices(input_text)
    indices += get_figure_indices(input_text)
    t = input_text
    diff = 0
    indices.sort(key=lambda x: x[0])
    for x in indices:
        t, d = remove_text_by_indices(t, x[0] - diff, x[1] - diff)
        diff += d
    return t
