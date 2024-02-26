class Node:
    def __init__(self, val) -> None:
        self.val = val
        self.next = None

    def __str__(self):
        return self.val


class Llist:
    def __init__(self) -> None:
        self.head = None
 
    def appendval(self, val):
        if self.head is None:
            self.head = Node(val)
            return True
        curr = self.head
        while curr.next is not None:
            curr = curr.next
        curr.next = Node(val)
        return True
 
    def print_list(self):
        store = ""
        if self.head is None:
            return 'empty'

        curr = self.head
        while curr.next is not None:
            store += str(curr.val) + ' '
            curr = curr.next

        store += curr.val
        print(store)
        return True


temp = "his wallet"
ll1 = Llist()
print(ll1.print_list())
for c in temp:
    ll1.appendval(c)
ll1.print_list()
