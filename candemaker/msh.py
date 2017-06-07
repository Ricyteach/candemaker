from collections import namedtuple as nt
from candemaker.msh_parmatters import CountLine, NodeLine, ElementLine, BoundaryLine

Mesh = nt('Mesh', 'nodes elements boundaries')
UnformatFile = nt('UnformatFile', 'struct result')

def unformat_file(path, line_rules):
    '''Builds the LineType sequence and LineType.unformat result for a file
    line_rules: defines valid LineType succession. a dict of the form:
        parse.compile obj: (parse.compile obj, parse.compile obj, ...)
        use None for the first line
    raises TypeError if an invalid line sequence is encountered'''
    with open(path) as f:
        lines = list(f)
        
    file_struct=[]
    file_items=[]

    for i,line in enumerate(lines):
        # skip blank lines
        if line.strip():
            try:
                PrevType=file_struct[-1]
            except IndexError:
                # first line
                PrevType=None
            for LineType in line_rules[PrevType]:
                unformat=LineType.unformat(line)
                if unformat is None:
                    # format not matched
                    continue
                else:
                    file_items.append(unformat)
                    file_struct.append(LineType)
                    break
                raise TypeError('Failed to read {} at line #{:d}:\n{!r}"'.format(path.name,i+1,line))
        else:
            file_items.append(None)
            file_struct.append(None)
            
    assert len(file_struct)==len(file_items)
    return UnformatFile(file_struct, file_items)

def read(path, validate=False):
    '''Create a Mesh object from a .msh file'''
    # define which lines are allowed to follow a LineType
    line_rules={    None:(CountLine,NodeLine,ElementLine,BoundaryLine),
                    CountLine:(NodeLine,ElementLine,BoundaryLine,CountLine),
                    NodeLine:(NodeLine,CountLine),
                    ElementLine:(ElementLine,CountLine),
                    BoundaryLine:(BoundaryLine,CountLine)
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