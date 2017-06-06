def read(path):
    with open(path) as f:
        lines = list(f)

    Mesh = nt('Mesh', 'nodes elements boundaries')

    mesh = Mesh([],[],[])
    counts=[]
        
    for line in lines:
        try:
            count,*_=CountLine.unformat(line).fixed
        except AttributeError:
            pass
        else:
            if count>0:
                counts.append(count)
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
            mesh.nodes.append(node)
            continue
            
    mesh_count=Mesh(*counts)