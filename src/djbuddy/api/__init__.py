"""The FastAPI service.

What lives here (from P2-1):
    - The app factory, routers for the library, tracks, sets and recommendations, and the
      Pydantic request and response schemas.
    - A consistent error model. The OpenAPI schema is snapshot-tested because the React
      editor's TypeScript client is generated from it.

Routers stay thin: they validate input, call repositories and core functions, and shape the
response.
"""
