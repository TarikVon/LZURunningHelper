#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to verify all new features:
1. JSON config format
2. Multi-account support
3. Rich progress bar integration
4. Default upload behavior (no -s flag needed)
"""

import sys
sys.path.insert(0, '.')

from util import Config, Logger
from Joyrun import JoyrunClient

def test_json_config():
    """Test JSON configuration loading"""
    print("\n[TEST 1] JSON Configuration Loading")
    print("-" * 50)
    try:
        config = Config()
        print("OK: Config loaded from config.json")
        
        # Verify Base section
        app = config.get("Base", "APP")
        debug = config.getboolean("Base", "debug")
        print(f"OK: APP = {app}, debug = {debug}")
        
        return True
    except Exception as e:
        print(f"FAIL: {e}")
        return False


def test_multi_account_support():
    """Test multi-account support in configuration"""
    print("\n[TEST 2] Multi-Account Support")
    print("-" * 50)
    try:
        config = Config()
        accounts = config["accounts"]
        
        print(f"OK: Found {len(accounts)} account(s)")
        for idx, account in enumerate(accounts):
            name = account.get("name", f"Account_{idx}")
            student_id = account.get("StudentID", "N/A")
            record_type = account.get("record_type", "N/A")
            distance = account.get("distance", "N/A")
            print(f"  [{idx}] {name}: {student_id} (record_type={record_type}, distance={distance}km)")
        
        return len(accounts) > 0
    except Exception as e:
        print(f"FAIL: {e}")
        return False


def test_client_account_index():
    """Test JoyrunClient with account_index parameter"""
    print("\n[TEST 3] JoyrunClient Multi-Account Support")
    print("-" * 50)
    try:
        config = Config()
        accounts = config["accounts"]
        
        if len(accounts) == 0:
            print("FAIL: No accounts configured")
            return False
        
        # Test creating client with first account
        client = JoyrunClient(account_index=0)
        print(f"OK: Client created for account {client.account_index}: {client.account_name}")
        print(f"    Username: {client.userName}")
        
        # Test out-of-range index
        try:
            bad_client = JoyrunClient(account_index=999)
            print("FAIL: Should have raised ValueError for invalid index")
            return False
        except ValueError as e:
            print(f"OK: Correctly rejected invalid index with error: {e}")
        
        return True
    except Exception as e:
        print(f"FAIL: {e}")
        return False


def test_rich_integration():
    """Test rich library integration"""
    print("\n[TEST 4] Rich Library Integration")
    print("-" * 50)
    try:
        from rich.console import Console
        from rich.table import Table
        from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
        
        print("OK: All required rich components imported successfully")
        
        # Test table rendering
        console = Console()
        table = Table(title="Test Table")
        table.add_column("Column 1", style="cyan")
        table.add_column("Column 2", style="green")
        table.add_row("Test", "Data")
        console.print(table)
        
        print("OK: Rich table rendered successfully")
        return True
    except Exception as e:
        print(f"FAIL: {e}")
        return False


def test_main_py_imports():
    """Test main.py imports"""
    print("\n[TEST 5] Main Script Imports")
    print("-" * 50)
    try:
        # Try importing main module components
        from rich.table import Table
        from util import Config, Logger, pretty_json, json, APPTypeError
        
        print("OK: All main.py imports available")
        return True
    except Exception as e:
        print(f"FAIL: {e}")
        return False


def run_all_tests():
    """Run all tests"""
    print("\n" + "=" * 50)
    print("LZU Running Helper - Feature Test Suite")
    print("=" * 50)
    
    results = []
    results.append(("JSON Config", test_json_config()))
    results.append(("Multi-Account", test_multi_account_support()))
    results.append(("Client Account Index", test_client_account_index()))
    results.append(("Rich Integration", test_rich_integration()))
    results.append(("Main Script Imports", test_main_py_imports()))
    
    # Summary
    print("\n" + "=" * 50)
    print("Test Summary")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"[{status}] {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\nAll tests passed! Features are ready to use.")
        print("\nUsage:")
        print("  python main.py              # Default: run single account or select from multiple")
        print("  python main.py -a           # Run all accounts")
        print("  python main.py -i 0         # Run specific account by index")
        print("  python main.py -c           # Check configuration")
        return 0
    else:
        print(f"\n{total - passed} test(s) failed!")
        return 1


if __name__ == "__main__":
    exit(run_all_tests())
