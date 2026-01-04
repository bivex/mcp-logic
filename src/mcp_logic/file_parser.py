# Copyright (c) 2026 Bivex
#
# Author: Bivex
# Available for contact via email: support@b-b.top
# For up-to-date contact information:
# https://github.com/bivex
#
# Created: 2026-01-04T10:10:31
# Last Updated: 2026-01-04T10:10:40
#
# Licensed under the MIT License.
# Commercial licensing available upon request.

"""
File parser for Prover9/Mace4 .in files
"""

import re
from pathlib import Path
from typing import List, Tuple, Optional


class Prover9FileParser:
    """Parser for Prover9/Mace4 input files"""

    def __init__(self):
        pass

    def parse_file(self, file_path: str) -> Tuple[List[str], Optional[str]]:
        """
        Parse a Prover9 .in file and extract premises and conclusion.

        Args:
            file_path: Path to the .in file

        Returns:
            Tuple of (premises_list, conclusion_string_or_none)
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        return self.parse_content(content)

    def parse_content(self, content: str) -> Tuple[List[str], Optional[str]]:
        """
        Parse Prover9 file content and extract premises and conclusion.

        Args:
            content: The content of a Prover9 .in file

        Returns:
            Tuple of (premises_list, conclusion_string_or_none)
        """
        # Remove comments (lines starting with %)
        lines = []
        for line in content.split('\n'):
            line = line.strip()
            if line and not line.startswith('%'):
                lines.append(line)

        content = '\n'.join(lines)

        # Extract assumptions (premises)
        premises = []
        assumptions_match = re.search(r'formulas\(assumptions\)\.\s*(.*?)\s*end_of_list\.', content, re.DOTALL | re.IGNORECASE)
        if assumptions_match:
            assumptions_block = assumptions_match.group(1).strip()
            # Split by dots and clean up
            formulas = re.split(r'\.\s*', assumptions_block)
            for formula in formulas:
                formula = formula.strip()
                if formula and not formula.lower().startswith('end'):
                    premises.append(formula)

        # Extract goals (conclusion)
        conclusion = None
        goals_match = re.search(r'formulas\(goals\)\.\s*(.*?)\s*end_of_list\.', content, re.DOTALL | re.IGNORECASE)
        if goals_match:
            goals_block = goals_match.group(1).strip()
            # Split by dots and clean up
            goals = re.split(r'\.\s*', goals_block)
            for goal in goals:
                goal = goal.strip()
                if goal and not goal.lower().startswith('end'):
                    conclusion = goal
                    break  # Take the first goal as the conclusion

        return premises, conclusion

    def parse_mace4_file(self, file_path: str) -> List[str]:
        """
        Parse a Mace4 .in file and extract all formulas as premises.
        Mace4 files typically don't have goals, just assumptions.

        Args:
            file_path: Path to the Mace4 .in file

        Returns:
            List of premise formulas
        """
        premises, _ = self.parse_file(file_path)
        return premises


def parse_prover9_file(file_path: str) -> Tuple[List[str], Optional[str]]:
    """
    Convenience function to parse a Prover9 file.

    Args:
        file_path: Path to the .in file

    Returns:
        Tuple of (premises, conclusion)
    """
    parser = Prover9FileParser()
    return parser.parse_file(file_path)


def parse_mace4_file(file_path: str) -> List[str]:
    """
    Convenience function to parse a Mace4 file.

    Args:
        file_path: Path to the .in file

    Returns:
        List of premises
    """
    parser = Prover9FileParser()
    return parser.parse_mace4_file(file_path)
