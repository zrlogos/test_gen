import re

class UserRegistration:
    def __init__(self):
        self.user_db = {}  # 模拟用户数据库

    def validate_username(self, username):
        """检查用户名是否合法"""
        if not username:
            return False, "用户名不能为空"
        if len(username) > 20:
            return False, "用户名不能超过20个字符"
        if username in self.user_db:
            return False, "用户名已存在"
        return True, "用户名合法"

    def validate_password(self, password):
        """检查密码是否合法"""
        if len(password) < 8:
            return False, "密码长度必须至少为8个字符"
        if not re.search(r"[A-Za-z]", password) or not re.search(r"\d", password):
            return False, "密码必须包含字母和数字"
        return True, "密码合法"

    def register_user(self, username, password):
        """用户注册"""
        valid_username, username_message = self.validate_username(username)
        if not valid_username:
            return False, username_message

        valid_password, password_message = self.validate_password(password)
        if not valid_password:
            return False, password_message

        # 注册成功，存储用户信息
        self.user_db[username] = password
        return True, "注册成功"

# 示例用法
if __name__ == "__main__":
    user_reg = UserRegistration()
    print(user_reg.register_user("user1", "password123"))  # 注册成功
    print(user_reg.register_user("user1", "pass"))        # 密码不合法
    print(user_reg.register_user("user2", ""))            # 用户名为空
