"""
==========================================================================
DORYTorusRouteUnitRTL_test.py
==========================================================================
Test for DORYTorusRouteUnitRTL

Author : Yanghui Ou
  Date : June 28, 2019
"""
from itertools import product

import pytest

from ocnlib.ifcs.packets import mk_mesh_pkt
from ocnlib.ifcs.positions import mk_mesh_pos
from ocnlib.test import run_sim
from ocnlib.test.net_sinks import TestNetSinkRTL
from pymtl3 import *
from pymtl3.stdlib.rtl.queues import BypassQueueRTL
from pymtl3.stdlib.test.test_srcs import TestSrcRTL
from torusnet.DORYTorusRouteUnitRTL import DORYTorusRouteUnitRTL
from torusnet.RouteUnitDorFL import RouteUnitDorFL

#-------------------------------------------------------------------------
# TestHarness
#-------------------------------------------------------------------------

class TestHarness( Component ):

  def construct( s, PktType, src_msgs, sink_msgs, ncols=2, nrows=2, pos_x=0, pos_y=0 ):

    outports = 5
    MeshPos = mk_mesh_pos( ncols, nrows )

    match_func = lambda a, b : a.src_x == b.src_x and a.src_y == b.src_y and \
                               a.dst_y == b.dst_y and a.payload == b.payload


    s.src   = TestSrcRTL( PktType, src_msgs )
    s.src_q = BypassQueueRTL( PktType, num_entries=1 )
    s.dut   = DORYTorusRouteUnitRTL( PktType, MeshPos, ncols=ncols, nrows=nrows )
    s.sinks = [ TestNetSinkRTL( PktType, sink_msgs[i], match_func=match_func )
                for i in range ( outports ) ]

    # Connections
    s.src.send  //= s.src_q.enq
    s.src_q.deq //= s.dut.get

    for i in range ( s.dut.num_outports ):
      s.dut.give[i].msg //= s.sinks[i].recv.msg

    @s.update
    def up_give_en():
      for i in range (s.dut.num_outports):
        if s.dut.give[i].rdy and s.sinks[i].recv.rdy:
          s.dut.give[i].en   = b1(1)
          s.sinks[i].recv.en = b1(1)
        else:
          s.dut.give[i].en   = b1(0)
          s.sinks[i].recv.en = b1(0)

    @s.update
    def up_dut_pos():
      s.dut.pos = MeshPos( pos_x, pos_y )

  def done( s ):
    sinks_done = 1
    for i in range( s.dut.num_outports ):
      if not s.sinks[i].done():
        sinks_done = 0
    return s.src.done() and sinks_done

  def line_trace( s ):
    return "{}".format( s.dut.line_trace() )

#-------------------------------------------------------------------------
# mk_dst_pkts
#-------------------------------------------------------------------------
# A helper function that computes destination packets using the FL model.

def mk_dst_pkts( pos_x, pos_y, ncols, nrows, src_pkts ):
  route_unit = RouteUnitDorFL( pos_x, pos_y, ncols, nrows, dimension='y' )
  return route_unit.route( src_pkts )

#=========================================================================
# Test cases
#=========================================================================
# TODO: Test DORX as well.

class RouteUnitDorRTL_Tests:

  @classmethod
  def setup_method( cls ):
    pass

  @pytest.mark.parametrize(
    'pos_x, pos_y',
    product( [ 0, 1, 2, 3 ], [ 0, 1, 2, 3 ] )
  )
  def test_simple_4x4( s, pos_x, pos_y ):

    ncols = 4
    nrows  = 4

    Pkt = mk_mesh_pkt( ncols, nrows, vc=2 )

    src_pkts = [
      #   src_x  y  dst_x  y  opq  vc  payload
      Pkt(    0, 0,     1, 1,   0,  0, 0xfaceb00c ),
      Pkt(    0, 0,     0, 0,   0,  0, 0xdeaddead ),
      Pkt(    0, 0,     1, 0,   0,  0, 0xdeadface ),
      Pkt(    0, 0,     3, 3,   0,  0, 0xdeadface ),
    ]
    dst_pkts = mk_dst_pkts( pos_x, pos_y, ncols, nrows, src_pkts )
    th = TestHarness( Pkt, src_pkts, dst_pkts, ncols, nrows, pos_x, pos_y )
    run_sim( th )
