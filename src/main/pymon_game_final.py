#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RMIT University
Programming Fundamentals - Assignment 3 
Pymon Game Implementation

Author: Mohammed Danish alam
Student ID: S4065642
Date: November 2024

Highest Level Attempted: HD

Program Description:
-----------------
This program implements a virtual pet game called Pymon where players control
a creature called Pymon to explore interconnected locations, battle other creatures,
and collect items. The game uses object-oriented programming concepts and file I/O.

"""
""""
# Pymon Game Documentation

## Overview
The Pymon game is an interactive, text-based role-playing game (RPG) that allows the player to control a Pymon, explore various locations, battle other creatures, and collect items. This project is built using Python, leveraging object-oriented programming principles to create a modular and extensible game structure.

The game includes features such as:
- Navigating different locations.
- Capturing adoptable Pymons after battles.
- Collecting and using items to assist in battles.
- Saving and loading game progress using CSV files for persistence.

This docstring serves as a comprehensive guide to understanding the design, implementation, and key challenges encountered during the development of the Pymon game.

## Design Process

### Initial Planning
The initial concept was inspired by classic RPGs. The goal was to create an engaging game where a player could:
- Control a Pymon to navigate through different areas.
- Battle and capture other Pymons.
- Collect items that could be used to enhance gameplay.

A modular design approach was adopted to ensure scalability and maintainability. This made it easy to add new game features without major code overhauls.

### Class and Method Design
#### Class Structure:
1. **Pymon Class**: Represents each creature in the game. This class encapsulates all the attributes of a Pymon, such as its nickname, description, energy, and its ability to challenge and capture other creatures.
2. **Location Class**: Represents the various areas in the game world. Each location is connected to others, allowing players to explore and find items or creatures.
3. **Item Class**: Represents items in the game that players can collect and use. Items may have different properties such as being consumable or non-consumable.
4. **Operation Class**: Manages the main game operations, including the game loop, player actions, and state management. This class acts as a central controller.

#### Methods Design:
- Methods such as `handle_movement()`, `view_inventory()`, and `handle_challenge()` were created to handle different aspects of gameplay.
- Each method encapsulates a specific game function, making it easier to maintain and modify individual features without impacting other areas of the code.

### Game Flow Design
The game is structured around a main game loop using a `while True` construct to continuously interact with the player until they decide to quit. Player actions like moving, battling, and collecting items are facilitated through input prompts.

To ensure a consistent experience, error handling was included for invalid inputs, guiding the player to provide valid responses and ensuring a smooth experience.

## Key Challenges and Solutions
### Managing Game State and Persistence
A major challenge was maintaining game state, allowing players to save progress and continue from where they left off. CSV files were chosen for simplicity and readability. Methods like `save_game()` and `load_game()` were implemented to serialize and deserialize game data, ensuring an accurate restoration of game state.

#### Challenge Encountered:
- Handling dynamic interactions, such as using items and capturing creatures, required maintaining consistency between saved and loaded states.

#### Solution:
- Helper methods were implemented for adding and removing items and creatures, ensuring that each action updated the game state correctly. Rigorous testing helped to resolve any discrepancies.

### Complexity in Interactions
Managing interactions between different entities—such as using items or capturing Pymons—required careful state management. The `Operation` class acted as the central hub for all interactions, with helper functions ensuring state consistency.

### Data Handling
Using CSV files to manage game data was a design choice driven by simplicity. However, ensuring that the correct data was saved and loaded, and dealing with any inconsistencies, proved challenging. This was addressed by:
- Implementing systematic methods for saving and restoring attributes.
- Testing different scenarios to verify the accuracy of data handling.

## Detailed Design Choices
### Object-Oriented Approach
Using classes to represent game elements allowed for clean encapsulation of behaviors and properties. The `Operation` class acted as the game controller, similar to the MVC pattern, where `Operation` interacted with models (`Pymon`, `Item`, `Location`) to facilitate gameplay.

### Data Persistence
Data persistence was achieved through CSV files for the following reasons:
- **Simplicity**: CSV files are easy to read, write, and debug.
- **Human-Readable**: This made it easy to verify saved game states manually.

The `save_game()` and `load_game()` methods were carefully written to store all aspects of the game state, from inventory items to Pymon energy levels. This required careful testing to ensure consistency between saved and loaded states.

### User Interaction
The game utilizes a `while True` loop for continuous interaction. Exception handling was added to manage incorrect user inputs gracefully, ensuring a smooth experience.

## Reflection on Challenges and Lessons Learned
### Modular Approach and Extendibility
The modular approach allowed easy addition of new features. For example, new Pymons, items, or even game modes can be added without modifying the core gameplay significantly.

### Debugging State Management
Managing interactions between different game elements was challenging, especially when saving and loading data. This highlighted the importance of proper state management and the value of thorough testing.

### Learning Outcomes
This project provided a deep understanding of:
- **Object-Oriented Design**: Creating classes that interact with each other in a clean and efficient manner.
- **Data Serialization**: Using CSV for persistence was an excellent way to learn about data serialization and ensuring state consistency.
- **User Interaction and Exception Handling**: Designing a fluid game flow while managing invalid user inputs taught valuable lessons in user experience design.

## References
1. **CSV Handling in Python**:
   - **Source**: ["Working with CSV in Python" by RealPython](https://realpython.com/python-csv/)
   - **Usage**: This helped implement the `save_game()` and `load_game()` methods, providing best practices for working with CSV files in Python.
2. **Object-Oriented Game Design Concepts**:
   - General tutorials and examples of turn-based RPG mechanics were used to design the classes and methods for game interactions.
3. **Python Mocking for Testing**:
   - **Source**: Python's `unittest.mock` documentation.
   - **Usage**: Used to create comprehensive unit tests for simulating user inputs and verifying different game features.

## How to Use the Game Code
- **Start Game**: Run the `Operation.start_game()` method to begin gameplay.
- **Save and Load**: Use the `save_game()` and `load_game()` methods to save your progress or resume a saved game.
- **Admin Features**: The `handle_admin_menu()` function allows adding new items, creatures, and locations for enhanced gameplay.

## Acknowledgements
This project was made possible by resources from Python tutorials, online forums, and hands-on practice. The Python community provided invaluable help in overcoming challenges related to object-oriented programming, data persistence, and testing.

"""

""""
Design Approach:
--------------
The program is structured using multiple classes following OOP principles:
- Location: Manages game locations and their connections
- Creature: Base class for all game entities
- Pymon: Main player character (inherits from Creature)
- Record: Handles data management and file operations
- Operation: Controls game flow and user interface

Implementation Notes:
------------------
- Using only basic Python packages: sys, os, datetime, csv, random
- File-based data storage using CSV format
- Exception handling for file operations and user input

References:
----------
1. RMIT Programming Fundamentals Course Materials
2. Python Documentation: https://docs.python.org/3/
"""

import sys
import os
import csv
import random
from datetime import datetime


# In[2]:


# Custom Exceptions
class InvalidDirectionException(Exception):
    """Raised when an invalid direction is selected."""
    def __init__(self, direction):
        self.direction = direction
        self.message = f"Invalid direction: {direction}"
        super().__init__(self.message)

class InvalidInputFileFormat(Exception):
    """Raised when a CSV file has invalid content or format."""
    def __init__(self, filename, error_detail):
        self.filename = filename
        self.message = f"Invalid format in file {filename}: {error_detail}"
        super().__init__(self.message)


# In[ ]:



class Item:
    """
    Represents items that can be found in locations.
    
    Attributes:
        name (str): Name of the item
        description (str): Item description
        pickable (bool): Whether item can be picked up
        consumable (bool): Whether item can be consumed/used
    """
    def __init__(self, name, description, pickable=True, consumable=False):
        self.name = name
        self.description = description
        self.pickable = pickable
        self.consumable = consumable
        self.location = None
    
    def get_description(self):
        """Return item description with pickup status."""
        status = "Can be picked up" if self.pickable else "Cannot be picked up"
        return f"{self.name}: {self.description} ({status})"


# In[4]:


class Location:
    """
    Location class represents a place in the game world.
    
    Attributes:
        name (str): Name of the location
        description (str): Description of the location
        doors (dict): Dictionary of connected locations in each direction
        creatures (list): List of creatures in this location
        items (list): List of items in this location
    """
    
    def __init__(self, name="New Room", description="An empty room", west=None, north=None, east=None, south=None):
        """
        Initialize a new Location object.
        
        Args:
            name (str): Location name
            description (str): Location description
            west, north, east, south: Connected locations in each direction
        """
        self.name = name
        self.description = description
        self.doors = {
            "west": west,
            "north": north, 
            "east": east,
            "south": south
        }
        self.creatures = []
        self.items = []
        
    def add_item(self, item):
        """Add an item to this location."""
        self.items.append(item)
        item.location = self
        print(f"Item '{item.name}' added to '{self.name}'")
    
    def remove_item(self, item):
        """Remove an item from this location."""
        if item in self.items:
            self.items.remove(item)
            item.location = None
            print(f"Item '{item.name}' removed from location '{self.name}'.")
        else:
            print(f"Item '{item.name}' not found in location '{self.name}' to remove.")
            
    def connect(self, direction, other_location):
        """
        Connect this location to another in the specified direction.
        
        Args:
            direction (str): Direction of connection ("west", "north", "east", "south")
            other_location (Location): Location to connect to
        """
        if direction not in ["west", "north", "east", "south"]:
            raise ValueError("Invalid direction")
        
        # Prevent self-connection
        if self == other_location:
            raise ValueError("Cannot connect a location to itself")
        # Set bidirectional connection
        opposite = {
            "west": "east",
            "east": "west",
            "north": "south",
            "south": "north"
        }
        # Check for existing connections and warn if overwriting
        if self.doors[direction]:
            print(f"Warning: Overwriting existing connection to {self.doors[direction].name} in direction '{direction}'.")
        if other_location.doors[opposite[direction]]:
            print(f"Warning: Overwriting existing connection to {other_location.doors[opposite[direction]].name} in direction '{opposite[direction]}'.")

        self.doors[direction] = other_location
        other_location.doors[opposite[direction]] = self

        # Debugging output
        print(f"Connected {self.name} to {other_location.name} towards {direction}")
        print(f"Connected {other_location.name} to {self.name} towards {opposite[direction]}")

    def add_creature(self, creature):
        """Add a creature to this location."""
        self.creatures.append(creature)
        creature.location = self
    
    def remove_creature(self, creature):
        """Remove a creature from this location."""
        if creature in self.creatures:
            self.creatures.remove(creature)
            creature.location = None
    
    def get_description(self):
        """
        Return a detailed description of the location and its contents.
        
        Returns:
            str: Formatted description including location details, available directions,
                creatures, and items
        """
        # Start with basic location info
        desc = f"\nLocation: {self.name}\n"
        desc += f"Description: {self.description}\n"
        
        # Add available directions
        directions = [dir for dir in self.doors if self.doors[dir] is not None]
        if directions:
            desc += "Available directions: " + ", ".join(directions) + "\n"
        
        # Add creatures
        if self.creatures:
            desc += "\nCreatures here:\n"
            for creature in self.creatures:
                desc += f"- {creature.nickname}: {creature.description}\n"
        else:
            desc += "\nNo creatures here.\n"
        
        # Add items
        if self.items:
            desc += "\nItems here:\n"
            for item in self.items:
                desc += f"- {item.get_description()}\n"
        
        return desc


# In[5]:


class Creature:
    """
    Base class for all creatures in the game.
    
    Attributes:
        nickname (str): Unique name of the creature
        description (str): Description of the creature
        location (Location): Current location of the creature
    """
    
    def __init__(self, nickname, description="A mysterious creature", adoptable = False):
        """
        Initialize a new Creature object.
        
        Args:
            nickname (str): Creature's unique name
            description (str): Creature's description
        """
        self.nickname = nickname
        self.description = description
        self.location = None
        self.adoptable = adoptable
        
    def get_description(self):
        """Return the creature's description."""
        status = "Can be adopted" if self.adoptable else "Cannot be adopted"
        return f"{self.nickname}: {self.description} ({status})"
        


# In[6]:


from datetime import datetime

class BattleRecord:
    """Class to store battle information."""
    def __init__(self, opponent_name, wins, draws, losses):
        self.timestamp = datetime.now()
        self.opponent = opponent_name
        self.wins = wins
        self.draws = draws
        self.losses = losses

    def __str__(self):
        return (f"Battle {self.timestamp.strftime('%d/%m/%Y %I:%M%p')} "
                f"Opponent: {self.opponent}, W: {self.wins} D: {self.draws} L: {self.losses}")


# In[7]:


class Pymon(Creature):
    """
    Player-controlled creature with additional capabilities.
    Inherits from Creature class.
    
    Additional Attributes:
        energy (int): Current energy level (max 3)
        inventory (list): List of collected items
        captured_pymons (list): List of Pymons captured in battles
        current_immunity (bool): Whether Pymon has battle immunity (from potion)
        Adds item usage, battle mechanics, and movement features.
        Enhanced Pymon class with DI level features.
        Includes energy management and improved item usage.
    """
    
    def __init__(self, nickname, description="A friendly Pymon"):
        """Initialize a Pymon with 3 energy points."""
        super().__init__(nickname, description, adoptable=True)
        self.energy = 3
        self.inventory = []
        self.captured_pymons = []  # List to store captured Pymons
        self.current_immunity = False  # For magic potion effect
        self.battle_stats = {
            'wins': 0,
            'losses': 0,
            'draws': 0
        }
        self.moves_count = 0  # Track number of moves
        self.battle_history = []  # For timestamped battle records
    
    def pick_item(self, item_name):
        """
        Attempt to pick up an item from current location.

        Args:
            item_name (str): Name of item to pick up
        Returns:
            bool: True if item was picked up, False otherwise
        """
        if not self.location:
            print("Pymon is not in any location.")
            return False

        print(f"Pymon is at location '{self.location.name}'. Items available: {[item.name for item in self.location.items]}")

        for item in self.location.items:
            print(f"Checking item '{item.name}' (Pickable: {item.pickable})")
            if item.name.lower() == item_name.lower() and item.pickable:
                print(f"Picking up item '{item.name}'...")
                self.inventory.append(item)
                self.location.remove_item(item)
                print(f"Item '{item.name}' picked up and removed from location '{self.location.name}'.")

                return True

        print(f"Item '{item_name}' not found or not pickable.")
        return False
    
    
    def _handle_energy_depletion(self):
        """Handle what happens when Pymon runs out of energy."""
        if self.random_move_after_loss():
            if self.captured_pymons:
                print("Switching to a captured Pymon...")
                new_pymon = self.switch_active_pymon(0)
                if new_pymon:
                    self = new_pymon
                    print(f"Switched to {self.nickname}")
            else:
                print("Game Over! No more Pymons available!")
                raise GameOverException("No energy and no backup Pymons")
                
                
#     def challenge_creature(self, target):
#         """
#         Challenge another creature to a battle.
        
#         Args:
#             target (Creature): Creature to battle
#         Returns:
#             bool: True if won battle, False if lost
#         """
#         if not target.adoptable or target.location != self.location:
#             return False
            
#         print(f"\nBattle with {target.nickname} begins!")
#         wins = 0
#         losses = 0
#         rounds = 0
        
#         while rounds < 3 and wins < 2 and losses < 2:
#             rounds += 1
#             result = self._battle_round(target)
            
#             if result == 'win':
#                 wins += 1
#                 self.battle_stats['wins'] += 1
#             elif result == 'lose':
#                 losses += 1
#                 self.battle_stats['losses'] += 1
#                 if not self.current_immunity:
#                     self.energy -= 1  # Lose energy point only if not immune
#                     print(f"Energy reduced to {self.energy}")
#                 else:
#                     print("Magic potion protected you from energy loss!")
#                     self.current_immunity = False  # Use up the immunity
#             else:
#                 self.battle_stats['draws'] += 1
                
#             if self.energy <= 0:
#                 print("Out of energy! Battle lost!")
#                 return False
        
#         battle_record = BattleRecord(
#             opponent_name=target.nickname,
#             wins=wins,
#             draws=draws,
#             losses=losses
#         )
#         self.battle_history.append(battle_record)
        
#         battle_won = wins > losses
#         if battle_won:
#             self.capture_pymon(target)
        
#         return battle_won

    def challenge_creature(self, target):
        """
        Challenge another creature to a battle.

        Args:
            target (Creature): Creature to battle
        Returns:
            bool: True if won battle, False if lost
        """
        if not target.adoptable or target.location != self.location:
            return False

        print(f"\nBattle with {target.nickname} begins!")
        wins = 0
        draws = 0
        losses = 0
        rounds = 0

        while rounds < 3 and wins < 2 and losses < 2:
            rounds += 1
            result = self._battle_round(target)

            if result == 'win':
                wins += 1
                self.battle_stats['wins'] += 1
            elif result == 'lose':
                losses += 1
                self.battle_stats['losses'] += 1
                if not self.current_immunity:
                    self.energy -= 1  # Lose energy point only if not immune
                    print(f"Energy reduced to {self.energy}")
                else:
                    print("Magic potion protected you from energy loss!")
                    self.current_immunity = False  # Use up the immunity
            else:
                draws += 1
                self.battle_stats['draws'] += 1

            if self.energy <= 0:
                print("Out of energy! Battle lost!")
                return False

        battle_record = BattleRecord(
            opponent_name=target.nickname,
            wins=wins,
            draws=draws,
            losses=losses
        )
        self.battle_history.append(battle_record)

        battle_won = wins > losses
        if battle_won:
            self.capture_pymon(target)

        return battle_won

    def _handle_binocular_use(self):
        """
        Interactive binocular usage interface.

        Returns:
            bool: True if binocular was used successfully
        """
        while True:
            print("\nHow would you like to use the binocular?")
            print("1) View current location")
            print("2) Look north")
            print("3) Look south")
            print("4) Look east")
            print("5) Look west")
            print("6) Stop using binocular")

            choice = input("Enter your choice (1-6): ")

            try:
                if choice == "1":
                    self.use_binocular("current")
                    return True
                elif choice == "2":
                    self.use_binocular("north")
                    return True
                elif choice == "3":
                    self.use_binocular("south")
                    return True
                elif choice == "4":
                    self.use_binocular("east")
                    return True
                elif choice == "5":
                    self.use_binocular("west")
                    return True
                elif choice == "6":
                    return True
                else:
                    print("Invalid choice! Please try again.")
            except Exception as e:
                print(f"Error using binocular: {str(e)}")

            input("\nPress Enter to continue...")

#     def use_binocular(self, direction):
#         """
#         View in a specific direction using binocular.

#         Args:
#             direction (str): Direction to look ("current", "north", "south", "east", "west")
#         """
#         if direction == "current":
#             print(f"\nCurrently at {self.location.name}:")
#             print(f"Description: {self.location.description}")

#             # Show creatures
#             creatures = ", ".join(c.nickname for c in self.location.creatures if c != self)
#             if creatures:
#                 print(f"Creatures here: {creatures}")

#             # Show items
#             items = ", ".join(item.name for item in self.location.items)
#             if items:
#                 print(f"Items here: {items}")

#             # Show available paths
#             connections = [d for d in self.location.doors if self.location.doors[d]]
#             if connections:
#                 print(f"Paths leading to: {', '.join(connections)}")

#         elif direction in self.location.doors:
#             next_loc = self.location.doors[direction]
#             if next_loc:
#                 print(f"\nLooking {direction} towards {next_loc.name}:")
#                 print(f"Description: {next_loc.description}")

#                 # Show creatures in next location
#                 creatures = [c.nickname for c in next_loc.creatures]
#                 if creatures:
#                     print("Creatures visible:", ", ".join(creatures))

#                 # Show items in next location
#                 items = [item.name for item in next_loc.items]
#                 if items:
#                     print("Items visible:", ", ".join(items))
#             else:
#                 print(f"\nThere's nothing to see in the {direction} direction.")
#         else:
#             print(f"\nThere's nothing to see in the {direction} direction.")
      
    def use_binocular(self, direction=None):
        """
        Interactive binocular usage interface.

        Args:
            direction (str, optional): Direction to look ("current", "north", "south", "east", "west"). If not provided, the method will display a menu for the user to select the direction.

        Returns:
            bool: True if binocular was used successfully
        """
        
        if direction == "current":
            print(f"\nCurrently at {self.location.name}:")
            print(f"Description: {self.location.description}")
            # Show creatures
            creatures = ", ".join(c.nickname for c in self.location.creatures if c != self)
            if creatures:
                print(f"Creatures here: {creatures}")
            # Show items
            items = ", ".join(item.name for item in self.location.items)
            if items:
                print(f"Items here: {items}")
            # Show available paths
            connections = [d for d in self.location.doors if self.location.doors[d]]
            if connections:
                print(f"Paths leading to: {', '.join(connections)}")
        elif direction in self.location.doors:
            next_loc = self.location.doors[direction]
            if next_loc:
                print(f"\nLooking {direction} towards {next_loc.name}:")
                print(f"Description: {next_loc.description}")
                # Show creatures in next location
                creatures = [c.nickname for c in next_loc.creatures]
                if creatures:
                    print("Creatures visible:", ", ".join(creatures))
                # Show items in next location
                items = [item.name for item in next_loc.items]
                if items:
                    print("Items visible:", ", ".join(items))
            else:
                print(f"\nThere's nothing to see in the {direction} direction.")
        else:
            print(f"\nThere's nothing to see in the {direction} direction.")

    def random_move_after_loss(self):
        """Move Pymon to random location after losing battle."""
        if hasattr(self, 'record'):  # Check if record reference exists
            available_locations = list(self.record.locations.values())
        else:
            # Gather all connected locations
            available_locations = []
            locations_to_check = [self.location]
            checked_locations = set()

            while locations_to_check:
                current = locations_to_check.pop(0)
                if current not in checked_locations:
                    checked_locations.add(current)
                    available_locations.append(current)

                    # Add connected locations
                    for direction in current.doors:
                        if current.doors[direction] and current.doors[direction] not in checked_locations:
                            locations_to_check.append(current.doors[direction])

        if available_locations:
            # Remove current location from options
            if self.location in available_locations:
                available_locations.remove(self.location)

            if available_locations:
                new_location = random.choice(available_locations)
                self.location.remove_creature(self)
                new_location.add_creature(self)
                print(f"Your Pymon has fled to {new_location.name}!")
                return True
        return False


    def capture_pymon(self, target):
        """
        Capture a Pymon after winning a battle.

        Args:
            target (Creature): Pymon to capture
        """
        if target.adoptable:
            print(f"\nAttempting to capture {target.nickname}...")  # Debugging statement

            # Remove from current location
            target.location.remove_creature(target)

            # Convert the target to an instance of Pymon if it's not already
            if not isinstance(target, Pymon):
                target = Pymon(target.nickname, target.description)
                target.energy = 3  # Set default energy to 3

            # Add to captured list
            self.captured_pymons.append(target)
            print(f"{target.nickname} has been captured successfully!")  # Debugging statement
            print(f"Total Pymons captured: {len(self.captured_pymons)}")
            
            
    def _battle_round(self, opponent):
        """
        Play one round of rock, paper, scissors.
        
        Returns:
            str: 'win', 'lose', or 'draw'
        """
        choices = ['rock', 'paper', 'scissors']
        
        print("\nChoose: rock, paper, or scissors")
        player_choice = input("Your choice: ").lower()
        while player_choice not in choices:
            print("Invalid choice! Try again.")
            player_choice = input("Your choice: ").lower()
            
        opponent_choice = random.choice(choices)
        print(f"Opponent chose: {opponent_choice}")
        
        if player_choice == opponent_choice:
            print("Draw!")
            return 'draw'
        elif (
            (player_choice == 'rock' and opponent_choice == 'scissors') or
            (player_choice == 'paper' and opponent_choice == 'rock') or
            (player_choice == 'scissors' and opponent_choice == 'paper')
        ):
            print("You win this round!")
            return 'win'
        else:
            print("You lose this round!")
            return 'lose'
        
    def switch_active_pymon(self, index):
        """
        Switch to a different captured Pymon.

        Args:
            index (int): Index of Pymon to switch to
        Returns:
            Pymon: The new active Pymon if switch successful, None otherwise
        """
        # Debugging: Print captured Pymons to verify contents
        print("\nCurrent Captured Pymons:")
        for i, captured_pymon in enumerate(self.captured_pymons):
            print(f"{i}: {captured_pymon.nickname} ({type(captured_pymon)})")

        if 0 <= index < len(self.captured_pymons):
            # Store current state
            old_location = self.location
            old_inventory = self.inventory
            old_energy = self.energy
            old_battle_stats = self.battle_stats
            old_current_immunity = self.current_immunity

            # Get the new Pymon from the captured list
            new_pymon = self.captured_pymons[index]

            # Debugging: Verify the type of the new Pymon
            print(f"\nAttempting to switch to: {new_pymon.nickname} ({type(new_pymon)})")

            # Ensure that new_pymon is an instance of Pymon
            if not isinstance(new_pymon, Pymon):
                new_pymon = Pymon(new_pymon.nickname, new_pymon.description)

            # Update captured list: Replace the captured Pymon with the current one
            self.captured_pymons[index] = self

            # Transfer attributes to new Pymon
            new_pymon.location = old_location
            new_pymon.inventory = old_inventory
            new_pymon.energy = old_energy
            new_pymon.battle_stats = old_battle_stats
            new_pymon.current_immunity = old_current_immunity

            return new_pymon
        else:
            # Debugging: Index out of range
            print("\nError: Index out of range for captured Pymons.")
        return None

    def move(self, direction):
        """
        Move Pymon in specified direction with energy management.

        Args:
            direction (str): Direction to move ("north", "south", "east", "west")

        Returns:
            bool: True if movement successful, False otherwise

        Raises:
            InvalidDirectionException: If direction is invalid or no path exists
        """
        # Validate direction
        if direction not in ["north", "south", "east", "west"]:
            raise InvalidDirectionException(f"Invalid direction: {direction}")

        # Check if movement is possible
        if not self.location:
            return False

        if direction not in self.location.doors:
            raise InvalidDirectionException(f"No door in direction: {direction}")

        new_location = self.location.doors[direction]
        if not new_location:
            raise InvalidDirectionException(f"No path to {direction}")

        # Energy management before movement
        self.moves_count += 1
        if self.moves_count % 2 == 0:  # Every 2 moves
            self.energy -= 1
            print(f"Energy decreased to {self.energy} after 2 moves")

            # Handle energy depletion
            if self.energy <= 0:
                print("Out of energy! Your Pymon will escape!")
                self._handle_energy_depletion()
                return False

        # Perform the actual movement
        try:
            self.location.remove_creature(self)
            new_location.add_creature(self)
            self.location = new_location  # Update current location
            print(f"Moved to {new_location.name}")
            return True
        except Exception as e:
            print(f"Movement failed: {str(e)}")
            return False
    
    def use_item(self, item_name):
        """
        Enhanced item usage with energy management and binocular handling.

        Args:
            item_name (str): Name of item to use
        Returns:
            bool: True if item was used successfully
        """
        # Find matching item in inventory
        for item in self.inventory[:]:  # Use slice copy to safely modify during iteration
            if item.name.lower() == item_name.lower():
                # Handle Apple
                if item.name == "Apple":
                    if self.energy < 3:
                        self.energy += 1
                        self.inventory.remove(item)
                        print(f"Energy restored to {self.energy}/3")
                        return True
                    else:
                        print("Energy already full!")
                        return False

                # Handle Magic Potion
                elif item.name == "Magic Potion":
                    self.current_immunity = True
                    self.inventory.remove(item)
                    print("Magic potion applied! You're immune to the next battle loss.")
                    return True

                # Handle Binocular
                elif item.name == "Binocular":
                    # Use the menu-based binocular interface
                    return self._handle_binocular_use()

        # Item not found or couldn't be used
        print(f"No {item_name} in inventory or cannot be used!")
        return False

    
    
    def get_description(self):
        """Return detailed information including captured Pymons."""
        desc = f"""Your Pymon: {self.nickname}
    Description: {self.description}
    Energy: {self.energy}/3
    Current Location: {self.location.name if self.location else 'Unknown'}
    Battle Stats: Wins: {self.battle_stats['wins']}, Losses: {self.battle_stats['losses']}, Draws: {self.battle_stats['draws']}"""

        # Show inventory
        if self.inventory:
            desc += "\nInventory:\n"
            for item in self.inventory:
                desc += f"- {item.get_description()}\n"
        else:
            desc += "\nInventory: Empty\n"

        # Show captured Pymons
        if self.captured_pymons:
            desc += "\nCaptured Pymons:\n"
            for i, pymon in enumerate(self.captured_pymons):
                desc += f"{i+1}) {pymon.nickname}: {pymon.description}\n"

        if self.current_immunity:
            desc += "\nStatus: Protected by magic potion\n"

        return desc
    
    def generate_stats(self):
        """Generate complete battle statistics."""
        print(f"\nBattle Statistics for {self.nickname}:")
        
        if not self.battle_history:
            print("No battles fought yet!")
            return
            
        for i, battle in enumerate(self.battle_history, 1):
            print(f"Battle {i}: {battle}")
            
        # Calculate totals
        total_wins = sum(b.wins for b in self.battle_history)
        total_draws = sum(b.draws for b in self.battle_history)
        total_losses = sum(b.losses for b in self.battle_history)
        
        print(f"\nTotals: W: {total_wins} D: {total_draws} L: {total_losses}")
        


# In[8]:


class Record:
    """
    Manages game data and file operations.
    
    Attributes:
        locations (list): List of all game locations
        creatures (list): List of all creatures
        items (list): List of all items
    """
    
    def __init__(self):
        """Initialize empty lists for game data."""
        self.locations = {}
        self.creatures = []
        self.items = []
        
    def load_data(self, locations_file="locations.csv", 
                 creatures_file="creatures.csv", 
                 items_file="items.csv"):
        """Load all game data with validation."""
        try:
            # Load locations
            with open(locations_file, 'r') as file:
                self.validate_csv_format(file, ['name', 'description', 'west', 'north', 'east', 'south'])
                self.load_locations(locations_file)
                
            # Load creatures
            with open(creatures_file, 'r') as file:
                self.validate_csv_format(file, ['name', 'description', 'adoptable'])
                self.load_creatures(creatures_file)
                
            # Load items
            with open(items_file, 'r') as file:
                self.validate_csv_format(file, ['name', 'description', 'pickable', 'consumable'])
                self.load_items(items_file)
                
        except FileNotFoundError as e:
            print(f"Warning: {e.filename} not found. Using default setup.")
            self.setup_pass_level()
        except csv.Error as e:
            raise InvalidInputFileFormat(e.filename, f"CSV error: {str(e)}")
    
    
    def import_creatures(self):
        """Load and validate creatures from CSV file."""
        try:
            with open('creatures.csv', 'r', newline='') as file:
                reader = csv.DictReader(file)

                for row in reader:
                    # Strip whitespace and handle data
                    name = row['name'].strip()
                    description = row['description'].strip()
                    adoptable = row['adoptable'].strip().lower() == 'yes'

                    # Create creature
                    creature = Creature(name, description, adoptable)

                    # Add to master list
                    self.creatures.append(creature)

                    # Place creatures in initial locations
                    if name == "Kitimon":
                        self.locations["Playground"].add_creature(creature)
                    elif name == "Sheep":
                        self.locations["Beach"].add_creature(creature)
                    elif name == "Marimon":
                        self.locations["School"].add_creature(creature)

        except FileNotFoundError:
            print("Warning: creatures.csv not found. Using default setup.")
            self.setup_pass_level()
        except Exception as e:
            print(f"Error importing creatures: {str(e)}")

    def import_items(self):
        """Load and validate items from CSV file."""
        try:
            with open('items.csv', 'r', newline='') as file:
                reader = csv.DictReader(file)

                for row in reader:
                    # Strip whitespace and handle data
                    name = row['name'].strip()
                    description = row['description'].strip()
                    pickable = row['pickable'].strip().lower() == 'yes'
                    consumable = row['consumable'].strip().lower() == 'yes'

                    # Create item
                    item = Item(name, description, pickable, consumable)

                    # Add to master list
                    self.items.append(item)

                    # Place items in initial locations
                    if name in ["Tree", "Magic Potion"]:
                        self.locations["Playground"].add_item(item)
                    elif name == "Apple":
                        self.locations["Beach"].add_item(item)
                    elif name == "Binocular":
                        self.locations["School"].add_item(item)

        except FileNotFoundError:
            print("Warning: items.csv not found. Using default setup.")
            self._setup_default_items()
        except Exception as e:
            print(f"Error importing items: {str(e)}")

    def validate_csv_format(self, file, required_columns):
        """
        Generic CSV validation for any file.
        
        Args:
            file: File object to validate
            required_columns: List of required column names
        Raises:
            InvalidInputFileFormat: If format is invalid
        """
        reader = csv.DictReader(file)
        
        # Check for required columns
        if not all(col in reader.fieldnames for col in required_columns):
            raise InvalidInputFileFormat(
                file.name, 
                f"Missing required columns. Required: {required_columns}"
            )
        
        # Validate no empty required fields
        for row in reader:
            for col in required_columns:
                if not row[col]:
                    raise InvalidInputFileFormat(
                        file.name,
                        f"Missing value for {col} in row: {row}"
                    )
        
        # Reset file pointer for actual data loading
        file.seek(0)
        next(reader)  # Skip header row
        
    def load_locations(self, filename="locations.csv"):
        """
        Load and validate locations from CSV file.

        Args:
            filename (str): Path to locations CSV file

        Raises:
            InvalidInputFileFormat: If CSV format is invalid
            FileNotFoundError: If file is not found
        """
        required_columns = ['name', 'description', 'west', 'north', 'east', 'south']

        try:
            with open(filename, 'r') as file:
                reader = csv.DictReader(file)

                # Validate headers
                if not all(col in reader.fieldnames for col in required_columns):
                    raise InvalidInputFileFormat(filename, "Missing required columns")

                # First pass: Create locations
                for row in reader:
                    # Validate data and strip whitespace from name and description
                    name = row['name'].strip()
                    description = row['description'].strip()

                    if not name or not description:
                        raise InvalidInputFileFormat(filename, 
                            f"Missing name or description for row: {row}")

                    # Create and store the Location instance
                    location = Location(name, description)
                    self.locations[name] = location

                # Second pass: Connect locations
                file.seek(0)
                next(reader)  # Skip header

                for row in reader:
                    # Get the location by name
                    location_name = row['name'].strip()
                    loc = self.locations[location_name]

                    # Strip whitespace for directions and handle "None" properly
                    directions = {
                        "west": row["west"].strip() if row["west"].strip().lower() != 'none' else None,
                        "north": row["north"].strip() if row["north"].strip().lower() != 'none' else None,
                        "east": row["east"].strip() if row["east"].strip().lower() != 'none' else None,
                        "south": row["south"].strip() if row["south"].strip().lower() != 'none' else None
                    }

                    # Connect locations if a valid reference is provided
                    for direction, neighbor in directions.items():
                        if neighbor and neighbor in self.locations:
                            loc.connect(direction, self.locations[neighbor])
                        elif neighbor:  # If there's an invalid reference
                            raise InvalidInputFileFormat(filename, f"Invalid location reference: {neighbor}")

        except FileNotFoundError:
            print(f"Warning: {filename} not found. Using default setup.")
            self.setup_pass_level()
        except csv.Error as e:
            raise InvalidInputFileFormat(filename, f"CSV parsing error: {str(e)}")
        except KeyError as e:
            raise InvalidInputFileFormat(filename, f"Missing required column: {str(e)}")
        except Exception as e:
            raise InvalidInputFileFormat(filename, f"Unexpected error: {str(e)}")

    def load_creatures(self, filename="creatures.csv"):
        """
        Load and validate creatures from CSV file.

        Args:
            filename (str): Path to creatures CSV file

        Raises:
            InvalidInputFileFormat: If CSV format is invalid
            FileNotFoundError: If file is not found
        """
        try:
            with open(filename, 'r') as file:
                reader = csv.DictReader(file)
                
                # Strip the field names of whitespace
                reader.fieldnames = [field.strip() for field in reader.fieldnames]

                # Print out fieldnames to see what's being read (for debugging purposes)
                print("CSV Headers:", reader.fieldnames)
            
                for row in reader:
                    # Strip whitespace from relevant fields
                    name = row['name'].strip()
                    description = row['description'].strip()
                    adoptable = row['adoptable'].strip().lower() == 'yes'

                    # Validate data
                    if not name or not description:
                        raise InvalidInputFileFormat(filename, 
                            f"Missing name or description for row: {row}")

                    # Create Creature instance
                    creature = Creature(name, description, adoptable)

                    # Add creature to the master list
                    self.creatures.append(creature)

                    # Optionally, place the creature in a starting location (if desired)
                    if creature.nickname == "Kitimon":
                        self.locations["Playground"].add_creature(creature)
                    elif creature.nickname == "Sheep":
                        self.locations["Beach"].add_creature(creature)
                    elif creature.nickname == "Marimon":
                        self.locations["School"].add_creature(creature)

        except FileNotFoundError:
            print(f"Warning: {filename} not found. Using default setup.")
            self.setup_pass_level()
        except csv.Error as e:
            raise InvalidInputFileFormat(filename, f"CSV parsing error: {str(e)}")

        
    def load_items(self, filename="items.csv"):
        """Load and validate items from CSV file."""
        try:
            with open(filename, 'r') as file:
                reader = csv.DictReader(file)
                
                # Strip the field names of whitespace
                reader.fieldnames = [field.strip().lower() for field in reader.fieldnames]

                # Print out fieldnames to see what's being read (for debugging purposes)
                print("CSV Headers:", reader.fieldnames)
                
                for row in reader:
                    # Strip whitespace from relevant fields
                    name = row['name'].strip()
                    description = row['description'].strip()
                    pickable = row['pickable'].strip().lower() == 'yes'
                    consumable = row['consumable'].strip().lower() == 'yes'

                    # Create item from CSV data
                    item = Item(name=name, description=description, pickable=pickable, consumable=consumable)

                    # Add item to the master list
                    self.items.append(item)

                    # Optionally, place the item in a specific location
                    if item.name == "Tree" or item.name == "Magic Potion":
                        self.locations["Playground"].add_item(item)
                    elif item.name == "Apple":
                        self.locations["Beach"].add_item(item)
                    elif item.name == "Binocular":
                        self.locations["School"].add_item(item)

        except FileNotFoundError:
            # Fall back to default items
            self._setup_default_items()
        except csv.Error as e:
            raise InvalidInputFileFormat(filename, f"CSV error: {str(e)}")

        
    def _setup_default_items(self):
        """Setup default items if CSV file is not found."""
        apple = Item("Apple", "An edible green fruit that will boost your energy", 
                    pickable=True, consumable=True)
        potion = Item("Magic Potion", "Gives temporary immunity in battle", 
                     pickable=True, consumable=True)
        binocular = Item("Binocular", "Device to see super far", 
                        pickable=True, consumable=False)
        tree = Item("Tree", "A decorative tree", 
                   pickable=False, consumable=False)

        # Place items
        self.locations["Playground"].add_item(tree)
        self.locations["Playground"].add_item(potion)
        self.locations["Beach"].add_item(apple)
        self.locations["School"].add_item(binocular)

        self.items.extend([apple, potion, binocular, tree])
    
    def setup_pass_level(self):
        """
        Set up the initial game state for PASS level.

        Returns:
            Location: The starting location (School)
        """
        # Create locations with descriptions
        self.locations["School"] = Location(
            name="School",
            description="A secondary school for local creatures with 3 two-story buildings."
        )

        self.locations["Playground"] = Location(
            name="Playground",
            description="An outdoor playground with slide and swing clearly visible."
        )

        self.locations["Beach"] = Location(
            name="Beach",
            description="A wide open white sanded beach with a brown hill on the side."
        )

        # Connect locations
        self.locations["School"].connect("east", self.locations["Playground"])
        self.locations["Playground"].connect("north", self.locations["Beach"])

        # Create creatures
        kitimon = Creature(
            nickname="Kitimon",
            description="Large blue and white Pymon with yellow fangs",
            adoptable=True
        )

        sheep = Creature(
            nickname="Sheep",
            description="Small fluffy animal with interesting curly white fur",
            adoptable=False
        )

        marimon = Creature(
            nickname="Marimon",
            description="Medium red and yellow Pymon with a cute round face",
            adoptable=True
        )

        # Place creatures in locations
        self.locations["Playground"].add_creature(kitimon)
        self.locations["Beach"].add_creature(sheep)
        self.locations["School"].add_creature(marimon)

        # Add creatures to master list
        self.creatures.extend([kitimon, sheep, marimon])

        # Create and place default items
        apple = Item("Apple", "An edible green fruit that will boost your energy", 
                    pickable=True, consumable=True)
        potion = Item("Magic Potion", "Gives temporary immunity in battle", 
                     pickable=True, consumable=True)
        binocular = Item("Binocular", "Device to see super far", 
                        pickable=True, consumable=False)
        tree = Item("Tree", "A decorative tree", 
                   pickable=False, consumable=False)

        # Place items in locations
        self.locations["Playground"].add_item(tree)
        self.locations["Playground"].add_item(potion)
        self.locations["Beach"].add_item(apple)
        self.locations["School"].add_item(binocular)

        # Add items to master list
        self.items.extend([apple, potion, binocular, tree])

        return self.locations["School"]  # Return starting location


# In[9]:


import os

class Operation:
    """
    Controls game flow and user interface.
    
    Attributes:
        current_pymon (Pymon): Currently active Pymon
        record (Record): Game data manager
    """
    # def clear_console():
    #     """Clears the console output."""
    #     os.system('cls' if os.name == 'nt' else 'clear')
    
    def __init__(self):
        """Initialize game operation controller."""
        self.current_pymon = None
        self.record = Record()
    
    def start_game(self):
        """Initialize and start the game."""
        print("\nWelcome to Pymon World!")
        print("It's just you and your loyal Pymon roaming around to find more Pymons to capture and adopt.\n")
        
        # Create player's Pymon
        self.current_pymon = Pymon("Kimimon", "A white and yellow Pymon with a square face")
        
        # Set up initial game state
        starting_location = self.record.setup_pass_level()
        starting_location.add_creature(self.current_pymon)
        
        print(f"You started at {starting_location.name}")
        self.game_loop()
    
    def game_loop(self):
        """Main game loop with all features."""
        while True:
            try:
                choice = self.handle_menu()
                

                if choice == "1":
                    print(self.handle_inspect_pymon())
                    input("\nPress Enter to continue...")  # Add this
                elif choice == "2":
                    print(self.current_pymon.location.get_description())
                    input("\nPress Enter to continue...")  # Add this
                elif choice == "3":
                    self.handle_movement()
                elif choice == "4":
                    self.handle_item_pickup()
                elif choice == "5":
                    self.view_inventory()
                elif choice == "6":
                    self.handle_challenge()
                elif choice == "7":
                    self.current_pymon.generate_stats()
                elif choice == "8":
                    self.save_game()
                elif choice == "9":
                    self.load_game()
                elif choice == "10":
                    self.handle_admin_menu()
                elif choice == "11":
                    print("Thank you for playing!")
                    break
                else:
                    print("Invalid choice! Please try again.")
                    input("\nPress Enter to continue...")  # Add this

            except Exception as e:
                print(f"An error occurred: {str(e)}")
                input("\nPress Enter to continue...")
    
    def handle_menu(self):
        """Display menu with HD level options."""
        print("\nPlease issue a command to your Pymon:")
        print("1) Inspect Pymon")
        print("2) Inspect current location")
        print("3) Move")
        print("4) Pick an item")
        print("5) View inventory")
        print("6) Challenge a creature")
        print("7) Generate stats")
        print("8) Save game")
        print("9) Load game")
        print("10) Admin menu")
        print("11) Exit the program")
        return input("Enter your choice (1-11): ")
    
    def handle_admin_menu(self):
        """Handle admin features menu."""
        while True:
            print("\nAdmin Menu:")
            print("1) Add custom location")
            print("2) Add custom creature")
            print("3) Add custom item")
            print("4) Randomize location connections")
            print("5) Return to main menu")

            choice = input("Enter choice (1-5): ")

            if choice == "1":
                self.add_custom_location()
            elif choice == "2":
                self.add_custom_creature()
            elif choice == "3":
                self.add_custom_item()  # New option to add a custom item
            elif choice == "4":
                self.randomize_connections()
            elif choice == "5":
                break
            else:
                print("Invalid choice!")

    
    def handle_challenge(self):
        """Enhanced challenge handling with energy and immunity management."""
        location = self.current_pymon.location
        adoptable_creatures = [c for c in location.creatures if c.adoptable and c != self.current_pymon]

        if not adoptable_creatures:
            print("No creatures to challenge here!")
            return

        while True:
            try:
                print("\nAvailable creatures to challenge:")
                for i, creature in enumerate(adoptable_creatures, 1):
                    print(f"{i}) {creature.nickname}")

                choice = input("\nEnter creature number to challenge (or press Enter to cancel): ")

                if not choice:  # If the user presses enter without inputting a number
                    print("Cancelled.")
                    return

                if choice.isdigit() and 1 <= int(choice) <= len(adoptable_creatures):
                    target = adoptable_creatures[int(choice) - 1]
                    if self.current_pymon.challenge_creature(target):
                        print(f"\nVictory! {target.nickname} has been captured!")
                    else:
                        print("\nBattle lost!")
                        if self.current_pymon.energy <= 0:
                            self.current_pymon.random_move_after_loss()
                            if len(self.current_pymon.captured_pymons) > 0:
                                print("Switching to a captured Pymon...")
                                self.handle_pymon_switch()
                            else:
                                print("Game Over! No more Pymons available!")
                                exit()
                    break  # Exit the while loop after a challenge is done
                else:
                    print("Invalid choice! Please enter a valid creature number.")

            except Exception as e:
                print(f"An error occurred: {str(e)}")
                input("\nPress Enter to continue...")



    def handle_movement(self):
        """Enhanced movement handling with error checking."""
        try:
            print("\nAvailable directions:", end=" ")
            available = [dir for dir in self.current_pymon.location.doors 
                        if self.current_pymon.location.doors[dir]]
            print(", ".join(available) if available else "None")

            if not available:
                print("No available directions to move!")
                return

            direction = input("Enter direction to move: ").lower()
            if direction in available:
                if self.current_pymon.move(direction):
                    print(f"Moved to {self.current_pymon.location.name}")
            else:
                logging.error(f"Invalid direction: {direction}")
                print(f"Error: Invalid direction '{direction}'")
        except InvalidDirectionException as e:
            logging.error(f"Invalid direction: {e}")
            print(f"Error: {e}")
        except Exception as e:
            logging.error(f"Unexpected error during movement: {e}")
            print(f"An error occurred: {str(e)}")

    def handle_item_pickup(self):
        """Handle item pickup interaction."""
        # Check if there are any items at the current location
        available_items = [item for item in self.current_pymon.location.items if item.pickable]
        if not available_items:
            print("No items to pick up here!")
            return

        print("\nAvailable items:")
        for item in available_items:
            print(f"- {item.name}")

        item_name = input("\nEnter item name to pick up (or press Enter to cancel): ").strip()
        if item_name:
            # Try to find the item by name
            item_to_pickup = next((item for item in available_items if item.name.lower() == item_name.lower()), None)
            if item_to_pickup:
                # Add item to inventory and remove from location
                self.current_pymon.pick_item(item_to_pickup)
                self.current_pymon.location.items.remove(item_to_pickup)
                print(f"Picked up {item_name}!")
            else:
                print(f"No item named '{item_name}' found here.")
        else:
            print("Item pickup canceled.")
    
#     def view_inventory(self):
#         """Enhanced inventory view with item usage option."""
#         if not self.current_pymon.inventory:
#             print("Your inventory is empty!")
#             return
            
#         while True:
#             print("\nInventory:")
#             for i, item in enumerate(self.current_pymon.inventory, 1):
#                 print(f"{i}) {item.name}: {item.description}")
            
#             print("\nWhat would you like to do?")
#             print("1) Use an item")
#             print("2) Return to main menu")
            
#             choice = input("Enter choice (1-2): ")
            
#             if choice == "1":
#                 if not self.current_pymon.inventory:
#                     print("No items to use!")
#                     break
                    
#                 item_name = input("Enter the name of the item to use: ")
#                 self.current_pymon.use_item(item_name)
#             elif choice == "2":
#                 break
#             else:
#                 print("Invalid choice!")

    def view_inventory(self):
        """Enhanced inventory view with item usage option."""
        if not self.current_pymon.inventory:
            print("Your inventory is empty!")
            input("\nPress Enter to return to the main menu...")
            return

        while True:
            print("\nInventory:")
            for i, item in enumerate(self.current_pymon.inventory, 1):
                print(f"{i}) {item.name}: {item.description}")

            print("\nWhat would you like to do?")
            print("1) Use an item")
            print("2) Return to main menu")

            choice = input("Enter choice (1-2): ")

            if choice == "1":
                if not self.current_pymon.inventory:
                    print("No items to use!")
                    break

                item_name = input("Enter the name of the item to use: ")
                item_to_use = next((item for item in self.current_pymon.inventory if item.name == item_name), None)

                if item_to_use:
                    if item_name == "Binocular":
                        # Handle binocular usage
                        self.current_pymon._handle_binocular_use()
                    else:
                        self.current_pymon.use_item(item_name)

                    # Remove the item if it is consumable
                    if item_to_use.consumable:
                        try:
                            self.current_pymon.inventory.remove(item_to_use)
                            print(f"{item_name} has been used and removed from your inventory.")
                        except ValueError:
                            print(f"An error occurred while removing {item_name} from your inventory.")
                else:
                    print(f"No item named '{item_name}' found in inventory.")
            elif choice == "2":
                break
            else:
                print("Invalid choice!")

                
                
    def handle_pymon_switch(self):
        """Handle switching between captured Pymons."""
        if not self.current_pymon.captured_pymons:
            print("No captured Pymons available!")
            return
            
        print("\nCaptured Pymons:")
        for i, pymon in enumerate(self.current_pymon.captured_pymons):
        # Check if the captured creature is a Pymon and has energy attribute
            if isinstance(pymon, Pymon):
                print(f"{i+1}) {pymon.nickname} - Energy: {pymon.energy}/3")
            else:
                print(f"{i+1}) {pymon.nickname}")

        choice = input("\nEnter Pymon number to switch to (or press Enter to cancel): ")
        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(self.current_pymon.captured_pymons):
                new_pymon = self.current_pymon.captured_pymons[index]
                if isinstance(new_pymon, Pymon):
                    self.current_pymon = new_pymon
                    print(f"Switched to {new_pymon.nickname}!")
                else:
                    print(f"{new_pymon.nickname} is not a Pymon, cannot switch.")
            else:
                print("Invalid selection!") 
                
    def display_menu(self):
        """Display the main game menu."""
        print("\nPlease issue a command to your Pymon:")
        print("1) Inspect Pymon")
        print("2) Inspect current location")
        print("3) Move")
        print("4) Exit the program")
        
    def handle_inspect_pymon(self):
        """Handle Pymon inspection with switch option."""
        while True:
            print("1) Inspect current Pymon")
            print("2) List and select a captured Pymon")
            print("3) Back to main menu")
            
            choice = input("Enter choice (1-3): ")
            
            if choice == "1":
                print(self.current_pymon.get_description())
            elif choice == "2":
                self.handle_pymon_switch()
            elif choice == "3":
                break
            else:
                print("Invalid choice!")
     
    def add_custom_location(self):
        """Add new location and save to locations.csv."""
        print("\nAdd New Location:")
        name = input("Enter location name: ").strip()
        description = input("Enter location description: ").strip()

        # Create new location
        new_location = Location(name, description)
        self.record.locations[name] = new_location

        # Ask the user if they want to set connections now
        connect_now = input("Do you want to connect this location to existing ones now? (yes/no): ").strip().lower()
        if connect_now == 'yes':
            # Allow user to connect the new location to existing locations
            directions = ['west', 'north', 'east', 'south']
            for direction in directions:
                connect_name = input(f"Enter the name of the location to connect to the {direction} (or press Enter to skip): ").strip()

                if connect_name and connect_name in self.record.locations:
                    connected_location = self.record.locations[connect_name]
                    new_location.doors[direction] = connected_location
                    # Also set the opposite direction for the connected location if applicable
                    opposite_direction = self.get_opposite_direction(direction)
                    connected_location.doors[opposite_direction] = new_location
                elif connect_name:
                    print(f"Location '{connect_name}' not found. Skipping {direction} connection.")

        # Save to CSV
        self.save_locations_to_csv()

        print(f"Location '{name}' added successfully!")

    def get_opposite_direction(self, direction):
        """Helper function to get the opposite direction."""
        opposite = {
            'west': 'east',
            'east': 'west',
            'north': 'south',
            'south': 'north'
        }
        return opposite.get(direction)

    def save_locations_to_csv(self):
        """Save the current locations with connections to the CSV file."""
        with open('locations.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['name', 'description', 'west', 'north', 'east', 'south'])  # Header
            for location in self.record.locations.values():
                west = location.doors.get('west')
                north = location.doors.get('north')
                east = location.doors.get('east')
                south = location.doors.get('south')
                writer.writerow([
                    location.name, location.description,
                    west.name if west else 'None',
                    north.name if north else 'None',
                    east.name if east else 'None',
                    south.name if south else 'None'
                ])
                file.flush()
        print("Locations saved to locations.csv")
    
    
    
    
    def add_custom_item(self):
        """Add new item and save to items.csv."""
        print("\nAdd New Item:")
        name = input("Enter item name: ").strip()
        description = input("Enter item description: ").strip()
        pickable = input("Is this item pickable? (yes/no): ").strip().lower() == 'yes'
        consumable = input("Is this item consumable? (yes/no): ").strip().lower() == 'yes'

        # Create item
        item = Item(name, description, pickable, consumable)

        # Add item to in-memory list
        self.record.items.append(item)

        # Ask the user if they want to assign the item to a location
        assign_location = input("Do you want to assign this item to a location? (yes/no): ").strip().lower()
        if assign_location == 'yes':
            available_locations = list(self.record.locations.keys())
            print("\nAvailable Locations:")
            for idx, loc_name in enumerate(available_locations, start=1):
                print(f"{idx}) {loc_name}")

            location_choice = input("\nEnter the location number to assign this item (or press Enter to skip): ")
            if location_choice.isdigit() and 1 <= int(location_choice) <= len(available_locations):
                location_name = available_locations[int(location_choice) - 1]
                location = self.record.locations[location_name]
                location.add_item(item)
                print(f"Item '{item.name}' assigned to '{location_name}'.")
            else:
                print("No valid location selected. Item not assigned to any location.")

        # Save to CSV
        with open('items.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([name, description, 'yes' if pickable else 'no', 'yes' if consumable else 'no'])
            file.flush()
            
        print(f"Item '{name}' added successfully!")

    def add_custom_creature(self):
        """Add new creature and save to creatures.csv."""
        print("\nAdd New Creature:")
        name = input("Enter creature name: ")
        description = input("Enter creature description: ")
        is_pymon = input("Is this a Pymon? (yes/no): ").lower() == 'yes'

        # Create creature
        if is_pymon:
            creature = Pymon(name, description)
        else:
            creature = Creature(name, description, adoptable=False)

        # Add to in-memory creature list
        self.record.creatures.append(creature)

        # Ask the user if they want to assign a location to this creature
        assign_location = input("Do you want to assign this creature to a location? (yes/no): ").lower() == 'yes'
        if assign_location:
            available_locations = list(self.record.locations.keys())
            print("\nAvailable Locations:")
            for idx, loc_name in enumerate(available_locations, start=1):
                print(f"{idx}) {loc_name}")

            location_choice = input("\nEnter the location number to assign this creature (or press Enter to skip): ")
            if location_choice.isdigit() and 1 <= int(location_choice) <= len(available_locations):
                location_name = available_locations[int(location_choice) - 1]
                location = self.record.locations[location_name]
                location.add_creature(creature)
                print(f"Creature '{creature.nickname}' assigned to '{location_name}'.")
            else:
                print("No valid location selected. Creature not assigned to any location.")

        # Save to CSV
        with open('creatures.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([name, description, 'yes' if is_pymon else 'no'])
            file.flush()

        print(f"Creature '{name}' added successfully!")


        
    def randomize_connections(self):
        """Randomize connections between locations."""
        locations = list(self.record.locations.values())
        
        # Reset all connections
        for location in locations:
            for direction in ['west', 'north', 'east', 'south']:
                location.doors[direction] = None
        
        # Randomly connect locations
        for location in locations:
            available_directions = ['west', 'north', 'east', 'south']
            random.shuffle(available_directions)
            
            # Connect to 1-3 other locations
            num_connections = random.randint(1, min(3, len(locations)-1))
            
            for i in range(num_connections):
                direction = available_directions[i]
                available_locations = [loc for loc in locations 
                                    if loc != location and 
                                    not any(d for d in loc.doors.values() if d == location)]
                
                if available_locations:
                    target = random.choice(available_locations)
                    location.connect(direction, target)
        # Save the updated connections to CSV
        with open('locations.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['name', 'description', 'west', 'north', 'east', 'south'])  # Header
            for location in locations:
                west = location.doors.get('west')
                north = location.doors.get('north')
                east = location.doors.get('east')
                south = location.doors.get('south')

                writer.writerow([location.name, location.description,
                                 west.name if west else 'None',
                                 north.name if north else 'None',
                                 east.name if east else 'None',
                                 south.name if south else 'None'])
        print("Location connections randomized and saved!")
        
    
    def save_game(self, filename=None):
        """Save current game state to file."""
        if not filename:
            filename = input("Enter save file name (e.g., save2024.csv): ")

        try:
            with open(filename, 'w', newline='') as file:
                writer = csv.writer(file)

                # Save header
                writer.writerow(['Type', 'Data'])

                # Save current Pymon state
                if self.current_pymon:
                    writer.writerow(['CurrentPymon', self.current_pymon.nickname])
                    writer.writerow(['Energy', self.current_pymon.energy])
                    writer.writerow(['Location', self.current_pymon.location.name if self.current_pymon.location else 'Unknown'])
                else:
                    raise ValueError("Current Pymon is not defined.")

                # Save inventory with all attributes
                for item in self.current_pymon.inventory:
                    if hasattr(item, 'name') and hasattr(item, 'description'):
                        writer.writerow(['Inventory', f"{item.name},{item.description},{item.pickable},{item.consumable}"])
                    else:
                        raise ValueError("Item in inventory is missing required attributes.")

                # Save captured Pymons
                for pymon in self.current_pymon.captured_pymons:
                    if hasattr(pymon, 'nickname') and hasattr(pymon, 'description'):
                        writer.writerow(['CapturedPymon', f"{pymon.nickname},{pymon.description}"])
                    else:
                        raise ValueError("Captured Pymon is missing required attributes.")

                # Add battle history
                for battle in self.current_pymon.battle_history:
                    if hasattr(battle, 'timestamp') and hasattr(battle, 'opponent') and hasattr(battle, 'wins') and hasattr(battle, 'draws') and hasattr(battle, 'losses'):
                        writer.writerow(['Battle', f"{battle.timestamp},{battle.opponent},{battle.wins},{battle.draws},{battle.losses}"])
                    else:
                        raise ValueError("Battle record is missing required attributes.")

                # Save battle stats
                if 'wins' in self.current_pymon.battle_stats and 'losses' in self.current_pymon.battle_stats and 'draws' in self.current_pymon.battle_stats:
                    writer.writerow(['BattleStats', f"{self.current_pymon.battle_stats['wins']},{self.current_pymon.battle_stats['losses']},{self.current_pymon.battle_stats['draws']}"])
                else:
                    raise ValueError("Battle stats are missing required keys.")

            print(f"Game saved to {filename}!")

        except Exception as e:
            print(f"Error saving game: {str(e)}")

            
    def load_game(self, filename=None):
        """Load game state from file."""
        if not filename:
            filename = input("Enter save file name to load: ")

        try:
            with open(filename, 'r') as file:
                reader = csv.reader(file)
                header = next(reader)  # Skip header
                if header != ['Type', 'Data']:
                    raise ValueError("Invalid file format: Header does not match expected format.")
                
#                 # Clear current state before loading
#                 self.current_pymon.inventory.clear()
#                 self.current_pymon.captured_pymons.clear()
#                 self.current_pymon.battle_history.clear()
                for row in reader:
                    if len(row) != 2:
                        raise ValueError("Invalid file format: Each row must have exactly 2 columns.")

                    data_type, data = row

                    if data_type == 'CurrentPymon':
                        # Find and set current Pymon
                        found = False
                        for pymon in self.record.creatures:
                            if pymon.nickname == data:
                                self.current_pymon = pymon
                                found = True
                                break
                        if not found:
                            raise ValueError(f"Pymon '{data}' not found in records.")

                    elif data_type == 'Energy':
                        if not data.isdigit():
                            raise ValueError("Energy value must be an integer.")
                        self.current_pymon.energy = int(data)

                    elif data_type == 'Location':
                        if data in self.record.locations:
                            if self.current_pymon.location:
                                self.current_pymon.location.remove_creature(self.current_pymon)
                            self.record.locations[data].add_creature(self.current_pymon)
                        else:
                            raise ValueError(f"Location '{data}' not found in records.")

                    elif data_type == 'Inventory':
                        try:
                            # Updated to parse the full attributes for the item
                            name, description, pickable, consumable = data.split(',')
                            item = Item(
                                name=name,
                                description=description,
                                pickable=pickable.lower() == 'true',
                                consumable=consumable.lower() == 'true'
                            )
                            self.current_pymon.inventory.append(item)
                        except ValueError:
                            raise ValueError("Invalid inventory item format. Expected format: 'name,description,pickable,consumable'.")

                    elif data_type == 'CapturedPymon':
                        try:
                            name, desc = data.split(',')
                            pymon = Pymon(name, desc)
                            self.current_pymon.captured_pymons.append(pymon)
                        except ValueError:
                            raise ValueError("Invalid captured Pymon format.")

                    elif data_type == 'BattleStats':
                        try:
                            wins, losses, draws = map(int, data.split(','))
                            self.current_pymon.battle_stats = {
                                'wins': wins,
                                'losses': losses,
                                'draws': draws
                            }
                        except ValueError:
                            raise ValueError("Invalid battle stats format. Expected three integer values.")

                    elif data_type == 'Battle':
                        try:
                            timestamp, opponent, wins, draws, losses = data.split(',')
                            battle = BattleRecord(opponent, int(wins), int(draws), int(losses))
                            battle.timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
                            self.current_pymon.battle_history.append(battle)
                        except ValueError:
                            raise ValueError("Invalid battle record format.")

            print("Game loaded successfully!")

        except FileNotFoundError:
            print(f"Save file {filename} not found!")
        except ValueError as ve:
            print(f"Error loading game: {str(ve)}")
        except Exception as e:
            print(f"Unexpected error loading game: {str(e)}")


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




# Step 5: Switching Captured Pymons

        print("\nAttempting to switch to a captured Pymon...")
        
        # Switch to "Kitimon" which is at index 0 of the captured list
        new_pymon = pymon.switch_active_pymon(0)
        
        # Verify if switch was successful
        if new_pymon:
            print(f"\nSwitched to {new_pymon.nickname} successfully!")
        
            # Verify the attributes of the new active Pymon
            print("\nNew Active Pymon's Details:")
            print(new_pymon.get_description())
        
            # Try moving to test if everything works correctly after the switch
            direction_to_move = "north" if "north" in new_pymon.location.doors else "east"
            try:
                if new_pymon.move(direction_to_move):
                    print(f"\n{new_pymon.nickname} successfully moved {direction_to_move} to {new_pymon.location.name}.")
                else:
                    print(f"\n{new_pymon.nickname} failed to move {direction_to_move}.")
            except InvalidDirectionException as e:
                print(f"Error: {str(e)}")
        
        else:
            print("\nFailed to switch Pymon.")

# In[10]:


# import unittest
# import os
# import csv
# from datetime import datetime
# # from your_module_name import Operation, Pymon, Item, Creature, Location  # Import the required classes here

# class TestFileHandling(unittest.TestCase):

#     def setUp(self):
#         # Set up the operation instance and any required state
#         self.operation = Operation()
#         self.pymon = Pymon("TestMon", "A friendly Pymon")

#         # Set up creatures and locations for testing
#         self.operation.current_pymon = self.pymon
#         self.operation.record.creatures.append(self.pymon)  # Add TestMon to creatures

#         # Add a test location called "TestRoom"
#         test_location = Location("TestRoom", "A special room for testing purposes.")
#         self.operation.record.locations["TestRoom"] = test_location

#         # Set the current Pymon's location to TestRoom
#         self.pymon.location = test_location
#         test_location.add_creature(self.pymon)


#     def test_save_game(self):
#         """Test saving the game state to a CSV file."""
#         filename = "test_save.csv"
        
#         # Call save_game with a specified filename
#         self.operation.save_game(filename)

#         # Check if file was created
#         self.assertTrue(os.path.exists(filename), f"File {filename} should exist after saving the game.")

#         # Clean up
#         if os.path.exists(filename):
#             os.remove(filename)

#     def test_load_game(self):
#         """Test loading the game state from a CSV file."""
#         filename = "test_load.csv"
#         # Create a sample save file
#          # Ensure "TestMon" is in the creatures list before saving
# #         self.operation.record.creatures.append(self.pymon)
#         with open(filename, 'w', newline='') as f:
#             writer = csv.writer(f)
#             writer.writerow(['Type', 'Data'])
#             writer.writerow(['CurrentPymon', self.pymon.nickname])
#             writer.writerow(['Energy', 2])
#             writer.writerow(['Location', 'TestRoom'])
        
#         # Call load_game with a specified filename
#         self.operation.load_game(filename)

#         # Check if the loaded energy is correct
#         self.assertEqual(self.operation.current_pymon.energy, 2, "Loaded Pymon energy should be 2.")

#         # Clean up
#         if os.path.exists(filename):
#             os.remove(filename)

#     def test_inventory_save_load(self):
#         """Test saving and loading the inventory."""
#         filename = "test_inventory_save.csv"

#         # Add items to inventory
#         apple = Item("Apple", "An edible green fruit that will boost your energy")
#         apple.pickable = True
#         apple.consumable = True
#         self.operation.current_pymon.inventory.append(apple)

#         # Save the game state
#         self.operation.save_game(filename)

#         # Load the game state
#         self.operation.load_game(filename)

#         # Check if inventory is loaded correctly
#         self.assertEqual(len(self.operation.current_pymon.inventory), 1, "Inventory should contain one item after loading.")
#         loaded_item = self.operation.current_pymon.inventory[0]
#         self.assertEqual(loaded_item.name, "Apple", "Loaded item should be Apple.")
#         self.assertTrue(loaded_item.pickable, "Loaded item should be pickable.")
#         self.assertTrue(loaded_item.consumable, "Loaded item should be consumable.")

#         # Clean up
#         if os.path.exists(filename):
#             os.remove(filename)


#     def test_add_new_creature_and_save(self):
#         """Test adding a new creature and saving it to the CSV file."""
#         filename = "test_creatures.csv"
        
#         # Add a new creature
#         new_creature = Creature("FlameMon", "A fiery Pymon with blazing abilities")
#         self.operation.record.creatures.append(new_creature)

#         # Save creatures to the CSV file
#         with open(filename, 'w', newline='') as f:
#             writer = csv.writer(f)
#             writer.writerow(['Name', 'Description', 'Adoptable'])
#             for creature in self.operation.record.creatures:
#                 writer.writerow([creature.nickname, creature.description, 'yes' if creature.adoptable else 'no'])

#         # Verify if the new creature is in the file
#         found = False
#         with open(filename, 'r') as f:
#             reader = csv.reader(f)
#             next(reader)  # Skip header
#             for row in reader:
#                 if row[0] == "FlameMon":
#                     found = True
#                     break

#         self.assertTrue(found, "Newly added creature should be saved in the CSV file.")

#         # Clean up
#         if os.path.exists(filename):
#             os.remove(filename)

#     def test_add_new_location_and_save(self):
#         """Test adding a new location and saving it to the CSV file."""
#         filename = "test_locations.csv"
        
#         # Add a new location
#         new_location = Location("Mystic Valley", "A serene valley filled with mystical energy")
#         self.operation.record.locations[new_location.name] = new_location

#         # Save locations to the CSV file
#         with open(filename, 'w', newline='') as f:
#             writer = csv.writer(f)
#             writer.writerow(['Name', 'Description', 'North', 'South', 'East', 'West'])
#             for location in self.operation.record.locations.values():
#                 writer.writerow([location.name, location.description, 'None', 'None', 'None', 'None'])

#         # Verify if the new location is in the file
#         found = False
#         with open(filename, 'r') as f:
#             reader = csv.reader(f)
#             next(reader)  # Skip header
#             for row in reader:
#                 if row[0] == "Mystic Valley":
#                     found = True
#                     break

#         self.assertTrue(found, "Newly added location should be saved in the CSV file.")

#         # Clean up
#         if os.path.exists(filename):
#             os.remove(filename)

#     def test_add_new_item_and_save(self):
#         """Test adding a new item and saving it to the CSV file."""
#         filename = "test_items.csv"
        
#         # Add a new item
#         new_item = Item("Magic Wand", "A wand that sparkles with magic")
#         new_item.pickable = True
#         new_item.consumable = False
#         self.operation.record.items.append(new_item)

#         # Save items to the CSV file
#         with open(filename, 'w', newline='') as f:
#             writer = csv.writer(f)
#             writer.writerow(['Name', 'Description', 'Pickable', 'Consumable'])
#             for item in self.operation.record.items:
#                 writer.writerow([item.name, item.description, 'yes' if item.pickable else 'no', 'yes' if item.consumable else 'no'])

#         # Verify if the new item is in the file
#         found = False
#         with open(filename, 'r') as f:
#             reader = csv.reader(f)
#             next(reader)  # Skip header
#             for row in reader:
#                 if row[0] == "Magic Wand":
#                     found = True
#                     break

#         self.assertTrue(found, "Newly added item should be saved in the CSV file.")

#         # Clean up
#         if os.path.exists(filename):
#             os.remove(filename)

# if __name__ == "__main__":
#     unittest.main(argv=['first-arg-is-ignored'], exit=False, verbosity=2)


# In[11]:



# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-
# """
# RMIT University
# Programming Fundamentals - Assignment 3 
# Pymon Game Test Suite

# Test suite covering all levels (PASS, CREDIT, DI, HD) of the Pymon game implementation.
# Includes comprehensive testing of:
# - Location system and connections
# - Creature management and battles
# - Item system and inventory
# - Energy management
# - Save/Load functionality
# - Admin features
# """

# import unittest
# import os
# import csv
# from datetime import datetime
# import io
# from contextlib import redirect_stdout
# import sys

# class TestPymonGame(unittest.TestCase):
#     @classmethod
#     def setUpClass(cls):
#         """Create necessary test files before any tests run."""
#         cls.create_test_files()
#         print("\n=== Starting Pymon Game Test Suite ===")

#     def setUp(self):
#         """Set up test environment before each test."""
#         # Initialize output capture
#         self.test_output = io.StringIO()
        
#         # Initialize game operation
#         self.operation = Operation()
#         self.operation.record = Record()  # Ensure record is initialized
        
#         # Create test locations
#         self.school = Location("School", "A school building")
#         self.playground = Location("Playground", "A playground area")
#         self.beach = Location("Beach", "A beach area")
        
#         # Connect locations
#         self.school.connect("east", self.playground)
#         self.playground.connect("north", self.beach)
        
#         # Store locations in record
#         self.operation.record.locations = {
#             "School": self.school,
#             "Playground": self.playground,
#             "Beach": self.beach
#         }
        
#         # Create test Pymon
#         self.test_pymon = Pymon("TestMon", "A test Pymon")
        
#         # Set up current location
#         self.test_location = self.school  # Explicitly set test_location
#         self.test_location.add_creature(self.test_pymon)
#         self.test_pymon.location = self.test_location
        
#         # Set up operation's current Pymon
#         self.operation.current_pymon = self.test_pymon
        
#         # Initialize creatures list
#         self.operation.record.creatures = [self.test_pymon]
        
#         # Initialize items
#         self.operation.record.items = []


#     def test_pass_level(self):
#         """Test PASS level requirements."""
#         print("\n=== Testing PASS Level ===")
#         try:
#             # Test location setup
#             print("\nTesting location setup...")
#             required_locations = {'School', 'Playground', 'Beach'}
#             actual_locations = set(self.operation.record.locations.keys())
#             self.assertTrue(required_locations.issubset(actual_locations), 
#                           f"Missing required locations. Expected {required_locations}, got {actual_locations}")

#             # Test location connections
#             print("\nTesting location connections...")
#             self.assertEqual(self.school.doors["east"], self.playground,
#                            "School should connect to Playground on east")
#             self.assertEqual(self.playground.doors["west"], self.school,
#                            "Playground should connect to School on west")
#             self.assertEqual(self.playground.doors["north"], self.beach,
#                            "Playground should connect to Beach on north")

#             # Test basic movement
#             print("\nTesting basic movement...")
#             success = self.test_pymon.move("east")
#             self.assertTrue(success, "Movement to east should succeed")
#             self.assertEqual(self.test_pymon.location, self.playground,
#                            "Should move to Playground")

#             print("✓ PASS level tests completed successfully")

#         except AssertionError as e:
#             print(f"✗ PASS level test failed: {str(e)}")
#             raise
#         except Exception as e:
#             print(f"✗ Unexpected error in PASS level test: {str(e)}")
#             raise

#     def test_credit_level(self):
#         """Test CREDIT level requirements."""
#         print("\n=== Testing CREDIT Level ===")
#         try:
#             # Test item pickup
#             print("\nTesting item pickup...")
#             self.verify_location_setup()
#             # Create test item
#             apple = Item("Apple", "Test apple", True, True)
#             self.test_location.add_item(apple)  # Add to current location
            
#             # Capture output and attempt pickup
#             output = io.StringIO()
#             with redirect_stdout(output):
#                 success = self.test_pymon.pick_item("Apple")
            
#             self.assertTrue(success, "Failed to pick up Apple")
#             self.assertIn(apple, self.test_pymon.inventory, "Apple not in inventory after pickup")

#             # Test battle system
#             print("\nTesting battle system...")
#             opponent = Pymon("OpponentMon", "Test opponent")
#             self.test_location.add_creature(opponent)
            
#             # Mock battle round
#             original_battle = self.test_pymon._battle_round
#             self.test_pymon._battle_round = lambda target: 'win'
            
#             # Test battle
#             battle_result = self.test_pymon.challenge_creature(opponent)
#             self.assertTrue(battle_result, "Battle should be won with mocked win")
            
#             # Restore original battle method
#             self.test_pymon._battle_round = original_battle
#             success = self.test_pymon.pick_item("Apple")
#             self.verify_inventory("Apple")
#             print("✓ CREDIT level tests completed successfully")
            
#         except AssertionError as e:
#             print(f"✗ CREDIT level test failed: {str(e)}")
#             raise
#         except Exception as e:
#             print(f"✗ Unexpected error in CREDIT level test: {str(e)}")
#             raise


#     def test_di_level(self):
#         """Test DI level requirements."""
#         print("\n=== Testing DI Level ===")
#         try:
#             # Test energy management
#             print("\nTesting energy management...")
#             initial_energy = self.test_pymon.energy
            
#             # Verify current location and connections
#             self.assertEqual(self.test_pymon.location, self.test_location, 
#                            "Pymon should be in test location")
#             self.assertIsNotNone(self.test_pymon.location.doors["east"],
#                                "Test location should have east connection")
            
#             # Test movement and energy depletion
#             output = io.StringIO()
#             with redirect_stdout(output):
#                 self.test_pymon.moves_count = 1  # Setup for energy depletion
#                 success = self.test_pymon.move("east")
            
#             self.assertTrue(success, "Movement to east should succeed")
#             self.assertLess(self.test_pymon.energy, initial_energy,
#                            "Energy should decrease after moves")

#             # Test item usage
#             print("\nTesting item usage...")
#             apple = Item("Apple", "Test apple", True, True)
#             self.test_pymon.inventory.append(apple)
#             energy_before = self.test_pymon.energy
#             self.test_pymon.use_item("Apple")
#             self.assertGreater(self.test_pymon.energy, energy_before,
#                              "Energy should increase after using Apple")

#             print("✓ DI level tests completed successfully")
            
#         except AssertionError as e:
#             print(f"✗ DI level test failed: {str(e)}")
#             raise
#         except Exception as e:
#             print(f"✗ Unexpected error in DI level test: {str(e)}")
#             raise

#     def test_hd_level(self):
#         """Test HD level requirements."""
#         print("\n=== Testing HD Level ===")
#         try:
#             # Test save/load functionality
#             print("\nTesting save/load functionality...")
#             save_filename = "test_save.csv"
            
#             # Set initial state
#             self.test_pymon.energy = 2
#             original_location = self.test_pymon.location
            
#             # Save game state with complete data
#             with open(save_filename, 'w', newline='') as f:
#                 writer = csv.writer(f)
#                 writer.writerow(['Type', 'Data'])
#                 writer.writerow(['CurrentPymon', self.test_pymon.nickname])
#                 writer.writerow(['Energy', '2'])
#                 writer.writerow(['Location', self.test_pymon.location.name])
#                 writer.writerow(['BattleStats', '0,0,0'])
#                 # Save any inventory items
#                 for item in self.test_pymon.inventory:
#                     writer.writerow(['Inventory', f"{item.name},{item.description},{item.pickable},{item.consumable}"])
            
#             # Modify current state
#             self.test_pymon.energy = 1
            
#             # Load saved state
#             self.operation.load_game(save_filename)
            
#             # Verify state restoration
#             self.assertEqual(self.test_pymon.energy, 2,
#                            "Energy should be restored to saved value")
#             self.assertEqual(self.test_pymon.location, original_location,
#                            "Location should be restored to saved value")

#             # Test battle statistics
#             print("\nTesting battle statistics...")
#             test_battle = BattleRecord("TestOpponent", 2, 1, 1)
#             self.test_pymon.battle_history.append(test_battle)
            
#             with redirect_stdout(self.test_output):
#                 self.test_pymon.generate_stats()
#             output = self.test_output.getvalue()
#             self.assertIn("TestOpponent", output, "Battle statistics should show opponent")

#             print("✓ HD level tests completed successfully")

#         except AssertionError as e:
#             print(f"✗ HD level test failed: {str(e)}")
#             raise
#         except Exception as e:
#             print(f"✗ Unexpected error in HD level test: {str(e)}")
#             raise

#     @classmethod
#     def create_test_files(cls):
#         """Create required test files with proper content."""
#         # Create locations.csv
#         with open('locations.csv', 'w', newline='') as f:
#             writer = csv.writer(f)
#             writer.writerow(['name', 'description', 'west', 'north', 'east', 'south'])
#             writer.writerow(['School', 'A school building', 'None', 'None', 'Playground', 'None'])
#             writer.writerow(['Playground', 'A playground area', 'School', 'Beach', 'None', 'None'])
#             writer.writerow(['Beach', 'A sandy beach', 'None', 'None', 'None', 'Playground'])

#         # Create creatures.csv
#         with open('creatures.csv', 'w', newline='') as f:
#             writer = csv.writer(f)
#             writer.writerow(['name', 'description', 'adoptable'])
#             writer.writerow(['TestMon', 'A test Pymon', 'yes'])

#         # Create items.csv
#         with open('items.csv', 'w', newline='') as f:
#             writer = csv.writer(f)
#             writer.writerow(['name', 'description', 'pickable', 'consumable'])
#             writer.writerow(['Apple', 'Energy fruit', 'yes', 'yes'])
#             writer.writerow(['Magic Potion', 'Battle immunity', 'yes', 'yes'])
#             writer.writerow(['Binocular', 'View device', 'yes', 'no'])

#     def tearDown(self):
#         """Clean up after each test."""
#         test_files = ['test_save.csv']
#         for file in test_files:
#             if os.path.exists(file):
#                 os.remove(file)

#     @classmethod
#     def tearDown(self):
#         """Clean up after each test."""
#         # Close the StringIO object
#         self.test_output.close()
        
#         # Clean up test files
#         test_files = ['test_save.csv']
#         for file in test_files:
#             if os.path.exists(file):
#                 os.remove(file)
# def verify_location_setup(self):
#     """Verify location setup is correct."""
#     self.assertIsNotNone(self.test_location, "Test location should be initialized")
#     self.assertIsNotNone(self.test_pymon.location, "Pymon should have a location")
#     self.assertEqual(self.test_pymon.location, self.test_location, 
#                     "Pymon should be in test location")

# def verify_inventory(self, item_name):
#     """Verify item is in inventory."""
#     items = [item.name for item in self.test_pymon.inventory]
#     self.assertIn(item_name, items, f"{item_name} should be in inventory")

# def capture_output(self, func, *args, **kwargs):
#     """Capture output from a function call."""
#     output = io.StringIO()
#     with redirect_stdout(output):
#         result = func(*args, **kwargs)
#     return result, output.getvalue()

# def run_tests():
#     """Run the complete test suite."""
#     suite = unittest.TestLoader().loadTestsFromTestCase(TestPymonGame)
#     result = unittest.TextTestRunner(verbosity=2).run(suite)
    
#     print("\nTest Summary:")
#     print(f"Tests Run: {result.testsRun}")
#     print(f"Failures: {len(result.failures)}")
#     print(f"Errors: {len(result.errors)}")
    
#     return result.wasSuccessful()

# if __name__ == '__main__':
#     success = run_tests()
#     sys.exit(0 if success else 1)


# In[12]:


# if __name__ == '__main__':
#     success = run_tests()
#     print("\nTest Summary:")
#     if success:
#         print("✓ All tests passed successfully")
#     else:
#         print("✗ Some tests failed")


# In[13]:



# class TestPymonGame(unittest.TestCase):
#     def verify_location_setup(self):
#         """Helper method to verify location setup."""
#         self.assertIsNotNone(self.test_pymon.location, "Pymon should have a location")
#         self.assertEqual(self.test_pymon.location, self.school, 
#                         "Pymon should be in school location")

#     def verify_inventory(self, item_name):
#         """Helper method to verify inventory contents."""
#         items = [item.name for item in self.test_pymon.inventory]
#         self.assertIn(item_name, items, f"{item_name} should be in inventory")

#     @classmethod
#     def setUpClass(cls):
#         """Set up test files and initial data."""
#         # Create test CSV files
#         with open('locations.csv', 'w', newline='') as f:
#             writer = csv.writer(f)
#             writer.writerow(['name', 'description', 'west', 'north', 'east', 'south'])
#             writer.writerow(['School', 'A school building', 'None', 'None', 'Playground', 'None'])
#             writer.writerow(['Playground', 'A playground area', 'School', 'Beach', 'None', 'None'])
#             writer.writerow(['Beach', 'A sandy beach', 'None', 'None', 'None', 'Playground'])

#         with open('creatures.csv', 'w', newline='') as f:
#             writer = csv.writer(f)
#             writer.writerow(['name', 'description', 'adoptable'])
#             writer.writerow(['TestMon', 'A test Pymon', 'yes'])

#         with open('items.csv', 'w', newline='') as f:
#             writer = csv.writer(f)
#             writer.writerow(['name', 'description', 'pickable', 'consumable'])
#             writer.writerow(['Apple', 'Energy fruit', 'yes', 'yes'])
#             writer.writerow(['Magic Potion', 'Battle immunity', 'yes', 'yes'])

#         print("\n=== Starting Pymon Game Test Suite ===")

#     def setUp(self):
#         """Set up test environment before each test."""
#         # Initialize base objects
#         self.operation = Operation()
#         self.operation.record = Record()
#         self.operation.record.import_location()  # Load locations from CSV
        
#         # Set up test locations
#         self.school = self.operation.record.locations["School"]
#         self.playground = self.operation.record.locations["Playground"]
#         self.beach = self.operation.record.locations["Beach"]
        
#         # Create test Pymon
#         self.test_pymon = Pymon("TestMon", "A test Pymon")
#         self.school.add_creature(self.test_pymon)
#         self.test_pymon.location = self.school
#         self.operation.current_pymon = self.test_pymon
        
#         # Add Pymon to record's creatures
#         self.operation.record.creatures.append(self.test_pymon)
        
#         # Initialize output capture
#         self.output = io.StringIO()

#     def test_credit_level(self):
#         """Test CREDIT level requirements."""
#         print("\n=== Testing CREDIT Level ===")
        
#         # Verify initial setup
#         self.verify_location_setup()
        
#         # Test item pickup
#         apple = Item("Apple", "Test apple", True, True)
#         self.school.add_item(apple)
        
#         with redirect_stdout(self.output):
#             success = self.test_pymon.pick_item("Apple")
        
#         self.assertTrue(success)
#         self.verify_inventory("Apple")
        
#         # Test battle system
#         opponent = Pymon("OpponentMon", "Test opponent")
#         self.school.add_creature(opponent)
        
#         # Mock battle round
#         def mock_battle_round(target):
#             return 'win'
        
#         original_battle = self.test_pymon._battle_round
#         self.test_pymon._battle_round = mock_battle_round
        
#         battle_result = self.test_pymon.challenge_creature(opponent)
#         self.assertTrue(battle_result)
        
#         self.test_pymon._battle_round = original_battle
        
#         print("✓ CREDIT level tests completed successfully")

#     def test_di_level(self):
#         """Test DI level requirements."""
#         print("\n=== Testing DI Level ===")
        
#         # Test energy management
#         initial_energy = self.test_pymon.energy
#         self.test_pymon.moves_count = 1
        
#         with redirect_stdout(self.output):
#             self.test_pymon.move("east")
        
#         self.assertLess(self.test_pymon.energy, initial_energy)
        
#         # Test item usage
#         apple = Item("Apple", "Test apple", True, True)
#         self.test_pymon.inventory.append(apple)
        
#         energy_before = self.test_pymon.energy
#         self.test_pymon.use_item("Apple")
#         self.assertGreater(self.test_pymon.energy, energy_before)
        
#         print("✓ DI level tests completed successfully")

#     def test_hd_level(self):
#         """Test HD level requirements."""
#         print("\n=== Testing HD Level ===")
        
#         # Test save/load
#         save_filename = "test_save.csv"
#         self.test_pymon.energy = 2
        
#         # Create save file
#         with open(save_filename, 'w', newline='') as f:
#             writer = csv.writer(f)
#             writer.writerow(['Type', 'Data'])
#             writer.writerow(['CurrentPymon', self.test_pymon.nickname])
#             writer.writerow(['Energy', '2'])
#             writer.writerow(['Location', self.test_pymon.location.name])
#             writer.writerow(['BattleStats', '0,0,0'])
        
#         # Change state and load
#         self.test_pymon.energy = 1
#         self.operation.load_game(save_filename)
        
#         self.assertEqual(self.test_pymon.energy, 2)
        
#         # Test battle statistics
#         battle = BattleRecord("TestOpponent", 2, 1, 1)
#         self.test_pymon.battle_history.append(battle)
        
#         with redirect_stdout(self.output):
#             self.test_pymon.generate_stats()
            
#         stats_output = self.output.getvalue()
#         self.assertIn("TestOpponent", stats_output)
        
#         print("✓ HD level tests completed successfully")

#     def tearDown(self):
#         """Clean up test environment after each test."""
#         # Close output capture if it exists
#         if hasattr(self, 'output'):
#             self.output.close()
        
#         # Clean up any test files created during the test
#         if os.path.exists("test_save.csv"):
#             os.remove("test_save.csv")

#     @classmethod
#     def tearDownClass(cls):
#         """Clean up test files after all tests."""
#         test_files = ['locations.csv', 'creatures.csv', 'items.csv']
#         for file in test_files:
#             if os.path.exists(file):
#                 os.remove(file)
#         print("\n=== Pymon Game Test Suite Completed ===")

# # Helper function to run and display test results
# def run_and_display_test(test_name):
#     # Create a separator line
#     print("="*50)
#     print(f"Running {test_name}")
#     print("-"*50)
    
#     # Run the test
#     test = TestPymonGame(test_name)
#     test.setUp()
    
#     try:
#         # Capture output
#         with redirect_stdout(io.StringIO()) as output:
#             getattr(test, test_name)()
        
#         print(f"✓ {test_name} completed successfully!")
#         print("\nTest Output:")
#         print(output.getvalue())
        
#     except Exception as e:
#         print(f"✗ {test_name} failed:")
#         print(f"Error: {str(e)}")
#         import traceback
#         print("\nTraceback:")
#         print(traceback.format_exc())
        
#     finally:
#         test.tearDown()
    
#     print("="*50 + "\n")

#     # Run all tests with nice formatting
#     test_names = [
#         'test_pass_level',
#         'test_credit_level',
#         'test_di_level',
#         'test_hd_level'
#     ]

#     for test_name in test_names:
#         run_and_display_test(test_name)


# In[14]:


# run_and_display_test("TestPymonGame")


# In[15]:


# if __name__ == '__main__':
#     success = run_tests()
#     print("\nTest Summary:")
#     if success:
#         print("✓ All tests passed successfully")
#     else:
#         print("✗ Some tests failed")


# In[16]:


# import unittest
# import os
# import csv
# from datetime import datetime
# import io
# from contextlib import redirect_stdout
# import sys


# In[17]:


# # Create test files
# def create_test_files():
#     with open('locations.csv', 'w', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow(['name', 'description', 'west', 'north', 'east', 'south'])
#         writer.writerow(['School', 'A school building', 'None', 'None', 'Playground', 'None'])
#         writer.writerow(['Playground', 'A playground area', 'School', 'Beach', 'None', 'None'])
#         writer.writerow(['Beach', 'A sandy beach', 'None', 'None', 'None', 'Playground'])

#     with open('creatures.csv', 'w', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow(['name', 'description', 'adoptable'])
#         writer.writerow(['TestMon', 'A test Pymon', 'yes'])

#     with open('items.csv', 'w', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow(['name', 'description', 'pickable', 'consumable'])
#         writer.writerow(['Apple', 'Energy fruit', 'yes', 'yes'])
#         writer.writerow(['Magic Potion', 'Battle immunity', 'yes', 'yes'])

# create_test_files()


# In[18]:


# def run_single_test(test_name):
#     """Run a single test with detailed output."""
#     print(f"\n{'='*60}")
#     print(f"Running {test_name}")
#     print(f"{'-'*60}")
    
#     test = TestPymonGame(test_name)
#     test.setUp()
#     try:
#         getattr(test, test_name)()
#         print(f"\n✓ {test_name} passed successfully!")
#     except Exception as e:
#         print(f"\n✗ {test_name} failed:")
#         print(f"Error: {str(e)}")
#         import traceback
#         print("\nTraceback:")
#         print(traceback.format_exc())
#     finally:
#         test.tearDown()
#     print(f"{'='*60}\n")

# # Run all tests
# test_names = [
#     'test_pass_level',
#     'test_credit_level',
#     'test_di_level',
#     'test_hd_level'
# ]

# for test_name in test_names:
#     run_single_test(test_name)


# In[19]:


# class TestPymonGame(unittest.TestCase):
#     def verify_location_setup(self):
#         """Helper method to verify location setup."""
#         self.assertIsNotNone(self.test_pymon.location, "Pymon should have a location")
#         self.assertEqual(self.test_pymon.location, self.school, 
#                         "Pymon should be in school location")

#     def verify_inventory(self, item_name):
#         """Helper method to verify inventory contents."""
#         items = [item.name for item in self.test_pymon.inventory]
#         self.assertIn(item_name, items, f"{item_name} should be in inventory")

#     def setUp(self):
#         """Set up test environment before each test."""
#         # Initialize base objects
#         self.operation = Operation()
#         self.operation.record = Record()
#         self.operation.record.import_location()  # Load locations from CSV
        
#         # Set up test locations
#         self.school = self.operation.record.locations["School"]
#         self.playground = self.operation.record.locations["Playground"]
#         self.beach = self.operation.record.locations["Beach"]
        
#         # Create test Pymon
#         self.test_pymon = Pymon("TestMon", "A test Pymon")
#         self.school.add_creature(self.test_pymon)
#         self.test_pymon.location = self.school
#         self.operation.current_pymon = self.test_pymon
        
#         # Add Pymon to record's creatures
#         self.operation.record.creatures.append(self.test_pymon)
        
#         # Initialize output capture
#         self.output = io.StringIO()

#     def test_pass_level(self):
#         """Test PASS level requirements."""
#         print("\n=== Testing PASS Level ===")
        
#         # Test location connections
#         self.assertIsNotNone(self.school.doors["east"])
#         self.assertEqual(self.school.doors["east"], self.playground)
#         self.assertEqual(self.playground.doors["west"], self.school)
        
#         # Test basic movement
#         initial_location = self.test_pymon.location
#         self.test_pymon.move("east")
#         self.assertNotEqual(self.test_pymon.location, initial_location)
#         self.assertEqual(self.test_pymon.location, self.playground)
        
#         print("✓ PASS level tests completed successfully")

#     def test_credit_level(self):
#         """Test CREDIT level requirements."""
#         print("\n=== Testing CREDIT Level ===")
        
#         # Verify initial setup
#         self.verify_location_setup()
        
#         # Test item pickup
#         apple = Item("Apple", "Test apple", True, True)
#         self.school.add_item(apple)
        
#         with redirect_stdout(self.output):
#             success = self.test_pymon.pick_item("Apple")
        
#         self.assertTrue(success)
#         self.verify_inventory("Apple")
        
#         # Test battle system
#         opponent = Pymon("OpponentMon", "Test opponent")
#         self.school.add_creature(opponent)
        
#         # Mock battle round
#         def mock_battle_round(target):
#             return 'win'
        
#         original_battle = self.test_pymon._battle_round
#         self.test_pymon._battle_round = mock_battle_round
        
#         battle_result = self.test_pymon.challenge_creature(opponent)
#         self.assertTrue(battle_result)
        
#         self.test_pymon._battle_round = original_battle
        
#         print("✓ CREDIT level tests completed successfully")

#     def test_di_level(self):
#         """Test DI level requirements."""
#         print("\n=== Testing DI Level ===")
        
#         # Test energy management
#         initial_energy = self.test_pymon.energy
#         self.test_pymon.moves_count = 1
        
#         with redirect_stdout(self.output):
#             self.test_pymon.move("east")
        
#         self.assertLess(self.test_pymon.energy, initial_energy)
        
#         # Test item usage
#         apple = Item("Apple", "Test apple", True, True)
#         self.test_pymon.inventory.append(apple)
        
#         energy_before = self.test_pymon.energy
#         self.test_pymon.use_item("Apple")
#         self.assertGreater(self.test_pymon.energy, energy_before)
        
#         print("✓ DI level tests completed successfully")

#     def test_hd_level(self):
#         """Test HD level requirements."""
#         print("\n=== Testing HD Level ===")
        
#         # Test save/load
#         save_filename = "test_save.csv"
#         self.test_pymon.energy = 2
        
#         # Create save file
#         with open(save_filename, 'w', newline='') as f:
#             writer = csv.writer(f)
#             writer.writerow(['Type', 'Data'])
#             writer.writerow(['CurrentPymon', self.test_pymon.nickname])
#             writer.writerow(['Energy', '2'])
#             writer.writerow(['Location', self.test_pymon.location.name])
#             writer.writerow(['BattleStats', '0,0,0'])
        
#         # Change state and load
#         self.test_pymon.energy = 1
#         self.operation.load_game(save_filename)
        
#         self.assertEqual(self.test_pymon.energy, 2)
        
#         # Test battle statistics
#         battle = BattleRecord("TestOpponent", 2, 1, 1)
#         self.test_pymon.battle_history.append(battle)
        
#         with redirect_stdout(self.output):
#             self.test_pymon.generate_stats()
            
#         stats_output = self.output.getvalue()
#         self.assertIn("TestOpponent", stats_output)
        
#         print("✓ HD level tests completed successfully")

#     def tearDown(self):
#         """Clean up test environment after each test."""
#         if hasattr(self, 'output'):
#             self.output.close()
        
#         if os.path.exists("test_save.csv"):
#             os.remove("test_save.csv")


# In[20]:



# def main():
#     """Main function to run the Pymon game."""
#     try:
#         print("\n" + "="*50)
#         print("Welcome to Pymon World!")
#         print("="*50 + "\n")

#         # Initialize game operation
#         operation = Operation()

#         # Process command line arguments if provided
#         if len(sys.argv) > 1:
#             # Load files based on provided arguments
#             if len(sys.argv) >= 2:
#                 operation.record.load_locations(sys.argv[1])
#             if len(sys.argv) >= 3:
#                 operation.record.load_creatures(sys.argv[2])
#             if len(sys.argv) >= 4:
#                 operation.record.load_items(sys.argv[3])
#         else:
#             # Use default filenames
#             operation.record.load_data()

#         # Start the game
#         operation.start_game()

#         # Main game loop
#         while True:
#             try:
#                 choice = operation.handle_menu()

#                 if choice == "1":  # Inspect Pymon
#                     operation.handle_inspect_pymon()
#                 elif choice == "2":  # Inspect current location
#                     print(operation.current_pymon.location.get_description())
#                 elif choice == "3":  # Move
#                     operation.handle_movement()
#                 elif choice == "4":  # Pick an item
#                     operation.handle_item_pickup()
#                 elif choice == "5":  # View inventory
#                     operation.view_inventory()
#                 elif choice == "6":  # Challenge a creature
#                     operation.handle_challenge()
#                 elif choice == "7":  # Generate stats
#                     operation.current_pymon.generate_stats()
#                 elif choice == "8":  # Save game
#                     operation.save_game()
#                 elif choice == "9":  # Load game
#                     operation.load_game()
#                 elif choice == "10":  # Admin menu
#                     operation.handle_admin_menu()
#                 elif choice == "11":  # Exit
#                     print("\nThank you for playing Pymon!")
#                     break
#                 else:
#                     print("\nInvalid choice! Please try again.")

#                 input("\nPress Enter to continue...")

#             except InvalidDirectionException as e:
#                 print(f"\nError: {str(e)}")
#                 input("\nPress Enter to continue...")
#             except Exception as e:
#                 print(f"\nAn error occurred: {str(e)}")
#                 input("\nPress Enter to continue...")

#     except FileNotFoundError as e:
#         print(f"\nError: Required file not found - {e.filename}")
#         print("Please ensure all required files are present.")
#     except InvalidInputFileFormat as e:
#         print(f"\nError: Invalid file format - {e.message}")
#     except Exception as e:
#         print(f"\nUnexpected error occurred: {str(e)}")
#     finally:
#         print("\nGame session ended.")

# def print_help():
#     """Print help information about command line usage."""
#     print("\nPymon Game Usage:")
#     print("1. Basic usage:")
#     print("   python pymon_game.py")
#     print("\n2. With custom files:")
#     print("   python pymon_game.py locations.csv")
#     print("   python pymon_game.py locations.csv creatures.csv")
#     print("   python pymon_game.py locations.csv creatures.csv items.csv")
#     print("\nDefault files used if not specified:")
#     print("- locations.csv")
#     print("- creatures.csv")
#     print("- items.csv")

# if __name__ == "__main__":
#     # Check if help is requested
#     if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
#         print_help()
#     else:
#         try:
#             main()
#         except KeyboardInterrupt:
#             print("\n\nGame interrupted by user.")
#         except Exception as e:
#             print(f"\nCritical error occurred: {str(e)}")
#             print("Please report this error to the developers.")
#         finally:
#             print("\nThank you for playing Pymon!")


# In[21]:



# def create_initial_files():
#     """Create initial CSV files with proper formatting."""
    
#     # Create locations.csv
#     try:
#         with open('locations.csv', 'w', newline='') as f:
#             writer = csv.writer(f)
#             writer.writerow(['name', 'description', 'west', 'north', 'east', 'south'])
#             writer.writerow(['School', 'A school building', 'None', 'None', 'Playground', 'None'])
#             writer.writerow(['Playground', 'A playground area', 'School', 'Beach', 'None', 'None'])
#             writer.writerow(['Beach', 'A sandy beach', 'None', 'None', 'None', 'Playground'])

#         # Create creatures.csv
#         with open('creatures.csv', 'w', newline='') as f:
#             writer = csv.writer(f)
#             writer.writerow(['name', 'description', 'adoptable'])
#             writer.writerow(['Kitimon', 'large blue and white Pymon with yellow fangs', 'yes'])
#             writer.writerow(['Sheep', 'small fluffy animal with interesting curly white fur', 'no'])
#             writer.writerow(['Marimon', 'medium red and yellow Pymon with a cute round face', 'yes'])

#         # Create items.csv
#         with open('items.csv', 'w', newline='') as f:
#             writer = csv.writer(f)
#             writer.writerow(['name', 'description', 'pickable', 'consumable'])
#             writer.writerow(['Apple', 'An edible green fruit that will boost your energy', 'yes', 'yes'])
#             writer.writerow(['Magic Potion', 'Gives temporary immunity in battle', 'yes', 'yes'])
#             writer.writerow(['Binocular', 'Device to see super far', 'yes', 'no'])
#             writer.writerow(['Tree', 'A decorative tree', 'no', 'no'])

#         return True

#     except Exception as e:
#         print(f"Error creating initial files: {str(e)}")
#         return False

# def main():
#     """Main function to run the Pymon game."""
#     try:
#         print("\n" + "="*50)
#         print("Welcome to Pymon World!")
#         print("="*50 + "\n")

#         # Create initial files if they don't exist
#         if not all(os.path.exists(f) for f in ['locations.csv', 'creatures.csv', 'items.csv']):
#             if not create_initial_files():
#                 print("Failed to create necessary files. Exiting...")
#                 return

#         # Initialize game operation
#         operation = Operation()
#         operation.record = Record()  # Ensure record is initialized

#         # Load game data
#         try:
#             if len(sys.argv) > 1:
#                 # Load files based on provided arguments
#                 if len(sys.argv) >= 2:
#                     operation.record.load_locations(sys.argv[1])
#                 if len(sys.argv) >= 3:
#                     operation.record.load_creatures(sys.argv[2])
#                 if len(sys.argv) >= 4:
#                     operation.record.load_items(sys.argv[3])
#             else:
#                 # Use default setup
#                 operation.record.import_location()
#                 operation.record.import_creatures()
#                 operation.record.import_items()
#         except Exception as e:
#             print(f"Error loading game data: {str(e)}")
#             return

#         # Create and set up initial Pymon
#         starting_pymon = Pymon("Kimimon", "A white and yellow Pymon with a square face")
#         starting_location = operation.record.locations.get("School")
#         if starting_location:
#             starting_location.add_creature(starting_pymon)
#             starting_pymon.location = starting_location
#             operation.current_pymon = starting_pymon
#         else:
#             print("Error: Could not find starting location.")
#             return

#         # Main game loop
#         while True:
#             try:
#                 choice = operation.handle_menu()

#                 if choice == "1":  # Inspect Pymon
#                     print(operation.handle_inspect_pymon())
#                 elif choice == "2":  # Inspect current location
#                     print(operation.current_pymon.location.get_description())
#                 elif choice == "3":  # Move
#                     operation.handle_movement()
#                 elif choice == "4":  # Pick an item
#                     operation.handle_item_pickup()
#                 elif choice == "5":  # View inventory
#                     operation.view_inventory()
#                 elif choice == "6":  # Challenge a creature
#                     operation.handle_challenge()
#                 elif choice == "7":  # Generate stats
#                     operation.current_pymon.generate_stats()
#                 elif choice == "8":  # Save game
#                     operation.save_game()
#                 elif choice == "9":  # Load game
#                     operation.load_game()
#                 elif choice == "10":  # Admin menu
#                     operation.handle_admin_menu()
#                 elif choice == "11":  # Exit
#                     print("\nThank you for playing Pymon!")
#                     break
#                 else:
#                     print("\nInvalid choice! Please try again.")

#                 input("\nPress Enter to continue...")

#             except InvalidDirectionException as e:
#                 print(f"\nError: {str(e)}")
#                 input("\nPress Enter to continue...")
#             except Exception as e:
#                 print(f"\nAn error occurred: {str(e)}")
#                 input("\nPress Enter to continue...")

#     except Exception as e:
#         print(f"\nUnexpected error occurred: {str(e)}")
#     finally:
#         print("\nGame session ended.")

# if __name__ == "__main__":
#     try:
#         main()
#     except KeyboardInterrupt:
#         print("\n\nGame interrupted by user.")
#     except Exception as e:
#         print(f"\nCritical error occurred: {str(e)}")
#     finally:
#         print("\nThank you for playing Pymon!")




def main():
    try:
        operation = Operation()
        operation.start_game()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()



