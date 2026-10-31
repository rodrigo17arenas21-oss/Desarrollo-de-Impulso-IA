import reflex as rx


def header(active: str = "inicio") -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.a(
                rx.el.span(
                    "impulso",
                    class_name="text-[27px] font-bold tracking-[-1.3px] text-[#242668]",
                ),
                rx.el.span(
                    "IA",
                    class_name="rounded-lg bg-[#242668] px-2 py-1 text-sm font-semibold tracking-normal text-white",
                ),
                href="/",
                aria_label="Impulso IA — inicio",
                class_name="flex items-center gap-2 rounded-lg focus-visible:outline-2 focus-visible:outline-[#242668]",
            ),
            rx.el.nav(
                rx.el.a(
                    "Inicio",
                    href="/",
                    aria_current=rx.cond(active == "inicio", "page", "false"),
                    class_name=rx.cond(
                        active == "inicio",
                        "hidden sm:block rounded-lg px-3 py-2 text-sm font-semibold text-[#242668] underline decoration-[#EF755D] decoration-2 underline-offset-8",
                        "hidden sm:block rounded-lg px-3 py-2 text-sm text-gray-600 hover:text-[#242668] focus-visible:outline-2",
                    ),
                ),
                rx.el.a(
                    rx.icon("history", class_name="h-4 w-4"),
                    rx.el.span("Historial", class_name="hidden sm:inline"),
                    href="/historial",
                    aria_label="Historial local",
                    aria_current=rx.cond(
                        active == "historial", "page", "false"
                    ),
                    class_name="flex items-center gap-2 rounded-lg px-2 py-2 text-sm font-medium text-[#242668] hover:bg-[#242668]/5 focus-visible:outline-2",
                ),
                rx.el.a(
                    rx.icon("settings", class_name="h-4 w-4"),
                    rx.el.span(
                        "Ayuda y ajustes", class_name="hidden lg:inline"
                    ),
                    href="/configuracion",
                    aria_label="Configuración y ayuda",
                    aria_current=rx.cond(
                        active == "configuracion", "page", "false"
                    ),
                    class_name="flex h-11 min-w-11 items-center justify-center gap-2 rounded-lg px-2 text-sm font-medium text-[#242668] hover:bg-[#242668]/5 focus-visible:outline-2",
                ),
                rx.el.a(
                    "Cómo funciona",
                    href="/#como-funciona",
                    class_name="hidden md:block rounded-lg px-3 py-2 text-sm text-gray-600 hover:text-[#242668] focus-visible:outline-2",
                ),
                rx.el.a(
                    rx.icon("plus", class_name="h-4 w-4"),
                    rx.el.span("Crear", class_name="sm:hidden"),
                    rx.el.span("Crear campaña", class_name="hidden sm:inline"),
                    href="/crear?nueva=1",
                    aria_current=rx.cond(active == "crear", "page", "false"),
                    class_name="flex items-center gap-2 rounded-xl bg-[#242668] px-4 py-3 text-sm font-semibold text-white transition hover:bg-[#343784] active:scale-[0.98] focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-[#242668]",
                ),
                aria_label="Navegación principal",
                class_name="flex items-center gap-1 sm:gap-3 lg:gap-4",
            ),
            class_name="mx-auto flex w-full max-w-7xl items-center justify-between gap-3 px-5 py-5 sm:px-8 lg:px-12",
        ),
        class_name="shrink-0 border-b border-[#242668]/10 bg-[#F8F7F2]",
    )


def footer() -> rx.Component:
    return rx.el.footer(
        rx.el.div(
            rx.el.p(
                "Un pequeño impulso. Muchas posibilidades.",
                class_name="text-sm text-[#242668]",
            ),
            rx.el.p(
                "Hecho para negocios con algo que contar.",
                class_name="text-xs text-gray-600",
            ),
            class_name="mx-auto flex max-w-7xl flex-col justify-between gap-3 px-5 py-7 sm:flex-row sm:px-8 lg:px-12",
        ),
        class_name="border-t border-[#242668]/10 bg-[#F8F7F2]",
    )
