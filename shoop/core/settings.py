# -*- coding: utf-8 -*-
# This file is part of Shoop.
#
# Copyright (c) 2012-2015, Shoop Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
from __future__ import unicode_literals

"""
Settings of Shoop Core.

See :ref:`apps-settings` (in :obj:`shoop.apps`) for general information
about the Shoop settings system.  Especially, when inventing settings of
your own, the :ref:`apps-naming-settings` section is an important read.
"""


#: The home currency for the Shoop installation. All monetary values
#: are implicitly in this currency unless somehow otherwise specified.
SHOOP_HOME_CURRENCY = "EUR"

#: The home country code (ISO 3166-1 alpha 2) for the Shoop installation.
#: Among other things, addresses that would be printed with this country
#: visible are printed with no country.
SHOOP_ADDRESS_HOME_COUNTRY = None

#: Whether or not anonymous orders (without a ``creator`` user)
#: are allowed.
SHOOP_ALLOW_ANONYMOUS_ORDERS = True

#: Which method is used to calculate order identifiers ("order numbers").
#: May be either the string "id", a callable or a spec string pointing
#: to a callable that must return a string given an ``order``.
SHOOP_ORDER_IDENTIFIER_METHOD = "id"

#: Which method is used to calculate order reference numbers.
#: May be a spec string pointing to a callable that must return a string
#: given an ``order``, or one of the following built-in generators.
#: ``unique``
#:    Unique reference number based on time and the order ID.
#:    The reference number has the Finnish bank reference check digit
#:    appended, making the reference number valid for Finnish bank transfers.
#: ``running``
#:    Ascending reference number. The length of the reference number will be
#:    ``SHOOP_REFERENCE_NUMBER_LENGTH`` + 1 (for the check digit described below).
#:    ``SHOOP_REFERENCE_NUMBER_PREFIX`` is prepended, if set.
#:    The reference number has the Finnish bank reference check digit
#:    appended, making the reference number valid for Finnish bank transfers.
#: ``shop_running``
#:    As ``running``, but with the shop ID prepended.
SHOOP_REFERENCE_NUMBER_METHOD = "unique"

#: The length of reference numbers generated by certain reference number generators.
SHOOP_REFERENCE_NUMBER_LENGTH = 10

#: An arbitrary (numeric) prefix for certain reference number generators.
SHOOP_REFERENCE_NUMBER_PREFIX = ""

#: The identifier of the pricing module to use for pricing products.
#:
#: Determines how product prices are calculated.  See
#: :obj:`shoop.core.pricing` for details.
SHOOP_PRICING_MODULE = "simple_pricing"

#: The identifier of the tax module to use for determining taxes of products and order lines.
#:
#: Determines taxing rules for products, shipping/payment methods and
#: other order lines.  See :obj:`shoop.core.taxing` for details.
SHOOP_TAX_MODULE = "default_tax"

#: Whether product attributes are enabled.  For installations not requiring attributes,
#: disabling this may confer a small performance increase.
SHOOP_ENABLE_ATTRIBUTES = True

#: Whether multiple shops are expected to be enabled in this installation.
#: Enabling or disabling this flag does not make it (im)possible to set up multiple shops,
#: but having it disabled may confer a small performance increase.
SHOOP_ENABLE_MULTIPLE_SHOPS = False

#: A list of order labels (2-tuples of internal identifier / visible name).
#:
#: Order labels serve as a simple taxonomy layer for easy "tagging" of orders even within
#: a single Shop.  For instance, an installation could define ``"default"`` and ``"internal"``
#: order labels, which are then usable in reports, admin filtering, etc.
SHOOP_ORDER_LABELS = [
    ("default", "Default"),
]

#: The order label (see ``SHOOP_ORDER_LABELS``) to apply to orders by default.
#: This should naturally be one of the keys in ``SHOOP_ORDER_LABELS``.
SHOOP_DEFAULT_ORDER_LABEL = "default"

#: A list of "known keys" within the ``Order.payment_data`` property bag.
#:
#: The format of this setting is a list of 2-tuples of dict key / visible name,
#: for example ``[("ssn", "Social Security Number")]``.
#:
#: For installations where customizations may save some human-readable, possibly important
#: information in ``payment_data``, this setting may be used to make this data easily visible
#: in the administration backend.
SHOOP_ORDER_KNOWN_PAYMENT_DATA_KEYS = []

#: A list of "known keys" within the ``Order.shipping_data`` property bag.
#:
#: The format of this setting is a list of 2-tuples of dict key / visible name,
#: for example ``[("shipping_instruction", "Special Shipping Instructions")]``.
#:
#: For installations where customizations may save some human-readable, possibly important
#: information in ``shipping_data``, this setting may be used to make this data easily visible
#: in the administration backend.
SHOOP_ORDER_KNOWN_SHIPPING_DATA_KEYS = []

#: A list of "known keys" within the ``Order.extra_data`` property bag.
#:
#: The format of this setting is a list of 2-tuples of dict key / visible name,
#: for example ``[("wrapping_color", "Wrapping Paper Color")]``.
#:
#: For installations where customizations may save some human-readable, possibly important
#: information in ``extra_data``, this setting may be used to make this data easily visible
#: in the administration backend.
SHOOP_ORDER_KNOWN_EXTRA_DATA_KEYS = []

#: A flag to enable/disable the telemetry system
SHOOP_TELEMETRY_ENABLED = True

#: The submission URL for Shoop's telemetry (statistics) system
SHOOP_TELEMETRY_URL = "https://telemetry.shoop.io/collect/"

#: Default cache duration for various caches in seconds
SHOOP_DEFAULT_CACHE_DURATION = 60 * 30

#: Overrides for default cache durations by key namespace.
#: These override possible defaults in `shoop.core.cache.impl.DEFAULT_CACHE_DURATIONS`.
SHOOP_CACHE_DURATIONS = {}
