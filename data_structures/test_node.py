class Node:
    def __init__(self, val=None, next=None) -> None:
        self.val = val
        self.next = next

    def append(self, head, val):
        new = Node(val)
        while head and head.next:
            head = head.next
        head.next = new

    def display(self, head):
        result = []
        curr = head
        while curr:
            
            if curr.val is not None:
                result.append(curr.val)
            curr = curr.next
        return result
    
    def delete(self, head, val):
        if head is None:
            return []
        if head.val == val:
            head = head.next
            return head
        curr = head
        while curr.next:            
            if curr.next.val == val:
                break
            curr = curr.next
        if curr.next is None:
            return []
        else:
            curr.next = curr.next.next
            return head
    
    def reverse(self, head):
        prev = None
        while head:
            nxt = head.next
            head.next = prev
            prev = head
            head = nxt
        return prev

node = Node()
node.append(node, 0)
node.append(node, 1)
node.append(node, 2)
node.append(node, 3)
result = node.display(node)
print(result)
node = node.reverse(node)
result = node.display(node)
print(result)
node = node.delete(node, 3)
result = node.display(node)
print(result)