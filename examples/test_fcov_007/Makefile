# ----------------------------------------------------
# SPDX-FileCopyrightText: AsFigo Technologies, UK
# SPDX-FileCopyrightText: VerifWorks, India
# SPDX-License-Identifier: MIT
# ----------------------------------------------------

FCOVLINT = python3 ../../bin/fcovlint.py

all: run_f run_p

run_f:
	$(FCOVLINT) -t test_fcov_007_f.sv

run_p:
	$(FCOVLINT) -t test_fcov_007_p.sv
