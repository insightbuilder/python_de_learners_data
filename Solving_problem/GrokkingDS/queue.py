class QNode:
    def __init__(self, val) -> None:
        self.val = val
        self.next = None


class GroQue(object):
    def __init__(self) -> None:
        self.front = None
        self.back = None
        self.size = 0

    def enqueue(self, val):
        node = QNode(val)
        if self.size == 0:
            self.front = node
            self.back = node
        else:
            self.back.next = node
            self.back = node
        self.size += 1
        return

    def print_by_loop(self):
        if self.size == 0:
            print('empty')
            return
        store = ''
        curr = self.front
        while curr is not None:
            store += str(curr.val) + ' '
            curr = curr.next
        print(store)
        return

    def dequeue(self):
        if self.size == 0:
            print('empty')
        remnode = self.front
        self.front = self.front.next
        print(remnode.val)
        return


q1 = GroQue()
lq = 'eiouafg'

for i in lq:
    q1.enqueue(i)

q1.print_by_loop()
q1.dequeue()
q1.print_by_loop()
q1.dequeue()
q1.print_by_loop()