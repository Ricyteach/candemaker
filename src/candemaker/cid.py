from collections import namedtuple as nt
from parmatter import unformat_file
from .cid_parmatters import A1, D1, E1
from .L3_parmatters import A2, C1, C2, C3, C4, C5

Mesh = nt('Mesh', 'nodes elements boundaries')

def read(path, validate=False):
    '''Create a Mesh object from a .msh file'''
    # define which lines are allowed to follow a LineType
    line_rules={    None:(A1),
                    A1:(A2),
                    
                    }
                    
    unformat_tuple = unformat_file(path, line_rules)
    
    mesh = Mesh([],[],[])
    counts=[]

    # action to be performed for each LineType
    items_actions={ CountLine: lambda items: counts.append(items[0]) if items[0]>0 else None,
                    NodeLine:mesh.nodes.append,
                    ElementLine:mesh.elements.append,
                    BoundaryLine:mesh.boundaries.append
                    }

    for LineType, file_result in zip(*unformat_tuple):
        # skip blank lines
        if file_result is not None:
            items=file_result.fixed
            action=items_actions[LineType]
            action(items)
                        
    mesh_count=Mesh(*counts)
    
    if validate:
        for name, count, items in zip(('node', 'element', 'boundary'), mesh_count, mesh):
            if len(items)!=count:
                raise ValueError('Mismatched {} count {:d} with {:d} items.'.format(name, count, len(items)))
            if len(items)!=items[-1].Num:
                raise ValueError('Numbering sequence for {} items is invalid.'.format(name))
    
    return mesh