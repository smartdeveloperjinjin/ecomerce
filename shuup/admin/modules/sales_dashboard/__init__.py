# -*- coding: utf-8 -*-
# This file is part of Shuup.
#
# Copyright (c) 2012-2016, Shoop Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
from django.utils.translation import ugettext_lazy as _

from shuup.admin.base import AdminModule
from shuup.admin.currencybound import CurrencyBound


class SalesDashboardModule(CurrencyBound, AdminModule):
    name = _("Sales Dashboard")

    def get_required_permissions(self):
        return ("shuup.view_sales_dashboard",)

    def get_dashboard_blocks(self, request):
        import shuup.admin.modules.sales_dashboard.dashboard as dashboard
        currency = self.currency
        if not currency:
            return
        yield dashboard.get_sales_of_the_day_block(request, currency)
        yield dashboard.get_lifetime_sales_block(request, currency)
        yield dashboard.get_avg_purchase_size_block(request, currency)
        yield dashboard.get_open_orders_block(request, currency)
        yield dashboard.get_order_value_chart_dashboard_block(request, currency)
