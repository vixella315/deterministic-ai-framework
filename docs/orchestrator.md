# Orchestrator

The orchestrator coordinates provider → parse → validate → classify → repair or stop → revalidate → accept.

Provider output remains untrusted. Repair execution alone never constitutes acceptance; repaired output must pass validation again.