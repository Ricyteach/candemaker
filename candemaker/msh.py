from collections import namedtuple as nt
from candemaker.msh_parmatters import CountLine, NodeLine, ElementLine, BoundaryLine

Mesh = nt('Mesh', 'nodes elements boundaries')

def read(path, validate=False):
    with open(path) as f:
        lines = list(f)

    mesh = Mesh([],[],[])
    counts=[]
        
    for i,line in enumerate(lines):
        # skip blank lines
        if line.strip():
            try:
                count,*_=CountLine.unformat(line).fixed
                print('\n######\nCOUNT IS: {}'.format(count))
            except AttributeError:
                pass
            else:
                if count>0:
                    counts.append(count)
                    print('\n######\nLINE \n{!r}'.format(line))
                else:
                    print('\n######\nSKIPPED A ZERO AT LINE {}'.format(i+1))
                continue
            try:
                node=NodeLine.unformat(line).fixed
            except AttributeError:
                pass
            else:
                mesh.nodes.append(node)
                continue
            try:
                element=ElementLine.unformat(line).fixed
            except AttributeError:
                pass
            else:
                mesh.elements.append(element)
                continue
            try:
                boundary=BoundaryLine.unformat(line).fixed
            except AttributeError:
                pass
            else:
                mesh.boundaries.append(node)
                continue
            raise TypeError('Error reading {} at line #{:d}:\n\n{!r}"'.format(path.name,i+1,line))

    print('\nMade it to line: ', i+1)
    print('\nCounts:\n', counts)
    print('\nNodes:\n', len(mesh.nodes))
    print('\nElements:\n', len(mesh.elements))
    print('\nBoundaries:\n', len(mesh.boundaries))
    mesh_count=Mesh(*counts)
    
    if validate:
        for name, count, items in zip(('node', 'element', 'boundary'), mesh_count, mesh):
            if len(items)!=count:
                raise ValueError('Mismatched {} count {:d} with {:d} nodes.'.format(name, count, len(items)))
            if len(items)!=items[-1].Num:
                raise ValueError('Numbering sequence for {} items is invalid.'.format(name))
    
    return mesh