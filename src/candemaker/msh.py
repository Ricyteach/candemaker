from collections import namedtuple as nt
from parmatter import unformat_lines
from .msh_parmatters import CountLine, NodeLine, ElementLine, BoundaryLine

Mesh = nt('Mesh', 'nodes elements boundaries')


def read(path, validate=False):
    '''Create a Mesh object from a .msh file'''
    # define which lines are allowed to follow a LineType
    line_rules = {None: (CountLine, NodeLine, ElementLine, BoundaryLine),
                  CountLine: (NodeLine, ElementLine, BoundaryLine, CountLine),
                  NodeLine: (NodeLine, CountLine),
                  ElementLine: (ElementLine, CountLine),
                  BoundaryLine: (BoundaryLine, CountLine)
                  }

    with open(path) as f:
        lines = list(f)

    try:
        unformat_tuple = unformat_lines(lines, line_rules)
    except TypeError as e:
        raise IOError('Failed to successfully read the msh-formatted file: '
                      '{!r}'.format(path.name)) from e

    mesh = Mesh([], [], [])
    counts = []

    # action to be performed for each LineType
    items_actions = {CountLine: lambda items: counts.append(items[0])
                     if items[0] > 0 else None,
                     NodeLine: mesh.nodes.append,
                     ElementLine: mesh.elements.append,
                     BoundaryLine: mesh.boundaries.append
                     }

    for LineType, file_result in zip(*unformat_tuple):
        # skip blank lines
        if file_result is not None:
            items = file_result.fixed
            action = items_actions[LineType]
            action(items)

    mesh_count = Mesh(*counts)

    if validate:
        for name, count, items in zip(('node', 'element', 'boundary'),
                                      mesh_count, mesh):
            if len(items) != count:
                raise ValueError('Mismatched {} count {:d} with {:d} '
                                 'items.'.format(name, count, len(items)))
            if len(items) != items[-1].Num:
                raise ValueError('Numbering sequence for '
                                 '{} items is invalid.'.format(name))
    return mesh
