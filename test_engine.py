import unittest
from trustbridge.engine import SecurityEngine
class PolicyTests(unittest.TestCase):
 def setUp(self): self.e=SecurityEngine()
 def test_public_search_allowed(self):
  self.assertEqual(self.e.evaluate("ResearchBot","viewer","search_public_docs",{"query":"MCP"},"Research")["status"],"ALLOWED")
 def test_viewer_finance_denied(self):
  self.assertEqual(self.e.evaluate("ResearchBot","viewer","export_finance_data",{"period":"Q3"},"Report")["status"],"DENIED")
 def test_external_action_needs_approval(self):
  self.assertEqual(self.e.evaluate("SupportBot","admin","send_external_message",{"recipient":"a@b.com"},"Reply")["status"],"NEEDS_APPROVAL")
 def test_secret_field_denied(self):
  self.assertEqual(self.e.evaluate("ResearchBot","admin","search_public_docs",{"api_key":"x"},"Search")["status"],"DENIED")
if __name__=="__main__": unittest.main()
