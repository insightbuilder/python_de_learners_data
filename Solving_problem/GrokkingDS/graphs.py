class Gnode(object):
    def __init__(self, val) -> None:
        self.val = val
        self.left = None
        self.right = None


class Grokraph(object):
    def __init__(self):
        self.head = None

    def connect_dfs(self, val):
        if self.head is None:
            self.head = Gnode(val)
        else:
            stk = [self.head]
            while len(stk) > 0:
                curr = stk.pop(0)
                if curr.right is None:
                    curr.right = Gnode(val)
                    return
                else:
                    stk.insert(0, curr.right)
                
                if curr.left is None:
                    curr.left = Gnode(val)
                    return
                else:
                    stk.insert(0, curr.left)
        return
    
    def print_dfs(self):
        store = ""
        if self.head is None:
            print('empty')
            return
        else:
            stk = [self.head]
            while len(stk) > 0:
                curr = stk.pop(0)
                store += str(curr.val) + ' '
                if curr.right is not None:
                    stk.insert(0, curr.right)
                if curr.left is not None:
                    stk.insert(0, curr.left)
            print(store)
            print(len(store.split(' ')))
        return


ter = 'intogrpaphology'
print(len(ter))
g1 = Grokraph()

for x in ter:
    g1.connect_dfs(x)

g1.print_dfs()