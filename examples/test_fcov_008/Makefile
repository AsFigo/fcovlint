# ----------------------------------------------------
# SPDX-FileCopyrightText: AsFigo Technologies, UK
# SPDX-FileCopyrightText: VerifWorks, India
# SPDX-License-Identifier: MIT
# ----------------------------------------------------

FCOVLINT = python3 ../../bin/fcovlint.py

all: run_f run_ap run_bp

run_f:
	$(FCOVLINT) -t test_fcov_008_f.sv

run_ap:
	$(FCOVLINT) -t test_fcov_008a_p.sv
run_bp:
	$(FCOVLINT) -t test_fcov_008b_p.sv
