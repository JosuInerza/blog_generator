from app.services.slug_service import generate_slug, ensure_unique, clear_store


def test_generate_slug_basic():
    assert generate_slug("My First Post") == "my-first-post"
    assert generate_slug("  Leading and   multiple   spaces ") == "leading-and-multiple-spaces"


def test_generate_slug_accents_and_punctuation():
    assert generate_slug("Café — A day!") == "cafe-a-day"


def test_generate_slug_empty_fallback():
    assert generate_slug("") == ""


def test_ensure_unique_basic():
    clear_store()
    s1 = ensure_unique("post")
    s2 = ensure_unique("post")
    s3 = ensure_unique("post")
    assert s1 == "post"
    assert s2 == "post-2"
    assert s3 == "post-3"
