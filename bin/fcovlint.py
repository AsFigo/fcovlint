# ----------------------------------------------------
# SPDX-FileCopyrightText: AsFigo Technologies, UK
# SPDX-FileCopyrightText: VerifWorks, India
# SPDX-License-Identifier: MIT
# ----------------------------------------------------

import sys
import os
import argparse
import logging
import verible_verilog_syntax

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from af_lint_rule import AsFigoLintRule
from asfigo_linter import AsFigoLinter
from rules.af_fcov_cross_coverpoint import FCOVCrossCptRuleVlt
from rules.af_fcov_transition_bins import FCOVTrBinsRuleVlt
from rules.af_fcov_constant_option import FCOVConstOptionVlt
from rules.af_fcov_array_bin_limit import FCOVArrayBinLimitRule
from rules.af_fcov_no_hier_cross import FCOVNoHierCrossRule
from rules.af_fcov_intf_in_mod import FCOVInterfaceInModuleRule
from rules.af_fcov_class_mem import FCOVClMemVlt
from rules.af_fcov_trans_range import FCOVTransRangeVlt
from rules.af_fcov_rept_vlt import (
    FCovCnsqRptVlt,
    FCovNCsqRptVlt,
    FCovGotoRptVlt
)
from rules.af_fcov_no_ill_bins import FCOVNoILBinsFunc
from rules.af_fcov_use_end_lbl import FCOVEndlabelStyle
from rules.af_fcov_no_impl_sampl import FcovPerfNoImplSamp
from rules.af_fcov_no_edge_sampl import FcovPerfNoEdgeImplSamp
from rules.af_fcov_per_inst import FcovRequirePerInstance
from rules.af_fcov_perf_cr_abin_max import FcovPerfUseCrAbinMax
from rules.af_fcov_no_cr_abmax_vlt import FcovNoCrAbinMaxVlt
from rules.af_fcov_no_merg_inst import FcovNoMergeInstances
from rules.af_fcov_no_goal_opt import FcovNoGoalInCode
from rules.af_fcov_cg_naming import FcovCgNaming

class FCOVLinter(AsFigoLinter):
    """Linter that applies functional coverage lint rules on SystemVerilog code."""

    def __init__(self, configFile="config.toml", logLevel=logging.INFO):
        super().__init__(configFile=configFile, logLevel=logLevel)
        self.rules = [rule_cls(self) for rule_cls in AsFigoLintRule.__subclasses__()]

    def loadSyntaxTree(self, file_path: str):
        """Loads SystemVerilog syntax tree using VeribleVerilogSyntax."""
        parser = verible_verilog_syntax.VeribleVerilogSyntax()
        return parser.parse_files([file_path], options={"gen_tree": True})

    def runOnSingleFile(self, file_path: str):
        """Runs all registered lint rules on a single file."""
        self.resetFileState(file_path)

        if not os.path.exists(file_path):
            self.logger.error(f"File not found: {file_path}")
            return

        treeData = self.loadSyntaxTree(file_path)

        for path, fileData in treeData.items():
            self.logInfo("FCOVLint", f"Loaded test file: {file_path}")
            for rule in self.rules:
                rule.run(path, fileData)

    def runOnFlist(self, flist_path: str):
        """Runs registered rules sequentially on files listed in a filelist."""
        files = self._parseFlist(flist_path)
        for file_path in files:
            self.runOnSingleFile(file_path)

    def runCli(self) -> int:
        """Parses command-line arguments and triggers linter execution."""
        parser = argparse.ArgumentParser(description="AsFigo FCOVLint Engine")
        parser.add_argument("-t", "--test", help="Path to single SystemVerilog target file")
        parser.add_argument("-f", "--filelist", help="Path to filelist containing SystemVerilog target files")
        parser.add_argument("-c", "--config", default="config.toml", help="Path to rules configuration file")

        args = parser.parse_args()

        if args.config != "config.toml":
            self.rulesConfig = self.loadConfig(args.config)

        if args.test:
            self.runOnSingleFile(args.test)
        elif args.filelist:
            self.runOnFlist(args.filelist)
        else:
            parser.print_help()
            return 1

        self.logSummary()
        return 1 if self.totalErrorCount > 0 else 0


if __name__ == "__main__":
    linter = FCOVLinter(configFile="config.toml", logLevel=logging.INFO)
    sys.exit(linter.runCli())
