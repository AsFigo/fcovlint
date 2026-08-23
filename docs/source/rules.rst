Lint Rules
==========

.. _AF_FCOV_ARRAY_BIN_LIMIT_VLT:

AF_FCOV_ARRAY_BIN_LIMIT_VLT
---------------------------

Array-based coverpoint bin expansion must not exceed 1024 bins.

**Rationale**: When ``bins b[] = {[low:high]}`` is used, the simulator
creates one named bin per value in the range. Very large ranges (> 1024)
cause significant memory overhead and slow down coverage collection.
Keeping the number of expanded bins within 1024 ensures manageable
simulation performance and coverage database size.

**Violation**::

    covergroup cg;
      option.per_instance = 1;
      cp_a : coverpoint a {
        bins b[] = {[0:65535]};  // expands to 65536 bins -- violation
      }
    endgroup : cg

**Correct usage**::

    covergroup cg;
      option.per_instance = 1;
      cp_a : coverpoint a {
        bins b[] = {[0:15]};  // expands to 16 bins -- compliant
      }
    endgroup : cg

**Severity**: ERROR

----

.. _AF_FCOV_CLASS_MEM_REF_VLT:

AF_FCOV_CLASS_MEM_REF_VLT
-------------------------

Coverpoints must not directly reference member variables of the enclosing class.

**Rationale**: Verilator does not support coverpoints that reference member
variables of the class that contains the covergroup. The reference is
resolved through the implicit ``this`` pointer, which Verilator cannot
handle in the coverage context. Pass the variable as a covergroup argument
instead, or reference a non-member signal from the enclosing scope.

**Violation**::

    class env;
      int data;
      covergroup cg;
        option.per_instance = 1;
        cp : coverpoint data;  // references class member 'data' -- violation
      endgroup : cg
    endclass

**Correct usage**::

    int data;           // module-level variable
    covergroup cg;
      option.per_instance = 1;
      cp : coverpoint data;  // references module-level 'data' -- compliant
    endgroup : cg

**Severity**: ERROR

----

.. _AF_FCOV_CONST_OPT_VLT:

AF_FCOV_CONST_OPT_VLT
---------------------

``option.at_least`` and ``option.auto_bin_max`` must be assigned constant integer values.

**Rationale**: Verilator evaluates covergroup options at elaboration time.
Assigning a runtime variable to ``option.at_least`` or
``option.auto_bin_max`` prevents Verilator from resolving the option value
and causes a compilation error or silent misbehaviour. Using literal integer
constants guarantees correct elaboration across all simulators.

**Violation**::

    covergroup cg;
      option.per_instance = 1;
      option.at_least     = threshold;         // variable -- violation
      option.auto_bin_max = threshold + 5;     // expression -- violation
      cp_a : coverpoint a;
    endgroup : cg

**Correct usage**::

    covergroup cg;
      option.per_instance = 1;
      option.at_least     = 10;   // constant -- compliant
      option.auto_bin_max = 64;   // constant -- compliant
      cp_a : coverpoint a;
    endgroup : cg

**Severity**: ERROR

----

.. _AF_FCOV_CROSS_USE_CP_VLT:

AF_FCOV_CROSS_USE_CP_VLT
------------------------

Every item in a cross must be an explicitly declared coverpoint name.

**Rationale**: Verilator requires each item in a ``cross`` statement to refer
to an explicitly declared coverpoint, not a raw variable or signal name. A
raw variable reference causes Verilator to silently ignore the cross or emit
a compilation error, producing incomplete coverage data without any clear
warning to the engineer.

**Violation**::

    covergroup cg;
      option.per_instance = 1;
      cp_addr : coverpoint addr;
      cross_addr_data : cross cp_addr, data;  // 'data' is not a coverpoint -- violation
    endgroup : cg

**Correct usage**::

    covergroup cg;
      option.per_instance = 1;
      cp_addr : coverpoint addr;
      cp_data : coverpoint data;
      cross_addr_data : cross cp_addr, cp_data;  // both are coverpoints -- compliant
    endgroup : cg

**Severity**: ERROR

----

.. _AF_FCOV_INTF_IN_MOD_VLT:

AF_FCOV_INTF_IN_MOD_VLT
-----------------------

Interface declarations must not be nested inside module declarations.

**Rationale**: The SystemVerilog standard permits interfaces to be declared
at the global scope or inside packages, but not nested inside module bodies.
Verilator rejects nested interface declarations with a parse error. Moving
the interface definition to the global scope ensures portability across
simulators and tools.

**Violation**::

    module top;
      interface my_intf;  // nested inside module -- violation
        logic req;
        logic ack;
      endinterface
    endmodule

**Correct usage**::

    interface my_intf;  // declared at global scope -- compliant
      logic req;
      logic ack;
    endinterface

    module top;
      my_intf intf_inst();
    endmodule

**Severity**: ERROR

----

.. _AF_FCOV_CR_ABIN_MAX_IN_CROSS_VLT:

AF_FCOV_CR_ABIN_MAX_IN_CROSS_VLT
--------------------------------

``option.cross_auto_bin_max`` must not appear inside a cross coverage specification.

**Rationale**: Verilator does not recognise ``option.cross_auto_bin_max``
inside a ``cross`` body. Using it causes a compilation error or silent
coverage loss. To limit cross bin growth under Verilator, reduce the number
of coverpoints or manually define ``bins`` entries. For non-Verilator flows
that do support the option, use rule ``AF_FCOV_PERF_USE_CR_ABIN_MAX`` to
enforce its presence instead.

**Violation**::

    covergroup cg;
      option.per_instance = 1;
      cp_a : coverpoint a;
      cp_b : coverpoint b;
      x_ab : cross cp_a, cp_b {
        option.cross_auto_bin_max = 16;  // unsupported by Verilator -- violation
      }
    endgroup : cg

**Correct usage**::

    covergroup cg;
      option.per_instance = 1;
      cp_a : coverpoint a;
      cp_b : coverpoint b;
      x_ab : cross cp_a, cp_b;  // no cross_auto_bin_max -- compliant
    endgroup : cg

**Severity**: ERROR

----

.. _AF_FCOV_PERF_NO_EDGE_IMPL_SAMP:

AF_FCOV_PERF_NO_EDGE_IMPL_SAMP
------------------------------

Clock-edge implicit sampling (``posedge``/``negedge``) must not be used in covergroups.

**Rationale**: Attaching a clock edge to the covergroup header
(``covergroup cg @(posedge clk)``) causes the covergroup to sample on every
clock edge regardless of whether a meaningful transaction has occurred. This
creates unnecessary simulation overhead and inflates coverage numbers with
redundant samples. Use transaction-triggered event sampling or explicit
``cg.sample()`` calls so that coverage is recorded only when relevant
activity takes place.

**Violation**::

    covergroup cg @(posedge clk);  // edge-based implicit sampling -- violation
      option.per_instance = 1;
      cp_addr : coverpoint addr;
    endgroup : cg

**Correct usage**::

    covergroup cg;                 // no implicit sampling trigger -- compliant
      option.per_instance = 1;
      cp_addr : coverpoint addr;
    endgroup : cg
    // sample explicitly when a transaction completes:
    // cg_inst.sample();

**Severity**: ERROR

----

.. _AF_FCOV_FUNC_NO_GOAL_OPT:

AF_FCOV_FUNC_NO_GOAL_OPT
------------------------

``option.goal`` must not be set in SystemVerilog source code.

**Rationale**: Coverage goals define the acceptance threshold for a
verification sign-off decision. Hard-coding ``option.goal`` inside a
covergroup couples the goal to the RTL source and makes it impossible to
adjust targets without a code change and re-simulation. Coverage goals should
be managed externally via a vPlan or HVP coverage reporting tool, keeping the
verification intent separate from the coverage model implementation.

**Violation**::

    covergroup cg;
      option.per_instance = 1;
      option.goal = 90;  // goal hardcoded in source -- violation
      cp_a : coverpoint a;
    endgroup : cg

**Correct usage**::

    covergroup cg;
      option.per_instance = 1;  // no option.goal -- compliant
      cp_a : coverpoint a;
    endgroup : cg
    // set coverage goals in vPlan or reporting configuration

**Severity**: ERROR

----

.. _AF_FCOV_NO_HIER_CROSS_VLT:

AF_FCOV_NO_HIER_CROSS_VLT
-------------------------

Cross coverage must not use hierarchical references.

**Rationale**: Verilator does not support hierarchical path expressions
(e.g., ``u_child.sig``) inside cross coverage items. Such references cause a
Verilator compilation error or are silently ignored, leaving the cross
unmonitored. All items in a cross must be locally declared coverpoint names.

**Violation**::

    module fcov_f;
      logic [1:0] a; child u_child();
      covergroup cg;
        option.per_instance = 1;
        cp_a : coverpoint a;
        x_ab : cross cp_a, u_child.sig;  // hierarchical ref -- violation
      endgroup : cg
    endmodule

**Correct usage**::

    module fcov_p;
      logic [1:0] a; logic [1:0] b;
      covergroup cg;
        option.per_instance = 1;
        cp_a : coverpoint a;
        cp_b : coverpoint b;
        x_ab : cross cp_a, cp_b;  // only local coverpoints -- compliant
      endgroup : cg
    endmodule

**Severity**: ERROR

----

.. _AF_FCOV_FUNC_NO_ILLEGAL_BINS:

AF_FCOV_FUNC_NO_ILLEGAL_BINS
----------------------------

Covergroups must not use ``illegal_bins``.

**Rationale**: An ``illegal_bins`` entry causes the simulator to throw a
fatal error whenever the sampled value falls in the illegal range. This stops
the simulation immediately, which can abort the testbench, disrupt UVM error
reporting, and mask the coverage of subsequent stimulus. Use ``ignore_bins``
to exclude unwanted values from the coverage metric, and enforce illegal-state
detection separately via SVA assertions or a scoreboard check.

**Violation**::

    covergroup cg;
      option.per_instance = 1;
      cp_state : coverpoint state {
        illegal_bins ill = {3'b111};  // fatal on hit -- violation
      }
    endgroup : cg

**Correct usage**::

    covergroup cg;
      option.per_instance = 1;
      cp_state : coverpoint state {
        ignore_bins unused = {3'b111};  // silently excluded -- compliant
      }
    endgroup : cg
    // enforce illegal state separately:
    // assert property (@(posedge clk) state != 3'b111);

**Severity**: ERROR

----

.. _AF_FCOV_PERF_NO_IMPL_SAMP:

AF_FCOV_PERF_NO_IMPL_SAMP
-------------------------

Implicit event-triggered sampling must not be used in covergroups.

**Rationale**: Implicit sampling (any ``@(...)`` on the covergroup header)
causes the covergroup to sample on every occurrence of that event. When the
event is a clock edge this fires on every cycle; even for transaction events
it couples the coverage model to a specific event, making it fragile and hard
to reuse. Using explicit ``cg.sample()`` calls gives precise control over
when samples are taken and makes the sampling intent visible at the call site.

**Violation**::

    covergroup cg @(posedge clk);  // any implicit @(...) -- violation
      option.per_instance = 1;
      cp_addr : coverpoint addr;
    endgroup : cg

**Correct usage**::

    covergroup cg;                 // no @(...) trigger -- compliant
      option.per_instance = 1;
      cp_addr : coverpoint addr;
    endgroup : cg
    // call explicitly at transaction boundaries:
    // cg_inst.sample();

**Severity**: ERROR

----

.. _AF_FCOV_FUNC_NO_MERGE_INST:

AF_FCOV_FUNC_NO_MERGE_INST
--------------------------

``type_option.merge_instances`` must not be set in covergroups.

**Rationale**: Setting ``type_option.merge_instances = 1`` collapses the
coverage data from all instances of the covergroup into a single type-level
report. This masks per-instance coverage holes — an instance that never
samples certain bins is invisible in the merged report. Keeping instances
separate (the default) provides full visibility into which instance is
under-covered.

**Violation**::

    covergroup cg;
      option.per_instance = 1;
      type_option.merge_instances = 1;  // hides per-instance holes -- violation
      cp_a : coverpoint a;
    endgroup : cg

**Correct usage**::

    covergroup cg;
      option.per_instance = 1;  // no merge_instances -- compliant
      cp_a : coverpoint a;
    endgroup : cg

**Severity**: ERROR

----

.. _AF_FCOV_FUNC_PER_INSTANCE:

AF_FCOV_FUNC_PER_INSTANCE
-------------------------

All covergroups must set ``option.per_instance = 1``.

**Rationale**: Without ``option.per_instance = 1``, the simulator merges
coverage data from all instances of a covergroup into a single type-level
bucket. In reusable components (UVM agents, environments) that are
instantiated multiple times, this hides the fact that some instances may
never exercise certain bins. Setting ``option.per_instance = 1`` ensures each
instance is tracked individually, making coverage holes visible at the
instance level.

**Violation**::

    covergroup cg;          // no per_instance option -- violation
      cp_a : coverpoint a;
    endgroup : cg

**Correct usage**::

    covergroup cg;
      option.per_instance = 1;  // instance-level tracking -- compliant
      cp_a : coverpoint a;
    endgroup : cg

**Severity**: ERROR

----

.. _AF_FCOV_PERF_USE_CR_ABIN_MAX:

AF_FCOV_PERF_USE_CR_ABIN_MAX
----------------------------

All cross coverage specifications must define ``option.cross_auto_bin_max``.

**Rationale**: A cross of two coverpoints each with N bins produces up to N²
automatically generated bins. Without ``option.cross_auto_bin_max``, the
simulator generates every combination, which can exhaust memory and slow
coverage database writes. Explicitly setting a maximum caps the bin count
and prevents combinatorial explosion.

**Violation**::

    covergroup cg;
      option.per_instance = 1;
      cp_a : coverpoint a;
      cp_b : coverpoint b;
      x_ab : cross cp_a, cp_b;  // no cross_auto_bin_max -- violation
    endgroup : cg

**Correct usage**::

    covergroup cg;
      option.per_instance = 1;
      cp_a : coverpoint a;
      cp_b : coverpoint b;
      x_ab : cross cp_a, cp_b {
        option.cross_auto_bin_max = 64;  // caps bin count -- compliant
      }
    endgroup : cg

**Severity**: ERROR

----

.. _AF_FCOV_CONSEC_RPT_VLT:

AF_FCOV_CONSEC_RPT_VLT
----------------------

Consecutive repetition ``[*]`` in coverage transition bins is unsupported by Verilator.

**Rationale**: Verilator emits ``%Warning-COVERIGN`` and silently ignores
any coverage bin that uses a consecutive repetition operator ``[*N]``. The
bin is present in the source but never hit, leaving contiguous state
transitions permanently unmonitored without any runtime indication.
Replace the repetition with explicit single-step transitions.

**Violation**::

    bins b = (sig [*2]);  // consecutive repetition -- violation

**Correct usage**::

    bins b = (sig => sig);  // explicit two-step transition -- compliant

**Severity**: ERROR

----

.. _AF_FCOV_GOTO_RPT_VLT:

AF_FCOV_GOTO_RPT_VLT
--------------------

Goto repetition ``[->]`` in coverage transition bins is unsupported by Verilator.

**Rationale**: Verilator emits ``%Warning-COVERIGN`` and silently ignores
any coverage bin that uses a goto repetition operator ``[->N]``. The bin is
never hit during simulation, failing to track target reachability across
delays. Restructure the bin using explicit single-step transition sequences.

**Violation**::

    bins b = (sig [->2]);  // goto repetition -- violation

**Correct usage**::

    bins b = (0 => 1 => 0 => 1);  // explicit transition sequence -- compliant

**Severity**: ERROR

----

.. _AF_FCOV_NONCONSEC_RPT_VLT:

AF_FCOV_NONCONSEC_RPT_VLT
-------------------------

Non-consecutive repetition ``[=]`` in coverage transition bins is unsupported by Verilator.

**Rationale**: Verilator emits ``%Warning-COVERIGN`` and silently ignores
any coverage bin that uses a non-consecutive repetition operator ``[=N]``.
The bin is never hit during simulation, resulting in silent coverage loss for
sparse or delayed events. Reframe the coverage using explicit transition
sequences.

**Violation**::

    bins b = (sig [=2]);  // non-consecutive repetition -- violation

**Correct usage**::

    bins b = (0 => 1 => 0 => 1);  // explicit transition sequence -- compliant

**Severity**: ERROR

----

.. _AF_FCOV_TRANS_RANGE_VLT:

AF_FCOV_TRANS_RANGE_VLT
-----------------------

Value ranges ``[low:high]`` must not appear in transition bin specifications.

**Rationale**: Verilator does not support value ranges inside transition
expressions (e.g., ``([0:3] => 4)``). The transition bin is silently ignored,
leaving the corresponding state-machine arc unmonitored. Replace the range
with discrete values or define separate bins for each value of interest.

**Violation**::

    bins trans_b = ([0:3] => 4);  // range in transition -- violation

**Correct usage**::

    bins trans_0 = (0 => 4);      // discrete values -- compliant
    bins trans_1 = (1 => 4);
    bins trans_2 = (2 => 4);
    bins trans_3 = (3 => 4);

**Severity**: ERROR

----

.. _AF_FCOV_TRANS_MULTI_VAL_VLT:

AF_FCOV_TRANS_MULTI_VAL_VLT
---------------------------

Multi-value transition bins are not supported by Verilator.

**Rationale**: Verilator only supports transition bins with a single value on
each side of the ``=>`` operator (e.g., ``(3 => 4)``). A comma-separated
list on either side (e.g., ``(1,2,3 => 4,5)``) is not recognised by
Verilator and the bin is silently ignored, producing no coverage hits for
those transitions. Use one explicit bin per transition pair.

**Violation**::

    cp_state : coverpoint state {
      bins state_trans = (1,2,3 => 4,5);  // multi-value -- violation
    }

**Correct usage**::

    cp_state : coverpoint state {
      bins state_trans = (3 => 4);  // single value each side -- compliant
    }

**Severity**: ERROR

----

.. _AF_FCOV_STYLE_ENDLABEL:

AF_FCOV_STYLE_ENDLABEL
----------------------

Covergroups must include an explicit endlabel after ``endgroup``.

**Rationale**: Adding a label to ``endgroup`` (e.g., ``endgroup : cg_name``)
mirrors the style used for modules, interfaces, and other named blocks in
SystemVerilog. It makes the scope boundaries immediately visible in code
review and grep output, and helps tools that associate the closing token with
the named covergroup. Omitting the label is legal but reduces readability.

**Violation**::

    covergroup cg;
      option.per_instance = 1;
      cp_a : coverpoint a;
    endgroup                // no endlabel -- violation

**Correct usage**::

    covergroup cg;
      option.per_instance = 1;
      cp_a : coverpoint a;
    endgroup : cg           // explicit endlabel -- compliant

**Severity**: ERROR
