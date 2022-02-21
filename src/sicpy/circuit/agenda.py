import functools

from ..scheme import *
from ..queue import *

# The agenda
# The only thing needed to complete the simulator is after-delay. The idea here is that we maintain a data structure, called an agenda, that contains a schedule of things to do. The following operations are defined for agendas:
#
# (make-agenda)
# returns a new empty agenda.
# (empty-agenda? <agenda>)
# is true if the specified agenda is empty.
# (first-agenda-item <agenda>)
# returns the first item on the agenda.
# (remove-first-agenda-item! <agenda>)
# modifies the agenda by removing the first item.
# (add-to-agenda! <time> <action> <agenda>)
# modifies the agenda by adding the given action procedure to be run at the specified time.
# (current-time <agenda>)
# returns the current simulation time.
# The particular agenda that we use is denoted by the-agenda. The procedure after-delay adds new elements to the-agenda:
#
# (define (after-delay delay action)
#   (add-to-agenda! (+ delay (current-time the-agenda))
#                   action
#                   the-agenda))
def after_delay(delay, action, agenda=None):
  if agenda is None:
    agenda = the_agenda()
  return add_to_agenda(delay + current_time(agenda),
                       action,
                       agenda)

# The simulation is driven by the procedure propagate, which operates on the-agenda, executing each procedure on the agenda in sequence. In general, as the simulation runs, new items will be added to the agenda, and propagate will continue the simulation as long as there are items on the agenda:
#
# (define (propagate)
#   (if (empty-agenda? the-agenda)
#       'done
#       (let ((first-item (first-agenda-item the-agenda)))
#         (first-item)
#         (remove-first-agenda-item! the-agenda)
#         (propagate))))
def propagate(agenda=None):
  if agenda is None:
    agenda = the_agenda()
  while True:
    if empty_agenda_p(agenda):
      return "done"
    else:
      first_item = first_agenda_item(agenda)
      first_item()
      remove_first_agenda_item(agenda)

# Implementing the agenda
#
# Finally, we give details of the agenda data structure, which holds the procedures that are scheduled for future
# execution.
#
# The agenda is made up of time segments. Each time segment is a pair consisting of a number (the time) and a queue
# (see exercise 3.32) that holds the procedures that are scheduled to be run during that time segment.

# (define (make-time-segment time queue)
#   (cons time queue))
def make_time_segment(time, queue):
  return cons(time, queue)

# (define (segment-time s) (car s))
def segment_time(s):
  return car(s)

# (define (segment-queue s) (cdr s))
def segment_queue(s):
  return cdr(s)

# We will operate on the time-segment queues using the queue operations described in section 3.3.2.
#
# The agenda itself is a one-dimensional table of time segments. It differs from the tables described in section 3.3.3
# in that the segments will be sorted in order of increasing time. In addition, we store the current time (i.e., the
# time of the last action that was processed) at the head of the agenda. A newly constructed agenda has no time
# segments and has a current time of 0:28

# (define (make-agenda) (list 0))
def make_agenda():
  return list(0)

# (define (current-time agenda) (car agenda))
def current_time(agenda):
  return car(agenda)

# (define (set-current-time! agenda time)
#   (set-car! agenda time))
def set_current_time(agenda, time):
  return set_car(agenda, time)

# (define (segments agenda) (cdr agenda))
def segments(agenda):
  return cdr(agenda)

# (define (set-segments! agenda segments)
#   (set-cdr! agenda segments))
def set_segments(agenda, segments):
  return set_cdr(agenda, segments)

# (define (first-segment agenda) (car (segments agenda)))
def first_segment(agenda):
  return car(segments(agenda))

# (define (rest-segments agenda) (cdr (segments agenda)))
def rest_segments(agenda):
  return cdr(segments(agenda))

# An agenda is empty if it has no time segments:
#
# (define (empty-agenda? agenda)
#   (null? (segments agenda)))
def empty_agenda_p(agenda):
  return null(segments(agenda))

# To add an action to an agenda, we first check if the agenda is empty. If so, we create a time segment for the action
# and install this in the agenda. Otherwise, we scan the agenda, examining the time of each segment. If we find a
# segment for our appointed time, we add the action to the associated queue. If we reach a time later than the one to
# which we are appointed, we insert a new time segment into the agenda just before it. If we reach the end of the
# agenda, we must create a new time segment at the end.
#
# (define (add-to-agenda! time action agenda)
#   (define (belongs-before? segments)
#     (or (null? segments)
#         (< time (segment-time (car segments)))))
#   (define (make-new-time-segment time action)
#     (let ((q (make-queue)))
#       (insert-queue! q action)
#       (make-time-segment time q)))
#   (define (add-to-segments! segments)
#     (if (= (segment-time (car segments)) time)
#         (insert-queue! (segment-queue (car segments))
#                        action)
#         (let ((rest (cdr segments)))
#           (if (belongs-before? rest)
#               (set-cdr!
#                segments
#                (cons (make-new-time-segment time action)
#                      (cdr segments)))
#               (add-to-segments! rest)))))
#   (let ((segments (segments agenda)))
#     (if (belongs-before? segments)
#         (set-segments!
#          agenda
#          (cons (make-new-time-segment time action)
#                segments))
#         (add-to-segments! segments))))
def add_to_agenda(time, action, agenda):
  def belongs_before_p(segments):
    return null(segments) or time < segment_time(car(segments))
  def make_new_time_segment(time, action):
    q = make_queue()
    insert_queue(q, action)
    return make_time_segment(time, q)
  def add_to_segments(segments):
    if segment_time(car(segments)) == time:
      insert_queue(segment_queue(car(segments)),
                   action)
    else:
      rest = cdr(segments)
      if belongs_before_p(rest):
        set_cdr(segments, cons(make_new_time_segment(time, action),
                               cdr(segments)))
      else:
        add_to_segments(rest)
  segs = segments(agenda)
  if belongs_before_p(segs):
    set_segments(agenda,
                 cons(make_new_time_segment(time, action),
                      segs))
  else:
    add_to_segments(segs)

# The procedure that removes the first item from the agenda deletes the item at the front of the queue in the first time
# segment. If this deletion makes the time segment empty, we remove it from the list of segments:29
#
# (define (remove-first-agenda-item! agenda)
#   (let ((q (segment-queue (first-segment agenda))))
#     (delete-queue! q)
#     (if (empty-queue? q)
#         (set-segments! agenda (rest-segments agenda)))))
def remove_first_agenda_item(agenda):
  q = segment_queue(first_segment(agenda))
  delete_queue(q)
  if empty_queue_p(q):
    set_segments(agenda, rest_segments(agenda))

# The first agenda item is found at the head of the queue in the first time segment. Whenever we extract an item, we
# also update the current time:30

# (define (first-agenda-item agenda)
#   (if (empty-agenda? agenda)
#       (error "Agenda is empty -- FIRST-AGENDA-ITEM")
#       (let ((first-seg (first-segment agenda)))
#         (set-current-time! agenda (segment-time first-seg))
#         (front-queue (segment-queue first-seg)))))
def first_agenda_item(agenda):
  if empty_agenda_p(agenda):
    return error("Agenda is empty -- FIRST-AGENDA-ITEM")
  else:
    first_seg = first_segment(agenda)
    set_current_time(agenda, segment_time(first_seg))
    return front_queue(segment_queue(first_seg))

# Exercise 3.32.  The procedures to be run during each time segment of the agenda are kept in a queue. Thus, the
# procedures for each segment are called in the order in which they were added to the agenda (first in, first out).
# Explain why this order must be used. In particular, trace the behavior of an and-gate whose inputs change from 0,1 to
# 1,0 in the same segment and say how the behavior would differ if we stored a segment's procedures in an ordinary list,
# adding and removing procedures only at the front (last in, first out).

@functools.lru_cache
def the_agenda():
  return make_agenda()