#!/usr/bin/env python3
"""Remove backgrounds using withoutbg (local, open-source model).

Uses Focus v1.0.0 model - no API key needed, runs completely offline.
First run downloads ~320MB of models.

Usage:
    # Single file
    python scripts/remove_background_local.py input.png output.png [--size 64]

    # Batch processing
    python scripts/remove_background_local.py --batch input_dir/ output_dir/ [--size 64]
"""

import argparse
import sys
from pathlib import Path

try:
    from withoutbg import WithoutBG
except ImportError:
    print("Error: withoutbg is required. Install with: uv add withoutbg")
    sys.exit(1)

try:
    from PIL import Image
except ImportError:
    print("Error: PIL/Pillow is required. Install with: uv add pillow")
    sys.exit(1)


def resize_image(image: Image.Image, target_size: int) -> Image.Image:
    """Resize image to target_size x target_size maintaining aspect ratio with padding."""
    # Calculate scaling to fit within target_size while maintaining aspect ratio
    width, height = image.size
    scale = min(target_size / width, target_size / height)
    new_width = int(width * scale)
    new_height = int(height * scale)

    # Resize image
    resized = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # Create new image with transparent background
    final = Image.new("RGBA", (target_size, target_size), (0, 0, 0, 0))

    # Center the resized image
    x = (target_size - new_width) // 2
    y = (target_size - new_height) // 2
    final.paste(resized, (x, y), resized if resized.mode == "RGBA" else None)

    return final


def remove_background_single(
    input_path: str, output_path: str, model: WithoutBG, target_size: int | None = None
) -> None:
    """Remove background from a single image.

    Args:
        input_path: Path to input image
        output_path: Path to save processed image
        model: WithoutBG model instance (reused for efficiency)
        target_size: Optional size to resize to (width=height)
    """
    print(f"Processing {input_path}...")

    # Remove background
    result = model.remove_background(input_path)

    # Resize if requested
    if target_size:
        result = resize_image(result, target_size)
        print(f"  Resized to {target_size}x{target_size}")

    # Save result
    result.save(output_path)
    print(f"  Saved to {output_path}")


def remove_background_batch(
    input_dir: str, output_dir: str, model: WithoutBG, target_size: int | None = None
) -> None:
    """Remove background from all images in a directory.

    Args:
        input_dir: Directory containing input images
        output_dir: Directory to save processed images
        model: WithoutBG model instance (reused for efficiency)
        target_size: Optional size to resize to (width=height)
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)

    # Create output directory
    output_path.mkdir(parents=True, exist_ok=True)

    # Find all image files
    image_extensions = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}
    image_files = [
        f for f in input_path.iterdir() if f.is_file() and f.suffix.lower() in image_extensions
    ]

    if not image_files:
        print(f"No images found in {input_dir}")
        return

    print(f"Found {len(image_files)} images to process")
    print("-" * 50)

    # Process each image
    for img_file in image_files:
        output_file = output_path / f"{img_file.stem}_nobg.png"
        try:
            remove_background_single(str(img_file), str(output_file), model, target_size)
        except Exception as e:
            print(f"  Error processing {img_file}: {e}")

    print("-" * 50)
    print(f"Batch processing complete! Output in {output_dir}")


def main():
    parser = argparse.ArgumentParser(
        description="Remove backgrounds using withoutbg (local, open-source)"
    )
    parser.add_argument("input", help="Input image path or directory (with --batch)")
    parser.add_argument("output", help="Output image path or directory (with --batch)")
    parser.add_argument(
        "--batch", action="store_true", help="Process all images in input directory"
    )
    parser.add_argument("--size", type=int, help="Resize to this size (width=height)")

    args = parser.parse_args()

    # Validate input exists
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input '{args.input}' not found")
        sys.exit(1)

    # Validate batch mode
    if args.batch and not input_path.is_dir():
        print("Error: --batch mode requires input to be a directory")
        sys.exit(1)

    # Initialize model once (reusing is 10-100x faster)
    print("Loading withoutbg Focus v1.0.0 model...")
    print("(First run will download ~320MB of models)")
    model = WithoutBG.opensource()
    print("Model loaded successfully!\n")

    # Process image(s)
    if args.batch:
        remove_background_batch(args.input, args.output, model, args.size)
    else:
        # Create output directory if needed
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        remove_background_single(args.input, args.output, model, args.size)


if __name__ == "__main__":
    main()
