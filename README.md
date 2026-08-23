# FCOVLint

**FCOVLint** is an open-source, minimalist linter designed to enforce compatibility, functionality, performance, and style consistency rules for SystemVerilog Functional Coverage (`covergroup`, `coverpoint`, `cross`).

Built on the philosophy of **BYOL** (**Build Your Own Linter**), FCOVLint demonstrates how verification engineers can roll out custom static analysis rules using Python and Google's [Verible](https://github.com/chipsalliance/verible) parser.

---

## Table of Contents

1. [BYOL - Build Your Own Linter](#byol---build-your-own-linter)
2. [Documentation](#documentation)
3. [Directory Structure](#directory-structure)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Adding New Lint Rules](#adding-new-lint-rules)
7. [Dependencies](#dependencies)
8. [License](#license)
9. [Credits](#credits)

---
## BYOL - Build Your Own Linter

The core concept of **FCOVLint** is **BYOL**, a framework that lets you easily define custom linting rules tailored to your team's SystemVerilog coverage standards. Whether enforcing `option.per_instance = 1`, preventing non-consecutive repetitions, or flagging Verilator-unsupported coverage constructs, FCOVLint is lightweight and easily extensible.

---

## Documentation

Full rule reference and API documentation are hosted on GitHub Pages:
👉 **[FCOVLint Documentation](https://asfigo.github.io/fcovlint/)**

---

## Directory Structure

```text
FCOVLint/
├── bin/
│   ├── fcovlint.py                   # Main executable CLI
│   └── verible_verilog_syntax.py     # Verible Python bindings
├── docs/                             # Sphinx documentation source
├── examples/                         # Example pass/fail SV files
│   ├── Makefile
│   ├── test_fcov_007_f.sv            # Violation example
│   └── test_fcov_007_p.sv            # Compliant example
└── src/
    ├── af_lint_rule.py               # Base rule class (AsFigoLintRule)
    ├── asfigo_linter.py              # Core linter engine
    └── rules/                        # Functional coverage rules
        └── af_fcov_*.py

## Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/AsFigo/fcovlint.git](https://github.com/AsFigo/fcovlint.git)
   cd fcovlint
   ```

2. **Install Verible Parser:**
   FCOVLint requires Google's Verible parser binary (`verible-verilog-syntax`) in your executable path. Download it from the [Verible Releases](https://github.com/chipsalliance/verible/releases).

3. **Install Python dependencies:**
   ```bash
   pip install anytree tomli
   pip install -r docs/requirements.txt
   ```

---

## Usage

Run the linter against a SystemVerilog target file from your project root:

```bash
python3 bin/fcovlint.py -t examples/test_fcov_007_f.sv
```

---

## Adding New Lint Rules

1. Create a new Python file inside `src/rules/` starting with `af_fcov_` (e.g., `af_fcov_my_rule.py`).
2. Class structure should inherit from `AsFigoLintRule`:

```python
from af_lint_rule import AsFigoLintRule

class MyCustomRule(AsFigoLintRule):
    """AF_FCOV_CUSTOM_001: Description of your custom rule."""
    
    def apply(self, filePath: str, data):
        # Rule check logic using Verible AST data
        pass
```

3. Add a corresponding entry in `docs/source/rules.rst` documenting the rule rationale, violation example, correct usage, and severity.

---

## Dependencies

* **Python**: 3.8+
* **Verible Parser**: [`verible-verilog-syntax`](https://github.com/chipsalliance/verible) executable
* **Python Packages**: `anytree`, `tomli`, `sphinx`, `furo` (for docs)

---

## License

This project is open-source and licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## Credits

* **Verible**: Open-source SystemVerilog parser maintained by Google & [ChipsAlliance](https://github.com/chipsalliance/verible).
* **AsFigo Technologies**: Created as part of the AsFigo BYOL initiative.

