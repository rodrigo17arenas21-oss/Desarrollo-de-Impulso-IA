import reflex as rx
from app.components.layout import header, footer
from app.states.campaign_state import CampaignState
from app.states.browser_state import BrowserState


BUTTON = "inline-flex items-center justify-center gap-2 rounded-xl border border-[#242668]/20 bg-white px-4 py-2.5 text-sm font-medium text-[#242668] hover:bg-[#242668]/5 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#242668] disabled:opacity-50 disabled:cursor-not-allowed"
CONTROL = "w-full resize-y rounded-xl border border-[#242668]/20 bg-white p-4 text-sm leading-6 text-[#202126] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#242668]"


def text_editor(
    field: str, label: str, rows: int = 3, headline: bool = False
) -> rx.Component:
    return rx.el.section(
        rx.el.form(
            rx.el.label(
                label,
                html_for=field,
                class_name="mb-3 block text-sm font-semibold text-[#242668]",
            ),
            rx.el.textarea(
                id=field,
                name="text",
                default_value=CampaignState.texts[field],
                key=CampaignState.texts[field],
                rows=rows,
                max_length=10000,
                aria_describedby="editing-help",
                class_name=CONTROL,
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("check", class_name="h-4 w-4"),
                    "Guardar edición",
                    type="submit",
                    disabled=CampaignState.generating,
                    class_name=BUTTON,
                ),
                rx.el.button(
                    rx.icon("copy", class_name="h-4 w-4"),
                    "Copiar guardado",
                    type="button",
                    on_click=lambda: CampaignState.copy_text(field),
                    class_name=BUTTON,
                ),
                rx.cond(
                    headline,
                    rx.el.button(
                        rx.cond(
                            CampaignState.selected_headline == field,
                            "Titular seleccionado",
                            "Usar titular",
                        ),
                        type="button",
                        on_click=lambda: CampaignState.choose_headline(field),
                        aria_pressed=CampaignState.selected_headline == field,
                        class_name=rx.cond(
                            CampaignState.selected_headline == field,
                            "rounded-xl bg-[#242668] px-4 py-2.5 text-sm font-medium text-white focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#242668]",
                            BUTTON,
                        ),
                    ),
                    rx.fragment(),
                ),
                class_name="mt-3 flex flex-wrap gap-2",
            ),
            on_submit=lambda data: CampaignState.save_text(field, data),
            reset_on_submit=False,
        ),
        class_name="rounded-2xl border border-[#242668]/10 bg-white p-5 sm:p-6",
    )


def promotion_panel() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.icon("lightbulb", class_name="h-5 w-5 text-[#EF755D]"),
            rx.el.h2(
                "Promoción: tú decides",
                class_name="text-xl font-semibold text-[#242668]",
            ),
            class_name="mb-4 flex items-center gap-3",
        ),
        rx.cond(
            CampaignState.campaign["oferta"].strip() != "",
            rx.el.div(
                rx.el.p(
                    "Oferta aportada por el negocio",
                    class_name="text-sm font-semibold text-[#242668]",
                ),
                rx.el.p(
                    CampaignState.campaign["oferta"],
                    class_name="mt-3 whitespace-pre-wrap break-words text-sm leading-6 text-[#202126]",
                ),
                rx.el.p(
                    "Se incorporó literalmente al texto principal, identificada como información tuya. No hemos verificado sus condiciones. Si editas el texto principal, revisa que siga siendo fiel a la oferta.",
                    class_name="mt-3 text-xs leading-5 text-gray-600",
                ),
                class_name="rounded-xl border border-[#242668]/10 bg-[#F8F7F2] p-5",
            ),
            rx.el.div(
                rx.el.span(
                    "IDEA NO APROBADA · NO PUBLICAR",
                    class_name="block w-fit rounded-lg bg-[#EF755D]/10 px-3 py-2 text-xs font-semibold text-[#8B3524]",
                ),
                rx.el.p(
                    "Estos ejemplos no son ofertas reales. No se añaden a tus textos ni a la publicación. Elige una idea solo si encaja con tu negocio y define condiciones reales antes de confirmarla.",
                    class_name="my-4 text-sm leading-6 text-gray-600",
                ),
                rx.el.div(
                    rx.foreach(
                        [
                            ["descuento", "Descuento"],
                            ["paquete", "Paquete"],
                            ["tiempo", "Tiempo limitado"],
                            ["nuevo", "Nuevo cliente"],
                            ["lealtad", "Lealtad"],
                        ],
                        lambda item: rx.el.button(
                            item[1],
                            on_click=lambda: CampaignState.choose_promotion(
                                item[0]
                            ),
                            aria_pressed=CampaignState.promotion_kind
                            == item[0],
                            class_name=rx.cond(
                                CampaignState.promotion_kind == item[0],
                                "rounded-xl bg-[#242668] px-4 py-2 text-xs font-semibold text-white focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#242668]",
                                BUTTON,
                            ),
                        ),
                    ),
                    class_name="mb-5 flex flex-wrap gap-2",
                ),
                text_editor(
                    "promotion_idea", "Idea de promoción (no publicable)", 3
                ),
                rx.el.form(
                    rx.el.label(
                        "Condiciones reales autorizadas por el negocio",
                        html_for="promotion-terms",
                        class_name="mb-2 block text-sm font-semibold text-[#242668]",
                    ),
                    rx.el.textarea(
                        id="promotion-terms",
                        name="terms",
                        rows=4,
                        max_length=1200,
                        default_value=rx.cond(
                            CampaignState.pending_terms != "",
                            CampaignState.pending_terms,
                            CampaignState.promotion_terms,
                        ),
                        key=CampaignState.pending_terms,
                        placeholder="Escribe el texto exacto de tu promoción y sus condiciones reales. No copies una idea genérica.",
                        aria_describedby="promotion-help promotion-error",
                        class_name=CONTROL,
                    ),
                    rx.el.p(
                        "Incluye únicamente el beneficio y las condiciones que tu negocio haya decidido: qué incluye, a quién aplica y, si procede, precio y fechas reales. No inventaremos datos faltantes.",
                        id="promotion-help",
                        class_name="mt-2 text-xs leading-5 text-gray-600",
                    ),
                    rx.el.label(
                        rx.el.input(
                            type="checkbox",
                            name="approved",
                            id="promotion-approved",
                            required=True,
                            default_checked=CampaignState.pending_approved,
                            key=CampaignState.pending_approved,
                            class_name="h-4 w-4 shrink-0 accent-[#242668] focus-visible:outline-2 focus-visible:outline-[#242668]",
                        ),
                        "Confirmo que estas condiciones son reales, están autorizadas por mi negocio y quiero incluirlas en la publicación.",
                        html_for="promotion-approved",
                        class_name="my-4 flex items-start gap-3 text-sm leading-6 text-[#202126]",
                    ),
                    rx.el.p(
                        CampaignState.promotion_error,
                        id="promotion-error",
                        role="alert",
                        class_name="mb-3 text-sm text-red-700",
                    ),
                    rx.el.button(
                        "Confirmar e incluir condiciones",
                        type="submit",
                        class_name=BUTTON,
                    ),
                    on_submit=CampaignState.confirm_promotion,
                    reset_on_submit=False,
                    class_name="mt-5 rounded-xl border border-[#242668]/10 bg-[#F8F7F2] p-5",
                ),
                rx.cond(
                    CampaignState.promotion_confirmed,
                    rx.el.div(
                        rx.el.p(
                            "Confirmada por el negocio · incluida en la publicación",
                            class_name="text-sm font-semibold text-green-800",
                        ),
                        rx.el.p(
                            CampaignState.promotion_terms,
                            class_name="mt-3 whitespace-pre-wrap break-words text-sm leading-6 text-[#202126]",
                        ),
                        rx.el.button(
                            "Retirar de la publicación",
                            on_click=CampaignState.revoke_promotion,
                            class_name=BUTTON,
                        ),
                        class_name="mt-4 flex flex-col items-start gap-3 rounded-xl border border-green-200 bg-green-50 p-5",
                    ),
                    rx.fragment(),
                ),
            ),
        ),
        class_name="rounded-2xl border border-[#242668]/10 bg-white p-5 sm:p-6",
    )


def results_body() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2(
                "Tres titulares alternativos",
                class_name="text-xl font-semibold text-[#242668]",
            ),
            rx.el.p(
                "Elige uno para tu publicación. Puedes editar los tres.",
                class_name="mt-2 text-sm text-gray-600",
            ),
            class_name="mb-4",
        ),
        rx.el.div(
            text_editor("headline_1", "Titular 1", 2, True),
            text_editor("headline_2", "Titular 2", 2, True),
            text_editor("headline_3", "Titular 3", 2, True),
            class_name="grid gap-4 lg:grid-cols-3",
        ),
        rx.el.div(
            rx.el.div(
                text_editor("copy", "Texto principal", 10),
                text_editor("description", "Descripción corta", 3),
                text_editor("cta", "Llamada a la acción", 3),
                text_editor("hashtags", "Hashtags", 2),
                rx.el.p(
                    "WhatsApp: sin hashtags por defecto. Facebook y LinkedIn: etiquetas breves. Instagram: etiquetas de negocio y sector, sin promesas.",
                    class_name="px-2 text-xs leading-5 text-gray-600",
                ),
                class_name="flex min-w-0 flex-col gap-4",
            ),
            rx.el.div(
                promotion_panel(),
                rx.el.section(
                    rx.el.h2(
                        "Vista previa de la publicación",
                        class_name="text-xl font-semibold text-[#242668]",
                    ),
                    rx.el.p(
                        "Titular seleccionado + texto principal + condiciones confirmadas (si existen) + CTA + hashtags. La descripción corta se copia por separado.",
                        class_name="mt-3 text-xs leading-5 text-gray-600",
                    ),
                    rx.el.p(
                        CampaignState.publication,
                        tab_index=0,
                        class_name="my-5 whitespace-pre-wrap break-words rounded-xl bg-[#F8F7F2] p-5 text-sm leading-7 text-[#202126] focus-visible:outline-2 focus-visible:outline-[#242668]",
                    ),
                    rx.el.button(
                        rx.icon("copy", class_name="h-4 w-4"),
                        "Copiar publicación",
                        on_click=lambda: CampaignState.copy_text("publication"),
                        class_name="flex w-full items-center justify-center gap-2 rounded-xl bg-[#242668] px-5 py-3 text-sm font-semibold text-white hover:bg-[#343784] focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-[#242668]",
                    ),
                    rx.el.p(
                        "Revisa lo que has editado. No hay publicación automática ni verificación externa de ofertas.",
                        class_name="mt-3 text-xs leading-5 text-gray-600",
                    ),
                    class_name="rounded-2xl border border-[#242668]/10 bg-white p-5 sm:p-6",
                ),
                class_name="flex min-w-0 flex-col gap-4",
            ),
            class_name="mt-6 grid items-start gap-6 lg:grid-cols-2",
        ),
        rx.el.div(
            rx.el.p(
                "El diseñador recoge también las ediciones de texto que aún no hayas enviado. Las condiciones pendientes no se aprueban automáticamente.",
                class_name="text-xs leading-6 text-gray-600",
            ),
            rx.el.button(
                rx.icon("panels-top-left", class_name="h-4 w-4"),
                "Continuar al diseñador",
                on_click=BrowserState.to_designer,
                class_name="flex items-center justify-center gap-2 rounded-xl bg-[#242668] px-5 py-3 text-sm font-semibold text-white hover:bg-[#343784] focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-[#242668]",
            ),
            rx.el.p(
                BrowserState.notice,
                role="alert",
                class_name="text-sm text-red-800",
            ),
            class_name="mt-7 flex flex-col items-start gap-4 rounded-2xl border border-[#242668]/10 bg-white p-6",
        ),
    )


def content() -> rx.Component:
    return rx.el.div(
        header("contenido"),
        rx.el.main(
            rx.el.a(
                rx.icon("arrow-left", class_name="h-4 w-4"),
                "Volver al formulario",
                href="/crear",
                class_name="mb-7 inline-flex items-center gap-2 rounded-lg text-sm text-gray-600 hover:text-[#242668] focus-visible:outline-2",
            ),
            rx.el.span(
                "PASO 02 · TU MENSAJE",
                class_name="block text-[10px] font-semibold tracking-[0.15em] text-[#242668]",
            ),
            rx.el.h1(
                "Tu contenido, con tus palabras.",
                class_name="mt-3 text-3xl font-semibold tracking-tight text-[#202126] sm:text-4xl",
            ),
            rx.el.p(
                "Generación local y determinista mediante plantillas. No es IA; no hay IA conectada ni llamadas a servicios externos para generar estos textos.",
                class_name="mt-4 max-w-3xl text-sm leading-6 text-gray-600",
            ),
            rx.cond(
                CampaignState.missing_fields.length() > 0,
                rx.el.section(
                    rx.icon(
                        "file-pen-line", class_name="h-9 w-9 text-[#242668]"
                    ),
                    rx.el.h2(
                        "Necesitamos tu punto de partida",
                        class_name="mt-5 text-xl font-semibold text-[#242668]",
                    ),
                    rx.el.p(
                        "No hay datos suficientes en esta sesión. Si la sesión terminó, vuelve a completar el formulario. Los datos disponibles se conservan.",
                        class_name="mt-3 text-sm leading-6 text-gray-600",
                    ),
                    rx.el.p(
                        f"Falta: {CampaignState.missing_fields.join(', ')}.",
                        class_name="mt-3 text-sm font-medium text-[#202126]",
                    ),
                    rx.el.a(
                        "Completar datos del negocio",
                        href="/crear",
                        class_name="mt-6 inline-flex rounded-xl bg-[#242668] px-5 py-3 text-sm font-semibold text-white focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-[#242668]",
                    ),
                    class_name="mt-8 rounded-3xl border border-[#242668]/10 bg-white p-6 sm:p-10",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.p(
                            f"{CampaignState.campaign['red_social']} · {CampaignState.campaign['tono']} · {CampaignState.campaign['objetivo']}",
                            class_name="text-xs leading-6 text-[#242668]",
                        ),
                        rx.el.button(
                            rx.icon("refresh-cw", class_name="h-4 w-4"),
                            "Regenerar alternativa",
                            on_click=CampaignState.regenerate_content,
                            disabled=CampaignState.generating,
                            class_name=BUTTON,
                        ),
                        class_name="my-6 flex flex-col items-start justify-between gap-4 sm:flex-row sm:items-center",
                    ),
                    rx.el.p(
                        "Guarda cada edición antes de copiar o cambiar de pantalla. Regenerar reemplaza los siete textos guardados; las condiciones de promoción confirmadas se conservan. Las plantillas alternan entre tres versiones, no producen variaciones ilimitadas.",
                        id="editing-help",
                        class_name="mb-5 text-xs leading-6 text-gray-600",
                    ),
                    rx.el.div(
                        CampaignState.content_notice,
                        role="status",
                        aria_live="polite",
                        class_name="mb-4 text-sm leading-6 text-[#242668]",
                    ),
                    rx.cond(
                        CampaignState.content_error != "",
                        rx.el.div(
                            rx.el.p(
                                CampaignState.content_error,
                                role="alert",
                                class_name="text-sm leading-6 text-red-800",
                            ),
                            rx.el.button(
                                "Volver a intentar generación",
                                on_click=CampaignState.generate_content,
                                disabled=CampaignState.generating,
                                class_name=BUTTON,
                            ),
                            class_name="mb-5 flex flex-col items-start gap-3 rounded-xl border border-red-200 bg-red-50 p-5",
                        ),
                        rx.fragment(),
                    ),
                    rx.cond(
                        CampaignState.generating,
                        rx.el.div(
                            rx.el.p(
                                "Preparando tu borrador local…",
                                role="status",
                                class_name="text-sm font-medium text-[#242668]",
                            ),
                            rx.el.div(
                                class_name="mt-4 h-40 animate-pulse rounded-xl bg-[#242668]/10"
                            ),
                            class_name="rounded-2xl border border-[#242668]/10 bg-white p-6",
                        ),
                        rx.cond(
                            CampaignState.content_ready,
                            results_body(),
                            rx.el.p(
                                "Tu borrador aparecerá aquí al completar la generación.",
                                class_name="text-sm text-gray-600",
                            ),
                        ),
                    ),
                ),
            ),
            class_name="mx-auto w-full max-w-7xl flex-1 px-5 py-8 sm:px-8 sm:py-10 lg:px-12",
        ),
        footer(),
        class_name="flex min-h-dvh flex-col bg-[#F8F7F2] font-['Inter'] text-[#202126]",
    )
