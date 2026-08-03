namespace Sigil4CPython

inductive PacapdgUapArtifactKind where
  | sigilAstV2
  | sigilSyntacticalKernelV2
  | sigilSemanticalKernelV2
  deriving DecidableEq, Repr

structure PacapdgUapContract where
  pacapdgTyped : Prop
  uapTyped : Prop
  qunoTyped : Prop
  tracePreserved : Prop
  noIdentityTransport : Prop
  noPluralCollapse : Prop
  piFixedOrHold : Prop
  noRuntimeExecution : Prop
  noGitMerge : Prop
  candidateNotPromoted : Prop


def PacapdgUapAdmissible (contract : PacapdgUapContract) : Prop :=
  contract.pacapdgTyped ∧
    contract.uapTyped ∧
      contract.qunoTyped ∧
        contract.tracePreserved ∧
          contract.noIdentityTransport ∧
            contract.noPluralCollapse ∧
              contract.piFixedOrHold ∧
                contract.noRuntimeExecution ∧
                  contract.noGitMerge ∧ contract.candidateNotPromoted

structure PacapdgUapCompilation where
  ast : PacapdgUapArtifactKind
  syntacticalKernel : PacapdgUapArtifactKind
  semanticalKernel : PacapdgUapArtifactKind
  contract : PacapdgUapContract
  contractAdmissible : PacapdgUapAdmissible contract


def compilePacapdgUap
    (contract : PacapdgUapContract)
    (admissible : PacapdgUapAdmissible contract) : PacapdgUapCompilation :=
  {
    ast := .sigilAstV2
    syntacticalKernel := .sigilSyntacticalKernelV2
    semanticalKernel := .sigilSemanticalKernelV2
    contract := contract
    contractAdmissible := admissible
  }


theorem compilation_is_pacapdg_typed
    (contract : PacapdgUapContract)
    (admissible : PacapdgUapAdmissible contract) :
    (compilePacapdgUap contract admissible).contract.pacapdgTyped := by
  exact admissible.1


theorem compilation_is_uap_typed
    (contract : PacapdgUapContract)
    (admissible : PacapdgUapAdmissible contract) :
    (compilePacapdgUap contract admissible).contract.uapTyped := by
  exact admissible.2.1


theorem compilation_is_quno_typed
    (contract : PacapdgUapContract)
    (admissible : PacapdgUapAdmissible contract) :
    (compilePacapdgUap contract admissible).contract.qunoTyped := by
  exact admissible.2.2.1


theorem compilation_preserves_trace
    (contract : PacapdgUapContract)
    (admissible : PacapdgUapAdmissible contract) :
    (compilePacapdgUap contract admissible).contract.tracePreserved := by
  exact admissible.2.2.2.1


theorem compilation_preserves_identity_boundary
    (contract : PacapdgUapContract)
    (admissible : PacapdgUapAdmissible contract) :
    (compilePacapdgUap contract admissible).contract.noIdentityTransport := by
  exact admissible.2.2.2.2.1


theorem compilation_preserves_plural_typing
    (contract : PacapdgUapContract)
    (admissible : PacapdgUapAdmissible contract) :
    (compilePacapdgUap contract admissible).contract.noPluralCollapse := by
  exact admissible.2.2.2.2.2.1


theorem compilation_preserves_pi_boundary
    (contract : PacapdgUapContract)
    (admissible : PacapdgUapAdmissible contract) :
    (compilePacapdgUap contract admissible).contract.piFixedOrHold := by
  exact admissible.2.2.2.2.2.2.1


theorem compilation_does_not_execute_runtime
    (contract : PacapdgUapContract)
    (admissible : PacapdgUapAdmissible contract) :
    (compilePacapdgUap contract admissible).contract.noRuntimeExecution := by
  exact admissible.2.2.2.2.2.2.2.1


theorem compilation_does_not_merge_branches
    (contract : PacapdgUapContract)
    (admissible : PacapdgUapAdmissible contract) :
    (compilePacapdgUap contract admissible).contract.noGitMerge := by
  exact admissible.2.2.2.2.2.2.2.2.1


theorem compilation_does_not_promote_candidate
    (contract : PacapdgUapContract)
    (admissible : PacapdgUapAdmissible contract) :
    (compilePacapdgUap contract admissible).contract.candidateNotPromoted := by
  exact admissible.2.2.2.2.2.2.2.2.2


theorem ast_ne_syntactical :
    PacapdgUapArtifactKind.sigilAstV2 ≠
      PacapdgUapArtifactKind.sigilSyntacticalKernelV2 := by
  decide


theorem syntactical_ne_semantical :
    PacapdgUapArtifactKind.sigilSyntacticalKernelV2 ≠
      PacapdgUapArtifactKind.sigilSemanticalKernelV2 := by
  decide

end Sigil4CPython
