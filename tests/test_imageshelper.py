import base64

import pytest

from openai_messages_token_helper import count_tokens_for_image


@pytest.fixture
def small_image():
    return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z/C/HgAGgwJ/lK3Q6wAAAABJRU5ErkJggg=="


@pytest.fixture
def large_image():
    large_image = open("tests/image_large.png", "rb").read()
    img = base64.b64encode(large_image).decode("utf-8")
    return f"data:image/png;base64,{img}"


def test_count_tokens_for_image(small_image, large_image):
    assert count_tokens_for_image(small_image, "low") == 85
    assert count_tokens_for_image(small_image, "low", "gpt-4o-mini") == 2833
    assert count_tokens_for_image(small_image, "high") == 255
    assert count_tokens_for_image(small_image) == 255
    assert count_tokens_for_image(large_image, "low") == 85
    assert count_tokens_for_image(large_image, "high") == 1105
    with pytest.raises(ValueError, match="Invalid value for detail parameter."):
        assert count_tokens_for_image(large_image, "medium")
    with pytest.raises(ValueError, match="Image must be a base64 string."):
        assert count_tokens_for_image("http://domain.com/image.png")
