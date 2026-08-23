// ----------------------------------------------------
// SPDX-FileCopyrightText: AsFigo Technologies, UK
// SPDX-FileCopyrightText: VerifWorks, India
// SPDX-License-Identifier: MIT
// ----------------------------------------------------

module fcov007_bad;

  logic [1:0] addr;
  logic [1:0] data;

  covergroup cg;
    option.per_instance = 1;
    cp_addr : coverpoint addr;

    // VIOLATION: 'data' is referenced directly in the cross
    // instead of using a declared coverpoint.
    cross_addr_data : cross cp_addr, data {
      option.cross_auto_bin_max = 64;
    }

  endgroup : cg

  cg cg_inst = new();

endmodule
