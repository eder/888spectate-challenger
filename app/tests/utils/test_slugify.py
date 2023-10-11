from utils.slugify import to_slug

def test_to_slug():
    assert to_slug("Hello World! How are you?") == "hello-world-how-are-you"
    assert to_slug("TEST") == "test"
    assert to_slug("123 !@#") == "123"
    assert to_slug("     Spaces before and after     ") == "spaces-before-and-after"
    assert to_slug("Today! Is! The day!") == "today-is-the-day"

