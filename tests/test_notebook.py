from investigation_notebook.notebook import add_timeline, new_case, render_markdown, set_conclusion


def test_timeline_is_sorted():
    case = new_case("CASE-1", "Test")
    add_timeline(case, "2026-07-19", "second")
    add_timeline(case, "2026-07-18", "first")
    assert [row["event"] for row in case["timeline"]] == ["first", "second"]


def test_render_markdown_contains_conclusion():
    case = new_case("CASE-1", "Test")
    set_conclusion(case, "Escalate.")
    assert "Escalate." in render_markdown(case)
