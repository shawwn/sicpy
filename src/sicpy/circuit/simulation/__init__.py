from ..gates import *

# A sample simulation

# The following procedure, which places a ``probe'' on a wire, shows the simulator in action. The probe tells the wire
# that, whenever its signal changes value, it should print the new signal value, together with the current time and a
# name that identifies the wire:

# (define (probe name wire)
#   (add-action! wire
#                (lambda ()
#                  (newline)
#                  (display name)
#                  (display " ")
#                  (display (current-time the-agenda))
#                  (display "  New-value = ")
#                  (display (get-signal wire)))))
def probe(name, wire):
  def probe_action():
    display(name)
    display(" ")
    display(current_time(the_agenda()))
    display("  New-value = ")
    display(get_signal(wire))
    newline()
  return add_action(wire, probe_action)

