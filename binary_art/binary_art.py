#!/usr/bin/env python3
"""
Binary Art Generator - Pure Algorithmic Image Generation
No neural networks, no ML - just mathematics and deterministic algorithms.

Uses hex codes as seeds for procedural generation of abstract art.
"""

from PIL import Image, ImageDraw
import math
import random


class HexArtGenerator:
    """Generate procedural art from hex codes using pure mathematics."""

    def __init__(self, hex_code: str, width: int = 800, height: int = 800):
        self.hex_code = hex_code.replace('-', '').upper()
        self.width = width
        self.height = height

        # Parse hex code into components for different algorithms
        self.parse_hex_code()

    def parse_hex_code(self):
        """Extract numerical parameters from hex code."""
        # Split hex into parts
        if len(self.hex_code) >= 8:
            self.seed1 = int(self.hex_code[:4], 16)  # First 4 chars
            self.seed2 = int(self.hex_code[4:8], 16)  # Next 4 chars
        else:
            self.seed1 = int(self.hex_code[:len(self.hex_code)//2], 16)
            self.seed2 = int(self.hex_code[len(self.hex_code)//2:], 16)

        # Derive colors from hex
        self.color1 = self._hex_to_rgb(self.hex_code[:6] if len(self.hex_code) >= 6 else self.hex_code + '0' * (6 - len(self.hex_code)))

        # Use seeds for random but deterministic generation
        random.seed(self.seed1 ^ self.seed2)

    def _hex_to_rgb(self, hex_str: str) -> tuple:
        """Convert hex string to RGB tuple."""
        if len(hex_str) < 6:
            hex_str = hex_str + '0' * (6 - len(hex_str))
        r = int(hex_str[0:2], 16)
        g = int(hex_str[2:4], 16)
        b = int(hex_str[4:6], 16)
        return (r, g, b)

    def generate_fractal_pattern(self):
        """Generate a fractal-based image using the hex seed."""
        img = Image.new('RGB', (self.width, self.height), 'black')
        pixels = img.load()

        # Parameters derived from seeds
        zoom = self.seed1 / 10000.0
        offset_x = (self.seed2 % 1000) / 500.0 - 1.0
        offset_y = ((self.seed2 // 1000) % 1000) / 500.0 - 1.0
        max_iter = 50 + (self.seed1 % 100)

        for x in range(self.width):
            for y in range(self.height):
                # Map pixel to complex plane
                zx = (x - self.width / 2) / (self.width / 4) * zoom + offset_x
                zy = (y - self.height / 2) / (self.height / 4) * zoom + offset_y

                # Mandelbrot-like iteration
                cx, cy = zx, zy
                iteration = 0

                while zx*zx + zy*zy < 4 and iteration < max_iter:
                    tmp = zx*zx - zy*zy + cx
                    zy = 2*zx*zy + cy
                    zx = tmp
                    iteration += 1

                # Color based on iteration count
                if iteration == max_iter:
                    pixels[x, y] = (0, 0, 0)
                else:
                    hue = int(255 * iteration / max_iter)
                    r = (self.color1[0] * hue) // 255
                    g = (self.color1[1] * hue) // 255
                    b = (self.color1[2] * hue) // 255
                    pixels[x, y] = (r, g, b)

        return img

    def generate_wave_interference(self):
        """Generate interference patterns from wave equations."""
        img = Image.new('RGB', (self.width, self.height), 'black')
        pixels = img.load()

        # Wave parameters from seeds
        freq1 = (self.seed1 % 20 + 1) / 10.0
        freq2 = (self.seed2 % 20 + 1) / 10.0
        phase1 = (self.seed1 % 360) * math.pi / 180
        phase2 = (self.seed2 % 360) * math.pi / 180

        for x in range(self.width):
            for y in range(self.height):
                # Normalized coordinates
                nx = x / self.width
                ny = y / self.height

                # Multiple wave interference
                wave1 = math.sin(nx * freq1 * math.pi * 2 + phase1)
                wave2 = math.sin(ny * freq2 * math.pi * 2 + phase2)
                wave3 = math.cos((nx + ny) * freq1 * math.pi + phase1)
                wave4 = math.cos((nx - ny) * freq2 * math.pi + phase2)

                # Combine waves
                intensity = (wave1 + wave2 + wave3 + wave4) / 4.0
                intensity = (intensity + 1) / 2  # Normalize to 0-1

                # Apply color gradient
                value = int(intensity * 255)
                r = (self.color1[0] * value) // 255
                g = (self.color1[1] * value) // 255
                b = (self.color1[2] * value) // 255
                pixels[x, y] = (r, g, b)

        return img

    def generate_cellular_automata(self):
        """Generate patterns using cellular automata rules."""
        img = Image.new('RGB', (self.width, self.height), 'black')
        pixels = img.load()

        # Initialize grid with random state based on seed
        grid = [[random.random() > 0.5 for _ in range(self.width)] for _ in range(self.height)]

        # Rule derived from hex code
        rule_num = (self.seed1 + self.seed2) % 256

        # Apply cellular automata rules
        for y in range(1, self.height):
            for x in range(self.width):
                # Get neighbors
                left = grid[y-1][(x-1) % self.width]
                center = grid[y-1][x]
                right = grid[y-1][(x+1) % self.width]

                # Convert to rule index
                idx = (left << 2) | (center << 1) | right

                # Apply rule
                grid[y][x] = bool((rule_num >> idx) & 1)

                # Set pixel color
                if grid[y][x]:
                    pixels[x, y] = self.color1
                else:
                    # Darker variant
                    pixels[x, y] = (self.color1[0]//4, self.color1[1]//4, self.color1[2]//4)

        return img

    def generate_geometric_pattern(self):
        """Generate geometric patterns using circles and lines."""
        img = Image.new('RGB', (self.width, self.height), (20, 20, 30))
        draw = ImageDraw.Draw(img)

        # Parameters from seeds
        num_shapes = (self.seed1 % 50) + 10
        rotation_factor = (self.seed2 % 360) / 360.0

        cx, cy = self.width // 2, self.height // 2

        for i in range(num_shapes):
            angle = (i / num_shapes) * math.pi * 2 + rotation_factor * math.pi * 2
            radius = (i / num_shapes) * min(self.width, self.height) // 2

            # Calculate position
            x = cx + int(radius * math.cos(angle))
            y = cy + int(radius * math.sin(angle))

            # Circle size based on position
            circle_r = max(5, (self.seed1 % 30) * (i % 5 + 1) // 10)

            # Color variation
            hue = int(255 * i / num_shapes)
            r = (self.color1[0] * hue) // 255
            g = (self.color1[1] * hue) // 255
            b = (self.color1[2] * hue) // 255

            draw.ellipse([x - circle_r, y - circle_r, x + circle_r, y + circle_r],
                        fill=(r, g, b), outline=(r+50, g+50, b+50))

            # Draw connecting lines
            if i > 0:
                prev_angle = ((i-1) / num_shapes) * math.pi * 2 + rotation_factor * math.pi * 2
                prev_radius = ((i-1) / num_shapes) * min(self.width, self.height) // 2
                px = cx + int(prev_radius * math.cos(prev_angle))
                py = cy + int(prev_radius * math.sin(prev_angle))
                draw.line([px, py, x, y], fill=(r//2, g//2, b//2), width=2)

        return img

    def generate_all(self, output_dir='output'):
        """Generate all pattern types."""
        import os
        os.makedirs(output_dir, exist_ok=True)

        print(f"Generating art from hex code: {self.hex_code}")
        print(f"Seed 1: {self.seed1}, Seed 2: {self.seed2}")
        print(f"Primary Color: RGB{self.color1}")

        patterns = [
            ('fractal', self.generate_fractal_pattern),
            ('wave', self.generate_wave_interference),
            ('cellular', self.generate_cellular_automata),
            ('geometric', self.generate_geometric_pattern),
        ]

        generated_files = []
        for name, generator_func in patterns:
            filename = f"{output_dir}/{self.hex_code}_{name}.png"
            print(f"  Generating {name} pattern...")
            img = generator_func()
            img.save(filename)
            generated_files.append(filename)
            print(f"    Saved: {filename}")

        return generated_files


def main():
    """Main entry point."""
    # The hex code from the request
    hex_code = "4CD7-B18D"

    print("=" * 60)
    print("BINARY ART GENERATOR - Pure Algorithmic Image Generation")
    print("No neural networks. No machine learning. Just mathematics.")
    print("=" * 60)
    print()

    generator = HexArtGenerator(hex_code, width=800, height=800)
    files = generator.generate_all()

    print()
    print("=" * 60)
    print(f"Generated {len(files)} images successfully!")
    print("=" * 60)

    return files


if __name__ == "__main__":
    main()
