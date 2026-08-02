# cython: language_level=3
# distutils: language=c

cdef inline unsigned long long _mix(unsigned long long state, unsigned long long value) noexcept nogil:
    return (state ^ value) * <unsigned long long>1099511628211

cpdef unsigned long long coherent_fixed_point(unsigned long long seed, tuple section_digests):
    cdef unsigned long long state = seed
    cdef object item
    for item in section_digests:
        state = _mix(state, <unsigned long long>int(item))
    return state