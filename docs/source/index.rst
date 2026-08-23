FCOVLint — SystemVerilog Functional Coverage Linter
====================================================

**FCOVLint** is an open-source linter for SystemVerilog functional coverage
constructs, developed by `AsFigo Technologies <https://asfigo.com>`_ as part
of the **BYOL** (Build Your Own Linter) framework.

It enforces Verilator-compatible coverage coding practices — covering
covergroup structure, bin definitions, cross coverage, sampling events, and
coverage options — helping verification teams ship simulation-ready coverage
models from day one.

.. code-block:: bash

   python bin/fcovlint.py -t <your_file.sv>

----

.. toctree::
   :maxdepth: 2
   :caption: Rule Reference

   rules
