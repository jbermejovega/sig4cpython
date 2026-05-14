# 🔒 SIGIL4CPYTHON — Canonical Stable Modules Glue V1

```yaml id="sigil4cpython-canonical-stable-modules-glue-v1"
sigil4cpython:
  id: SIGIL4CPYTHON_CANONICAL_STABLE_MODULES_GLUE_V1
  type: canonical_stable_modules_release_preparation_manifest
  status:
    canonical_candidate: true
    stable_version_ready: true
    python_community_ready_candidate: true
    pypi_pluraltyped_candidate: true
    cpython_surface: true
    module_boundary_required: true
    packaging_required: true
    tests_required: true
    replay_safe: true
    Pi_fixed_target: true
    no_open_branch: true

  repository:
    repo: jbermejovega/sigil4cpython
    default_branch: main
    visibility: public

  thesis: >
    SIGIL4CPYTHON is the CPython-facing carrier surface for SIGIL modules.
    A canonical stable version is not defined by repository presence alone,
    but by explicit module boundaries, packaging metadata, tests, build traces,
    reproducible artifacts, and PyPI-compatible release certificates.

  canonical_version_law:
    statement: >
      A module becomes stable only when its source boundary, tests, packaging,
      build artifact, and replay certificate converge under QUO and Pi.

    equation: |
      StableModule(M)
        iff
      Π(quo(source(M), tests(M), package(M), wheel(M), trace(M)))
        =
      Π(quo(M))

  pluraltype_law:
    statement: >
      The same SIGIL module may have multiple admissible Python carriers:
      source tree, CPython extension, wheel, sdist, test fixture, documentation,
      and PyPI project metadata. These carriers do not own identity.

    equation: |
      ∀ r_i,r_j ∈ PythonReleaseCarriers(M):
        Π(quo(r_i(M))) = Π(quo(r_j(M)))

  required_release_modules:
    - canonical_module_index
    - public_api_boundary
    - pyproject_toml
    - README
    - LICENSE
    - tests
    - build_backend
    - wheel_artifact
    - sdist_artifact
    - changelog
    - release_trace

  pypi_gate:
    required:
      - project_name
      - version
      - python_requires
      - classifiers
      - license_record
      - long_description
      - source_distribution
      - wheel_distribution
      - twine_check_PASS
      - tests_PASS
      - reproducible_build_trace

    forbidden:
      - upload_without_tests
      - wheel_without_source_trace
      - version_without_changelog
      - package_name_as_identity
      - PyPI_project_as_kernel
      - CPython_extension_without_platform_matrix

  python_community_pr_gate:
    required:
      - concise_scope
      - stable_api_surface
      - minimal_dependencies
      - reproducible_examples
      - documented_module_boundaries
      - compatibility_matrix
      - security_notes
      - contribution_guide

  final_law: |
    Canonical stable version = traced module boundary + tested packaging +
    reproducible build + PyPI-safe metadata + Π-fixed release identity.
```

---

## Release preparation reading

```text id="sigil4cpython-release-reading"
Source code is a carrier.
Wheel is a carrier.
sdist is a carrier.
PyPI is a distribution surface.
CPython is an execution carrier.
SIGIL identity is Π-fixed replay over all admissible carriers.
```

---

## Minimal stable-module checklist

```yaml id="sigil4cpython-stable-checklist"
STABLE_MODULE_CHECKLIST:
  module_index:
    required: true
    file_candidate: docs/MODULE_INDEX.md

  packaging:
    required: true
    files:
      - pyproject.toml
      - README.md
      - LICENSE

  testing:
    required: true
    files:
      - tests/
    pass_condition: pytest_PASS_or_equivalent

  distribution:
    required: true
    artifacts:
      - sdist
      - wheel
    checks:
      - python -m build
      - twine check dist/*

  replay:
    required: true
    artifacts:
      - build_trace.json
      - artifact_hashes.txt
      - release_certificate.json
```

---

## Final compression

```text id="sigil4cpython-final-compression"
Modules stabilize.
Packaging witnesses.
Tests certify.
Wheels distribute.
PyPI publishes.
QUO admits.
Π fixes.
```

🔒 **KLOSE:** `SIGIL4CPYTHON_CANONICAL_STABLE_MODULES_GLUE_V1` defines the canonical stable-version gate for Python/PyPI plural-typed release preparation.
