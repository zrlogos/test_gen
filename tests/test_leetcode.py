import pytest
import allure
from codes.leetcode import Solution
from util.collections import ListNode, TreeNode


@pytest.fixture
def solution():
    return Solution()


@allure.feature("Solution")
class TestSolution:

    @allure.story("Two Sum")
    def test_twoSum(self, solution):
        # Normal cases
        assert solution.twoSum([2, 7, 11, 15], 9) == [0, 1]
        assert solution.twoSum([3, 2, 4], 6) == [1, 2]
        assert solution.twoSum([3, 3], 6) == [0, 1]

        # Edge cases
        assert solution.twoSum([], 0) == []
        assert solution.twoSum([1, 2, 3], 10) == []
        assert solution.twoSum([1], 1) == []

    @allure.story("Palindrome Linked List")
    def test_isPalindrome(self, solution):
        # Normal cases
        head1 = ListNode(1, ListNode(2, ListNode(2, ListNode(1))))
        assert solution.isPalindrome(head1) == True

        head2 = ListNode(1, ListNode(2))
        assert solution.isPalindrome(head2) == False

        # Edge cases
        assert solution.isPalindrome(None) == True
        assert solution.isPalindrome(ListNode(1)) == True

    @allure.story("Valid Parentheses")
    def test_isValid(self, solution):
        # Normal cases
        assert solution.isValid("()") == True
        assert solution.isValid("()[]{}") == True
        assert solution.isValid("(]") == False

        # Edge cases
        assert solution.isValid("") == True
        assert solution.isValid("([)]") == False
        assert solution.isValid("{[]}") == True

    @allure.story("Merge Two Sorted Lists")
    def test_mergeTwoLists(self, solution):
        # Normal cases
        list1 = ListNode(1, ListNode(2, ListNode(4)))
        list2 = ListNode(1, ListNode(3, ListNode(4)))
        merged = solution.mergeTwoLists(list1, list2)
        assert merged.val == 1
        assert merged.next.val == 1
        assert merged.next.next.val == 2

        # Edge cases
        assert solution.mergeTwoLists(None, None) == None
        assert solution.mergeTwoLists(None, ListNode(0)).val == 0

    @allure.story("Maximum Depth of Binary Tree")
    def test_maxDepth(self, solution):
        # Normal cases
        root = TreeNode(3, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))
        assert solution.maxDepth(root) == 3

        # Edge cases
        assert solution.maxDepth(None) == 0
        assert solution.maxDepth(TreeNode(1)) == 1

    @allure.story("Invert Binary Tree")
    def test_invertTree(self, solution):
        # Normal cases
        root = TreeNode(4, TreeNode(2, TreeNode(1), TreeNode(3)), TreeNode(7, TreeNode(6), TreeNode(9)))
        inverted = solution.invertTree(root)
        assert inverted.left.val == 7
        assert inverted.right.val == 2

        # Edge cases
        assert solution.invertTree(None) == None
        assert solution.invertTree(TreeNode(1)).val == 1

    @allure.story("Climbing Stairs")
    def test_climbStairs(self, solution):
        # Normal cases
        assert solution.climbStairs(2) == 2
        assert solution.climbStairs(3) == 3
        assert solution.climbStairs(5) == 8

        # Edge cases
        assert solution.climbStairs(1) == 1
        assert solution.climbStairs(0) == 0

    @allure.story("Best Time to Buy and Sell Stock")
    def test_maxProfit(self, solution):
        # Normal cases
        assert solution.maxProfit([7, 1, 5, 3, 6, 4]) == 5
        assert solution.maxProfit([7, 6, 4, 3, 1]) == 0

        # Edge cases
        assert solution.maxProfit([]) == 0
        assert solution.maxProfit([1]) == 0

    @allure.story("Valid Anagram")
    def test_isAnagram(self, solution):
        # Normal cases
        assert solution.isAnagram("anagram", "nagaram") == True
        assert solution.isAnagram("rat", "car") == False

        # Edge cases
        assert solution.isAnagram("", "") == True
        assert solution.isAnagram("a", "a") == True
        assert solution.isAnagram("a", "b") == False

    @allure.story("Maximum Subarray")
    def test_maxSubArray(self, solution):
        # Normal cases
        assert solution.maxSubArray([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6
        assert solution.maxSubArray([1]) == 1

        # Edge cases
        assert solution.maxSubArray([]) == 0
        assert solution.maxSubArray([-1, -2, -3]) == -1

    @allure.story("Reverse Linked List")
    def test_reverseList(self, solution):
        # Normal cases
        head = ListNode(1, ListNode(2, ListNode(3, ListNode(4))))
        reversed_head = solution.reverseList(head)
        assert reversed_head.val == 4
        assert reversed_head.next.val == 3

        # Edge cases
        assert solution.reverseList(None) == None
        assert solution.reverseList(ListNode(1)).val == 1

    @allure.story("Linked List Cycle")
    def test_hasCycle(self, solution):
        # Normal cases
        node1 = ListNode(3)
        node2 = ListNode(2)
        node3 = ListNode(0)
        node4 = ListNode(-4)
        node1.next = node2
        node2.next = node3
        node3.next = node4
        node4.next = node2  # Cycle
        assert solution.hasCycle(node1) == True

        # No cycle
        node4.next = None
        assert solution.hasCycle(node1) == False

        # Edge cases
        assert solution.hasCycle(None) == False

    @allure.story("Sliding Window Maximum")
    def test_maxSlidingWindow(self, solution):
        # Normal cases
        assert solution.maxSlidingWindow([1, 3, -1, -3, 5, 3, 6, 7], 3) == [3, 3, 5, 5, 6, 7]
        assert solution.maxSlidingWindow([1], 1) == [1]

        # Edge cases
        assert solution.maxSlidingWindow([], 0) == []
        assert solution.maxSlidingWindow([1, -1], 1) == [1, -1]

    @allure.story("Longest Substring Without Repeating Characters")
    def test_lengthOfLongestSubstring(self, solution):
        # Normal cases
        assert solution.lengthOfLongestSubstring("abcabcbb") == 3
        assert solution.lengthOfLongestSubstring("bbbbb") == 1
        assert solution.lengthOfLongestSubstring("pwwkew") == 3

        # Edge cases
        assert solution.lengthOfLongestSubstring("") == 0
        assert solution.lengthOfLongestSubstring(" ") == 1

    @allure.story("3Sum")
    def test_threeSum(self, solution):
        # Normal cases
        assert solution.threeSum([-1, 0, 1, 2, -1, -4]) == [[-1, -1, 2], [-1, 0, 1]]
        assert solution.threeSum([0, 0, 0]) == [[0, 0, 0]]

        # Edge cases
        assert solution.threeSum([]) == []
        assert solution.threeSum([0]) == []

    @allure.story("Subtree of Another Tree")
    def test_isSubtree(self, solution):
        # Normal cases
        root = TreeNode(3, TreeNode(4, TreeNode(1), TreeNode(2)), TreeNode(5))
        subRoot = TreeNode(4, TreeNode(1), TreeNode(2))
        assert solution.isSubtree(root, subRoot) == True

        # Not a subtree
        subRoot = TreeNode(4, TreeNode(1), TreeNode(3))
        assert solution.isSubtree(root, subRoot) == False

        # Edge cases
        assert solution.isSubtree(None, None) == True
        assert solution.isSubtree(root, None) == True
        assert solution.isSubtree(None, subRoot) == False

    @allure.story("Validate Binary Search Tree")
    def test_isValidBST(self, solution):
        # Normal cases
        root = TreeNode(2, TreeNode(1), TreeNode(3))
        assert solution.isValidBST(root) == True

        # Invalid BST
        root = TreeNode(5, TreeNode(1), TreeNode(4, TreeNode(3), TreeNode(6)))
        assert solution.isValidBST(root) == False

        # Edge cases
        assert solution.isValidBST(None) == True
        assert solution.isValidBST(TreeNode(1)) == True

    @allure.story("Kth Smallest Element in a BST")
    def test_kthSmallest(self, solution):
        # Normal cases
        root = TreeNode(3, TreeNode(1, None, TreeNode(2)), TreeNode(4))
        assert solution.kthSmallest(root, 1) == 1
        assert solution.kthSmallest(root, 3) == 3

        # Edge cases
        assert solution.kthSmallest(TreeNode(1), 1) == 1

    @allure.story("House Robber")
    def test_rob(self, solution):
        # Normal cases
        assert solution.rob([1, 2, 3, 1]) == 4
        assert solution.rob([2, 7, 9, 3, 1]) == 12

        # Edge cases
        assert solution.rob([]) == 0
        assert solution.rob([1]) == 1
        assert solution.rob([1, 2]) == 2

    @allure.story("Number of Islands")
    def test_numIslands(self, solution):
        # Normal cases
        grid = [
            ["1", "1", "1", "1", "0"],
            ["1", "1", "0", "1", "0"],
            ["1", "1", "0", "0", "0"],
            ["0", "0", "0", "0", "0"]
        ]
        assert solution.numIslands(grid) == 1

        grid = [
            ["1", "1", "0", "0", "0"],
            ["1", "1", "0", "0", "0"],
            ["0", "0", "1", "0", "0"],
            ["0", "0", "0", "1", "1"]
        ]
        assert solution.numIslands(grid) == 3

        # Edge cases
        assert solution.numIslands([]) == 0
        assert solution.numIslands([["1"]]) == 1

    @allure.story("Merge Intervals")
    def test_merge(self, solution):
        # Normal cases
        assert solution.merge([[1, 3], [2, 6], [8, 10], [15, 18]]) == [[1, 6], [8, 10], [15, 18]]
        assert solution.merge([[1, 4], [4, 5]]) == [[1, 5]]

        # Edge cases
        assert solution.merge([]) == []
        assert solution.merge([[1, 4]]) == [[1, 4]]

    @allure.story("Coin Change")
    def test_coinChange(self, solution):
        # Normal cases
        assert solution.coinChange([1, 2, 5], 11) == 3
        assert solution.coinChange([2], 3) == -1

        # Edge cases
        assert solution.coinChange([], 0) == 0
        assert solution.coinChange([1], 0) == 0

    @allure.story("Valid Palindrome (String)")
    def test_isPalindromeString(self, solution):
        # Normal cases
        assert solution.isPalindromeString("A man, a plan, a canal: Panama") == True
        assert solution.isPalindromeString("race a car") == False

        # Edge cases
        assert solution.isPalindromeString("") == True
        assert solution.isPalindromeString(" ") == True

    @allure.story("Contains Duplicate")
    def test_containsDuplicate(self, solution):
        # Normal cases
        assert solution.containsDuplicate([1, 2, 3, 1]) == True
        assert solution.containsDuplicate([1, 2, 3, 4]) == False

        # Edge cases
        assert solution.containsDuplicate([]) == False
        assert solution.containsDuplicate([1]) == False

    @allure.story("Set Matrix Zeroes")
    def test_setZeroes(self, solution):
        # Normal cases
        matrix = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
        solution.setZeroes(matrix)
        assert matrix == [[1, 0, 1], [0, 0, 0], [1, 0, 1]]

        # Edge cases
        matrix = [[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]]
        solution.setZeroes(matrix)
        assert matrix == [[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]]

    @allure.story("Search in Rotated Sorted Array")
    def test_search(self, solution):
        # Normal cases
        assert solution.search([4, 5, 6, 7, 0, 1, 2], 0) == 4
        assert solution.search([4, 5, 6, 7, 0, 1, 2], 3) == -1

        # Edge cases
        assert solution.search([1], 0) == -1
        assert solution.search([1], 1) == 0

    @allure.story("Find Minimum in Rotated Sorted Array")
    def test_findMin(self, solution):
        # Normal cases
        assert solution.findMin([3, 4, 5, 1, 2]) == 1
        assert solution.findMin([4, 5, 6, 7, 0, 1, 2]) == 0

        # Edge cases
        assert solution.findMin([1]) == 1
        assert solution.findMin([1, 2]) == 1

    @allure.story("Product of Array Except Self")
    def test_productExceptSelf(self, solution):
        # Normal cases
        assert solution.productExceptSelf([1, 2, 3, 4]) == [24, 12, 8, 6]
        assert solution.productExceptSelf([-1, 1, 0, -3, 3]) == [0, 0, 9, 0, 0]

        # Edge cases
        assert solution.productExceptSelf([0, 0]) == [0, 0]
        assert solution.productExceptSelf([1]) == [1]


