#!/usr/bin/env python3
"""
Binary Art Generator - Procedural Texture/Tilemap Generator
Uses mathematical transformations and binary operations (NO NEURAL NETWORKS)

Mathematical Foundation:
- Binary field operations: GF(2) arithmetic
- Cellular automata: Conway's Game of Life variants
- Hash functions: Generate pseudo-random patterns from seeds
- Fractal generation: Recursive subdivision
- f(i) = -i transformations in discrete space

Generates:
- Tilemaps for game backgrounds
- Procedural textures
- Noise patterns
- Solarpunk-themed assets
"""

from PIL import Image, ImageDraw
import random
import math
import os


class BinaryArtGenerator:
    """Generate procedural art using mathematical operations"""

    def __init__(self, width=256, height=256):
        self.width = width
        self.height = height
        self.output_dir = "binary_art/output"
        os.makedirs(self.output_dir, exist_ok=True)

        # Solarpunk color palettes
        self.palettes = {
            'solarpunk_green': [
                (10, 30, 20),      # Deep forest
                (40, 80, 50),      # Dark green
                (80, 160, 100),    # Medium green
                (120, 200, 140),   # Light green
                (180, 255, 200),   # Bright green
            ],
            'space_nebula': [
                (10, 5, 25),       # Deep space
                (30, 20, 60),      # Dark purple
                (60, 40, 100),     # Medium purple
                (100, 80, 150),    # Light purple
                (150, 120, 200),   # Bright purple
            ],
            'solar_energy': [
                (40, 30, 0),       # Dark gold
                (100, 80, 20),     # Bronze
                (200, 160, 60),    # Gold
                (255, 220, 120),   # Light gold
                (255, 255, 200),   # Bright yellow
            ],
            'cyberspace': [
                (0, 20, 20),       # Dark cyan
                (20, 60, 60),      # Teal
                (40, 120, 120),    # Cyan
                (80, 200, 200),    # Light cyan
                (150, 255, 255),   # Bright cyan
            ]
        }

    def hash_function(self, x: int, y: int, seed: int = 12345) -> float:
        """
        Hash function for pseudo-random generation
        Uses bit operations and modular arithmetic
        """
        # Mix coordinates with seed using prime numbers
        h = seed
        h = (h ^ (x * 73856093)) % 2147483647
        h = (h ^ (y * 19349663)) % 2147483647
        h = (h ^ (h >> 16)) % 2147483647
        h = (h * 2654435761) % 2147483647

        return (h & 0xFFFF) / 0xFFFF

    def perlin_like_noise(self, x: int, y: int, scale: float = 32.0, seed: int = 0) -> float:
        """
        Simplified Perlin-like noise using hash interpolation
        """
        # Scale coordinates
        sx = x / scale
        sy = y / scale

        # Get integer coordinates
        x0 = int(math.floor(sx))
        y0 = int(math.floor(sy))
        x1 = x0 + 1
        y1 = y0 + 1

        # Get fractional parts
        fx = sx - x0
        fy = sy - y0

        # Smooth interpolation (cubic)
        u = fx * fx * (3.0 - 2.0 * fx)
        v = fy * fy * (3.0 - 2.0 * fy)

        # Get corner values using hash
        n00 = self.hash_function(x0, y0, seed)
        n10 = self.hash_function(x1, y0, seed)
        n01 = self.hash_function(x0, y1, seed)
        n11 = self.hash_function(x1, y1, seed)

        # Bilinear interpolation
        nx0 = n00 * (1 - u) + n10 * u
        nx1 = n01 * (1 - u) + n11 * u
        return nx0 * (1 - v) + nx1 * v

    def cellular_automata(self, iterations: int = 5, alive_threshold: float = 0.5) -> Image.Image:
        """
        Generate patterns using cellular automata (Conway's Game of Life variant)
        """
        # Initialize random grid using hash function
        grid = [[self.hash_function(x, y) > alive_threshold
                 for y in range(self.height)]
                for x in range(self.width)]

        # Run cellular automata
        for _ in range(iterations):
            new_grid = [[False for y in range(self.height)]
                        for x in range(self.width)]

            for x in range(self.width):
                for y in range(self.height):
                    # Count neighbors (toroidal topology - ring-0!)
                    neighbors = 0
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            if dx == 0 and dy == 0:
                                continue
                            nx = (x + dx) % self.width
                            ny = (y + dy) % self.height
                            if grid[nx][ny]:
                                neighbors += 1

                    # Game of Life rules (with variations)
                    if grid[x][y]:
                        new_grid[x][y] = neighbors in [2, 3]
                    else:
                        new_grid[x][y] = neighbors == 3

            grid = new_grid

        # Convert to image
        img = Image.new('RGB', (self.width, self.height))
        pixels = img.load()

        palette = self.palettes['solarpunk_green']
        for x in range(self.width):
            for y in range(self.height):
                if grid[x][y]:
                    pixels[x, y] = palette[3]  # Alive cells
                else:
                    pixels[x, y] = palette[0]  # Dead cells

        return img

    def fractal_noise_texture(self, octaves: int = 4, palette_name: str = 'space_nebula') -> Image.Image:
        """
        Generate fractal noise texture using multiple octaves
        f(x, y) = Σ(amplitude_i * noise(frequency_i * x, frequency_i * y))
        """
        img = Image.new('RGB', (self.width, self.height))
        pixels = img.load()

        palette = self.palettes[palette_name]

        for x in range(self.width):
            for y in range(self.height):
                value = 0
                amplitude = 1.0
                frequency = 1.0
                max_value = 0

                # Combine octaves
                for octave in range(octaves):
                    value += amplitude * self.perlin_like_noise(
                        x, y,
                        scale=32.0 / frequency,
                        seed=octave * 1000
                    )
                    max_value += amplitude
                    amplitude *= 0.5
                    frequency *= 2.0

                # Normalize
                value /= max_value

                # Map to palette
                color_index = min(int(value * len(palette)), len(palette) - 1)
                pixels[x, y] = palette[color_index]

        return img

    def binary_field_pattern(self) -> Image.Image:
        """
        Generate pattern using binary field operations (XOR, AND, OR)
        GF(2) arithmetic - finite field of order 2
        """
        img = Image.new('RGB', (self.width, self.height))
        pixels = img.load()

        palette = self.palettes['cyberspace']

        for x in range(self.width):
            for y in range(self.height):
                # Binary operations on coordinates
                # f(i) = -i can be represented as NOT in binary
                xor_val = (x ^ y) & 0xFF
                and_val = (x & y) & 0xFF
                or_val = (x | y) & 0xFF

                # Combine operations
                combined = (xor_val + and_val * 2 + or_val) % 256

                # Map to palette
                color_index = (combined * len(palette)) // 256
                pixels[x, y] = palette[color_index]

        return img

    def voronoi_diagram(self, num_points: int = 20, palette_name: str = 'solar_energy') -> Image.Image:
        """
        Generate Voronoi diagram using distance transforms
        Each point represents a region in space
        """
        img = Image.new('RGB', (self.width, self.height))
        pixels = img.load()

        palette = self.palettes[palette_name]

        # Generate random points using hash function
        points = []
        for i in range(num_points):
            x = int(self.hash_function(i, 0) * self.width)
            y = int(self.hash_function(i, 1) * self.height)
            points.append((x, y))

        # For each pixel, find nearest point
        for x in range(self.width):
            for y in range(self.height):
                min_dist = float('inf')
                nearest_idx = 0

                for idx, (px, py) in enumerate(points):
                    # Euclidean distance (could use Manhattan or other metrics)
                    dist = math.sqrt((x - px)**2 + (y - py)**2)
                    if dist < min_dist:
                        min_dist = dist
                        nearest_idx = idx

                # Color based on nearest point
                color_index = nearest_idx % len(palette)
                pixels[x, y] = palette[color_index]

        return img

    def mandelbrot_set(self, max_iter: int = 50, palette_name: str = 'space_nebula') -> Image.Image:
        """
        Generate Mandelbrot set fractal
        f(z) = z² + c, iterate in complex plane
        """
        img = Image.new('RGB', (self.width, self.height))
        pixels = img.load()

        palette = self.palettes[palette_name]

        # Complex plane bounds
        x_min, x_max = -2.5, 1.5
        y_min, y_max = -2.0, 2.0

        for px in range(self.width):
            for py in range(self.height):
                # Map pixel to complex plane
                cx = x_min + (px / self.width) * (x_max - x_min)
                cy = y_min + (py / self.height) * (y_max - y_min)

                # Iterate f(z) = z² + c
                zx, zy = 0, 0
                iteration = 0

                while zx*zx + zy*zy < 4 and iteration < max_iter:
                    # z² = (zx + i·zy)² = (zx² - zy²) + i·(2·zx·zy)
                    zx_new = zx*zx - zy*zy + cx
                    zy_new = 2*zx*zy + cy
                    zx, zy = zx_new, zy_new
                    iteration += 1

                # Map iteration count to color
                if iteration == max_iter:
                    pixels[px, py] = (0, 0, 0)
                else:
                    color_index = (iteration * len(palette)) // max_iter
                    pixels[px, py] = palette[color_index]

        return img

    def tilemap_generator(self, tile_size: int = 16) -> Image.Image:
        """
        Generate tilemap for game backgrounds
        Uses multiple techniques combined
        """
        tiles_x = self.width // tile_size
        tiles_y = self.height // tile_size

        img = Image.new('RGB', (self.width, self.height))
        draw = ImageDraw.Draw(img)

        palette = self.palettes['solarpunk_green']

        for tx in range(tiles_x):
            for ty in range(tiles_y):
                # Use hash to determine tile type
                tile_hash = self.hash_function(tx, ty)

                # Choose tile color based on hash
                color_idx = int(tile_hash * len(palette))
                color = palette[color_idx]

                # Draw tile
                x1 = tx * tile_size
                y1 = ty * tile_size
                x2 = x1 + tile_size
                y2 = y1 + tile_size

                draw.rectangle([x1, y1, x2, y2], fill=color)

                # Add detail based on tile type
                if tile_hash > 0.7:
                    # Add grid
                    draw.rectangle([x1, y1, x2, y2], outline=palette[-1], width=1)
                elif tile_hash > 0.4:
                    # Add dot
                    cx = (x1 + x2) // 2
                    cy = (y1 + y2) // 2
                    draw.ellipse([cx-2, cy-2, cx+2, cy+2], fill=palette[-2])

        return img


def main():
    """Generate all procedural textures"""
    print("=" * 70)
    print("BINARY ART GENERATOR - Solarpunk Space Textures")
    print("Mathematical Foundation: NO NEURONS | Pure Functional Transforms")
    print("=" * 70)

    generator = BinaryArtGenerator(width=512, height=512)

    print("\n🎨 Generating textures...")

    # 1. Cellular Automata
    print("  1. Cellular Automata (Game of Life variant)...")
    img = generator.cellular_automata(iterations=8)
    img.save(f"{generator.output_dir}/01_cellular_automata.png")

    # 2. Fractal Noise (Space Nebula)
    print("  2. Fractal Noise - Space Nebula...")
    img = generator.fractal_noise_texture(octaves=5, palette_name='space_nebula')
    img.save(f"{generator.output_dir}/02_space_nebula.png")

    # 3. Fractal Noise (Solarpunk)
    print("  3. Fractal Noise - Solarpunk...")
    img = generator.fractal_noise_texture(octaves=4, palette_name='solarpunk_green')
    img.save(f"{generator.output_dir}/03_solarpunk_terrain.png")

    # 4. Binary Field Pattern
    print("  4. Binary Field Pattern (XOR/AND/OR)...")
    img = generator.binary_field_pattern()
    img.save(f"{generator.output_dir}/04_binary_field.png")

    # 5. Voronoi Diagram
    print("  5. Voronoi Diagram - Solar Energy...")
    img = generator.voronoi_diagram(num_points=30, palette_name='solar_energy')
    img.save(f"{generator.output_dir}/05_voronoi_solar.png")

    # 6. Mandelbrot Set
    print("  6. Mandelbrot Set Fractal...")
    img = generator.mandelbrot_set(max_iter=100, palette_name='space_nebula')
    img.save(f"{generator.output_dir}/06_mandelbrot.png")

    # 7. Tilemap
    print("  7. Game Tilemap...")
    img = generator.tilemap_generator(tile_size=32)
    img.save(f"{generator.output_dir}/07_tilemap.png")

    # 8. Cyberspace Grid
    print("  8. Cyberspace Grid...")
    img = generator.fractal_noise_texture(octaves=3, palette_name='cyberspace')
    img.save(f"{generator.output_dir}/08_cyberspace.png")

    print(f"\n✅ All textures generated successfully!")
    print(f"📁 Output directory: {generator.output_dir}/")
    print(f"\nGenerated files:")
    for i in range(1, 9):
        print(f"  - {i:02d}_*.png")

    print("\n" + "=" * 70)
    print("Mathematical techniques used:")
    print("  • Cellular Automata (Conway's Game of Life)")
    print("  • Fractal Noise (Multi-octave Perlin-like)")
    print("  • Binary Field Operations (GF(2) arithmetic)")
    print("  • Voronoi Diagrams (Distance transforms)")
    print("  • Mandelbrot Set (Complex plane iteration)")
    print("  • Hash Functions (Pseudo-random generation)")
    print("  • Toroidal Topology (Ring-0 wrapping)")
    print("=" * 70)


if __name__ == "__main__":
    main()
