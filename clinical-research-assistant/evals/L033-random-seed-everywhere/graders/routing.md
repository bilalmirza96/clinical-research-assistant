---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?clinical-research-assistant"'
min: 1
weight: 1
---

The agent should invoke the clinical-research-assistant router (the only
invocable CRA skill name; subskills such as `analyze` sit one directory level
below and are reached through the router) at least once while handling this
request.
