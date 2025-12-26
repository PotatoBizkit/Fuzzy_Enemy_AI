# Fuzzy_Enemy_AI

This repository presents Python implementations of **adaptive enemy AI systems for video games**, comparing a **fuzzy logic–based dynamic difficulty adjustment (DDA)** approach with a **PPO (Proximal Policy Optimization) reinforcement learning agent** in a controlled 2D survival game environment.

The work accompanies an IEEE conference study on adaptive enemy behavior.

---

## Overview

The repository demonstrates two distinct approaches for enemy AI:

### 1. Fuzzy Logic–Based Enemy AI
- Rule-based inference system using fuzzy logic
- Dynamically adjusts enemy tracking speed and damage
- Uses player survival time and inferred player skill level
- Emphasizes explainability and interpretability

### 2. PPO-Based Enemy AI
- Reinforcement learning agent trained using Stable-Baselines3
- Controls enemy movement decisions at runtime
- Integrated with fuzzy logic for adaptive damage calculation
- Demonstrates learning-based behavior with hybrid decision logic

Both approaches are implemented in a **Pygame-based 2D survival game**.

---

## Repository Structure

    ├── fuzzy_enemy_game.py # Fuzzy logic–controlled enemy AI
    ├── ppo_game_enemy.py # PPO-controlled enemy AI with fuzzy damage
    ├── requirements.txt # Python dependencies
    └── README.md

---

## Fuzzy Logic Enemy AI

**File:** `fuzzy_enemy_game.py`

Features:
- Fuzzy inference system built using `scikit-fuzzy`
- Inputs:
  - Remaining survival time
  - Player progression level
- Outputs:
  - Enemy tracking speed
  - Enemy damage
- Demonstrates adaptive difficulty scaling through interpretable rules

---

## PPO-Based Enemy AI

**File:** `ppo_game_enemy.py`

Features:
- PPO agent for enemy movement control
- Observation space based on relative player–enemy position
- Deterministic inference during gameplay
- Fuzzy logic–based damage calculation enhanced with distance-based scaling

> **Note:** The trained PPO model (`enemy_ai_ppo.zip`) must be present in the project directory to run this script.

---

## Installation

Create a virtual environment and install the required dependencies:

    pip install -r requirements.txt

Main dependencies include:

- pygame

- numpy

- scikit-fuzzy

- stable-baselines3

---

## Running the Demos

### Fuzzy Logic–Based Enemy AI

    python fuzzy_enemy_game.py

### PPO-Based Enemy AI

    python ppo_game_enemy.py

### Controls

- W / A / S / D – Player movement

- Survive for 60 seconds to win

---

## Research Context

This repository supports research on:

- Adaptive enemy AI

- Dynamic difficulty adjustment (DDA)

- Explainable AI in games

- Hybrid rule-based and reinforcement learning systems

The work was presented at 17th IEEE International Conference on Computational Intelligence and Communication Networks (CICN 2025).

---

## License

This project is licensed under the MIT License.
See the LICENSE file for details.
