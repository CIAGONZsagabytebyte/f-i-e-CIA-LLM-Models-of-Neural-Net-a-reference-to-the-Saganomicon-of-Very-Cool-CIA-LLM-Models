# Solarpunk Space Starter Kit - v2

This repository contains small prototypes and utilities to start building games and apps with a solarpunk + space-travel aesthetic.

## Projects included:

### 1. Python / Pygame Prototype (v2 - Playable Demo)
A playable 2D demo with solarpunk aesthetics.
- **Gameplay**: Fly your ship, collect "Solar Orbs" to score points, and avoid floating "Debris".
- **Features**: Player movement, parallax background, collectibles, obstacles with pixel-perfect collision, and a simple game-over/restart loop.
- **Code**: Now organized into `main.py` (game loop) and `game_objects.py` (game entities).

**How to run:**
  1. Install dependencies: `pip install pygame`
  2. Run: `python pygame_solarpunk/main.py`

### 2. Web Canvas Prototype (HTML/JS)
Lightweight, shareable mini-game for browser.
- Pure HTML/CSS/JavaScript
- No frameworks required
- Works offline

**How to run:**
  1. Open `web_solarpunk/index.html` in a browser (or serve with `python -m http.server`).

### 3. Binary Art Generator (Python)
**Pure algorithmic image generation - NO neural networks, NO machine learning!**

Generates procedural art using mathematical algorithms:
- **Fractal patterns** - Mandelbrot-like iterations
- **Wave interference** - Sine/cosine wave equations
- **Cellular automata** - Rule-based evolution
- **Geometric patterns** - Mathematical spirals and circles

Uses hex codes as seeds for deterministic generation.

**How to run:**
  1. Install dependencies: `pip install pillow`
  2. Run: `python binary_art/binary_art.py` — generates PNGs in the `binary_art/output/` folder.
  3. Generated images: `4CD7B18D_*.png` files

### 4. Unity C# Snippet
A spaceship controller for 2D or 3D Unity scenes.
- Works with both Rigidbody2D and Rigidbody
- Solar energy boost system
- Configurable movement parameters

**How to run:**
  1. Create a Unity project, add the C# script to a GameObject.
  2. Attach a Rigidbody (3D) or Rigidbody2D (2D) component.
  3. Configure movement parameters in the Inspector.

## Design Notes and Next Steps
- **Assets**: Replace placeholder procedural art with your own solarpunk sprites: lush vertical gardens on asteroids, ships with solar sails, and floating eco-domes.
- **Sound**: Add soundscapes (ambient synth, nature sounds, collection chimes) to enhance the solarpunk vibe.
- **Mechanics**: Expand gameplay with resource-gathering, ship upgrades, or trade routes between habitats.

## Image Generation - Ring0 Algorithm

The binary art generator uses **pure deterministic mathematics** - zero neural networks:

```python
# Hex code "4CD7-B18D" becomes:
# Seed 1: 19671 (0x4CD7)
# Seed 2: 45453 (0xB18D)
# Color: RGB(76, 215, 177) - extracted from hex

# All patterns generated using:
# - Complex number iteration (fractals)
# - Trigonometric functions (waves)
# - Cellular automata rules
# - Parametric equations (geometry)
```

## What's Next?

Tell me which direction you'd like to go:
1.  **Expand Pygame**: Add levels, new enemy/obstacle types, or a weapon system.
2.  **Upgrade Web**: Convert the web prototype into a more robust game using a framework like Phaser.js.
3.  **Go 3D**: Build a basic Unity scene using the C# controller and procedural assets.
4.  **Try Godot**: Create a new prototype in the Godot engine, known for its ease of use.
5.  **More Art**: Generate more procedural art with different algorithms and patterns.

I will produce the next set of files and a development plan based on your choice.
