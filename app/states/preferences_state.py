import reflex as rx
import json
import logging
from typing import Any


TONES = ["Cercano", "Profesional", "Inspirador", "Divertido"]
NETWORKS = ["Instagram", "Facebook", "WhatsApp", "LinkedIn"]


def preferences_script(expression: str) -> str:
    return f"(async () => {{ try {{ for (let n=0; n<100 && !window.ImpulsoBrowser; n++) await new Promise(r=>setTimeout(r,50)); if (!window.ImpulsoBrowser) throw new Error('No se cargaron las preferencias. Recarga e intenta de nuevo.'); return {expression}; }} catch(e) {{ return JSON.stringify({{ok:false,error:e.message}}); }} }})()"


class PreferencesState(rx.State):
    tone: str = "Cercano"
    network: str = "Instagram"
    ready: bool = False
    notice: str = ""
    error: str = ""

    @rx.event
    def load_preferences(self):
        self.ready = False
        self.notice = ""
        self.error = ""
        return rx.call_script(
            preferences_script("window.ImpulsoBrowser.preferences('read')"),
            callback=PreferencesState.preferences_result,
        )

    @rx.event
    def save_preferences(self, form_data: dict[str, Any]):
        tone = str(form_data.get("tono", ""))
        network = str(form_data.get("red_social", ""))
        if tone not in TONES or network not in NETWORKS:
            self.error = "Selecciona un tono y una red de la lista."
            return
        self.ready = False
        encoded = json.dumps(
            {"version": 1, "tono": tone, "red_social": network}
        )
        return rx.call_script(
            preferences_script(
                f"window.ImpulsoBrowser.preferences('save', {encoded})"
            ),
            callback=PreferencesState.preferences_result,
        )

    @rx.event
    def restore_defaults(self):
        self.ready = False
        return rx.call_script(
            preferences_script("window.ImpulsoBrowser.preferences('reset')"),
            callback=PreferencesState.preferences_result,
        )

    @rx.event
    def preferences_result(self, raw: str):
        self.ready = True
        self.notice = ""
        self.error = ""
        try:
            result = json.loads(raw)
            if not result.get("ok"):
                self.error = str(
                    result.get("error", "No se guardaron las preferencias.")
                )
                return
            values = result["values"]
            if (
                values["tono"] not in TONES
                or values["red_social"] not in NETWORKS
            ):
                raise ValueError("Preferencias incompatibles")
            self.tone = values["tono"]
            self.network = values["red_social"]
            self.notice = result["notice"]
        except (ValueError, KeyError, TypeError, AttributeError) as e:
            logging.exception(f"Error: {e}")
            self.error = "No se pudieron leer las preferencias. Reintenta; no se modificó tu historial."
