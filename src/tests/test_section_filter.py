from src.ingestion.section_filter import filter_boilerplate_lines, is_boilerplate_line


def test_exhibit_line_is_boilerplate():
    assert is_boilerplate_line("Exhibit 10.1 STOCK OPTION GRANT NOTICE")


def test_supply_chain_line_is_not_boilerplate():
    line = (
        "We depend on a limited number of third party foundries and suppliers "
        "for our semiconductor manufacturing."
    )
    assert not is_boilerplate_line(line)


def test_filter_removes_exhibit_lines():
    raw = "Exhibit 10.1 Grant Notice\nReal risk factor about suppliers and manufacturing."
    filtered = filter_boilerplate_lines(raw)
    assert "Exhibit" not in filtered
    assert "suppliers" in filtered
