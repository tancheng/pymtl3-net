#=========================================================================
# Torus.py
#=========================================================================
# Initial implementation of Torus topology
#
# Author : Cheng Tan
#   Date : Mar 10, 2019

from pymtl import *
from pclib.ifcs.EnRdyIfc      import InEnRdyIfc, OutEnRdyIfc

from network.LinkUnitRTL          import LinkUnitRTL
from ocn_pclib.Packet             import Packet
from ocn_pclib.Position           import *

from Configs import configure_network

# Manipulate the input and output ports of network.routers to connect each other.
def mk_torus_topology( network ):
  NORTH = 0
  SOUTH = 1
  WEST  = 2
  EAST  = 3
  SELF  = 4
  num_routers = len(network.routers)

  link_index  = 0
  # recv/send_index
  rs_i = len(network.routers)

  for i in range (num_routers):
#    # Connect network.routers together in Mesh
#    if network.routers[i].router_id / network.cols > 0:
#      network.connect( network.routers[i].send[NORTH], 
#              network.links[link_index].recv )
#      network.connect( network.links[link_index].send,      
#              network.routers[network.routers[i].router_id-network.cols].recv[SOUTH] )
#      link_index += 1
#
#    if network.routers[i].router_id / network.cols < network.rows - 1:
#      network.connect( network.routers[i].send[SOUTH], 
#              network.links[link_index].recv )
#      network.connect( network.links[link_index].send,      
#              network.routers[network.routers[i].router_id+network.cols].recv[NORTH] )
#      link_index += 1
#
#    if network.routers[i].router_id % network.cols > 0:
#      network.connect( network.routers[i].send[WEST], 
#              network.links[link_index].recv )
#      network.connect( network.links[link_index].send,   
#              network.routers[network.routers[i].router_id-1].recv[EAST] )
#      link_index += 1
#
#    if network.routers[i].router_id % network.cols < network.cols - 1:
#      network.connect( network.routers[i].send[EAST], 
#              network.links[link_index].recv )
#      network.connect( network.links[link_index].send,   
#              network.routers[network.routers[i].router_id+1].recv[WEST] )
#      link_index += 1

    # Connect the self port (with Network Interface)
    network.connect(network.recv_noc_ifc[i], network.routers[i].recv[SELF])
    network.connect(network.send_noc_ifc[i], network.routers[i].send[SELF])

    # Connect the unused ports
#    if network.routers[i].router_id / network.cols == 0:
#      network.connect( network.routers[i].send[NORTH], network.send[rs_i] )
#      network.connect( network.routers[i].recv[NORTH], network.recv[rs_i] )
#      rs_i += 1
#
#    if network.routers[i].router_id / network.cols == network.rows - 1:
#      network.connect( network.routers[i].send[SOUTH], network.send[rs_i] )
#      network.connect( network.routers[i].recv[SOUTH], network.recv[rs_i] )
#      rs_i += 1
#
#    if network.routers[i].router_id % network.cols == 0:
#      network.connect( network.routers[i].send[WEST], network.send[rs_i] )
#      network.connect( network.routers[i].recv[WEST], network.recv[rs_i] )
#      rs_i += 1
#
#    if network.routers[i].router_id % network.cols == network.cols - 1:
#      network.connect( network.routers[i].send[EAST], network.send[rs_i] )
#      network.connect( network.routers[i].recv[EAST], network.recv[rs_i] )
#      rs_i += 1

    network.connect(network.routers[i].send[NORTH], network.links[link_index].recv)
    network.connect(network.links[link_index].send, network.routers[(network.routers[i].
         router_id-network.rows+network.num_routers)%network.num_routers].recv[SOUTH])
    link_index += 1

    network.connect(network.routers[i].send[SOUTH], network.links[link_index].recv)
    network.connect(network.links[link_index].send, network.routers[(network.routers[i].
         router_id+network.rows+network.num_routers)%network.num_routers].recv[NORTH])
    link_index += 1

    network.connect(network.routers[i].send[WEST],  network.links[link_index].recv)
    network.connect(network.links[link_index].send, network.routers[(network.routers[i].
         router_id-1+network.num_routers)%network.num_routers].recv[EAST])
    link_index += 1

    network.connect(network.routers[i].send[EAST],  network.links[link_index].recv)
    network.connect(network.links[link_index].send, network.routers[(network.routers[i].
         router_id+1+network.num_routers)%network.num_routers].recv[WEST])
    link_index += 1
