# Sprite Processing Scripts

Utility scripts for processing game assets with intelligent categorization and background removal.

## Unified Preprocessing Pipeline (Recommended)

**`sprite_preprocess.py`** - One-stop solution for sprite preparation with automatic category detection and sizing.

### Features

- **Auto-detection:** Categorizes sprites by filename (player, enemy, powerup, tile, etc.)
- **Category-based sizing:** Applies appropriate dimensions per sprite type
- **Background removal:** Uses withoutbg (Focus v1.0.0 multi-stage AI)
- **Batch processing:** Process entire directories with progress tracking
- **Dry-run mode:** Preview changes before processing
- **Flexible:** Override categories and sizes, skip BG removal if needed

### Quick Start

```bash
# Single file (auto-detects category from filename)
uv run python scripts/sprite_preprocess.py input.png output.png

# Batch process entire directory
uv run python scripts/sprite_preprocess.py --batch sprites/ processed/

# Preview without processing
uv run python scripts/sprite_preprocess.py --batch sprites/ processed/ --dry-run
```

### Category Detection & Sizes

The script auto-detects sprite types and applies appropriate sizes:

| Category | Size | Auto-detected from |
|----------|------|-------------------|
| **player** | 64x64 | `player_*.png` |
| **enemy** | 64x64 | `zombie_*.png`, `enemy_*.png`, `boss_*.png` |
| **powerup** | 64x64 | `powerup_*.png`, `pickup_*.png` |
| **projectile** | 32x32 | `bullet_*.png`, `projectile_*.png` |
| **tile** | 128x128 | `tile_*.png`, `background_*.png` |
| **ui** | 48x48 | `ui_*.png`, `icon_*.png`, `button_*.png` |
| **effect** | 64x64 | `effect_*.png`, `explosion_*.png` |

### Advanced Usage

```bash
# Force specific category
uv run python scripts/sprite_preprocess.py input.png output.png --category enemy

# Custom size override
uv run python scripts/sprite_preprocess.py input.png output.png --size 96

# Batch with specific category (all sprites same type)
uv run python scripts/sprite_preprocess.py --batch sprites/ processed/ --category powerup

# Resize only, skip background removal
uv run python scripts/sprite_preprocess.py input.png output.png --no-bg-removal

# Combine options
uv run python scripts/sprite_preprocess.py --batch sprites/ processed/ --category tile --size 256
```

### Examples

```bash
# Process powerup icons (auto-detected as 64x64)
uv run python scripts/sprite_preprocess.py --batch powerups/ processed_powerups/

# Process background tiles (auto-detected as 128x128)
uv run python scripts/sprite_preprocess.py --batch tiles/ processed_tiles/

# Custom projectile sprites at 48x48 instead of default 32x32
uv run python scripts/sprite_preprocess.py --batch bullets/ processed/ --category projectile --size 48

# Preview what would happen (dry-run)
uv run python scripts/sprite_preprocess.py --batch sprites/ output/ --dry-run
```

---

## Alternative Methods (Educational / Baseline Comparison)

### Local Background Removal Only

**`remove_background_local.py`** - Direct withoutbg usage without preprocessing.

```bash
# Single file
uv run python scripts/remove_background_local.py input.png output.png --size 64

# Batch processing
uv run python scripts/remove_background_local.py --batch input_dir/ output_dir/
```

**Uses:** Focus v1.0.0 model with multi-stage pipeline (Depth Anything V2 + ISNet + Focus matting)
**First run:** Downloads ~320MB of models
**Speed:** ~2-5 seconds per image after model loads

### Manual Background Removal

**`remove_background.py`** - Simple color-based removal using PIL.

```bash
# Basic usage
uv run python scripts/remove_background.py input.png output.png

# With threshold adjustment
uv run python scripts/remove_background.py input.png output.png --threshold 50 --size 64
```

**Good for:** Simple backgrounds (white, solid colors)
**Limitations:** May not work well with complex backgrounds

---

## Recommended Workflow

**For new sprites:**

1. **Use sprite_preprocess.py** with dry-run first to preview:
   ```bash
   uv run python scripts/sprite_preprocess.py --batch new_sprites/ processed/ --dry-run
   ```

2. **Review the preview**, adjust categories/sizes if needed

3. **Process the batch:**
   ```bash
   uv run python scripts/sprite_preprocess.py --batch new_sprites/ processed/
   ```

4. **Copy processed sprites** to `assets/sprites/`

**For single sprites:**

```bash
# Quick processing with auto-detection
uv run python scripts/sprite_preprocess.py zombie_boss.png assets/sprites/zombie_boss.png
```

---

## Technical Details

### Background Removal Model (withoutbg)

Multi-stage AI pipeline:
1. **Depth Anything V2** - Monocular depth estimation
2. **ISNet** - Instance segmentation
3. **Focus matting** - Alpha matting for precise edges
4. **Focus refiner** - Final edge refinement

**Quality:** Superior to cloud APIs (remove.bg) for game sprites
**Cost:** Free, unlimited, offline after initial download
**Consistency:** Same model, reproducible results

### Image Processing

- **Aspect ratio:** Preserved with transparent padding
- **Centering:** Images centered in canvas
- **Resampling:** LANCZOS algorithm for high quality
- **Format:** Output as RGBA PNG with transparency

---

## Tips

1. **Use consistent naming** for auto-detection to work:
   - `powerup_health.png` → powerup (64x64)
   - `zombie_fast.png` → enemy (64x64)
   - `tile_grass.png` → tile (128x128)

2. **Dry-run first** when batch processing to preview results

3. **Override when needed:**
   - Category auto-detection wrong? Use `--category`
   - Size not right? Use `--size`

4. **Skip BG removal** if sprites already have transparency:
   ```bash
   uv run python scripts/sprite_preprocess.py input.png output.png --no-bg-removal
   ```

5. **Model loads once** for batch processing (10-100x faster than single files)
