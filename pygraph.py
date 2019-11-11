
#import copy
#th2.additem(copy.deepcopy(ni))

import pickle
from collections import deque

class node(object):

  def __init__(self, id):
    self.id = id
    self.flag = False

  def flagnode(self):
    self.flag = True

  def unflagnode(self):
    self.flag = False

  def isflagged(self):
    return self.flag

class astarnode(object):

  def __init__(self, n=None, p=None, csf=0, etc=0):
    self.node = n
    self.parent = p
    self.csf = csf
    self.etc = etc

  def __eq__(self, other):
    return (self.node.id == other.node.id)

class edge(object):

  def __init__(self, n1, n2, w):
    self.node1 = n1
    self.node2 = n2
    self.weight = w

class edgelite(object):
  
  def __init__(self, n, w):
    self.node = n
    self.weight = w
    
class graph(object):

  def __init__(self, d):
    self.directed = d
    self.nodes = []
    self.edges = []

  def debug(self):

    for x in range(1, 12):
      self.addnode(x)

    self.addedge(1, 2, 5);
    self.addedge(1, 3, 10);
    self.addedge(2, 4, 15);
    self.addedge(3, 5, 15);
    self.addedge(3, 8, 5);
    self.addedge(4, 5, 25);
    self.addedge(4, 6, 10);
    self.addedge(4, 7, 30);
    self.addedge(5, 2, 20);
    self.addedge(5, 7, 10);
    self.addedge(6, 9, 5);
    self.addedge(6, 11, 15);
    self.addedge(7, 10, 15);
    self.addedge(8, 5, 15);
    self.addedge(8, 10, 20);
    self.addedge(9, 7, 15);
    self.addedge(9, 11, 20);
    self.addedge(10, 11, 40);

    #self.dfs(1)
    #self.bfs(1)
    
    thepath = self.astar(1, 11)

    for p in thepath:
      print(p)
    
  def clear(self):
    self.directed = False
    self.nodes = []
    self.edges = []

  def clean(self):
    for n in self.nodes:
      n.unflagnode()

  def load(self, fn):
    self.clear()
    try:
      fh = open(fn, "rb")
      self.edges = pickle.load(fh)
      self.nodes = pickle.load(fh)
      self.directed = pickle.load(fh)
      fh.close()
    except IOError:
      return

  def save(self, fn):
    try:
      fh = open(fn, "wb")
      pickle.dump(self.directed, fh)
      pickle.dump(self.nodes, fh)
      pickle.dump(self.edges, fh)
      fh.close()
    except IOError:
      return

  def addnode(self, id):
    if not self.hasnode(id):
      self.nodes.append(node(id))

  def remnode(self, id):
    c=0
    for n in self.nodes:
      if n.id == id:
        self.nodes.pop(c)
      c += 1

  def hasnode(self, id):
    for n in self.nodes:
      if n.id == id:
        return True
    return False

  def addedge(self, id1, id2, w):

    n1 = self.findnode(id1)
    n2 = self.findnode(id2)

    if n1 == None or n2 == None:
      return

    if not self.hasedge(id1, id2):
      self.edges.append(edge(n1, n2, w))

    if not self.directed:
      if not self.hasedge(id2, id1):
        self.edges.append(edge(n2, n1, w))

  def remedge(self, id1, id2):

    c=0
    if not self.directed:

      for e in self.edges:
        if (e.node1.id == id1 and e.node2.id == id2) or (e.node2.id == id1 and e.node1.id == id2):
          self.edges.pop(c)
        c += 1

    else:

      for e in self.edges:
        if e.node1.id == id1 and e.node2.id == id2:
          self.edges.pop(c)
        c += 1

  def hasedge(self, id1, id2):
    for e in self.edges:
      if e.node1.id == id1 and e.node2.id == id2:
        return True
    return False

  def findnode(self, id):
    for n in self.nodes:
      if n.id == id:
        return n
    return None

  def getneighbors(self, node):
    rlist = []
    for e in self.edges:
      if e.node1.id == node.id:
        rlist.append(edgelite(e.node2, e.weight))
    return rlist

  def dfs(self, id):

    entry = self.findnode(id)
    if entry == None:
      return

    self.clean()
    entry.flagnode()
    nlist = []
    nlist.append(entry)
    current = None

    while len(nlist) > 0:
      current = nlist.pop()
      print("%d" % current.id)
      nbors = self.getneighbors(current)
      for n in nbors:
        if not n.node.isflagged():
          n.node.flagnode()
          nlist.append(n.node)
    
  def bfs(self, id):

    entry = self.findnode(id)
    if entry == None:
      return
    
    self.clean()
    entry.flagnode()
    nlist = deque()
    nlist.append(entry)
    current = None

    while len(nlist) > 0:
      current = nlist.popleft()
      print("%d" % current.id)
      nbors = self.getneighbors(current)
      for n in nbors:
        if not n.node.isflagged():
          n.node.flagnode()
          nlist.append(n.node)

  def astar(self, start, goal):

    a_open = []
    a_closed = []
    a_allrecords = []
    a_nbors = []
    a_path = []

    a_start = self.findnode(start)
    a_end = self.findnode(goal)

    if a_start == None or a_end == None:
      return None

    an1 = astarnode(a_start, None, 0, self.astar_estimate(a_start, a_end))
    a_allrecords.append(an1)
    a_current = None
    a_open.append(an1)

    while len(a_open) > 0:

      a_current = self.astarnode_getsmallest(a_open)
      if a_current.node.id == a_end.id: # goal reached
        break
    
      a_nbors = self.getneighbors(a_current.node)
      for nb in a_nbors:
        endnode = nb.node
        endnodecost = a_current.csf + nb.weight
    
        endnoderecord = None
        endnodeheuristic = self.astar_estimate(endnode, a_end)
    
        if self.astarnode_contains(endnode, a_closed):
          endnoderecord = self.astarnode_find(endnode, a_closed)
          if (endnoderecord.csf <= endnodecost):
            continue
          astarnode_pop(endnoderecord, a_closed)
        elif self.astarnode_contains(endnode, a_open):
          endnoderecord = self.astarnode_find(endnode, a_open)
          if (endnoderecord.csf <= endnodecost):
            continue
        else:
          endnoderecord = astarnode(endnode)

        endnoderecord.csf = endnodecost
        endnoderecord.parent = a_current
        endnoderecord.etc = endnodecost + endnodeheuristic

        if not self.astarnode_contains(endnode, a_open):
          a_open.append(endnoderecord)

      self.astarnode_pop(a_current, a_open)
      a_closed.append(a_current)

    # build up path, if found
    if a_current.node.id != a_end.id:
      print("path not found")
    else:
      dummy = a_current
      while (dummy.node.id  != a_start.id):
        a_path.append(dummy.node.id)
        dummy = dummy.parent
      a_path.append(a_start.id)

    a_path.reverse()
    return a_path

  # custom heuristics implementation goes here
  def astar_estimate(self, node, goal):
    return 1

  def astarnode_getsmallest(self, q):

    min = q[0]
    for a in q:
      #if (q[i]->estimated_total_cost < min->estimated_total_cost)
      if a.etc < min.etc:
        min = a

    return min

  def astarnode_pop(self, asn, q):

    c = 0
    for a in q:
      if asn == a:
        q.pop(c)
      c += 1

  def astarnode_contains(self, n, q):

    for a in q:
      if a.node.id == n.id:
        return True

    return False

  def astarnode_find(self, n, q):

    for a in q:
      if a.node.id == n.id:
        return a
  
    return a # incorrect usage
