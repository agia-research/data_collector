import pylatexenc.latexwalker as latexwalker
from pylatexenc.latex2text import LatexNodes2Text
from pylatexenc.latexwalker import LatexWalker

node_parser = LatexNodes2Text()


def get_text_from_body_group(nodes):
    text = ''
    for n in nodes:
        if str(n.__class__) == "<class 'pylatexenc.latexwalker.LatexCharsNode'>":
            try:
                text += node_parser.chars_node_to_text(n)
            except:
                pass
        elif str(n.__class__) == "<class 'pylatexenc.latexwalker.LatexGroupNode'>":
            try:
                text += node_parser.group_node_to_text(n)
            except Exception as e:
                pass
        # elif str(n.__class__) == "<class 'pylatexenc.latexwalker.LatexCommentNode'>":
        #
        elif str(n.__class__) == "<class 'pylatexenc.latexwalker.LatexMacroNode'>":
            try:
                text += node_parser.macro_node_to_text(n)
            except Exception as e:
                pass
        elif str(n.__class__) == "<class 'pylatexenc.latexwalker.LatexEnvironmentNode'>":
            try:
                text += node_parser.environment_node_to_text(n)
            except Exception as e:
                pass
        elif str(n.__class__) == "<class 'pylatexenc.latexwalker.LatexSpecialsNode'>":
            try:
                text += node_parser.specials_node_to_text(n)
            except Exception as e:
                pass
        elif str(n.__class__) == "<class 'pylatexenc.latexwalker.LatexMathNode'>":
            try:
                text += node_parser.math_node_to_text(n)
            except Exception as e:
                pass
    return text


def find_section_name(macro_node):
    name = node_parser.node_to_text(macro_node)
    if name:
        # s = '§ Introduction'
        # s[2:] = 'Introduction'
        return name.strip()[2:].title()
    else:
        return None


def break_sections(section_heads, body_groups):
    section_map = {}
    for i in range(len(section_heads)):
        section_name = find_section_name(section_heads[i])
        if (section_name):
            section_text = get_text_from_body_group(body_groups[i])
            section_map[section_name] = section_text
    return section_map


def get_flat_nodes(nodes):
    node_list = []
    for n in nodes:
        if str(n.__class__) == "<class 'pylatexenc.latexwalker.LatexCharsNode'>":
            node_list.append(n)
        # elif str(n.__class__) == "<class 'pylatexenc.latexwalker.LatexCommentNode'>":
        #     node_list.append(n)
        elif str(n.__class__) == "<class 'pylatexenc.latexwalker.LatexMacroNode'>":
            node_list.append(n)
        elif str(n.__class__) == "<class 'pylatexenc.latexwalker.LatexSpecialsNode'>":
            node_list.append(n)

        elif str(n.__class__) == "<class 'pylatexenc.latexwalker.LatexGroupNode'>":
            node_list += get_flat_nodes(n.nodelist)
        elif str(n.__class__) == "<class 'pylatexenc.latexwalker.LatexEnvironmentNode'>":
            node_list += get_flat_nodes(n.nodelist)
        elif str(n.__class__) == "<class 'pylatexenc.latexwalker.LatexMathNode'>":
            node_list += get_flat_nodes(n.nodelist)
    return node_list


def parse_latex(t):
    LatexWalker
    parsed_latex = LatexWalker(t)

    section_heads = []
    body_groups = []

    section_node_indexes = []

    initial_nodes, pos, len_ = parsed_latex.get_latex_nodes()
    nodes = get_flat_nodes(initial_nodes)
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
