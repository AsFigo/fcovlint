# ----------------------------------------------------
# SPDX-FileCopyrightText: AsFigo Technologies, UK
# SPDX-FileCopyrightText: VerifWorks, India
# SPDX-License-Identifier: MIT
# Author: Miles Huang
# ----------------------------------------------------

from af_lint_rule import AsFigoLintRule
import logging
import anytree

class FcovCgNaming(AsFigoLintRule):
    """Checks if covergroup follows a naming convention - start with "cg_" or ends with "_cg" """

    def __init__(self, linter):
        self.linter = linter
        self.ruleID = "CG_NAMING"

    def apply(self, filePath: str, data: AsFigoLintRule.VeribleSyntax.SyntaxData):
        for curNode in data.tree.iter_find_all({"tag": "kCovergroupHeader"}):
            lvLabel = curNode.children[1].text

            if not lvLabel:
                continue

            if not (lvLabel.startswith("cg_") or lvLabel.endswith("_cg")):
                message = (
                    f"Debug: Found covergroup name without cg_ prefix or _cg suffix. "
                    f"Use cg_ as prefix or _cg suffix for covergroup. This helps users to "
                    f"grep/filter in large designs. "
                    f"Found a Cover Group as:\n"
                    f"{curNode.text}\n"
                )
                self.linter.logViolation(self.ruleID, message, "WARNING")
        