class Stack:
    def __init__(self):
        self.ds = []

    def push(self, el):
        self.ds.append(el)

    def pop(self):
        self.ds.pop()

    def peek(self):
        return self.ds[-1]

    def is_empty(self):
        if len(self.ds) == 0:
            return True
        else:
            return False

new_st = Stack()


print(new_st.is_empty())
new_st.push(0)
new_st.push(1)
new_st.push(2)
new_st.push(3)
new_st.push(4)
print(new_st.pop())
print(new_st.pop())
print(new_st.peek())
print(new_st.pop())
print(new_st.is_empty())
