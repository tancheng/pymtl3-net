#=========================================================================
# DORYTorusRouteUnitCL.py
#=========================================================================
# A DOR route unit with get/give interface for Torus topology in CL.
#
# Author : Cheng Tan
#   Date : May 20, 2019

from pymtl                 import *
from directions            import *
from pclib.ifcs.GuardedIfc import (
  GuardedCallerIfc,
  GuardedCalleeIfc,
  guarded_ifc
)

class DORYTorusRouteUnitCL( Component ):

  def construct( s, 
                 PacketType, 
                 PositionType, 
                 num_outports, 
                 cols=2, 
                 rows=2 ):

    # Constants 
    s.num_outports = num_outports
    s.cols = cols
    s.rows = rows

    # Interface

#    s.get  = GetIfcRTL( PacketType )
#    s.give = [ GiveIfcRTL (PacketType) for _ in range ( s.num_outports ) ]

    s.get  = GuardedCallerIfc()
    s.give = [ GuardedCalleeIfc() for _ in range ( s.num_outports ) ]
    s.pos  = InPort( PositionType )

    # Componets

#    s.out_dir  = Wire( mk_bits( clog2( s.num_outports ) ) )
#    s.give_ens = Wire( mk_bits( s.num_outports ) ) 

    s.rdy_lst = [ False for _ in range( s.num_outports ) ]
    s.msg     = None

    # Connections

    for i in range( s.num_outports ):
#      s.connect( s.get.msg,     s.give[i].msg )
      s.connect( s.give_ens[i], s.give[i].en  )
    
    # Routing logic
    @s.update
    def up_ru_routing():

      if s.msg is None and s.get.rdy():
        s.msg = s.get()
      if s.msg is not None:
        if s.msg.dst == s.pos.pos:
          s.rdy_lst[SELF] = True
        if s.pos.pos_x == s.msg.dst_x and s.pos.pos_y == s.msg.dst_y:
          s.rdy_lst[SELF] = True
        elif s.msg.dst_y < s.pos.pos_y:
          if s.pos.pos_y - s.msg.dst_y <= s.rows - s.pos.pos_y + s.msg.dst_y:
            s.rdy_lst[SOUTH] = True
          else:
            s.rdy_lst[NORTH] = True
        elif s.msg.dst_y > s.pos.pos_y:
          if s.msg.dst_y - s.pos.pos_y <= s.rows - s.msg.dst_y + s.pos.pos_y:
            s.rdy_lst[NORTH] = True
          else:
            s.rdy_lst[SOUTH] = True
        elif s.msg.dst_x < s.pos.pos_x:
          if s.pos.pos_x - s.msg.dst_x <= s.cols - s.pos.pos_x + s.msg.dst_x:
            s.rdy_lst[WEST] = True
          else:
            s.rdy_lst[EAST] = True
        else:
          if s.msg.dst_x - s.pos.pos_x <= s.rows - s.msg.dst_x + s.pos.pos_x:
            s.rdy_lst[EAST] = True
          else:
            s.rdy_lst[WEST] = True
      else:
        s.rdy_lst = [ False for _ in range( s.num_outports ) ]

    # Assign method and ready
    for i in range( s.num_outports ):
      def gen_give_rdy( s, port_id ):
        def give_rdy():
          if s.msg is not None:
            return s.rdy_lst[port_id]
          else:
            return False
        return give_rdy

      s.give[i].rdy.method = gen_give_rdy( s, i )
      s.give[i].method.method = s.give_method

    for i in range( s.num_outports ):
      s.add_constraints(
        M( s.get ) < U( up_ru_route ) < M( s.give[i] ),
      )
 
  def give_method( s ):
    assert s.msg is not None
    ret = s.msg
    s.msg = None
    return ret

   # TODO: CL line trace

  def line_trace( s ):

    out_str = [ "" for _ in range( s.num_outports ) ]
    for i in range (s.num_outports):
      out_str[i] = "{}".format( s.give[i] ) 

    return "{}({}){}".format( s.get, s.out_dir, "|".join( out_str ) )