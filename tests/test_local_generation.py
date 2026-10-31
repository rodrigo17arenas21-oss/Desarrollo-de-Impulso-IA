import reflex as rx
import unittest
from app.generation import (
    generate_local,
    publication_text,
    confirmed_promotion,
    PROMOTION_IDEAS,
    TEXT_KEYS,
)


class LocalGenerationTests(unittest.TestCase):
    def data(self) -> dict[str, str]:
        return {
            "nombre_negocio": "Café Sol",
            "tipo_negocio": "Cafetería",
            "producto": "Pan",
            "publico": "Vecinos del barrio",
            "objetivo": "Recibir consultas",
            "oferta": "",
            "precio": "",
            "tono": "Cercano",
            "red_social": "Instagram",
            "formato": "cuadrado",
        }

    def test_deterministic_exactly_three_headlines(self):
        result = generate_local(self.data())
        self.assertEqual(result, generate_local(self.data()))
        self.assertEqual(set(result), set(TEXT_KEYS))
        self.assertEqual(len({result[f"headline_{i}"] for i in (1, 2, 3)}), 3)
        self.assertNotEqual(result, generate_local(self.data(), 1))
        self.assertEqual(result, generate_local(self.data(), 3))

    def test_no_invented_claims_or_promotions(self):
        for variant in range(3):
            result = generate_local(self.data(), variant)
            text = " ".join(result.values()).lower()
            for claim in (
                "descuento",
                "%",
                "gratis",
                "garantizado",
                "testimonio",
                "artesanal",
                "orgánico",
                "hoy",
                "últimas",
                "mxn",
                "€",
                "paquete",
                "promoción",
                "mejor",
                "saludable",
            ):
                self.assertNotIn(claim, text)
            self.assertIn("Vecinos del barrio", result["copy"])
            self.assertIn("Pan", result["copy"])

    def test_offer_and_price_verbatim_and_attributed(self):
        data = self.data()
        data["oferta"] = "  Dos piezas por 50 MXN\nSolo martes.  "
        data["precio"] = " 30 MXN por pieza "
        result = generate_local(data)
        self.assertIn(
            f"Oferta aportada por el negocio:\n{data['oferta']}", result["copy"]
        )
        self.assertIn(
            f"Precio aportado por el negocio:\n{data['precio']}", result["copy"]
        )
        self.assertNotIn(data["oferta"], result["description"])

    def test_promotion_never_published_without_confirmation(self):
        result = generate_local(self.data())
        for idea in PROMOTION_IDEAS.values():
            self.assertEqual(confirmed_promotion(idea, False), "")
            self.assertNotIn(
                idea, publication_text(result, "headline_1", idea, False)
            )
        terms = "Paquete: dos panes por 50 MXN. Solo martes."
        self.assertIn(
            terms, publication_text(result, "headline_1", terms, True)
        )
        self.assertNotIn(
            terms, publication_text(result, "headline_1", terms, False)
        )
        self.assertEqual(confirmed_promotion("  ", True), "")

    def test_channel_tone_sector_objective_adaptation(self):
        original = generate_local(self.data())
        for field, value in (
            ("tipo_negocio", "Taller de reparación"),
            ("publico", "Estudiantes"),
            ("tono", "Profesional"),
            ("objetivo", "Invitar a una visita"),
            ("red_social", "LinkedIn"),
        ):
            with self.subTest(field=field):
                data = self.data()
                data[field] = value
                self.assertNotEqual(original, generate_local(data))
        data = self.data()
        data["red_social"] = "WhatsApp"
        result = generate_local(data)
        self.assertEqual(result["hashtags"], "")
        self.assertIn("Responde", result["cta"])
        for tone in ("Cercano", "Profesional", "Inspirador", "Divertido"):
            for channel in ("Instagram", "Facebook", "WhatsApp", "LinkedIn"):
                data.update(tono=tone, red_social=channel)
                self.assertEqual(len(generate_local(data)), 7)

    def test_all_tones_channels_and_variants_do_not_invent_terms(self):
        for tone in ("Cercano", "Profesional", "Inspirador", "Divertido"):
            for network in ("Instagram", "Facebook", "WhatsApp", "LinkedIn"):
                for variant in range(3):
                    with self.subTest(
                        tone=tone, network=network, variant=variant
                    ):
                        data = self.data()
                        data.update(tono=tone, red_social=network)
                        text = " ".join(
                            generate_local(data, variant).values()
                        ).lower()
                        for claim in (
                            "gratis",
                            "garantizado",
                            "%",
                            "mxn",
                            "descuento",
                            "últimas unidades",
                            "testimonio",
                        ):
                            self.assertNotIn(claim, text)

    def test_missing_data_rejected(self):
        for field in ("nombre_negocio", "producto", "publico", "objetivo"):
            data = self.data()
            data[field] = "  "
            with self.assertRaises(ValueError):
                generate_local(data)
        with self.assertRaises(ValueError):
            generate_local({})

    def test_publication_requires_nonblank_terms_and_confirmation(self):
        texts = generate_local(self.data())
        baseline = publication_text(texts, "headline_1")
        terms = "Dos panes por 50 MXN."
        for value in ("", "  ", "\n\t", terms):
            for approved in (False, True):
                with self.subTest(terms=value, approved=approved):
                    expected = value if approved and value.strip() else ""
                    self.assertEqual(
                        confirmed_promotion(value, approved), expected
                    )
                    publication = publication_text(
                        texts, "headline_1", value, approved
                    )
                    if expected:
                        self.assertEqual(
                            publication,
                            "\n\n".join(
                                (
                                    texts["headline_1"],
                                    texts["copy"],
                                    expected,
                                    texts["cta"],
                                    texts["hashtags"],
                                )
                            ),
                        )
                    else:
                        self.assertEqual(publication, baseline)
        self.assertEqual(
            publication_text(texts, "headline_1", terms, False), baseline
        )

    def test_changed_promotion_idea_is_not_publication_authorization(self):
        texts = generate_local(self.data())
        terms = "Dos panes por 50 MXN."
        baseline = publication_text(texts, "headline_1")
        for key, idea in PROMOTION_IDEAS.items():
            with self.subTest(idea=key):
                edited = {**texts, "promotion_idea": idea}
                self.assertEqual(
                    publication_text(edited, "headline_1"), baseline
                )
                self.assertEqual(
                    publication_text(edited, "headline_1", terms, False),
                    baseline,
                )
                approved = publication_text(edited, "headline_1", terms, True)
                self.assertIn(terms, approved)
                self.assertNotIn(idea, approved)
                self.assertEqual(texts, generate_local(self.data()))


if __name__ == "__main__":
    unittest.main()
