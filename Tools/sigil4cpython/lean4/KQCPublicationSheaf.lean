namespace Sigil4CPython

inductive Authority where
  | writeOwnRepository
  | openReviewCandidate
  | planOnly
  deriving DecidableEq, Repr

inductive UAPState where
  | admit
  | holdWithObstruction
  | reject
  deriving DecidableEq, Repr

structure RepositorySection where
  repository : String
  ref : String
  commitSha : String
  isPublic : Bool
  deriving Repr

structure KQCKernelType where
  cTyped : Bool
  qTyped : Bool
  kTyped : Bool
  contextType : String
  quoQuantumType : String
  noIdentityTransport : Bool
  noPluralCollapse : Bool
  deriving Repr

structure PullbackWitness where
  witnessId : String
  leftObject : String
  rightObject : String
  baseObject : String
  commutes : Bool
  deriving Repr

structure CompilerKernel where
  kernelId : String
  strategy : String
  sourceType : String
  targetType : String
  contextId : String
  kqcType : KQCKernelType
  maxResourceCalls : Nat
  runtimeExecuted : Bool
  deriving Repr

structure PublicationHop where
  hopId : String
  sourceRepository : String
  targetRepository : String
  authority : Authority
  directWrite : Bool
  deriving Repr

structure ThirdWheelFactor where
  factorId : String
  parentId : String
  leftId : String
  rightId : String
  obstructionId : String
  remainingBudget : Nat
  deriving Repr

structure KQCPublicationSheaf where
  source : RepositorySection
  publicMirror : RepositorySection
  upstream : RepositorySection
  kernels : List CompilerKernel
  pullbacks : List PullbackWitness
  sourceToMirror : PublicationHop
  mirrorToUpstream : PublicationHop
  thirdWheelFactors : List ThirdWheelFactor
  allPullbacksCommute : ∀ p ∈ pullbacks, p.commutes = true
  upstreamPlanOnly : mirrorToUpstream.authority = Authority.planOnly
  noDirectUpstreamWrite : mirrorToUpstream.directWrite = false
  sourceBound : Bool
  replayPreserved : Bool
  humanReviewRequired : Bool


def KQCKernelType.WellTyped (k : KQCKernelType) : Prop :=
  k.cTyped = true ∧
  k.qTyped = true ∧
  k.kTyped = true ∧
  k.noIdentityTransport = true ∧
  k.noPluralCollapse = true


def CompilerKernel.Bounded (k : CompilerKernel) : Prop :=
  0 < k.maxResourceCalls


def PublicationHop.UpstreamSafe (h : PublicationHop) : Prop :=
  h.targetRepository = "python/cpython" →
    h.authority = Authority.planOnly ∧ h.directWrite = false


def ThirdWheelFactor.Valid (f : ThirdWheelFactor) : Prop :=
  f.leftId ≠ f.rightId ∧ f.obstructionId ≠ ""


theorem upstream_is_plan_only (s : KQCPublicationSheaf) :
    s.mirrorToUpstream.authority = Authority.planOnly := by
  exact s.upstreamPlanOnly


theorem upstream_write_is_forbidden (s : KQCPublicationSheaf) :
    s.mirrorToUpstream.directWrite = false := by
  exact s.noDirectUpstreamWrite


theorem admitted_pullbacks_commute
    (s : KQCPublicationSheaf)
    (p : PullbackWitness)
    (hp : p ∈ s.pullbacks) :
    p.commutes = true := by
  exact s.allPullbacksCommute p hp


theorem KQC_no_identity_transport
    (k : KQCKernelType)
    (h : k.WellTyped) :
    k.noIdentityTransport = true := by
  exact h.2.2.2.1


theorem KQC_no_plural_collapse
    (k : KQCKernelType)
    (h : k.WellTyped) :
    k.noPluralCollapse = true := by
  exact h.2.2.2.2


theorem third_wheel_preserves_distinct_factors
    (f : ThirdWheelFactor)
    (h : f.Valid) :
    f.leftId ≠ f.rightId := by
  exact h.1

/--
This file proves only the finite internal contract represented by the supplied
structures. It does not establish a quotient isomorphism between repositories,
a Fourier–Mukai theorem, a TQFT, an aperiodic-compression theorem, or acceptance
of any patch by the CPython project.
-/
theorem claim_boundary : True := by
  trivial

end Sigil4CPython
