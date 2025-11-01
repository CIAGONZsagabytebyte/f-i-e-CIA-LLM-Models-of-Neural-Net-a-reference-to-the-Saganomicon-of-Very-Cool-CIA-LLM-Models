"""
Field Examples - Comprehensive examples for I/O, UI, and GA fields

Demonstrates the Saga principle: i(f(Saga)=i) across all field types.
"""

# Example 1: I/O Fields - Data Stream Processing
def example_io_fields():
    """Demonstrate I/O field capabilities"""
    print("=" * 60)
    print("EXAMPLE 1: I/O Fields - Data Stream Processing")
    print("=" * 60)

    from io_fields import StreamProcessor, DataPipeline, QuantumChannel
    from io_fields import FieldReader, FieldWriter, CosmicBuffer

    # Create a stream processor
    processor = StreamProcessor()

    # Create multiple streams
    data_stream = processor.create_stream("cosmic_data")
    signal_stream = processor.create_stream("signal")

    # Emit data into streams
    for i in range(10):
        data_stream.emit({'value': i, 'timestamp': i * 0.1})
        signal_stream.emit({'signal': i ** 2})

    # Apply transformation fields
    data_stream.apply_field(lambda x: {**x, 'transformed': x['value'] * 2})

    print(f"Created streams: {list(processor.streams.keys())}")
    print(f"Data stream size: {len(list(data_stream.flow()))}")

    # Create a data pipeline
    pipeline = DataPipeline("saga_transform")
    pipeline.add_stage("amplify", lambda x: x * 2)
    pipeline.add_stage("normalize", lambda x: x / 100)
    pipeline.add_stage("resonate", lambda x: x * 1.618033988749)  # Golden ratio

    result = pipeline.saga_transform(42.0)
    print(f"Pipeline result: {result}")

    # Quantum channels
    channel = QuantumChannel("cosmic_channel")
    channel.send("Hello from the Saga")
    channel.send("Cosmic message")

    received = channel.receive()
    print(f"Received from quantum channel: {received}")

    # Cosmic buffer (3D addressing)
    buffer = CosmicBuffer("spacetime_buffer")
    buffer.write(time_coord=0, space_coord=0, energy_coord=0, data="Origin")
    buffer.write(time_coord=1, space_coord=5, energy_coord=3, data="Future point")

    print(f"Cosmic buffer dimensions: {buffer.get_dimensions()}")
    print()


# Example 2: UI Fields - Interactive Components
def example_ui_fields():
    """Demonstrate UI field capabilities"""
    print("=" * 60)
    print("EXAMPLE 2: UI Fields - Interactive Components")
    print("=" * 60)

    from ui_fields import TextField, NumberField, SelectField, ColorField
    from ui_fields import FormField, GridField, FlowField
    from ui_fields import create_email_validator

    # Create form fields
    username = TextField("username", "Username", "")
    username.add_validator(lambda v: len(v) >= 3)

    email = TextField("email", "Email", "")
    email_validator = create_email_validator()
    email.add_validator(email_validator)

    age = NumberField("age", "Age", 0, min_value=0, max_value=150)

    color = ColorField("theme_color", "Theme Color", "#64C8B4")
    color.set_solarpunk_color("mint")

    # Create a form
    form = FormField("user_registration", "User Registration")
    form.add_field(username)
    form.add_field(email)
    form.add_field(age)
    form.add_field(color)

    # Set values
    username.set_value("paul_rutherfords")
    email.set_value("paul@saga.cosmos")
    age.set_value(33)

    print(f"Form valid: {form.validate()}")
    print(f"Form values: {form.get_values()}")

    # Create a grid field
    grid = GridField("cosmic_grid", width=10, height=10, default_value=0)
    grid.fill(0)
    grid.set_cell(5, 5, 100)  # Center
    print(f"Grid center value: {grid.get_cell(5, 5)}")

    # Create a flow field with vortex
    flow = FlowField("vortex_field", width=100, height=100)
    flow.create_vortex(center_x=50, center_y=50, strength=2.0)

    # Trace a particle through the flow
    path = flow.trace_particle(start_x=10, start_y=10, steps=50)
    print(f"Particle path length: {len(path)}")
    print()


# Example 3: GA Fields - Genetic Algorithms
def example_ga_fields():
    """Demonstrate GA field capabilities"""
    print("=" * 60)
    print("EXAMPLE 3: GA Fields - Genetic Algorithms")
    print("=" * 60)

    from ga_fields import GeneticAlgorithm, Population, FitnessFunction
    from ga_fields import MutationField, CrossoverField
    from ga_fields import CosmicGenerator, SpaceGenerator

    # Define a fitness function (maximize sum of genes)
    def fitness_func(genome):
        return sum(genome)

    fitness = FitnessFunction(fitness_func, "maximize_sum")

    # Create population
    population = Population(
        size=50,
        genome_length=10,
        fitness_function=fitness,
        gene_initializer=lambda: __import__('random').random()
    )

    # Create genetic algorithm
    ga = GeneticAlgorithm(
        population=population,
        mutation_rate=0.01,
        crossover_rate=0.7,
        elitism_count=5
    )

    # Run evolution
    print("Running genetic algorithm...")
    best = ga.run(generations=20)
    print(f"Best individual: fitness={best.fitness:.4f}")
    print(f"Best genome (first 5 genes): {best.genome[:5]}")

    # Mutation field
    mutation = MutationField("cosmic_mutation", mutation_rate=0.05)
    mutation.set_cosmic_resonance()

    genome = [1.0, 2.0, 3.0, 4.0, 5.0]
    mutated = mutation.apply(genome)
    print(f"Original genome: {genome}")
    print(f"Mutated genome: {mutated}")

    # Procedural generation
    space_gen = SpaceGenerator(seed=42)
    star_system = space_gen.generate_star_system()

    print(f"\nGenerated star system: {star_system['name']}")
    print(f"Star type: {star_system['star']['type']}")
    print(f"Number of planets: {len(star_system['planets'])}")

    for i, planet in enumerate(star_system['planets'][:3]):
        print(f"  Planet {i+1}: {planet['name']} ({planet['type']})")

    # Generate space habitat
    habitat = space_gen.generate_space_habitat()
    print(f"\nGenerated habitat: {habitat['name']}")
    print(f"Type: {habitat['type']}")
    print(f"Population: {habitat['population']:,}")
    print(f"Sustainability: {habitat['ecosystem']['sustainability_rating']:.2f}")
    print()


# Example 4: Game Architecture
def example_game_architecture():
    """Demonstrate game architecture with ECS"""
    print("=" * 60)
    print("EXAMPLE 4: Game Architecture - Entity Component System")
    print("=" * 60)

    from ga_fields import GameStateField, EntityField, SystemField
    from ga_fields import PhysicsSystem, WorldField

    # Create game world
    world = WorldField(width=800, height=600, name="solarpunk_space")

    # Create some entities
    ship = world.create_spatial_entity(x=400, y=300, tags=["player", "ship"])
    ship.add_component('velocity', {'vx': 10, 'vy': 0, 'drag': 0.1})
    ship.add_component('sprite', {'name': 'solarpunk_ship', 'color': '#64C8B4', 'z_order': 10})

    # Create energy orbs
    for i in range(5):
        orb = world.create_spatial_entity(x=100 + i * 100, y=200, tags=["orb", "collectible"])
        orb.add_component('sprite', {'name': 'energy_orb', 'color': '#FFD700', 'z_order': 5})

    # Add physics system
    physics = PhysicsSystem()
    world.game_state.add_system(physics)

    print(f"World created: {world.name}")
    print(f"Total entities: {len(world.game_state.entities)}")

    # Update world
    for frame in range(10):
        world.update(dt=0.016)  # ~60 FPS

    print(f"After 10 frames:")
    ship_transform = ship.get_component('transform')
    print(f"Ship position: ({ship_transform['x']:.2f}, {ship_transform['y']:.2f})")

    # Find entities near player
    nearby = world.find_entities_near(x=400, y=300, radius=200)
    print(f"Entities near player: {len(nearby)}")
    print()


# Example 5: Saga Transformation Chain
def example_saga_transformation():
    """Demonstrate the Saga principle: i(f(Saga)=i)"""
    print("=" * 60)
    print("EXAMPLE 5: Saga Transformation - i(f(Saga)=i)")
    print("=" * 60)

    from io_fields import DataPipeline
    from ui_fields import SagaValidator

    # Create a saga validator
    validator = SagaValidator("type_preservation")
    validator.enable_type_checking()
    validator.enable_structure_checking()

    # Add custom constraint
    validator.add_constraint(
        lambda orig, trans: len(str(orig)) == len(str(trans)),
        "Length must be preserved"
    )

    # Create pipeline with saga validation
    pipeline = DataPipeline("validated_saga")

    def amplify(x):
        if isinstance(x, (int, float)):
            return x * 2
        return x

    def normalize(x):
        if isinstance(x, (int, float)):
            return x / 100
        return x

    pipeline.add_stage("amplify", amplify)
    pipeline.add_stage("normalize", normalize)

    # Test transformation
    original = 50
    transformed = pipeline.saga_transform(original)

    print(f"Original: {original} (type: {type(original).__name__})")
    print(f"Transformed: {transformed} (type: {type(transformed).__name__})")

    # Validate saga property
    is_valid, errors = validator.validate_transformation(original, transformed)
    print(f"Saga property preserved: {is_valid}")
    if errors:
        print(f"Validation errors: {errors}")

    # Test with list
    original_list = [1, 2, 3, 4, 5]
    pipeline_list = DataPipeline("list_saga")
    pipeline_list.add_stage("double", lambda lst: [x * 2 for x in lst])
    pipeline_list.add_stage("sort", lambda lst: sorted(lst, reverse=True))

    transformed_list = pipeline_list.saga_transform(original_list)
    print(f"\nOriginal list: {original_list}")
    print(f"Transformed list: {transformed_list}")

    is_valid, errors = validator.validate_transformation(original_list, transformed_list)
    print(f"List saga property preserved: {is_valid}")
    print()


# Example 6: Cosmic Canvas Visualization
def example_cosmic_canvas():
    """Demonstrate cosmic canvas and particle fields"""
    print("=" * 60)
    print("EXAMPLE 6: Cosmic Canvas & Particle Fields")
    print("=" * 60)

    from ui_fields import CosmicCanvas, ParticleField, VectorField

    # Create cosmic canvas
    canvas = CosmicCanvas(width=800, height=600, name="star_field")

    # Add stars
    for i in range(20):
        import random
        canvas.add_element({
            'id': f'star_{i}',
            'type': 'star',
            'x': random.uniform(0, 800),
            'y': random.uniform(0, 600),
            'brightness': random.random()
        })

    print(f"Canvas: {canvas}")
    print(f"Elements: {len(canvas.elements)}")

    # Create particle field
    particles = ParticleField("cosmic_particles")

    # Add gravity force
    particles.add_force(lambda p: (0, 9.8 * p['mass']))

    # Add boundary constraint
    def boundary(p):
        p['x'] = max(0, min(800, p['x']))
        p['y'] = max(0, min(600, p['y']))

    particles.add_constraint(boundary)

    # Create particles
    for i in range(10):
        import random
        particles.add_particle(
            x=400,
            y=100,
            vx=random.uniform(-50, 50),
            vy=random.uniform(-50, 0),
            mass=1.0,
            color=(100, 200, 255)
        )

    print(f"Particle field: {particles}")

    # Update particles
    for _ in range(60):  # Simulate 1 second at 60fps
        particles.update(dt=0.016)

    print(f"Active particles after 1 second: {len(particles.particles)}")

    # Create vector field
    vectors = VectorField("flow", width=800, height=600, resolution=40)
    vectors.create_vortex(center_x=400, center_y=300, strength=1.0)

    print(f"Vector field: {vectors}")
    print()


def main():
    """Run all examples"""
    print("\n" + "=" * 60)
    print("SAGA FIELD EXAMPLES")
    print("Inspired by the Saganomicon and PAUL RUTHERFORDS")
    print("Demonstrating i(f(Saga)=i) across I/O, UI, and GA fields")
    print("=" * 60 + "\n")

    try:
        example_io_fields()
        example_ui_fields()
        example_ga_fields()
        example_game_architecture()
        example_saga_transformation()
        example_cosmic_canvas()

        print("=" * 60)
        print("ALL EXAMPLES COMPLETED SUCCESSFULLY!")
        print("The Saga continues across the cosmos...")
        print("=" * 60)

    except Exception as e:
        print(f"Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
