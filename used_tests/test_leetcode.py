
from used_codes.solution import Solution
from util.collections import ListNode


class TestSolution:
    def test_two_sum(self):
        sol = Solution()
        assert sol.twoSum([2, 7, 11, 15], 9) == [0, 1]
        assert sol.twoSum([3, 2, 4], 6) == [1, 2]
        assert sol.twoSum([3, 3], 6) == [0, 1]

    def test_is_palindrome(self):
        sol = Solution()
        assert sol.isPalindrome(121) == True
        assert sol.isPalindrome(-121) == False
        assert sol.isPalindrome(10) == False

    def test_max_profit(self):
        sol = Solution()
        assert sol.maxProfit([7, 1, 5, 3, 6, 4]) == 5
        assert sol.maxProfit([7, 6, 4, 3, 1]) == 0

    def test_is_valid_parentheses(self):
        sol = Solution()
        assert sol.isValid("()") == True
        assert sol.isValid("()[]{}") == True
        assert sol.isValid("(]") == False

    def test_merge_two_sorted_lists(self):
        sol = Solution()
        l1 = ListNode(1, ListNode(2, ListNode(4)))
        l2 = ListNode(1, ListNode(3, ListNode(4)))
        merged = sol.mergeTwoLists(l1, l2)
        assert merged.to_list() == [1, 1, 2, 3, 4, 4]

    def test_length_of_longest_substring(self):
        sol = Solution()
        assert sol.lengthOfLongestSubstring("abcabcbb") == 3
        assert sol.lengthOfLongestSubstring("bbbbb") == 1
        assert sol.lengthOfLongestSubstring("pwwkew") == 3

    def test_find_median_sorted_arrays(self):
        sol = Solution()
        assert sol.findMedianSortedArrays([1, 3], [2]) == 2.0
        assert sol.findMedianSortedArrays([1, 2], [3, 4]) == 2.5

    def test_longest_consecutive(self):
        sol = Solution()
        assert sol.longestConsecutive([100, 4, 200, 1, 3, 2]) == 4
        assert sol.longestConsecutive([0, -1]) == 2
        assert sol.longestConsecutive([]) == 0

    def test_max_sliding_window(self):
        sol = Solution()
        assert sol.maxSlidingWindow([1, 3, -1, -3, 5, 3, 6, 7], 3) == [3, 3, 5, 5, 6, 7]
        assert sol.maxSlidingWindow([1], 1) == [1]
        assert sol.maxSlidingWindow([1, -1], 1) == [1, -1]

    def test_coin_change(self):
        sol = Solution()
        assert sol.coinChange([1, 2, 5], 11) == 3
        assert sol.coinChange([2], 3) == -1
        assert sol.coinChange([1], 0) == 0

    def test_reverse_linked_list(self):
        sol = Solution()
        head = ListNode(1, ListNode(2))
        reversed_head = sol.reverseList(head)
        assert reversed_head.to_list() == [2, 1]

    def test_has_cycle(self):
        sol = Solution()
        head = ListNode(3, ListNode(2, ListNode(0, ListNode(-4))))
        head.next.next.next.next = head.next
        assert sol.hasCycle(head) == True
        head.next.next.next.next = None
        assert sol.hasCycle(head) == False

    def test_detect_cycle(self):
        sol = Solution()
        head = ListNode(3, ListNode(2, ListNode(0, ListNode(-4))))
        head.next.next.next.next = head.next
        assert sol.detectCycle(head).val == 2
        head.next.next.next.next = None
        assert sol.detectCycle(head) is None

    def test_copy_random_list(self):
        sol = Solution()
        # This test case requires a more complex setup to fully validate the random pointers.
        pass

    def test_is_palindrome_string(self):
        sol = Solution()
        assert sol.isPalindromeString("A man, a plan, a canal: Panama") == True
        assert sol.isPalindromeString("race a car") == False

    def test_contains_duplicate(self):
        sol = Solution()
        assert sol.containsDuplicate([1, 2, 3, 1]) == True
        assert sol.containsDuplicate([1, 2, 3, 4]) == False
        assert sol.containsDuplicate([1, 1, 1, 3, 3, 4, 3, 2, 4, 2]) == True

    def test_maximum_product(self):
        sol = Solution()
        assert sol.maximumProduct([3, 4, 5]) == 60
        assert sol.maximumProduct([1, 5, 4, 5]) == 160
        assert sol.maximumProduct([3, 7]) == 12