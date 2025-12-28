#!/usr/bin/env python3
"""Remove white/light backgrounds from images and make them transparent.

Usage:
    python scripts/remove_background.py input.png output.png [--size 64] [--threshold 30]
"""

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Error: PIL/Pillow is required. Install with: uv add pillow")
    sys.exit(1)


def remove_background(
    input_path: str,
    output_path: str,
    target_size: int | None = None,
    threshold: int = 30,
) -> None:
    """Remove white/light background from image and make transparent.

    Args:
        input_path: Path to input image
        output_path: Path to save processed image
        target_size: Optional size to resize to (width=height)
        threshold: Color similarity threshold (0-255, lower = more strict)
    """
    # Load the image
    img = Image.open(input_path)
    print(f"Loaded {input_path}: {img.size[0]}x{img.size[1]}")

    # Convert to RGBA if not already
    img = img.convert("RGBA")

    # Get pixel data
    pixels = img.load()

    # Detect background color by sampling corners
    corner_colors = [
        pixels[0, 0],
        pixels[img.size[0] - 1, 0],
        pixels[0, img.size[1] - 1],
        pixels[img.size[0] - 1, img.size[1] - 1],
    ]

    # Average the corner colors to get background color
    bg_r = sum(c[0] for c in corner_colors) // 4
    bg_g = sum(c[1] for c in corner_colors) // 4
    bg_b = sum(c[2] for c in corner_colors) // 4

    print(f"Detected background color: RGB({bg_r}, {bg_g}, {bg_b})")

    # Remove background with color similarity threshold
    transparent_count = 0
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            r, g, b, a = pixels[x, y]

            # Calculate Euclidean color distance from background
            color_distance = ((r - bg_r) ** 2 + (g - bg_g) ** 2 + (b - bg_b) ** 2) ** 0.5

            # If pixel is similar to background, make transparent
            if color_distance < threshold:
                pixels[x, y] = (r, g, b, 0)
                transparent_count += 1

    total_pixels = img.size[0] * img.size[1]
    print(
        f"Made {transparent_count}/{total_pixels} pixels transparent "
        f"({100 * transparent_count / total_pixels:.1f}%)"
    )

    # Resize if requested
    if target_size:
        img = img.resize((target_size, target_size), Image.Resampling.LANCZOS)
        print(f"Resized to {target_size}x{target_size}")

    # Save the processed image
    img.save(output_path)
    print(f"Saved to {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Remove white/light backgrounds from images")
    parser.add_argument("input", help="Input image path")
    parser.add_argument("output", help="Output image path")
    parser.add_argument("--size", type=int, help="Resize to this size (width=height)")
    parser.add_argument(
        "--threshold",
        type=int,
        default=30,
        help="Color similarity threshold (default: 30)",
    )

    args = parser.parse_args()

    # Validate input file exists
    if not Path(args.input).exists():
        print(f"Error: Input file '{args.input}' not found")
        sys.exit(1)

    # Create output directory if needed
    output_dir = Path(args.output).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    # Process the image
    remove_background(args.input, args.output, args.size, args.threshold)


if __name__ == "__main__":
    main()
