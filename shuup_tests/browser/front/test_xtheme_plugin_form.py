# -*- coding: utf-8 -*-
# This file is part of Shuup.
#
# Copyright (c) 2012-2018, Shuup Inc. All rights reserved.
#
# This source code is licensed under the OSL-3.0 license found in the
# LICENSE file in the root directory of this source tree.
import os

import time
import pytest
from django.test.utils import override_settings

from django.utils.translation import get_language, activate
from shuup.testing.browser_utils import (
    click_element, page_has_loaded, wait_until_appeared,
    wait_until_condition
)
from shuup.testing.utils import initialize_admin_browser_test

pytestmark = pytest.mark.skipif(os.environ.get("SHUUP_BROWSER_TESTS", "0") != "1", reason="No browser tests run.")



@pytest.mark.parametrize("default_language", ["it", "pt-br", "fi"])
@pytest.mark.browser
@pytest.mark.djangodb
def test_xtheme_plugin_form_language_order(admin_user, browser, live_server, settings, default_language):
    """
    Test that the first language option is the Parler default

    As you can see, we check for that the page has loaded and we use a sleep of 1 second.
    This is necessary specially into iframes. On this test, when we click to add a new plugin row
    or after a row selection, the iframe content is changed through a request,
    like a internal link when user clicks on a anchor. We have to make sure the NEW content is loaded
    before doing any element check, because it looks like the iframe won't find the correct elements
    if you start checking that before the new content gets loaded.
    """
    with override_settings(PARLER_DEFAULT_LANGUAGE_CODE=default_language):
        browser = initialize_admin_browser_test(browser, live_server, settings)
        browser.visit(live_server + "/")

        # Start edit
        wait_until_condition(browser, lambda x: page_has_loaded(x), timeout=20)
        wait_until_appeared(browser, ".xt-edit-toggle button[type='submit']")
        click_element(browser, ".xt-edit-toggle button[type='submit']")

        placeholder_selector = "#xt-ph-front_content-xtheme-person-contact-layout"
        placeholder_name = "front_content"
        wait_until_condition(browser, lambda x: x.is_element_present_by_css(placeholder_selector))
        click_element(browser, placeholder_selector)

        with browser.get_iframe("xt-edit-sidebar-iframe") as iframe:
            # make sure all scripts are loaded
            wait_until_condition(iframe, lambda x: page_has_loaded(x), timeout=20)

            wait_until_condition(iframe, lambda x: x.is_text_present("Edit Placeholder: %s" % placeholder_name))
            wait_until_appeared(iframe, "button.layout-add-row-btn")
            time.sleep(1)
            wait_until_condition(iframe, lambda x: page_has_loaded(x), timeout=20)

            # click to add a new row
            click_element(iframe, "button.layout-add-row-btn")
            time.sleep(1)
            wait_until_condition(iframe, lambda x: page_has_loaded(x), timeout=20)

            # select the last row (the added one)
            click_element(iframe, "button.layout-add-row-btn")
            iframe.find_by_css("div.layout-cell").last.click()
            time.sleep(1)
            wait_until_condition(iframe, lambda x: page_has_loaded(x), timeout=20)

            # select the TextPlugin
            wait_until_appeared(iframe, "select[name='general-plugin']")
            iframe.select("general-plugin", "text")
            time.sleep(1)
            wait_until_condition(iframe, lambda x: page_has_loaded(x), timeout=20)
            wait_until_appeared(iframe, "ul.editor-tabs")

            # check the languages order
            languages = [el.text for el in iframe.find_by_css("ul.editor-tabs li a")]
            assert languages[0] == default_language


@pytest.mark.parametrize("language", ["it", "pt-br", "fi", "en"])
@pytest.mark.browser
@pytest.mark.djangodb
def test_xtheme_plugin_form_selected_language_pane(admin_user, browser, live_server, settings, language):
    """
    Test that the current language is selected by default
    """
    browser = initialize_admin_browser_test(browser, live_server, settings, language=language)
    browser.visit(live_server + "/")

    # Start edit
    wait_until_condition(browser, lambda x: page_has_loaded(x), timeout=20)
    wait_until_appeared(browser, ".xt-edit-toggle button[type='submit']")
    click_element(browser, ".xt-edit-toggle button[type='submit']")

    placeholder_selector = "#xt-ph-front_content-xtheme-person-contact-layout"
    wait_until_condition(browser, lambda x: x.is_element_present_by_css(placeholder_selector))
    click_element(browser, placeholder_selector)

    with browser.get_iframe("xt-edit-sidebar-iframe") as iframe:
        # make sure all scripts are loaded
        wait_until_condition(iframe, lambda x: page_has_loaded(x), timeout=20)

        wait_until_condition(iframe, lambda x: x.is_text_present("front_content"))
        wait_until_appeared(iframe, "button.layout-add-row-btn")
        time.sleep(1)
        wait_until_condition(iframe, lambda x: page_has_loaded(x), timeout=20)

        # click to add a new row
        click_element(iframe, "button.layout-add-row-btn")
        time.sleep(1)
        wait_until_condition(iframe, lambda x: page_has_loaded(x), timeout=20)

        # select the last row (the added one)
        click_element(iframe, "button.layout-add-row-btn")
        iframe.find_by_css("div.layout-cell").last.click()
        time.sleep(1)
        wait_until_condition(iframe, lambda x: page_has_loaded(x), timeout=20)

        # select the TextPlugin
        wait_until_appeared(iframe, "select[name='general-plugin']")
        iframe.select("general-plugin", "text")
        time.sleep(1)
        wait_until_condition(iframe, lambda x: page_has_loaded(x), timeout=20)
        wait_until_appeared(iframe, "ul.editor-tabs")

        # check the active language
        assert language == iframe.find_by_css("ul.editor-tabs li.active a").first.text
