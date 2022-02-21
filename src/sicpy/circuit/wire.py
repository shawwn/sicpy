from ..scheme import *

# Representing wires

# A wire in our simulation will be a computational object with two local state variables: a signal-value (initially
# taken to be 0) and a collection of action-procedures to be run when the signal changes value. We implement the wire,
# using message-passing style, as a collection of local procedures together with a dispatch procedure that selects the
# appropriate local operation, just as we did with the simple bank-account object in section  3.1.1:

# (define (make-wire)
#   (let ((signal-value 0) (action-procedures '()))
#     (define (set-my-signal! new-value)
#       (if (not (= signal-value new-value))
#           (begin (set! signal-value new-value)
#                  (call-each action-procedures))
#           'done))
#     (define (accept-action-procedure! proc)
#       (set! action-procedures (cons proc action-procedures))
#       (proc))
#     (define (dispatch m)
#       (cond ((eq? m 'get-signal) signal-value)
#             ((eq? m 'set-signal!) set-my-signal!)
#             ((eq? m 'add-action!) accept-action-procedure!)
#             (else (error "Unknown operation -- WIRE" m))))
#     dispatch))

def make_wire():
  signal_value = 0
  action_procedures = list()
  def set_my_signal(new_value):
    nonlocal signal_value
    if signal_value != new_value:
      signal_value = new_value
      return call_each(action_procedures)
    else:
      return "done"
  def accept_action_procedure(proc):
    nonlocal action_procedures
    action_procedures = cons(proc, action_procedures)
    return proc()
  def dispatch(m):
    if m == "get-signal":
      return signal_value
    elif m == "set-signal!":
      return set_my_signal
    elif m == "add-action!":
      return accept_action_procedure
    else:
      return error("Unknown operation -- WIRE", m)
  return dispatch

# The local procedure set-my-signal! tests whether the new signal value changes the signal on the wire. If so, it runs
# each of the action procedures, using the following procedure call-each, which calls each of the items in a list of
# no-argument procedures:

# (define (call-each procedures)
#   (if (null? procedures)
#       'done
#       (begin
#         ((car procedures))
#         (call-each (cdr procedures)))))
def call_each(procedures):
  while True:
    if null(procedures):
      return "done"
    car(procedures)()
    procedures = cdr(procedures)

# The local procedure accept-action-procedure! adds the given procedure to the list of procedures to be run, and then
# runs the new procedure once. (See exercise 3.31.)
#
# With the local dispatch procedure set up as specified, we can provide the following procedures to access the local operations on wires:27
#
# (define (get-signal wire)
#   (wire 'get-signal))
def get_signal(wire):
  return wire("get-signal")

# (define (set-signal! wire new-value)
#   ((wire 'set-signal!) new-value))
def set_signal(wire, new_value):
  return wire("set-signal!")(new_value)

# (define (add-action! wire action-procedure)
#   ((wire 'add-action!) action-procedure))
def add_action(wire, action_procedure):
  return wire("add-action!")(action_procedure)

# Wires, which have time-varying signals and may be incrementally attached to devices, are typical of mutable objects.
# We have modeled them as procedures with local state variables that are modified by assignment. When a new wire is
# created, a new set of state variables is allocated (by the let expression in make-wire) and a new dispatch procedure
# is constructed and returned, capturing the environment with the new state variables.
#
# The wires are shared among the various devices that have been connected to them. Thus, a change made by an interaction
# with one device will affect all the other devices attached to the wire. The wire communicates the change to its
# neighbors by calling the action procedures provided to it when the connections were established.
