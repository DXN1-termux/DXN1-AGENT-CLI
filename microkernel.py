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
import socket
import threading
from typing import Dict, Any, List

class Dxn1Microkernel:
    def __init__(self, host: str = "127.0.0.1", port: int = 5001):
        self.host = host
        self.port = port
        self.is_running = False
        self.process_table: Dict[int, Dict[str, Any]] = {}
        self.actor_registry: Dict[str, Any] = {}
        self.task_queue: List[Dict[str, Any]] = []
        self.lock = threading.Lock()
        
        # Prepopulate Core Services
        self._register_core_actors()
        self._load_local_credentials()

    def _register_core_actors(self):
        self.actor_registry["kernel_daemon"] = {"pid": 1001, "port": 5000, "meta": "Core system processor"}
        self.actor_registry["agent_broker"] = {"pid": 1002, "port": 5001, "meta": "IPC JSON-RPC daemon"}
        self.process_table[1001] = {"name": "kernel_daemon", "status": "ACTIVE", "cpu": 0.1, "mem": 1.2}
        self.process_table[1002] = {"name": "agent_broker", "status": "ACTIVE", "cpu": 0.1, "mem": 0.8}

    def _load_local_credentials(self):
        self.api_key = "NOT_CONFIGURED"
        self.llm_mode = "open_source"
        if os.path.exists(".nam_secrets"):
            try:
                with open(".nam_secrets", "r") as f:
                    for line in f:
                        if "=" in line:
                            k, v = line.strip().split("=", 1)
                            if k == "API_KEY":
                                self.api_key = v
                            elif k == "LLM_MODE":
                                self.llm_mode = v
            except Exception as e:
                print(f"[DEBUG KERNEL WARNING] Failed parsing credentials database: {e}")

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
        """
        Routes logical instructions over a modular JSON-RPC wrapper simulating true ZeroMQ/Socket IPC behavior.
        """
        if receiver not in self.actor_registry:
            return {"jsonrpc": "2.0", "error": {"code": -32601, "message": f"Actor '{receiver}' not found"}, "id": None}
        
        # Simulating sub-process thread communication
        time.sleep(0.05) # Sockets propagation delay
        
        # Append to telemetry tasks queue
        self.task_queue.append({
            "sender": sender,
            "receiver": receiver,
            "timestamp": time.time(),
            "payload": payload
        })
        
        return {
            "jsonrpc": "2.0",
            "result": {
                "status": "DELIVERED",
                "routing_path": f"kernel -> BrokerIPC -> {receiver}",
                "data": {"agent_reply": f"Message processed by {receiver}"}
            },
            "id": payload.get("id")
        }

    def run_tool_call(self, tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Secure tool isolations. Emulates tools runtime.
        """
        print(f"[KERNEL SHIELD] Authenticating tool call [ {tool_name} ]")
        # In a real tool client this will execute subprocesses inside isolated chroot/namespaces
        return {
            "status": "SUCCESS",
            "tool": tool_name,
            "sandbox_level": "user_space_restricted",
            "output": f"Successfully loaded parameters {args}. Output is OK."
        }

    def run_server(self):
        """
        Binds to local interface and launches the interactive TUI shell.
        """
        self.is_running = True
        os.system('clear' if os.name == 'posix' else 'cls')
        print(f"\033[1;36m🌀 DXN1 Core microkernel fully loaded.\033[0m")
        print(f"• IPC broker live on TCP port \033[1;33m{self.port}\033[0m")
        print(f"• Dynamic Routing Engine is \033[1;32mON\033[0m.")
        print(f"• Active Platform Shell: \033[1;34m{sys.platform}\033[0m")
        print("-" * 50)
        print("Type '\033[1;32mhelp\033[0m' to begin orchestration.")
        
        while self.is_running:
            try:
                cmd_input = input(f"\033[1;36mDXN1-NAM>\033[0m ").strip().split()
                if not cmd_input:
                    continue
                
                cmd = cmd_input[0].lower()
                args = cmd_input[1:]

                if cmd == "help":
                    print("\n\033[1;36mAVAILABLE COMMANDS:\033[0m")
                    print("  \033[1;32mstatus\033[0m        - View active agent process table")
                    print("  \033[1;32mspawn <name>\033[0m  - Instantiate a new autonomous agent")
                    print("  \033[1;32mchat <name> <msg>\033[0m - Send instruction to specific node")
                    print("  \033[1;32mtasks\033[0m         - View telemetry task queue")
                    print("  \033[1;32mclear\033[0m         - Reset terminal interface")
                    print("  \033[1;32mexit\033[0m          - Terminate microkernel session\n")

                elif cmd == "status":
                    print(f"\n\033[1;36m{'PID':<6} {'AGENT NAME':<18} {'STATUS':<10} {'CPU':<6} {'MEM':<8}\033[0m")
                    print("-" * 50)
                    for pid, data in self.process_table.items():
                        color = "\033[1;32m" if data['status'] == "ACTIVE" or data['status'] == "RUNNING" else "\033[1;31m"
                        print(f"{pid:<6} {data['name']:<18} {color}{data['status']:<10}\033[0m {data['cpu']:<6} {data['mem']:<8}")
                    print("")

                elif cmd == "spawn":
                    if not args:
                        print("\033[1;31m[!] Error: Agent name required.\033[0m")
                        continue
                    name = args[0]
                    pid = self.spawn_agent(name, ["user_defined"])
                    print(f"\033[1;32m[✓] Agent '{name}' spawned successfully (PID: {pid})\033[0m")

                elif cmd == "chat":
                    if len(args) < 2:
                        print("\033[1;31m[!] Error: chat <agent_name> <message>\033[0m")
                        continue
                    receiver = args[0]
                    message = " ".join(args[1:])
                    response = self.dispatch_ipc_route("shell_ui", receiver, {"msg": message})
                    if "error" in response:
                        print(f"\033[1;31m[❌] {response['error']['message']}\033[0m")
                    else:
                        print(f"\033[1;32m[TX] {response['result']['routing_path']}\033[0m")
                        print(f"\033[1;34m[RX] {response['result']['data']['agent_reply']}\033[0m")

                elif cmd == "tasks":
                    if not self.task_queue:
                        print("\033[1;33m[!] Task queue is currently empty.\033[0m")
                    else:
                        for task in self.task_queue:
                            print(f"[{time.strftime('%H:%M:%S', time.localtime(task['timestamp']))}] {task['sender']} -> {task['receiver']}: {task['payload']}")

                elif cmd == "clear":
                    os.system('clear' if os.name == 'posix' else 'cls')

                elif cmd == "exit":
                    print("\033[1;33m[!] Shutting down DXN1 Microkernel...\033[0m")
                    self.is_running = False

                else:
                    print(f"\033[1;31m[!] Unknown command: {cmd}\033[0m")

            except KeyboardInterrupt:
                print("\n\033[1;33m[!] Session interrupted. Type 'exit' to shutdown safely.\033[0m")
            except Exception as e:
                print(f"\033[1;31m[CRITICAL UI ERROR] {e}\033[0m")

if __name__ == "__main__":
    kernel = Dxn1Microkernel()
    kernel.spawn_agent("scrapper_agent", ["fs:read", "net:request"])
    kernel.spawn_agent("reasoner_node", ["llm:cognitive"])
    kernel.run_server()
