namespace Sigil4CPython

inductive CanonicalArtifactKind where
  | sigilAst
  | sigilSyntacticalKernel
  | sigilSemanticalKernel
  deriving DecidableEq, Repr

structure PersistentPacaSkill where
  tracePreserved : Prop
  noIdentityTransport : Prop
  noGitMerge : Prop
  noRuntimeExecution : Prop
  pluralTyped : Prop


def Admissible (skill : PersistentPacaSkill) : Prop :=
  skill.tracePreserved ∧
    skill.noIdentityTransport ∧
      skill.noGitMerge ∧ skill.noRuntimeExecution ∧ skill.pluralTyped

structure CanonicalCompilation where
  ast : CanonicalArtifactKind
  syntacticalKernel : CanonicalArtifactKind
  semanticalKernel : CanonicalArtifactKind
  source : PersistentPacaSkill
  sourceAdmissible : Admissible source


def compilePersistentSkill
    (skill : PersistentPacaSkill)
    (admissible : Admissible skill) : CanonicalCompilation :=
  {
    ast := .sigilAst
    syntacticalKernel := .sigilSyntacticalKernel
    semanticalKernel := .sigilSemanticalKernel
    source := skill
    sourceAdmissible := admissible
  }


theorem compilation_preserves_trace
    (skill : PersistentPacaSkill)
    (admissible : Admissible skill) :
    (compilePersistentSkill skill admissible).source.tracePreserved := by
  exact admissible.1


theorem compilation_preserves_identity_boundary
    (skill : PersistentPacaSkill)
    (admissible : Admissible skill) :
    (compilePersistentSkill skill admissible).source.noIdentityTransport := by
  exact admissible.2.1


theorem compilation_does_not_merge_git_branches
    (skill : PersistentPacaSkill)
    (admissible : Admissible skill) :
    (compilePersistentSkill skill admissible).source.noGitMerge := by
  exact admissible.2.2.1


theorem compilation_does_not_execute_runtime
    (skill : PersistentPacaSkill)
    (admissible : Admissible skill) :
    (compilePersistentSkill skill admissible).source.noRuntimeExecution := by
  exact admissible.2.2.2.1


theorem compilation_preserves_plural_typing
    (skill : PersistentPacaSkill)
    (admissible : Admissible skill) :
    (compilePersistentSkill skill admissible).source.pluralTyped := by
  exact admissible.2.2.2.2


theorem ast_ne_syntactical :
    CanonicalArtifactKind.sigilAst ≠
      CanonicalArtifactKind.sigilSyntacticalKernel := by
  decide


theorem syntactical_ne_semantical :
    CanonicalArtifactKind.sigilSyntacticalKernel ≠
      CanonicalArtifactKind.sigilSemanticalKernel := by
  decide

end Sigil4CPython
