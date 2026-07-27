import unittest
from dataclasses import replace

from sigil4cpython.kqc_sheaf import (
    CompilerKernel,
    CompilerStrategy,
    HarmonicConstraint,
    KQCKernelType,
    KQCPublicationSheaf,
    MeasurementProfile,
    PublicationAuthority,
    PublicationHop,
    PullbackWitness,
    RepositorySection,
    TQFTCoherenceProfile,
    ThirdWheelFactor,
    UAPState,
    compile_publication_sheaf,
)


SOURCE_SHA = "0" * 40
MIRROR_SHA = "1" * 40
UPSTREAM_SHA = "2" * 40


class KQCPublicationSheafTests(unittest.TestCase):
    def kqc_type(self, suffix):
        return KQCKernelType(
            c_typed=True,
            q_typed=True,
            k_typed=True,
            context_type=f"CONTEXT::{suffix}",
            quoquantum_type=f"QQUAPP::{suffix}",
        )

    def kernel(self, kernel_id, strategy, source_type, target_type, pullback_id, backend):
        return CompilerKernel(
            kernel_id=kernel_id,
            strategy=strategy,
            source_type=source_type,
            target_type=target_type,
            context_id=f"context:{kernel_id}",
            backend=backend,
            kqc_type=self.kqc_type(kernel_id),
            source_paths=(f"source:{kernel_id}",),
            pullback_ids=(pullback_id,),
            max_resource_calls=64,
        )

    def valid_sheaf(self):
        pullbacks = (
            PullbackWitness("pb:bytecode", "BYTECODE", "SOURCE", "BASE", True, "trace:1"),
            PullbackWitness("pb:adaptive", "ADAPTIVE", "BYTECODE", "BASE", True, "trace:2"),
            PullbackWitness("pb:jit", "JIT", "ADAPTIVE", "BASE", True, "trace:3"),
            PullbackWitness("pb:aot", "AOT", "SOURCE", "BASE", True, "trace:4"),
        )
        kernels = (
            self.kernel(
                "BYTECODE",
                CompilerStrategy.BYTECODE_COMPILE,
                "PYTHON_SOURCE",
                "CPYTHON_BYTECODE",
                "pb:bytecode",
                "CPYTHON_COMPILER",
            ),
            self.kernel(
                "ADAPTIVE",
                CompilerStrategy.ADAPTIVE_INTERPRETER,
                "CPYTHON_BYTECODE",
                "TIER1_STATE",
                "pb:adaptive",
                "CPYTHON_ADAPTIVE_INTERPRETER",
            ),
            self.kernel(
                "JIT",
                CompilerStrategy.EXPERIMENTAL_JIT,
                "TIER1_STATE",
                "JIT_EXECUTOR",
                "pb:jit",
                "CPYTHON_JIT",
            ),
            self.kernel(
                "AOT",
                CompilerStrategy.NATIVE_AOT,
                "C_TYPED_IR",
                "NATIVE_EXTENSION",
                "pb:aot",
                "C_COMPILER",
            ),
        )
        return KQCPublicationSheaf(
            report_id="test:publication-sheaf",
            source=RepositorySection(
                "jbermejovega/sigilbook",
                "agent/source",
                SOURCE_SHA,
                "private",
                "source",
            ),
            public_mirror=RepositorySection(
                "jbermejovega/sigil4cpython",
                "agent/mirror",
                MIRROR_SHA,
                "public",
                "public_mirror",
            ),
            upstream=RepositorySection(
                "python/cpython",
                "main",
                UPSTREAM_SHA,
                "public",
                "upstream",
            ),
            kernels=kernels,
            relations=(),
            pullbacks=pullbacks,
            publication_hops=(
                PublicationHop(
                    "hop:source:mirror",
                    "jbermejovega/sigilbook",
                    "jbermejovega/sigil4cpython",
                    SOURCE_SHA,
                    MIRROR_SHA,
                    PublicationAuthority.WRITE_OWN_REPOSITORY,
                    ("STRIKK", "PYDANTIKA", "HUMAN"),
                ),
                PublicationHop(
                    "hop:mirror:upstream",
                    "jbermejovega/sigil4cpython",
                    "python/cpython",
                    MIRROR_SHA,
                    UPSTREAM_SHA,
                    PublicationAuthority.PLAN_ONLY,
                    ("CPYTHON_DEVGUIDE", "CORE_REVIEW"),
                ),
            ),
            third_wheel_factors=(
                ThirdWheelFactor(
                    "third-wheel:compiler",
                    "BYTECODE",
                    "STATIC_BRANCH",
                    "DYNAMIC_BRANCH",
                    "obstruction:strategy",
                    4,
                ),
            ),
            harmonic_constraints=(
                HarmonicConstraint(
                    "harmonic:declared",
                    True,
                    True,
                    True,
                    True,
                    True,
                    True,
                    ("haar", "plancherel"),
                ),
            ),
            measurement_profiles=(
                MeasurementProfile(
                    "measurement:z",
                    "Z",
                    "X",
                    True,
                    True,
                    True,
                ),
            ),
            tqft_profiles=(
                TQFTCoherenceProfile(
                    "tqft:message-router",
                    "assoc",
                    "pentagon",
                    "trace",
                    "3-cocycle",
                    ("twist:void", "twist:vortex", "twist:alhambra"),
                    tuple(item.witness_id for item in pullbacks),
                ),
            ),
            replay_trace=("trace:source", "trace:mirror", "trace:upstream-plan"),
        )

    def test_valid_publication_sheaf_is_admitted_as_plan(self):
        sheaf = self.valid_sheaf()
        self.assertEqual(sheaf.validate(), ())
        result = compile_publication_sheaf(sheaf)
        self.assertEqual(result["uap_state"], UAPState.ADMIT.value)
        self.assertFalse(result["source_files_copied"])
        self.assertFalse(result["upstream_write_performed"])
        self.assertEqual(result["sheaf_sha256"], sheaf.canonical_digest())

    def test_direct_upstream_write_is_rejected(self):
        sheaf = self.valid_sheaf()
        invalid_hop = replace(
            sheaf.publication_hops[1],
            authority=PublicationAuthority.WRITE_OWN_REPOSITORY,
            direct_upstream_write=True,
        )
        result = compile_publication_sheaf(
            replace(sheaf, publication_hops=(sheaf.publication_hops[0], invalid_hop))
        )
        self.assertEqual(result["uap_state"], UAPState.REJECT.value)
        self.assertIn("direct_upstream_write_forbidden", result["obstruction_ledger"])

    def test_noncommuting_pullback_holds(self):
        sheaf = self.valid_sheaf()
        bad_pullback = replace(sheaf.pullbacks[0], commutes=False)
        result = compile_publication_sheaf(
            replace(sheaf, pullbacks=(bad_pullback,) + sheaf.pullbacks[1:])
        )
        self.assertEqual(result["uap_state"], UAPState.HOLD_WITH_OBSTRUCTION.value)
        self.assertIn("noncommuting_pullback:pb:bytecode", result["obstruction_ledger"])

    def test_unbounded_bunched_resource_calls_hold(self):
        sheaf = self.valid_sheaf()
        bad_kernel = replace(
            sheaf.kernels[0],
            resource_calls_bounded=False,
            max_resource_calls=0,
        )
        result = compile_publication_sheaf(
            replace(sheaf, kernels=(bad_kernel,) + sheaf.kernels[1:])
        )
        self.assertEqual(result["uap_state"], UAPState.HOLD_WITH_OBSTRUCTION.value)
        self.assertIn(
            "unbounded_bunched_resource_calls:BYTECODE",
            result["obstruction_ledger"],
        )

    def test_quotient_isomorphism_is_not_promoted(self):
        sheaf = replace(self.valid_sheaf(), quotient_isomorphism_claimed=True)
        result = compile_publication_sheaf(sheaf)
        self.assertEqual(result["uap_state"], UAPState.HOLD_WITH_OBSTRUCTION.value)
        self.assertIn("quotient_isomorphism_requires_proof", result["obstruction_ledger"])


if __name__ == "__main__":
    unittest.main()
