import pytest
import allure
from codes.shopping_cart import ShoppingCart


@pytest.fixture
def empty_cart():
    """返回一个空购物车对象"""
    return ShoppingCart()

@pytest.fixture
def limited_cart():
    """返回一个有商品数量限制的购物车"""
    return ShoppingCart(max_unique_items=3)

@pytest.fixture
def filled_cart():
    """返回一个已添加商品的购物车"""
    cart = ShoppingCart()
    cart.add_item("apple", 2)
    cart.add_item("banana", 3)
    return cart

@allure.epic("购物车功能测试")
@allure.feature("购物车初始化")
class TestShoppingCartInitialization:
    
    @allure.story("正常初始化")
    def test_init_default(self):
        cart = ShoppingCart()
        assert cart.max_unique_items is None
        assert cart.get_items() == {}
    
    @allure.story("设置最大商品种类限制")
    def test_init_with_max_items(self):
        cart = ShoppingCart(max_unique_items=5)
        assert cart.max_unique_items == 5
        assert cart.get_items() == {}
    
    @allure.story("负数最大商品种类限制")
    def test_init_with_negative_max_items(self):
        with pytest.raises(ValueError, match="Maximum unique items cannot be negative"):
            ShoppingCart(max_unique_items=-1)

@allure.epic("购物车功能测试")
@allure.feature("添加商品")
class TestAddItem:
    
    @allure.story("添加新商品")
    def test_add_new_item(self, empty_cart):
        empty_cart.add_item("apple", 2)
        assert empty_cart.get_items() == {"apple": 2}
        assert empty_cart.get_total_quantity() == 2
    
    @allure.story("添加已存在商品")
    def test_add_existing_item(self, filled_cart):
        filled_cart.add_item("apple", 3)
        assert filled_cart.get_items()["apple"] == 5
        assert filled_cart.get_total_quantity() == 8
    
    @allure.story("空商品名称")
    def test_add_empty_item_name(self, empty_cart):
        with pytest.raises(ValueError, match="Item name cannot be empty"):
            empty_cart.add_item("", 2)
        
        with pytest.raises(ValueError, match="Item name cannot be empty"):
            empty_cart.add_item(None, 2)
    
    @allure.story("无效商品数量")
    def test_add_invalid_quantity(self, empty_cart):
        with pytest.raises(ValueError, match="Quantity must be a positive integer"):
            empty_cart.add_item("apple", 0)
            
        with pytest.raises(ValueError, match="Quantity must be a positive integer"):
            empty_cart.add_item("apple", -1)
            
        with pytest.raises(ValueError, match="Quantity must be a positive integer"):
            empty_cart.add_item("apple", "2")
    
    @allure.story("超出最大商品种类限制")
    def test_add_exceeding_max_unique_items(self, limited_cart):
        limited_cart.add_item("apple", 1)
        limited_cart.add_item("banana", 1)
        limited_cart.add_item("orange", 1)
        
        with pytest.raises(ValueError, match="Cannot add more than 3 unique items"):
            limited_cart.add_item("grape", 1)
            
        # 但已有商品仍可添加
        limited_cart.add_item("apple", 1)
        assert limited_cart.get_items()["apple"] == 2

@allure.epic("购物车功能测试")
@allure.feature("移除商品")
class TestRemoveItem:
    
    @allure.story("部分移除商品")
    def test_remove_partial_quantity(self, filled_cart):
        filled_cart.remove_item("apple", 1)
        assert filled_cart.get_items()["apple"] == 1
        assert filled_cart.get_total_quantity() == 4
    
    @allure.story("完全移除商品")
    def test_remove_full_quantity(self, filled_cart):
        filled_cart.remove_item("apple", 2)
        assert "apple" not in filled_cart.get_items()
        assert filled_cart.get_total_quantity() == 3
    
    @allure.story("移除不存在商品")
    def test_remove_nonexistent_item(self, filled_cart):
        with pytest.raises(KeyError, match="Item 'grape' not found in cart"):
            filled_cart.remove_item("grape", 1)
    
    @allure.story("空商品名称")
    def test_remove_empty_item_name(self, filled_cart):
        with pytest.raises(ValueError, match="Item name cannot be empty"):
            filled_cart.remove_item("", 1)
            
        with pytest.raises(ValueError, match="Item name cannot be empty"):
            filled_cart.remove_item(None, 1)
    
    @allure.story("无效商品数量")
    def test_remove_invalid_quantity(self, filled_cart):
        with pytest.raises(ValueError, match="Quantity must be a positive integer"):
            filled_cart.remove_item("apple", 0)
            
        with pytest.raises(ValueError, match="Quantity must be a positive integer"):
            filled_cart.remove_item("apple", -1)
            
        with pytest.raises(ValueError, match="Quantity must be a positive integer"):
            filled_cart.remove_item("apple", "1")
    
    @allure.story("移除数量超过现有数量")
    def test_remove_excessive_quantity(self, filled_cart):
        with pytest.raises(ValueError, match="Cannot remove 3 of apple; only 2 available"):
            filled_cart.remove_item("apple", 3)

@allure.epic("购物车功能测试")
@allure.feature("购物车状态查询")
class TestCartQueries:
    
    @allure.story("获取总商品数量")
    def test_get_total_quantity(self, empty_cart, filled_cart):
        assert empty_cart.get_total_quantity() == 0
        assert filled_cart.get_total_quantity() == 5
        
        # 添加更多商品后测试
        filled_cart.add_item("orange", 4)
        assert filled_cart.get_total_quantity() == 9
    
    @allure.story("获取唯一商品种类数量")
    def test_get_unique_item_count(self, empty_cart, filled_cart):
        assert empty_cart.get_unique_item_count() == 0
        assert filled_cart.get_unique_item_count() == 2
        
        # 添加新商品后测试
        filled_cart.add_item("orange", 4)
        assert filled_cart.get_unique_item_count() == 3
    
    @allure.story("获取购物车内容")
    def test_get_items(self, filled_cart):
        items = filled_cart.get_items()
        assert items == {"apple": 2, "banana": 3}
        
        # 验证返回的是副本（修改不影响原对象）
        items["apple"] = 10
        assert filled_cart.get_items()["apple"] == 2

@allure.epic("购物车功能测试")
@allure.feature("清空购物车")
class TestClearCart:
    
    @allure.story("清空非空购物车")
    def test_clear_non_empty_cart(self, filled_cart):
        filled_cart.clear_cart()
        assert filled_cart.get_items() == {}
        assert filled_cart.get_total_quantity() == 0
        assert filled_cart.get_unique_item_count() == 0
    
    @allure.story("清空空购物车")
    def test_clear_empty_cart(self, empty_cart):
        empty_cart.clear_cart()
        assert empty_cart.get_items() == {}