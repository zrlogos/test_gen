# shopping_cart.py

class ShoppingCart:
    """
    一个简单的购物车类，用于演示单元测试。
    """
    def __init__(self, max_unique_items: int = None):
        """
        初始化购物车。

        Args:
            max_unique_items (int, optional): 购物车中允许的最大不同商品种类数量。
                                             默认为 None (无限制)。
        """
        self._items = {}  # 存储商品及其数量的字典，例如: {'apple': 2}
        self.max_unique_items = max_unique_items
        if max_unique_items is not None and max_unique_items < 0:
            raise ValueError("Maximum unique items cannot be negative.")

    def add_item(self, item_name: str, quantity: int):
        """
        向购物车添加指定数量的商品。

        Args:
            item_name (str): 商品名称。
            quantity (int): 要添加的数量。

        Raises:
            ValueError: 如果 item_name 为空、quantity 小于等于 0，
                        或者添加后超出 max_unique_items 限制。
        """
        if not isinstance(item_name, str) or not item_name:
            raise ValueError("Item name cannot be empty.")
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Quantity must be a positive integer.")

        # 检查是否超出唯一商品种类限制
        if self.max_unique_items is not None and \
           item_name not in self._items and \
           len(self._items) >= self.max_unique_items:
            raise ValueError(f"Cannot add more than {self.max_unique_items} unique items.")

        current_quantity = self._items.get(item_name, 0)
        self._items[item_name] = current_quantity + quantity
        print(f"Added {quantity} of {item_name}. Cart: {self._items}") # 简单打印，方便调试

    def remove_item(self, item_name: str, quantity: int):
        """
        从购物车移除指定数量的商品。

        Args:
            item_name (str): 商品名称。
            quantity (int): 要移除的数量。

        Raises:
            ValueError: 如果 quantity 小于等于 0，或者尝试移除的数量超过现有数量。
            KeyError: 如果尝试移除购物车中不存在的商品。
        """
        if not isinstance(item_name, str) or not item_name:
             raise ValueError("Item name cannot be empty.") # 与 add_item 保持一致
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Quantity must be a positive integer.")
        if item_name not in self._items:
            raise KeyError(f"Item '{item_name}' not found in cart.")

        current_quantity = self._items[item_name]
        if quantity > current_quantity:
            raise ValueError(f"Cannot remove {quantity} of {item_name}; only {current_quantity} available.")

        if quantity == current_quantity:
            del self._items[item_name]
            print(f"Removed all {item_name}. Cart: {self._items}")
        else:
            self._items[item_name] = current_quantity - quantity
            print(f"Removed {quantity} of {item_name}. Cart: {self._items}")

    def get_total_quantity(self) -> int:
        """返回购物车中所有商品的总数量。"""
        return sum(self._items.values())

    def get_unique_item_count(self) -> int:
        """返回购物车中不同商品种类的数量。"""
        return len(self._items)

    def get_items(self) -> dict:
        """返回购物车内容的副本。"""
        return self._items.copy()

    def clear_cart(self):
        """清空购物车。"""
        self._items = {}
        print("Cart cleared.")