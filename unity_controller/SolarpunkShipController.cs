using UnityEngine;

/// <summary>
/// Solarpunk Ship Controller for Unity
///
/// Attach this to your spaceship GameObject.
/// Works with both 2D and 3D Unity projects.
///
/// Requirements:
/// - Rigidbody (2D or 3D) component on the same GameObject
/// - Input System (uses legacy Input for compatibility)
///
/// Features:
/// - Smooth acceleration-based movement
/// - Speed limiting
/// - Optional rotation toward movement direction
/// </summary>
public class SolarpunkShipController : MonoBehaviour
{
    [Header("Movement Settings")]
    [Tooltip("Maximum speed the ship can reach")]
    public float maxSpeed = 10f;

    [Tooltip("How quickly the ship accelerates")]
    public float acceleration = 5f;

    [Tooltip("Drag coefficient (0 = no drag, 1 = stops immediately)")]
    [Range(0f, 1f)]
    public float drag = 0.95f;

    [Header("Rotation Settings")]
    [Tooltip("Should the ship rotate toward movement direction?")]
    public bool rotateTowardsMovement = true;

    [Tooltip("How quickly the ship rotates")]
    public float rotationSpeed = 5f;

    [Header("2D/3D Mode")]
    [Tooltip("Is this a 2D game? (affects which plane movement occurs on)")]
    public bool is2D = true;

    // Private variables
    private Vector3 velocity = Vector3.zero;
    private Rigidbody rb3D;
    private Rigidbody2D rb2D;

    void Start()
    {
        // Get the appropriate Rigidbody component
        if (is2D)
        {
            rb2D = GetComponent<Rigidbody2D>();
            if (rb2D == null)
            {
                Debug.LogError("SolarpunkShipController: Rigidbody2D component required for 2D mode!");
            }
        }
        else
        {
            rb3D = GetComponent<Rigidbody>();
            if (rb3D == null)
            {
                Debug.LogError("SolarpunkShipController: Rigidbody component required for 3D mode!");
            }
        }
    }

    void Update()
    {
        HandleInput();
        HandleRotation();
    }

    void FixedUpdate()
    {
        ApplyMovement();
    }

    /// <summary>
    /// Handle player input and update velocity
    /// </summary>
    void HandleInput()
    {
        // Get input axes
        float horizontal = Input.GetAxis("Horizontal");
        float vertical = Input.GetAxis("Vertical");

        Vector3 inputDirection;

        if (is2D)
        {
            // 2D: movement on X-Y plane
            inputDirection = new Vector3(horizontal, vertical, 0f);
        }
        else
        {
            // 3D: movement on X-Z plane (typical for top-down or flight)
            inputDirection = new Vector3(horizontal, 0f, vertical);
        }

        // Normalize to prevent faster diagonal movement
        if (inputDirection.magnitude > 1f)
        {
            inputDirection.Normalize();
        }

        // Apply acceleration
        velocity += inputDirection * acceleration * Time.deltaTime;

        // Apply drag
        velocity *= drag;

        // Limit speed
        if (velocity.magnitude > maxSpeed)
        {
            velocity = velocity.normalized * maxSpeed;
        }
    }

    /// <summary>
    /// Apply the calculated velocity to the Rigidbody
    /// </summary>
    void ApplyMovement()
    {
        if (is2D && rb2D != null)
        {
            rb2D.velocity = new Vector2(velocity.x, velocity.y);
        }
        else if (!is2D && rb3D != null)
        {
            rb3D.velocity = velocity;
        }
    }

    /// <summary>
    /// Rotate the ship toward its movement direction
    /// </summary>
    void HandleRotation()
    {
        if (!rotateTowardsMovement || velocity.magnitude < 0.1f)
            return;

        if (is2D)
        {
            // 2D rotation
            float angle = Mathf.Atan2(velocity.y, velocity.x) * Mathf.Rad2Deg;
            Quaternion targetRotation = Quaternion.Euler(0f, 0f, angle - 90f); // -90 if your sprite points up
            transform.rotation = Quaternion.Lerp(
                transform.rotation,
                targetRotation,
                rotationSpeed * Time.deltaTime
            );
        }
        else
        {
            // 3D rotation
            Quaternion targetRotation = Quaternion.LookRotation(velocity);
            transform.rotation = Quaternion.Lerp(
                transform.rotation,
                targetRotation,
                rotationSpeed * Time.deltaTime
            );
        }
    }

    /// <summary>
    /// Add an external force (e.g., from explosions or boosts)
    /// </summary>
    /// <param name="force">The force vector to apply</param>
    public void AddForce(Vector3 force)
    {
        velocity += force;
    }

    /// <summary>
    /// Get the current velocity
    /// </summary>
    public Vector3 GetVelocity()
    {
        return velocity;
    }

    /// <summary>
    /// Get the current speed
    /// </summary>
    public float GetSpeed()
    {
        return velocity.magnitude;
    }

    /// <summary>
    /// Reset velocity to zero
    /// </summary>
    public void StopMovement()
    {
        velocity = Vector3.zero;
        if (is2D && rb2D != null)
        {
            rb2D.velocity = Vector2.zero;
        }
        else if (!is2D && rb3D != null)
        {
            rb3D.velocity = Vector3.zero;
        }
    }

    // Optional: Draw gizmos in the editor to visualize velocity
    void OnDrawGizmos()
    {
        if (Application.isPlaying)
        {
            Gizmos.color = Color.cyan;
            Gizmos.DrawLine(transform.position, transform.position + velocity);
        }
    }
}
