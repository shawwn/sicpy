from .scheme import *

# 3.3.2  Representing Queues
# The mutators set-car! and set-cdr! enable us to use pairs to construct data structures that cannot be built with cons, car, and cdr alone. This section shows how to use pairs to represent a data structure called a queue. Section 3.3.3 will show how to represent data structures called tables.
#
# A queue is a sequence in which items are inserted at one end (called the rear of the queue) and deleted from the other end (the front). Figure 3.18 shows an initially empty queue in which the items a and b are inserted. Then a is removed, c and d are inserted, and b is removed. Because items are always removed in the order in which they are inserted, a queue is sometimes called a FIFO (first in, first out) buffer.
#
#
# Operation	Resulting Queue
# (define q (make-queue))
# (insert-queue! q 'a)	a
# (insert-queue! q 'b)	a b
# (delete-queue! q)	b
# (insert-queue! q 'c)	b c
# (insert-queue! q 'd)	b c d
# (delete-queue! q)	c d
# Figure 3.18:  Queue operations.
# In terms of data abstraction, we can regard a queue as defined by the following set of operations:
#
# a constructor:
# (make-queue)
# returns an empty queue (a queue containing no items).
# two selectors:
# (empty-queue? <queue>)
# tests if the queue is empty.
# (front-queue <queue>)
# returns the object at the front of the queue, signaling an error if the queue is empty; it does not modify the queue.
# two mutators:
# (insert-queue! <queue> <item>)
# inserts the item at the rear of the queue and returns the modified queue as its value.
# (delete-queue! <queue>)
# removes the item at the front of the queue and returns the modified queue as its value, signaling an error if the queue is empty before the deletion.
# Because a queue is a sequence of items, we could certainly represent it as an ordinary list; the front of the queue would be the car of the list, inserting an item in the queue would amount to appending a new element at the end of the list, and deleting an item from the queue would just be taking the cdr of the list. However, this representation is inefficient, because in order to insert an item we must scan the list until we reach the end. Since the only method we have for scanning a list is by successive cdr operations, this scanning requires (n) steps for a list of n items. A simple modification to the list representation overcomes this disadvantage by allowing the queue operations to be implemented so that they require (1) steps; that is, so that the number of steps needed is independent of the length of the queue.
#
# The difficulty with the list representation arises from the need to scan to find the end of the list. The reason we need to scan is that, although the standard way of representing a list as a chain of pairs readily provides us with a pointer to the beginning of the list, it gives us no easily accessible pointer to the end. The modification that avoids the drawback is to represent the queue as a list, together with an additional pointer that indicates the final pair in the list. That way, when we go to insert an item, we can consult the rear pointer and so avoid scanning the list.
#
# A queue is represented, then, as a pair of pointers, front-ptr and rear-ptr, which indicate, respectively, the first and last pairs in an ordinary list. Since we would like the queue to be an identifiable object, we can use cons to combine the two pointers. Thus, the queue itself will be the cons of the two pointers. Figure 3.19 illustrates this representation.
#
#
#
# Figure 3.19:  Implementation of a queue as a list with front and rear pointers.

# To define the queue operations we use the following procedures, which enable us to select and to modify the front and rear pointers of a queue:
#
# (define (front-ptr queue) (car queue))
def front_ptr(queue):
  return car(queue)
# (define (rear-ptr queue) (cdr queue))
def rear_ptr(queue):
  return cdr(queue)
# (define (set-front-ptr! queue item) (set-car! queue item))
def set_front_ptr(queue, item):
  set_car(queue, item)
# (define (set-rear-ptr! queue item) (set-cdr! queue item))
def set_rear_ptr(queue, item):
  set_cdr(queue, item)

# Now we can implement the actual queue operations. We will consider a queue to be empty if its front pointer is the empty list:
#
# (define (empty-queue? queue) (null? (front-ptr queue)))
def empty_queue_p(queue):
  return null(front_ptr(queue))

# The make-queue constructor returns, as an initially empty queue, a pair whose car and cdr are both the empty list:
#
# (define (make-queue) (cons '() '()))
def make_queue():
  return cons(list(), list())

# To select the item at the front of the queue, we return the car of the pair indicated by the front pointer:
#
# (define (front-queue queue)
#   (if (empty-queue? queue)
#       (error "FRONT called with an empty queue" queue)
#       (car (front-ptr queue))))
def front_queue(queue):
  if empty_queue_p(queue):
    return error("FRONT called with an empty queue", queue)
  else:
    return car(front_ptr(queue))

# To insert an item in a queue, we follow the method whose result is indicated in figure 3.20. We first create a new pair whose car is the item to be inserted and whose cdr is the empty list. If the queue was initially empty, we set the front and rear pointers of the queue to this new pair. Otherwise, we modify the final pair in the queue to point to the new pair, and also set the rear pointer to the new pair.
#
#
#
# Figure 3.20:  Result of using (insert-queue! q 'd) on the queue of figure 3.19.
# (define (insert-queue! queue item)
#   (let ((new-pair (cons item '())))
#     (cond ((empty-queue? queue)
#            (set-front-ptr! queue new-pair)
#            (set-rear-ptr! queue new-pair)
#            queue)
#           (else
#            (set-cdr! (rear-ptr queue) new-pair)
#            (set-rear-ptr! queue new-pair)
#            queue))))
def insert_queue(queue, item):
  new_pair = cons(item, list())
  if empty_queue_p(queue):
    set_front_ptr(queue, new_pair)
    set_rear_ptr(queue, new_pair)
    return queue
  else:
    set_cdr(rear_ptr(queue), new_pair)
    set_rear_ptr(queue, new_pair)
    return queue

# To delete the item at the front of the queue, we merely modify the front pointer so that it now points at the second item in the queue, which can be found by following the cdr pointer of the first item (see figure 3.21):22
#
#
#
# Figure 3.21:  Result of using (delete-queue! q) on the queue of figure 3.20.
# (define (delete-queue! queue)
#   (cond ((empty-queue? queue)
#          (error "DELETE! called with an empty queue" queue))
#         (else
#          (set-front-ptr! queue (cdr (front-ptr queue)))
#          queue)))
def delete_queue(queue):
  if empty_queue_p(queue):
    return error("DELETE! called with an empty queue", queue)
  else:
    set_front_ptr(queue, cdr(front_ptr(queue)))
    return queue

# Exercise 3.21.  Ben Bitdiddle decides to test the queue implementation described above. He types in the procedures to the Lisp interpreter and proceeds to try them out:
#
# (define q1 (make-queue))
# (insert-queue! q1 'a)
# ((a) a)
# (insert-queue! q1 'b)
# ((a b) b)
# (delete-queue! q1)
# ((b) b)
# (delete-queue! q1)
# (() b)
def ex_3_21():
  q1 = make_queue()
  insert_queue(q1, "a")
  assert repr(q1) == "((a) a)"
  insert_queue(q1, "b")
  assert repr(q1) == "((a b) b)"
  delete_queue(q1)
  assert repr(q1) == "((b) b)"
  delete_queue(q1)
  assert repr(q1) == "(() b)"
  return q1

ex_3_21()

# ``It's all wrong!'' he complains. ``The interpreter's response shows that the last item is inserted into the queue twice. And when I delete both items, the second b is still there, so the queue isn't empty, even though it's supposed to be.'' Eva Lu Ator suggests that Ben has misunderstood what is happening. ``It's not that the items are going into the queue twice,'' she explains. ``It's just that the standard Lisp printer doesn't know how to make sense of the queue representation. If you want to see the queue printed correctly, you'll have to define your own print procedure for queues.'' Explain what Eva Lu is talking about. In particular, show why Ben's examples produce the printed results that they do. Define a procedure print-queue that takes a queue as input and prints the sequence of items in the queue.
#
# Exercise 3.22.  Instead of representing a queue as a pair of pointers, we can build a queue as a procedure with local state. The local state will consist of pointers to the beginning and the end of an ordinary list. Thus, the make-queue procedure will have the form
#
# (define (make-queue)
#   (let ((front-ptr ...)
#         (rear-ptr ...))
#     <definitions of internal procedures>
#     (define (dispatch m) ...)
#     dispatch))
#
# Complete the definition of make-queue and provide implementations of the queue operations using this representation.
#
# Exercise 3.23.  A deque (``double-ended queue'') is a sequence in which items can be inserted and deleted at either the front or the rear. Operations on deques are the constructor make-deque, the predicate empty-deque?, selectors front-deque and rear-deque, and mutators front-insert-deque!, rear-insert-deque!, front-delete-deque!, and rear-delete-deque!. Show how to represent deques using pairs, and give implementations of the operations.23 All operations should be accomplished in (1) steps.