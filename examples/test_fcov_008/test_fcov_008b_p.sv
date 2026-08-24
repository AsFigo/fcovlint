// ----------------------------------------------------
// SPDX-FileCopyrightText: AsFigo Technologies, UK
// SPDX-FileCopyrightText: VerifWorks, India
// SPDX-License-Identifier: MIT
// ----------------------------------------------------

module fcov008_good;

  logic a;
  logic b;
  covergroup ab_cg; // compliant: has _cg suffix 
    option.per_instance = 1;
    cp_a : coverpoint a;
    cp_b : coverpoint b;
  endgroup : ab_cg            

  ab_cg cg_inst = new();

endmodule