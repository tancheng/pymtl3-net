import sys

import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout, to_agraph
import matplotlib.pyplot as plt

from graphviz import Digraph
import pydot

class DrawGraph( object ):

  def __init__( s ):

    s.edge_pool = []

  def draw_topology( s, routers, channels ):

    edges = []
    color = []
    size = []

    G = nx.Graph()
    G.add_nodes_from( routers  )
    G.add_nodes_from( channels )
 
    for (n1, n2) in s.edge_pool:
      if ( n1._dsl.parent_obj in G.nodes() ) and ( n2._dsl.parent_obj in G.nodes() ):
        edges.append( ( n1._dsl.parent_obj, n2._dsl.parent_obj) )

    G.add_edges_from( edges )
    for i in G.nodes():
      if i in routers:
        color.append( 'r' )
        size.append( 250 )
      else:
        color.append( 'y' )
        size.append( 50 )

#    dot_pos = nx.nx_pydot.pydot_layout(G, prog='dot')
    dot_pos = nx.nx_pydot.graphviz_layout(G)
    nx.draw(G, node_color = color, node_size = size, pos=dot_pos)
    plt.show()
  
  def register_connection( s, node1, node2 ):
    s.edge_pool.append( ( node1, node2 ) )
  
