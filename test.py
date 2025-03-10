import json
from libs.context import Context
from libs.models import Order, Trade


with open("./order.json", '+r', encoding="utf-8-sig") as f:
  o = json.load(f)
  o = Order.load_from_dict(o)
  print(o)

with open("./trade.json", '+r', encoding="utf-8-sig") as f:
  o = json.load(f)
  o = Trade.load_from_dict(o)
  print(o)