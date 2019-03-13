#=========================================================================
# RouteUnitWithRoutingRTL_test.py
#=========================================================================
# Test for RouteUnitWithRoutingRTL
#
# Author : Cheng Tan, Yanghui Ou
#   Date : Mar 3, 2019

import tempfile
from pymtl                import *
from ocn_pclib.TestVectorSimulator            import TestVectorSimulator
from ocn_pclib.Packet import Packet, mk_pkt
from network.router.RouteUnitRTL  import RouteUnitRTL

from network.routing.RoutingDORX import RoutingDORX
from network.routing.RoutingDORY import RoutingDORY

from ocn_pclib.Position import *

from Configs import configure_network

def run_test( model, test_vectors ):
 
  def tv_in( model, test_vector ):

    pos = MeshPosition( 2, 1, 1)
    model.pos = pos

    pkt = mk_pkt( test_vector[0], test_vector[1], test_vector[2], test_vector[3],
            test_vector[4], test_vector[5])
    model.recv.msg = pkt
    model.recv.rdy = 1
    model.recv.en  = 1
    for i in range( model.num_outports ):
      model.send[i].rdy = 1

  def tv_out( model, test_vector ):
    assert 1 == 1
  
  sim = TestVectorSimulator( model, test_vectors, tv_in, tv_out )
  sim.run_test()
  model.sim_reset()

def test_RouteUnitWithRouting( dump_vcd, test_verilog ):

  configs = configure_network()

  if configs.routing_strategy == 'DORX':
    Routing = RoutingDORX
  elif configs.routing_strategy == 'DORY':
    Routing = RoutingDORY
  else:
    print 'Please specific a valid Routing strategy!'

  routing_strategy = Routing( Packet )
  model = RouteUnitRTL( routing_strategy, MeshPosition )

  model.set_parameter("top.elaborate.num_outports", 5)

  run_test( model, [
    #  src_x  src_y  dst_x  dst_y  opaque  payload  
   [     1,     1,     1,     1,     1,    0xdeadd00d  ],
   [     0,     0,     2,     2,     1,    0xdeadcafe  ],
   [     1,     0,     2,     1,     1,    0xdead0afe  ],
   [     0,     0,     1,     2,     1,    0x00000afe  ],
   [     2,     2,     0,     0,     1,    0x00000afe  ],
  ])