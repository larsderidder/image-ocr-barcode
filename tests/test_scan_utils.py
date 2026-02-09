from image_ocr_barcode.cli import collect_paths


def test_collect_paths_filters(tmp_path):
    (tmp_path / "a.jpg").write_text("x")
    (tmp_path / "b.png").write_text("x")
    (tmp_path / "c.txt").write_text("x")

    found = collect_paths(str(tmp_path), ["*.jpg", "*.png"])
    assert len(found) == 2
    assert found[0].endswith("a.jpg")
    assert found[1].endswith("b.png")
