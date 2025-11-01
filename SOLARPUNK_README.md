# ☀️ Solarpunk Space Starter Kit

A collection of prototypes and utilities for building games and apps with a **solarpunk + space-travel aesthetic**. Features lush green technology, solar-powered ships, and an optimistic vision of humanity's future among the stars.

## 🎮 What's Included

This starter kit contains **4 complete prototypes** you can use as a foundation for your own solarpunk space game:

### 1. 🐍 Python / Pygame Prototype
**A fully playable 2D space game**

- **Gameplay**: Fly your solar-powered ship, collect energy orbs, avoid space debris
- **Features**:
  - Smooth acceleration-based movement
  - Parallax scrolling star field
  - Particle effects for collections and collisions
  - Score tracking and game-over/restart loop
  - Solarpunk color palette (mint, lavender, cyan, dusty orange)

- **Code Structure**:
  - `main.py` - Game loop and state management
  - `game_objects.py` - All game entities (Player, Orbs, Debris, etc.)

**How to run:**
```bash
cd pygame_solarpunk
pip install pygame
python main.py
```

**Controls**: WASD or Arrow Keys to move, R to restart (after game over), ESC to quit

---

### 2. 🌐 Web Canvas Prototype
**Browser-based mini-game** (no dependencies!)

- **Lightweight and shareable** - works in any modern browser
- **Same gameplay** as Pygame version but optimized for web
- **Responsive** - works on desktop and mobile
- **Features**:
  - HTML5 Canvas rendering
  - Smooth 60 FPS gameplay
  - Beautiful gradient UI
  - Click-to-restart button

**How to run:**
```bash
cd web_solarpunk
# Option 1: Open directly
open index.html

# Option 2: Serve with Python
python -m http.server 8000
# Then visit http://localhost:8000
```

**Controls**: WASD or Arrow Keys (desktop), touch controls coming soon!

---

### 3. 🎨 Binary Art Generator
**Procedural texture and sprite generator**

Creates solarpunk-themed game assets using binary patterns and algorithmic generation.

- **Backgrounds**: Star fields, nebulae, tilemaps
- **Sprites**: Solar orbs, ships, debris
- **Customizable**: Uses defined color palettes
- **Format**: PNG with transparency support

**How to run:**
```bash
cd binary_art
pip install pillow
python binary_art.py
```

**Output**: Creates `output/` folder with:
- `star_field.png` - Parallax star background
- `nebula.png` - Colorful nebula patterns
- `tilemap.png` - Procedural tile grid
- `solar_orb.png` - Collectible sprite
- `ship.png` - Player ship sprite
- `debris_*.png` - Obstacle sprites

---

### 4. 🎯 Unity C# Controller
**Drop-in ship controller for Unity**

A polished, production-ready spaceship controller that works with both 2D and 3D Unity projects.

- **Features**:
  - Acceleration-based movement with drag
  - Speed limiting
  - Optional rotation toward movement direction
  - Public API for boosts, knockback, etc.
  - Works with Rigidbody or Rigidbody2D
  - Extensive tooltips and comments

**How to use:**
1. Create a Unity project (2D or 3D)
2. Copy `SolarpunkShipController.cs` to `Assets/Scripts/`
3. Add script to your ship GameObject
4. Add Rigidbody (or Rigidbody2D for 2D)
5. Configure settings in Inspector
6. Press Play!

See `unity_controller/README.md` for full documentation and examples.

---

## 🎨 Solarpunk Design Philosophy

This kit uses a carefully chosen color palette that embodies solarpunk aesthetics:

- 🌿 **Mint Green** (`#64C8B4`): Living technology, growth, harmony
- 💜 **Lavender** (`#B4A0FF`): Energy fields, mystical tech
- 💎 **Cyan** (`#64C8DC`): Clean energy, water, atmosphere
- 🧡 **Dusty Orange** (`#DCA06E`): Natural materials, warmth
- 🌙 **Deep Purple-Black** (`#19141F`): Space, mystery, depth

### Visual Themes
- **Organic meets technological**: Ships with solar sails and living gardens
- **Hopeful future**: Bright colors against dark space
- **Sustainability in space**: Solar energy collection, eco-habitats
- **Community-focused**: Trade routes between cooperative space stations

---

## 🚀 Next Steps & Expansion Ideas

### Gameplay Mechanics
- [ ] **Resource Management**: Collect solar energy to power ship systems
- [ ] **Ship Upgrades**: Bigger solar arrays, better shields, faster engines
- [ ] **Trading System**: Visit space habitats to trade resources
- [ ] **Weapon Systems**: Non-lethal capture nets, EMP to disable debris
- [ ] **Crew Management**: Recruit specialists with unique abilities
- [ ] **Base Building**: Establish your own sustainable space habitat

### Visual Enhancements
- [ ] Replace procedural art with custom solarpunk sprites
- [ ] Add animated solar panels on ships
- [ ] Floating garden asteroids with vegetation
- [ ] Eco-dome stations with visible plant life
- [ ] Aurora effects around energy-rich zones
- [ ] Particle trails showing solar wind

### Audio
- [ ] Ambient synth soundscapes
- [ ] Nature sounds mixed with tech (wind chimes + computer hums)
- [ ] Satisfying collection sounds (soft chimes)
- [ ] Gentle thruster sounds
- [ ] Calm, exploratory music

### Technical Improvements
- [ ] Save/load system for progression
- [ ] Procedural level generation
- [ ] Mobile touch controls for web version
- [ ] Multiplayer cooperative collection
- [ ] Leaderboards and achievements
- [ ] Accessibility options (colorblind modes, difficulty settings)

---

## 📁 Project Structure

```
.
├── pygame_solarpunk/          # Python/Pygame game
│   ├── main.py                # Game loop
│   └── game_objects.py        # Entity classes
│
├── web_solarpunk/             # Web browser game
│   ├── index.html             # Game page
│   └── game.js                # Canvas game logic
│
├── binary_art/                # Procedural art generator
│   ├── binary_art.py          # Generator script
│   └── output/                # Generated assets (created on run)
│
├── unity_controller/          # Unity C# controller
│   ├── SolarpunkShipController.cs
│   └── README.md              # Unity setup guide
│
├── data_structures/           # CS fundamentals library
├── algorithms/                # Algorithm implementations
├── math_utils/                # Mathematical utilities
├── tests/                     # Unit tests
├── examples/                  # Usage examples
│
├── README.md                  # Main project documentation
└── SOLARPUNK_README.md        # This file (game starter kit docs)
```

---

## 🛠️ Technologies Used

- **Python 3.7+** with Pygame for the desktop game
- **HTML5 Canvas** + **JavaScript** for the web version
- **PIL/Pillow** for procedural art generation
- **Unity C#** for the 3D/2D game engine controller

---

## 🤝 Contributing & Customization

This is a **starter kit** - you're encouraged to:

- ✅ Use in personal or commercial projects
- ✅ Modify and extend the code
- ✅ Share your creations with the community
- ✅ Contribute improvements back

### Ideas for Your Own Game

**Arcade Style**: Fast-paced collection with increasing difficulty
**Exploration**: Open world with multiple habitats to discover
**Story-Driven**: Narrative about building a sustainable space civilization
**Educational**: Teach about solar energy and sustainability
**Multiplayer**: Cooperative energy collection and base building

---

## 📚 Additional Resources

### Solarpunk Inspiration
- [Solarpunk Manifesto](https://www.re-des.org/a-solarpunk-manifesto/)
- /r/solarpunk community
- "Solarpunk: Post-Industrial Design and Aesthetics" articles

### Game Development
- [Pygame Documentation](https://www.pygame.org/docs/)
- [HTML5 Canvas Tutorial](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API/Tutorial)
- [Unity Learn](https://learn.unity.com/)

### Color & Art
- [Solarpunk Color Palettes](https://lospec.com/palette-list/tag/solarpunk)
- Procedural generation techniques
- Pixel art tutorials for space games

---

## 📝 License

This starter kit is provided as-is for educational and creative purposes. Feel free to use, modify, and build upon it.

---

## 🌟 Let's Build a Better Future Among the Stars!

Made with 💚 for the solarpunk and game dev communities.

**Happy creating! May your solar sails always catch the stellar wind.** ☀️🚀🌿
