import sqlite3, json
from pathlib import Path
from datetime import datetime, timezone
DB=Path("data/trustbridge_audit.db")
class AuditStore:
    def __init__(self):
        DB.parent.mkdir(exist_ok=True)
        with sqlite3.connect(DB) as c:
            c.execute("CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY, created_at TEXT, agent TEXT, role TEXT, tool TEXT, arguments TEXT, decision TEXT)")
    def record(self,agent,role,tool,args,decision):
        with sqlite3.connect(DB) as c:
            c.execute("INSERT INTO events(created_at,agent,role,tool,arguments,decision) VALUES(?,?,?,?,?,?)",
              (datetime.now(timezone.utc).isoformat(),agent,role,tool,json.dumps(args),json.dumps(decision)))
    def recent(self,limit=20):
        with sqlite3.connect(DB) as c:
            rows=c.execute("SELECT created_at,agent,role,tool,decision FROM events ORDER BY id DESC LIMIT ?",(limit,)).fetchall()
        return [{"Time (UTC)":r[0],"Agent":r[1],"Role":r[2],"Tool":r[3],"Decision":json.loads(r[4]).get("status")} for r in rows]
