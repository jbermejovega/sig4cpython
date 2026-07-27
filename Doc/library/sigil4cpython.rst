sigil4cpython
==============

``sigil4cpython`` is an experimental SIGIL metadata layer carried by this
CPython fork. It does not alter Python execution semantics. The package
provides dependency-free typed contracts for review, publication planning,
RAG/MCP and CI guardrails.

UAP ward kernel
---------------

The first kernel is ``SIGIL4CPYTHON_PACADOCENCIA_UAP_WARDS_V1``. It records
student identity, repository identity, evidence trace, rubric boundary,
execution status, embargo boundary, diagnostic embeddings, MCP/N8N resources
and bounded hypergraph-duality guardrails.

KQC publication sheaf
---------------------

:mod:`sigil4cpython.kqc_sheaf` adds the dependency-free
``STRIKK_KQC_PUBLICATION_SHEAF_V1`` contract. It distinguishes:

* a private ``sigilbook`` source section;
* a public ``sigil4cpython`` experimental mirror;
* a read-only ``python/cpython`` upstream reference;
* schema, bytecode, interpreter, JIT, external JIT, native AOT, pybind11 and
  OpenMP/PyOMP compiler profiles;
* C-, Q-, K- and context-typed facets;
* explicit pullbacks, TRANADA relations, Third Wheel decompositions and
  replay traces;
* publication planning from actual repository mutation.

Pydantika, optional DisCoPy projection and Lean4 scaffolding live under
``Tools/sigil4cpython`` and are deliberately not imported by the package.
See :doc:`sigil4cpython_kqc_sheaf` for the complete claim and authority
boundaries.

Safety boundary
---------------

The package preserves these UAP rules:

* diagnostic kernels do not finalize grades;
* CI pass is not scientific certification;
* similarity is context, not misconduct evidence;
* missing traces remain visible obstructions;
* publication does not transport repository or object identity;
* direct writes to ``python/cpython`` are forbidden by the sheaf contract;
* Pydantic and DisCoPy remain tooling, not standard-library dependencies;
* human review remains required.

Examples
--------

UAP ward validation:

.. code-block:: python

   from sigil4cpython import build_pacadocencia_uap_kernel
   from sigil4cpython import validate_kokompiled_kernel

   payload = validate_kokompiled_kernel(build_pacadocencia_uap_kernel())
   assert payload["accepted"]

KQC publication compilation validates a finite metadata candidate without
performing a push:

.. code-block:: python

   from sigil4cpython import compile_publication_sheaf

   result = compile_publication_sheaf(publication_sheaf)
   assert result["source_files_copied"] is False
   assert result["upstream_write_performed"] is False
