CANDE Object Creation
=====================

Each line of a CID file is represented by a dictionary, from which is created one or more CANDE objects. Creating a dictionary and object for use in the program requires that the dictionary and object be defined similar to the definition of the corresponding line in the CANDE manual. The definition includes information about: 

1. The CID file prefix
2. The field names
3. The field specifications
3. The field defaults
4. The logic which defines the CID file parsing algorithm. 

This information is stored in the cande_maker registries in the form of CANDE objects for use later. 

We will go through the above items in reverse order. 

Parsing Algorithm
-----------------

The algorithm is implemented using a series of generators. The generator receives and CID container object and a sequence representing the current CID parsing history (empty to begin with for a new parse), and additionally any other atomic objects required to do its job (e.g., the node, or the pipe group material). Each generator should perform any logical checks or logical steps required, and then yield the CANDE object which stores the data for that line of the CID file. Optionally a generator can yield from another generator to direct the next steps of parsing. When a CID section is completed generators simply terminate. 

    def CandeNode_gen(cid_obj, history):
        check(cid_obj, history) #  some logical check
        yield CandeNode

Field Names, Specs, and Defaults
--------------------------------

Each CID line is represented by a dictionary from which is created at least one CANDE object. The dictionary looks like this: 

    cande_node_dict = dict(Num = ObjDef('{: >5d}', 0),
                           X = ObjDef('{: >5d}', 0),
                           Y = ObjDef('{: >5d}', 0)
                           )

A corresponding CANDE object can then created thusly (namedtuple used for convenience):

    CandeNode = collections.namedtuple('CandeNode', 'Num X Y')
    
CID Line Prefix
---------------

The CID line prefix (e.g., 'X-1') is designated like this:

    CandeNode._prefix = 'X-1'

Object Registration
-------------------

The CANDE object is given and name and then finally registered with the program:

    CandeNode._name = 'X1'
    candemaker.cid.register(CandeNode, cande_node_dict, CandeNode_gen)

The _name attribute contains the name of the formatter object to be used when reading and writing lines directly from the CID file (using the parmetters module). Example usage: 

    >>> candemaker.cid_parmatters.X1.format()
                          X-1!!    0    0    0