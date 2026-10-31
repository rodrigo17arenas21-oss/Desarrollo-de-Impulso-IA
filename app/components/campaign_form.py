import reflex as rx
from app.states.campaign_state import CampaignState
from app.components.layout import header, footer


CONTROL = "w-full rounded-xl border border-[#242668]/20 bg-white px-4 py-3 text-sm text-[#202126] placeholder:text-gray-500 transition hover:border-[#242668]/40 focus:border-[#242668] focus:outline-2 focus:outline-offset-2 focus:outline-[#242668]"


def field_error(name: str) -> rx.Component:
    return rx.cond(
        CampaignState.errors[name] != "",
        rx.el.p(
            CampaignState.errors[name],
            id=f"{name}-error",
            class_name="mt-2 text-xs leading-5 text-red-700",
        ),
        rx.el.span(id=f"{name}-error", class_name="hidden"),
    )


def text_field(
    name: str, label: str, placeholder: str, limit: int, required: bool = False
) -> rx.Component:
    return rx.el.div(
        rx.el.label(
            label,
            rx.cond(
                required,
                rx.el.span(" *", class_name="text-[#242668]"),
                rx.el.span(
                    " · opcional",
                    class_name="text-xs font-normal text-gray-500",
                ),
            ),
            html_for=name,
            class_name="mb-2 block text-sm font-medium text-[#202126]",
        ),
        rx.el.input(
            id=name,
            name=name,
            placeholder=placeholder,
            default_value=CampaignState.campaign[name],
            key=CampaignState.campaign[name],
            max_length=limit,
            aria_required=required,
            aria_invalid=CampaignState.errors[name] != "",
            aria_describedby=f"{name}-error",
            class_name=CONTROL,
        ),
        field_error(name),
        class_name="min-w-0",
    )


def long_field(
    name: str,
    label: str,
    placeholder: str,
    helper: str,
    limit: int,
    required: bool = False,
) -> rx.Component:
    return rx.el.div(
        rx.el.label(
            label,
            rx.cond(
                required,
                rx.el.span(" *", class_name="text-[#242668]"),
                rx.el.span(
                    " · opcional",
                    class_name="text-xs font-normal text-gray-500",
                ),
            ),
            html_for=name,
            class_name="mb-2 block text-sm font-medium text-[#202126]",
        ),
        rx.el.textarea(
            id=name,
            name=name,
            placeholder=placeholder,
            default_value=CampaignState.campaign[name],
            key=CampaignState.campaign[name],
            max_length=limit,
            rows=3,
            aria_required=required,
            aria_invalid=CampaignState.errors[name] != "",
            aria_describedby=f"{name}-help {name}-error",
            class_name="w-full resize-y rounded-xl border border-[#242668]/20 bg-white px-4 py-3 text-sm leading-6 text-[#202126] placeholder:text-gray-500 hover:border-[#242668]/40 focus:outline-2 focus:outline-offset-2 focus:outline-[#242668]",
        ),
        rx.el.p(
            helper,
            id=f"{name}-help",
            class_name="mt-2 text-xs leading-5 text-gray-600",
        ),
        field_error(name),
    )


def select_field(
    name: str, label: str, options: list[str], required: bool = False
) -> rx.Component:
    return rx.el.div(
        rx.el.label(
            label,
            rx.cond(
                required,
                rx.el.span(" *", class_name="text-[#242668]"),
                rx.fragment(),
            ),
            html_for=name,
            class_name="mb-2 block text-sm font-medium text-[#202126]",
        ),
        rx.el.div(
            rx.el.select(
                rx.cond(
                    required,
                    rx.el.option("Selecciona un objetivo", value=""),
                    rx.fragment(),
                ),
                rx.foreach(
                    options, lambda option: rx.el.option(option, value=option)
                ),
                id=name,
                name=name,
                default_value=CampaignState.campaign[name],
                key=CampaignState.campaign[name],
                aria_required=required,
                aria_invalid=CampaignState.errors[name] != "",
                aria_describedby=f"{name}-error",
                class_name="w-full appearance-none rounded-xl border border-[#242668]/20 bg-white py-3 pl-4 pr-10 text-sm text-[#202126] hover:border-[#242668]/40 focus:outline-2 focus:outline-offset-2 focus:outline-[#242668]",
            ),
            rx.icon(
                "chevron-down",
                class_name="pointer-events-none absolute right-4 top-3.5 h-4 w-4 text-[#242668]",
            ),
            class_name="relative",
        ),
        field_error(name),
    )


def section_heading(number: str, title: str, description: str) -> rx.Component:
    return rx.el.div(
        rx.el.span(
            number,
            class_name="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-[#242668]/7 text-xs font-semibold text-[#242668]",
        ),
        rx.el.div(
            rx.el.h2(title, class_name="text-lg font-semibold text-[#202126]"),
            rx.el.p(
                description, class_name="mt-1 text-xs leading-5 text-gray-600"
            ),
        ),
        class_name="mb-6 flex items-start gap-3",
    )


def format_option(
    value: str, title: str, dimensions: str, icon: str
) -> rx.Component:
    return rx.el.label(
        rx.el.input(
            type="radio",
            name="formato",
            value=value,
            default_checked=CampaignState.campaign["formato"] == value,
            key=CampaignState.campaign["formato"],
            class_name="peer h-4 w-4 shrink-0 accent-[#242668] focus-visible:outline-2 focus-visible:outline-[#242668]",
        ),
        rx.icon(icon, class_name="h-7 w-7 text-[#242668]"),
        rx.el.span(
            rx.el.span(
                title, class_name="block text-sm font-semibold text-[#202126]"
            ),
            rx.el.span(
                dimensions, class_name="mt-1 block text-xs text-gray-600"
            ),
        ),
        class_name="flex cursor-pointer items-center gap-4 rounded-xl border border-[#242668]/20 bg-white p-4 transition hover:border-[#242668] has-[:checked]:border-[#242668] has-[:checked]:bg-[#242668]/5",
    )


def creation() -> rx.Component:
    return rx.el.div(
        header("crear"),
        rx.el.main(
            rx.el.a(
                rx.icon("arrow-left", class_name="h-4 w-4"),
                "Volver al inicio",
                href="/",
                class_name="mb-7 inline-flex items-center gap-2 rounded-lg text-xs font-medium text-gray-600 hover:text-[#242668] focus-visible:outline-2",
            ),
            rx.el.div(
                rx.el.span(
                    "PASO 01 · TU PUNTO DE PARTIDA",
                    class_name="text-[10px] font-semibold tracking-[0.15em] text-[#242668]",
                ),
                rx.el.h1(
                    "Empecemos por tu negocio.",
                    class_name="mt-3 text-3xl font-semibold tracking-[-1px] text-[#202126] sm:text-4xl",
                ),
                rx.el.p(
                    "Cuéntanos qué quieres comunicar. No hace falta ser experto en marketing.",
                    class_name="mt-3 text-sm leading-6 text-gray-600",
                ),
                class_name="mb-9",
            ),
            rx.el.p(
                CampaignState.form_notice,
                role="status",
                class_name="mb-4 text-sm leading-6 text-[#242668]",
            ),
            rx.cond(
                CampaignState.form_ready,
                rx.fragment(),
                rx.el.p(
                    "Preparando el formulario…",
                    role="status",
                    class_name="mb-4 animate-pulse text-sm text-[#242668]",
                ),
            ),
            rx.el.div(
                rx.el.form(
                    rx.cond(
                        CampaignState.has_errors,
                        rx.el.div(
                            rx.el.p(
                                "Revisa los campos señalados antes de continuar.",
                                class_name="font-semibold",
                            ),
                            rx.el.p(
                                "Tus datos se conservan. Completa o corrige lo indicado debajo de cada campo.",
                                class_name="mt-1 text-xs leading-5",
                            ),
                            id="form-errors",
                            role="alert",
                            tab_index=-1,
                            class_name="mb-6 rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-800 focus:outline-2 focus:outline-red-700",
                        ),
                        rx.fragment(),
                    ),
                    rx.el.p(
                        "* Campos obligatorios",
                        class_name="mb-6 text-xs text-gray-600",
                    ),
                    rx.el.section(
                        section_heading(
                            "01",
                            "Tu negocio y tu idea",
                            "La información que hace único lo que ofreces.",
                        ),
                        rx.el.div(
                            text_field(
                                "nombre_negocio",
                                "Nombre del negocio",
                                "Ej. El Horno del Barrio",
                                120,
                                True,
                            ),
                            text_field(
                                "tipo_negocio",
                                "Tipo de negocio",
                                "Ej. Panadería artesanal",
                                120,
                            ),
                            class_name="grid gap-5 sm:grid-cols-2",
                        ),
                        rx.el.div(
                            text_field(
                                "producto",
                                "Producto o servicio",
                                "Ej. Panes artesanales para compartir",
                                240,
                                True,
                            ),
                            class_name="mt-5",
                        ),
                        rx.el.div(
                            long_field(
                                "publico",
                                "Público objetivo",
                                "Ej. Familias del barrio que buscan opciones para su mesa",
                                "Piensa en sus necesidades, intereses o ubicación. No incluyas datos personales de clientes.",
                                600,
                                True,
                            ),
                            class_name="mt-5",
                        ),
                        rx.el.div(
                            select_field(
                                "objetivo",
                                "Objetivo de la publicación",
                                [
                                    "Dar a conocer mi negocio",
                                    "Presentar un producto o servicio",
                                    "Recibir consultas",
                                    "Conseguir ventas",
                                    "Invitar a una visita",
                                ],
                                True,
                            ),
                            class_name="mt-5",
                        ),
                    ),
                    rx.el.section(
                        section_heading(
                            "02",
                            "Lo que quieres ofrecer",
                            "Solo condiciones reales que hayas decidido para tu negocio.",
                        ),
                        long_field(
                            "oferta",
                            "Descripción de la oferta",
                            "Describe qué incluye y, si aplica, sus condiciones o vigencia",
                            "Si no tienes una oferta definida, déjalo vacío. No se confirmarán descuentos, beneficios ni condiciones que no hayas aportado.",
                            1200,
                        ),
                        rx.el.div(
                            text_field(
                                "precio", "Precio", "Ej. 120 MXN por unidad", 80
                            ),
                            rx.el.p(
                                "Incluye moneda y unidad. Déjalo vacío si no quieres comunicar un precio.",
                                class_name="mt-2 text-xs leading-5 text-gray-600",
                            ),
                            class_name="mt-5",
                        ),
                        class_name="mt-8 border-t border-[#242668]/10 pt-8",
                    ),
                    rx.el.section(
                        section_heading(
                            "03",
                            "El estilo de tu publicación",
                            "Elige cómo quieres expresarte y dónde compartirlo.",
                        ),
                        rx.el.div(
                            select_field(
                                "tono",
                                "Tono",
                                [
                                    "Cercano",
                                    "Profesional",
                                    "Inspirador",
                                    "Divertido",
                                ],
                            ),
                            select_field(
                                "red_social",
                                "Red social",
                                [
                                    "Instagram",
                                    "Facebook",
                                    "WhatsApp",
                                    "LinkedIn",
                                ],
                            ),
                            class_name="grid gap-5 sm:grid-cols-2",
                        ),
                        rx.el.fieldset(
                            rx.el.legend(
                                "Formato",
                                class_name="mb-3 text-sm font-medium text-[#202126]",
                            ),
                            rx.el.div(
                                format_option(
                                    "cuadrado",
                                    "Cuadrado",
                                    "1:1 · publicación",
                                    "square",
                                ),
                                format_option(
                                    "vertical",
                                    "Vertical",
                                    "9:16 · historia",
                                    "rectangle-vertical",
                                ),
                                class_name="grid gap-3 sm:grid-cols-2",
                            ),
                            field_error("formato"),
                            class_name="mt-6",
                        ),
                        class_name="mt-8 border-t border-[#242668]/10 pt-8",
                    ),
                    rx.el.div(
                        rx.el.p(
                            "Al continuar se conservarán tus datos en esta sesión y se preparará un borrador local con plantillas. No es IA y no se publicará automáticamente.",
                            class_name="max-w-sm text-xs leading-5 text-gray-600",
                        ),
                        rx.el.button(
                            "Continuar",
                            rx.icon("arrow-right", class_name="h-4 w-4"),
                            type="submit",
                            class_name="flex w-full items-center justify-center gap-3 rounded-xl bg-[#EF755D] px-6 py-4 text-sm font-semibold text-[#292022] transition hover:bg-[#E96850] active:scale-[0.98] focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-[#242668] sm:w-auto",
                        ),
                        class_name="mt-8 flex flex-col items-start justify-between gap-5 border-t border-[#242668]/10 pt-7 sm:flex-row sm:items-center",
                    ),
                    on_submit=CampaignState.submit_campaign,
                    reset_on_submit=False,
                    no_validate=True,
                    id="campaign-form",
                    class_name=rx.cond(
                        CampaignState.form_ready,
                        "min-w-0 rounded-3xl border border-[#242668]/10 bg-white p-5 sm:p-8",
                        "hidden",
                    ),
                ),
                rx.el.aside(
                    rx.el.div(
                        rx.icon(
                            "lightbulb",
                            class_name="mb-5 h-7 w-7 text-[#242668]",
                        ),
                        rx.el.h2(
                            "Una buena campaña empieza con una idea clara.",
                            class_name="text-xl font-semibold leading-7 tracking-tight text-[#242668]",
                        ),
                        rx.el.p(
                            "No necesitas escribir perfecto. Usa tus propias palabras y sé concreto: qué ofreces, para quién y para qué.",
                            class_name="mt-4 text-sm leading-6 text-gray-600",
                        ),
                        rx.el.div(
                            rx.icon(
                                "check",
                                class_name="h-4 w-4 shrink-0 text-[#242668]",
                            ),
                            rx.el.p(
                                "Un producto o servicio por campaña ayuda a mantener el mensaje enfocado.",
                                class_name="text-xs leading-5 text-gray-600",
                            ),
                            class_name="mt-6 flex items-start gap-2 border-t border-[#242668]/10 pt-5",
                        ),
                        class_name="rounded-2xl border border-[#242668]/10 bg-[#EEEEE7] p-6",
                    ),
                    rx.el.div(
                        rx.icon(
                            "shield-check", class_name="h-5 w-5 text-[#242668]"
                        ),
                        rx.el.h2(
                            "Tu información, con cuidado",
                            class_name="mt-3 text-sm font-semibold text-[#242668]",
                        ),
                        rx.el.p(
                            "No hace falta registrarte ni conectar tus redes. No hay publicación automática. Evita introducir datos sensibles.",
                            class_name="mt-2 text-xs leading-6 text-gray-600",
                        ),
                        class_name="p-6",
                    ),
                    class_name="flex flex-col gap-2 lg:sticky lg:top-6 lg:self-start",
                ),
                class_name="grid items-start gap-7 lg:grid-cols-[minmax(0,1fr)_300px]",
            ),
            class_name="mx-auto w-full max-w-7xl flex-1 px-5 py-8 sm:px-8 sm:py-10 lg:px-12",
        ),
        footer(),
        class_name="flex min-h-dvh flex-col bg-[#F8F7F2] font-['Inter'] text-[#202126]",
    )
