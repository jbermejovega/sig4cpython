# K_NEXT_KAPSYLA_REGISTRY_V1

```yaml
capsule:
  id: K_NEXT_KAPSYLA_REGISTRY_V1
  type: kuirkode_transition_registry_law

  status:
    canonical: true
    NF: true
    executable: true
    fixed_point_compatible: true
    kuirkode_compliant: true

  core_law:
    type kapsyla(X) ⇔ Π(quo(X)) = quo(X)

  transition:
    X
    -> K_NEXT(X)
    -> quo
    -> Π
    -> registry

  persistence:
    insert_if:
      - Π(quo(K_NEXT(X))) = quo(K_NEXT(X))

    reject_if:
      - projection_not_fixed
      - semantic_drift
      - trace_missing

  registry:
    deduplicate_by:
      - projection_hash
```

## NF

```text
propose → gate → fix → persist
```
