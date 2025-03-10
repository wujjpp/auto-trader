"""
Created by 满仓干 on - 2025/03/10.
使用本程序造成的投资上的任何损失与程序作者无任何关系，同意才能使用
"""


class NotConnectError(Exception):
    def __init__(self):
        msg = "未连接到交易终端"
        self.message = msg
        super().__init__(msg)
