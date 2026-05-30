#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DXN1-AGENT-CLI - CORE SCHEDULER & BROKER
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
from typing import Dict, Any, List
from tool_executor import ToolSandboxExecutor

# UI Enhancement libraries
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.live import Live
from rich.spinner import Spinner
from rich.markdown import Markdown
from rich.align import Align

console = Console()

class Dxn1Microkernel:
    def __init__(self, host: str = "127.0.0.1", port: int = 5001):
        self.host = host
        self.port = port
        self.is_running = False
        self.process_table: Dict[int, Dict[str, Any]] = {}
        self.actor_registry: Dict[str, Any] = {}
        self.task_queue: List[Dict[str, Any]] = []
        self.chat_history: List[Dict[str, str]] = [] # Persisted context for /continue
        self.lock = threading.Lock()
        self.tool_executor = ToolSandboxExecutor()
        
        # Identity and Credentials
        self.api_key = "NOT_CONFIGURED"
        self.api_provider = "gemini" 
        self.llm_mode = "open_source"
        
        # Prepopulate Core Services
        self._register_core_actors()
        self._load_local_credentials()
        self._setup_readline()

    def _setup_readline(self):
        """Enable command history for a professional terminal experience."""
        histfile = os.path.join(os.path.expanduser("~"), ".dxn1_history")
        try:
            readline.read_history_file(histfile)
        except FileNotFoundError:
            pass
        readline.set_history_length(1000)
        import atexit
        atexit.register(readline.write_history_file, histfile)

    def _register_core_actors(self):
        self.actor_registry["kernel_daemon"] = {"pid": 1001, "port": 5000, "meta": "Core system processor"}
        self.actor_registry["agent_broker"] = {"pid": 1002, "port": 5001, "meta": "IPC JSON-RPC daemon"}
        self.process_table[1001] = {"name": "kernel_daemon", "status": "ACTIVE", "cpu": 0.1, "mem": 1.2}
        self.process_table[1002] = {"name": "agent_broker", "status": "ACTIVE", "cpu": 0.1, "mem": 0.8}

    def _load_local_credentials(self):
        if os.path.exists(".nam_secrets"):
            try:
                with open(".nam_secrets", "r") as f:
                    for line in f:
                        if "=" in line:
                            k, v = line.strip().split("=", 1)
                            if k == "API_KEY":
                                self.api_key = v
                            elif k == "API_PROVIDER":
                                # Handle numeric mapping if still present in old configs
                                mapping = {"1": "gemini", "2": "openai", "3": "anthropic"}
                                self.api_provider = mapping.get(v, v.lower())
                            elif k == "LLM_MODE":
                                self.llm_mode = v
            except Exception as e:
                console.print(f"[bold yellow][!] KERNEL WARNING: Failed parsing credentials: {e}[/bold yellow]")

    def _call_llm(self, prompt: str, use_history: bool = False) -> str:
        """
        Professional LLM Dispatcher. Supports multiple providers via native REST.
        """
        if self.llm_mode == "open_source":
            return "Kernel Note: Running in Offline/Local Mode. Deploy Ollama to process cognitive prompts."
        
        if self.api_key == "NOT_CONFIGURED":
            return "Kernel Error: API Key not found. Run launcher.py to inject credentials."

        # Manage history for /continue
        history_context = ""
        if use_history:
            for entry in self.chat_history[-5:]: # Last 5 turns for context
                history_context += f"User: {entry['user']}\nAI: {entry['ai']}\n"
        
        full_prompt = history_context + f"User: {prompt}" if use_history else prompt

        try:
            if "gemini" in self.api_provider:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.api_key}"
                headers = {'Content-Type': 'application/json'}
                # Gemini native format for multi-turn would be better, but simple concatenation works for 'llmcontinue'
                data = {"contents": [{"parts": [{"text": full_prompt}]}]}
                response = requests.post(url, headers=headers, json=data, timeout=30)
                res_json = response.json()
                if 'candidates' in res_json:
                    reply = res_json['candidates'][0]['content']['parts'][0]['text']
                    self.chat_history.append({"user": prompt, "ai": reply})
                    return reply
                return f"Gemini API Exception: {res_json}"
            
            elif "openai" in self.api_provider:
                url = "https://api.openai.com/v1/chat/completions"
                headers = {"Authorization": f"Bearer {self.api_key}"}
                messages = []
                if use_history:
                    for entry in self.chat_history[-5:]:
                        messages.append({"role": "user", "content": entry['user']})
                        messages.append({"role": "assistant", "content": entry['ai']})
                messages.append({"role": "user", "content": prompt})
                
                data = {
                    "model": "gpt-4o-mini",
                    "messages": messages
                }
                response = requests.post(url, headers=headers, json=data, timeout=30)
                reply = response.json()['choices'][0]['message']['content']
                self.chat_history.append({"user": prompt, "ai": reply})
                return reply
            
            elif "anthropic" in self.api_provider:
                url = "https://api.anthropic.com/v1/messages"
                headers = {
                    "x-api-key": self.api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json"
                }
                messages = []
                if use_history:
                    for entry in self.chat_history[-5:]:
                        messages.append({"role": "user", "content": entry['user']})
                        messages.append({"role": "assistant", "content": entry['ai']})
                messages.append({"role": "user", "content": prompt})

                data = {
                    "model": "claude-3-haiku-20240307",
                    "max_tokens": 1024,
                    "messages": messages
                }
                response = requests.post(url, headers=headers, json=data, timeout=30)
                reply = response.json()['content'][0]['text']
                self.chat_history.append({"user": prompt, "ai": reply})
                return reply

            return f"Error: Provider {self.api_provider} not supported."
        except Exception as e:
            return f"Cognitive Routing Error: {str(e)}"

    def spawn_agent(self, name: str, capabilities: List[str]) -> int:
        with self.lock:
            pid = max(self.process_table.keys(), default=1000) + 1
            self.process_table[pid] = {
                "name": name,
                "status": "RUNNING",
                "cpu": 0.0,
                "mem": 2.1,
                "capabilities": capabilities
            }
            self.actor_registry[name] = {
                "pid": pid,
                "port": 5000 + len(self.process_table),
                "meta": f"Agent Node - {', '.join(capabilities)}"
            }
            return pid

    def dispatch_ipc_route(self, sender: str, receiver: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        if receiver not in self.actor_registry:
            return {"jsonrpc": "2.0", "error": {"code": -32601, "message": f"Actor '{receiver}' not found"}, "id": None}
        
        self.task_queue.append({
            "sender": sender,
            "receiver": receiver,
            "timestamp": time.time(),
            "payload": payload
        })
        
        msg = payload.get("msg", "")
        use_history = payload.get("use_history", False)

        if receiver == "reasoner_node" or "reasoner" in receiver:
            # Professional status indicator
            status_msg = "[bold cyan]Reasoning (Long Context)...[/bold cyan]" if use_history else "[bold cyan]Reasoning...[/bold cyan]"
            with console.status(status_msg, spinner="dots9"):
                if "search" in msg.lower() or "find" in msg.lower():
                    tool_output = self.tool_executor.run_safe_query(msg)
                    ai_reply = f"**TOOL OUTPUT:**\n> {tool_output}\n\n" + self._call_llm(f"Analyze this tool output: {tool_output}", use_history=use_history)
                else:
                    ai_reply = self._call_llm(msg, use_history=use_history)
            
            return {
                "jsonrpc": "2.0",
                "result": {
                    "status": "COMPLETED",
                    "routing_path": f"kernel -> AI_GATEWAY -> {receiver}",
                    "data": {"agent_reply": ai_reply}
                },
                "id": payload.get("id")
            }

        return {
            "jsonrpc": "2.0",
            "result": {
                "status": "DELIVERED",
                "routing_path": f"kernel -> BrokerIPC -> {receiver}",
                "data": {"agent_reply": f"Default echo from {receiver}: Message received."}
            },
            "id": payload.get("id")
        }

    def run_server(self):
        self.is_running = True
        self.use_history = False # Default state for llmcontinue
        self._show_dashboard()
        
        while self.is_running:
            try:
                mode_label = "[bold green]CONTINUE-ON[/bold green]" if self.use_history else "[dim]CONTINUE-OFF[/dim]"
                prompt = f"{mode_label} [bold blue]YOU[/bold blue] [cyan]»[/cyan] "
                user_input = console.input(prompt).strip()
                if not user_input:
                    continue
                
                if user_input.startswith("/"):
                    parts = user_input[1:].split()
                    cmd = parts[0].lower()
                    args = parts[1:]

                    if cmd == "help":
                        table = Table(title="[bold cyan]SYSTEM MANIFEST[/bold cyan]", box=None)
                        table.add_column("Command", style="green")
                        table.add_column("Description", style="dim")
                        table.add_row("/continue", "Toggle multi-turn conversation memory")
                        table.add_row("/status", "Active agent matrix")
                        table.add_row("/spawn", "Create agent node")
                        table.add_row("/pulse", "System health monitor")
                        table.add_row("/clear", "Reset UI")
                        table.add_row("/exit", "Shutdown kernel")
                        console.print(table)

                    elif cmd == "continue":
                        self.use_history = not self.use_history
                        state = "[bold green]ENABLED[/bold green]" if self.use_history else "[bold red]DISABLED[/bold red]"
                        console.print(f"[i] Conversation memory {state}.[/i]")

                    elif cmd == "status":
                        table = Table(title="[bold cyan]NODE MATRIX[/bold cyan]")
                        table.add_column("PID", style="dim")
                        table.add_column("IDENTITY", style="bold white")
                        table.add_column("STATUS")
                        table.add_column("CPU", style="yellow")
                        table.add_column("MEM", style="magenta")
                        for pid, data in self.process_table.items():
                            status_col = f"[green]{data['status']}[/green]" if data['status'] in ["ACTIVE", "RUNNING"] else f"[red]{data['status']}[/red]"
                            table.add_row(str(pid), data['name'], status_col, f"{data['cpu']}%", f"{data['mem']} MB")
                        console.print(table)

                    elif cmd == "pulse":
                        panel_content = Text()
                        panel_content.append(f"Host:     {os.name.upper()} ({sys.platform})\n", style="white")
                        panel_content.append(f"Memory:   {len(self.process_table) * 2.4:.1f} MB allocated\n", style="green")
                        panel_content.append(f"Traffic:  {len(self.task_queue)} packets processed\n", style="blue")
                        panel_content.append(f"Uptime:   {int(time.time() % 3600)}s session life", style="dim")
                        console.print(Panel(panel_content, title="[bold cyan]SYSTEM PULSE[/bold cyan]", border_style="cyan", width=40))

                    elif cmd == "spawn":
                        if not args:
                            console.print("[red][!] NODE_NAME required.[/red]")
                            continue
                        name = args[0]
                        pid = self.spawn_agent(name, ["user_defined"])
                        console.print(f"[green][✓] Node '{name}' integrated at PID {pid}.[/green]")

                    elif cmd == "tasks":
                        for task in self.task_queue[-5:]:
                            ts = time.strftime('%H:%M:%S', time.localtime(task['timestamp']))
                            console.print(f"[dim][{ts}][/dim] [green]{task['sender']}[/green] -> [blue]{task['receiver']}[/blue]: [italic]{task['payload']['msg'][:30]}...[/italic]")

                    elif cmd == "clear":
                        self._show_dashboard()

                    elif cmd == "exit":
                        console.print("[bold yellow][!] Terminating Microkernel. Signal sent to agents...[/bold yellow]")
                        self.is_running = False

                    else:
                        console.print(f"[red][!] Invalid command: {cmd}[/red]")
                
                else:
                    response = self.dispatch_ipc_route("shell_ui", "reasoner_node", {"msg": user_input, "use_history": self.use_history})
                    if "error" in response:
                        console.print(f"[bold red]ERROR »[/bold red] {response['error']['message']}")
                    else:
                        ai_text = response['result']['data']['agent_reply']
                        console.print(Panel(Markdown(ai_text), title="[bold magenta]AI RESPONSE[/bold magenta]", border_style="magenta", padding=(1, 1)))

            except KeyboardInterrupt:
                console.print("\n[bold yellow][!] Use /exit to shutdown safely.[/bold yellow]")
            except Exception as e:
                console.print(f"[bold red][CRITICAL] {e}[/bold red]")

if __name__ == "__main__":
    kernel = Dxn1Microkernel()
    kernel.spawn_agent("scrapper_agent", ["fs:read", "net:request"])
    kernel.spawn_agent("reasoner_node", ["llm:cognitive"])
    kernel.run_server()
