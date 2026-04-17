

class DynamicArray:
    """Simulates a dynamic array (like Python list) with manual resizing."""

    def __init__(self, capacity=2):
        self._capacity = capacity
        self._size = 0
        self._data = [None] * self._capacity

    def _resize(self, new_capacity):
        """Internal: doubles capacity and copies elements."""
        new_data = [None] * new_capacity
        for i in range(self._size):
            new_data[i] = self._data[i]
        self._data = new_data
        self._capacity = new_capacity
        print(f"  [RESIZE] Capacity doubled → new capacity = {self._capacity}")

    def append(self, x):
        """Append element; resize if full (amortized O(1))."""
        if self._size == self._capacity:
            self._resize(2 * self._capacity)
        self._data[self._size] = x
        self._size += 1

    def pop(self):
        """Remove and return last element (O(1))."""
        if self._size == 0:
            raise IndexError("pop from empty array")
        val = self._data[self._size - 1]
        self._data[self._size - 1] = None
        self._size -= 1
        return val

    def __str__(self):
        elements = [str(self._data[i]) for i in range(self._size)]
        return f"[{', '.join(elements)}]  (size={self._size}, capacity={self._capacity})"


# TASK 2A: Singly Linked List

class SLLNode:
    def __init__(self, data):
        self.data = data
        self.next = None


class SinglyLinkedList:
    def __init__(self):
        self.head = None

    def insert_at_beginning(self, x):
        node = SLLNode(x)
        node.next = self.head
        self.head = node

    def insert_at_end(self, x):
        node = SLLNode(x)
        if self.head is None:
            self.head = node
            return
        curr = self.head
        while curr.next:
            curr = curr.next
        curr.next = node

    def delete_by_value(self, x):
        if self.head is None:
            print(f"  [WARN] List is empty, cannot delete {x}")
            return
        if self.head.data == x:
            self.head = self.head.next
            return
        curr = self.head
        while curr.next:
            if curr.next.data == x:
                curr.next = curr.next.next
                return
            curr = curr.next
        print(f"  [WARN] Value {x} not found in list")

    def traverse(self):
        elements = []
        curr = self.head
        while curr:
            elements.append(str(curr.data))
            curr = curr.next
        print("SLL: " + " -> ".join(elements) if elements else "SLL: (empty)")

    def get_head_node(self):
        return self.head


# TASK 2B: Doubly Linked List

class DLLNode:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def insert_at_beginning(self, x):
        node = DLLNode(x)
        if self.head is None:
            self.head = self.tail = node
        else:
            node.next = self.head
            self.head.prev = node
            self.head = node

    def insert_at_end(self, x):
        node = DLLNode(x)
        if self.tail is None:
            self.head = self.tail = node
        else:
            node.prev = self.tail
            self.tail.next = node
            self.tail = node

    def insert_after_node(self, target, x):
        """Insert x after first occurrence of target value."""
        curr = self.head
        while curr:
            if curr.data == target:
                node = DLLNode(x)
                node.prev = curr
                node.next = curr.next
                if curr.next:
                    curr.next.prev = node
                else:
                    self.tail = node
                curr.next = node
                return
            curr = curr.next
        print(f"  [WARN] Target {target} not found")

    def delete_at_position(self, pos):
        """Delete node at 0-based position."""
        if self.head is None:
            print("  [WARN] List is empty")
            return
        curr = self.head
        idx = 0
        while curr and idx < pos:
            curr = curr.next
            idx += 1
        if curr is None:
            print(f"  [WARN] Position {pos} out of range")
            return
        if curr.prev:
            curr.prev.next = curr.next
        else:
            self.head = curr.next
        if curr.next:
            curr.next.prev = curr.prev
        else:
            self.tail = curr.prev

    def traverse(self):
        elements = []
        curr = self.head
        while curr:
            elements.append(str(curr.data))
            curr = curr.next
        print("DLL: " + " <-> ".join(elements) if elements else "DLL: (empty)")


# TASK 3A: Stack ADT using Singly Linked List

class Stack:
    """LIFO Stack built on SinglyLinkedList. Push/pop at head → O(1)."""

    def __init__(self):
        self._sll = SinglyLinkedList()
        self._size = 0

    def push(self, x):
        self._sll.insert_at_beginning(x)
        self._size += 1

    def pop(self):
        if self.is_empty():
            raise IndexError("Stack underflow: pop from empty stack")
        val = self._sll.head.data
        self._sll.head = self._sll.head.next
        self._size -= 1
        return val

    def peek(self):
        if self.is_empty():
            raise IndexError("Stack underflow: peek on empty stack")
        return self._sll.head.data

    def is_empty(self):
        return self._size == 0

    def __str__(self):
        elements = []
        curr = self._sll.head
        while curr:
            elements.append(str(curr.data))
            curr = curr.next
        return "Stack (top→bottom): " + " | ".join(elements) if elements else "Stack: (empty)"


# TASK 3B: Queue ADT using Singly Linked List

class Queue:
    """FIFO Queue built on SinglyLinkedList. Uses head+tail for O(1) ops."""

    def __init__(self):
        self._head = None   # dequeue end (front)
        self._tail = None   # enqueue end (rear)
        self._size = 0

    def enqueue(self, x):
        node = SLLNode(x)
        if self._tail is None:
            self._head = self._tail = node
        else:
            self._tail.next = node
            self._tail = node
        self._size += 1

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Queue underflow: dequeue from empty queue")
        val = self._head.data
        self._head = self._head.next
        if self._head is None:
            self._tail = None
        self._size -= 1
        return val

    def front(self):
        if self.is_empty():
            raise IndexError("Queue underflow: front on empty queue")
        return self._head.data

    def is_empty(self):
        return self._size == 0

    def __str__(self):
        elements = []
        curr = self._head
        while curr:
            elements.append(str(curr.data))
            curr = curr.next
        return "Queue (front→rear): " + " -> ".join(elements) if elements else "Queue: (empty)"


# TASK 4: Balanced Parentheses Checker

def is_balanced(expr):
    """Returns True if brackets in expr are balanced, False otherwise."""
    stack = Stack()
    matching = {')': '(', '}': '{', ']': '['}
    opening = set('({[')
    closing = set(')}]')

    for ch in expr:
        if ch in opening:
            stack.push(ch)
        elif ch in closing:
            if stack.is_empty() or stack.peek() != matching[ch]:
                return False
            stack.pop()

    return stack.is_empty()


# MAIN RUNNER – All Test Cases

def separator(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def run_task1():
    separator("TASK 1: Dynamic Array Simulation")

    da = DynamicArray(capacity=2)
    print(f"\nInitial: {da}")

    print("\nAppending 12 elements (capacity starts at 2):")
    for i in range(1, 13):
        da.append(i * 10)
        print(f"  append({i*10}) → {da}")

    print("\nPopping 3 elements:")
    for _ in range(3):
        val = da.pop()
        print(f"  pop() returned {val} → {da}")


def run_task2():
    separator("TASK 2A: Singly Linked List")

    sll = SinglyLinkedList()
    print("\nInsert 3 elements at beginning (10, 20, 30):")
    for v in [10, 20, 30]:
        sll.insert_at_beginning(v)
        sll.traverse()

    print("\nInsert 3 elements at end (40, 50, 60):")
    for v in [40, 50, 60]:
        sll.insert_at_end(v)
        sll.traverse()

    print("\nDelete by value 20:")
    sll.delete_by_value(20)
    sll.traverse()

    print("\nDelete by value 60 (last element):")
    sll.delete_by_value(60)
    sll.traverse()

    print("\nDelete by value 99 (not in list):")
    sll.delete_by_value(99)
    sll.traverse()

    # ---- Doubly Linked List ----
    separator("TASK 2B: Doubly Linked List")

    dll = DoublyLinkedList()
    print("\nBuild DLL: insert at end → 10, 20, 30, 40, 50")
    for v in [10, 20, 30, 40, 50]:
        dll.insert_at_end(v)
    dll.traverse()

    print("\nInsert 99 after node with value 30:")
    dll.insert_after_node(30, 99)
    dll.traverse()

    print("\nDelete at position 1 (0-based → removes 20):")
    dll.delete_at_position(1)
    dll.traverse()

    print("\nDelete at position 0 (head):")
    dll.delete_at_position(0)
    dll.traverse()

    print("\nDelete at last position (index 3 → removes 50):")
    dll.delete_at_position(3)
    dll.traverse()


def run_task3():
    separator("TASK 3A: Stack ADT (LIFO)")

    stack = Stack()
    print("\nPush 10, 20, 30, 40:")
    for v in [10, 20, 30, 40]:
        stack.push(v)
        print(f"  push({v}) → {stack}")

    print(f"\nPeek (top element): {stack.peek()}")

    print("\nPop 2 elements:")
    for _ in range(2):
        val = stack.pop()
        print(f"  pop() returned {val} → {stack}")

    print("\nTest underflow on empty stack:")
    stack2 = Stack()
    try:
        stack2.pop()
    except IndexError as e:
        print(f"  Exception caught: {e}")

    # ---- Queue ----
    separator("TASK 3B: Queue ADT (FIFO)")

    queue = Queue()
    print("\nEnqueue A, B, C, D, E:")
    for v in ['A', 'B', 'C', 'D', 'E']:
        queue.enqueue(v)
        print(f"  enqueue({v}) → {queue}")

    print(f"\nFront element: {queue.front()}")

    print("\nDequeue 3 elements:")
    for _ in range(3):
        val = queue.dequeue()
        print(f"  dequeue() returned {val} → {queue}")

    print("\nTest underflow on empty queue:")
    queue2 = Queue()
    try:
        queue2.dequeue()
    except IndexError as e:
        print(f"  Exception caught: {e}")


def run_task4():
    separator("TASK 4: Balanced Parentheses Checker")

    test_cases = [
        ("([])",   True,  "Balanced"),
        ("([)]",   False, "Not balanced"),
        ("(((", False, "Not balanced"),
        ("",       True,  "Balanced (empty string)"),
        ("{[()]}",True,  "Balanced"),
        ("({[}])", False, "Not balanced"),
        ("((()))", True,  "Balanced"),
        ("]",      False, "Not balanced"),
    ]

    print(f"\n{'Expression':<15} {'Expected':<15} {'Got':<10} {'Pass?'}")
    print("-" * 55)
    for expr, expected, label in test_cases:
        result = is_balanced(expr)
        status = "✓ PASS" if result == expected else "✗ FAIL"
        display = repr(expr) if expr == "" else expr
        print(f"{display:<15} {label:<15} {str(result):<10} {status}")


if __name__ == "__main__":
    run_task1()
    run_task2()
    run_task3()
    run_task4()
    print("\n" + "=" * 60)
    print("  All test cases completed.")
