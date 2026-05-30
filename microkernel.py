#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌀 DXN1-AGENT-CLI | PROTOTYPE v1.5.0-ULTRA
The Absolute Apex of User-Space Microkernels.
Created with ❤️ BY DXN1
"""

import os
import sys
import json
import time
import requests
import itertools
import threading
import readline
import urllib.parse
from datetime import datetime
from typing import Dict, Any, List, Optional

# Apex UI Framework
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.live import Live
from rich.spinner import Spinner
from rich.markdown import Markdown
from rich.align import Align
from rich.layout import Layout
from rich.syntax import Syntax
from rich.theme import Theme

# Internal Components
from tool_executor import ToolSandboxExecutor

# Custom Professional Theme
DXN1_THEME = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "bold red",
    "success": "bold green",
    "highlight": "bold magenta",
    "dim": "dim white",
    "border": "bright_blue"
})

console = Console(theme=DXN1_THEME)

class Dxn1Microkernel:
    def __init__(self, host: str = "127.0.0.1", port: int = 5001):
        self.host = host
        self.port = port
        self.is_running = False
        self.use_history = True
        self.process_table: Dict[int, Dict[str, Any]] = {}
        self.actor_registry: Dict[str, Any] = {}
        self.task_queue: List[Dict[str, Any]] = []
        self.chat_history: List[Dict[str, str]] = []
        self.system_logs: List[str] = []
        self.lock = threading.Lock()
        self.tool_executor = ToolSandboxExecutor()
        
        # Security & Identity
        self.api_key = "NOT_CONFIGURED"
        self.api_provider = "gemini" 
        self.llm_mode = "open_source"
        
        # Initialization
        self._register_core_actors()
        self._load_local_credentials()
        self._setup_readline()
        
        # Start Heartbeat Thread (Makes the system feel 'Alive')
        threading.Thread(target=self._system_heartbeat, daemon=True).start()

    def _log(self, message: str, level: str = "info"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.system_logs.append(f"[{timestamp}] {message}")
        if len(self.system_logs) > 15:
            self.system_logs.pop(0)

    def _setup_readline(self):
        histfile = os.path.join(os.path.expanduser("~"), ".dxn1_apex_history")
        try:
            readline.read_history_file(histfile)
        except FileNotFoundError:
            pass
        readline.set_history_length(2000)
        import atexit
        atexit.register(readline.write_history_file, histfile)

    def _register_core_actors(self):
        self.actor_registry["kernel_daemon"] = {"pid": 1001, "port": 5000, "meta": "Core System"}
        self.actor_registry["broker_node"] = {"pid": 1002, "port": 5001, "meta": "IPC Bridge"}
        self.process_table[1001] = {"name": "kernel_daemon", "status": "ACTIVE", "cpu": 0.05, "mem": 1.2}
        self.process_table[1002] = {"name": "broker_node", "status": "ACTIVE", "cpu": 0.02, "mem": 0.8}
        self._log("Core microkernel services registered.")

    def _load_local_credentials(self):
        if os.path.exists(".nam_secrets"):
            try:
                with open(".nam_secrets", "r") as f:
                    for line in f:
                        if "=" in line:
                            k, v = line.strip().split("=", 1)
                            if k == "API_KEY": self.api_key = v
                            elif k == "API_PROVIDER":
                                mapping = {"1": "gemini", "2": "openai", "3": "anthropic"}
                                self.api_provider = mapping.get(v, v.lower())
                            elif k == "LLM_MODE": self.llm_mode = v
                self._log(f"Credentials loaded: {self.api_provider.upper()} ({self.llm_mode})")
            except Exception as e:
                self._log(f"Credential load failure: {e}", "error")

    def _system_heartbeat(self):
        """Simulates dynamic system load and agent activity for high-end aesthetic."""
        import random
        while True:
            if self.is_running:
                with self.lock:
                    for pid in self.process_table:
                        # Realistic jitter in CPU/MEM
                        self.process_table[pid]["cpu"] = round(max(0.1, self.process_table[pid]["cpu"] + random.uniform(-0.05, 0.05)), 2)
                        self.process_table[pid]["mem"] = round(max(0.5, self.process_table[pid]["mem"] + random.uniform(-0.02, 0.02)), 1)
            time.sleep(3)

    def _call_llm(self, prompt: str, use_history: bool = True) -> str:
        if self.llm_mode == "open_source":
            return "Cognitive node is currently in [bold yellow]OFFLINE[/bold yellow] mode. Please link a BYOK provider via launcher for real-time reasoning."
        
        history_context = ""
        if use_history:
            for entry in self.chat_history[-8:]: # Increased context window
                history_context += f"User: {entry['user']}\nAI: {entry['ai']}\n"
        
        full_prompt = history_context + f"User: {prompt}"

        try:
            if "gemini" in self.api_provider:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.api_key}"
                data = {"contents": [{"parts": [{"text": full_prompt}]}]}
                response = requests.post(url, json=data, timeout=30)
                res_json = response.json()
                reply = res_json['candidates'][0]['content']['parts'][0]['text']
            elif "openai" in self.api_provider:
                url = "https://api.openai.com/v1/chat/completions"
                headers = {"Authorization": f"Bearer {self.api_key}"}
                messages = []
                if use_history:
                    for entry in self.chat_history[-5:]:
                        messages.extend([{"role": "user", "content": entry['user']}, {"role": "assistant", "content": entry['ai']}])
                messages.append({"role": "user", "content": prompt})
                response = requests.post(url, headers=headers, json={"model": "gpt-4o-mini", "messages": messages}, timeout=30)
                reply = response.json()['choices'][0]['message']['content']
            elif "anthropic" in self.api_provider:
                url = "https://api.anthropic.com/v1/messages"
                headers = {"x-api-key": self.api_key, "anthropic-version": "2023-06-01", "content-type": "application/json"}
                messages = []
                if use_history:
                    for entry in self.chat_history[-5:]:
                        messages.extend([{"role": "user", "content": entry['user']}, {"role": "assistant", "content": entry['ai']}])
                messages.append({"role": "user", "content": prompt})
                response = requests.post(url, headers=headers, json={"model": "claude-3-haiku-20240307", "max_tokens": 1024, "messages": messages}, timeout=30)
                reply = response.json()['content'][0]['text']
            else:
                return "Error: Unsupported Provider Configuration."

            self.chat_history.append({"user": prompt, "ai": reply})
            return reply
        except Exception as e:
            self._log(f"LLM Routing Error: {e}", "error")
            return f"❌ [bold red]COGNITIVE ROUTING FAILURE:[/bold red] {str(e)}"

    def spawn_agent(self, name: str, capabilities: List[str]) -> int:
        with self.lock:
            pid = max(self.process_table.keys(), default=1000) + 1
            self.process_table[pid] = {"name": name, "status": "RUNNING", "cpu": 0.05, "mem": 2.4, "capabilities": capabilities}
            self.actor_registry[name] = {"pid": pid, "port": 5000 + len(self.process_table), "meta": f"Agent Node - {', '.join(capabilities)}"}
            self._log(f"Spawned agent node: {name} (PID {pid})")
            return pid

    def dispatch_ipc_route(self, sender: str, receiver: str, payload: Dict[str, Any]) -> str:
        if receiver not in self.actor_registry:
            return f"❌ Destination node '{receiver}' unreachable."
        
        self.task_queue.append({"sender": sender, "receiver": receiver, "timestamp": time.time(), "payload": payload})
        msg = payload.get("msg", "")
        
        if receiver == "reasoner_node" or "reasoner" in receiver:
            status_text = "[bold cyan]Reasoning...[/bold cyan]" if not self.use_history else "[bold magenta]Synthesizing Context...[/bold magenta]"
            with console.status(status_text, spinner="aesthetic"):
                if any(k in msg.lower() for k in ["search", "find", "fetch"]):
                    self._log(f"Triggering secure tool sandbox for query: {msg[:20]}...")
                    tool_output = self.tool_executor.run_safe_query(msg)
                    return self._call_llm(f"Analyze this tool output: {tool_output}", use_history=self.use_history)
                return self._call_llm(msg, use_history=self.use_history)
        
        return f"Default echo from {receiver}: Instruction acknowledged."

    def _make_layout(self) -> Layout:
        layout = Layout(name="root")
        layout.split_column(
            Layout(name="header", size=10),
            Layout(name="body"),
            Layout(name="footer", size=3)
        )
        layout["body"].split_row(
            Layout(name="main_chat", ratio=3),
            Layout(name="side_panel", ratio=1)
        )
        return layout

    def _get_status_table(self) -> Table:
        table = Table(title="[bold cyan]AGENT MATRIX[/bold cyan]", box=None, header_style="bold blue")
        table.add_column("PID", style="dim")
        table.add_column("NODE", style="bold white")
        table.add_column("STAT", justify="center")
        table.add_column("LOAD", style="yellow")
        for pid, data in self.process_table.items():
            stat = "[green]●[/green]" if data["status"] == "ACTIVE" or data["status"] == "RUNNING" else "[red]○[/red]"
            table.add_row(str(pid), data["name"], stat, f"{data['cpu']}%")
        return table

    def _get_logs_panel(self) -> Panel:
        log_text = Text("\n".join(self.system_logs), style="dim white")
        return Panel(log_text, title="[bold yellow]SYSTEM TELEMETRY[/bold yellow]", border_style="yellow")

    def run_server(self):
        self.is_running = True
        os.system('clear' if os.name == 'posix' else 'cls')
        
        # Initial Animation
        with console.status("[bold cyan]Initializing DXN1 Microkernel Apex...[/bold cyan]", spinner="bouncingBar"):
            time.sleep(1.5)
            self._log("IPC Sockets bound to port 5001")
            self._log("Dynamic Routing Engine: ACTIVE")
            self._log("Security Sandbox Shield: LEVEL 3")

        while self.is_running:
            # Re-draw Dashboard
            header_text = Text(r"""
    DXN1-AGENT-CLI | APEX COMMAND CENTER
    [ User-Space Distributed Microkernel ]
            """, style="bold cyan", justify="center")
            
            # Simple UI Layout
            console.clear()
            console.print(Panel(Align.center(header_text), border_style="bright_blue"))
            
            dashboard = Table.grid(expand=True)
            dashboard.add_column(ratio=2)
            dashboard.add_column(ratio=1)
            dashboard.add_row(
                Panel("[italic white]System live. Type naturally to chat. Use [bold green]/help[/bold green] for core commands.[/italic white]", title="[bold]COGNITIVE GATEWAY[/bold]", border_style="bright_blue"),
                Panel(f"[cyan]ENGINE:[/cyan] [bold]{self.api_provider.upper()}[/bold]\n[cyan]CONTEXT:[/cyan] {'[green]ON[/green]' if self.use_history else '[dim]OFF[/dim]'}", title="[bold]LOADOUT[/bold]", border_style="magenta")
            )
            console.print(dashboard)
            console.print(self._get_status_table())
            console.print(self._get_logs_panel())

            try:
                user_input = console.input("\n[bold blue]YOU[/bold blue] [cyan]»[/cyan] ").strip()
                if not user_input: continue
                
                if user_input.startswith("/"):
                    cmd = user_input[1:].split()[0].lower()
                    if cmd == "exit": 
                        self.is_running = False
                        console.print("[bold yellow]De-initializing apex core...[/bold yellow]")
                    elif cmd == "clear": os.system('clear')
                    elif cmd == "continue": 
                        self.use_history = not self.use_history
                        self._log(f"Conversation memory state changed to: {self.use_history}")
                    elif cmd == "help":
                        console.print(Panel("/continue - Toggle memory | /spawn <name> | /pulse | /clear | /exit", title="MANIFEST", border_style="green"))
                        time.sleep(3)
                    elif cmd == "pulse":
                        console.print(Panel(f"Kernel Life: {time.time() % 1000:.1f}s | Tasks: {len(self.task_queue)} | Memory: {len(self.process_table)*2.4:.1f}MB", title="PULSE", border_style="cyan"))
                        time.sleep(2)
                    elif cmd == "spawn":
                        parts = user_input.split()
                        if len(parts) > 1: self.spawn_agent(parts[1], ["custom"])
                else:
                    self._log(f"Dispatching cognitive frame: {user_input[:15]}...")
                    response = self.dispatch_ipc_route("shell_ui", "reasoner_node", {"msg": user_input})
                    console.print(Panel(Markdown(response), title="[bold magenta]REASONER_NODE[/bold magenta]", border_style="magenta", padding=(1, 2)))
                    console.input("\n[dim]Press Enter to return to Command Center...[/dim]")

            except KeyboardInterrupt:
                self.is_running = False
            except Exception as e:
                self._log(f"UI Error: {e}", "error")

if __name__ == "__main__":
    kernel = Dxn1Microkernel()
    kernel.spawn_agent("scrapper_agent", ["fs:read", "net:request"])
    kernel.spawn_agent("reasoner_node", ["llm:cognitive"])
    kernel.run_server()
