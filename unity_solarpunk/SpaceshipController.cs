using UnityEngine;

/// <summary>
/// Solarpunk Spaceship Controller for Unity
/// Attach this to a GameObject with a Rigidbody component
/// Works in both 2D (Rigidbody2D) and 3D (Rigidbody) modes
/// </summary>
public class SpaceshipController : MonoBehaviour
{
    [Header("Movement Settings")]
    [Tooltip("Speed of spaceship movement")]
    public float moveSpeed = 10f;

    [Tooltip("Rotation speed for turning")]
    public float rotationSpeed = 5f;

    [Tooltip("Use 2D physics (Rigidbody2D) or 3D physics (Rigidbody)")]
    public bool use2D = true;

    [Header("Solar Boost")]
    [Tooltip("Boost speed multiplier")]
    public float boostMultiplier = 2f;

    [Tooltip("Current solar energy (0-100)")]
    [Range(0, 100)]
    public float solarEnergy = 100f;

    [Tooltip("Energy drain rate per second when boosting")]
    public float boostDrainRate = 20f;

    [Tooltip("Energy recharge rate per second")]
    public float rechargeRate = 10f;

    private Rigidbody rb3D;
    private Rigidbody2D rb2D;
    private bool isBoosting = false;

    void Start()
    {
        // Get the appropriate Rigidbody component
        if (use2D)
        {
            rb2D = GetComponent<Rigidbody2D>();
            if (rb2D == null)
            {
                Debug.LogError("Rigidbody2D component required when use2D is true!");
            }
        }
        else
        {
            rb3D = GetComponent<Rigidbody>();
            if (rb3D == null)
            {
                Debug.LogError("Rigidbody component required when use2D is false!");
            }
        }
    }

    void Update()
    {
        HandleInput();
        ManageSolarEnergy();
    }

    void FixedUpdate()
    {
        HandleMovement();
    }

    void HandleInput()
    {
        // Check for boost input
        if (Input.GetKey(KeyCode.LeftShift) || Input.GetKey(KeyCode.Space))
        {
            if (solarEnergy > 0)
            {
                isBoosting = true;
            }
        }
        else
        {
            isBoosting = false;
        }
    }

    void HandleMovement()
    {
        // Get input
        float horizontal = Input.GetAxis("Horizontal"); // A/D or Left/Right arrows
        float vertical = Input.GetAxis("Vertical");     // W/S or Up/Down arrows

        // Calculate speed with boost
        float currentSpeed = isBoosting ? moveSpeed * boostMultiplier : moveSpeed;

        if (use2D)
        {
            HandleMovement2D(horizontal, vertical, currentSpeed);
        }
        else
        {
            HandleMovement3D(horizontal, vertical, currentSpeed);
        }
    }

    void HandleMovement2D(float horizontal, float vertical, float speed)
    {
        // 2D top-down movement
        Vector2 movement = new Vector2(horizontal, vertical).normalized;
        rb2D.velocity = movement * speed;

        // Rotate ship to face movement direction
        if (movement.magnitude > 0.1f)
        {
            float angle = Mathf.Atan2(movement.y, movement.x) * Mathf.Rad2Deg - 90f;
            Quaternion targetRotation = Quaternion.Euler(0, 0, angle);
            transform.rotation = Quaternion.Slerp(transform.rotation, targetRotation, rotationSpeed * Time.fixedDeltaTime);
        }
    }

    void HandleMovement3D(float horizontal, float vertical, float speed)
    {
        // 3D space flight controls
        Vector3 movement = new Vector3(horizontal, 0, vertical).normalized;
        rb3D.velocity = transform.TransformDirection(movement) * speed;

        // Rotate ship with horizontal input
        if (Mathf.Abs(horizontal) > 0.1f)
        {
            transform.Rotate(Vector3.up, horizontal * rotationSpeed * Time.fixedDeltaTime);
        }
    }

    void ManageSolarEnergy()
    {
        if (isBoosting)
        {
            // Drain energy while boosting
            solarEnergy -= boostDrainRate * Time.deltaTime;
            solarEnergy = Mathf.Max(0, solarEnergy);

            // Visual feedback (you can extend this)
            if (solarEnergy <= 0)
            {
                isBoosting = false;
            }
        }
        else
        {
            // Recharge energy when not boosting
            solarEnergy += rechargeRate * Time.deltaTime;
            solarEnergy = Mathf.Min(100, solarEnergy);
        }
    }

    // Public method to add solar energy (called when collecting solar orbs)
    public void CollectSolarEnergy(float amount)
    {
        solarEnergy += amount;
        solarEnergy = Mathf.Min(100, solarEnergy);
    }

    // Check if ship is currently boosting (for visual effects)
    public bool IsBoosting()
    {
        return isBoosting;
    }

    // Get current energy percentage (for UI)
    public float GetEnergyPercentage()
    {
        return solarEnergy;
    }

    // Optional: Draw debug info
    void OnGUI()
    {
        GUIStyle style = new GUIStyle();
        style.fontSize = 20;
        style.normal.textColor = Color.green;

        GUI.Label(new Rect(10, 10, 300, 30), $"Solar Energy: {solarEnergy:F0}%", style);

        if (isBoosting)
        {
            style.normal.textColor = Color.yellow;
            GUI.Label(new Rect(10, 40, 300, 30), "BOOSTING!", style);
        }
    }
}
