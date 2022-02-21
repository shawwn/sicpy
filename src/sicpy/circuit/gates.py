from .wire import *
from .agenda import *
from .constants import *

# We can connect primitive functions together to construct more complex functions. To accomplish this we wire the outputs of some function boxes to the inputs of other function boxes. For example, the half-adder circuit shown in figure 3.25 consists of an or-gate, two and-gates, and an inverter. It takes two input signals, A and B, and has two output signals, S and C. S will become 1 whenever precisely one of A and B is 1, and C will become 1 whenever A and B are both 1. We can see from the figure that, because of the delays involved, the outputs may be generated at different times. Many of the difficulties in the design of digital circuits arise from this fact.
#
#
#
# Figure 3.25:  A half-adder circuit.
# We will now build a program for modeling the digital logic circuits we wish to study. The program will construct computational objects modeling the wires, which will ``hold'' the signals. Function boxes will be modeled by procedures that enforce the correct relationships among the signals.
#
# One basic element of our simulation will be a procedure make-wire, which constructs wires. For example, we can construct six wires as follows:
#
# (define a (make-wire))
# (define b (make-wire))
# (define c (make-wire))
#
# (define d (make-wire))
# (define e (make-wire))
# (define s (make-wire))
#
# We attach a function box to a set of wires by calling a procedure that constructs that kind of box. The arguments to the constructor procedure are the wires to be attached to the box. For example, given that we can construct and-gates, or-gates, and inverters, we can wire together the half-adder shown in figure 3.25:
#
# (or-gate a b d)
# ok
#
# (and-gate a b c)
# ok
#
# (inverter c e)
# ok
#
# (and-gate d e s)
# ok
#
# Better yet, we can explicitly name this operation by defining a procedure half-adder that constructs this circuit, given the four external wires to be attached to the half-adder:
#
# (define (half-adder a b s c)
#   (let ((d (make-wire)) (e (make-wire)))
#     (or-gate a b d)
#     (and-gate a b c)
#     (inverter c e)
#     (and-gate d e s)
#     'ok))
def half_adder(a, b, s, c):
  d = make_wire()
  e = make_wire()
  or_gate(a, b, d)
  and_gate(a, b, c)
  inverter(c, e)
  and_gate(d, e, s)
  return "ok"

# The advantage of making this definition is that we can use half-adder itself as a building block in creating more complex circuits. Figure 3.26, for example, shows a full-adder composed of two half-adders and an or-gate.26 We can construct a full-adder as follows:
#
# (define (full-adder a b c-in sum c-out)
#   (let ((s (make-wire))
#         (c1 (make-wire))
#         (c2 (make-wire)))
#     (half-adder b c-in s c1)
#     (half-adder a s sum c2)
#     (or-gate c1 c2 c-out)
#     'ok))
def full_adder(a, b, c_in, sum, c_out):
  s = make_wire()
  c1 = make_wire()
  c2 = make_wire()
  half_adder(b, c_in, s, c1)
  half_adder(a, s, sum, c2)
  or_gate(c1, c2, c_out)
  return "ok"

# Having defined full-adder as a procedure, we can now use it as a building block for creating still more complex circuits. (For example, see exercise 3.30.)
#
#
#
# Figure 3.26:  A full-adder circuit.
#
# In essence, our simulator provides us with the tools to construct a language of circuits. If we adopt the general perspective on languages with which we approached the study of Lisp in section 1.1, we can say that the primitive function boxes form the primitive elements of the language, that wiring boxes together provides a means of combination, and that specifying wiring patterns as procedures serves as a means of abstraction.

# Primitive function boxes

# The primitive function boxes implement the ``forces'' by which a change in the signal on one wire influences the signals on other wires. To build function boxes, we use the following operations on wires:

# - (get-signal <wire>)
# returns the current value of the signal on the wire.

# - (set-signal! <wire> <new value>)
# changes the value of the signal on the wire to the new value.

# - (add-action! <wire> <procedure of no arguments>)
# asserts that the designated procedure should be run whenever the signal on the wire changes value. Such procedures are the vehicles by which changes in the signal value on the wire are communicated to other wires.

# In addition, we will make use of a procedure after-delay that takes a time delay and a procedure to be run and executes the given procedure after the given delay.

# Using these procedures, we can define the primitive digital logic functions. To connect an input to an output through an inverter, we use add-action! to associate with the input wire a procedure that will be run whenever the signal on the input wire changes value. The procedure computes the logical-not of the input signal, and then, after one inverter-delay, sets the output signal to be this new value:

# (define (inverter input output)
#   (define (invert-input)
#     (let ((new-value (logical-not (get-signal input))))
#       (after-delay inverter-delay
#                    (lambda ()
#                      (set-signal! output new-value)))))
#   (add-action! input invert-input)
#   'ok)
def inverter(input, output):
  def invert_input():
    new_value = logical_not(get_signal(input))
    return after_delay(inverter_delay(), lambda: set_signal(output, new_value))
  add_action(input, invert_input)
  return "ok"

# (define (logical-not s)
#   (cond ((= s 0) 1)
#         ((= s 1) 0)
#         (else (error "Invalid signal" s))))
def logical_not(s):
  if s == 0:
    return 1
  elif s == 1:
    return 0
  else:
    return error("Invalid signal", s)

# An and-gate is a little more complex. The action procedure must be run if either of the inputs to the gate changes. It
# computes the logical-and (using a procedure analogous to logical-not) of the values of the signals on the input wires
# and sets up a change to the new value to occur on the output wire after one and-gate-delay.

# (define (and-gate a1 a2 output)
#   (define (and-action-procedure)
#     (let ((new-value
#            (logical-and (get-signal a1) (get-signal a2))))
#       (after-delay and-gate-delay
#                    (lambda ()
#                      (set-signal! output new-value)))))
#   (add-action! a1 and-action-procedure)
#   (add-action! a2 and-action-procedure)
#   'ok)
def and_gate(a1, a2, output):
  def and_action_procedure():
    new_value = logical_and(get_signal(a1), get_signal(a2))
    return after_delay(and_gate_delay(), lambda: set_signal(output, new_value))
  add_action(a1, and_action_procedure)
  add_action(a2, and_action_procedure)
  return "ok"

def logical_and(a, b):
  return a & b

# Exercise 3.28.  Define an or-gate as a primitive function box. Your or-gate constructor should be similar to and-gate.
def or_gate(a1, a2, output):
  def or_action_procedure():
    new_value = logical_or(get_signal(a1), get_signal(a2))
    return after_delay(or_gate_delay(), lambda: set_signal(output, new_value))
  add_action(a1, or_action_procedure)
  add_action(a2, or_action_procedure)
  return "ok"

def logical_or(a, b):
  return a | b

# Exercise 3.29.  Another way to construct an or-gate is as a compound digital logic device, built from and-gates and
# inverters. Define a procedure or-gate that accomplishes this. What is the delay time of the or-gate in terms of
# and-gate-delay and inverter-delay?
