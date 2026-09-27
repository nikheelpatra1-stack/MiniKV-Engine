import socket
import json
import os
import time

class MiniKVStore:
    def __init__(self, host='127.0.0.1', port=6379, snapshot_file='db_snapshot.json'):
        self.host = host
        self.port = port
        self.snapshot_file = snapshot_file
        self.store = {}
        self.stats = {"total_queries": 0, "sets": 0, "gets": 0, "dels": 0, "start_time": time.time()}
        self._load_from_disk()

    def _load_from_disk(self):
        if os.path.exists(self.snapshot_file):
            try:
                with open(self.snapshot_file, 'r') as f:
                    self.store = json.load(f)
                print(f"[INIT] Loaded {len(self.store)} keys from {self.snapshot_file}")
            except Exception as e:
                print(f"[WARNING] Could not load snapshot: {e}")

    def _save_to_disk(self):
        try:
            with open(self.snapshot_file, 'w') as f:
                json.dump(self.store, f, indent=2)
        except Exception as e:
            print(f"[ERROR] Persistence failed: {e}")

    def execute_command(self, raw_cmd):
        self.stats["total_queries"] += 1
        parts = raw_cmd.strip().split(maxsplit=2)
        if not parts:
            return "ERROR: Empty command\n"

        cmd = parts[0].upper()

        if cmd == "SET":
            if len(parts) < 3:
                return "ERROR: Usage -> SET <key> <value>\n"
            key, val = parts[1], parts[2]
            self.store[key] = val
            self.stats["sets"] += 1
            self._save_to_disk()
            return f"OK (Key '{key}' stored successfully)\n"

        elif cmd == "GET":
            if len(parts) < 2:
                return "ERROR: Usage -> GET <key>\n"
            key = parts[1]
            self.stats["gets"] += 1
            val = self.store.get(key)
            if val is None:
                return "(nil) Key not found\n"
            return f"{val}\n"

        elif cmd == "DEL":
            if len(parts) < 2:
                return "ERROR: Usage -> DEL <key>\n"
            key = parts[1]
            self.stats["dels"] += 1
            if key in self.store:
                del self.store[key]
                self._save_to_disk()
                return f"OK (Key '{key}' deleted)\n"
            return "(integer) 0 (Key did not exist)\n"

        elif cmd == "KEYS":
            keys_list = list(self.store.keys())
            return f"Keys ({len(keys_list)}): {', '.join(keys_list)}\n"

        elif cmd == "STATS":
            uptime = int(time.time() - self.stats["start_time"])
            res = (
                f"--- DATABASE METRICS ---\n"
                f"Uptime: {uptime}s\n"
                f"Total Keys Stored: {len(self.store)}\n"
                f"Total Queries: {self.stats['total_queries']}\n"
                f"GETs: {self.stats['gets']} | SETs: {self.stats['sets']} | DELs: {self.stats['dels']}\n"
            )
            return res

        else:
            return f"ERROR: Unknown command '{cmd}'. Available: SET, GET, DEL, KEYS, STATS\n"

    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self.host, self.port))
        server.listen(5)
        print(f"==========================================")
        print(f" MiniKV Engine Running on {self.host}:{self.port}")
        print(f" Persistence File: {self.snapshot_file}")
        print(f"==========================================")

        try:
            while True:
                conn, addr = server.accept()
                data = conn.recv(1024).decode('utf-8')
                if data:
                    response = self.execute_command(data)
                    conn.sendall(response.encode('utf-8'))
                conn.close()
        except KeyboardInterrupt:
            print("\n[SHUTDOWN] Database server stopped cleanly.")
            server.close()

if __name__ == "__main__":
    db = MiniKVStore()
    db.start()