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
