# 🟡 Pac-Man AI Project

A Python-based AI-powered Pac-Man game built as part of our semester project. This implementation includes intelligent ghost behavior (scatter, chase, return), a reactive AI using a greedy strategy, and a visually engaging interface to showcase classic gameplay with modern AI features.

---

## 📋 Table of Contents

- [Introduction](#introduction)
- [Project Files](#project-files)
- [How to Run](#how-to-run)
- [Demo](#demo)
- [Report](#report)
- [Project Proposal](#project-proposal)
- [AI Features](#ai-features)
- [Conclusion](#conclusion)

---

## 📖 Introduction

Pac-Man is a classic arcade game where the player navigates a maze, collecting pellets and avoiding ghosts. In this project, we bring Pac-Man to life using Python with advanced AI behavior for the ghost enemies. The ghosts act based on different strategies such as chasing the player, scattering to corners, returning after being eaten, and adapting to player actions through a reactive greedy approach.

---

## 📁 Project Files

| File/Folder           | Description |
|----------------------|-------------|
| `pacman.py`            | Main game logic and loop |
| `images/`            | Game assets (images, sounds) |
| `board.py`          | Maze layout in text format |
| `report.pdf`         | Project report |
| `proposal.pdf`       | Original project proposal |
| `README.md`          | This documentation file |

---

## ▶️ How to Run

```bash
python pacman.py
```

---

## 🎥 Demo
Click the link below to view a live demo of the game in action:

[View Project DEMO](https://drive.google.com/file/d/1K67UA8EQrCGK6gAvClez6dvMH8G959AK/view?usp=sharing)

---

## 📑 Report
Download the final report here:

---

## 📝 Project Proposal
View our original proposal here:
[View Project Proposal](https://docs.google.com/document/d/14RaQcEfyaPpi5PNuj5qPtyg9m3B_3g9P/edit?usp=drive_link&ouid=100827600261452189958&rtpof=true&sd=true)

---

## 🧠 AI Features
Our ghost AI is inspired by the behavior patterns in the original Pac-Man game, enhanced with modern techniques:

**Scatter Mode**: Each ghost retreats when powerups are enabled.

**Chase Mode**: Ghosts track Pac-Man using a greedy pathfinding strategy.

**Return Mode**: Ghosts return to the ghost house after being eaten.

**Reactive AI**: Ghosts change behavior based on Pac-Man's current direction, location and enviroment.

**Greedy Approach**: Ghosts make immediate best choices rather than planning ahead.

**Different Ghost Behaviors**: Each ghost may follow different strategies — one chases directly, another predicts movement, and one may block paths.

---

## 🏁 Conclusion
This project demonstrates how traditional game mechanics can be enhanced using AI techniques. We combined search-based strategies and state-driven behavior models to simulate intelligent and reactive enemy agents. The final result is a fun, challenging, and technically enriched recreation of Pac-Man.















