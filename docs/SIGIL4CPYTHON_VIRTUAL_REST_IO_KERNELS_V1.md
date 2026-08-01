# SIGIL4CPYTHON VIRTUAL REST IO KERNELS V1

Status: canonical_candidate, STRIKK_TYPED, virtual_io, pacaiogames, restful_ios_conformal.

## Core Law

SIGIL APIs treat REST endpoints, IOS handles, MCP resources, and scheduler
interfaces as virtual IO ports before a physical resource cell is attached.

```text
REST(endpoint) ~= IOS(handle) ~= VirtualIOPort(stream)
until
ResourceCell(authority, strikk_type, resource_ref)
is attached by a cellular move.
```

The virtual stream is not hardware authority.  The hardware or scheduler
authority appears only after a STRIKK typed resource cell is added to the
diagram.

## PACAIoGames Interpretation

In PACAIoGames, all API moves are played on a uniform virtual IO stream.
REST logic is lifted away from sockets and HTTP servers.  IOS logic is lifted
away from file descriptors, devices, terminals, and platform handles.  At that
level both sides are the same kind of typed stream:

```text
PACAIoGamesMove
  = cellular_typed_move(VirtualIOPort -> VirtualIOPort)
```

The move remains replay-safe while it preserves:

- stream type
- semantic type
- authority boundary
- STRIKK witness
- obstruction ledger

## Resource Attachment Rule

Direct access to resources is forbidden unless the diagram contains an explicit
resource cell.

```text
DirectResourceAccess(cell)
  implies
cell.kind = RESOURCE_CELL
and cell.authority != VIRTUAL_ONLY
and cell.resource_refs != empty
and cell.strikk_type != empty
```

This is the boundary between virtual user space and resource authority space.
It covers hardware, scheduler jobs, devices, sockets, files, cloud APIs, and
HPC resource managers such as SLURM-like systems.

## REST/IOS Conformality

REST and IOS are conformal only when their lifted ports share the same semantic
type and stream type.

```text
ConformalRESTIOS(K)
  iff
forall p in ports(K), p.protocol in {REST, IOS}:
    p.stream_type = UNIFORM_VIRTUAL_IO_STREAM
and
    p.semantic_type = shared_context_type
```

If either type drifts, the kernel must hold with obstruction instead of
claiming admission.

## Cellular Twisted Moves

A cellular twisted move is an allowed rewrite between IO cells.  It may change
presentation, routing, or carrier surface, but it must preserve stream type and
authority boundary unless the target is a typed resource cell.

```text
TwistedMove(A -> B)
  admits
when
  preserves_stream_type
  and preserves_authority_boundary
  and has STRIKK witness
```

## Dependency Boundaries

The dependency-free runtime surface lives in:

```text
Lib/sigil4cpython/virtual_io.py
```

The optional Pydantika tooling surface lives in:

```text
Tools/sigil4cpython/virtual_io_models.py
```

Pydantika remains tooling.  It is not a CPython standard-library dependency and
does not execute REST calls, IOS calls, scheduler jobs, or hardware operations.

## Source Bindings

This kernel binds the request to the existing SIGIL4CPython laws:

- external glue remains modular and ecosystem-sovereign
- stable releases require tested boundaries and replay certificates
- publication and upstream contribution remain review-gated
- virtual streams do not carry physical authority

It also aligns the mathematical vocabulary as follows:

- association schemes supply typed relation partitions and symmetry checks
- hypergraph duality supplies incidence, transversal, and covering language
- expansion lemma methods supply kernel reduction and obstruction pruning
- K-theory of algebraic tori supplies the Fourier/mirror analogy for typed dual
  carrier surfaces
- SLURM-like schedulers supply the canonical resource-cell example for
  topologically aware job placement

## Final Compression

```text
REST lifts.
IOS lifts.
Streams conform.
Cells witness.
Resources attach.
STRIKK guards.
PACAIoGames admits only typed authority.
```

KLOSE: `SIGIL4CPYTHON_VIRTUAL_REST_IO_KERNELS_V1` defines the canonical virtual
REST/IOS API kernel rule for SIGIL4CPython.
