"""
Created by 满仓干 on - 2025/03/10.
"""

"""
免责声明: 
本程序仅供学习交流使用，在实盘使用本程序造成的投资上(不仅限于)的任何损失与程序作者无任何关系, 同意才能使用
运行本程序即同意上述免责声明 
"""

class NotConnectError(Exception):
    def __init__(self):
        msg = "未连接到交易终端"
        self.message = msg
        super().__init__(msg)
