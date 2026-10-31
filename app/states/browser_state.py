import reflex as rx
import json
import logging
from app.states.campaign_state import CampaignState


def script_call(expression: str, report_errors: bool = False) -> str:
    operation = f"for (let n = 0; n < 100 && !window.ImpulsoBrowser; n++) await new Promise(r => setTimeout(r, 50)); if (!window.ImpulsoBrowser) throw new Error('No se cargaron las herramientas locales. Recarga la página o vuelve a intentar.'); return await {expression};"
    if report_errors:
        operation = f"try {{ {operation} }} catch (e) {{ return JSON.stringify({{mount_error: e.message || 'No se pudo preparar esta pantalla. Recarga la página o vuelve a intentar.'}}); }}"
    return f"(async () => {{ {operation} }})()"


class BrowserState(rx.State):
    notice: str = ""

    @rx.event
    def load_history(self):
        self.notice = ""
        return rx.call_script(
            script_call("window.ImpulsoBrowser.history()", report_errors=True),
            callback=BrowserState.mount_result,
        )

    @rx.event
    def mount_result(self, raw: str):
        try:
            result = json.loads(raw) if raw else {}
            self.notice = str(result.get("mount_error", ""))
        except (ValueError, TypeError, AttributeError) as e:
            logging.exception(f"Error: {e}")
            self.notice = "No se pudo preparar esta pantalla. Recarga la página o vuelve a intentar."

    @rx.event
    async def load_designer(self):
        self.notice = ""
        campaign = await self.get_state(CampaignState)
        encoded = json.dumps(campaign._snapshot(), ensure_ascii=True).replace(
            "<", "\\u003c"
        )
        return rx.call_script(
            script_call(
                f"window.ImpulsoBrowser.resolve({encoded})", report_errors=True
            ),
            callback=BrowserState.resolve_result,
        )

    @rx.event
    async def resolve_result(self, raw: str):
        campaign = await self.get_state(CampaignState)
        try:
            data = json.loads(raw)
            if isinstance(data, dict) and data.get("mount_error"):
                self.notice = str(data["mount_error"])
                return
            if data:
                campaign._restore(data)
            encoded = json.dumps(
                campaign._snapshot(), ensure_ascii=True
            ).replace("<", "\\u003c")
            self.notice = ""
            yield rx.call_script(
                script_call(
                    f"window.ImpulsoBrowser.designer({encoded})",
                    report_errors=True,
                ),
                callback=BrowserState.mount_result,
            )
        except (ValueError, TypeError, KeyError, AttributeError) as e:
            logging.exception(f"Error: {e}")
            self.notice = "No se pudo restaurar la campaña. El historial original no se ha modificado."

    @rx.event
    def open_saved(self):
        return rx.call_script(
            script_call("window.ImpulsoBrowser.consumeOpen()"),
            callback=BrowserState.open_result,
        )

    @rx.event
    async def open_result(self, raw: str):
        campaign = await self.get_state(CampaignState)
        try:
            campaign._restore(json.loads(raw))
            self.notice = ""
            yield rx.redirect("/diseno")
        except (ValueError, TypeError, KeyError) as e:
            logging.exception(f"Error: {e}")
            self.notice = (
                "No se pudo abrir la campaña. No se ha cambiado el historial."
            )

    @rx.event
    def to_designer(self):
        return rx.call_script(
            script_call("window.ImpulsoBrowser.captureContent()"),
            callback=BrowserState.content_captured,
        )

    @rx.event
    async def content_captured(self, raw: str):
        campaign = await self.get_state(CampaignState)
        try:
            drafts = json.loads(raw)
            for field, value in drafts.get("texts", {}).items():
                if (
                    field in campaign.texts
                    and isinstance(value, str)
                    and len(value) <= 10000
                ):
                    campaign.texts[field] = value
            campaign.pending_terms = str(
                drafts.get("pending_terms", campaign.promotion_terms)
            )[:1200]
            campaign.pending_approved = bool(
                drafts.get("pending_approved", False)
            )
            encoded = json.dumps(
                campaign._snapshot(), ensure_ascii=True
            ).replace("<", "\\u003c")
            yield rx.call_script(
                script_call(f"window.ImpulsoBrowser.receive({encoded})")
            )
            yield rx.redirect("/diseno")
        except (ValueError, TypeError) as e:
            logging.exception(f"Error: {e}")
            self.notice = "No se pudieron recoger las ediciones; permanece en esta pantalla y vuelve a intentar."

    @rx.event
    def sync_editor(self):
        return rx.call_script(
            script_call("window.ImpulsoBrowser.editorData()"),
            callback=BrowserState.editor_synced,
        )

    @rx.event
    async def editor_synced(self, raw: str):
        campaign = await self.get_state(CampaignState)
        try:
            campaign._restore(json.loads(raw))
            yield rx.redirect("/contenido")
        except (ValueError, TypeError, KeyError) as e:
            logging.exception(f"Error: {e}")
            self.notice = "No se pudo abrir el contenido. Tus cambios siguen en el diseñador."
