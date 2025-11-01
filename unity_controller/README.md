# Unity Solarpunk Ship Controller

A flexible ship controller script for Unity that works with both 2D and 3D projects.

## Setup Instructions

### 1. Add to Your Project

1. Create a Unity project (2D or 3D)
2. Copy `SolarpunkShipController.cs` to your `Assets/Scripts/` folder
3. Create a GameObject for your ship (or use an existing one)

### 2. Add Required Components

Your ship GameObject needs:
- **SolarpunkShipController** script (the one you just added)
- **Rigidbody2D** (for 2D) or **Rigidbody** (for 3D)
- **Sprite Renderer** or **Mesh Renderer** for visuals
- **Collider2D** or **Collider** (optional, for collision detection)

### 3. Configure the Script

Select your ship GameObject and configure the inspector:

#### Movement Settings
- **Max Speed**: Maximum velocity (default: 10)
- **Acceleration**: How fast it speeds up (default: 5)
- **Drag**: How quickly it slows down when not moving (default: 0.95)

#### Rotation Settings
- **Rotate Towards Movement**: Should ship face movement direction?
- **Rotation Speed**: How fast it rotates (default: 5)

#### 2D/3D Mode
- **Is 2D**: Check for 2D games, uncheck for 3D

### 4. Set Up Input

Unity's default Input settings should work (WASD/Arrow keys).

To verify:
1. Go to `Edit > Project Settings > Input Manager`
2. Ensure "Horizontal" and "Vertical" axes exist

### 5. Rigidbody Settings

**For 2D:**
- Set Rigidbody2D Gravity Scale to 0
- Set Constraints: Freeze Rotation Z (if you want the script to handle rotation)

**For 3D:**
- Uncheck "Use Gravity" (unless you want falling)
- Set Constraints: Freeze Rotation on axes you don't want to rotate

## Usage Examples

### Basic Setup (2D)
```csharp
// The controller works automatically with arrow keys / WASD
// No additional code needed!
```

### Adding Boost Power-Up
```csharp
public class BoostPickup : MonoBehaviour
{
    public float boostForce = 15f;

    void OnTriggerEnter2D(Collider2D other)
    {
        SolarpunkShipController ship = other.GetComponent<SolarpunkShipController>();
        if (ship != null)
        {
            // Apply forward boost
            Vector3 boostDirection = other.transform.up;
            ship.AddForce(boostDirection * boostForce);
            Destroy(gameObject);
        }
    }
}
```

### Reading Ship Speed (for UI)
```csharp
public class Speedometer : MonoBehaviour
{
    public SolarpunkShipController ship;
    public Text speedText;

    void Update()
    {
        float speed = ship.GetSpeed();
        speedText.text = $"Speed: {speed:F1}";
    }
}
```

### Explosion Knockback
```csharp
public class Explosion : MonoBehaviour
{
    public float explosionForce = 20f;
    public float explosionRadius = 5f;

    void Explode()
    {
        Collider[] hitColliders = Physics.OverlapSphere(transform.position, explosionRadius);

        foreach (Collider hit in hitColliders)
        {
            SolarpunkShipController ship = hit.GetComponent<SolarpunkShipController>();
            if (ship != null)
            {
                Vector3 direction = (hit.transform.position - transform.position).normalized;
                ship.AddForce(direction * explosionForce);
            }
        }
    }
}
```

## Advanced Customization

### Change Movement Plane (3D)

By default, 3D mode uses X-Z plane (top-down). To change:

```csharp
// In HandleInput(), replace:
inputDirection = new Vector3(horizontal, 0f, vertical);

// With (for side-scroller):
inputDirection = new Vector3(horizontal, vertical, 0f);
```

### Add Speed Boost While Holding Shift

```csharp
// Add to HandleInput():
float speedMultiplier = Input.GetKey(KeyCode.LeftShift) ? 2f : 1f;
velocity += inputDirection * acceleration * speedMultiplier * Time.deltaTime;
```

### Limit to Screen Bounds (2D)

```csharp
// Add to FixedUpdate():
Vector3 pos = transform.position;
pos.x = Mathf.Clamp(pos.x, -8f, 8f);
pos.y = Mathf.Clamp(pos.y, -5f, 5f);
transform.position = pos;
```

## Troubleshooting

**Ship doesn't move:**
- Check Rigidbody component is attached
- Verify Input axes in Project Settings
- Make sure Is2D setting matches your game type

**Ship rotates unexpectedly:**
- Freeze Rigidbody rotation constraints
- Disable "Rotate Towards Movement" if you want manual rotation

**Ship moves too fast/slow:**
- Adjust Max Speed and Acceleration values
- Increase drag for more "floaty" movement
- Decrease drag for more precise control

## Credits

Part of the Solarpunk Space Starter Kit.
