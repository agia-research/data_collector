import pylatexenc.latexwalker as latexwalker
from pylatexenc.latexwalker import LatexWalker


def get_text_from_body_group(body_group):
    text = ""
    for node in body_group:
        if str(node.__class__) == "<class 'pylatexenc.latexwalker.LatexCharsNode'>":
            text += node.chars
    return text


def find_section_name(macro_node):
    if (str(macro_node.nodeargd.argnlist[2].__class__) == "<class 'pylatexenc.latexwalker.LatexGroupNode'>"):
        nodes = macro_node.nodeargd.argnlist[2].nodelist
        for n in nodes:
            if str(n.__class__) == "<class 'pylatexenc.latexwalker.LatexCharsNode'>":
                return n.chars
    return None


def break_sections(section_heads, body_groups):
    section_map = {}
    for i in range(len(section_heads)):
        section_name = find_section_name(section_heads[i])
        if (section_name):
            section_text = get_text_from_body_group(body_groups[i])
            section_map[section_name] = section_text
    return section_map


def get_flat_nodes(nodes, collected=[]):
    for n in nodes:
        if str(n.__class__) == "<class 'pylatexenc.latexwalker.LatexCharsNode'>":
            collected.append(n)
        elif str(n.__class__) == "<class 'pylatexenc.latexwalker.LatexGroupNode'>":
            collected.append(get_flat_nodes(n.nodelist, collected))
        elif str(n.__class__) == "<class 'pylatexenc.latexwalker.LatexCommentNode'>":
            collected.append(n)
        elif str(n.__class__) == "<class 'pylatexenc.latexwalker.LatexMacroNode'>":
            collected.append(n)
        elif str(n.__class__) == "<class 'pylatexenc.latexwalker.LatexEnvironmentNode'>":
            collected.append(get_flat_nodes(n.nodelist, collected))
        elif str(n.__class__) == "<class 'pylatexenc.latexwalker.LatexSpecialsNode'>":
            collected.append(n)
        elif str(n.__class__) == "<class 'pylatexenc.latexwalker.LatexMathNode'>":
            collected.append(get_flat_nodes(n.nodelist, collected))
    return collected


def parse_latex(t):
    LatexWalker
    parsed_latex = LatexWalker(t)

    section_heads = []
    body_groups = []

    section_node_indexes = []

    intial_nodes, pos, len_ = parsed_latex.get_latex_nodes()
    nodes = get_flat_nodes(intial_nodes, [])
    for i in range(len(nodes)):
        node = nodes[i]
        if isinstance(node, latexwalker.LatexMacroNode):
            if node.macroname == 'section':
                section_node_indexes.append(i)
                section_heads.append(node)

    num_of_nodes = len(nodes)
    num_of_sections = len(section_node_indexes)
    for i in range(num_of_sections):
        group_start_index = section_node_indexes[i] + 1
        if (i + 1 < num_of_sections):
            group_end_index_upper_bound = section_node_indexes[i + 1]
        else:
            group_end_index_upper_bound = num_of_nodes
        body_groups.append(nodes[group_start_index:group_end_index_upper_bound])
    return break_sections(section_heads, body_groups)
    # return section_heads,body_groups
