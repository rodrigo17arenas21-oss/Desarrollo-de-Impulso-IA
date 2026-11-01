import reflex as rx
from app.components.layout import header, footer


def campaign_example() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.span(
                rx.icon("sparkles", class_name="h-3.5 w-3.5"),
                "ASÍ PODRÍA VERSE TU IDEA",
                class_name="flex items-center gap-2 text-[10px] font-semibold tracking-[0.13em] text-[#242668]",
            ),
            rx.el.span(
                "Ejemplo ilustrativo",
                class_name="w-fit rounded-full border border-[#242668]/15 bg-white px-3 py-1 text-[10px] font-medium text-[#242668]",
            ),
            class_name="flex flex-wrap items-center justify-between gap-3 pb-5",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        "PANADERÍA · EJEMPLO",
                        class_name="text-[10px] font-semibold tracking-[0.18em] text-white/80",
                    ),
                    rx.icon("sun", class_name="h-6 w-6 text-[#EF755D]"),
                    class_name="flex items-center justify-between",
                ),
                rx.el.div(
                    rx.el.span(
                        "Lo cotidiano,",
                        class_name="block text-4xl font-semibold tracking-[-1.5px] sm:text-[46px]",
                    ),
                    rx.el.span(
                        "extraordinario.",
                        class_name="block text-4xl font-semibold tracking-[-1.5px] text-[#F4A18F] sm:text-[46px]",
                    ),
                    rx.el.p(
                        "Un momento para ti.\nUn pan para compartir.",
                        class_name="mt-6 whitespace-pre-line text-sm leading-6 text-white/85",
                    ),
                    class_name="py-11",
                ),
                rx.el.div(
                    rx.el.span(
                        "EL HORNO DEL BARRIO",
                        class_name="text-[10px] font-semibold tracking-[0.15em] text-white",
                    ),
                    rx.el.span(
                        "Hecho para compartir",
                        class_name="text-[10px] text-white/75",
                    ),
                    class_name="flex items-center justify-between gap-2 border-t border-white/20 pt-5",
                ),
                class_name="relative rounded-2xl bg-[#242668] p-7 text-white sm:p-9",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "message-square-text",
                        class_name="h-4 w-4 text-[#242668]",
                    ),
                    rx.el.span(
                        "Una idea, en palabras",
                        class_name="text-xs font-semibold text-[#242668]",
                    ),
                    class_name="flex items-center gap-2",
                ),
                rx.el.p(
                    "Hay momentos que saben mejor cuando se comparten. Conoce El Horno del Barrio y encuentra tu próximo favorito.",
                    class_name="mt-3 text-sm leading-6 text-gray-700",
                ),
                rx.el.p(
                    "#Panadería #NegocioLocal #ParaCompartir",
                    class_name="mt-3 text-xs text-[#242668]",
                ),
                class_name="rounded-2xl border border-[#242668]/10 bg-white p-5",
            ),
            class_name="flex flex-col gap-3",
        ),
        rx.el.p(
            "Negocio y textos ficticios. No es una campaña generada ni una oferta confirmada.",
            class_name="mt-4 text-[11px] leading-5 text-gray-600",
        ),
        class_name="w-full rounded-3xl border border-[#242668]/10 bg-[#EEEEE7] p-5 sm:p-6",
    )


def process_step(
    number: str, icon: str, title: str, description: str
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.span(
                number, class_name="text-xs font-semibold text-[#242668]/70"
            ),
            rx.icon(icon, class_name="h-5 w-5 text-[#242668]"),
            class_name="mb-3 flex items-center justify-between",
        ),
        rx.el.h3(
            title,
            class_name="text-lg font-semibold tracking-tight text-[#242668]",
        ),
        rx.el.p(description, class_name="mt-2 text-sm leading-6 text-gray-600"),
        class_name="rounded-2xl border border-[#242668]/10 bg-white p-4",
    )


def home() -> rx.Component:
    return rx.el.div(
        header(),
        rx.el.main(
            rx.el.section(
                rx.el.div(
                    rx.el.a(
                        rx.icon("history", class_name="h-4 w-4"),
                        "Abrir mis campañas guardadas",
                        href="/historial",
                        class_name="mt-5 flex w-fit items-center gap-2 rounded-lg text-sm font-medium text-[#242668] underline underline-offset-4 focus-visible:outline-2",
                    ),
                    rx.el.p(
                        rx.icon(
                            "check",
                            class_name="h-2 w-2 rounded-full bg-[#EF755D]",
                        ),
                        "IDEAS GRANDES PARA PEQUEÑOS NEGOCIOS",
                        class_name="mb-7 flex items-center gap-2 text-[10px] font-semibold tracking-[0.13em] text-[#242668] sm:text-xs",
                    ),
                    rx.el.h1(
                        "Tu negocio tiene",
                        rx.el.br(),
                        "mucho que contar.",
                        rx.el.br(),
                        rx.el.span(
                            "Dale impulso.", class_name="text-[#242668]"
                        ),
                        class_name="text-[42px] font-semibold leading-[1.1] tracking-[-2px] text-[#202126] sm:text-[56px] lg:text-[62px]",
                    ),
                    rx.el.p(
                        "De una idea a una campaña con tu esencia. Un espacio para preparar el contenido de tu negocio, sin empezar desde una hoja en blanco.",
                        class_name="mt-7 max-w-md text-base leading-7 text-gray-600",
                    ),
                    rx.el.a(
                        "Crear mi primera campaña",
                        rx.icon("arrow-up-right", class_name="h-5 w-5"),
                        href="/crear?nueva=1",
                        class_name="mt-8 inline-flex items-center justify-center gap-4 rounded-xl bg-[#EF755D] px-6 py-4 text-sm font-semibold text-[#292022] transition hover:bg-[#E96850] active:scale-[0.98] focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-[#242668]",
                    ),
                    rx.el.p(
                        rx.icon("check", class_name="h-4 w-4 text-[#242668]"),
                        "Sin registro. Empieza con lo que ya sabes.",
                        class_name="mt-4 flex items-center gap-2 text-xs text-gray-600",
                    ),
                    rx.el.div(
                        rx.icon("sprout", class_name="h-5 w-5 text-[#242668]"),
                        rx.el.p(
                            "Tu conocimiento del negocio es el punto de partida.",
                            class_name="text-xs leading-5 text-gray-600",
                        ),
                        class_name="mt-10 flex max-w-sm items-center gap-3 border-t border-[#242668]/10 pt-5",
                    ),
                    class_name="py-2 lg:py-8",
                ),
                campaign_example(),
                class_name="grid items-center gap-10 py-12 sm:py-16 lg:grid-cols-[1.1fr_1fr] lg:gap-16 lg:py-20",
            ),
            rx.el.section(
                rx.el.div(
                    rx.el.span(
                        "SENCILLO, PASO A PASO",
                        class_name="text-[10px] font-semibold tracking-[0.16em] text-[#242668]",
                    ),
                    rx.el.h2(
                        "Tú conoces tu negocio. Aquí empieza el resto.",
                        class_name="mt-3 text-2xl font-semibold tracking-tight text-[#202126] sm:text-3xl",
                    ),
                    rx.el.p(
                        "Prepara textos locales, personaliza un diseño y guarda tu campaña en este navegador.",
                        class_name="mt-3 text-sm leading-6 text-gray-600",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    process_step(
                        "01 / DISPONIBLE",
                        "pencil-line",
                        "Cuéntanos tu idea",
                        "Describe tu negocio, qué ofreces y a quién quieres llegar. No necesitas tenerlo todo resuelto.",
                    ),
                    process_step(
                        "02 / DISPONIBLE",
                        "message-square-text",
                        "Dale forma al mensaje",
                        "Prepara y revisa borradores locales basados en la información que aportes. No hay IA conectada.",
                    ),
                    process_step(
                        "03 / DISPONIBLE",
                        "panels-top-left",
                        "Hazlo tuyo",
                        "Adapta una plantilla con tus textos, colores e imagen; descarga un PNG y guarda tu campaña localmente.",
                    ),
                    class_name="grid gap-3 md:grid-cols-3",
                ),
                id="como-funciona",
                class_name="scroll-mt-6 border-t border-[#242668]/10 py-8 sm:py-10",
            ),
            class_name="mx-auto w-full max-w-7xl flex-1 px-5 sm:px-8 lg:px-12",
        ),
        footer(),
        class_name="flex min-h-dvh flex-col bg-[#F8F7F2] font-['Inter'] text-[#202126]",
    )
