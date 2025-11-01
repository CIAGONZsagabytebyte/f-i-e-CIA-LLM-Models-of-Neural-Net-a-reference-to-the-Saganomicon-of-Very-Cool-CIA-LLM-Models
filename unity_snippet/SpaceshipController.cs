using UnityEngine;

/// <summary>
/// Solarpunk Space Starter Kit - Unity Spaceship Controller
/// Attach this to a GameObject with a Rigidbody component
/// Pure algorithmic movement - no neural networks or AI
/// Uses complex number-inspired rotation math
/// </summary>
public class SpaceshipController : MonoBehaviour
{
    [Header("Movement Settings")]
    [Tooltip("Forward thrust power")]
    public float thrustForce = 10f;

    [Tooltip("Rotation speed in degrees per second")]
    public float rotationSpeed = 100f;

    [Tooltip("Strafe (side-to-side) movement speed")]
    public float strafeSpeed = 5f;

    [Tooltip("Maximum velocity magnitude")]
    public float maxVelocity = 20f;

    [Header("Physics")]
    [Tooltip("Drag coefficient for space friction")]
    public float drag = 0.5f;

    [Header("Visual Effects")]
    [Tooltip("Trail renderer for ship trail effect")]
    public TrailRenderer trailRenderer;

    [Tooltip("Particle system for engine thrust")]
    public ParticleSystem engineParticles;

    // Components
    private Rigidbody rb;
    private Vector3 velocity;

    // Input state
    private float horizontalInput;
    private float verticalInput;
    private float strafeInput;
    private bool thrustInput;

    void Start()
    {
        // Get or add Rigidbody
        rb = GetComponent<Rigidbody>();
        if (rb == null)
        {
            rb = gameObject.AddComponent<Rigidbody>();
        }

        // Configure Rigidbody for space physics
        rb.useGravity = false;
        rb.drag = drag;
        rb.angularDrag = 0.5f;

        // Initialize trail if present
        if (trailRenderer != null)
        {
            trailRenderer.startColor = new Color(0.39f, 1f, 0.59f, 1f); // Solarpunk green
            trailRenderer.endColor = new Color(0.39f, 1f, 0.59f, 0f);
        }
    }

    void Update()
    {
        // Get input
        horizontalInput = Input.GetAxis("Horizontal");
        verticalInput = Input.GetAxis("Vertical");

        // Strafe input (Q/E keys)
        strafeInput = 0f;
        if (Input.GetKey(KeyCode.Q))
            strafeInput = -1f;
        if (Input.GetKey(KeyCode.E))
            strafeInput = 1f;

        // Thrust input (Space key)
        thrustInput = Input.GetKey(KeyCode.Space);

        // Control engine particles
        if (engineParticles != null)
        {
            if (thrustInput && !engineParticles.isPlaying)
                engineParticles.Play();
            else if (!thrustInput && engineParticles.isPlaying)
                engineParticles.Stop();
        }
    }

    void FixedUpdate()
    {
        // Rotation (using quaternion math similar to complex number rotations)
        HandleRotation();

        // Movement
        HandleMovement();

        // Velocity limiting
        ClampVelocity();
    }

    void HandleRotation()
    {
        // Yaw (left/right rotation)
        float yawRotation = horizontalInput * rotationSpeed * Time.fixedDeltaTime;

        // Pitch (up/down rotation) - optional, remove if only 2D rotation needed
        float pitchRotation = verticalInput * rotationSpeed * Time.fixedDeltaTime;

        // Apply rotation using quaternions (mathematical representation similar to complex numbers)
        // Quaternions handle 3D rotation elegantly, avoiding gimbal lock
        Quaternion yaw = Quaternion.AngleAxis(yawRotation, Vector3.up);
        Quaternion pitch = Quaternion.AngleAxis(pitchRotation, Vector3.right);

        rb.MoveRotation(rb.rotation * yaw * pitch);
    }

    void HandleMovement()
    {
        // Forward thrust
        if (thrustInput)
        {
            Vector3 thrustDirection = transform.forward;
            rb.AddForce(thrustDirection * thrustForce, ForceMode.Acceleration);
        }

        // Strafe movement (perpendicular to forward direction)
        if (Mathf.Abs(strafeInput) > 0.1f)
        {
            Vector3 strafeDirection = transform.right;
            rb.AddForce(strafeDirection * strafeInput * strafeSpeed, ForceMode.Acceleration);
        }
    }

    void ClampVelocity()
    {
        // Limit maximum velocity
        if (rb.velocity.magnitude > maxVelocity)
        {
            rb.velocity = rb.velocity.normalized * maxVelocity;
        }
    }

    /// <summary>
    /// Apply an external force (e.g., from collision, explosion)
    /// </summary>
    public void ApplyImpulse(Vector3 force)
    {
        rb.AddForce(force, ForceMode.Impulse);
    }

    /// <summary>
    /// Get current velocity magnitude (useful for UI display)
    /// </summary>
    public float GetSpeed()
    {
        return rb.velocity.magnitude;
    }

    /// <summary>
    /// Set velocity directly (useful for respawn, teleport)
    /// </summary>
    public void SetVelocity(Vector3 newVelocity)
    {
        rb.velocity = newVelocity;
    }

    // Visualize thrust direction in editor
    void OnDrawGizmos()
    {
        Gizmos.color = Color.green;
        Gizmos.DrawRay(transform.position, transform.forward * 2f);

        Gizmos.color = Color.blue;
        Gizmos.DrawRay(transform.position, transform.right * 1f);
    }
}
