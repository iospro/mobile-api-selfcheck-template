# YAML contracts in demo template

This folder mirrors the contract layer from the production `api-tests` project.

- `contracts/methods/*` describe request shape and envelope mode per method.
- `contracts/dto/*` keep DTO notes close to method contracts.

In this offline demo, method contracts are checked at runtime before DTO validators:

1. request `method/path` matches `ApiMethodSpec`;
2. `uses_envelope` matches method expectation.

DTO files here are intentionally lightweight and serve as documentation anchors
for expanding the template.
