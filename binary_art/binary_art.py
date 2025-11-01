"""
Binary Art Generator for Solarpunk Space Game

Generates procedural textures and tilemaps based on binary patterns.
Uses solarpunk color palette: mint, lavender, cyan, dusty orange.
"""

from PIL import Image, ImageDraw
import random
import os


# Solarpunk color palette
COLORS = {
    'mint': [(100, 200, 150), (150, 220, 200), (80, 180, 130)],
    'lavender': [(180, 160, 255), (200, 180, 255), (160, 140, 230)],
    'cyan': [(100, 200, 220), (150, 230, 245), (80, 180, 200)],
    'orange': [(220, 160, 110), (240, 180, 130), (200, 140, 90)],
    'dark': [(25, 20, 35), (35, 30, 45), (45, 40, 55)],
    'light': [(200, 255, 220), (220, 255, 240), (180, 235, 200)]
}


def binary_to_color(binary_value, palette_name='mint'):
    """Convert binary value to color from palette."""
    palette = COLORS[palette_name]
    index = binary_value % len(palette)
    return palette[index]


def generate_binary_pattern(width, height, seed=None):
    """Generate a binary pattern grid."""
    if seed:
        random.seed(seed)

    pattern = []
    for y in range(height):
        row = []
        for x in range(width):
            # Create interesting patterns with bit operations
            value = (x ^ y) & ((x * y) % 256)
            row.append(value)
        pattern.append(row)

    return pattern


def create_star_field(width=800, height=600, num_stars=200):
    """Create a star field background."""
    img = Image.new('RGB', (width, height), COLORS['dark'][0])
    draw = ImageDraw.Draw(img)

    for _ in range(num_stars):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        size = random.randint(1, 3)
        brightness = random.choice(COLORS['light'])

        if size == 1:
            draw.point((x, y), fill=brightness)
        else:
            draw.ellipse([x - size, y - size, x + size, y + size], fill=brightness)

    return img


def create_nebula_pattern(width=800, height=600):
    """Create a nebula-like background using binary patterns."""
    img = Image.new('RGB', (width, height), COLORS['dark'][0])
    pixels = img.load()

    pattern = generate_binary_pattern(width // 4, height // 4, seed=42)

    for y in range(height):
        for x in range(width):
            # Sample from pattern
            px = x // 4
            py = y // 4
            if px < len(pattern[0]) and py < len(pattern):
                value = pattern[py][px]

                # Use different color palettes based on value
                if value < 64:
                    color = binary_to_color(value, 'dark')
                elif value < 128:
                    color = binary_to_color(value, 'lavender')
                elif value < 192:
                    color = binary_to_color(value, 'cyan')
                else:
                    color = binary_to_color(value, 'mint')

                # Add some randomness for organic feel
                color = tuple(max(0, min(255, c + random.randint(-10, 10))) for c in color)
                pixels[x, y] = color

    return img


def create_tilemap(tile_size=64, grid_width=16, grid_height=12):
    """Create a tilemap with procedural tiles."""
    img = Image.new('RGB',
                    (grid_width * tile_size, grid_height * tile_size),
                    COLORS['dark'][0])

    for gy in range(grid_height):
        for gx in range(grid_width):
            # Generate binary pattern for this tile
            pattern = generate_binary_pattern(8, 8, seed=gx * grid_height + gy)

            # Draw tile
            for ty in range(8):
                for tx in range(8):
                    value = pattern[ty][tx]

                    # Choose color based on value
                    if value < 64:
                        continue  # Skip dark tiles
                    elif value < 128:
                        palette = 'orange'
                    elif value < 192:
                        palette = 'cyan'
                    else:
                        palette = 'mint'

                    color = binary_to_color(value, palette)

                    # Draw pixel block
                    pixel_size = tile_size // 8
                    x = gx * tile_size + tx * pixel_size
                    y = gy * tile_size + ty * pixel_size

                    img_draw = ImageDraw.Draw(img)
                    img_draw.rectangle(
                        [x, y, x + pixel_size - 1, y + pixel_size - 1],
                        fill=color
                    )

    return img


def create_solar_orb_sprite(size=64):
    """Create a solar orb sprite."""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    center = size // 2

    # Outer glow
    for i in range(size // 2, 0, -2):
        alpha = int(100 * (i / (size // 2)))
        color = (255, 220, 100, alpha)
        draw.ellipse([center - i, center - i, center + i, center + i], fill=color)

    # Main orb
    draw.ellipse([center - 12, center - 12, center + 12, center + 12],
                fill=(255, 220, 100, 255))

    # Highlight
    draw.ellipse([center - 8, center - 8, center - 2, center - 2],
                fill=(255, 255, 150, 255))

    return img


def create_ship_sprite(width=40, height=50):
    """Create a solarpunk ship sprite."""
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Ship body (mint green)
    ship_points = [
        (width // 2, 0),
        (0, height),
        (width, height)
    ]
    draw.polygon(ship_points, fill=COLORS['mint'][0])

    # Solar panels (lavender accents)
    draw.polygon([(5, 20), (0, 30), (15, 25)], fill=COLORS['lavender'][0])
    draw.polygon([(width - 5, 20), (width, 30), (width - 15, 25)], fill=COLORS['lavender'][0])

    # Solar core (orange/yellow)
    draw.ellipse([width // 2 - 6, height // 2 - 6,
                  width // 2 + 6, height // 2 + 6],
                fill=COLORS['orange'][1])

    return img


def create_debris_sprite(size=60):
    """Create a debris sprite."""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Irregular rocky shape
    center = size // 2
    points = []
    num_points = random.randint(7, 10)

    for i in range(num_points):
        angle = (i / num_points) * 2 * 3.14159
        radius = random.randint(size // 4, size // 2)
        x = center + int(radius * random.uniform(0.8, 1.2) * (angle % 1))
        y = center + int(radius * random.uniform(0.8, 1.2) * ((angle + 1) % 1))
        points.append((x, y))

    draw.polygon(points, fill=COLORS['orange'][2])

    # Add some darker patches
    for _ in range(random.randint(2, 4)):
        x = random.randint(size // 4, 3 * size // 4)
        y = random.randint(size // 4, 3 * size // 4)
        r = random.randint(3, 8)
        draw.ellipse([x - r, y - r, x + r, y + r], fill=COLORS['dark'][1])

    return img


def main():
    """Generate all art assets."""
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)

    print("Generating solarpunk space art assets...")

    # Star field
    print("  - Star field background...")
    star_field = create_star_field()
    star_field.save(os.path.join(output_dir, 'star_field.png'))

    # Nebula
    print("  - Nebula background...")
    nebula = create_nebula_pattern()
    nebula.save(os.path.join(output_dir, 'nebula.png'))

    # Tilemap
    print("  - Procedural tilemap...")
    tilemap = create_tilemap()
    tilemap.save(os.path.join(output_dir, 'tilemap.png'))

    # Sprites
    print("  - Solar orb sprite...")
    orb = create_solar_orb_sprite()
    orb.save(os.path.join(output_dir, 'solar_orb.png'))

    print("  - Ship sprite...")
    ship = create_ship_sprite()
    ship.save(os.path.join(output_dir, 'ship.png'))

    print("  - Debris sprites...")
    for i in range(3):
        debris = create_debris_sprite()
        debris.save(os.path.join(output_dir, f'debris_{i + 1}.png'))

    print(f"\n✓ Generated all assets in '{output_dir}/' directory!")
    print(f"  Files: star_field.png, nebula.png, tilemap.png, solar_orb.png, ship.png, debris_*.png")


if __name__ == "__main__":
    main()
