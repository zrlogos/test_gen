import pytest
import allure
from used_codes.calculator import Calculator


@allure.epic("计算器功能测试")
@allure.feature("基本运算功能")
class TestCalculator:
    
    @allure.story("初始化测试")
    def test_initialization(self):
        """测试计算器初始化"""
        with allure.step("创建默认计算器对象"):
            calc = Calculator()
        
        with allure.step("验证默认初始值为0"):
            assert calc.value == 0
            assert calc.history == []
        
        with allure.step("创建带初始值的计算器对象"):
            calc2 = Calculator(10)
            assert calc2.value == 10
    
    @allure.story("加法运算测试")
    def test_add(self):
        """测试加法运算"""
        with allure.step("初始化计算器"):
            calc = Calculator(5)
        
        with allure.step("执行加法运算"):
            result = calc.add(3)
        
        with allure.step("验证结果与历史记录"):
            assert result == 8
            assert calc.value == 8
            assert calc.history == ["5 + 3"]
            
            # 进行连续运算
            calc.add(7)
            assert calc.value == 15
            assert len(calc.history) == 2
    
    @allure.story("减法运算测试")
    def test_subtract(self):
        """测试减法运算"""
        with allure.step("初始化计算器"):
            calc = Calculator(10)
        
        with allure.step("执行减法运算"):
            result = calc.subtract(4)
        
        with allure.step("验证结果与历史记录"):
            assert result == 6
            assert calc.value == 6
            assert calc.history == ["10 - 4"]
    
    @allure.story("乘法运算测试")
    def test_multiply(self):
        """测试乘法运算"""
        with allure.step("初始化计算器"):
            calc = Calculator(6)
        
        with allure.step("执行乘法运算"):
            result = calc.multiply(3)
        
        with allure.step("验证结果与历史记录"):
            assert result == 18
            assert calc.value == 18
            assert calc.history == ["6 * 3"]
    
    @allure.story("除法运算测试")
    def test_divide(self):
        """测试除法运算"""
        with allure.step("初始化计算器"):
            calc = Calculator(8)
        
        with allure.step("执行除法运算"):
            result = calc.divide(2)
        
        with allure.step("验证结果与历史记录"):
            assert result == 4
            assert calc.value == 4
            assert calc.history == ["8 / 2"]
    
    @allure.story("除零异常测试")
    def test_divide_by_zero(self):
        """测试除以零的情况"""
        with allure.step("初始化计算器"):
            calc = Calculator(10)
        
        with allure.step("验证除以零时抛出ValueError异常"):
            with pytest.raises(ValueError) as excinfo:
                calc.divide(0)
            assert "除数不能为零" in str(excinfo.value)
    
    @allure.story("历史记录测试")
    def test_history(self):
        """测试历史记录功能"""
        with allure.step("创建计算器并执行多个操作"):
            calc = Calculator()
            calc.add(5)
            calc.multiply(2)
            calc.subtract(3)
            calc.divide(2)
        
        with allure.step("验证历史记录是否正确"):
            history = calc.get_history()
            assert len(history) == 4
            assert history[0] == "0 + 5"
            assert history[1] == "5 * 2"
            assert history[2] == "10 - 3"
            assert history[3] == "7 / 2"
            assert calc.value == 3.5
    
    @allure.story("清除功能测试")
    def test_clear(self):
        """测试清除功能"""
        with allure.step("创建计算器并执行操作"):
            calc = Calculator(5)
            calc.add(10)
            assert calc.value == 15
            assert len(calc.history) == 1
        
        with allure.step("执行清除操作"):
            result = calc.clear()
        
        with allure.step("验证清除后的状态"):
            assert result == 0
            assert calc.value == 0
            assert calc.history == [] 