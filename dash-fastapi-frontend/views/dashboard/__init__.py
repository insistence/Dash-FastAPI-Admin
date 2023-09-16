from .components import page_top, page_bottom


def render_dashboard():
    return [
        page_top.render_page_top(),
        page_bottom.render_page_bottom()
    ]
