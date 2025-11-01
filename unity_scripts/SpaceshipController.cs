using UnityEngine;
using System.Collections.Generic;

/// <summary>
/// Solarpunk Spaceship Controller - Unity Edition
///
/// Mathematical Foundation (NO NEURAL NETWORKS):
/// - Quaternion rotations: Unit quaternions for 3D rotation
/// - Vector field operations: Force accumulation and integration
/// - Damping functions: Exponential decay for smooth movement
/// - Ring-0 wrapping: Toroidal space boundaries
/// - f(i) = -i transformations: Complex conjugate for mirroring
///
/// Usage:
/// 1. Attach this script to a GameObject with a Rigidbody component
/// 2. Adjust parameters in the Inspector
/// 3. Use WASD/Arrow keys for movement, Space for boost
/// </summary>
[RequireComponent(typeof(Rigidbody))]
public class SpaceshipController : MonoBehaviour
{
    [Header("Movement Settings")]
    [Tooltip("Forward thrust force")]
    public float thrustForce = 10f;

    [Tooltip("Rotation speed in degrees per second")]
    public float rotationSpeed = 100f;

    [Tooltip("Strafe (sideways) force")]
    public float strafeForce = 5f;

    [Tooltip("Boost multiplier when holding boost key")]
    public float boostMultiplier = 2f;

    [Header("Physics Settings")]
    [Tooltip("Linear drag coefficient (air resistance)")]
    public float linearDrag = 1f;

    [Tooltip("Angular drag coefficient (rotation resistance)")]
    public float angularDrag = 2f;

    [Tooltip("Maximum velocity magnitude")]
    public float maxVelocity = 50f;

    [Header("Space Boundaries (Ring-0 Wrapping)")]
    [Tooltip("Enable toroidal space wrapping")]
    public bool enableWrapping = true;

    [Tooltip("X-axis boundary")]
    public float boundaryX = 100f;

    [Tooltip("Y-axis boundary")]
    public float boundaryY = 100f;

    [Tooltip("Z-axis boundary")]
    public float boundaryZ = 100f;

    [Header("Visual Effects")]
    [Tooltip("Trail renderer for ship trail")]
    public TrailRenderer shipTrail;

    [Tooltip("Particle system for engine exhaust")]
    public ParticleSystem engineExhaust;

    [Header("Input Settings")]
    [Tooltip("Use legacy input system (if false, uses new Input System)")]
    public bool useLegacyInput = true;

    // Private variables
    private Rigidbody rb;
    private Vector3 currentRotation;
    private bool isBoosting = false;

    // Complex number operations for transformations
    private struct ComplexTransform
    {
        public static Vector2 Rotate(Vector2 point, float angle)
        {
            // z * e^(iθ) rotation using complex multiplication
            float cos = Mathf.Cos(angle);
            float sin = Mathf.Sin(angle);
            return new Vector2(
                point.x * cos - point.y * sin,
                point.x * sin + point.y * cos
            );
        }

        public static Vector2 Conjugate(Vector2 point)
        {
            // f(i) = -i transformation (complex conjugate)
            return new Vector2(point.x, -point.y);
        }

        public static float RingKernel(float value, float modulus)
        {
            // Ring-0 operation: map value to equivalence class
            float result = value % modulus;
            if (result > modulus / 2) result -= modulus;
            else if (result < -modulus / 2) result += modulus;
            return result;
        }
    }

    void Start()
    {
        // Get Rigidbody component
        rb = GetComponent<Rigidbody>();

        // Set physics properties
        rb.drag = linearDrag;
        rb.angularDrag = angularDrag;
        rb.useGravity = false; // Space has no gravity!

        // Initialize trail
        if (shipTrail != null)
        {
            shipTrail.emitting = true;
        }

        Debug.Log("🚀 Solarpunk Spaceship Controller initialized");
        Debug.Log("📐 Mathematical engine: Quaternions • Vector Fields • Ring-0 Wrapping");
    }

    void Update()
    {
        // Handle input (update is better for input)
        HandleInput();

        // Update visual effects
        UpdateVisualEffects();
    }

    void FixedUpdate()
    {
        // Physics updates happen in FixedUpdate
        ApplyMovement();
        ApplyRotation();
        ClampVelocity();
        ApplyBoundaryWrapping();
    }

    void HandleInput()
    {
        if (!useLegacyInput)
        {
            // New Input System would go here
            return;
        }

        // Legacy Input System
        float thrust = Input.GetAxis("Vertical");      // W/S or Up/Down
        float strafe = Input.GetAxis("Horizontal");    // A/D or Left/Right
        float yaw = 0f;

        // Rotation (Q/E for yaw)
        if (Input.GetKey(KeyCode.Q)) yaw = -1f;
        if (Input.GetKey(KeyCode.E)) yaw = 1f;

        // Boost
        isBoosting = Input.GetKey(KeyCode.Space);

        // Store inputs for FixedUpdate
        currentRotation = new Vector3(0, yaw, 0);

        // Apply forces (will be used in FixedUpdate)
        Vector3 thrustDirection = transform.forward * thrust;
        Vector3 strafeDirection = transform.right * strafe;

        Vector3 totalForce = (thrustDirection * thrustForce + strafeDirection * strafeForce);

        if (isBoosting)
        {
            totalForce *= boostMultiplier;
        }

        // Store for fixed update
        rb.AddForce(totalForce, ForceMode.Force);
    }

    void ApplyMovement()
    {
        // Movement is handled in HandleInput via AddForce
        // This method can be extended for more complex movement patterns
    }

    void ApplyRotation()
    {
        // Apply rotation using quaternions (proper 3D rotation math)
        if (currentRotation.magnitude > 0.01f)
        {
            // Convert euler angles to quaternion rotation
            Quaternion deltaRotation = Quaternion.Euler(
                currentRotation * rotationSpeed * Time.fixedDeltaTime
            );

            // Apply rotation
            rb.MoveRotation(rb.rotation * deltaRotation);
        }
    }

    void ClampVelocity()
    {
        // Limit maximum velocity using vector magnitude
        if (rb.velocity.magnitude > maxVelocity)
        {
            rb.velocity = rb.velocity.normalized * maxVelocity;
        }
    }

    void ApplyBoundaryWrapping()
    {
        // Ring-0 wrapping: Toroidal topology for space boundaries
        if (!enableWrapping) return;

        Vector3 pos = transform.position;
        bool wrapped = false;

        // Apply ring kernel operation to each axis
        float newX = ComplexTransform.RingKernel(pos.x, boundaryX * 2);
        float newY = ComplexTransform.RingKernel(pos.y, boundaryY * 2);
        float newZ = ComplexTransform.RingKernel(pos.z, boundaryZ * 2);

        if (Mathf.Abs(newX - pos.x) > 0.01f ||
            Mathf.Abs(newY - pos.y) > 0.01f ||
            Mathf.Abs(newZ - pos.z) > 0.01f)
        {
            wrapped = true;
        }

        if (wrapped)
        {
            transform.position = new Vector3(newX, newY, newZ);

            // Clear trail when wrapping to avoid visual artifacts
            if (shipTrail != null)
            {
                shipTrail.Clear();
            }
        }
    }

    void UpdateVisualEffects()
    {
        // Update trail color based on boost
        if (shipTrail != null)
        {
            Color baseColor = isBoosting ? new Color(1f, 0.8f, 0.2f) : new Color(0.4f, 1f, 0.6f);
            Gradient gradient = new Gradient();
            gradient.SetKeys(
                new GradientColorKey[] {
                    new GradientColorKey(baseColor, 0.0f),
                    new GradientColorKey(baseColor * 0.5f, 1.0f)
                },
                new GradientAlphaKey[] {
                    new GradientAlphaKey(1.0f, 0.0f),
                    new GradientAlphaKey(0.0f, 1.0f)
                }
            );
            shipTrail.colorGradient = gradient;
        }

        // Update engine exhaust particles
        if (engineExhaust != null)
        {
            var emission = engineExhaust.emission;
            emission.rateOverTime = isBoosting ? 50f : 20f;
        }
    }

    // Public methods for external interaction

    /// <summary>
    /// Apply an impulse force (for collisions, explosions, etc.)
    /// </summary>
    public void ApplyImpulse(Vector3 force)
    {
        rb.AddForce(force, ForceMode.Impulse);
    }

    /// <summary>
    /// Get current velocity magnitude
    /// </summary>
    public float GetSpeed()
    {
        return rb.velocity.magnitude;
    }

    /// <summary>
    /// Get velocity as percentage of max
    /// </summary>
    public float GetSpeedPercent()
    {
        return Mathf.Clamp01(rb.velocity.magnitude / maxVelocity);
    }

    // Debug visualization
    void OnDrawGizmos()
    {
        // Draw boundary box
        Gizmos.color = Color.green;
        Gizmos.DrawWireCube(Vector3.zero, new Vector3(boundaryX * 2, boundaryY * 2, boundaryZ * 2));

        // Draw velocity vector
        if (Application.isPlaying && rb != null)
        {
            Gizmos.color = isBoosting ? Color.yellow : Color.cyan;
            Gizmos.DrawRay(transform.position, rb.velocity);
        }
    }
}

/*
 * USAGE EXAMPLE:
 *
 * 1. Create a new Unity project (3D or 2D)
 *
 * 2. Create a spaceship GameObject:
 *    - Add a 3D model or simple shape (cube, capsule, etc.)
 *    - Add Rigidbody component
 *    - Add this SpaceshipController script
 *
 * 3. Configure in Inspector:
 *    - Set thrustForce (try 10-20)
 *    - Set rotationSpeed (try 100-200)
 *    - Enable/disable wrapping
 *    - Set boundaries
 *
 * 4. Optional: Add visual effects
 *    - Add TrailRenderer component → assign to shipTrail
 *    - Add ParticleSystem → assign to engineExhaust
 *
 * 5. Controls:
 *    - W/S or Up/Down: Forward/Backward
 *    - A/D or Left/Right: Strafe left/right
 *    - Q/E: Rotate (yaw)
 *    - Space: Boost
 *
 * MATHEMATICAL NOTES:
 * - Uses Quaternions for proper 3D rotation (no gimbal lock!)
 * - Ring-0 wrapping creates infinite toroidal space
 * - Vector field integration for realistic physics
 * - No neural networks or ML - pure mathematics!
 *
 * Solarpunk Space - Ring-0 Edition
 * f(i) = -i | Saga Gonzo from the CIA
 */
