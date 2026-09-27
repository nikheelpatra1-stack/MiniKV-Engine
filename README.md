# ⚡ MiniKV — Lightweight In-Memory Key-Value Database Engine

> A minimalist, persistent, in-memory key-value storage engine built from scratch using pure Python. Built for the **E-Cell SRMIST Technical Domain Trial**.

---

## 📌 Overview

**MiniKV** is a high-speed key-value store built to demonstrate fundamental backend systems design: socket programming, protocol parsing, memory management, and file-based persistence. 

Inspired by the *Build Your Own Database / Redis* module in `build-your-own-x`, MiniKV wraps an in-memory Hash Table in a non-blocking TCP server, providing instant reads and writes while ensuring data safety via automated JSON disk snapshots.

---

## ✨ Key Features

- **In-Memory Speed:** $O(1)$ hash map lookups and writes for maximum throughput.
- **TCP Socket Server:** Native TCP listener on port `6379`, compatible with `netcat` (`nc`), `telnet`, or custom socket clients.
- **Automated JSON Snapshotting:** Automatically flushes state updates to `db_snapshot.json` on write operations (`SET`, `DEL`), ensuring crash recovery upon reboot.
- **Real-Time Telemetry & Metrics:** Built-in `STATS` engine tracking server uptime, active keys, query volumes, and operation breakdowns.
- **Zero External Dependencies:** Built entirely with the standard Python library (`socket`, `json`, `time`, `os`).

---

## 🏗️ System Architecture
┌─────────────────────────────────────────────────────────┐
│                    Client (nc / telnet)                 │
└────────────────────────────┬────────────────────────────┘
│  (TCP Socket Commands)
v
┌─────────────────────────────────────────────────────────┐
│                MiniKV TCP Listener Engine               │
│                     (Port 6379)                         │
└──────────────┬───────────────────────────┬──────────────┘
│                           │
v                           v
┌───────────────────────────┐ ┌───────────────────────────┐
│     In-Memory Store       │ │    Persistence Engine     │
│   (Python Hash Table)     │ │   (db_snapshot.json)      │
└───────────────────────────┘ └───────────────────────────┘
---

## 🛠️ Supported Commands

| Command | Syntax | Description | Example |
| :--- | :--- | :--- | :--- |
| **`SET`** | `SET <key> <value>` | Stores a key-value pair and triggers disk sync | `SET user:101 "Alex"` |
| **`GET`** | `GET <key>` | Retrieves the value of a key | `GET user:101` |
| **`DEL`** | `DEL <key>` | Deletes a key from memory and updates disk | `DEL user:101` |
| **`KEYS`** | `KEYS` | Lists all active keys currently stored | `KEYS` |
| **`STATS`** | `STATS` | Displays real-time server telemetry and uptime | `STATS` |

---

## 🚀 Quickstart Guide

### Prerequisite
- Python 3.8+ installed on your system.

### 1. Clone the Repository
```bash
git clone https://github.com/nikheelpatra1-stack/MiniKV-Engine.git
cd MiniKV-Engine
