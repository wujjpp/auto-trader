"""
Created by 满仓干 on - 2025/03/10.
"""

import threading
from typing import Optional
import pandas as pd

class Context:
    _instance:Optional["Context"] = None
    lock = threading.Lock()

    def __init__(self):
      df = pd.read_csv("stocks.csv")
      self.candidate_stocks = df["stock_code"]

    @classmethod
    def get_instance(cls) -> "Context":
        with cls.lock:
            if not cls._instance:
                cls._instance = Context()
            return cls._instance