from voxcausal.pii import contains_pii, scrub


def test_scrubs_all_kinds():
    text = ("Soy 12.345.678-9, mi correo es ana.perez@mail.cl, "
            "fono +56 9 8765 4321 y tarjeta 4111 1111 1111 1111")
    clean, n = scrub(text)
    assert n == 4
    assert not contains_pii(clean)
    for label in ("[RUT]", "[EMAIL]", "[TELEFONO]", "[TARJETA]"):
        assert label in clean


def test_clean_text_untouched():
    text = "El cliente pidió hablar con un supervisor tras 3 transferencias"
    assert scrub(text) == (text, 0)
    assert not contains_pii(text)
