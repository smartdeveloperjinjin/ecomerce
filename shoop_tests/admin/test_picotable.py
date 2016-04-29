# -*- coding: utf-8 -*-
# This file is part of Shoop.
#
# Copyright (c) 2012-2016, Shoop Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
import datetime

import pytest
from django.contrib.auth import get_user_model

from shoop.admin.utils.picotable import (
    ChoicesFilter, Column, DateRangeFilter, Filter, MultiFieldTextFilter,
    Picotable, RangeFilter, TextFilter
)
from shoop.core.models import Product
from shoop.testing.mock_population import populate_if_required
from shoop_tests.utils import empty_iterable
from shoop_tests.utils.fixtures import regular_user


class PicoContext(object):
    def superuser_display(self, instance):  # Test indirect `display` callable
        return "very super" if instance.is_superuser else "-"

def instance_id(instance):  # Test direct `display` callable
    return instance.id

def false_and_true():
    return [(False, "False"), (True, "True")]

def get_pico(rf, model=None, columns=None):
    model = model or get_user_model()
    columns = columns or [
        Column("id", "Id", filter_config=Filter(), display=instance_id),
        Column("username", "Username", sortable=False, filter_config=MultiFieldTextFilter(filter_fields=("username", "email"), operator="iregex")),
        Column("email", "Email", sortable=False, filter_config=TextFilter()),
        Column("is_superuser", "Is Superuser", display="superuser_display", filter_config=ChoicesFilter(choices=false_and_true())),
        Column("is_active", "Is Active", filter_config=ChoicesFilter(choices=false_and_true)),  # `choices` callable
        Column("date_joined", "Date Joined", filter_config=DateRangeFilter())
    ]

    return Picotable(
        request=rf.get("/"),
        columns=columns,
        queryset=model.objects.all(),
        context=PicoContext()
    )


@pytest.mark.django_db
@pytest.mark.usefixtures("regular_user")
def test_picotable_basic(rf, admin_user, regular_user):
    pico = get_pico(rf)
    data = pico.get_data({"perPage": 100, "page": 1})
    assert len(data["items"]) == get_user_model().objects.count()


@pytest.mark.django_db
@pytest.mark.usefixtures("regular_user")
def test_picotable_display(rf, admin_user, regular_user):
    pico = get_pico(rf)
    data = pico.get_data({"perPage": 100, "page": 1})
    for item in data["items"]:
        if item["id"] == admin_user.pk:
            assert item["is_superuser"] == "very super"
        if item["id"] == regular_user.pk:
            assert item["is_superuser"] == "-"


@pytest.mark.django_db
@pytest.mark.usefixtures("regular_user")
def test_picotable_sort(rf, admin_user, regular_user):
    pico = get_pico(rf)
    data = pico.get_data({"perPage": 100, "page": 1, "sort": "-id"})
    id = None
    for item in data["items"]:
        if id is not None:
            assert item["id"] <= id, "sorting does not work"
        id = item["id"]


@pytest.mark.django_db
@pytest.mark.usefixtures("regular_user")
def test_picotable_invalid_sort(rf, admin_user, regular_user):
    pico = get_pico(rf)
    with pytest.raises(ValueError):
        data = pico.get_data({"perPage": 100, "page": 1, "sort": "-email"})


@pytest.mark.django_db
@pytest.mark.usefixtures("regular_user")
def test_picotable_choice_filter(rf, admin_user, regular_user):
    pico = get_pico(rf)
    data = pico.get_data({"perPage": 100, "page": 1, "filters": {"is_superuser": True}})
    assert len(data["items"]) == get_user_model().objects.filter(is_superuser=True).count()


@pytest.mark.django_db
@pytest.mark.usefixtures("regular_user")
def test_picotable_text_filter(rf, admin_user, regular_user):
    pico = get_pico(rf)
    data = pico.get_data({"perPage": 100, "page": 1, "filters": {"email": admin_user.email}})
    assert len(data["items"]) == get_user_model().objects.filter(is_superuser=True).count()


@pytest.mark.django_db
@pytest.mark.usefixtures("regular_user")
def test_picotable_multi_filter(rf, admin_user, regular_user):
    pico = get_pico(rf)
    data = pico.get_data({"perPage": 100, "page": 1, "filters": {"username": "."}})
    assert len(data["items"]) == get_user_model().objects.count()


@pytest.mark.django_db
@pytest.mark.usefixtures("regular_user")
def test_picotable_range_filter(rf, regular_user):
    pico = get_pico(rf)
    one_day = datetime.timedelta(days=1)
    assert not empty_iterable(pico.get_data({"perPage": 100, "page": 1, "filters": {"date_joined": {"min": regular_user.date_joined - one_day}}})["items"])
    assert not empty_iterable(pico.get_data({"perPage": 100, "page": 1, "filters": {"date_joined": {"max": regular_user.date_joined + one_day}}})["items"])
    # TODO: a false test for this

def test_column_is_user_friendly():
    with pytest.raises(NameError):
        Column(id="foo", title="bar", asdf=True)

@pytest.mark.django_db
@pytest.mark.usefixtures("regular_user")
def test_picotable_no_mobile_link_for_missing_object_url(rf, admin_user, regular_user):
    pico = get_pico(rf)
    pico.get_object_url = lambda object: "http://www.fakeurl.com"
    data = pico.get_data({"perPage": 100, "page": 1})
    assert data["items"][0]["_linked_in_mobile"]

    pico.get_object_url = None
    data = pico.get_data({"perPage": 100, "page": 1})
    assert not data["items"][0]["_linked_in_mobile"]


@pytest.mark.django_db
@pytest.mark.usefixtures("regular_user")
def test_picotable_correctly_sorts_translated_fields(rf, admin_user, regular_user):
    """
    Make sure that translated fields, such as product names, are correctly sorted
    """
    populate_if_required()

    columns = [
        Column("id", "Id", filter_config=Filter(), display=instance_id),
        Column(
            "name", "Name", sort_field="translations__name",
            filter_config=TextFilter(filter_field="translations__name")),
    ]

    pico = get_pico(rf, model=Product, columns=columns)

    # Verify ascending sort
    sorted_products = pico.get_data({"perPage": 100, "page": 1, "sort": "+name"})
    sorted_names = [p["name"] for p in sorted_products["items"]]
    assert sorted_names == sorted(sorted_names)

    # Verify descending sort
    sorted_products = pico.get_data({"perPage": 100, "page": 1, "sort": "-name"})
    sorted_names = [p["name"] for p in sorted_products["items"]]
    assert sorted_names == sorted(sorted_names, reverse=True)
