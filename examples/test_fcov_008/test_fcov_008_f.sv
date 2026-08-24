// ----------------------------------------------------
// SPDX-FileCopyrightText: AsFigo Technologies, UK
// SPDX-FileCopyrightText: VerifWorks, India
// SPDX-License-Identifier: MIT
// ----------------------------------------------------
module fcov008_bad;

  logic a;
  logic b;
  covergroup ab;  // violation: no cg_ prefix or _cg suffix
    option.per_instance = 1;
    cp_a : coverpoint a;
    cp_b : coverpoint b;
  endgroup : ab           

  ab cg_inst = new();

endmodule