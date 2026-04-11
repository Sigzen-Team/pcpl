# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__version__ = '1.0.6'

from erpnext.stock import stock_balance
from pcpl.override import stock_balance as pcpl_stock_balance

stock_balance.repost_actual_qty=pcpl_stock_balance.repost_actual_qty