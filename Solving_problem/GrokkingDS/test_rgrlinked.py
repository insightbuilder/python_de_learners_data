from .rgrlinked import Node, Llist


def test_instantiate_node():
    assert Node(val='a')


def test_next_node():
    x = Node(val='a')
    assert not x.next


def test_print_node(capsys):
    x = Node(val='a')
    print(x)
    captures = capsys.readouterr()
    print('looking at captture', captures.out)
    assert captures.out == 'a\n'

def test_instantiate_linkedl():
    assert Llist()


def test_linkedlist_headattr():
    ll = Llist()
    assert not ll.head

def test_llist_appendval():
    ll = Llist()
    assert ll.appendval('a')
