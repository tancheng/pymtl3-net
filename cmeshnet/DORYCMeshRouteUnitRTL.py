#=========================================================================
# DORYRouteUnitRTL.py
#=========================================================================
# A DOR-Y route unit with get/give interface for CMesh.
#
# Author : Yanghui Ou, Cheng Tan
#   Date : Mar 25, 2019

from pymtl      import *
from pclib.ifcs import GetIfcRTL, GiveIfcRTL
from Direction  import *

class DORYCMeshRouteUnitRTL( Component ):

  def construct( s, PacketType, PositionType, num_outports = 5 ):

    # Constants 

    s.num_outports = num_outports

    # Interface

    s.get  = GetIfcRTL( PacketType )
    s.give = [ GiveIfcRTL (PacketType) for _ in range ( s.num_outports ) ]
    s.pos  = InPort( PositionType )

    # Componets

    s.out_dir  = Wire( mk_bits( clog2( s.num_outports ) ) )
    s.give_ens = Wire( mk_bits( s.num_outports ) ) 

    # Connections

    for i in range( s.num_outports ):
      s.connect( s.get.msg,     s.give[i].msg )
      s.connect( s.give_ens[i], s.give[i].en  )
    
    # Routing logic
    @s.update
    def up_ru_routing():
 
      s.out_dir = 0
      for i in range( s.num_outports ):
        s.give[i].rdy = 0

      if s.get.rdy:
        if s.pos.pos_x == s.get.msg.dst_x and s.pos.pos_y == s.get.msg.dst_y:
          s.out_dir = Bits3(4) + s.get.msg.dst_terminal
        elif s.get.msg.dst_y < s.pos.pos_y:
          s.out_dir = NORTH
        elif s.get.msg.dst_y > s.pos.pos_y:
          s.out_dir = SOUTH
        elif s.get.msg.dst_x < s.pos.pos_x:
          s.out_dir = WEST
        else:
          s.out_dir = EAST
        s.give[ s.out_dir ].rdy = 1

    @s.update
    def up_ru_get_en():
      s.get.en = s.give_ens > 0 

  # Line trace
  def line_trace( s ):

    out_str = [ "" for _ in range( s.num_outports ) ]
    for i in range (s.num_outports):
      out_str[i] = "{}".format( s.give[i] ) 

    return "{}({}){}".format( s.get, s.out_dir, "|".join( out_str ) )