import reflex as rx
import re
import unicodedata
from typing import Protocol


TEXT_KEYS = (
    "headline_1",
    "headline_2",
    "headline_3",
    "copy",
    "description",
    "cta",
    "hashtags",
)
PROMOTION_IDEAS = {
    "descuento": "Evaluar un descuento para este producto o servicio. El negocio debe definir y confirmar importe, elegibilidad y condiciones antes de comunicarlo.",
    "paquete": "Evaluar un paquete de productos o servicios. El negocio debe confirmar qué incluye, disponibilidad, precio y condiciones antes de comunicarlo.",
    "tiempo": "Evaluar una promoción de tiempo limitado. El negocio debe confirmar el beneficio y las fechas reales antes de comunicarla.",
    "nuevo": "Evaluar una propuesta para nuevos clientes. El negocio debe definir el beneficio, quién puede acceder y las condiciones antes de comunicarla.",
    "lealtad": "Evaluar una propuesta de lealtad para clientes habituales. El negocio debe definir requisitos, beneficio y condiciones antes de comunicarla.",
}


class ContentGenerator(Protocol):
    """Contract for a future adapter; the current implementation is local only."""

    def generate(
        self, campaign: dict[str, str], variant: int = 0
    ) -> dict[str, str]: ...


def sector_context(business_type: str) -> tuple[str, str]:
    normalized = unicodedata.normalize("NFKD", business_type.lower())
    normalized = "".join(c for c in normalized if not unicodedata.combining(c))
    groups = (
        (
            ("cafe", "cafeter", "panad", "restaur", "comida", "pastel"),
            "Para tu mesa y tus encuentros",
            "Gastronomia",
        ),
        (
            ("belleza", "peluquer", "estet", "barber"),
            "Para tus momentos de cuidado personal",
            "CuidadoPersonal",
        ),
        (
            ("ropa", "moda", "boutique", "calzado"),
            "Para explorar tu estilo",
            "Moda",
        ),
        (
            ("repar", "taller", "mecanic", "tecnic"),
            "Para tus necesidades de mantenimiento",
            "Servicios",
        ),
        (
            ("educ", "curso", "academ", "clases"),
            "Para tus intereses de aprendizaje",
            "Educacion",
        ),
        (
            ("salud", "medic", "dental", "terapia"),
            "Información para tus consultas de salud",
            "Salud",
        ),
    )
    for keywords, context, tag in groups:
        if any(keyword in normalized for keyword in keywords):
            return context, tag
    return "Conoce nuestra propuesta", "Negocios"


def hashtag(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text)
    ascii_text = "".join(c for c in normalized if not unicodedata.combining(c))
    words = re.findall(r"[A-Za-z0-9]+", ascii_text)
    return (
        f"#{''.join(word.capitalize() for word in words)[:45]}"
        if words
        else "#Negocios"
    )


def confirmed_promotion(terms: str, confirmed: bool) -> str:
    return terms if confirmed and terms.strip() else ""


def publication_text(
    texts: dict[str, str],
    headline: str,
    terms: str = "",
    confirmed: bool = False,
) -> str:
    parts = [
        texts.get(headline, ""),
        texts.get("copy", ""),
        texts.get("cta", ""),
        texts.get("hashtags", ""),
    ]
    approved = confirmed_promotion(terms, confirmed)
    if approved:
        parts.insert(2, approved)
    return "\n\n".join(part for part in parts if part.strip())


class LocalContentGenerator:
    def generate(
        self, campaign: dict[str, str], variant: int = 0
    ) -> dict[str, str]:
        required = ("nombre_negocio", "producto", "publico", "objetivo")
        missing = [key for key in required if not campaign.get(key, "").strip()]
        if missing:
            raise ValueError(f"Faltan datos: {', '.join(missing)}")
        name = campaign["nombre_negocio"]
        product = campaign["producto"]
        audience = campaign["publico"]
        sector = campaign.get("tipo_negocio", "")
        context, sector_tag = sector_context(sector)
        tone = campaign.get("tono", "Cercano")
        channel = campaign.get("red_social", "Instagram")
        objective = campaign["objetivo"]
        intros = {
            "Cercano": (
                f"Hola, somos {name}.",
                f"Te damos la bienvenida a {name}.",
                f"Queremos que conozcas {name}.",
            ),
            "Profesional": (
                f"Presentamos la propuesta de {name}.",
                f"Información de {name}.",
                f"Conozca la oferta de productos o servicios de {name}.",
            ),
            "Inspirador": (
                f"Una idea para explorar: {name}.",
                f"Conoce una nueva propuesta: {name}.",
                f"Tu próxima consulta puede empezar en {name}.",
            ),
            "Divertido": (
                f"¡Hablemos de {name}!",
                f"¡{name} tiene algo que contar!",
                f"¿Ya conoces {name}?",
            ),
        }
        index = variant % 3
        intro = intros.get(tone, intros["Cercano"])[index]
        body = (
            f"Producto o servicio: {product}.\nDirigido a: {audience}.",
            f"Para quienes se identifican con este público: {audience}.\nTe presentamos: {product}.",
            f"Esta publicación está dirigida a: {audience}.\nConoce nuestra propuesta: {product}.",
        )[index]
        purpose = {
            "Dar a conocer mi negocio": "Queremos presentarte nuestro negocio.",
            "Presentar un producto o servicio": "Queremos compartir información sobre este producto o servicio.",
            "Recibir consultas": "Puedes consultarnos tus dudas sobre esta propuesta.",
            "Conseguir ventas": "Consúltanos cómo comprar o contratar esta propuesta.",
            "Invitar a una visita": "Consulta cómo visitarnos y conocer esta propuesta.",
        }.get(objective, "Consulta más información sobre nuestra propuesta.")
        contact = {
            "Instagram": "Envíanos un mensaje directo",
            "Facebook": "Escríbenos por mensaje privado",
            "WhatsApp": "Responde a este mensaje",
            "LinkedIn": "Contacta con nosotros por mensaje",
        }.get(channel, "Escríbenos")
        actions = {
            "Dar a conocer mi negocio": "para conocer el negocio",
            "Presentar un producto o servicio": "para saber más sobre esta propuesta",
            "Recibir consultas": "con tus preguntas",
            "Conseguir ventas": "para consultar cómo comprar o contratar",
            "Invitar a una visita": "para consultar ubicación y horarios de visita",
        }
        cta = f"{contact} {actions.get(objective, 'para pedir información')}."
        if tone == "Profesional":
            cta = f"{cta} Con gusto atenderemos su consulta."
        elif tone == "Divertido":
            cta = f"¿Hablamos? {cta}"
        elif tone == "Inspirador":
            cta = f"Da el siguiente paso: {cta}"
        details = [intro, context, body, purpose]
        if sector.strip():
            details.insert(2, f"Tipo de negocio: {sector}.")
        offer = campaign.get("oferta", "")
        if offer.strip():
            details.append(f"Oferta aportada por el negocio:\n{offer}")
        price = campaign.get("precio", "")
        if price.strip():
            details.append(f"Precio aportado por el negocio:\n{price}")
        headlines = (
            (
                f"Conoce {name}",
                f"{product} · {name}",
                f"{name}: una propuesta para conocer",
            ),
            (
                f"Te presentamos {product}",
                f"Descubre la propuesta de {name}",
                f"Hablemos de {product}",
            ),
            (
                f"¿Conoces {name}?",
                f"Más información sobre {product}",
                f"Tu consulta empieza en {name}",
            ),
        )[index]
        if tone == "Profesional":
            headlines = (
                (
                    f"Presentación de {name}",
                    f"Información sobre {product}",
                    f"La propuesta de {name}",
                )
                if index == 0
                else headlines
            )
        elif tone == "Divertido":
            headlines = tuple(f"¡{h}!" for h in headlines)
        tags = [hashtag(name), f"#{sector_tag}", "#ConoceNuestroNegocio"]
        if channel == "LinkedIn":
            tags = [hashtag(name), f"#{sector_tag}"]
        elif channel == "Facebook":
            tags = [hashtag(name), f"#{sector_tag}"]
        elif channel == "WhatsApp":
            tags = []
        return {
            "headline_1": headlines[0],
            "headline_2": headlines[1],
            "headline_3": headlines[2],
            "copy": "\n\n".join(details),
            "description": f"{name} · {product}. {context}. Público: {audience}.",
            "cta": cta,
            "hashtags": " ".join(dict.fromkeys(tags)),
        }


def generate_local(
    campaign: dict[str, str], variant: int = 0
) -> dict[str, str]:
    generator: ContentGenerator = LocalContentGenerator()
    return generator.generate(campaign, variant)
