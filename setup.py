from setuptools import setup, find_packages

setup(
    name="image-ocr-barcode",
    version="0.1.0",
    description="CLI for OCR, barcode, and optional vision label scans",
    author="Lars de Ridder",
    author_email="lars@xithing.io",
    license="MIT",
    python_requires=">=3.6",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "pillow>=5.0",
        "pytesseract>=0.2",
        "pyzbar>=0.1",
    ],
    extras_require={
        "vision": ["google-cloud-vision>=0.33"],
        "dev": ["pytest>=3.0"],
    },
    entry_points={
        "console_scripts": [
            "image-ocr-barcode=image_ocr_barcode.cli:main",
        ],
    },
)
