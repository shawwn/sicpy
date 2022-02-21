from . import *

# We begin by initializing the agenda and specifying delays for the primitive function boxes:
#
# (define the-agenda (make-agenda))
# (define inverter-delay 2)
# (define and-gate-delay 3)
# (define or-gate-delay 5)

# Now we define four wires, placing probes on two of them:

# (define input-1 (make-wire))
input_1 = make_wire()
# (define input-2 (make-wire))
input_2 = make_wire()
# (define sum (make-wire))
sum = make_wire()
# (define carry (make-wire))
carry = make_wire()
# (probe 'sum sum)
probe("sum", sum)
# sum 0  New-value = 0
# (probe 'carry carry)
probe("carry", carry)
# carry 0  New-value = 0

# Next we connect the wires in a half-adder circuit (as in figure 3.25), set the signal on input-1 to 1, and run the
# simulation:

# (half-adder input-1 input-2 sum carry)
# ok
half_adder(input_1, input_2, sum, carry)
# (set-signal! input-1 1)
# done
set_signal(input_1, 1)
# (propagate)
# sum 8  New-value = 1
# done
propagate()

# The sum signal changes to 1 at time 8. We are now eight time units from the beginning of the simulation. At this
# point, we can set the signal on input-2 to 1 and allow the values to propagate:
#
# (set-signal! input-2 1)
# done
set_signal(input_2, 1)
# (propagate)
propagate()
# carry 11  New-value = 1
# sum 16  New-value = 0
# done
#
# The carry changes to 1 at time 11 and the sum changes to 0 at time 16.
#
# Exercise 3.31.   The internal procedure accept-action-procedure! defined in make-wire specifies that when a new action procedure is added to a wire, the procedure is immediately run. Explain why this initialization is necessary. In particular, trace through the half-adder example in the paragraphs above and say how the system's response would differ if we had defined accept-action-procedure! as
#
# (define (accept-action-procedure! proc)
#   (set! action-procedures (cons proc action-procedures)))