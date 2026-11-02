TOOL_CATALOG = {
 "search_public_docs":{"description":"Search a public documentation index","risk":"low","role":"viewer","example":'{"query":"MCP security"}'},
 "read_customer_record":{"description":"Read a simulated customer support record","risk":"medium","role":"analyst","example":'{"customer_id":"C-1042"}'},
 "send_external_message":{"description":"Send a simulated external message","risk":"high","role":"admin","example":'{"recipient":"review@example.com","message":"Please review"}'},
 "export_finance_data":{"description":"Export simulated finance data","risk":"critical","role":"admin","example":'{"period":"Q3","format":"csv"}'}
}
ROLE_LEVEL = {"viewer":1,"analyst":2,"admin":3}
def run_mock_tool(tool_name, arguments):
    if tool_name == "search_public_docs":
        return {"results":["MCP overview","Tool authorization checklist"],"query":arguments.get("query","")}
    if tool_name == "read_customer_record":
        return {"customer_id":arguments.get("customer_id"),"status":"open","demo_data":True}
    if tool_name == "send_external_message":
        return {"sent":True,"recipient":arguments.get("recipient"),"simulation":True}
    if tool_name == "export_finance_data":
        return {"export_id":"DEMO-EXPORT-001","period":arguments.get("period"),"simulation":True}
    return {"error":"Unknown tool"}
