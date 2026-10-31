import reflex as rx
import unittest
from app.states.campaign_state import CampaignState


class CampaignValidationTests(unittest.TestCase):
    def valid_data(self) -> dict[str, str]:
        return {
            "nombre_negocio": "Mi negocio",
            "tipo_negocio": "",
            "producto": "Servicio de reparación",
            "publico": "Vecinos del barrio",
            "objetivo": "Recibir consultas",
            "oferta": "",
            "precio": "",
            "tono": "Cercano",
            "red_social": "Instagram",
            "formato": "cuadrado",
        }

    def test_required_fields_reject_whitespace(self):
        values = self.valid_data()
        for field in ("nombre_negocio", "producto", "publico", "objetivo"):
            with self.subTest(field=field):
                invalid = values.copy()
                invalid[field] = "   "
                self.assertTrue(CampaignState._validate_fields(invalid)[field])

    def test_offer_and_price_are_optional(self):
        values = self.valid_data()
        self.assertFalse(any(CampaignState._validate_fields(values).values()))
        self.assertEqual(values["oferta"], "")
        self.assertEqual(values["precio"], "")

    def test_invalid_options_rejected(self):
        for field in ("objetivo", "tono", "red_social", "formato"):
            with self.subTest(field=field):
                values = self.valid_data()
                values[field] = "opción desconocida"
                self.assertTrue(CampaignState._validate_fields(values)[field])

    def test_both_formats_are_valid(self):
        for format_name in ("cuadrado", "vertical"):
            values = self.valid_data()
            values["formato"] = format_name
            self.assertFalse(
                any(CampaignState._validate_fields(values).values())
            )

    def test_long_values_rejected(self):
        values = self.valid_data()
        values["oferta"] = "x" * 1201
        self.assertTrue(CampaignState._validate_fields(values)["oferta"])


if __name__ == "__main__":
    unittest.main()
