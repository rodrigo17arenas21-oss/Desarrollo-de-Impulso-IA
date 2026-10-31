import reflex as rx
from app.components.home import home
from app.components.campaign_form import creation
from app.components.content import content
from app.states.campaign_state import CampaignState
from app.components.browser_pages import designer, history
from app.states.browser_state import BrowserState
from app.browser_scripts import BROWSER_SCRIPT
from app.components.settings import configuration
from app.states.preferences_state import PreferencesState


def index() -> rx.Component:
    return home()


app = rx.App(
    head_components=[
        rx.script(BROWSER_SCRIPT, id="impulso-browser-tools"),
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(
            rel="preconnect",
            href="https://fonts.gstatic.com",
            cross_origin="",
        ),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(
    index,
    route="/",
    title="Impulso IA · Dale impulso a tu negocio",
    description="Un punto de partida claro para comunicar tu negocio.",
)
app.add_page(
    creation,
    route="/crear",
    title="Crear campaña · Impulso IA",
    description="Cuéntanos tu negocio, tu público y lo que quieres comunicar.",
    on_load=CampaignState.load_form,
)
app.add_page(
    content,
    route="/contenido",
    title="Tu contenido · Impulso IA",
    description="Borradores locales editables para comunicar tu negocio, sin IA conectada.",
    on_load=CampaignState.load_content,
)
app.add_page(
    designer,
    route="/diseno",
    title="Tu diseño · Impulso IA",
    on_load=BrowserState.load_designer,
)
app.add_page(
    configuration,
    route="/configuracion",
    title="Configuración y ayuda · Impulso IA",
    description="Preferencias locales, privacidad y ayuda práctica, sin IA conectada.",
    on_load=PreferencesState.load_preferences,
)
app.add_page(
    history,
    route="/historial",
    title="Historial local · Impulso IA",
    on_load=BrowserState.load_history,
)
