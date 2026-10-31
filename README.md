# Impulso IA · guía sencilla

Prepara textos y diseños para tu negocio. **Generación de textos local, no IA conectada. Las imágenes son plantillas Canvas. El adaptador de IA futura no está activo.** No hay publicación automática ni conexión a tus redes.

## Si estás en el teléfono

Para usar una instalación ya disponible, abre su dirección en tu navegador. No necesitas instalar Python ni crear una cuenta. Este documento no afirma que exista una dirección pública publicada.

1. Toca **Crear**. Describe negocio, producto, público y objetivo; oferta y precio son opcionales.
2. Revisa el contenido. Elige un titular y guarda cada edición antes de copiar. Regenerar sustituye los textos guardados por otra de tres variantes.
3. Una idea de promoción no es una oferta: escribe y confirma condiciones reales para incluirlas. Puedes retirarlas.
4. Continúa al diseñador: plantilla, formato, colores e imagen propia opcional. Los textos del diseño son independientes de los textos para publicar.
5. Toca **Guardar / actualizar** para conservar la campaña. **Descargar PNG** solo solicita un archivo; no guarda la campaña ni publica en redes. Revisa Descargas o Archivos en el teléfono.
6. En **Historial**, abre, duplica o elimina con confirmación. Cancelar no elimina nada.
7. El icono de ajustes abre **Configuración y ayuda**. Guarda tono y red predeterminados; se aplican al pulsar Crear, no al volver a una campaña en curso ni al abrir una guardada.

Los cambios del formulario se capturan temporalmente en la pestaña para volver desde Ajustes sin perder lo escrito. No es guardado automático en disco. Cerrar o recargar puede perder cambios sin guardar.

## Todas las pantallas

| Dirección | Para qué sirve |
| --- | --- |
| `/` | Inicio, ejemplo ilustrativo y explicación del proceso (`/#como-funciona`). |
| `/crear` | Formulario de diez campos; vuelve a la campaña en curso. |
| `/crear?nueva=1` | Inicia una nueva campaña y aplica preferencias. Después se limpia ese parámetro para que recargar no reinicie otra campaña. |
| `/contenido` | Tres titulares, texto principal, descripción corta, CTA, hashtags y propuestas de promoción; edición y copia. |
| `/diseno` | Tres plantillas Canvas, imagen propia, vista previa, guardar y descargar PNG. |
| `/historial` | Campañas guardadas en este navegador; abrir, actualizar lista, duplicar y eliminar. |
| `/configuracion` | Preferencias, estado real de integraciones, instrucciones, privacidad y ayuda. |

## Instalar y ejecutar tu propia copia

Esto requiere una computadora o un entorno de desarrollo con terminal; no basta un navegador de teléfono. Para principiantes, pide ayuda con la instalación y publicación. Usa Python **3.13**, acceso a internet y espacio para dependencias y compilación. La versión fijada en `requirements.txt` es Reflex 0.10.0. Reflex instala o prepara sus herramientas de frontend; **no es un proyecto React/Vite que se ejecute con npm run dev**. Node es opcional para nuestras pruebas JavaScript, no un servicio de IA.

Abre una terminal en la carpeta que contiene `requirements.txt` y `rxconfig.py`:

```sh
python -m venv .venv
```

Activa el entorno según tu computadora:

- macOS/Linux: `source .venv/bin/activate`
- Windows PowerShell: `.venv\Scripts\Activate.ps1`

Después:

```sh
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
reflex run
```

Abre la dirección que muestre Reflex. Mantén la terminal abierta. Detén la app con Ctrl+C. No necesitas claves de IA. Para probar desde el teléfono, computadora y teléfono deben poder comunicarse en la misma red y debes seguir la guía de acceso de red de Reflex; no expongas el entorno de desarrollo a internet. Un teléfono no puede acceder al localhost de otra computadora usando su propio localhost.

### Producción y compilación

En el entorno Python activado, desde la raíz:

```sh
reflex run --env prod
```

Compila y sirve la aplicación en modo producción; no la publica por sí solo. Para preparar los paquetes de producción con el comando de exportación de Reflex:

```sh
reflex export
```

Consulta `reflex export --help` y la documentación de tu versión para opciones y artefactos. Una exportación no equivale a una publicación y el frontend solo no sustituye al servidor Python. Estos comandos **no se ejecutaron en esta entrega**.

## Configuración

Desde `/configuracion` puedes guardar tono y red o **Restablecer solo preferencias** (Cercano e Instagram). No elimina el historial. **Volver a leer** recoge los cambios de otra pestaña. Cada campaña permite cambiar tono y red aunque hayas guardado valores predeterminados. Si el almacenamiento está bloqueado, se comunica el fallo y no se afirma que se guardó. Un ajuste dañado no se sobrescribe silenciosamente; restablecer ese ajuste es una decisión explícita.

No hay configuración de proveedores de IA ni un interruptor para activarlos. El contrato para un adaptador futuro no ejecuta un servicio externo.

## Qué archivos encontrarás

- `app/app.py`: entrada y registro de las seis rutas principales.
- `app/components/`: pantallas y UI reutilizable (inicio, formulario, contenido, diseñador/historial, ajustes y navegación).
- `app/states/`: estados y eventos de campaña, herramientas del navegador y preferencias.
- `app/generation.py`: plantillas deterministas de texto y reglas de publicación.
- `app/browser_scripts.py`: preferencias, borrador temporal, almacenamiento de historial y herramientas Canvas en el navegador.
- `assets/`: recursos visuales de la interfaz; las imágenes del usuario no se guardan aquí.
- `tests/`: validación, veracidad de contenido y pruebas de JavaScript con Node si está disponible.
- `requirements.txt` y `rxconfig.py`: dependencias y configuración de Reflex.

## Publicar de forma viable, sin promesas de precio

**No se ha publicado esta app en esta entrega.** Consulta [Reflex](https://reflex.dev/docs/) y [Reflex Publish](https://reflex.dev/) para el flujo vigente de publicación. Los nombres de los servicios, cuotas, disponibilidad de planes gratuitos y condiciones pueden cambiar: **verifica hoy si existe un nivel gratuito y sus límites antes de aceptar cargos**. No hay precios ni gratuidad garantizada en esta guía.

Un camino práctico:

1. Ejecuta y prueba la app localmente con este README.
2. Revisa la guía de publicación correspondiente a Reflex 0.10.0. Usa el flujo guiado de Publish si está disponible para tu cuenta; consulta `reflex --help` para las opciones de despliegue de la CLI instalada. La disponibilidad del flujo no se ha verificado aquí.
3. Inicia sesión en el proveedor si lo pide, conecta tu proyecto y sigue su guía para una app Reflex con Python. Revisa plan, recursos, HTTPS y condiciones antes de confirmar. No compartas credenciales ni las incluyas en el código.
4. Como alternativa, usa una plataforma que ejecute Python de forma persistente y soporte WebSocket además de servir el frontend generado por Reflex. Sigue su guía de Reflex; un alojamiento solo de archivos estáticos no es suficiente para los eventos Python.
5. Compila/exporta con Reflex según la plataforma y comprueba que la sesión funciona por HTTPS. Verifica desde un teléfono crear → contenido → diseño → guardar → abrir historial antes de anunciarla.
6. Recuerda: cambiar la dirección del sitio no traslada localStorage. Conserva manualmente textos y PNG antes de cambiar de dominio.

No se proporcionan credenciales ni se afirma tener cuenta, plan, URL pública o publicación completada.

## Privacidad, límites y posibles costos

- Historial y preferencias persisten en **localStorage**: mismo navegador y origen del sitio. No hay copia de seguridad, cuenta, sincronización de dispositivos ni base de datos de campañas. Las pestañas comparten almacenamiento pero no actualizan automáticamente sus listas.
- localStorage no está cifrado por la app. Un dispositivo compartido o scripts del mismo sitio pueden acceder a él. No introduzcas datos sensibles, claves ni datos personales de clientes.
- Los datos del negocio y textos se procesan en el servidor Reflex durante la sesión. Las imágenes se leen, redimensionan y conservan únicamente en el navegador. No se envían a un servicio de IA. Inter se solicita a Google Fonts, que puede recibir datos de conexión; la app no es completamente sin conexión.
- Se aceptan JPG/PNG/WebP de hasta 20 MB, con límite de 50 millones de píxeles. Se redimensionan a un máximo de 1440 px y comprimen como JPEG: puede cambiar calidad/transparencia. El diseño usa recorte central.
- PNG de 1080×1080 o 1080×1920. El texto demasiado largo produce un error en vez de exportar contenido recortado. La app confirma la solicitud de descarga, no la escritura en disco.
- El navegador decide la cuota de almacenamiento. Imágenes, muchas campañas, modo privado o bloqueo de almacenamiento pueden impedir guardar. Borrar datos del sitio puede eliminar todo; no hay recuperación desde el servidor.
- Guardar puede detectar que otra pestaña actualizó la misma campaña y evitar sobrescribirla. Eso no es sincronización en tiempo real ni garantía de transacciones entre pestañas.
- Hay tres variantes deterministas, no creatividad ilimitada ni verificación externa de condiciones. No se inventan precios, descuentos ni testimonios; revisa todo antes de comunicarlo.
- Costos posibles: alojamiento Python, memoria/CPU, compilaciones, tráfico, dominio y servicios elegidos por el proveedor. Más sesiones aumentan los recursos necesarios. La versión actual no consume tokens de IA ni APIs pagadas de generación. Una futura integración podría generar cargos por tokens/imágenes y exigir credenciales; **no está activa**.

## Problemas frecuentes

- **No encuentra reflex:** activa el entorno virtual y reinstala `requirements.txt` con el mismo Python.
- **Falla la instalación/compilación:** verifica Python, conexión y espacio libre; lee el primer error de la terminal. Usa la versión fijada, no una actualización improvisada. La primera compilación puede tardar.
- **Pantalla desconectada:** comprueba que el servidor sigue ejecutándose y que la red funciona. Una plataforma de producción debe permitir sesiones WebSocket. No confundas frontend visible con servidor operativo.
- **Preferencias no se guardan:** habilita almacenamiento para el sitio, vuelve a leer y revisa el aviso. Si están dañadas, restablece solo preferencias. No borres el historial como solución.
- **Historial vacío:** confirma navegador/dirección y que pulsaste Guardar. Recargar no guarda cambios pendientes.
- **Historial dañado:** no se sobrescribe ni borra automáticamente. Conserva una copia antes de cualquier limpieza; no hay recuperación automática.
- **No hay espacio:** copia textos y descarga PNG primero; quita/reduce la imagen o elimina campañas que ya no necesites.
- **No copia:** usa HTTPS y revisa permisos. Selecciona el texto de la vista previa y cópialo manualmente.
- **PNG ausente:** revisa Descargas/Archivos y permisos. Espera a la imagen; acorta textos si no caben. No se puede confirmar desde la app que el teléfono guardó el archivo.
- **Conflicto entre pestañas:** actualiza Historial, vuelve a abrir la versión vigente o guarda como copia. No se actualizan las pantallas en tiempo real.

## Pruebas y estado de entrega: sin confundir código con verificación

Para ejecutar las pruebas:

```sh
python -m unittest discover -s tests -v
```

**Implementado:** seis pantallas, validaciones, generación local editable, autorización explícita de promociones, diseñador Canvas, persistencia de campañas, historial con acciones, preferencias para campañas nuevas y ayuda/privacidad. Ajustes tiene guardar, restablecer y volver a leer; la navegación usa enlaces reales. No hay botones de conexión ficticia.

**Suite ampliada ejecutada (según los resultados proporcionados):** `python -m unittest discover -s tests -v` terminó con **23 ejecuciones aprobadas (OK)**. Algunas pruebas se ejecutaron más de una vez por importaciones entre módulos de prueba; no son 23 casos únicos. La cobertura incluye validación del formulario; generación local y veracidad de textos en todos los tonos, redes y variantes; autorización de promociones; fixture serializable; preferencias persistidas y errores de versión/JSON/opciones/cuota/permisos; borrador sin enviar y campañas restauradas sin sobreescritura; restablecimiento sin borrar historial; acciones del historial y guardado mediante DOM simulado (abrir, duplicar, cancelar/eliminar, actualizar, guardar copia, conflicto y reintento); rechazo de IDs duplicados antes de escribir; montaje tardío del DOM y fallo acotado si no aparece. Node ejecutó el JavaScript real con DOM y almacenamiento simulados: **no es una prueba de interacción en un navegador real**. Si Node falta, esas pruebas se omiten explícitamente. La suite no requiere `test_utils` ni instanciar estados Reflex directamente.

**Comprobaciones independientes de eventos Reflex aprobadas:** en el entorno de comprobación con `run_event`, se verificaron envío válido y validación de errores del formulario; generación local, aprobación explícita de promociones y manejo del error de portapapeles; restauración de una instantánea de campaña; y resultados de preferencias, incluido un error sin pérdida de selección. Son comprobaciones de eventos aislados, no un recorrido completo por la interfaz ni una prueba de guardado y recarga en un navegador real.

**Renderizado confirmado mediante capturas:** `/`, `/crear`, `/contenido` con datos faltantes, `/configuracion`, `/diseno` sin campaña y `/historial` vacío. Las capturas finales del diseñador y del historial muestran sus estados resueltos, no solo el mensaje de carga. Esta evidencia confirma esas pantallas y estados, pero no sus interacciones ni su presentación a ancho móvil.

**Credenciales necesarias:** ninguna para los flujos actuales ni para ejecutar localmente; solo las de una cuenta de alojamiento si decides publicar. No se necesitan credenciales de redes o IA. Nunca las compartas ni las subas al proyecto.

**No verificado en esta entrega:** interacción real en navegador, navegación con teclado, ancho móvil, carga/lectura de imágenes aportadas por el usuario, portapapeles real y descarga efectiva del PNG. Sigue pendiente el recorrido manual completo crear → contenido → diseñador → guardar → recargar → abrir con imagen/ediciones/aprobación; tres plantillas en ambos formatos; preferencias → nueva campaña frente a retorno al borrador/restaurada; eliminación cancelada/confirmada; error de cuota/permisos y conflicto de dos pestañas en un navegador real. Las simulaciones Node, los eventos aislados y las capturas no sustituyen esas pruebas de extremo a extremo. Tampoco se ejecutaron los comandos de modo producción o exportación ni se verificó la disponibilidad actual de planes gratuitos. **No hay un despliegue publicado en esta entrega.**

**Problemas y límites conocidos:** pérdida de cambios al cerrar/recargar sin guardar, cuota dependiente del navegador, datos ligados al origen, ausencia de copias de seguridad y sincronización, descargas/permisos dependientes del teléfono, riesgo de escrituras simultáneas entre pestañas. Se corrigió el rechazo ausente de IDs duplicados en la escritura del historial y se añadió conservación temporal del formulario al visitar Ajustes. También se corrigió la inicialización del diseñador y del historial cuando el DOM se monta después de la llamada inicial: ahora se espera su montaje con un límite y se comunica el fallo si no aparece. La suite cubre ese montaje tardío y su fallo acotado; las capturas finales confirman los estados sin campaña e historial vacío. No se afirma que no existan otros fallos hasta ejecutar las comprobaciones pendientes.
