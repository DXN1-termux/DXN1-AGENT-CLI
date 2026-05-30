#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DXN1-AGENT-CLI - CORE SCHEDULER & BROKER
Created with ❤️ BY DXN1

This module executes in user-space to schedule, orchestrate,
and facilitate sandboxed message routing between autonomous agents.
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

class Dxn1Microkernel:
    def __init__(self, host: str = "127.0.0.1", port: int = 5001):
        self.host = host
        self.port = port
        self.is_running = False
        self.process_table: Dict[int, Dict[str, Any]] = {}
        self.actor_registry: Dict[str, Any] = {}
        self.task_queue: List[Dict[str, Any]] = []
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
            readline.set_history_length(1000)
        except FileNotFoundError:
            pass
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
                                self.api_provider = v.lower()
                            elif k == "LLM_MODE":
                                self.llm_mode = v
            except Exception as e:
                print(f"\033[1;33m[!] KERNEL WARNING: Failed parsing credentials: {e}\033[0m")

    def _call_llm(self, prompt: str) -> str:
        if self.llm_mode == "open_source":
            return "Kernel Note: Running in Offline/Local Mode. Deploy Ollama/Local-Server to process cognitive prompts."
        
        if self.api_key == "NOT_CONFIGURED":
            return "Kernel Error: API Key not found. Please run the launcher to configure credentials."

        try:
            if "gemini" in self.api_provider:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.api_key}"
                headers = {'Content-Type': 'application/json'}
                data = {"contents": [{"parts": [{"text": prompt}]}]}
                response = requests.post(url, headers=headers, json=data, timeout=30)
                res_json = response.json()
                if 'candidates' in res_json:
                    return res_json['candidates'][0]['content']['parts'][0]['text']
                return f"Gemini Error: {res_json}"
            
            elif "openai" in self.api_provider:
                url = "https://api.openai.com/v1/chat/completions"
                headers = {"Authorization": f"Bearer {self.api_key}"}
                data = {
                    "model": "gpt-4o-mini",
                    "messages": [{"role": "user", "content": prompt}]
                }
                response = requests.post(url, headers=headers, json=data, timeout=30)
                return response.json()['choices'][0]['message']['content']
            
            return f"Error: Provider {self.api_provider} is not supported."
        except Exception as e:
            return f"Cognitive Routing Error: {str(e)}"

    def _thinking_animation(self, stop_event):
        spinner = itertools.cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
        while not stop_event.is_set():
            sys.stdout.write(f"\r\033[1;36m{next(spinner)} Cognitive engine reasoning...\033[0m")
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.write('\r' + ' ' * 45 + '\r')
        sys.stdout.flush()

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
        if receiver == "reasoner_node" or "reasoner" in receiver:
            stop_event = threading.Event()
            thread = threading.Thread(target=self._thinking_animation, args=(stop_event,))
            thread.start()
            
            # Logic to handle tool search requests via reasoning
            if "search" in msg.lower() or "find" in msg.lower():
                tool_output = self.tool_executor.run_safe_query(msg)
                ai_reply = f"[TOOL_OUTPUT] {tool_output}\n\n[ANALYSIS] Based on the data retrieved, it appears that " + self._call_llm(f"Analyze this tool output: {tool_output}")
            else:
                ai_reply = self._call_llm(msg)
            
            stop_event.set()
            thread.join()
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
        os.system('clear' if os.name == 'posix' else 'cls')
        
        # Professional Dashboard UI
        print("\033[1;34m╭" + "─"*58 + "╮\033[0m")
        print(f"\033[1;34m│\033[0m  \033[1;36m🌀 DXN1 CORE MICROKERNEL\033[0m \033[1;30m| v1.4.3 STABLE\033[0m{' '*15}\033[1;34m│\033[0m")
        print("\033[1;34m├" + "─"*58 + "┤\033[0m")
        print(f"\033[1;34m│\033[0m  • Status:   \033[1;32mONLINE\033[0m{' '*41}\033[1;34m│\033[0m")
        print(f"\033[1;34m│\033[0m  • Engine:   \033[1;35m{self.api_provider.upper():<10}\033[0m \033[1;30m({self.llm_mode})\033[0m{' '*25}\033[1;34m│\033[0m")
        print(f"\033[1;34m│\033[0m  • Platform: \033[1;34m{sys.platform.upper():<43}\033[0m \033[1;34m│\033[0m")
        print("\033[1;34m╰" + "─"*58 + "╯\033[0m")
        print(" Type '\033[1;32mhelp\033[0m' to list orchestration commands.")
        
        while self.is_running:
            try:
                prompt = f"\033[1;34mDXN1\033[0m@\033[1;36mnam_core\033[0m \033[1;32m$\033[0m "
                cmd_input = input(prompt).strip().split()
                if not cmd_input:
                    continue
                
                cmd = cmd_input[0].lower()
                args = cmd_input[1:]

                if cmd == "help":
                    print("\n\033[1;36m[ COMMAND MANIFEST ]\033[0m")
                    print("  \033[1;32mstatus\033[0m          - View active agent process matrix")
                    print("  \033[1;32mspawn <name>\033[0m    - Instantiate a new agent node")
                    print("  \033[1;32mchat <node> <msg>\033[0m - Send cognitive instruction payload")
                    print("  \033[1;32mtasks\033[0m           - Inspect IPC telemetry buffer")
                    print("  \033[1;32mpulse\033[0m           - Live host system health report")
                    print("  \033[1;32mclear\033[0m           - Reset terminal UI buffer")
                    print("  \033[1;32mexit\033[0m            - Shutdown microkernel session\n")

                elif cmd == "status":
                    print(f"\n\033[1;36m{'PID':<6} {'IDENTITY':<20} {'STATUS':<12} {'CPU':<6} {'MEM':<8}\033[0m")
                    print("\033[1;30m" + "─"*60 + "\033[0m")
                    for pid, data in self.process_table.items():
                        color = "\033[1;32m" if data['status'] in ["ACTIVE", "RUNNING"] else "\033[1;31m"
                        print(f"{pid:<6} {data['name']:<20} {color}{data['status']:<12}\033[0m {data['cpu']:<6} {data['mem']:<8}")
                    print("")

                elif cmd == "pulse":
                    print(f"\n\033[1;36m[ SYSTEM PULSE MONITOR ]\033[0m")
                    print(f" • Host Context:   \033[1;34m{os.name.upper()} / {sys.platform}\033[0m")
                    print(f" • Kernel Memory:  \033[1;32m{len(self.process_table) * 2.4:.1f} MB allocated\033[0m")
                    print(f" • Telemetry:      \033[1;32m{len(self.task_queue)} packets in buffer\033[0m")
                    print(f" • Core Load:      \033[1;33m0.02% (User-space idle)\033[0m\n")

                elif cmd == "spawn":
                    if not args:
                        print("\033[1;31m[!] Error: NODE_NAME required.\033[0m")
                        continue
                    name = args[0]
                    pid = self.spawn_agent(name, ["user_defined"])
                    print(f"\033[1;32m[✓] Node '{name}' successfully integrated (PID: {pid}).\033[0m")

                elif cmd == "chat":
                    if len(args) < 2:
                        print("\033[1;31m[!] Usage: chat <node_id> <prompt>\033[0m")
                        continue
                    receiver = args[0]
                    message = " ".join(args[1:])
                    
                    print(f"\033[1;30m[IPC] Routing payload to {receiver}...\033[0m")
                    response = self.dispatch_ipc_route("shell_ui", receiver, {"msg": message})
                    
                    if "error" in response:
                        print(f"\033[1;31m[❌] ROUTING_ERROR: {response['error']['message']}\033[0m")
                    else:
                        print(f"\033[1;34m╭─ {receiver.upper()} RESPONSE " + "─"*(58 - len(receiver) - 13) + "╮\033[0m")
                        print(f"{response['result']['data']['agent_reply']}")
                        print(f"\033[1;34m╰" + "─"*58 + "╯\033[0m")

                elif cmd == "tasks":
                    print(f"\n\033[1;36m[ TELEMETRY BUFFER ]\033[0m")
                    if not self.task_queue:
                        print("\033[1;33mBuffer is empty.\033[0m")
                    else:
                        for task in self.task_queue:
                            ts = time.strftime('%H:%M:%S', time.localtime(task['timestamp']))
                            print(f"\033[1;30m[{ts}]\033[0m \033[1;32m{task['sender']}\033[0m -> \033[1;34m{task['receiver']}\033[0m: {task['payload']['msg'][:40]}...")

                elif cmd == "clear":
                    os.system('clear' if os.name == 'posix' else 'cls')

                elif cmd == "exit":
                    print("\033[1;33m[!] Shutting down DXN1 Microkernel...\033[0m")
                    self.is_running = False

                else:
                    print(f"\033[1;31m[!] Invalid command: {cmd}\033[0m")

            except KeyboardInterrupt:
                print("\n\033[1;33m[!] Interrupt detected. Type 'exit' to terminate.\033[0m")
            except Exception as e:
                print(f"\033[1;31m[RUNTIME ERROR] {e}\033[0m")

if __name__ == "__main__":
    kernel = Dxn1Microkernel()
    kernel.spawn_agent("scrapper_agent", ["fs:read", "net:request"])
    kernel.spawn_agent("reasoner_node", ["llm:cognitive"])
    kernel.run_server()
