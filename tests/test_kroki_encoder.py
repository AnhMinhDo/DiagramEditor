from source.kroki_encoder import KrokiEncoder

def test_text_diagram_to_kroki_url() -> None:
    diag: KrokiEncoder = KrokiEncoder("./tests/test_data/text_diagram.txt","plantuml", "png")
    output_link: str = diag._text_diagram_to_kroki_url("./tests/test_data/text_diagram.txt","plantuml", "png")
    assert output_link == "https://kroki.io/plantuml/png/eNplkE1qwzAQhdfRKQa6SfCmP_QAJjElLSXBuGsh5IktJEtCUqCl-O6V7CC7ZJbfzLz3ZrwU2jLHBnBMS48WXh6Jz7C1Ap6eX1fEMi5Zh40ICkslOj2gDqDwEgiZIByO5VtdftLqcGxONZzr03u1bwi5bcLeOPwKQsEvgVhcMe_hwxkpKs1Ni-7WSFVchEJqWegXhN8BtRdGL6gVrIvhaPixuFCZNOnVqQWJISaY9TJ8oLxHLmm22u7uesvev2aIWWg2NzQ7bnewGpuxQ2-N9pgGJ72VVHG1LQuJTGgkq9fsU4JztF7_JUUBstkULSoMOVoEvGf6Pmsx37GiIxn_AJwmlXU="
