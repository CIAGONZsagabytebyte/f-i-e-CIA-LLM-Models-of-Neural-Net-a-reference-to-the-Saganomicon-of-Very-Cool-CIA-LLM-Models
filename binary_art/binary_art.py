"""
Binary Art Generator for Solarpunk Space Starter Kit
Generates procedural tilemaps and textures from binary patterns
Pure algorithmic approach using mathematical transformations
No neural networks or ML - just beautiful math!
"""

import random
import os
from PIL import Image, ImageDraw
import math


class BinaryArtGenerator:
    """Generate procedural art from binary patterns"""

    def __init__(self, width=512, height=512):
        self.width = width
        self.height = height

    def generate_from_seed(self, seed):
        """Generate art from a numeric seed"""
        random.seed(seed)

        # Convert seed to binary and use it as pattern
        binary = bin(seed)[2:].zfill(32)
        return binary

    def binary_to_tilemap(self, binary_pattern, tile_size=32):
        """Convert binary pattern to a tilemap texture"""
        img = Image.new('RGB', (self.width, self.height), color=(10, 5, 30))
        draw = ImageDraw.Draw(img)

        cols = self.width // tile_size
        rows = self.height // tile_size

        # Extend pattern if needed
        pattern_length = len(binary_pattern)
        extended_pattern = binary_pattern * ((cols * rows) // pattern_length + 1)

        for row in range(rows):
            for col in range(cols):
                idx = row * cols + col
                bit = int(extended_pattern[idx % len(extended_pattern)])

                x = col * tile_size
                y = row * tile_size

                if bit == 1:
                    # Solarpunk green tile
                    color = self._get_solarpunk_color(row, col)
                    draw.rectangle([x, y, x + tile_size, y + tile_size],
                                 fill=color, outline=(50, 200, 100))
                else:
                    # Space/dark tile
                    color = self._get_space_color(row, col)
                    draw.rectangle([x, y, x + tile_size, y + tile_size],
                                 fill=color)

        return img

    def _get_solarpunk_color(self, row, col):
        """Get a variant of solarpunk green"""
        base_green = 200 + random.randint(-50, 50)
        return (100, min(255, base_green), 150)

    def _get_space_color(self, row, col):
        """Get a variant of deep space color"""
        variance = random.randint(-5, 10)
        return (10 + variance, 5 + variance, 30 + variance)

    def generate_starfield(self, star_count=200, layers=3):
        """Generate a procedural starfield background"""
        img = Image.new('RGB', (self.width, self.height), color=(10, 5, 30))
        draw = ImageDraw.Draw(img)

        for layer in range(layers):
            stars_in_layer = star_count // layers

            for _ in range(stars_in_layer):
                x = random.randint(0, self.width)
                y = random.randint(0, self.height)
                size = layer + 1
                brightness = 150 + random.randint(0, 105)
                color = (brightness, brightness, brightness)

                draw.ellipse([x - size, y - size, x + size, y + size], fill=color)

        return img

    def generate_nebula(self):
        """Generate a procedural nebula using complex number mathematics"""
        img = Image.new('RGB', (self.width, self.height), color=(10, 5, 30))
        pixels = img.load()

        # Use complex number transformations
        for y in range(self.height):
            for x in range(self.width):
                # Map pixel to complex plane
                cx = (x - self.width / 2) / (self.width / 4)
                cy = (y - self.height / 2) / (self.height / 4)
                c = complex(cx, cy)

                # Apply complex function: f(z) = z^2 + c
                z = complex(0, 0)
                iterations = 0
                max_iterations = 50

                while abs(z) < 2 and iterations < max_iterations:
                    z = z * z + c * 0.3
                    iterations += 1

                # Map iterations to solarpunk colors
                if iterations < max_iterations:
                    ratio = iterations / max_iterations
                    r = int(100 * ratio)
                    g = int(150 + 105 * ratio)
                    b = int(150 * (1 - ratio))
                    pixels[x, y] = (r, g, b)
                else:
                    pixels[x, y] = (10, 5, 30)

        return img

    def generate_circuit_pattern(self):
        """Generate circuit-like patterns for tech aesthetic"""
        img = Image.new('RGB', (self.width, self.height), color=(10, 5, 30))
        draw = ImageDraw.Draw(img)

        # Generate random circuit paths
        num_circuits = 20

        for _ in range(num_circuits):
            start_x = random.randint(0, self.width)
            start_y = random.randint(0, self.height)

            current_x = start_x
            current_y = start_y

            # Draw circuit path
            path_length = random.randint(5, 15)
            color = (100, 255, 150) if random.random() > 0.5 else (255, 220, 100)

            for _ in range(path_length):
                # Random direction (up, down, left, right)
                direction = random.choice(['up', 'down', 'left', 'right'])
                length = random.randint(20, 100)

                new_x = current_x
                new_y = current_y

                if direction == 'up':
                    new_y -= length
                elif direction == 'down':
                    new_y += length
                elif direction == 'left':
                    new_x -= length
                elif direction == 'right':
                    new_x += length

                # Keep in bounds
                new_x = max(0, min(new_x, self.width))
                new_y = max(0, min(new_y, self.height))

                # Draw line
                draw.line([current_x, current_y, new_x, new_y],
                         fill=color, width=2)

                # Draw junction circle
                draw.ellipse([current_x - 4, current_y - 4,
                            current_x + 4, current_y + 4],
                           fill=color)

                current_x = new_x
                current_y = new_y

        return img

    def generate_solar_panel_pattern(self):
        """Generate solar panel tile pattern"""
        img = Image.new('RGB', (self.width, self.height), color=(20, 10, 40))
        draw = ImageDraw.Draw(img)

        panel_size = 64
        gap = 4

        for y in range(0, self.height, panel_size + gap):
            for x in range(0, self.width, panel_size + gap):
                # Panel background
                draw.rectangle([x, y, x + panel_size, y + panel_size],
                             fill=(30, 40, 60), outline=(50, 100, 150))

                # Cell grid
                cells = 4
                cell_size = panel_size // cells

                for cy in range(cells):
                    for cx in range(cells):
                        cell_x = x + cx * cell_size + 2
                        cell_y = y + cy * cell_size + 2

                        # Slight color variation for each cell
                        brightness = random.randint(-20, 20)
                        color = (30 + brightness, 60 + brightness, 100 + brightness)

                        draw.rectangle([cell_x, cell_y,
                                      cell_x + cell_size - 4,
                                      cell_y + cell_size - 4],
                                     fill=color)

        return img

    def generate_fractal_plant(self):
        """Generate fractal plant pattern using L-systems"""
        img = Image.new('RGB', (self.width, self.height), color=(10, 5, 30))
        draw = ImageDraw.Draw(img)

        # Simple L-system for plant-like structure
        # F = draw forward, + = turn right, - = turn left
        axiom = "F"
        rules = {"F": "F[+F]F[-F]F"}

        # Generate L-system
        current = axiom
        for _ in range(4):
            next_gen = ""
            for char in current:
                next_gen += rules.get(char, char)
            current = next_gen

        # Draw the L-system
        angle = 25
        length = 3

        x = self.width // 2
        y = self.height - 50
        current_angle = -90

        stack = []

        for cmd in current:
            if cmd == 'F':
                # Draw forward
                new_x = x + length * math.cos(math.radians(current_angle))
                new_y = y + length * math.sin(math.radians(current_angle))

                color = (100, 200 + random.randint(-50, 50), 150)
                draw.line([x, y, new_x, new_y], fill=color, width=2)

                x = new_x
                y = new_y
            elif cmd == '+':
                current_angle += angle
            elif cmd == '-':
                current_angle -= angle
            elif cmd == '[':
                stack.append((x, y, current_angle))
            elif cmd == ']':
                if stack:
                    x, y, current_angle = stack.pop()

        return img


def main():
    """Generate all procedural art variants"""
    output_dir = "binary_art/output"
    os.makedirs(output_dir, exist_ok=True)

    print("🌱 Solarpunk Binary Art Generator 🎨")
    print("Generating procedural textures...\n")

    generator = BinaryArtGenerator(512, 512)

    # 1. Binary tilemap
    print("Generating binary tilemap...")
    seed = random.randint(1000, 9999)
    binary = generator.generate_from_seed(seed)
    tilemap = generator.binary_to_tilemap(binary, tile_size=32)
    tilemap.save(f"{output_dir}/binary_tilemap.png")
    print(f"✓ Saved: binary_tilemap.png (seed: {seed})")

    # 2. Starfield
    print("Generating starfield...")
    starfield = generator.generate_starfield(star_count=300, layers=3)
    starfield.save(f"{output_dir}/starfield.png")
    print("✓ Saved: starfield.png")

    # 3. Nebula (using complex numbers)
    print("Generating nebula with complex number math...")
    nebula = generator.generate_nebula()
    nebula.save(f"{output_dir}/nebula.png")
    print("✓ Saved: nebula.png")

    # 4. Circuit pattern
    print("Generating circuit pattern...")
    circuits = generator.generate_circuit_pattern()
    circuits.save(f"{output_dir}/circuits.png")
    print("✓ Saved: circuits.png")

    # 5. Solar panel pattern
    print("Generating solar panel pattern...")
    solar = generator.generate_solar_panel_pattern()
    solar.save(f"{output_dir}/solar_panels.png")
    print("✓ Saved: solar_panels.png")

    # 6. Fractal plant
    print("Generating fractal plant...")
    plant = generator.generate_fractal_plant()
    plant.save(f"{output_dir}/fractal_plant.png")
    print("✓ Saved: fractal_plant.png")

    print(f"\n✨ All textures generated in {output_dir}/")
    print("Use these as backgrounds or assets in your games!")


if __name__ == "__main__":
    main()
