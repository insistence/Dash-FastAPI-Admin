from .components import page_top, page_bottom


def render():
    return [
        page_top.render_page_top(),
        page_bottom.render_page_bottom()
    ]
