import argparse
import json
import os
from typing import Iterable, List, Optional


class ScanOptions:
    """Runtime options for an image scan session."""

    def __init__(self, patterns, limit, ocr, barcodes, gcv, lang, emit_json):
        self.patterns = patterns
        self.limit = limit
        self.ocr = ocr
        self.barcodes = barcodes
        self.gcv = gcv
        self.lang = lang
        self.emit_json = emit_json


def collect_paths(root: str, patterns: Iterable[str]) -> List[str]:
    """Collect image paths from a root directory matching patterns."""
    matches: List[str] = []
    for base, _, files in os.walk(root):
        for name in files:
            for pattern in patterns:
                if _match_pattern(name, pattern):
                    matches.append(os.path.join(base, name))
                    break
    return sorted(matches)


def _match_pattern(name: str, pattern: str) -> bool:
    """Match simple filename patterns like '*.jpg'."""
    if pattern.startswith("*."):
        return name.lower().endswith(pattern[1:].lower())
    return name == pattern


def _maybe_google_client():
    """Create a Google Vision client when available."""
    try:
        from google.cloud import vision
    except Exception:
        return None
    return vision.ImageAnnotatorClient()


def _scan_ocr(image, lang: str) -> str:
    """Run OCR on an image."""
    import pytesseract

    return pytesseract.image_to_string(image, lang=lang)


def _scan_barcodes(image) -> List[str]:
    """Decode barcodes from an image."""
    from pyzbar.pyzbar import decode

    results = []
    for item in decode(image):
        try:
            results.append(item.data.decode("utf-8"))
        except Exception:
            results.append(str(item.data))
    return results


def _scan_gcv(image, client) -> dict:
    """Run Google Cloud Vision label/logo/text detection."""
    if client is None:
        return {}
    from google.cloud.vision import Image as VisionImage

    content = image.tobytes()
    payload = VisionImage(content=content)

    labels = client.label_detection(image=payload).label_annotations
    logos = client.logo_detection(image=payload).logo_annotations
    texts = client.text_detection(image=payload).text_annotations

    return {
        "labels": [label.description for label in labels],
        "logos": [logo.description for logo in logos],
        "texts": [text.description for text in texts],
    }


def scan_image(path: str, options: ScanOptions, gcv_client) -> dict:
    """Scan an image file and return structured results."""
    from PIL import Image

    image = Image.open(path)
    result = {
        "path": path,
        "ocr": None,
        "barcodes": [],
        "gcv": {},
    }

    if options.ocr:
        result["ocr"] = _scan_ocr(image, options.lang)

    if options.barcodes:
        result["barcodes"] = _scan_barcodes(image)

    if options.gcv:
        result["gcv"] = _scan_gcv(image, gcv_client)

    return result


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(description="Scan images for OCR and barcodes")
    parser.add_argument("path", help="Directory containing images")
    parser.add_argument("--pattern", action="append", default=["*.jpg", "*.jpeg", "*.png", "*.tif", "*.tiff"])
    parser.add_argument("--limit", type=int)
    parser.add_argument("--ocr", action="store_true", default=True)
    parser.add_argument("--no-ocr", action="store_false", dest="ocr")
    parser.add_argument("--barcodes", action="store_true", default=True)
    parser.add_argument("--no-barcodes", action="store_false", dest="barcodes")
    parser.add_argument("--gcv", action="store_true")
    parser.add_argument("--lang", default="eng")
    parser.add_argument("--json", action="store_true")
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> None:
    """CLI entry point."""
    args = parse_args(argv)
    options = ScanOptions(
        patterns=args.pattern,
        limit=args.limit,
        ocr=args.ocr,
        barcodes=args.barcodes,
        gcv=args.gcv,
        lang=args.lang,
        emit_json=args.json,
    )

    targets = collect_paths(args.path, options.patterns)
    if options.limit is not None:
        targets = targets[: options.limit]

    client = _maybe_google_client() if options.gcv else None

    for path in targets:
        payload = scan_image(path, options, client)
        if options.emit_json:
            print(json.dumps(payload, ensure_ascii=True))
        else:
            print(path)
            if options.ocr:
                print("OCR:")
                print(payload["ocr"] or "")
            if options.barcodes:
                print("Barcodes:")
                for value in payload["barcodes"]:
                    print(value)
            if options.gcv:
                print("Labels:")
                for label in payload["gcv"].get("labels", []):
                    print(label)
                print("Logos:")
                for logo in payload["gcv"].get("logos", []):
                    print(logo)
            print()


if __name__ == "__main__":
    main()
