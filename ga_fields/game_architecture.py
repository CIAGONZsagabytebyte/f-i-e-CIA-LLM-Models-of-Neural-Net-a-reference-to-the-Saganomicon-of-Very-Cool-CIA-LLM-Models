"""
Game Architecture - Field-based game systems and entity management

Implements Entity-Component-System architecture with saga field properties
for building games and simulations.
"""

import time
import uuid
from typing import Any, Dict, List, Optional, Callable, Set
from collections import defaultdict


class EntityField:
    """An entity in the game world with component-based architecture"""

    def __init__(self, entity_id: Optional[str] = None, tags: Optional[List[str]] = None):
        self.id = entity_id or str(uuid.uuid4())
        self.components = {}
        self.tags = set(tags or [])
        self.active = True
        self.created_at = time.time()
        self.updated_at = time.time()

    def add_component(self, component_name: str, component_data: Dict[str, Any]) -> 'EntityField':
        """Add a component to this entity"""
        self.components[component_name] = component_data
        self.updated_at = time.time()
        return self

    def remove_component(self, component_name: str) -> 'EntityField':
        """Remove a component from this entity"""
        if component_name in self.components:
            del self.components[component_name]
            self.updated_at = time.time()
        return self

    def get_component(self, component_name: str) -> Optional[Dict[str, Any]]:
        """Get a component's data"""
        return self.components.get(component_name)

    def has_component(self, component_name: str) -> bool:
        """Check if entity has a component"""
        return component_name in self.components

    def has_components(self, *component_names: str) -> bool:
        """Check if entity has all specified components"""
        return all(name in self.components for name in component_names)

    def add_tag(self, tag: str) -> 'EntityField':
        """Add a tag to this entity"""
        self.tags.add(tag)
        return self

    def remove_tag(self, tag: str) -> 'EntityField':
        """Remove a tag from this entity"""
        self.tags.discard(tag)
        return self

    def has_tag(self, tag: str) -> bool:
        """Check if entity has a tag"""
        return tag in self.tags

    def destroy(self) -> None:
        """Mark entity as inactive"""
        self.active = False

    def __repr__(self):
        return f"EntityField(id={self.id[:8]}, components={list(self.components.keys())}, active={self.active})"


class SystemField:
    """A system that processes entities with specific components"""

    def __init__(self, name: str, required_components: List[str]):
        self.name = name
        self.required_components = required_components
        self.enabled = True
        self.execution_count = 0
        self.total_time = 0.0

    def process(self, entities: List[EntityField], dt: float) -> None:
        """Process all entities that match required components"""
        if not self.enabled:
            return

        start_time = time.time()

        matching_entities = [
            entity for entity in entities
            if entity.active and entity.has_components(*self.required_components)
        ]

        self.update(matching_entities, dt)

        self.execution_count += 1
        self.total_time += time.time() - start_time

    def update(self, entities: List[EntityField], dt: float) -> None:
        """Override this in subclasses to implement system logic"""
        pass

    def get_average_time(self) -> float:
        """Get average execution time"""
        if self.execution_count == 0:
            return 0.0
        return self.total_time / self.execution_count

    def __repr__(self):
        return f"SystemField(name={self.name}, components={self.required_components}, executions={self.execution_count})"


class GameStateField:
    """Central game state manager using field-based architecture"""

    def __init__(self, name: str = "game_world"):
        self.name = name
        self.entities = {}
        self.systems = []
        self.global_state = {}
        self.time = 0.0
        self.paused = False
        self.update_count = 0

    def create_entity(self, tags: Optional[List[str]] = None) -> EntityField:
        """Create a new entity"""
        entity = EntityField(tags=tags)
        self.entities[entity.id] = entity
        return entity

    def destroy_entity(self, entity_id: str) -> bool:
        """Destroy an entity"""
        if entity_id in self.entities:
            self.entities[entity_id].destroy()
            del self.entities[entity_id]
            return True
        return False

    def get_entity(self, entity_id: str) -> Optional[EntityField]:
        """Get an entity by ID"""
        return self.entities.get(entity_id)

    def find_entities_with_components(self, *component_names: str) -> List[EntityField]:
        """Find all entities with specified components"""
        return [
            entity for entity in self.entities.values()
            if entity.active and entity.has_components(*component_names)
        ]

    def find_entities_with_tag(self, tag: str) -> List[EntityField]:
        """Find all entities with a specific tag"""
        return [
            entity for entity in self.entities.values()
            if entity.active and entity.has_tag(tag)
        ]

    def add_system(self, system: SystemField) -> 'GameStateField':
        """Add a system to the game"""
        self.systems.append(system)
        return self

    def remove_system(self, system_name: str) -> 'GameStateField':
        """Remove a system by name"""
        self.systems = [s for s in self.systems if s.name != system_name]
        return self

    def update(self, dt: float) -> 'GameStateField':
        """Update all systems"""
        if self.paused:
            return self

        self.time += dt
        self.update_count += 1

        # Process all systems
        active_entities = [e for e in self.entities.values() if e.active]
        for system in self.systems:
            system.process(active_entities, dt)

        return self

    def pause(self) -> 'GameStateField':
        """Pause the game"""
        self.paused = True
        return self

    def resume(self) -> 'GameStateField':
        """Resume the game"""
        self.paused = False
        return self

    def set_global(self, key: str, value: Any) -> 'GameStateField':
        """Set a global state variable"""
        self.global_state[key] = value
        return self

    def get_global(self, key: str, default: Any = None) -> Any:
        """Get a global state variable"""
        return self.global_state.get(key, default)

    def clear(self) -> 'GameStateField':
        """Clear all entities and reset state"""
        self.entities.clear()
        self.global_state.clear()
        self.time = 0.0
        self.update_count = 0
        return self

    def get_statistics(self) -> Dict[str, Any]:
        """Get game state statistics"""
        active_count = sum(1 for e in self.entities.values() if e.active)

        return {
            'total_entities': len(self.entities),
            'active_entities': active_count,
            'systems': len(self.systems),
            'time': self.time,
            'updates': self.update_count,
            'paused': self.paused
        }

    def __repr__(self):
        return f"GameStateField(name={self.name}, entities={len(self.entities)}, systems={len(self.systems)})"


class WorldField:
    """A complete game world with spatial partitioning and physics"""

    def __init__(self, width: float, height: float, name: str = "world"):
        self.name = name
        self.width = width
        self.height = height
        self.game_state = GameStateField(name)

        # Spatial partitioning (simple grid)
        self.grid_size = 50.0
        self.spatial_grid = defaultdict(list)

    def create_spatial_entity(self, x: float, y: float, tags: Optional[List[str]] = None) -> EntityField:
        """Create an entity with position"""
        entity = self.game_state.create_entity(tags)
        entity.add_component('transform', {
            'x': x,
            'y': y,
            'rotation': 0.0,
            'scale': 1.0
        })
        self._add_to_spatial_grid(entity)
        return entity

    def _add_to_spatial_grid(self, entity: EntityField) -> None:
        """Add entity to spatial grid"""
        transform = entity.get_component('transform')
        if transform:
            grid_x = int(transform['x'] // self.grid_size)
            grid_y = int(transform['y'] // self.grid_size)
            self.spatial_grid[(grid_x, grid_y)].append(entity.id)

    def _remove_from_spatial_grid(self, entity: EntityField) -> None:
        """Remove entity from spatial grid"""
        for cell_entities in self.spatial_grid.values():
            if entity.id in cell_entities:
                cell_entities.remove(entity.id)

    def find_entities_near(self, x: float, y: float, radius: float) -> List[EntityField]:
        """Find entities near a position"""
        nearby = []
        grid_x = int(x // self.grid_size)
        grid_y = int(y // self.grid_size)

        # Check surrounding cells
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                cell = (grid_x + dx, grid_y + dy)
                for entity_id in self.spatial_grid.get(cell, []):
                    entity = self.game_state.get_entity(entity_id)
                    if entity and entity.active:
                        transform = entity.get_component('transform')
                        if transform:
                            dist_sq = (transform['x'] - x)**2 + (transform['y'] - y)**2
                            if dist_sq <= radius**2:
                                nearby.append(entity)

        return nearby

    def update_spatial_entity(self, entity_id: str) -> None:
        """Update entity's position in spatial grid"""
        entity = self.game_state.get_entity(entity_id)
        if entity:
            self._remove_from_spatial_grid(entity)
            self._add_to_spatial_grid(entity)

    def update(self, dt: float) -> 'WorldField':
        """Update the world"""
        self.game_state.update(dt)
        return self

    def __repr__(self):
        return f"WorldField(name={self.name}, size={self.width}x{self.height}, entities={len(self.game_state.entities)})"


# Example system implementations

class PhysicsSystem(SystemField):
    """System for updating physics components"""

    def __init__(self):
        super().__init__("physics", ["transform", "velocity"])

    def update(self, entities: List[EntityField], dt: float) -> None:
        for entity in entities:
            transform = entity.get_component('transform')
            velocity = entity.get_component('velocity')

            if transform and velocity:
                # Update position
                transform['x'] += velocity['vx'] * dt
                transform['y'] += velocity['vy'] * dt

                # Apply drag if present
                drag = velocity.get('drag', 0.0)
                if drag > 0:
                    velocity['vx'] *= (1 - drag * dt)
                    velocity['vy'] *= (1 - drag * dt)


class RenderSystem(SystemField):
    """System for rendering entities"""

    def __init__(self):
        super().__init__("render", ["transform", "sprite"])
        self.render_calls = []

    def update(self, entities: List[EntityField], dt: float) -> None:
        self.render_calls = []

        # Sort entities by z-order
        sorted_entities = sorted(
            entities,
            key=lambda e: e.get_component('sprite').get('z_order', 0)
        )

        for entity in sorted_entities:
            transform = entity.get_component('transform')
            sprite = entity.get_component('sprite')

            if transform and sprite:
                self.render_calls.append({
                    'entity_id': entity.id,
                    'x': transform['x'],
                    'y': transform['y'],
                    'rotation': transform.get('rotation', 0),
                    'scale': transform.get('scale', 1.0),
                    'sprite_name': sprite.get('name', 'default'),
                    'color': sprite.get('color', '#FFFFFF')
                })


class LifetimeSystem(SystemField):
    """System for managing entity lifetimes"""

    def __init__(self, game_state: GameStateField):
        super().__init__("lifetime", ["lifetime"])
        self.game_state = game_state

    def update(self, entities: List[EntityField], dt: float) -> None:
        for entity in entities:
            lifetime = entity.get_component('lifetime')
            if lifetime:
                lifetime['remaining'] -= dt

                if lifetime['remaining'] <= 0:
                    # Entity expired
                    self.game_state.destroy_entity(entity.id)


class CosmicResonanceSystem(SystemField):
    """
    System that applies saga-inspired cosmic resonance to entities
    Entities influence each other based on harmonic patterns
    """

    def __init__(self):
        super().__init__("cosmic_resonance", ["transform", "resonance"])

    def update(self, entities: List[EntityField], dt: float) -> None:
        # Apply harmonic forces between entities
        for i, entity1 in enumerate(entities):
            transform1 = entity1.get_component('transform')
            resonance1 = entity1.get_component('resonance')

            for entity2 in entities[i+1:]:
                transform2 = entity2.get_component('transform')
                resonance2 = entity2.get_component('resonance')

                if transform1 and transform2 and resonance1 and resonance2:
                    # Calculate distance
                    dx = transform2['x'] - transform1['x']
                    dy = transform2['y'] - transform1['y']
                    dist = (dx*dx + dy*dy) ** 0.5

                    if dist > 0:
                        # Harmonic resonance based on golden ratio
                        phi = 1.618033988749
                        resonance_strength = resonance1.get('strength', 1.0) * resonance2.get('strength', 1.0)

                        # Apply force
                        force = resonance_strength / (dist * phi)
                        fx = (dx / dist) * force
                        fy = (dy / dist) * force

                        # Add velocity if entities have it
                        if entity1.has_component('velocity'):
                            vel1 = entity1.get_component('velocity')
                            vel1['vx'] += fx * dt
                            vel1['vy'] += fy * dt

                        if entity2.has_component('velocity'):
                            vel2 = entity2.get_component('velocity')
                            vel2['vx'] -= fx * dt
                            vel2['vy'] -= fy * dt
