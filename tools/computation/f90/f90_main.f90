!******************************************************************************
!******************************************************************************
!
!   Interface to fortran routines.
!
!   Design Choices:
!
!       Several interfaces are only done for testing purposes. These
!       are available at the end of this file and their names indicate
!       it.
!
!******************************************************************************
!******************************************************************************
SUBROUTINE wrapper_norm_cdf(rslt, x, mean, sd)

    !/* external libraries    */

    USE struct_main

    !/* setup    */

    IMPLICIT NONE

    !/* external objects    */

    DOUBLE PRECISION, INTENT(OUT)       :: rslt

    DOUBLE PRECISION, INTENT(IN)        :: x
    DOUBLE PRECISION, INTENT(IN)        :: mean
    DOUBLE PRECISION, INTENT(IN)        :: sd


!------------------------------------------------------------------------------
! Algorithm
!------------------------------------------------------------------------------

   CALL normal_cdf(rslt, x, mean, sd)
    
END SUBROUTINE
!******************************************************************************
!******************************************************************************
SUBROUTINE wrapper_norm_pdf(rslt, x, mean, sd)

    !/* external libraries    */

    USE struct_main

    !/* setup    */

    IMPLICIT NONE

    !/* external objects    */

    DOUBLE PRECISION, INTENT(OUT)       :: rslt

    DOUBLE PRECISION, INTENT(IN)        :: x
    DOUBLE PRECISION, INTENT(IN)        :: mean
    DOUBLE PRECISION, INTENT(IN)        :: sd

!------------------------------------------------------------------------------
! Algorithm
!------------------------------------------------------------------------------

   CALL normal_pdf(rslt, x, mean, sd)

END SUBROUTINE
!******************************************************************************
!******************************************************************************
SUBROUTINE wrapper_dotproduct(rslt, a, b)

    !/* external libraries    */

    USE struct_main

    !/* setup    */

    IMPLICIT NONE

    !/* external objects    */

    DOUBLE PRECISION, INTENT(OUT)       :: rslt

    DOUBLE PRECISION, INTENT(IN)        :: a(:)
    DOUBLE PRECISION, INTENT(IN)        :: b(:)

!------------------------------------------------------------------------------
! Algorithm
!------------------------------------------------------------------------------

   rslt = DOT_PRODUCT(a,b)

END SUBROUTINE
!******************************************************************************
!******************************************************************************
SUBROUTINE wrapper_clip_value(rslt, x, lowerBound, upperBound)

    !/* external libraries    */

    USE struct_main

    !/* setup    */

    IMPLICIT NONE

    !/* external objects    */

    DOUBLE PRECISION, INTENT(OUT)       :: rslt

    DOUBLE PRECISION, INTENT(IN)        :: x
    DOUBLE PRECISION, INTENT(IN)        :: lowerBound
    DOUBLE PRECISION, INTENT(IN)        :: upperBound


!------------------------------------------------------------------------------
! Algorithm
!------------------------------------------------------------------------------

   CALL clip_value(rslt, x, lowerBound, upperBound)
    
END SUBROUTINE
!******************************************************************************
!******************************************************************************
SUBROUTINE wrapper_normal_univariate_rv(rslt, numDev, mean, sd)

    !/* external libraries    */

    USE struct_main

    !/* setup    */

    IMPLICIT NONE

    !/* external objects    */

    DOUBLE PRECISION, INTENT(OUT)       :: rslt(numDev)
    DOUBLE PRECISION, INTENT(IN)        :: mean
    DOUBLE PRECISION, INTENT(IN)        :: sd

    INTEGER, INTENT(IN)                 :: numDev

!------------------------------------------------------------------------------
! Algorithm
!------------------------------------------------------------------------------

    CALL normal_rv(rslt, mean, sd)

END SUBROUTINE
!******************************************************************************
!******************************************************************************
SUBROUTINE wrapper_normal_multivariate_rv(rslt, numDev, numDim, mean, cov)

    !/* external libraries    */

    USE struct_main

    !/* setup    */

    IMPLICIT NONE

    !/* external objects    */

    DOUBLE PRECISION, INTENT(OUT)       :: rslt(numDev, numDim)

    DOUBLE PRECISION, INTENT(IN)        :: mean(:)
    DOUBLE PRECISION, INTENT(IN)        :: cov(:,:)

    INTEGER, INTENT(IN)                 :: numDev
    INTEGER, INTENT(IN)                 :: numDim

!------------------------------------------------------------------------------
! Algorithm
!------------------------------------------------------------------------------

    ! Antibugging.
    IF(SIZE(cov, 1) /= numDim) THEN

       PRINT *, 'error in wrapper_normal_multivariate_rv'; STOP

    END IF

    IF(SIZE(cov, 2) /= numDim) THEN

       PRINT *, 'error in wrapper_normal_multivariate_rv'; STOP

    END IF

    IF(SIZE(mean) /= numDim) THEN

       PRINT *, 'error in wrapper_normal_multivariate_rv'; STOP

    END IF

    ! Interface to fortran routine.

    CALL normal_rv(rslt, mean, cov)

END SUBROUTINE
!******************************************************************************
!******************************************************************************
SUBROUTINE wrapper_testing_logical_to_integer(indices, bool, numTrue)

    !/* external libraries    */

    USE struct_main

    !/* setup    */

    IMPLICIT NONE

    !/* external objects    */

    INTEGER, INTENT(OUT)        :: indices(numTrue)
    INTEGER, INTENT(IN)         :: numTrue

    LOGICAL, INTENT(IN)         :: bool(:)

!------------------------------------------------------------------------------
! Algorithm
!------------------------------------------------------------------------------

    !/* main    */

    CALL logical_to_integer(indices, bool, numTrue, .TRUE.)

END SUBROUTINE
!******************************************************************************
!******************************************************************************
SUBROUTINE wrapper_testing_cholesky(rslt, matrix, ncol)

    !/* external libraries    */

    USE struct_main

    !/* setup    */

    IMPLICIT NONE

    !/* external objects    */

    DOUBLE PRECISION, INTENT(OUT)       :: rslt(ncol,ncol)
    DOUBLE PRECISION, INTENT(IN)        :: matrix(ncol,ncol)

    INTEGER, INTENT(IN)                 :: ncol

!------------------------------------------------------------------------------
! Algorithm
!------------------------------------------------------------------------------

    CALL cholesky(matrix, rslt)

END SUBROUTINE
!******************************************************************************
!******************************************************************************
SUBROUTINE wrapper_testing_assert_eq_1(arg1, arg2)

    !/* external libraries    */

    USE struct_main

    !/* setup    */

    IMPLICIT NONE

    !/* external objects    */

    INTEGER, INTENT(IN)                 :: arg1
    INTEGER, INTENT(IN)                 :: arg2

!------------------------------------------------------------------------------
! Algorithm
!------------------------------------------------------------------------------

    CALL assert_eq(arg1, arg2)

END SUBROUTINE
!******************************************************************************
!******************************************************************************
SUBROUTINE wrapper_testing_assert_eq_2(arg1, arg2)

    !/* external libraries    */

    USE struct_main

    !/* setup    */

    IMPLICIT NONE

    !/* external objects    */

    DOUBLE PRECISION, INTENT(IN)    :: arg1
    DOUBLE PRECISION, INTENT(IN)    :: arg2

!------------------------------------------------------------------------------
! Algorithm
!------------------------------------------------------------------------------

    CALL assert_eq(arg1, arg2)

END SUBROUTINE
!******************************************************************************
!******************************************************************************
SUBROUTINE wrapper_testing_choice(rslt, elements, probs)

    !/* external libraries    */

    USE struct_main

    !/* setup    */

    IMPLICIT NONE

    !/* external objects    */

    DOUBLE PRECISION, INTENT(OUT)       :: rslt

    DOUBLE PRECISION, INTENT(IN)        :: elements(:)
    DOUBLE PRECISION, INTENT(IN)        :: probs(:)

!------------------------------------------------------------------------------
! Algorithm
!------------------------------------------------------------------------------

    CALL choice(rslt, elements, probs)

END SUBROUTINE
!******************************************************************************
!******************************************************************************
SUBROUTINE wrapper_testing_exp(rslt, arg)
    !
    !   Upper bound set ot intrinsic function HUGE().
    !

    !/* external libraries    */

    USE struct_main

    !/* setup    */

    IMPLICIT NONE

    !/* external objects    */

    DOUBLE PRECISION, INTENT(OUT)       :: rslt
    DOUBLE PRECISION, INTENT(IN)        :: arg

!------------------------------------------------------------------------------
! Algorithm
!------------------------------------------------------------------------------

    rslt = exp_wrapper(arg)

END SUBROUTINE
!******************************************************************************
!******************************************************************************
