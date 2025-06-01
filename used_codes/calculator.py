class Calculator:
    """简单计算器类，提供基本的数学运算功能"""
    
    def __init__(self, initial_value=0):
        """初始化计算器
        
        Args:
            initial_value: 初始值，默认为0
        """
        self.value = initial_value
        self.history = []
        
    def add(self, x):
        """加法运算
        
        Args:
            x: 要加的数值
            
        Returns:
            float: 计算结果
        """
        self.history.append(f"{self.value} + {x}")
        self.value += x
        return self.value
    
    def subtract(self, x):
        """减法运算
        
        Args:
            x: 要减的数值
            
        Returns:
            float: 计算结果
        """
        self.history.append(f"{self.value} - {x}")
        self.value -= x
        return self.value
    
    def multiply(self, x):
        """乘法运算
        
        Args:
            x: 乘数
            
        Returns:
            float: 计算结果
        """
        self.history.append(f"{self.value} * {x}")
        self.value *= x
        return self.value
    
    def divide(self, x):
        """除法运算
        
        Args:
            x: 除数，不能为0
            
        Returns:
            float: 计算结果
            
        Raises:
            ValueError: 当除数为0时抛出
        """
        if x == 0:
            raise ValueError("除数不能为零")
        
        self.history.append(f"{self.value} / {x}")
        self.value /= x
        return self.value
    
    def get_history(self):
        """获取计算历史记录
        
        Returns:
            list: 计算步骤的历史记录
        """
        return self.history
    
    def clear(self):
        """清除当前值和历史记录
        
        Returns:
            float: 重置后的值（0）
        """
        self.value = 0
        self.history = []
        return self.value 