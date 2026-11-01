import reflex as rx
from app.components.layout import header, footer
from app.states.browser_state import BrowserState


BUTTON = "inline-flex items-center justify-center gap-2 rounded-xl border border-[#242668]/20 bg-white px-4 py-3 text-sm font-medium text-[#242668] hover:bg-[#242668]/5 focus-visible:outline-2 focus-visible:outline-[#242668]"


def designer() -> rx.Component:
    return rx.el.div(
        header("diseno"),
        rx.el.main(
            rx.el.button(
                rx.icon("arrow-left", class_name="h-4 w-4"),
                "Editar contenido",
                on_click=BrowserState.sync_editor,
                class_name=BUTTON,
            ),
            rx.el.span(
                "PASO 03 · TU DISEÑO",
                class_name="mt-7 block text-xs font-semibold tracking-widest text-[#242668]",
            ),
            rx.el.h1(
                "Hazlo tuyo.",
                class_name="mt-3 text-3xl font-semibold text-[#202126] sm:text-4xl",
            ),
            rx.el.p(
                "Plantillas gráficas, tus palabras y tu imagen. Guarda explícitamente para conservar la campaña tras recargar o cerrar la sesión.",
                class_name="mt-4 text-sm leading-6 text-gray-600",
            ),
            rx.el.p(
                BrowserState.notice,
                role="alert",
                class_name="mt-4 text-sm text-red-800",
            ),
            rx.el.p(
                id="browser-status",
                aria_live="polite",
                role="status",
                class_name="my-4 text-sm text-[#242668]",
            ),
            rx.el.div(
                rx.cond(
                    BrowserState.notice == "",
                    rx.el.p(
                        "Preparando el editor local…",
                        class_name="text-sm text-gray-600",
                    ),
                    rx.el.button(
                        "Volver a intentar",
                        on_click=BrowserState.load_designer,
                        class_name=BUTTON,
                    ),
                ),
                id="designer-root",
                class_name="grid w-full items-start gap-6 lg:grid-cols-2",
            ),
            rx.el.a(
                "Ver historial guardado",
                href="/historial",
                class_name="mt-7 inline-block rounded-lg text-sm font-semibold text-[#242668] underline focus-visible:outline-2",
            ),
            rx.el.p(
                "Solo en este navegador y este sitio. Borrar los datos del navegador elimina el historial. No hay cuenta, base de datos ni sincronización. Las imágenes se procesan y conservan únicamente en tu dispositivo.",
                class_name="mt-4 text-xs leading-6 text-gray-600",
            ),
            class_name="mx-auto w-full max-w-7xl flex-1 px-5 py-8 sm:px-8 lg:px-12",
        ),
        footer(),
        class_name="flex min-h-dvh flex-col bg-[#F8F7F2] font-['Inter'] text-[#202126]",
    )


def history() -> rx.Component:
    return rx.el.div(
        rx.el.p(
            "Guardadas solo en este navegador y este sitio. No se sincronizan con otros dispositivos o pestañas. Recarga esta lista para ver cambios. Borrar los datos del navegador elimina estas campañas.",
            class_name="mx-auto w-full max-w-7xl px-5 pt-4 text-sm leading-6 text-gray-600 sm:px-8 lg:px-12",
        ),
        header("historial"),
        rx.el.main(
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        "TU ESPACIO LOCAL",
                        class_name="text-xs font-semibold tracking-widest text-[#242668]",
                    ),
                    rx.el.h1(
                        "Tus campañas, a mano.",
                        class_name="mt-3 text-3xl font-semibold text-[#202126] sm:text-4xl",
                    ),
                    class_name="min-w-0",
                ),
                rx.el.button(
                    rx.icon("refresh-cw", class_name="h-4 w-4"),
                    "Actualizar historial",
                    on_click=BrowserState.load_history,
                    class_name=BUTTON,
                ),
                class_name="flex flex-col items-start justify-between gap-5 sm:flex-row sm:items-center",
            ),
            rx.el.p(
                BrowserState.notice,
                role="alert",
                class_name="mt-4 text-sm text-red-800",
            ),
            rx.el.div(
                rx.cond(
                    BrowserState.notice == "",
                    rx.el.p(
                        "Leyendo campañas locales…",
                        class_name="text-sm text-gray-600",
                    ),
                    rx.el.p(
                        "Pulsa Actualizar historial para volver a intentar. Tus campañas guardadas no se han modificado.",
                        class_name="col-span-full text-sm leading-6 text-gray-600",
                    ),
                ),
                id="history-root",
                class_name="grid w-full items-start gap-5 sm:grid-cols-2 lg:grid-cols-3",
            ),
            rx.el.p(
                id="browser-status",
                role="status",
                aria_live="polite",
                class_name="my-4 text-sm text-[#242668]",
            ),
            rx.el.button(
                "Restaurar campaña seleccionada",
                id="restore-history-campaign",
                on_click=BrowserState.open_saved,
                tab_index=-1,
                class_name="hidden",
            ),
            rx.el.a(
                "Crear una campaña",
                href="/crear?nueva=1",
                class_name="mt-8 inline-flex rounded-xl bg-[#242668] px-5 py-3 text-sm font-semibold text-white focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-[#242668]",
            ),
            class_name="mx-auto w-full max-w-7xl flex-1 px-5 py-8 sm:px-8 lg:px-12",
        ),
        footer(),
        class_name="flex min-h-dvh flex-col bg-[#F8F7F2] font-['Inter'] text-[#202126]",
    )
