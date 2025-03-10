"""
Created by 满仓干 on - 2025/03/10.
"""


class NotConnectError(Exception):
    def __init__(self):
        msg = "未连接到交易终端"
        self.message = msg
        super().__init__(msg)
