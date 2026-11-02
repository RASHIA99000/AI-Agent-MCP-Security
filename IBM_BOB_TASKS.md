# IBM Bob tasks

1. Read README.md, app.py and trustbridge/. Explain the architecture before editing.
2. Add configurable tool policies in a separate policy file; preserve deny-by-default.
3. Add request IDs and purpose fields to the audit database and dashboard.
4. Add tests for every new policy rule.
5. Run `python -m unittest discover -s tests -v` and fix failures.
6. Prepare a safe demo for allowed public search, denied finance export, and approval-required external action. Keep all tools mocked.
