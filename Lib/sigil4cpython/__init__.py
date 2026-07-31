"""SIGIL4CPython experimental typed contracts.

The package is intentionally pure Python and dependency-free. It carries
SIGIL/UAP/KQC guardrail metadata without changing CPython interpreter semantics.
Optional Pydantika and DisCoPy projections live under ``Tools/sigil4cpython``.
"""

from .kqc_sheaf import (
    CompilerKernel,
    CompilerStrategy,
    HarmonicConstraint,
    KQCKernelType,
    KQCPublicationSheaf,
    MeasurementProfile,
    PublicationAuthority,
    PublicationHop,
    PullbackWitness,
    RelationKind,
    RepositorySection,
    TQFTCoherenceProfile,
    ThirdWheelFactor,
    TypedRelation,
    UAPState,
    compile_publication_sheaf,
)
from .uap_wards import (
    DEFAULT_CLAIM_BOUNDARY,
    KokompiledKernel,
    UAPWard,
    UAPWardVerdict,
    build_pacadocencia_uap_kernel,
    check_uap_wards,
    kokompile_kernel,
    validate_kokompiled_kernel,
)
from .virtual_io import (
    CellKind,
    CellularTwistedMove,
    IOCell,
    ResourceAuthority,
    VirtualIOKernel,
    VirtualIOPort,
    VirtualIOProtocol,
    VirtualIOState,
    build_pacaiogame_virtual_rest_kernel,
    compile_virtual_io_kernel,
)

__all__ = [
    "CellKind",
    "CellularTwistedMove",
    "CompilerKernel",
    "CompilerStrategy",
    "DEFAULT_CLAIM_BOUNDARY",
    "HarmonicConstraint",
    "IOCell",
    "KQCKernelType",
    "KQCPublicationSheaf",
    "KokompiledKernel",
    "MeasurementProfile",
    "PublicationAuthority",
    "PublicationHop",
    "PullbackWitness",
    "RelationKind",
    "RepositorySection",
    "ResourceAuthority",
    "TQFTCoherenceProfile",
    "ThirdWheelFactor",
    "TypedRelation",
    "UAPState",
    "UAPWard",
    "UAPWardVerdict",
    "VirtualIOKernel",
    "VirtualIOPort",
    "VirtualIOProtocol",
    "VirtualIOState",
    "build_pacadocencia_uap_kernel",
    "build_pacaiogame_virtual_rest_kernel",
    "check_uap_wards",
    "compile_publication_sheaf",
    "compile_virtual_io_kernel",
    "kokompile_kernel",
    "validate_kokompiled_kernel",
]
