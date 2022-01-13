#!/usr/bin/env python

"""Tests for `cellranger_job_templates` package."""


import unittest

from cellranger_job_templates import cellranger_job_templates, cli
from click.testing import CliRunner


class Testcellranger_job_templates(unittest.TestCase):
    """Tests for `cellranger_job_templates` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert "cellranger_job_templates.cli.main" in result.output
        help_result = runner.invoke(cli.main, ["--help"])
        assert help_result.exit_code == 0
        assert "--help  Show this message and exit." in help_result.output
