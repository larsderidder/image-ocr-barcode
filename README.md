# Image OCR Barcode

Scan images for OCR text, barcode data, and optional cloud vision labels/logos.

## Install (from source)
```sh
python -m venv .venv
. .venv/bin/activate
python -m pip install -U pip
python -m pip install -e .
```

## Usage
```sh
image-ocr-barcode ./images --ocr --barcodes --json
```

## Options
- `--pattern`: glob pattern for images (repeatable).
- `--limit`: max images to process.
- `--ocr`: enable OCR (default: on).
- `--barcodes`: enable barcode scanning (default: on).
- `--gcv`: enable Google Cloud Vision labels/logos/text (requires extras).
- `--lang`: OCR language code (default: `eng`).
- `--json`: emit JSON per image.

## Development
```sh
python -m venv .venv
. .venv/bin/activate
python -m pip install -U pip
python -m pip install -e ".[dev,vision]"
pytest
```

## License
See `LICENSE`.
