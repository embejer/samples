from listnode_class import ListNode

ln = ListNode(0)
ln.append(ln, 1)
ln.append(ln, 2)
ln.append(ln, 3)
ln.append(ln, 4)

'''Displays the list node values'''
# print(ln.display(ln))


'''Remove node from given index'''
# ln.delete(ln, 1)
# print(ln.display(ln))


'''Sum up all node values'''
# ln.append(ln, 1)
# print(f'Total: {ln.sum_list(ln)}')


'''Reversing node values'''
print(ln.reverse(ln))