# Solarpunk Space Starter Kit - v2

**Ring-0 Edition | f(i) = -i | No Neurons, Pure Mathematics**

A collection of small prototypes and utilities for building games and apps with a solarpunk + space-travel aesthetic, built entirely on mathematical foundations **WITHOUT any neural networks or ML units**.

## 🌿 Philosophy

This starter kit embraces **pure functional programming** and **mathematical transformations** instead of neural networks:

- **Complex Number Rotations**: `z * e^(iθ)` for smooth rotations
- **Ring Theory**: Toroidal topology via modular arithmetic (Ring-0 wrapping)
- **Harmonic Oscillators**: `f(t) = A·sin(ωt)` for natural animations
- **Binary Field Operations**: GF(2) arithmetic for procedural generation
- **Fractal Mathematics**: Mandelbrot sets, Perlin noise, cellular automata
- **Vector Fields**: Force integration and physics simulation

**f(i) = -i** - The complex conjugate transformation represents our philosophy: reflection, inversion, and mathematical elegance.

---

## 📦 Projects Included

### 1. Python / Pygame Prototype (v2 - Playable Demo)

A fully playable 2D space game with mathematical physics.

**Features:**
- Player ship with complex number rotation transforms
- Parallax starfield using affine transformations
- Collectible "Solar Orbs" with harmonic oscillation
- Floating "Debris" obstacles with chaotic rotation
- Pixel-perfect collision detection
- Ring-0 boundary wrapping (toroidal space)
- Trail effects and particle systems
- Game over/restart loop

**Code Organization:**
- `pygame_solarpunk/main.py` - Main game loop and state management
- `pygame_solarpunk/game_objects.py` - All game entities with mathematical transforms

**How to Run:**
```bash
# Install dependencies
pip install pygame

# Run the game
python pygame_solarpunk/main.py
```

**Controls:**
- Arrow Keys / WASD: Move ship
- ESC: Quit
- R: Restart after game over

**Mathematical Concepts Used:**
- Complex rotation: `(x,y) → (x·cos(θ) - y·sin(θ), x·sin(θ) + y·cos(θ))`
- Ring kernel: `x mod W` for boundary wrapping
- Harmonic oscillation: `r(t) = r₀ + A·sin(ωt)`
- Parallax: Depth-based velocity scaling

---

### 2. Web Canvas Prototype (HTML/JS)

Lightweight, shareable browser-based mini-game.

**Features:**
- Pure JavaScript - no frameworks required
- Complex number mathematics for movement
- Harmonic oscillators for pulsing effects
- Toroidal topology (wrap-around space)
- Click-to-restart game loop

**How to Run:**
```bash
# Option 1: Direct open
Open web_solarpunk/index.html in any modern browser

# Option 2: Local server
cd web_solarpunk
python -m http.server 8000
# Then visit http://localhost:8000
```

**Controls:**
- Arrow Keys / WASD: Move ship
- Click: Restart after game over

**Mathematical Engine:**
```javascript
ComplexMath.rotate(x, y, angle)      // Complex multiplication
ComplexMath.conjugate(x, y)          // f(i) = -i transformation
ComplexMath.ringKernel(value, mod)   // Ring-0 wrapping
ComplexMath.harmonicOscillator(...)  // Sinusoidal animation
```

---

### 3. Binary Art Generator (Python)

Procedural texture and tilemap generator using pure mathematics.

**Features:**
- Cellular automata (Conway's Game of Life variants)
- Multi-octave fractal noise (Perlin-like)
- Binary field patterns (XOR, AND, OR operations)
- Voronoi diagrams (distance transforms)
- Mandelbrot set fractals
- Tilemap generation for game backgrounds
- Multiple solarpunk color palettes

**How to Run:**
```bash
# Install dependencies
pip install pillow

# Generate all textures
python binary_art/binary_art.py
```

**Output:**
Generates 8 different procedural textures in `binary_art/output/`:
1. `01_cellular_automata.png` - Game of Life pattern
2. `02_space_nebula.png` - Fractal noise (purple)
3. `03_solarpunk_terrain.png` - Fractal noise (green)
4. `04_binary_field.png` - XOR/AND/OR patterns
5. `05_voronoi_solar.png` - Voronoi diagram (gold)
6. `06_mandelbrot.png` - Mandelbrot set fractal
7. `07_tilemap.png` - Game tilemap
8. `08_cyberspace.png` - Cyberspace grid (cyan)

**Mathematical Techniques:**
- **Cellular Automata**: `cell(t+1) = f(neighbors(t))`
- **Fractal Noise**: `noise(x,y) = Σᵢ aᵢ·n(fᵢ·x, fᵢ·y)`
- **Binary Fields**: GF(2) arithmetic on coordinates
- **Mandelbrot**: `z_{n+1} = z_n² + c` in complex plane
- **Hash Functions**: Pseudo-random generation

---

### 4. Unity C# Spaceship Controller

Professional 3D spaceship controller for Unity projects.

**Features:**
- Quaternion-based rotation (no gimbal lock!)
- Vector field physics simulation
- Boost system with visual feedback
- Ring-0 boundary wrapping for infinite space
- Trail renderer support
- Particle system integration
- Configurable parameters via Inspector

**How to Use:**

1. **Create Unity Project**:
   - Open Unity Hub → New Project → 3D

2. **Add Spaceship**:
   - Create GameObject (cube/capsule or import 3D model)
   - Add Component → Physics → Rigidbody
   - Disable "Use Gravity"

3. **Add Controller**:
   - Drag `unity_scripts/SpaceshipController.cs` into project
   - Add Component → SpaceshipController to ship

4. **Configure**:
   - Thrust Force: 10-20
   - Rotation Speed: 100-200
   - Enable Wrapping: ✓
   - Set Boundaries (X, Y, Z)

5. **Optional Visuals**:
   - Add Component → Effects → Trail Renderer → Assign to "Ship Trail"
   - Add Component → Effects → Particle System → Assign to "Engine Exhaust"

**Controls:**
- W/S or Up/Down: Forward/Backward thrust
- A/D or Left/Right: Strafe sideways
- Q/E: Rotate (yaw)
- Space: Boost

**Mathematical Foundation:**
```csharp
// Quaternion rotation (no gimbal lock)
Quaternion.Euler(angles) * currentRotation

// Ring-0 wrapping
float RingKernel(float value, float modulus)

// Complex operations
Vector2 Rotate(Vector2 point, float angle)
Vector2 Conjugate(Vector2 point)  // f(i) = -i
```

---

## 🎨 Color Palettes (Solarpunk Aesthetic)

All projects use these carefully chosen palettes:

### Solarpunk Green
```
Deep Forest:  #0A1E14  (10, 30, 20)
Dark Green:   #285032  (40, 80, 50)
Medium Green: #50A064  (80, 160, 100)
Light Green:  #78C88C  (120, 200, 140)
Bright Green: #B4FFC8  (180, 255, 200)
```

### Space Nebula
```
Deep Space:    #0A0519  (10, 5, 25)
Dark Purple:   #1E143C  (30, 20, 60)
Medium Purple: #3C2864  (60, 40, 100)
Light Purple:  #645096  (100, 80, 150)
Bright Purple: #9678C8  (150, 120, 200)
```

### Solar Energy
```
Dark Gold:   #281E00  (40, 30, 0)
Bronze:      #645014  (100, 80, 20)
Gold:        #C8A03C  (200, 160, 60)
Light Gold:  #FFDC78  (255, 220, 120)
Bright Gold: #FFFFC8  (255, 255, 200)
```

---

## 🔧 Design Notes and Next Steps

### Current Features
- ✅ Playable Pygame demo with full game loop
- ✅ Browser-based web version
- ✅ Procedural art generation
- ✅ Unity 3D controller
- ✅ Mathematical physics (no ML/AI)
- ✅ Solarpunk aesthetic
- ✅ Ring-0 toroidal wrapping

### Potential Expansions

**Expand Pygame:**
- Multiple levels with increasing difficulty
- Enemy AI using pure algorithms (state machines, behavior trees)
- Weapon system with projectile physics
- Power-ups and ship upgrades
- Sound effects and music
- Persistent high scores

**Upgrade Web:**
- Convert to Phaser.js or PixiJS framework
- Mobile touch controls
- Multiplayer using WebSockets
- Level editor
- Local storage for saves

**Go 3D (Unity):**
- Full Unity scene with asteroids and stations
- Procedural terrain using noise functions
- Shader effects for solar sails
- Orbital mechanics simulation
- Resource gathering gameplay

**Try Godot:**
- Port to Godot Engine (open-source!)
- GDScript implementation
- 2D or 3D versions
- Built-in physics engine
- Easy deployment to multiple platforms

**Advanced Mathematics:**
- Implement n-body gravity simulation
- Lagrange points and orbital mechanics
- Fluid dynamics for nebula effects
- Signed distance fields for procedural shapes
- Spectral synthesis for audio generation

---

## 📐 Mathematical Reference

### Complex Numbers
```
Rotation:    z' = z · e^(iθ) = (x·cos(θ) - y·sin(θ)) + i(x·sin(θ) + y·cos(θ))
Conjugate:   f(z) = z* = x - iy  (reflects imaginary component)
Magnitude:   |z| = √(x² + y²)
```

### Ring Theory
```
Ring-0 (Kernel):  f(x) = x mod m
Toroidal Space:   (x, y) → (x mod W, y mod H)
Equivalence Class: Elements mapping to same remainder
```

### Harmonic Oscillators
```
Simple:      f(t) = A·sin(ωt + φ)
Damped:      f(t) = A·e^(-λt)·sin(ωt + φ)
Multi-freq:  f(t) = Σᵢ Aᵢ·sin(ωᵢt + φᵢ)
```

### Fractals
```
Mandelbrot:  z_{n+1} = z_n² + c, |z| < 2
Julia Set:   Similar to Mandelbrot with fixed c
Perlin:      Multi-octave gradient noise
```

### Cellular Automata
```
Game of Life:
- Live cell with 2-3 neighbors → survives
- Dead cell with 3 neighbors → becomes alive
- All other cells → die/stay dead
```

---

## 🚀 Quick Start Guide

### Complete Setup (All Projects)

```bash
# Clone repository
git clone <repo-url>
cd solarpunk-space-starter-kit

# Install Python dependencies
pip install pygame pillow

# Run Pygame demo
python pygame_solarpunk/main.py

# Generate textures
python binary_art/binary_art.py

# Open web demo
open web_solarpunk/index.html

# For Unity: Import SpaceshipController.cs into your Unity project
```

### Minimum Requirements

**For Pygame/Binary Art:**
- Python 3.7+
- pygame library
- pillow library

**For Web Version:**
- Any modern browser (Chrome, Firefox, Safari, Edge)
- No dependencies!

**For Unity:**
- Unity 2020.3 LTS or newer
- Any platform (Windows, Mac, Linux)

---

## 🧮 Why No Neural Networks?

This project demonstrates that rich, engaging games and procedural content can be created using **pure mathematics** and **classical algorithms**:

| Traditional ML | Our Approach |
|----------------|--------------|
| Neural networks | Complex numbers, quaternions |
| Training data | Mathematical functions |
| Backpropagation | Direct computation |
| GPUs for inference | CPU-friendly algorithms |
| Black box | Fully interpretable |
| Probabilistic | Deterministic (or controlled random) |

**Benefits:**
- ⚡ Faster execution (no model inference)
- 🎯 Predictable behavior
- 🔍 Easy to debug and understand
- 📦 Smaller file sizes
- 🎓 Educational value
- 🎨 Artistic control

**When to Use Neural Networks:**
- Adaptive difficulty based on player skill
- Natural language interfaces
- Image/audio generation from examples
- Learning player preferences
- Procedural content that mimics training data

---

## 🌌 Solarpunk Aesthetic Guidelines

### Visual Style
- **Colors**: Greens, golds, purples (nature + technology)
- **Themes**: Sustainable futures, harmony with nature
- **Assets**: Solar panels, gardens, eco-friendly tech
- **Contrast**: Organic shapes + geometric precision

### Narrative Themes
- Cooperation over competition
- Renewable energy and sustainability
- Post-scarcity economics
- Community and trade networks
- Respect for ecosystems

### Game Mechanics Ideas
- Collect solar energy instead of fuel
- Trade resources between habitats
- Maintain ecosystem balance
- Build sustainable infrastructure
- Non-violent conflict resolution

---

## 📚 Learning Resources

### Mathematics
- Complex Analysis (for rotations)
- Abstract Algebra (for ring theory)
- Differential Equations (for physics)
- Fractal Geometry
- Numerical Methods

### Game Development
- Game Physics (vector math, collision)
- Procedural Generation
- Game Loop Architecture
- State Machines
- Entity-Component Systems

### Tools
- Python + Pygame (2D games)
- JavaScript + Canvas (web games)
- Unity + C# (3D games)
- Godot (open-source alternative)

---

## 🎮 What's Next?

Tell me which direction you'd like to go:

1. **Expand Pygame**: Add levels, enemies, weapons, or upgrades
2. **Upgrade Web**: Convert to Phaser.js or add multiplayer
3. **Go 3D**: Build complete Unity scene with procedural world
4. **Try Godot**: Port to Godot Engine
5. **Advanced Math**: Implement orbital mechanics, n-body simulation
6. **Sound Design**: Add procedural audio generation
7. **Networking**: Implement multiplayer functionality
8. **Mobile**: Create touch-friendly mobile version

I will produce the next set of files and a development plan based on your choice!

---

## 📝 License

MIT License - Feel free to use, modify, and distribute these prototypes.

## 🙏 Credits

**Mathematical Foundation**: Pure mathematics, no ML
**Aesthetic**: Solarpunk movement
**Philosophy**: f(i) = -i | Ring-0 Control | Saga Gonzo Edition

---

**"Building futures through mathematics, not matrices."**

🌿⚡🚀
