#!/usr/bin/env python3
"""
Agently Project Verification Script

This script verifies that all project components are properly configured.
"""

import sys
from pathlib import Path


def print_header(text: str) -> None:
    """Print formatted header"""
    print(f"\n{'=' * 70}")
    print(f"  {text}")
    print(f"{'=' * 70}\n")


def print_result(name: str, success: bool, message: str = "") -> None:
    """Print test result"""
    icon = "✅" if success else "❌"
    print(f"  {icon} {name}")
    if message:
        print(f"     {message}")


def verify_project_structure() -> bool:
    """Verify project directory structure"""
    print("Project Structure:")
    all_ok = True

    required_dirs = [
        "src/agently",
        "src/agently/cli",
        "src/agently/agents",
        "src/agently/orchestrator",
        "src/agently/core",
        "src/agently/infrastructure",
        "tests/unit",
        "tests/integration",
        ".github/workflows",
    ]

    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print_result(dir_path, True)
        else:
            print_result(dir_path, False, "Directory not found")
            all_ok = False

    return all_ok


def verify_configuration_files() -> bool:
    """Verify configuration files exist"""
    print("\nConfiguration Files:")
    all_ok = True

    required_files = [
        "pyproject.toml",
        "ruff.toml",
        "mypy.ini",
        "pytest.ini",
        ".gitignore",
        ".env.example",
        ".pre-commit-config.yaml",
        "Dockerfile",
        "docker-compose.yml",
        "Makefile",
    ]

    for file_path in required_files:
        if Path(file_path).exists():
            print_result(file_path, True)
        else:
            print_result(file_path, False, "File not found")
            all_ok = False

    return all_ok


def verify_source_files() -> bool:
    """Verify source files"""
    print("\nSource Files:")
    all_ok = True

    required_files = [
        "src/agently/__init__.py",
        "src/agently/config.py",
        "src/agently/logging.py",
        "src/agently/cli/__init__.py",
        "src/agently/cli/main.py",
    ]

    for file_path in required_files:
        if Path(file_path).exists():
            print_result(file_path, True)
        else:
            print_result(file_path, False, "File not found")
            all_ok = False

    return all_ok


def verify_test_files() -> bool:
    """Verify test files"""
    print("\nTest Files:")
    all_ok = True

    required_files = [
        "tests/unit/test_config.py",
        "tests/unit/test_logging.py",
        "tests/unit/test_cli.py",
    ]

    for file_path in required_files:
        if Path(file_path).exists():
            print_result(file_path, True)
        else:
            print_result(file_path, False, "File not found")
            all_ok = False

    return all_ok


def verify_documentation() -> bool:
    """Verify documentation files"""
    print("\nDocumentation:")
    all_ok = True
    required_files = [
        "README.md",
        "LICENSE",
        "mkdocs.yml",
    ]
    for file_path in required_files:
        if Path(file_path).exists():
            print_result(file_path, True)
        else:
            print_result(file_path, False, "File not found")
            all_ok = False

    return all_ok


def verify_ci_cd() -> bool:
    """Verify CI/CD workflows"""
    print("\nCI/CD Workflows:")
    all_ok = True

    required_files = [
        ".github/workflows/ci.yml",
        ".github/workflows/release.yml",
        ".github/workflows/docs.yml",
    ]

    for file_path in required_files:
        if Path(file_path).exists():
            print_result(file_path, True)
        else:
            print_result(file_path, False, "File not found")
            all_ok = False

    return all_ok


def main() -> int:
    """Main verification function"""
    print_header("Agently Project Verification")

    results = [
        verify_project_structure(),
        verify_configuration_files(),
        verify_source_files(),
        verify_test_files(),
        verify_documentation(),
        verify_ci_cd(),
    ]

    print_header("Verification Summary")

    if all(results):
        print("✅ All checks passed! Project is properly configured.")
        return 0
    else:
        failed = len([r for r in results if not r])
        print(f"❌ {failed} check(s) failed. Please review the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
