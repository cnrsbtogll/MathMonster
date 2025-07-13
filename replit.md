# Matematik Canavarı - Turkish Children's Math Game

## Overview

This is a terminal-based educational math game designed for Turkish-speaking children. The game presents progressive difficulty math problems and tracks the player's score while providing an engaging, emoji-rich interface.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Application Type
- **Platform**: Terminal/Console-based Python application
- **Target Audience**: Turkish-speaking children
- **Interface**: Command-line interface with Turkish text and emoji decorations
- **Execution Model**: Single-threaded, interactive game loop

### Programming Language & Framework
- **Language**: Python 3
- **Dependencies**: Built-in Python standard library only (random, sys, os)
- **Architecture Pattern**: Object-oriented design with single class structure

## Key Components

### Core Game Class: `MatematikCanavari`
- **Purpose**: Main game controller handling all game logic and user interaction
- **State Management**: 
  - Player score tracking (`self.skor`)
  - Difficulty progression (`self.zorluk_seviyesi`)
  - Available math operations (`self.operasyonlar`)

### Key Methods
1. **Screen Management**: `temizle_ekran()` - Cross-platform screen clearing
2. **User Interface**: `hosgeldin_mesaji()` - Welcome screen with game rules
3. **Game Logic**: `sayi_uret()` - Dynamic number generation based on difficulty

### Difficulty Progression System
- **Level 1-3**: Easy (numbers 1-10)
- **Level 4-6**: Medium (numbers 1-25) 
- **Level 7-10**: Hard (numbers 1-50)
- **Progressive Scaling**: Difficulty increases with correct answers

## Data Flow

### Game Session Flow
1. **Initialization**: Create game instance with default values
2. **Welcome Phase**: Display rules and wait for user input
3. **Question Generation**: Create math problems based on current difficulty
4. **Answer Validation**: Check user responses and update score
5. **Difficulty Adjustment**: Increase complexity after correct answers
6. **Game Termination**: End game on incorrect answer

### State Transitions
- Score increments with each correct answer
- Difficulty level increases periodically
- Game resets on completion or error

## External Dependencies

### System Dependencies
- **Operating System**: Cross-platform support (Windows/Unix-like systems)
- **Python Runtime**: Python 3.x required
- **Terminal**: Any standard terminal/command prompt

### Standard Library Usage
- `random`: For generating random numbers and operations
- `sys`: For system-level operations
- `os`: For cross-platform screen clearing

## Deployment Strategy

### Distribution Method
- **Format**: Single Python script file
- **Installation**: No installation required - direct script execution
- **Portability**: Fully portable across Python-supported platforms

### Execution Requirements
- Python 3 interpreter
- Terminal/console access
- UTF-8 support for Turkish characters and emojis

### File Structure
```
matematik_canavari.py    # Main application file (standalone)
```

### Running the Application
```bash
python3 matematik_canavari.py
```

## Technical Decisions

### Language Choice: Python
- **Rationale**: Simple syntax suitable for educational projects
- **Benefits**: Cross-platform, readable code, minimal setup
- **Trade-offs**: Requires Python runtime installation

### Terminal Interface
- **Rationale**: Lightweight, focuses attention on math content
- **Benefits**: No GUI framework dependencies, universal compatibility
- **Trade-offs**: Limited visual appeal compared to graphical interfaces

### Progressive Difficulty
- **Rationale**: Maintains engagement while building skills
- **Implementation**: Difficulty-based number range scaling
- **Benefits**: Adaptive learning experience

### Turkish Localization
- **Rationale**: Native language support for target audience
- **Implementation**: All text, messages, and instructions in Turkish
- **Benefits**: Better comprehension and engagement for Turkish children