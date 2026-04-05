# 🚗 Scriptiverse FiveM Toolkit

![Python Version](https://img.shields.io/badge/Python-3.x-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Platform: FiveM](https://img.shields.io/badge/Platform-FiveM-orange.svg)

An advanced, automated development suite designed to eliminate the tedious manual labor of creating FiveM vehicle packs. 

Whether you are combining hundreds of add-on cars, balancing server economies, or trying to track down a crash-inducing duplicate `<modelName>`, the Scriptiverse FiveM Toolkit handles it in seconds.

---

## 📖 The Origin Story

What started as a simple, personal Python script to extract FiveM spawn codes quickly snowballed into something much bigger. 

As a server developer, the most frustrating part of building a car pack wasn't downloading the cars. It was the hours spent balancing the economy, writing SQL files, and hunting down the one duplicate `.meta` tag that was crashing the server. This toolkit was built out of pure necessity to automate those headaches. Today, it serves as the foundational open-source tool for the **Scriptiverse** development brand.

---

## ✨ Core Features

### 1. 🧬 Spawn Code & Profile Generator
* Scans all subdirectories to find `vehicles.meta` files.
* Automatically extracts and formats spawn codes into `.lua` or `.txt`.
* **Handling Extraction:** Optionally parses `handling.meta` to build a mini-performance profile for each car, calculating top speed (KM/H), vehicle mass (kg), drive bias (AWD/RWD/FWD), and gears.

### 2. 💰 Smart SQL Economy Builder
* Generates a ready-to-import `.sql` file for QBCore or ESX databases.
* **Smart Pricing Algorithm:** Instead of a flat price, the toolkit reads the vehicle's top speed and drive type to automatically place it into an economy tier (Utility, Daily, Sports, Supercar, Hypercar).
* Automatically rounds prices to the nearest $1,000 for a clean in-game vehicle shop display.

### 3. 🛠️ Intelligent Duplicate Auto-Fixer
* Server crashing on startup? The toolkit scans every meta file to find conflicting duplicate spawn codes and tells you exactly which folders are fighting.
* **Intelligent Auto-Rename:** Safely rewrites XML tags inside your `.meta` files and physically renames the conflicting `.yft` and `.ytd` files in your stream folders by appending `_fix`.

### 4. 📜 vMenu Addon Generator
* Instantly converts your entire car pack into a perfectly formatted `addons.json` file.
* Just copy and paste the output directly into your server's `vMenu/config/addons.json`.

---

## 🗺️ Future Roadmap

The **Scriptiverse FiveM Toolkit** is continuously evolving. Below is the master plan for where this project is heading.

> **Status Key:** ✅ Completed  |  🚧 In Progress  |  📅 Planned

---

### ✅ Phase 1: The Core Engine *(We are here)*
**Status: Released (v1.0)**
* Built the standalone, open-source Python tool for local PC automation.
* Advanced duplicate fixing, handling data extraction, and smart economy generation.

### 🚧 Phase 2: The Web Dashboard (SaaS)
**Status: In Development**
* Transitioning this toolkit into a fully-fledged **Web Application**. 
* No more terminals. Simply upload your vehicle folders to a clean, modern web interface and run these tools directly in your browser.

### 📅 Phase 3: Live Server Sync
**Status: Planned**
* Developing a standalone FiveM Lua resource.
* Connects your live game server directly to the Scriptiverse web dashboard for real-time economy updates and instant spawn code synchronization without restarting your server.

---

## 📁 Installation & Setup

1. Download or clone this repository to your computer.
2. Ensure you have [Python 3.x](https://www.python.org/downloads/) installed.
3. Place your FiveM vehicle folders either in the same directory as the script, or configure a custom target path.
4. Run `main.py`.

---

## ⚙️ How to Use

The toolkit features three distinct execution modes depending on your workflow:

### Interactive Mode (Default)
Simply double-click `main.py` or run it in your terminal. The script will safely pre-scan your directories, report how many meta files were found, and guide you through an interactive menu.

### Fast Mode (Headless)
For power users doing repetitive tasks. Open `config.py` and set `FAST_MODE = True`. Ensure your `DEFAULT_MODULE` is selected. The script will execute instantly without any Y/N prompts.

### Developer Auto-Test
Set `AUTO_TEST = True` in the config to run a headless batch test of all modules at once. It generates a clean, timestamped output folder containing all generated `.lua`, `.sql`, and `.json` files for review.

---

## 🔧 Configuration (`config.py`)

You can fully customize the toolkit's behavior by editing the `config.py` file:
* `TARGET_DIRECTORY`: Hardcode a specific folder to scan (leave blank to scan the current directory).
* `OUTPUT_DIRECTORY`: Hardcode where generated files are saved.
* `OUTPUT_FORMAT`: Choose between `".lua"` or `".txt"`.
* `SMART_PRICING`: Toggle dynamic economy generation on or off.

---

## 📜 License
Distributed under the MIT License. See `LICENSE` for more information.

---
### 🛠️ Maintained & Developed by **Scriptiverse** > *Automating the Metaverse*
