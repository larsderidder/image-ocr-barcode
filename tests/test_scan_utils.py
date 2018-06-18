from image_ocr_barcode.cli import collect_paths


def test_collect_paths_filters(tmpdir):
    (tmpdir / "a.jpg").write("x")
    (tmpdir / "b.png").write("x")
    (tmpdir / "c.txt").write("x")

    found = collect_paths(str(tmpdir), ["*.jpg", "*.png"])
    assert len(found) == 2
    assert found[0].endswith("a.jpg")
    assert found[1].endswith("b.png")
