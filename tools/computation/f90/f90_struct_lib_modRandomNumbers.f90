!******************************************************************************
!******************************************************************************
!
!   Module for random number generation.
!
!   Important Notes:
!
!       In contrast to Python's numpy library, the interface requires
!       passing of the variance and not the standard deviation.
!
!
!******************************************************************************
!******************************************************************************
MODULE struct_modRandomNumbers

	!/*	external modules	*/

    USE struct_modProgramConstants
    USE struct_modLinearAlgebra

	!/*	setup	*/

	IMPLICIT NONE

    PRIVATE

    PUBLIC :: choice, normal_rv, normal_mixture_rv

    !/* polymorhisms */

    INTERFACE normal_rv

        MODULE PROCEDURE normal_univariate_rv, &
                         normal_multivariate_rv

    END INTERFACE

CONTAINS
!******************************************************************************
!******************************************************************************
SUBROUTINE normal_multivariate_rv(rslt, mean, cov)
!
!   This subroutine draws a random sample of deviates from a multivariate
!   normal distribution.
!
!
    !/* external objects    */

    REAL(our_dble), INTENT(INOUT)   :: rslt(:,:)
    REAL(our_dble), INTENT(IN)      :: mean(:)
    REAL(our_dble), INTENT(IN)      :: cov(:,:)

    !/*  internal objects    */

    INTEGER(our_int)                :: numDim
    INTEGER(our_int)                :: numDev
    INTEGER(our_int)                :: i

    REAL(our_dble), ALLOCATABLE     :: z(:)
    REAL(our_dble), ALLOCATABLE     :: ch(:,:)

!------------------------------------------------------------------------------
!   algorithm
!------------------------------------------------------------------------------

    ! Auxillary objects.
    numDev = SIZE(rslt, 1)
    numDim = SIZE(rslt, 2)

    ! Allocate arrays.
    ALLOCATE(z(numDim))
    ALLOCATE(ch(numDim, numDim))

    ! Main algorithm.
    ch = zero_dble

    CALL cholesky(cov, ch)

    DO i = 1, numDev

        CALL normal_univariate_rv(z(:), zero_dble, one_dble)

        rslt(i,:) = MATMUL(ch,z(:)) + mean(:)

    END DO

END SUBROUTINE
!******************************************************************************
!******************************************************************************
SUBROUTINE normal_univariate_rv(rslt, mean, var)
!
!   This subroutine draws a random sample of deviates from a normal
!   distribution.
!
!
    !/* external objects    */

    REAL(our_dble), INTENT(INOUT)   :: rslt(:)
    REAL(our_dble), INTENT(IN)      :: mean
    REAL(our_dble), INTENT(IN)      :: var

    !/*  internal objects    */

    REAL(our_dble), ALLOCATABLE     :: u(:)
    REAL(our_dble), ALLOCATABLE     :: r(:)
    REAL(our_dble)                  :: sd

    INTEGER(our_int)                :: g
    INTEGER(our_int)                :: i
    INTEGER(our_int)                :: numDev

!------------------------------------------------------------------------------
!   algorithm
!------------------------------------------------------------------------------

    ! Auxillary objects.
    numDev = SIZE(rslt)
    sd     = SQRT(var)

    ! Allocate internal objects.
    ALLOCATE(u(two_int*numDev))
    ALLOCATE(r(two_int*numDev))

    ! Call uniform random number.
    CALL RANDOM_NUMBER(u)

    ! Perform Box-Muller transformation.
    DO g = 1, (2*numDev), 2

       r(g)           = SQRT(-two_dble*log(u(g)))*COS(two_dble*pi_dble*u(g + 1))
       r(g + one_int) = SQRT(-two_dble*log(u(g)))*SIN(two_dble*pi_dble*u(g + 1))

    END DO

    ! Unstandardize deviates.
    DO i = 1, numDev

       rslt(i) = mean + sd*r(i)

    END DO

END SUBROUTINE
!******************************************************************************
!******************************************************************************
SUBROUTINE normal_mixture_rv(rslt, means, covs, shares)
!
!   This subroutine creates a sample from a multivariate random normal
!   distribution
!
!
    !/* external objects    */

    REAL(our_dble), INTENT(INOUT)   :: rslt(:,:)

    REAL(our_dble), INTENT(IN)      :: means(:,:)
    REAL(our_dble), INTENT(IN)      :: covs(:,:,:)
    REAL(our_dble), INTENT(IN)      :: shares(:)

    !/*  internal objects    */

    INTEGER                         :: numDev
    INTEGER                         :: numDim
    INTEGER                         :: numComp
    INTEGER                         :: i

    REAL(our_dble), ALLOCATABLE     :: cov(:,:)
    REAL(our_dble), ALLOCATABLE     :: mean(:)
    REAL(our_dble), ALLOCATABLE     :: compList(:)

    REAL(our_dble)                  :: idx


!------------------------------------------------------------------------------
!   algorithm
!------------------------------------------------------------------------------

    ! Auxillary objects.
    numDev  = SIZE(rslt,1)
    numDim  = SIZE(covs,3)
    numComp = SIZE(covs,1)

    ! Allocate arrays.
    ALLOCATE(cov(numDim, numDim))
    ALLOCATE(mean(numDim))
    ALLOCATE(compList(numComp))

    DO i = 1, numComp; compList(i) = i; END DO

    ! Main algorithm.
    DO i = 1, numDev

        CALL choice(idx, compList, shares)

        mean = means(INT(idx),:)
        cov  = covs(INT(idx),:,:)

        CALL normal_rv(rslt(i:i,:), mean, cov)

    END DO

END SUBROUTINE
!****************************************************************************** 
!****************************************************************************** 
SUBROUTINE choice(rslt, elements, probs)
!
!   This subroutine draws a random element with probs.
!
!   Development Notes: The probabilities are required to sum to one, but
!                      only on five digit precision.
!


    !/* external objects    */


    REAL(our_dble), INTENT(INOUT)   :: rslt

    REAL(our_dble), INTENT(IN)      :: elements(:)
    REAL(our_dble), INTENT(IN)      :: probs(:)

    !/*  internal objects    */

    INTEGER(our_int)                :: noElements
    INTEGER(our_int)                :: noProbs
    INTEGER(our_int)                :: i
    INTEGER(our_int)                :: counts

    REAL(our_dble)                  :: sumProbs
    REAL(our_dble)                  :: uniformRv

    LOGICAL                         :: bool


!------------------------------------------------------------------------------
!   algorithm
!------------------------------------------------------------------------------

    ! Antibugging.
    noElements = SIZE(elements)
    noProbs    = SIZE(probs)
    sumProbs   = SUM(probs)

    ! Rounding
    sumProbs = FLOAT(INT(sumProbs * 10000.0 + 0.5)) / 10000.0

    IF(noElements /= noProbs) THEN

        PRINT *, 'error in choice: noElements not equal to noProbs'; STOP

    END IF

    IF(sumProbs /= one_dble) THEN

        PRINT *, 'error in choice: sumProbs not equal to one'; STOP

    END IF

    ! Main algorithm.
    CALL random_number(uniformRv)

    counts = 1

    DO i = 1, noProbs

        bool = (SUM(probs(1:i)) >  uniformRv)

        if(bool) THEN; EXIT; END IF

        counts = counts + one_int

    END DO

    rslt = elements(counts)

END SUBROUTINE
!******************************************************************************
!******************************************************************************
END MODULE
