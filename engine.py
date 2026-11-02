from .tools import TOOL_CATALOG, ROLE_LEVEL
SENSITIVE_KEYS = {"password","secret","api_key","token","private_key"}
class SecurityEngine:
    def evaluate(self, agent, role, tool, arguments, reason):
        checks=[]
        meta=TOOL_CATALOG.get(tool)
        if not meta:
            return self.result("DENIED","Tool is not registered",100,[{"name":"Tool registry","passed":False,"detail":"Unknown tool"}])
        checks.append({"name":"Registered tool","passed":True,"detail":"Tool exists in local catalog"})
        ok=ROLE_LEVEL.get(role,0) >= ROLE_LEVEL[meta["role"]]
        checks.append({"name":"Role permission","passed":ok,"detail":f"{meta['role']} required; requester is {role}"})
        if not ok: return self.result("DENIED","Role does not have permission",90,checks)
        has_reason=bool(reason and reason.strip())
        checks.append({"name":"Purpose supplied","passed":has_reason,"detail":"Reason is required for accountability"})
        if not has_reason: return self.result("DENIED","Provide a reason",75,checks)
        secret=bool({str(k).lower() for k in arguments} & SENSITIVE_KEYS)
        checks.append({"name":"No credential-like arguments","passed":not secret,"detail":"Credential fields prohibited" if secret else "No obvious secret fields found"})
        if secret: return self.result("DENIED","Request contains a prohibited credential field",100,checks)
        risk={"low":10,"medium":35,"high":70,"critical":90}[meta["risk"]]
        checks.append({"name":"Risk classification","passed":risk<70,"detail":f"{meta['risk']} risk maps to {risk}/100"})
        if risk>=70: return self.result("NEEDS_APPROVAL","High-risk operation requires human approval",risk,checks)
        return self.result("ALLOWED","All mandatory policy checks passed",risk,checks)
    @staticmethod
    def result(status,message,risk,checks):
        return {"status":status,"message":message,"risk_score":risk,"checks":checks}
