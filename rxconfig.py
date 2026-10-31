import reflex as rx

config = rx.Config(
    app_name="app",
    default_color_mode="light",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
)
