from typing import TypeVar, Generic

T = TypeVar('T')

class Tree(Generic[T]):
    def __init__(self, val: int):
        self.left = None
        self.val = val
        self.right = None
        self.value_list = []

    def append(self, val: int) -> None:
        if self.val is None:
            self.val = val
        else:
            if val < self.val:
                if self.left is None:
                    self.left = Tree(val)
                else:
                    self.left.append(val)
            elif val > self.val:
                if self.right is None:
                    self.right = Tree(val)
                else:
                    self.right.append(val)


    def display(self, tree: T) -> list[int]:
        if tree is None:
            return self.value_list
        else:
            self.display(tree.left)
            self.value_list.append(tree.val)
            self.display(tree.right)
        return self.value_list


if __name__ == '__main__':
    tree = Tree(0)
    tree.append(1)
    tree.append(2)
    numbers = tree.display(tree)
    print(numbers)