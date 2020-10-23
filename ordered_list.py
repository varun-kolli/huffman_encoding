class Node:
    '''Node for use with doubly-linked list'''
    def __init__(self, item):
        self.item = item
        self.next = None
        self.prev = None

class OrderedList:
    '''A doubly-linked ordered list of items, from lowest (head of list) to highest (tail of list)'''

    def __init__(self):
        '''Use ONE dummy node as described in class
           ***No other attributes***
           DO NOT have an attribute to keep track of size'''
        self.dummy = Node(None)


    def is_empty(self):
        '''Returns True if OrderedList is empty
            MUST have O(1) performance'''
        return self.dummy.next == None

    def add(self, item):
        '''Adds an item to OrderedList, in the proper location based on ordering of items
           from lowest (at head of list) to highest (at tail of list) and returns True.
           If the item is already in the list, do not add it again and return False.
           MUST have O(n) average-case performance'''
        node = Node(item)
        ref = self.dummy
        while ref is not None:
            if ref.item == item:
                return False
            ref = ref.next

        if self.is_empty(): #empty base case
            node.prev = self.dummy.prev
            self.dummy.next = node
            self.dummy.prev = node
            return True

        elif self.dummy.next.item > node.item: #less
            node.next = self.dummy.next
            node.next.prev = node
            self.dummy.next = node
            return True

        else:
            ref = self.dummy.next
            while ref.next != None and node.item > ref.next.item:
                ref = ref.next

            node.next = ref.next

            if ref.next != None:
                node.next.prev = node

            ref.next = node
            node.prev = ref


            x = self.dummy
            while x.next != None: #this just fixes the tail
                self.dummy.prev = x.next
                x = x.next

            return True

    def remove(self, item): #removes by value not index
        '''Removes the first occurrence of an item from OrderedList. If item is removed (was in the list)
          returns True.  If item was not removed (was not in the list) returns False
           MUST have O(n) average-case performance'''

        if self.is_empty():
            return False

        ref = self.dummy

        if ref.next.item == item: #start
            temp = self.dummy.next.next
            self.dummy.next = temp
            if temp != None:
                temp.prev = self.dummy
            return True

        elif ref.prev.item == item: #end
            while ref.next.item != item:
                ref = ref.next
            self.dummy.prev = ref
            ref.next = None
            return True

        else:
            while ref.next != None:
                if ref.item == item:
                    break
                ref = ref.next

            if ref.next != None:
                ref.prev.next = ref.next
                ref.next.prev = ref.prev

                return True

            else:
                return False

    def index(self, item): #give a value, get an index
        '''Returns index of the first occurrence of an item in OrderedList (assuming head of list is index 0).
           If item is not in list, return None
           MUST have O(n) average-case performance'''
        count = 0
        x = None
        ref = self.dummy.next
        while ref.next != None:
            if ref.item == item:
                x = count
            count += 1
            ref = ref.next

        if self.dummy.prev.item == item:
            x = count

        return x

    def pop(self, index):
        '''Removes and returns item at index (assuming head of list is index 0).
           If index is negative or >= size of list, raises IndexError
           MUST have O(n) average-case performance'''
        size = -1
        ref = self.dummy
        x = []
        while ref is not None:
            size += 1
            x.append(ref.item)
            ref = ref.next

        if index < 0 or index >= size:
            raise IndexError

        else:
            self.remove(x[index + 1])
            return x[index + 1]


    def rec_helper(self, node, item):
        if node == None:
            return False
        elif node.item == item:
            return True
        else:
            return self.rec_helper(node.next, item)

    def search(self, item):
        '''Searches OrderedList for item, returns True if item is in list, False otherwise"
           To practice recursion, this method must call a RECURSIVE method that
           will search the list
           MUST have O(n) average-case performance'''
        return self.rec_helper(self.dummy.next, item)


    def python_list(self):
        '''Return a Python list representation of OrderedList, from head to tail
           For example, list with integers 1, 2, and 3 would return [1, 2, 3]
           MUST have O(n) performance'''
        x = []
        ref = self.dummy
        while ref is not None:
            x.append(ref.item)
            ref = ref.next
        return x[1:]

    def list_helper(self, node, x):
        """
        if node == None:
            return x
        else:
            x.append(node.item)
            return self.list_helper(node.prev, x)
        """
        if not node:
            return x
        else:
            x.append(node.item)
            return self.list_helper(node.prev, x)


    def python_list_reversed(self):
        '''Return a Python list representation of OrderedList, from tail to head, using recursion
           For example, list with integers 1, 2, and 3 would return [3, 2, 1]
           To practice recursion, this method must call a RECURSIVE method that
           will return a reversed list
           MUST have O(n) performance'''
        x = []
        return self.list_helper(self.dummy.prev, x)


    def size_helper(self, node, count):
        if node == None:
            return count
        else:
            return self.size_helper(node.next, count + 1)

    def size(self):
        '''Returns number of items in the OrderedList
           To practice recursion, this method must call a RECURSIVE method that
           will count and return the number of items in the list
           MUST have O(n) performance'''
        count = 0
        return self.size_helper(self.dummy.next, count)

