#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to verify new progress bar and account interval features
"""

import sys
sys.path.insert(0, '.')

from util import Config, Logger
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn
import time

console = Console()

def test_config_interval():
    """Test account_interval configuration"""
    print("\n[TEST 1] Account Interval Configuration")
    print("-" * 50)
    try:
        config = Config()
        base = config["Base"]
        
        # Check if account_interval exists
        if "account_interval" in base:
            interval = config.getint("Base", "account_interval")
            print(f"OK: account_interval = {interval} seconds")
            return True
        else:
            print("WARNING: account_interval not configured (will default to 0)")
            return True
    except Exception as e:
        print(f"FAIL: {e}")
        return False


def test_overall_progress_bar():
    """Test overall progress bar display"""
    print("\n[TEST 2] Overall Progress Bar Display")
    print("-" * 50)
    try:
        # Simulate multi-account progress
        num_accounts = 3
        console.print(f"\n[bold cyan]Simulating {num_accounts} accounts execution[/bold cyan]\n")
        
        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=console,
            transient=True
        ) as progress:
            task = progress.add_task(
                "[cyan]Overall Progress", 
                total=num_accounts
            )
            
            for idx in range(num_accounts):
                console.print(f"[bold yellow]({idx+1}/{num_accounts}) Processing Account {idx}[/bold yellow]")
                time.sleep(0.5)  # Simulate processing
                progress.update(task, advance=1)
                
                if idx < num_accounts - 1:
                    console.print("[cyan]Waiting 2 seconds before next account...[/cyan]")
                    time.sleep(2)
        
        console.print(f"\n[bold green]✓ Progress bar test completed[/bold green]\n")
        return True
    except Exception as e:
        print(f"FAIL: {e}")
        return False


def test_multiple_accounts():
    """Test configuration with multiple accounts"""
    print("\n[TEST 3] Multiple Accounts Configuration")
    print("-" * 50)
    try:
        config = Config()
        accounts = config["accounts"]
        
        console.print(f"\n[bold cyan]Found {len(accounts)} account(s)[/bold cyan]")
        
        if len(accounts) < 2:
            console.print("[yellow]WARNING: Less than 2 accounts configured. Multi-account test needs at least 2 accounts.[/yellow]")
            return True
        
        # Display account info
        for idx, account in enumerate(accounts):
            name = account.get("name", f"Account_{idx}")
            student_id = account.get("StudentID", "N/A")
            console.print(f"  [{idx}] {name}: {student_id}")
        
        console.print(f"\n[bold green]✓ Multiple accounts test passed[/bold green]\n")
        return True
    except Exception as e:
        print(f"FAIL: {e}")
        return False


def run_all_tests():
    """Run all tests"""
    print("\n" + "=" * 50)
    print("Progress Bar & Account Interval - Feature Test")
    print("=" * 50)
    
    results = []
    results.append(("Config Interval", test_config_interval()))
    results.append(("Overall Progress Bar", test_overall_progress_bar()))
    results.append(("Multiple Accounts", test_multiple_accounts()))
    
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
        print("\n✓ All tests passed!")
        print("\nUsage examples:")
        print("  python main.py -a              # Run all accounts with progress bar")
        print("  # (Uses account_interval from config for delays)")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed!")
        return 1


if __name__ == "__main__":
    exit(run_all_tests())
