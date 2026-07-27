SIGIL4CPython STRIKK/KQC publication sheaf
===========================================

.. module:: sigil4cpython.kqc_sheaf
   :synopsis: Dependency-free publication and compiler-classification contract.

Status and scope
----------------

``STRIKK_KQC_PUBLICATION_SHEAF_V1`` is an experimental, review-gated
contract for representing three different repository sections:

* ``jbermejovega/sigilbook`` as a private source atlas;
* ``jbermejovega/sigil4cpython`` as a public experimental projection;
* ``python/cpython`` as a read-only upstream reference and possible future
  contribution target.

The contract does not copy source files, push a branch, open an upstream pull
request, execute a compiler, or modify CPython interpreter semantics.  A valid
publication sheaf is a finite metadata and proof-obligation witness.

Authority boundary
------------------

The current GitHub authority boundary is strict:

* the owner may write to ``sigilbook`` and ``sigil4cpython``;
* the upstream ``python/cpython`` repository is not writable through this
  contract;
* every ``sigil4cpython -> python/cpython`` hop must therefore have
  ``authority = PLAN_ONLY`` and ``direct_upstream_write = false``.

An upstream proposal would require a separately reduced patch that follows the
CPython Developer Guide, issue and review process, test requirements, news
requirements, maintenance expectations, and accepted project scope.

Sheaf presentation
------------------

Let :math:`\mathcal C_{\mathrm{pub}}` be the finite category of publication
contexts and let

.. math::

   \mathscr K_{\mathrm{KQC}} :
   \mathcal C_{\mathrm{pub}}^{op}
   \longrightarrow
   \mathbf{KQCSection}

assign one finite typed section to each repository/ref/SHA context.

The implemented cover is

.. math::

   U_{\mathrm{source}}
   \longrightarrow
   U_{\mathrm{mirror}}
   \longrightarrow
   U_{\mathrm{upstream}}.

Each arrow is a publication morphism, not identity transport.  Source
provenance, public projection identity, and upstream project identity remain
separate.

A pullback witness has the form

.. math::

   X_L \times_B X_R

with a stable witness identifier, a base object, a trace identifier, and an
explicit ``commutes`` field.  Noncommuting pullbacks remain obstructions and
cannot be erased by publication.

K/Q/C typing
------------

Every admitted kernel carries three distinct facets:

``C_TYPED``
   The native ABI, C implementation, extension, memory, and low-level execution
   boundary.

``Q_TYPED``
   The QuoQuantum/QQUAPP representation, measurement, diagram, and contextual
   computation boundary.

``K_TYPED``
   The stable resource class, kernel/realization boundary, and Grothendieck-style
   accounting boundary.

The combined KQC type is conjunctive but non-collapsing:

.. math::

   \mathrm{KQC}(X)
   = C(X) \wedge Q(X) \wedge K(X),

while

.. math::

   C(X) \neq Q(X) \neq K(X)

as typed facets.

Compiler taxonomy
-----------------

The initial publication objective classifies the Python stack without treating
all compilation mechanisms as equivalent.

``SCHEMA_AOT``
   Deterministic Pydantic JSON-Schema and certificate construction.  This is
   schema compilation, not machine-code compilation.

``BYTECODE_COMPILE``
   CPython source-to-bytecode compilation.

``ADAPTIVE_INTERPRETER``
   CPython's default adaptive bytecode interpreter and specialization layer.

``EXPERIMENTAL_JIT``
   CPython's current experimental trace/uop/copy-and-patch JIT profile.  The
   profile is source-bound to the relevant CPython files and does not claim that
   a JIT build has been executed.

``EXTERNAL_JIT``
   Optional external specialization systems such as a declared Numba adapter.
   The external project remains independently versioned and governed.

``NATIVE_AOT``
   Ahead-of-time C/C++ extension compilation.

``PYBIND_BINDING``
   Optional pybind11 binding projection over an admitted native kernel.

``OPENMP_BINDING``
   Optional OpenMP/PyOMP-style adapter over an admitted C-typed kernel.

A compiler profile must declare source type, target type, context, backend,
source paths, pullbacks, dependency identities, resource-call bounds, and
execution status.

Bunched resources
-----------------

The resource model follows a bounded bunched-typing discipline.  It does not
claim a theorem that a bunch can never be invoked infinitely in every possible
logic.  Instead, every concrete compiler kernel has a finite
``max_resource_calls`` value and unrestricted contraction is not available in
the admitted contract.

Thus the implemented rule is

.. math::

   \operatorname{Admit}(K)
   \Longrightarrow
   0 < N_K < \infty,

where :math:`N_K` is the declared resource-call budget.

K-theory and VOID boundary
--------------------------

The standard stable statement retained by the architecture is

.. math::

   K^0(\mathrm{pt}) \cong \mathbb Z.

Positive and negative integers may encode a Grothendieck difference or a signed
resource ledger.  They are not automatically physical calls, negative physical
objects, or interpreter invocations.

``VOID`` is an internal SIGIL semantic role for an unrealized class, kernel,
obstruction, or absent realization in a declared context.  The contract
explicitly records

``void_is_semantic_kernel_role_not_literal_K_dual = true``.

It therefore does not assert that VOID is the standard mathematical dual of a
point or of :math:`\mathbb Z`.

Dyadic quotient candidate
-------------------------

The proposed dyadic relationship

.. math::

   \operatorname{Im}(\mathrm{SIGIL4CPython})
   \stackrel{?}{\cong}
   \mathrm{sigilbook}/\ker(\mathrm{SIGIL4CPython})

is represented only as a future proof obligation.  The executable schema fixes
``quotient_isomorphism_claimed = false``.  Establishing such an isomorphism
would require explicit objects, morphisms, a kernel notion, a quotient
construction, well-definedness, inverse maps, and compatibility with the KQC
order.

Third Wheel decomposition
-------------------------

A ``ThirdWheelFactor`` records a finite recursive split

.. math::

   P \rightsquigarrow (L, R, \Omega)

where :math:`P` is the parent carrier, :math:`L` and :math:`R` are distinct
factors, and :math:`\Omega` is the retained dyadic obstruction.  A nonnegative
remaining budget prevents unbounded recursive decomposition.

This is an internal PACA theorem schema for producing small review obligations.
It is not presented as an established theorem about every total category.

VOID/VORTEX/ALHAMBRA and TRANADA
--------------------------------

The messaging interpretation uses three non-collapsing sectors:

``VOID``
   Latent class, unresolved branch, unrealized resource, or retained
   obstruction.

``VORTEX``
   Contextual flow, temporal transition, monodromy, or dynamic message route.

``ALHAMBRA``
   Finite incidence, support, layout, address, or tensor-train realization.

A TRANADA junction combines three carriers only through explicit witnesses.
Associativity, pentagon coherence, trace cyclicity, normalized 3-cocycle data,
twisted-injection witnesses, and pullback families are all separate fields.

The Büerschaper/twisted-injective PEPS and string-net vocabulary is used here as
a typed messaging and diagrammatic constraint profile.  No spatial phase,
physical PEPS realization, TQFT, or topological-order certificate is inferred.

Harmonic and Fourier constraints
--------------------------------

A Jaranian harmonic profile may declare Fourier-style invertibility only when it
also declares:

* a group action;
* a locally compact Hausdorff/T2 setting;
* a commutative hyperoperation;
* point-separating characters;
* Haar and Plancherel witnesses.

This is a model-level gate.  It does not claim that every category, hypergroup,
or noncommutative product possesses a Fourier--Mukai transform or Pontryagin
reflexivity.

A generalized Jaranian Fourier--Mukai transform remains an additional proof
obligation whenever a new algebraic product is introduced.

Measurement profile
-------------------

The example profile distinguishes a repeatable measurement of a declared
``Z``-character basis from its effect on a dual ``X`` representation.  It may be
QND/repeatable with respect to the measured observable while destroying
coherence in the conjugate basis.  This is recorded as a symbolic profile; no
physical measurement is executed or certified.

Feature maps and physical analogies
-----------------------------------

Feature maps may be typed as curvature-reducing or localization-compatible
maps only after a concrete domain, codomain, metric or cohomological invariant,
and preservation witness are supplied.

Higgs models, Anderson localization, AdS/CFT, Kitaev models, Sachdev--Ye--Kitaev
models, nonabelian cohomology, and topological condensed-matter constructions
remain motivations or model-indexed adapters.  The publication sheaf does not
infer equivalence among them.

Aperiodic and tensor-train compression
--------------------------------------

The proposed chain

.. math::

   \text{twisted cocycle presentation}
   \longrightarrow
   \text{aperiodic cellulation candidate}
   \longrightarrow
   \text{Pachner-style moves}
   \longrightarrow
   \text{Grothendieck-compatible presentation}
   \longrightarrow
   \text{ALHAMBRA tensor train}

is retained as a candidate compression programme.  The schema fixes
``aperiodic_compression_theorem_claimed = false`` until termination,
confluence, invariant preservation, and reconstruction witnesses are provided.

Pydantika, DisCoPy, and Lean4
-----------------------------

The repository separates four layers:

* :mod:`sigil4cpython.kqc_sheaf` is dependency-free;
* ``Tools/sigil4cpython/kqc_publication_models.py`` contains strict Pydantic v2
  models;
* ``Tools/sigil4cpython/discopy_kqc_projection.py`` contains an optional
  DisCoPy projection plan;
* ``Tools/sigil4cpython/lean4/KQCPublicationSheaf.lean`` contains a finite Lean4
  proof scaffold.

Pydantic validation is not CPython acceptance.  DisCoPy materialization is not
compiler execution.  A Lean scaffold is not a proof of the quotient,
Fourier--Mukai, TQFT, or aperiodic-compression claims.

Publication states
------------------

``ADMIT``
   The finite publication metadata is internally consistent.  No push or
   upstream contribution is implied.

``HOLD_WITH_OBSTRUCTION``
   A proof, pullback, source selection, backend, review, or reconciliation
   obligation remains visible.

``REJECT``
   Identity transport, plural collapse, or direct unauthorized upstream writing
   was requested.

Irreducible law
---------------

::

   source section != public mirror != upstream project
   schema compile != bytecode compile != interpreter != JIT != native AOT
   relation != identity
   pullback witness != global theorem
   public branch != accepted CPython contribution
   KQC composition preserves C, Q, K, context, provenance, trace, and obstruction
