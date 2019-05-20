#=========================================================================
# InputUnitCL.py
#=========================================================================
# Cycle level implementeation of the CL model.
#
# Author : Yanghui Ou
#   Date : May 16, 2019

from pymtl                 import *
from pclib.ifcs.GuardedIfc import GuardedCallerIfc, GuardedCalleeIfc
from pclib.cl.queues       import NormalQueueCL

class InputUnitCL( Component ):

  def construct( s, PacketType, QueueType = NormalQueueCL ):

    # Interface

    s.recv = GuardedCalleeIfc()
    s.give = GuardedCalleeIfc()

    # Component

    s.queue = QueueType( size=2 )
    
    # Connections

    s.connect( s.recv,          s.queue.enq )
    s.connect( s.queue.deq,     s.give      )

  def line_trace( s ):
    return s.queue.line_trace()