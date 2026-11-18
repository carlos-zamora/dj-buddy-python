# Assistant evals

Evaluations of the set-planning assistant, built with pydantic-evals (P2-4). Mark them with
`@pytest.mark.evals`.

- **Deterministic checks gate CI:** only real track IDs, set length within 1 of the request,
  BPM ramp respected, at least 80% harmonic transitions, no repeated tracks.
- **Offline by default:** every push runs these against Pydantic AI's test model.
- **Live model nightly:** a scheduled job runs the same dataset against a real model with a key
  from a GitHub secret. A judge score for "fits the brief" is reported but never gates.
