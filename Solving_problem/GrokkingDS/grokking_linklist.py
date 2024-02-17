def linkedlist():
    import streamlit as st
    expandall = st.checkbox("Show Code")
    st.markdown("Grinding Linked List")
    with st.expander(label="LNode:",
                     expanded=expandall):
        st.code(body="""class Lnode:
        def __init__(self, val):
            self.val = val
            self.next = None""")
    with st.expander(label="LinkedList Init:",
                     expanded=expandall):
        st.code(body="""
class LinkedList(object):
    def __init__(self):
        self.head = None""")
    with st.expander(label="Append-loop",
                     expanded=expandall):
        st.code(body="""
    def append_by_loop(self, val):
        if self.head is None:
            self.head = Lnode(val)
            return
        curr = self.head
        while curr.next is not None:
            curr = curr.next
        curr.next = Lnode(val)
        return""")
    with st.expander(label="Print-loop",
                     expanded=expandall):
        st.code(body="""
        def print_by_loop(self):
        store = ""
        if self.head is None:
            print('empty')
            return

        curr = self.head
        while curr.next is not None:
            store += str(curr.val) + ' '
            curr = curr.next
        store += str(curr.val)
        print(store)
        return""")
    with st.expander(label="Contains",
                     expanded=expandall):
        st.code("""def contains_by_loop(self, val):
        if self.head is None:
            print(False)
            return
        curr = self.head
        while curr.next is not None:
            if curr.val == val:
                print(True)
                return
            curr = curr.next
        print(False)
        return""")

    with st.expander(label="Delete-loop",
                     expanded=expandall):
        st.code("""def delete_by_loop(self, val):
        if self.head is None:
            return
        if self.head.val == val:
            del_node = self.head
            self.head = self.head.next
            print(del_node.val)
            return

        prev = self.head
        curr = None

        while prev.next is not None:
            curr = prev.next
            if curr.val == val:
                prev.next = curr.next
                return
            prev = curr
        return""")

    with st.expander(label="Testing",
                     expanded=True):
        st.code("""ll1 = LinkedList()
lst = 'supernod'
ll1.print_by_loop()
for x in lst:
    ll1.append_by_loop(x)

ll1.print_by_loop()
ll1.contains_by_loop('u')
ll1.contains_by_loop('p')
ll1.delete_by_loop('s')
ll1.print_by_loop()
ll1.delete_by_loop('p')
ll1.print_by_loop()""")