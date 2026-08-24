// ----------------------------------------------------
// SPDX-FileCopyrightText: AsFigo Technologies, UK
// SPDX-FileCopyrightText: VerifWorks, India
// SPDX-License-Identifier: MIT
// ----------------------------------------------------

module fcov008_good;

  logic a;
  logic b;
  covergroup cg_ab; // compliant: has cg_ prefix 
    option.per_instance = 1;
    cp_a : coverpoint a;
    cp_b : coverpoint b;
  endgroup : cg_ab            

  cg_ab cg_inst = new();

endmodule