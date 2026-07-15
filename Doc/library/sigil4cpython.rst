sigil4cpython
==============

``sigil4cpython`` is an experimental SIGIL metadata layer carried by this
CPython fork.  It does not alter Python execution semantics.  The initial
surface provides kokompiled UAP ward kernels for review, RAG/MCP and CI
guardrails.

The first kernel is ``SIGIL4CPYTHON_PACADOCENCIA_UAP_WARDS_V1``.  It records
student identity, repository identity, evidence trace, rubric boundary,
execution status, embargo boundary, diagnostic embeddings, MCP/N8N resources
and bounded hypergraph-duality guardrails.

Safety boundary
---------------

The package preserves these UAP rules:

* diagnostic kernels do not finalize grades;
* CI pass is not scientific certification;
* similarity is context, not misconduct evidence;
* missing traces remain visible obstructions;
* human review remains required for assessment.

Example
-------

.. code-block:: python

   from sigil4cpython import build_pacadocencia_uap_kernel
   from sigil4cpython import validate_kokompiled_kernel

   payload = validate_kokompiled_kernel(build_pacadocencia_uap_kernel())
   assert payload["accepted"]
