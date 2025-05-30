from typing import Optional # Optional 是一个好习惯，用于表示参数或返回值可能为 None

# Definition for a singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        """
        初始化链表节点。

        Args:
            val: 节点存储的值，默认为 0。
            next: 指向下一个节点的指针，默认为 None。
        """
        self.val = val
        self.next: Optional[ListNode] = next # 类型提示 next 也是一个 ListNode 或 None

    def __repr__(self):
        """
        方便打印链表节点信息 (主要用于调试)。
        """
        if self.next:
            return f"ListNode({self.val}, next_val={self.next.val})"
        else:
            return f"ListNode({self.val}, next=None)"

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        """
        初始化二叉树节点。

        Args:
            val: 节点存储的值，默认为 0。
            left: 指向左子节点的指针，默认为 None。
            right: 指向右子节点的指针，默认为 None。
        """
        self.val = val
        self.left: Optional[TreeNode] = left   # 类型提示 left 也是一个 TreeNode 或 None
        self.right: Optional[TreeNode] = right # 类型提示 right 也是一个 TreeNode 或 None

    def __repr__(self):
        """
        方便打印树节点信息 (主要用于调试)。
        """
        left_val = self.left.val if self.left else None
        right_val = self.right.val if self.right else None
        return f"TreeNode({self.val}, left={left_val}, right={right_val})"

# --- 示例用法 (可选) ---
if __name__ == '__main__':
    # ListNode 示例
    node1 = ListNode(1)
    node2 = ListNode(2)
    node3 = ListNode(3)

    node1.next = node2
    node2.next = node3

    print("链表示例:")
    current = node1
    while current:
        print(current.val, end=" -> " if current.next else "")
        current = current.next
    print("\n")
    print(repr(node1)) # ListNode(1, next_val=2)
    print(repr(node3)) # ListNode(3, next=None)

    # TreeNode 示例
    #     1
    #    / \
    #   2   3
    #  /
    # 4
    leaf_node = TreeNode(4)
    left_child = TreeNode(2, left=leaf_node)
    right_child = TreeNode(3)
    root_node = TreeNode(1, left=left_child, right=right_child)

    print("树节点示例:")
    print(f"Root: {root_node.val}")
    if root_node.left:
        print(f"Root's Left Child: {root_node.left.val}")
    if root_node.right:
        print(f"Root's Right Child: {root_node.right.val}")
    if root_node.left and root_node.left.left:
        print(f"Root's Left-Left Grandchild: {root_node.left.left.val}")
    print("\n")
    print(repr(root_node))      # TreeNode(1, left=2, right=3)
    print(repr(left_child))     # TreeNode(2, left=4, right=None)
    print(repr(right_child))    # TreeNode(3, left=None, right=None)
    print(repr(leaf_node))      # TreeNode(4, left=None, right=None)