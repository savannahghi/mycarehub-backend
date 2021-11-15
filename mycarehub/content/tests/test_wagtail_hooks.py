from mycarehub.content.wagtail_hooks import get_global_admin_js


def test_get_global_admin_js():
    admin_script = get_global_admin_js()
    assert "DOMContentLoaded" in admin_script
