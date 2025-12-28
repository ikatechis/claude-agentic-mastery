---
name: game-artist
description: Manage game assets with Kenney-first approach. Search 36,000+ Kenney CC0 assets before generating. Use Pollinations for AI sprite generation when needed. Ensure style consistency with flat/vector Kenney aesthetic. Auto-triggers on asset requests.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, mcp__pollinations__generateImage, mcp__pollinations__generateImageUrl
---

# Game Artist Skill

Intelligent game asset management with **Kenney-first** workflow.

## When This Skill Activates

This skill automatically triggers when you:
- Request a game asset ("find a health icon", "need a tree sprite")
- Ask about visual elements ("what would work for power-ups?")
- Want to add new sprites/graphics
- Need asset recommendations

## Core Principle: Kenney First

**Don't generate what already exists!**

The project has access to Kenney's All-in-1 collection (~36,000 assets, all CC0):
- 150+ 2D asset packs
- Characters, tiles, props, UI, effects
- All in consistent flat/vector style
- Free for any use

**Workflow:**
1. 🔍 **Search** Kenney collection first
2. ✅ **Use** existing asset if good match
3. 🎨 **Generate** with Pollinations only if needed
4. ✔️ **Verify** style matches flat/vector aesthetic

## Step-by-Step Workflow

### Step 1: Understand the Request

**Questions to answer:**
- What type of asset? (character, item, prop, UI, effect)
- What size? (based on game world scale - see STYLE_GUIDE.md)
- What purpose? (collectible, decoration, functional)
- What colors? (check STYLE_GUIDE.md palette)
- Style requirements? (must match flat/vector style)

**Example:**
```
Request: "Need a health power-up sprite"
→ Type: Item/collectible
→ Size: 48x48 or 64x64 (smaller than character)
→ Purpose: Collectible power-up
→ Colors: Red/green (health colors)
→ Style: Flat/vector, must match player sprite
```

### Step 2: Search Kenney Collection

**Use KENNEY_CATALOG.md to find relevant packs:**

1. **Check catalog** - Review pack index for likely candidates
2. **Browse spritesheets** - Use `spritesheet*.png` files for visual overview
3. **Browse Preview.png** - Alternative visual inspection
4. **Navigate to assets** - Find individual sprites in PNG/ folders

**Visual Browsing Strategy:**

**Method 1: Spritesheets (Recommended)**
```bash
# Find all spritesheets in a pack
find "/path/to/Kenney/2D assets/[Pack Name]" -name "spritesheet*.png"

# Example for Puzzle Assets:
find "/path/to/Kenney/2D assets/Puzzle Assets" -name "spritesheet*.png"
```

Then use **Read tool with visual inspection** to see all sprites in one image:
```python
Read("/path/to/spritesheet_items.png")
# Claude Vision can see all sprites at once!
```

**Method 2: Preview.png**
```bash
# Single preview image showing asset samples
ls "/path/to/Kenney/2D assets/[Pack Name]/Preview.png"
```

**Method 3: Individual PNGs** (when needed)
```bash
# Browse individual sprites
ls "/path/to/Kenney/2D assets/[Pack Name]/PNG/"
```

**Search locations by asset type:**

| Asset Type | Primary Packs | Browse Method |
|------------|---------------|---------------|
| Characters | Topdown Shooter | Spritesheet in `Spritesheet/` folder |
| Items/Collectibles | Generic Items, Puzzle Assets | Spritesheet or Preview.png |
| Power-ups | Space Shooter Redux, Puzzle Assets | Check spritesheet_items.png |
| UI Elements | Game Icons, UI Pack | Preview.png (no spritesheets) |
| Props/Environment | Topdown Shooter, Generic Items | Spritesheet in pack |
| Effects | Explosion Pack, Particle Pack | Spritesheet for each effect type |

**Spritesheet File Patterns:**
```
spritesheet_complete.png    - All assets in pack
spritesheet_items.png        - Just items
spritesheet_characters.png   - Just characters
spritesheet_tiles.png        - Just tiles
spritesheet_enemies.png      - Just enemies
```

**Quick search workflow:**
```bash
# 1. Find relevant pack
ls "/path/to/Kenney/2D assets/" | grep -i "puzzle"

# 2. Check for spritesheets
find "/path/to/Kenney/2D assets/Puzzle Assets" -name "spritesheet*.png"

# 3. Visual inspect with Read tool
Read("/path/to/Kenney/2D assets/Puzzle Assets/Spritesheet/spritesheet_items.png")

# 4. If found what you need, navigate to individual PNG
ls "/path/to/Kenney/2D assets/Puzzle Assets/PNG/"
```

### Step 3: Evaluate Candidates

**For each candidate asset:**

✅ **Style Match:**
- Flat/vector (NOT pixel art)?
- Smooth rounded shapes?
- Thin dark outline?
- Simple geometric forms?

✅ **Color Match:**
- Uses game palette?
- Can be easily recolored if needed?
- Fits visual theme?

✅ **Size Match:**
- Appropriate game world scale?
- Can be resized to tile multiples (64, 96, 128, 192, 256)?
- Maintains quality at target size?

✅ **Purpose Match:**
- Communicates intended meaning?
- Clear silhouette/icon?
- Works in gameplay context?

**Decision tree:**
```
Found perfect match → Use it (Step 4)
Found close match  → Use and modify colors if needed (Step 4)
No good match      → Generate new asset (Step 5)
```

### Step 4: Use Kenney Asset

If suitable asset found:

1. **Identify exact sprite** from spritesheet visual inspection

2. **Navigate to individual PNG:**
   ```bash
   ls "/path/to/Kenney/[Pack]/PNG/[Category]/"
   # Find the specific sprite file
   ```

3. **Copy asset** from Kenney folder to project:
   ```bash
   cp "Kenney/path/to/sprite.png" "assets/sprites/sprite_name.png"
   ```

4. **Resize if needed** (maintain aspect ratio):
   ```bash
   # Use ImageMagick or similar
   magick sprite.png -resize 64x64 output.png
   ```

5. **Verify transparency** - Check alpha channel present

6. **Test in-game** - Place alongside existing sprites

7. **Document source** - Note which Kenney pack it came from

**Output to user:**
```
✅ Found Kenney asset: [Asset Name]
📁 Source: [Pack Name]
📏 Size: [Original] → [Scaled to]
🎨 Colors: [Matches palette]
💾 Saved to: assets/sprites/[filename]
```

### Step 5: Generate with AI

Only if no suitable Kenney asset exists:

1. **Check STYLE_GUIDE.md** - Review flat/vector characteristics

2. **Use Pollinations for AI generation:**

   ```python
   # Enhance prompt for game sprites
   enhanced_prompt = f"""
   [subject], top-down view, Kenney flat vector style,
   smooth rounded shapes, bright [color] (#HEX),
   transparent background, thin dark outline,
   simple geometric forms, clean silhouette,
   casual game aesthetic, high detailed, complete object,
   not cut off, white solid background, game sprite, 2D asset
   """

   mcp__pollinations__generateImage(prompt=enhanced_prompt)
   ```

3. **CRITICAL: Visually inspect with Read tool** - Use Claude Vision to verify the generated image matches the prompt requirements

4. **Post-processing:**
   - Save image to `assets/sprites/ai_generated/[filename]`
   - Remove background if needed:
     ```bash
     convert sprite.png -fuzz 20% -transparent "#COLOR" output.png
     ```
     Common background colors: white (#FFFFFF), light gray (#F5F5F5), cyan (#B3E5FC)

5. **Quality check** (see Step 6)

**Output to user:**
```
🎨 Generated new asset (no Kenney match found)
🤖 Service: Pollinations
📝 Prompt: [prompt used]
💾 Saved to: [file path]
⚠️ Note: Verify style matches in-game
```

### Step 6: Quality Verification

**⚠️ CRITICAL REQUIREMENT: Always use Read tool with Claude Vision to visually inspect sprites!**

Never assume a sprite matches requirements without visual confirmation. AI generators can produce unexpected results.

**Visual verification checklist:**

1. **VERIFY ACTUAL CONTENT** - Does the image show what it's supposed to? (e.g., lightning bolt vs pentagon star)
2. **Compare to references** - Side-by-side with player/zombie sprite
3. **Check style** - Flat/vector vs pixel art
4. **Verify transparency** - Alpha channel present? (look for gray checkerboard pattern)
5. **Inspect edges** - Smooth anti-aliased edges?
6. **Check colors** - Within palette?
7. **Test readability** - Clear at target size?

**Style consistency checklist:**
- [ ] Smooth rounded shapes (not pixelated)
- [ ] Thin dark outline
- [ ] Flat colors with subtle gradients
- [ ] Simple geometric forms
- [ ] Transparent background
- [ ] Matches player/zombie style
- [ ] Appropriate scale
- [ ] Clear silhouette

**If quality issues found:**
```
For Kenney assets:
→ Try different asset from same pack
→ Try similar pack with better style match

For generated assets:
→ Refine prompt with more style keywords
→ Regenerate with adjusted parameters
→ Compare multiple generations
```

## Advanced Features

### Batch Asset Requests

For multiple related assets:

1. **Group by type** - Characters, items, props, etc.
2. **Check spritesheet** - Visual overview of entire pack
3. **Extract all at once** - Batch copy from same pack
4. **Maintain consistency** - Same pack = same style

**When to use subagent instead:**
- Need 10+ assets from exploration
- Creating complete themed collection
- Batch generation with variations
- Complex multi-step asset pipeline

### Color Variations

If Kenney asset has wrong color:

1. **Load original** with image manipulation
2. **Hue shift** to target color
3. **Verify contrast** - Maintain readability
4. **Save variant** with descriptive name

```bash
# Example: shift green gem to blue
magick green_gem.png -modulate 100,100,180 blue_gem.png
```

### Style Transfer (Future)

When Layer.ai API becomes available:
- Upload Kenney reference
- Generate matching style assets
- Batch process for consistency

## Templates and Resources

Quick references:

- **KENNEY_CATALOG.md** - Asset pack index and search tips
- **STYLE_GUIDE.md** - Visual style specifications
- **EXAMPLES.md** - Real workflow walkthroughs
- **templates/pollinations_prompts.md** - Generation templates
- **templates/midjourney_prompts.md** - Moodboard prompts
- **templates/quality_checklist.md** - Verification criteria

## Common Scenarios

### Scenario 1: Power-Up Sprites

**Request:** "Need health, speed, shield power-up sprites"

**Workflow:**
1. Check KENNEY_CATALOG.md → "Puzzle Assets has colored gems!"
2. Find spritesheet: `find "Puzzle Assets" -name "spritesheet*.png"`
3. Visual inspect spritesheet with Read tool → See all gems at once
4. Navigate to PNG folder, copy: green gem, blue gem, gold gem
5. Resize all to 64x64
6. Test in-game alongside player sprite
7. ✅ Done - all from Kenney, no generation needed

### Scenario 2: Custom Enemy Character

**Request:** "Need a flying zombie enemy sprite"

**Workflow:**
1. Check Topdown Shooter spritesheet → Has zombies, but no flying variant
2. Check Space Shooter Redux spritesheet → Has flying enemies, but wrong theme
3. **Decision:** Generate custom asset
4. Enhanced prompt: "flying zombie, top-down view, Kenney flat vector style, green zombie with tattered wings, high detailed, complete object, not cut off, white solid background, game sprite, 2D asset"
5. Generate with Pollinations
   - `mcp__pollinations__generateImage(prompt=enhanced_prompt)`
6. Visually inspect with Read tool
7. Verify style matches existing zombie
8. Save to `assets/sprites/ai_generated/flying_zombie.png`

### Scenario 3: Environment Props

**Request:** "Need trees, bushes, rocks for environment"

**Workflow:**
1. Check Kenney catalog → Multiple options
2. Visual inspect `Topdown Shooter/Spritesheet/` spritesheets
3. Check `Foliage Pack/Spritesheet/` spritesheets
4. Extract several options from PNG folders
5. Resize to appropriate scale (trees 64x128, bushes 64x64)
6. Test variety in-game
7. ✅ Multiple Kenney assets, instant variety

## Error Handling

### Common Issues

**No suitable Kenney asset found:**
→ Search related packs (check KENNEY_CATALOG.md)
→ Try similar assets that can be modified
→ Generate custom asset with Pollinations

**Generated asset doesn't match style:**
→ Refine prompt with more "Kenney" keywords
→ Add negative prompts ("NOT pixel art")
→ Compare with Kenney reference in prompt
→ Regenerate with adjusted parameters
→ Try different Pollinations model

**Pollinations quality issues:**
→ Enhance prompt: ensure "high detailed, complete object, not cut off, white solid background, game sprite, 2D asset" is included
→ Try different Pollinations model
→ Regenerate multiple times and pick best result

**Kenney asset wrong size:**
→ Resize maintaining aspect ratio
→ Use multiples of 16px (64, 96, 128, 192, 256)
→ Verify quality after resize

**Colors don't match palette:**
→ Hue shift existing asset
→ Find alternative in same pack
→ Generate with specific color hex codes

## Tips for Success

✅ **Always check Kenney first** - 90% of needs covered
✅ **Use spritesheet files** - See entire pack at once with visual inspection
✅ **Use Preview.png files** - Alternative quick browse method
✅ **Use Pollinations for AI generation** - Free and unlimited
✅ **Maintain style consistency** - Flat/vector throughout
✅ **Verify in-game** - Test alongside existing sprites
✅ **Document sources** - Track which pack/service assets came from
✅ **Keep aspect ratios** - Don't stretch/squash
✅ **Use tile-based sizing** - Multiples of 64px base unit

❌ **Don't mix styles** - No pixel art with vector art
❌ **Don't over-generate** - Check Kenney exhaustively first
❌ **Don't ignore scale** - Size relative to characters matters
❌ **Don't forget transparency** - All sprites need alpha channel
❌ **Don't use raw prompts** - Always enhance prompts with style keywords

## Output Format

When completing an asset request:

```markdown
## Asset Request: [Asset Name]

**Source:** [Kenney Pack Name] OR [AI Generated - Pollinations]
**File Path:** assets/sprites/[filename]
**Size:** [dimensions] ([X tiles])
**Style Match:** ✅ Verified / ⚠️ Needs review
**Notes:** [Any special considerations]

[Visual preview if using Read tool]
```

## When to Recommend Subagent Instead

Suggest using a subagent for:
- **Batch exploration:** "Catalog all enemy sprites in Kenney packs"
- **Complex generation:** "Create 8-frame walk animation for new character"
- **Style redesign:** "Redesign all UI in cyberpunk theme"
- **Asset pipeline:** "Generate 20 weapon variations with stats"

**How to suggest:**
```
For this complex task, I recommend using a subagent:
- Run: `Task tool with subagent_type=Explore` for thorough pack search
- OR: Create custom subagent for batch generation workflow
This allows autonomous exploration and decision-making.
```

## Remember

**Kenney first, generate second!**

The goal is to maximize use of professional CC0 assets while maintaining visual consistency. Only generate when Kenney's collection doesn't have what we need.
