"""SIGIL4CPython experimental runtime wards.

This package is intentionally small and pure Python.  It carries SIGIL/UAP
guardrail metadata without changing CPython interpreter semantics.
"""

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

__all__ = [
    "DEFAULT_CLAIM_BOUNDARY",
    "KokompiledKernel",
    "UAPWard",
    "UAPWardVerdict",
    "build_pacadocencia_uap_kernel",
    "check_uap_wards",
    "kokompile_kernel",
    "validate_kokompiled_kernel",
]
