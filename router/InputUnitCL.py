"""
==========================================================================
InputUnitCL.py
==========================================================================
Cycle level implementeation of the CL model.

Author : Yanghui Ou
  Date : May 16, 2019
"""
from pymtl3 import *
from pymtl3.stdlib.cl.queues import NormalQueueCL


class InputUnitCL( Component ):

  def construct( s, PacketType, QueueType=NormalQueueCL ):

    # Interface

    s.recv = NonBlockingCalleeIfc( PacketType )
    s.give = NonBlockingCalleeIfc( PacketType )

    # Component

    s.queue = QueueType( num_entries=2 )( enq = s.recv, deq = s.give )

  def line_trace( s ):
    return f"{s.recv}(){s.give}"
