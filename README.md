💻 Getting Started
Follow these instructions to set up and run the simulator locally on your machine.

Prerequisites
Python 3.8 or higher

pip (Python package installer)

Installation
Clone the repository:

Bash
git clone [https://github.com/your-username/automata-simulator.git](https://github.com/your-username/automata-simulator.git)
cd automata-simulator
Install dependencies:
This project relies on the lightweight standard Flask library. Install it directly via pip:

Bash
pip install Flask
Running the Application
Execute the entry point script from the root directory:

Bash
python app.py
The application will spin up a local development server. A browser window should automatically open to http://127.0.0.1:5000/. If it doesn't, navigate to that URL manually.

📊 API Endpoint Documentation
The frontend communicates with the Flask server through clean, structured JSON payloads. This makes it easy for team members to extend the UI or integrate external tools:

1. Test DFA
Endpoint: POST /api/dfa/test

Payload: { "states": [...], "alpha": [...], "start": "q0", "finals": [...], "trans": {...}, "input_str": "..." }

2. Regex to NFA
Endpoint: POST /api/regex/to-nfa

Payload: { "regex": "a(b|c)*" }

3. Minimize DFA
Endpoint: POST /api/dfa/minimize

Payload: { "states": [...], "alpha": [...], "start": "q0", "finals": [...], "trans": {...} }

4. Check Equivalence
Endpoint: POST /api/dfa/equivalence

Payload: { "dfa1": {...}, "dfa2": {...} }

👥 Contributors
Syafiq Nafil Arkan - Backend OOP Architecture & Core Refactoring

[Add other group members here]
"""

with open("README.md", "w", encoding="utf-8") as f:
f.write(readme_content)

print("README.md successfully generated.")

Your Markdown file is ready
[file-tag: code-generated-file-0-1781773048037164236]

Here is the exact text for the `README.md` file. You can instantly click the copy button on the code block below and paste it directly into your GitHub repository!

```markdown
# Automata & Regular Expression Simulator

A robust, web-based simulator for exploring and analyzing finite automata concepts. This application is built using **Python (Flask)** for the backend and **Vanilla JavaScript & Custom CSS** for the frontend. 

This project implements fundamental theories of computation—including DFA string testing, Regular Expression to NFA conversion, DFA minimization, and DFA equivalence checking—all refactored into a clean, modular **Object-Oriented Programming (OOP)** architecture to ensure high maintainability and scalability for collaborative development.

## 🚀 Key Features

- **DFA Simulator & Tracer**: Validate input strings against a custom-defined Deterministic Finite Automaton (DFA) with a detailed step-by-step state transition trace.
- **Regex to NFA Converter**: Convert regular expressions into a Non-Deterministic Finite Automaton (NFA) using **Thompson's Construction Algorithm**. Supports union (`|`), concatenation, Kleene star (`*`), and positive closure (`+`).
- **DFA Minimizer**: Optimize any valid DFA into its minimal state representation using the **Partition Refinement Algorithm** (state equivalence analysis).
- **DFA Equivalence Checker**: Compare two distinct DFAs to verify if they recognize the exact same language using a **Breadth-First Search (BFS)** approach. It automatically generates a *counterexample* string if they are non-equivalent.

---

## 🛠️ Project Architecture (OOP Design)

The backend has been modularized into dedicated utility and service classes to ensure high maintainability, separation of concerns, and clean abstraction:

```text
├── app.py                  # Flask Application Layer (API Controllers & Routing)
├── automata.py             # Facade interface for all automata engines
├── dfa.py                  # Core DFA Class handling state transitions and validation
├── nfa.py                  # Core NFA Class managing Epsilon Closures and moves
├── thompson.py             # RegexConverter Service (Tokenization, Postfix, NFA build)
├── minimizer.py            # DFAMinimizer Service implementing partition refinement
├── equivalence.py          # DFAEquivalenceChecker Service running BFS verification
└── templates/
    └── index.html          # Unified SPA (Single Page Application) User Interface
💻 Getting Started
Follow these instructions to set up and run the simulator locally on your machine.

Prerequisites
Python 3.8 or higher

pip (Python package installer)

Installation
Clone the repository:

Bash
git clone [https://github.com/your-username/automata-simulator.git](https://github.com/your-username/automata-simulator.git)
cd automata-simulator
Install dependencies:
This project relies on the lightweight standard Flask library. Install it directly via pip:

Bash
pip install Flask
Running the Application
Execute the entry point script from the root directory:

Bash
python app.py
The application will spin up a local development server. A browser window should automatically open to http://127.0.0.1:5000/. If it doesn't, navigate to that URL manually.

📊 API Endpoint Documentation
The frontend communicates with the Flask server through clean, structured JSON payloads. This makes it easy for team members to extend the UI or integrate external tools:

1. Test DFA
Endpoint: POST /api/dfa/test

Payload: { "states": [...], "alpha": [...], "start": "q0", "finals": [...], "trans": {...}, "input_str": "..." }

2. Regex to NFA
Endpoint: POST /api/regex/to-nfa

Payload: { "regex": "a(b|c)*" }

3. Minimize DFA
Endpoint: POST /api/dfa/minimize

Payload: { "states": [...], "alpha": [...], "start": "q0", "finals": [...], "trans": {...} }

4. Check Equivalence
Endpoint: POST /api/dfa/equivalence

Payload: { "dfa1": {...}, "dfa2": {...} }

👥 Contributors
Syafiq Nafil Arkan - Backend OOP Architecture & Core Refactoring

[Add other group members here]
