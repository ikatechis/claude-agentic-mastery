#!/usr/bin/env python3
"""Unified sprite preprocessing pipeline.

Standardizes sprite sizes based on category and removes backgrounds using withoutbg.
Supports batch processing with auto-detection or manual category specification.

Categories and default sizes:
- player: 64x64 (main characters)
- enemy: 64x64 (zombies, bosses)
- powerup: 64x64 (collectibles)
- projectile: 32x32 (bullets, small effects)
- tile: 128x128 (background tiles)
- ui: 48x48 (icons, buttons)
- effect: 64x64 (explosions, particles)

Usage:
    # Single file with auto-detection
    python scripts/sprite_preprocess.py input.png output.png

    # Single file with category
    python scripts/sprite_preprocess.py input.png output.png --category enemy

    # Batch with auto-detection
    python scripts/sprite_preprocess.py --batch input_dir/ output_dir/

    # Batch with specific category
    python scripts/sprite_preprocess.py --batch input_dir/ output_dir/ --category powerup

    # Custom size override
    python scripts/sprite_preprocess.py input.png output.png --size 96

    # Dry run to preview
    python scripts/sprite_preprocess.py --batch input_dir/ output_dir/ --dry-run

    # Skip background removal (resize only)
    python scripts/sprite_preprocess.py input.png output.png --no-bg-removal
"""

import argparse
import sys
from pathlib import Path
from typing import Literal

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


# Category size mappings
CATEGORY_SIZES = {
    "player": 64,
    "enemy": 64,
    "powerup": 64,
    "projectile": 32,
    "tile": 128,
    "ui": 48,
    "effect": 64,
}

CategoryType = Literal["player", "enemy", "powerup", "projectile", "tile", "ui", "effect"]


def detect_category(filename: str) -> CategoryType | None:
    """Auto-detect sprite category from filename.

    Args:
        filename: Name of the file to analyze

    Returns:
        Detected category or None if unknown
    """
    filename_lower = filename.lower()

    # Check for keyword patterns
    if "player" in filename_lower:
        return "player"
    elif any(word in filename_lower for word in ["zombie", "enemy", "boss"]):
        return "enemy"
    elif "powerup" in filename_lower or "pickup" in filename_lower:
        return "powerup"
    elif any(word in filename_lower for word in ["bullet", "projectile", "shot"]):
        return "projectile"
    elif "tile" in filename_lower or "background" in filename_lower:
        return "tile"
    elif any(word in filename_lower for word in ["ui", "icon", "button"]):
        return "ui"
    elif any(word in filename_lower for word in ["effect", "explosion", "particle"]):
        return "effect"

    return None


def resize_and_center(image: Image.Image, target_size: int) -> Image.Image:
    """Resize image maintaining aspect ratio and center with transparent padding.

    Args:
        image: Input image
        target_size: Target size (width=height)

    Returns:
        Resized and centered image
    """
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


def preprocess_sprite(
    input_path: str,
    output_path: str,
    category: CategoryType | None = None,
    custom_size: int | None = None,
    remove_bg: bool = True,
    model: WithoutBG | None = None,
) -> dict:
    """Preprocess a single sprite.

    Args:
        input_path: Path to input image
        output_path: Path to save processed image
        category: Sprite category (auto-detected if None)
        custom_size: Override category size
        remove_bg: Whether to remove background
        model: WithoutBG model instance (optional, will create if needed)

    Returns:
        Dict with processing info
    """
    input_file = Path(input_path)

    # Auto-detect category if not provided
    if category is None:
        category = detect_category(input_file.name)

    # Determine target size
    if custom_size:
        target_size = custom_size
    elif category:
        target_size = CATEGORY_SIZES[category]
    else:
        # Default fallback
        target_size = 64

    # Load or process image
    if remove_bg:
        # Remove background first
        if model is None:
            model = WithoutBG.opensource()
        result = model.remove_background(input_path)
    else:
        # Just load the image
        result = Image.open(input_path)
        if result.mode != "RGBA":
            result = result.convert("RGBA")

    # Resize and center
    result = resize_and_center(result, target_size)

    # Save result
    result.save(output_path)

    return {
        "input": input_path,
        "output": output_path,
        "category": category or "unknown",
        "size": target_size,
        "bg_removed": remove_bg,
    }


def preprocess_batch(
    input_dir: str,
    output_dir: str,
    category: CategoryType | None = None,
    custom_size: int | None = None,
    remove_bg: bool = True,
    dry_run: bool = False,
) -> None:
    """Preprocess a batch of sprites.

    Args:
        input_dir: Directory containing input images
        output_dir: Directory to save processed images
        category: Force all sprites to this category (auto-detect if None)
        custom_size: Override category size for all sprites
        remove_bg: Whether to remove backgrounds
        dry_run: Preview without processing
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)

    # Find all image files
    image_extensions = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}
    image_files = [
        f for f in input_path.iterdir() if f.is_file() and f.suffix.lower() in image_extensions
    ]

    if not image_files:
        print(f"No images found in {input_dir}")
        return

    print(f"Found {len(image_files)} images to process")
    print("=" * 70)

    # Dry run: preview what would happen
    if dry_run:
        print("DRY RUN - No files will be modified\n")
        for img_file in image_files:
            detected_cat = category or detect_category(img_file.name)
            size = custom_size or (CATEGORY_SIZES.get(detected_cat, 64) if detected_cat else 64)
            output_file = output_path / f"{img_file.stem}_processed.png"
            print(f"📄 {img_file.name}")
            print(f"   Category: {detected_cat or 'unknown'}")
            print(f"   Size: {size}x{size}")
            print(f"   BG Removal: {'Yes' if remove_bg else 'No'}")
            print(f"   Output: {output_file.name}\n")
        return

    # Create output directory
    output_path.mkdir(parents=True, exist_ok=True)

    # Initialize model once if removing backgrounds
    model = None
    if remove_bg:
        print("Loading withoutbg model...")
        model = WithoutBG.opensource()
        print("Model loaded!\n")

    # Process each image
    processed = []
    failed = []

    for i, img_file in enumerate(image_files, 1):
        output_file = output_path / f"{img_file.stem}_processed.png"

        try:
            print(f"[{i}/{len(image_files)}] Processing {img_file.name}...")

            info = preprocess_sprite(
                str(img_file),
                str(output_file),
                category=category,
                custom_size=custom_size,
                remove_bg=remove_bg,
                model=model,
            )

            print(f"   ✓ Category: {info['category']} | Size: {info['size']}x{info['size']}")
            processed.append(info)

        except Exception as e:
            print(f"   ✗ Error: {e}")
            failed.append({"file": img_file.name, "error": str(e)})

    # Summary
    print("=" * 70)
    print(f"\n✓ Successfully processed: {len(processed)}")
    if failed:
        print(f"✗ Failed: {len(failed)}")
        for f in failed:
            print(f"   - {f['file']}: {f['error']}")

    print(f"\nOutput directory: {output_dir}")


def main():
    parser = argparse.ArgumentParser(
        description="Unified sprite preprocessing pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single file with auto-detection
  %(prog)s input.png output.png

  # Batch process with auto-detection
  %(prog)s --batch sprites/ processed/

  # Batch with specific category
  %(prog)s --batch sprites/ processed/ --category powerup

  # Custom size override
  %(prog)s input.png output.png --size 128

  # Preview without processing
  %(prog)s --batch sprites/ processed/ --dry-run

Categories: player, enemy, powerup, projectile, tile, ui, effect
        """,
    )

    parser.add_argument("input", help="Input image or directory (with --batch)")
    parser.add_argument("output", help="Output image or directory (with --batch)")

    parser.add_argument("--batch", action="store_true", help="Process directory of images")

    parser.add_argument(
        "--category",
        choices=list(CATEGORY_SIZES.keys()),
        help="Sprite category (auto-detected if not specified)",
    )

    parser.add_argument("--size", type=int, help="Custom size override (width=height in pixels)")

    parser.add_argument(
        "--no-bg-removal",
        action="store_true",
        help="Skip background removal (resize only)",
    )

    parser.add_argument("--dry-run", action="store_true", help="Preview changes without processing")

    args = parser.parse_args()

    # Validate inputs
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input '{args.input}' not found")
        sys.exit(1)

    if args.batch and not input_path.is_dir():
        print("Error: --batch mode requires input to be a directory")
        sys.exit(1)

    # Process
    if args.batch:
        preprocess_batch(
            args.input,
            args.output,
            category=args.category,
            custom_size=args.size,
            remove_bg=not args.no_bg_removal,
            dry_run=args.dry_run,
        )
    else:
        # Create output directory if needed
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Process single file
        info = preprocess_sprite(
            args.input,
            args.output,
            category=args.category,
            custom_size=args.size,
            remove_bg=not args.no_bg_removal,
        )

        print(f"✓ Processed: {info['input']}")
        print(f"  Category: {info['category']}")
        print(f"  Size: {info['size']}x{info['size']}")
        print(f"  BG Removed: {info['bg_removed']}")
        print(f"  Saved to: {info['output']}")


if __name__ == "__main__":
    main()
