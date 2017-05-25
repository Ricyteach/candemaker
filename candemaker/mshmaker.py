from candemaker.linemaker import LineMakerBase

class CountLine(LineMakerBase):
    Num = 0, dict(type='d')
        
class NodeLine(LineMakerBase):
    __sep__ = (' ', '\t')
    Num = 0, dict(type='d')
    x = 1, dict(type='f')
    y = 2, dict(type='f')
    
class ElementLine(LineMakerBase):
    __sep__ = (' ', '\t')
    Num = 0, dict(type='d')
    I = 1, dict(type='d')
    J = 2, dict(type='d')
    K = 3, dict(type='d')
    L = 4, dict(type='d')
    
class BoundaryLine(LineMakerBase):
    __sep__ = (' ', '\t')
    Num = 0, dict(type='d')
    Node = 1, dict(type='d')
