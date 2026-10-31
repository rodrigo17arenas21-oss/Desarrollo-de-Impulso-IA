import reflex as rx
from app.components.layout import header, footer
from app.states.preferences_state import PreferencesState, TONES, NETWORKS


BUTTON = "inline-flex items-center justify-center gap-2 rounded-xl border border-[#242668]/20 bg-white px-4 py-3 text-sm font-medium text-[#242668] hover:bg-[#242668]/5 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#242668] disabled:opacity-50"
CARD = "rounded-2xl border border-[#242668]/10 bg-white p-5 sm:p-7"


def preference_select(
    name: str, label: str, options: list[str], value: rx.Var[str]
) -> rx.Component:
    return rx.el.div(
        rx.el.label(
            label,
            html_for=f"default-{name}",
            class_name="mb-2 block text-sm font-semibold text-[#242668]",
        ),
        rx.el.div(
            rx.el.select(
                rx.foreach(
                    options, lambda option: rx.el.option(option, value=option)
                ),
                id=f"default-{name}",
                name=name,
                default_value=value,
                key=value,
                class_name="w-full appearance-none rounded-xl border border-[#242668]/20 bg-white py-3 pl-4 pr-10 text-sm text-[#202126] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#242668]",
            ),
            rx.icon(
                "chevron-down",
                class_name="pointer-events-none absolute right-4 top-3.5 h-4 w-4 text-[#242668]",
            ),
            class_name="relative",
        ),
    )


def help_detail(title: str, text: str) -> rx.Component:
    return rx.el.details(
        rx.el.summary(
            title,
            class_name="cursor-pointer rounded-lg py-3 text-sm font-semibold text-[#242668] focus-visible:outline-2 focus-visible:outline-[#242668]",
        ),
        rx.el.p(text, class_name="pb-4 text-sm leading-7 text-gray-600"),
        class_name="border-b border-[#242668]/10 last:border-0",
    )


def information(icon: str, title: str, text: str) -> rx.Component:
    return rx.el.div(
        rx.icon(icon, class_name="mt-1 h-5 w-5 shrink-0 text-[#242668]"),
        rx.el.div(
            rx.el.h3(title, class_name="text-sm font-semibold text-[#242668]"),
            rx.el.p(text, class_name="mt-2 text-sm leading-7 text-gray-600"),
        ),
        class_name="flex items-start gap-3",
    )


def configuration() -> rx.Component:
    return rx.el.div(
        header("configuracion"),
        rx.el.main(
            rx.el.span(
                "A TU MANERA",
                class_name="text-xs font-semibold tracking-widest text-[#242668]",
            ),
            rx.el.h1(
                "Configuración y ayuda",
                class_name="mt-3 text-3xl font-semibold tracking-tight text-[#202126] sm:text-4xl",
            ),
            rx.el.p(
                "Unos ajustes sencillos y respuestas claras para empezar con confianza.",
                class_name="mt-3 text-sm leading-7 text-gray-600",
            ),
            rx.el.div(
                rx.el.section(
                    rx.el.h2(
                        "Preferencias para campañas nuevas",
                        class_name="text-xl font-semibold text-[#242668]",
                    ),
                    rx.el.p(
                        "Se guardan solo en este navegador y este sitio. No cambian una campaña en curso ni una abierta del historial. Pulsa Crear para empezar con tus preferencias; volver al formulario conserva tu campaña.",
                        class_name="my-4 text-sm leading-7 text-gray-600",
                    ),
                    rx.cond(
                        PreferencesState.ready,
                        rx.el.form(
                            rx.el.div(
                                preference_select(
                                    "tono",
                                    "Tono predeterminado",
                                    TONES,
                                    PreferencesState.tone,
                                ),
                                preference_select(
                                    "red_social",
                                    "Red social predeterminada",
                                    NETWORKS,
                                    PreferencesState.network,
                                ),
                                class_name="grid gap-5 sm:grid-cols-2",
                            ),
                            rx.el.button(
                                rx.icon("check", class_name="h-4 w-4"),
                                "Guardar preferencias",
                                type="submit",
                                class_name="mt-6 inline-flex items-center gap-2 rounded-xl bg-[#242668] px-5 py-3 text-sm font-semibold text-white hover:bg-[#343784] focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-[#242668]",
                            ),
                            on_submit=PreferencesState.save_preferences,
                            reset_on_submit=False,
                        ),
                        rx.el.p(
                            "Leyendo preferencias…",
                            role="status",
                            class_name="animate-pulse py-4 text-sm text-[#242668]",
                        ),
                    ),
                    rx.el.p(
                        PreferencesState.notice,
                        role="status",
                        aria_live="polite",
                        class_name="mt-4 text-sm leading-7 text-[#242668]",
                    ),
                    rx.el.p(
                        PreferencesState.error,
                        role="alert",
                        class_name="mt-3 text-sm leading-7 text-red-800",
                    ),
                    rx.el.div(
                        rx.el.button(
                            "Restablecer solo preferencias",
                            type="button",
                            on_click=PreferencesState.restore_defaults,
                            disabled=~PreferencesState.ready,
                            class_name=BUTTON,
                        ),
                        rx.el.button(
                            rx.icon("refresh-cw", class_name="h-4 w-4"),
                            "Volver a leer",
                            type="button",
                            on_click=PreferencesState.load_preferences,
                            disabled=~PreferencesState.ready,
                            class_name=BUTTON,
                        ),
                        class_name="mt-4 flex flex-wrap gap-2",
                    ),
                    rx.el.p(
                        "Restablecer elimina solo el ajuste guardado: vuelve a Cercano e Instagram. No elimina campañas. En otra pestaña, pulsa Volver a leer para ver cambios.",
                        class_name="mt-4 text-xs leading-6 text-gray-600",
                    ),
                    class_name=CARD,
                ),
                rx.el.section(
                    rx.el.h2(
                        "Integraciones · estado real",
                        class_name="mb-5 text-xl font-semibold text-[#242668]",
                    ),
                    rx.el.div(
                        information(
                            "file-text",
                            "Generación de textos local, no IA conectada",
                            "Plantillas deterministas ejecutadas en Python, sin llamadas a proveedores de IA. Son un punto de partida, no una verificación de datos ni promesas de resultados.",
                        ),
                        information(
                            "panels-top-left",
                            "Imágenes: plantillas Canvas",
                            "Tres composiciones gráficas en el navegador con tus textos, colores e imagen propia opcional. No generan fotografías con IA.",
                        ),
                        information(
                            "unplug",
                            "Adaptador de IA futura no activo",
                            "Existe un contrato de código para un posible adaptador; no hay un proveedor conectado, clave requerida ni botón para activarlo. Tampoco hay conexión a redes o publicación automática.",
                        ),
                        class_name="flex flex-col gap-5",
                    ),
                    class_name=CARD,
                ),
                rx.el.section(
                    rx.el.h2(
                        "Cómo usar Impulso, paso a paso",
                        class_name="mb-5 text-xl font-semibold text-[#242668]",
                    ),
                    rx.el.ol(
                        rx.el.li(
                            "Pulsa Crear. Describe negocio, producto, público y objetivo. Oferta y precio son opcionales; aporta solo condiciones reales."
                        ),
                        rx.el.li(
                            "En Contenido, revisa los tres titulares y elige uno. Guarda cada edición antes de copiar o salir. Regenerar sustituye los textos guardados por otra de tres variantes."
                        ),
                        rx.el.li(
                            "Las ideas de promoción no son ofertas. Define condiciones reales y confírmalas expresamente para incluirlas; puedes retirarlas."
                        ),
                        rx.el.li(
                            "Continúa al diseñador: elige plantilla y formato, ajusta textos y colores y selecciona una imagen propia si quieres. Se recorta al centro y se comprime."
                        ),
                        rx.el.li(
                            "Pulsa Guardar / actualizar para conservar la campaña. Descargar PNG solicita un archivo, pero no guarda la campaña ni publica en redes."
                        ),
                        rx.el.li(
                            "Abre Historial para recuperar una campaña, duplicarla o eliminarla con confirmación. Revisa el aviso de éxito; si hay error, no asumas que se guardó."
                        ),
                        class_name="list-decimal space-y-3 pl-5 text-sm leading-7 text-gray-600",
                    ),
                    rx.el.div(
                        rx.el.a(
                            "Crear una campaña",
                            href="/crear?nueva=1",
                            class_name=BUTTON,
                        ),
                        rx.el.a(
                            "Abrir historial",
                            href="/historial",
                            class_name=BUTTON,
                        ),
                        class_name="mt-6 flex flex-wrap gap-2",
                    ),
                    class_name=CARD,
                ),
                rx.el.section(
                    rx.el.h2(
                        "Privacidad y almacenamiento",
                        class_name="mb-5 text-xl font-semibold text-[#242668]",
                    ),
                    rx.el.div(
                        information(
                            "hard-drive",
                            "Local no significa copia de seguridad",
                            "Historial y preferencias usan localStorage, ligado al navegador y al origen del sitio. Cambiar de dominio, navegador o teléfono no mueve tus datos. Borrar datos del sitio, la navegación privada o la limpieza automática puede eliminarlos. No hay cuenta ni sincronización.",
                        ),
                        information(
                            "shield-check",
                            "No incluyas información sensible",
                            "Los textos y datos del negocio se envían al servidor Reflex para procesarlos en la sesión. Las imágenes se procesan y conservan solo en tu navegador. localStorage no está cifrado por la app: quien acceda al dispositivo o scripts del mismo sitio podría leerlo. No guardes claves ni datos personales de clientes.",
                        ),
                        information(
                            "wifi",
                            "Necesitas conexión para la sesión",
                            "No es una app completamente sin conexión. Usa conexión segura al publicarla. La tipografía Inter se carga desde Google Fonts; esa solicitud puede comunicar datos de conexión al proveedor. No se envían textos a un servicio de IA.",
                        ),
                        class_name="flex flex-col gap-5",
                    ),
                    class_name=CARD,
                ),
                rx.el.section(
                    rx.el.h2(
                        "Ayuda práctica",
                        class_name="mb-3 text-xl font-semibold text-[#242668]",
                    ),
                    help_detail(
                        "¿Dónde está mi campaña?",
                        "Comprueba que estás en el mismo navegador y dirección del sitio y abre Historial. Solo se conservan campañas guardadas expresamente desde el diseñador. Copiar texto o descargar PNG no guarda el historial. Si borraste los datos del sitio, no hay recuperación desde el servidor.",
                    ),
                    help_detail(
                        "No puedo guardar o el almacenamiento está lleno",
                        "Revisa permisos de almacenamiento del sitio y evita el modo privado. Reduce o quita la imagen; copia tus textos y descarga lo necesario antes de eliminar campañas. La cuota depende del navegador. No borres todos los datos para arreglar un error: perderías el historial.",
                    ),
                    help_detail(
                        "Preferencias dañadas o cambios en otra pestaña",
                        "Pulsa Volver a leer. Si el ajuste tiene formato incompatible, usa Restablecer solo preferencias y guarda de nuevo. El historial queda intacto. En Historial pulsa Actualizar; no hay actualización automática de la lista. Si hay conflicto de campaña, vuelve a abrir la versión guardada o guarda como copia.",
                    ),
                    help_detail(
                        "Copiar no funciona en mi teléfono",
                        "El portapapeles puede requerir HTTPS y permisos del navegador. Mantén pulsado el texto de la vista previa y copia manualmente. Guarda las ediciones antes de copiar. No se publica automáticamente en ninguna red.",
                    ),
                    help_detail(
                        "No veo el PNG o el texto no cabe",
                        "Espera al procesamiento de la imagen y revisa Descargas o Archivos del teléfono. Permite descargas para este sitio. Si el texto no cabe, acórtalo o cambia de plantilla/formato; no se exporta un diseño recortado. Usa JPG, PNG o WebP de hasta 20 MB; se rechazan SVG y archivos incompatibles.",
                    ),
                    help_detail(
                        "Salí del formulario o perdí la conexión",
                        "Mientras esta pestaña sigue abierta, volver al formulario conserva el borrador capturado. No se guarda automáticamente en disco: recargar o cerrar puede perder los cambios. Si la conexión Reflex falla, comprueba internet antes de reintentar. Guarda tu campaña desde el diseñador cuando termines.",
                    ),
                    class_name="lg:col-span-2 rounded-2xl border border-[#242668]/10 bg-white p-5 sm:p-7",
                ),
                class_name="mt-8 grid items-start gap-6 lg:grid-cols-2",
            ),
            class_name="mx-auto w-full max-w-7xl flex-1 px-5 py-8 sm:px-8 lg:px-12",
        ),
        footer(),
        class_name="flex min-h-dvh flex-col bg-[#F8F7F2] font-['Inter'] text-[#202126]",
    )
