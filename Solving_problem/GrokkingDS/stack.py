class SNode(object):
    def __init__(self, val) -> None:
        self.val = val
        self.next = None


class GrokStak(object):
    def __init__(self) -> None:
        self.top = None
        self.size = 0

    def push(self, val):
        node = SNode(val) 
        if self.size == 0:
            self.top = node
        else:
            node.next = self.top
            self.top = node
        self.size += 1
        return
    
    def get_top(self):
        if self.size == 0:
            print('empty')
            return
        print(self.top.val)
        return

    def pop(self):
        if self.size == 0:
            return
        popnode = self.top
        self.top = self.top.next
        self.size -= 1
        print(popnode.val)
        return

    def print_by_loop(self):
        if self.size == 0:
            print('empty')
            return
        curr = self.top
        store = ""
        while curr.next is not None:
            store += str(curr.val) + ' '
            curr = curr.next
        print(store)
        return


tk = 'efqrztu'
stk1 = GrokStak()

for x in tk:
    stk1.push(x)

stk1.get_top()
stk1.print_by_loop()
stk1.pop()
stk1.print_by_loop()