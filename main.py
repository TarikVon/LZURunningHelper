#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: main.py
#
# 项目运行主程序
#

import time
from optparse import OptionParser
from util import (
    Config,
    Logger,
    pretty_json,
    json,
    APPTypeError,
)
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, BarColumn, TextColumn

config = Config()
logger = Logger("main")
console = Console()

app = config.get("Base", "APP")

if app == "Joyrun":
    from Joyrun import JoyrunClient as Client, __date__
else:
    raise APPTypeError("unsupported running APP -- %s !" % app)


parser = OptionParser(description="LZU running helper! Check your config first, then enjoy yourself!")
parser.add_option("-c", "--check", help="show config.json file", action="store_true", default=False)
parser.add_option("-a", "--all", help="run all accounts", action="store_true", default=False)
parser.add_option("-i", "--index", help="run specific account by index (0-based)", type="int", default=None)

options, args = parser.parse_args()

if options.check:
    print("# -- Using %s Client [%s] -- #" % (app, __date__))

    for section in config.sections():
        if section == "Base":
            print("# -- Section [%s] -- #" % section)
            print(pretty_json(dict(config[section])))
        elif section == "accounts":
            print("# -- Section [%s] -- #" % section)
            accounts = config[section]
            if isinstance(accounts, list):
                print(pretty_json(accounts))
            else:
                print(pretty_json(dict(accounts)))

else:
    # 默认行为：如果没有指定任何选项，则执行上传
    try:
        logger.info("Running %s Client [%s]" % (app, __date__))
        
        # 获取账号列表和配置
        accounts = config["accounts"]
        account_interval = config.getint("Base", "account_interval") if "account_interval" in config["Base"] else 0
        
        if options.all:
            # 运行所有账号 - 使用总进度条
            console.print(f"\n[bold cyan]开始执行所有账号（共 {len(accounts)} 个）[/bold cyan]\n")
            
            with Progress(
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                console=console,
                transient=True
            ) as overall_progress:
                overall_task = overall_progress.add_task(
                    "[cyan]总进度", 
                    total=len(accounts)
                )
                
                for idx, account in enumerate(accounts):
                    account_name = account.get('name', f'Account_{idx}')
                    console.print(f"\n[bold yellow]({idx+1}/{len(accounts)}) 正在执行账号: {account_name}[/bold yellow]")
                    
                    try:
                        client = Client(account_index=idx)
                        client.run()
                        console.print(f"[bold green]✓ 账号 {account_name} 上传成功[/bold green]")
                    except Exception as err:
                        console.print(f"[bold red]✗ 账号 {account_name} 上传失败[/bold red]")
                        logger.error(f"账号 {account_name} 上传失败: {err}")
                        raise err
                    
                    # 更新总进度条
                    overall_progress.update(overall_task, advance=1)
                    
                    # 如果不是最后一个账号，等待间隔时间
                    if idx < len(accounts) - 1 and account_interval > 0:
                        console.print(f"[cyan]等待 {account_interval} 秒后执行下一个账号...[/cyan]")
                        time.sleep(account_interval)
            
            console.print(f"\n[bold green]✓ 所有账号执行完毕！[/bold green]\n")
        elif options.index is not None:
            # 运行指定索引的账号
            if options.index < 0 or options.index >= len(accounts):
                console.print(f"[bold red]✗ 错误: 账号索引越界，有效范围: 0-{len(accounts)-1}[/bold red]")
                exit(1)
            account = accounts[options.index]
            console.print(f"\n[bold cyan]正在执行账号: {account.get('name', f'Account_{options.index}')}[/bold cyan]\n")
            client = Client(account_index=options.index)
            client.run()
            console.print(f"\n[bold green]✓ 账号 {account.get('name', f'Account_{options.index}')} 上传成功[/bold green]\n")
        else:
            # 默认行为：如果只有一个账号则直接运行，否则让用户选择
            if len(accounts) == 1:
                console.print(f"\n[bold cyan]执行唯一的账号: {accounts[0].get('name', 'Account_0')}[/bold cyan]\n")
                client = Client(account_index=0)
                client.run()
                console.print(f"\n[bold green]✓ 上传成功[/bold green]\n")
            else:
                # 显示账号列表
                table = Table(title="[bold cyan]请选择要执行的账号[/bold cyan]")
                table.add_column("序号", style="cyan")
                table.add_column("账号名", style="magenta")
                table.add_column("学号", style="green")
                
                for idx, account in enumerate(accounts):
                    table.add_row(
                        str(idx),
                        account.get("name", f"Account_{idx}"),
                        account.get("StudentID", "N/A")
                    )
                
                console.print(table)
                console.print()
                
                choice_str = input("请输入账号序号 (0-{}): ".format(len(accounts)-1))
                try:
                    choice = int(choice_str)
                    if choice < 0 or choice >= len(accounts):
                        console.print(f"[bold red]✗ 错误: 序号越界[/bold red]")
                        exit(1)
                    
                    account = accounts[choice]
                    console.print(f"\n[bold cyan]正在执行账号: {account.get('name', f'Account_{choice}')}[/bold cyan]\n")
                    client = Client(account_index=choice)
                    client.run()
                    console.print(f"\n[bold green]✓ 账号 {account.get('name', f'Account_{choice}')} 上传成功[/bold green]\n")
                except ValueError:
                    console.print("[bold red]✗ 错误: 请输入有效的数字[/bold red]")
                    exit(1)
                    
    except Exception as err:
        logger.error("upload record failed !")
        raise err

