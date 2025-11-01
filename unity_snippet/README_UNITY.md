# Unity Spaceship Controller Setup

## How to Use

1. **Create a Unity Project** (2021.3 LTS or newer recommended)

2. **Create a Spaceship GameObject**:
   - Right-click in Hierarchy → 3D Object → Cube (or use a custom 3D model)
   - Rename it to "Spaceship"

3. **Add the Script**:
   - Copy `SpaceshipController.cs` to your Unity project's `Assets/Scripts/` folder
   - Drag the script onto your Spaceship GameObject

4. **Configure the Rigidbody** (automatically added by script):
   - The script will add a Rigidbody component automatically
   - Gravity is disabled for space physics

5. **Optional: Add Visual Effects**:

   **Trail Renderer**:
   - Add Component → Effects → Trail Renderer
   - Drag the Trail Renderer component to the "Trail Renderer" slot in the SpaceshipController
   - Adjust width, time, and materials as desired

   **Engine Particles**:
   - Create a child GameObject under Spaceship
   - Add Component → Effects → Particle System
   - Position it at the back of the ship
   - Drag the Particle System to the "Engine Particles" slot in the SpaceshipController

6. **Controls**:
   - **Arrow Keys / WASD**: Rotate ship
   - **Space**: Forward thrust
   - **Q/E**: Strafe left/right

## Customization

Adjust these values in the Inspector:

- **Thrust Force**: How fast the ship accelerates forward
- **Rotation Speed**: How quickly the ship rotates
- **Strafe Speed**: Side-to-side movement speed
- **Max Velocity**: Top speed limit
- **Drag**: Space friction (lower = more momentum)

## Advanced Features

### Applying External Forces

```csharp
// From another script, push the spaceship
SpaceshipController ship = spaceshipObject.GetComponent<SpaceshipController>();
ship.ApplyImpulse(new Vector3(10, 0, 0)); // Push right
```

### Getting Ship Speed

```csharp
float currentSpeed = ship.GetSpeed();
Debug.Log($"Current speed: {currentSpeed}");
```

### Resetting Velocity

```csharp
ship.SetVelocity(Vector3.zero); // Stop the ship
```

## 2D Mode

To use in a 2D game:
1. Remove the pitch rotation code in `HandleRotation()`
2. Lock the Rigidbody Z-axis rotation constraint
3. Use Rigidbody2D instead if you prefer

## Tips

- The script uses **quaternion mathematics** (similar to complex numbers) for smooth rotation
- Physics are calculated in `FixedUpdate()` for consistent behavior
- All movement is force-based for realistic space physics
- No neural networks or AI - pure algorithmic control!

Enjoy your solarpunk space adventures! 🌱🚀
