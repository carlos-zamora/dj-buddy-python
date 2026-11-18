"""The LLM set-planning assistant (Pydantic AI).

What lives here (from P2-3):
    - The agent definition, its system prompt and its structured ``SetPlan`` output.
    - Tools the agent may call. Tools return track IDs and facts. Deterministic code in
      ``djbuddy.core`` does the BPM maths and ordering ("give the assistant access, not
      intelligence").

Rules:
    - Unit and integration tests use Pydantic AI's offline test model and need no API key.
    - Live-model evaluations live in ``tests/evals`` and run on a schedule, not on every push.
"""
