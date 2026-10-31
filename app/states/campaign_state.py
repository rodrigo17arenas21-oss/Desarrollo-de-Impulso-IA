import reflex as rx
from typing import Any
import json
import logging
import uuid
from datetime import datetime, timezone
from app.generation import generate_local, publication_text, PROMOTION_IDEAS


class CampaignState(rx.State):
    campaign: dict[str, str] = {
        "nombre_negocio": "",
        "tipo_negocio": "",
        "producto": "",
        "publico": "",
        "objetivo": "",
        "oferta": "",
        "precio": "",
        "tono": "Cercano",
        "red_social": "Instagram",
        "formato": "cuadrado",
    }
    errors: dict[str, str] = {
        "nombre_negocio": "",
        "tipo_negocio": "",
        "producto": "",
        "publico": "",
        "objetivo": "",
        "oferta": "",
        "precio": "",
        "tono": "",
        "red_social": "",
        "formato": "",
    }
    form_ready: bool = False
    form_notice: str = ""
    submitted: bool = False
    has_errors: bool = False
    texts: dict[str, str] = {
        "headline_1": "",
        "headline_2": "",
        "headline_3": "",
        "copy": "",
        "description": "",
        "cta": "",
        "hashtags": "",
        "promotion_idea": "",
    }
    content_ready: bool = False
    generating: bool = False
    content_error: str = ""
    content_notice: str = ""
    variant: int = 0
    selected_headline: str = "headline_1"
    promotion_confirmed: bool = False
    promotion_terms: str = ""
    promotion_error: str = ""
    promotion_kind: str = "paquete"
    missing_fields: list[str] = []

    campaign_id: str = ""
    created_at: str = ""
    updated_at: str = ""
    pending_terms: str = ""
    pending_approved: bool = False
    visual: dict[str, str] = {
        "template": "editorial",
        "format": "cuadrado",
        "headline": "",
        "subtext": "",
        "background": "#242668",
        "foreground": "#FFFFFF",
        "accent": "#EF755D",
        "initialized": "",
    }

    def _snapshot(self) -> dict:
        return {
            "version": 1,
            "id": self.campaign_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "campaign": dict(self.campaign),
            "texts": dict(self.texts),
            "selected_headline": self.selected_headline,
            "promotion_confirmed": self.promotion_confirmed,
            "promotion_terms": self.promotion_terms,
            "promotion_kind": self.promotion_kind,
            "variant": self.variant,
            "pending_terms": self.pending_terms,
            "pending_approved": self.pending_approved,
            "visual": dict(self.visual),
            "content_ready": self.content_ready,
        }

    def _restore(self, data: dict):
        if not isinstance(data, dict) or data.get("version") != 1:
            raise ValueError("Invalid campaign")
        business, texts = data.get("campaign"), data.get("texts")
        if not isinstance(business, dict) or not isinstance(texts, dict):
            raise ValueError("Invalid fields")
        if any(not isinstance(business.get(k), str) for k in self.campaign):
            raise ValueError("Missing business fields")
        if any(not isinstance(texts.get(k), str) for k in self.texts):
            raise ValueError("Missing text fields")
        headline = data.get("selected_headline", "headline_1")
        if headline not in ("headline_1", "headline_2", "headline_3"):
            raise ValueError("Invalid headline")
        self.campaign = {k: business[k] for k in self.campaign}
        self.texts = {k: texts[k] for k in self.texts}
        self.campaign_id = str(data.get("id", ""))
        self.created_at = str(data.get("created_at", ""))
        self.updated_at = str(data.get("updated_at", ""))
        self.selected_headline = headline
        self.promotion_terms = str(data.get("promotion_terms", ""))
        self.promotion_confirmed = data.get("promotion_confirmed") is True
        self.promotion_kind = (
            data.get("promotion_kind", "paquete")
            if data.get("promotion_kind") in PROMOTION_IDEAS
            else "paquete"
        )
        self.variant = int(data.get("variant", 0))
        self.pending_terms = str(data.get("pending_terms", ""))
        self.pending_approved = data.get("pending_approved") is True
        settings = data.get("visual", {})
        self.visual = {
            k: str(settings.get(k, v)) for k, v in self.visual.items()
        }
        self.content_ready = True
        self.submitted = True
        self.has_errors = False
        self.missing_fields = []
        self.content_error = ""
        self.content_notice = "Campaña restaurada desde este navegador. No se regeneraron tus textos."

    @rx.var
    def publication(self) -> str:
        return publication_text(
            self.texts,
            self.selected_headline,
            self.promotion_terms,
            self.promotion_confirmed,
        )

    @rx.event
    def load_form(self):
        from app.states.preferences_state import preferences_script

        self.form_ready = False
        self.form_notice = ""
        is_new = self.router.url.query_parameters.get("nueva") == "1"
        if is_new:
            self.campaign = {k: "" for k in self.campaign}
            self.campaign.update(
                {
                    "tono": "Cercano",
                    "red_social": "Instagram",
                    "formato": "cuadrado",
                }
            )
            self.texts = dict.fromkeys(self.texts, "")
            self.campaign_id = ""
            self.created_at = ""
            self.updated_at = ""
            self.content_ready = False
            self.submitted = False
            self.has_errors = False
            self.errors = dict.fromkeys(self.errors, "")
            self.promotion_confirmed = False
            self.promotion_terms = ""
            self.pending_terms = ""
            self.pending_approved = False
            self.variant = 0
            self.selected_headline = "headline_1"
            self.promotion_kind = "paquete"
            self.promotion_error = ""
            self.content_error = ""
            self.content_notice = ""
        encoded = json.dumps(self.campaign, ensure_ascii=True)
        owner = json.dumps(self.campaign_id)
        yield rx.call_script(
            preferences_script(
                f"window.ImpulsoBrowser.prepareForm({encoded}, {json.dumps(is_new)}, {owner})"
            ),
            callback=CampaignState.form_prepared,
        )

    @rx.event
    def form_prepared(self, raw: str):
        try:
            result = json.loads(raw)
            values = result.get("values")
            if not isinstance(values, dict) or any(
                not isinstance(values.get(k), str) for k in self.campaign
            ):
                raise ValueError("No se cargaron los valores del formulario")
            self.campaign = {k: values[k] for k in self.campaign}
            self.form_notice = str(result.get("notice", ""))
        except (ValueError, TypeError, AttributeError) as e:
            logging.exception(f"Error: {e}")
            self.form_notice = "No se cargaron las preferencias. Tus datos actuales se conservan; puedes elegir el tono y la red aquí."
        self.form_ready = True
        if self.router.url.query_parameters.get("nueva") == "1":
            yield rx.redirect("/crear", replace=True)

    @rx.event
    def load_content(self):
        self.missing_fields = [
            label
            for field, label in (
                ("nombre_negocio", "nombre del negocio"),
                ("producto", "producto o servicio"),
                ("publico", "público objetivo"),
                ("objetivo", "objetivo"),
            )
            if not self.campaign.get(field, "").strip()
        ]
        if self.missing_fields:
            self.content_ready = False
            self.content_error = ""
            return
        if not self.content_ready:
            yield CampaignState.generate_content

    @rx.event
    def generate_content(self):
        if self.generating:
            return
        self.content_error = ""
        self.content_notice = ""
        self.generating = True
        yield
        try:
            result = generate_local(dict(self.campaign), self.variant)
            result["promotion_idea"] = (
                self.texts["promotion_idea"]
                or PROMOTION_IDEAS[self.promotion_kind]
            )
            self.texts = result
            self.content_ready = True
            self.content_notice = "Borrador local listo. Revisa los datos y guarda cada edición antes de copiar."
        except Exception as e:
            logging.exception(f"Error: {e}")
            self.content_error = "No pudimos preparar el borrador. Tus datos y ediciones anteriores se conservan. Revisa el formulario o vuelve a intentar."
        finally:
            self.generating = False

    @rx.event
    def regenerate_content(self):
        self.variant += 1
        yield CampaignState.generate_content

    @rx.event
    def save_text(self, field: str, form_data: dict[str, Any]):
        if field not in self.texts or self.generating:
            return
        value = str(form_data.get("text", ""))
        if len(value) > 10000:
            self.content_error = (
                "La edición debe tener 10 000 caracteres o menos."
            )
            return
        if field != "hashtags" and not value.strip():
            self.content_error = "Este texto no puede quedar vacío."
            return
        self.texts[field] = value
        self.content_error = ""
        self.content_notice = "Edición guardada. La vista previa y la copia usan el texto guardado."
        if field == "promotion_idea":
            self.promotion_confirmed = False
            self.promotion_terms = ""
            self.content_notice = "Idea editada; sigue sin aprobar. Confirma condiciones reales para incluir una promoción."

    @rx.event
    def choose_headline(self, field: str):
        if field in ("headline_1", "headline_2", "headline_3"):
            self.selected_headline = field
            self.content_notice = "Titular seleccionado para la publicación."

    @rx.event
    def choose_promotion(self, kind: str):
        if kind in PROMOTION_IDEAS:
            self.promotion_kind = kind
            self.texts["promotion_idea"] = PROMOTION_IDEAS[kind]
            self.promotion_confirmed = False
            self.promotion_terms = ""
            self.promotion_error = ""
            self.content_notice = (
                "Idea seleccionada. No se ha añadido a la publicación."
            )

    @rx.event
    def confirm_promotion(self, form_data: dict[str, Any]):
        terms = str(form_data.get("terms", ""))
        if not terms.strip() or len(terms) > 1200:
            self.promotion_error = "Escribe las condiciones reales de la promoción (entre 1 y 1200 caracteres). No basta con aprobar una idea genérica."
            return
        if not form_data.get("approved"):
            self.promotion_error = "Confirma que las condiciones son reales y están autorizadas por tu negocio."
            return
        self.promotion_terms = terms
        self.pending_terms = terms
        self.pending_approved = True
        self.promotion_confirmed = True
        self.promotion_error = ""
        self.content_notice = "Promoción confirmada por ti. Sus condiciones exactas ya aparecen en la vista previa y en Copiar publicación."

    @rx.event
    def revoke_promotion(self):
        self.promotion_confirmed = False
        self.promotion_error = ""
        self.content_notice = "Promoción retirada de la publicación. La idea sigue siendo solo una propuesta."

    @rx.event
    def copy_text(self, field: str):
        text = (
            self.publication
            if field == "publication"
            else self.texts.get(field, "")
        )
        if not text.strip():
            self.content_error = "No hay texto para copiar en este campo. En WhatsApp no se añaden hashtags por defecto."
            return
        if field == "promotion_idea":
            text = f"IDEA NO APROBADA · NO PUBLICAR\n{text}"
        encoded = json.dumps(text, ensure_ascii=True).replace("<", "\\u003c")
        yield rx.call_script(
            f"(async () => {{ try {{ await navigator.clipboard.writeText({encoded}); return true; }} catch (e) {{ return false; }} }})()",
            callback=CampaignState.clipboard_result,
        )

    @rx.event
    def clipboard_result(self, success: bool):
        if success:
            self.content_error = ""
            self.content_notice = "Texto guardado copiado al portapapeles. No se ha publicado en ninguna red."
        else:
            self.content_error = "El navegador no permitió copiar. Selecciona el texto y cópialo manualmente; revisa los permisos del portapapeles."

    @staticmethod
    def _validate_fields(values: dict[str, str]) -> dict[str, str]:
        errors = dict.fromkeys(values, "")
        required = {
            "nombre_negocio": "Escribe el nombre de tu negocio para identificar la campaña.",
            "producto": "Cuéntanos qué producto o servicio quieres comunicar.",
            "publico": "Describe a quién quieres llegar; por ejemplo, familias de tu barrio.",
            "objetivo": "Elige qué quieres conseguir con esta publicación.",
        }
        for field, message in required.items():
            if not values.get(field, "").strip():
                errors[field] = message
        limits = {
            "nombre_negocio": 120,
            "tipo_negocio": 120,
            "producto": 240,
            "publico": 600,
            "oferta": 1200,
            "precio": 80,
        }
        for field, limit in limits.items():
            if len(values.get(field, "")) > limit:
                errors[field] = (
                    f"Acorta este texto a {limit} caracteres o menos."
                )
        choices = {
            "objetivo": [
                "",
                "Dar a conocer mi negocio",
                "Presentar un producto o servicio",
                "Recibir consultas",
                "Conseguir ventas",
                "Invitar a una visita",
            ],
            "tono": ["Cercano", "Profesional", "Inspirador", "Divertido"],
            "red_social": ["Instagram", "Facebook", "WhatsApp", "LinkedIn"],
            "formato": ["cuadrado", "vertical"],
        }
        for field, options in choices.items():
            if values.get(field, "") not in options:
                errors[field] = "Selecciona una de las opciones disponibles."
        return errors

    @rx.event
    def submit_campaign(self, form_data: dict[str, Any]):
        had_content = self.content_ready
        self.campaign = {
            field: (
                str(form_data.get(field, ""))
                if field in ("oferta", "precio")
                else str(form_data.get(field, "")).strip()
            )
            for field in self.campaign
        }
        self.errors = self._validate_fields(self.campaign)
        self.has_errors = any(self.errors.values())
        self.submitted = not self.has_errors
        if self.has_errors:
            yield rx.set_focus("form-errors")
            return
        if had_content:
            self.content_notice = "Datos del negocio actualizados. Tus textos y diseño se conservan; revisa su coherencia antes de publicar."
            yield rx.redirect("/contenido")
            return
        self.campaign_id = str(uuid.uuid4())
        self.created_at = datetime.now(timezone.utc).isoformat()
        self.updated_at = self.created_at
        self.visual = {
            "template": "editorial",
            "format": self.campaign["formato"],
            "headline": "",
            "subtext": "",
            "background": "#242668",
            "foreground": "#FFFFFF",
            "accent": "#EF755D",
            "initialized": "",
        }
        self.content_ready = False
        self.variant = 0
        self.selected_headline = "headline_1"
        self.promotion_confirmed = False
        self.promotion_terms = ""
        self.promotion_error = ""
        self.texts = dict.fromkeys(self.texts, "")
        self.content_notice = ""
        self.content_error = ""
        yield rx.redirect("/contenido")
