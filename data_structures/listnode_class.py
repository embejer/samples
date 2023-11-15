class ListNode:
    def __init__(self, val=None, next=None):
        self.val = val
        self.next = next

    def append(self, head, val):
        new = ListNode(val)
        curr = head
        while curr and curr.next:
            curr = curr.next
        curr.next = new
        return head

    def display(self, head):
        result = []
        curr = head
        while curr:
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

    def sum_list(self, head):
        total = 0
        while head:
            total += head.val
            head = head.next
        return total

    def insert(self, head, index, val):
        new = ListNode(val)
        cnt = 0
        while head:
            if cnt == index:
                prev = head
                temp = head.next
                new.next = temp
                head.next = new
                break
            else:
                head = head.next
                cnt += 1
        return head

    def reverse(self, head):
        prev = None
        while head:
            nxt = head.next
            head.next = prev
            prev = head           
            head = nxt
        result = self.display(prev)
        return result