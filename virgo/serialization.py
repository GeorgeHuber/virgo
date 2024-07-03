from virgo import graph

def serialize_out(out: graph.Output, inList, nodes):
        state = {
            "description": out.description,
            "parent": nodes.index(out.node),
            "edges": [inList.index(x) for x in out.edges]
        }
        return state

def serialize_in(inp: graph.Input, outList, nodes):
        state = {
            "description": inp.description,
            "parent": nodes.index(inp.node),
            "edges": [outList.index(x) for x in inp.edges]
        }
        return state

def serialize_node(n: graph.Node, inList, outList):
    state = n.get_state()
    state["ins"] = [inList.index(x) for x in n.ins]
    state["outs"] = [outList.index(x) for x in n.outs]
    return state

def serialize_nodes(nodes):
    nodeData = []
    inList = []
    outList = []
    inData, outData = [], []
    for node in nodes:
        inList.extend(node.ins)
        outList.extend(node.outs)
    for node in nodes:
        nodeData.append(serialize_node(node, inList, outList))
    for x in inList:
         inData.append(serialize_in(x, outList, nodes))
    for x in outList:
         outData.append(serialize_out(x, inList, nodes))
         
    return inData, outData, nodeData
