MODULE struct_modPerformanceEnhancements

	!/*	external modules	*/

    USE struct_modProgramConstants

	!/*	setup	*/

	IMPLICIT NONE

    PRIVATE

    PUBLIC ::   normal_cdf, normal_pdf, clip_value, assert_eq, &
                logical_to_integer, assert_lt, assert_gt, assert_egt, &
                exp_wrapper, assert_true

    !/* polymorhisms */

    INTERFACE assert_eq

        MODULE PROCEDURE assert_eq_1, assert_eq_2

    END INTERFACE

    INTERFACE assert_true

        MODULE PROCEDURE assert_true_1

    END INTERFACE

    INTERFACE assert_lt

        MODULE PROCEDURE assert_lt_1, assert_lt_2

    END INTERFACE

    INTERFACE assert_gt

        MODULE PROCEDURE assert_gt_1, assert_gt_2

    END INTERFACE

    INTERFACE assert_egt

        MODULE PROCEDURE assert_egt_1

    END INTERFACE

CONTAINS
!****************************************************************************** 
!****************************************************************************** 
SUBROUTINE normal_cdf(rslt, x, mean, sd)
!
!  This subroutine calculates the cumulative distribution function
!  based on an error function approximation.
!

	!/*	external objects	*/

   REAL(our_dble), INTENT(IN)		:: x
   REAL(our_dble), INTENT(IN)		:: mean
   REAL(our_dble), INTENT(IN)		:: sd
   REAL(our_dble), INTENT(INOUT)	:: rslt

   !/*	internal objects	*/

   REAL(our_dble)					:: std

!------------------------------------------------------------------------------
!	algorithm
!------------------------------------------------------------------------------

    std = ((x - mean)/sd)/sqrt(two_dble)

    rslt = erf(std)

    rslt = half_dble * (one_dble + rslt)

END SUBROUTINE 
!******************************************************************************
!******************************************************************************
SUBROUTINE normal_pdf(rslt, x, mean, sd)
!
!  This subroutine calculates the density function of a normal distribution.
!
!

    !/* external objects    */

   REAL(our_dble), INTENT(IN)       :: x
   REAL(our_dble), INTENT(IN)       :: mean
   REAL(our_dble), INTENT(IN)       :: sd
   REAL(our_dble), INTENT(INOUT)    :: rslt

   !/*  internal objects    */

   REAL(our_dble)                   :: std

!------------------------------------------------------------------------------
!   algorithm
!------------------------------------------------------------------------------

    std = ((x - mean)/sd)

    rslt = (one_dble/sd)*(one_dble/sqrt(two_dble*pi_dble))*exp(-(std*std)/two_dble)

END SUBROUTINE
!******************************************************************************
!******************************************************************************
SUBROUTINE clip_value(rslt, value, lowerBound, upperBound)

    !/* external objects    */

    REAL(our_dble), INTENT(IN)    :: lowerBound
    REAL(our_dble), INTENT(IN)    :: upperBound
    REAL(our_dble), INTENT(IN) 	  :: value
    REAL(our_dble), INTENT(INOUT) :: rslt

!------------------------------------------------------------------------------
!   algorithm
!------------------------------------------------------------------------------

    !/* antibugging */

    IF(lowerBound > upperBound) THEN

        PRINT *, 'error in clip_value'
        STOP

    END IF

    !/* main algorithms */

    IF(value < lowerBound) THEN

        rslt = lowerBound

    ELSEIF(value > upperBound) THEN

        rslt = upperBound

    ELSE

        rslt = value

    END IF

END SUBROUTINE
!******************************************************************************
!******************************************************************************
SUBROUTINE logical_to_integer(indices, bool, numTrue, truthValue)

    !/* external objects    */

    INTEGER(our_int), INTENT(INOUT)     :: indices(:)

    LOGICAL, INTENT(IN)                 :: bool(:)
    LOGICAL, INTENT(IN)                 :: truthValue
    INTEGER(our_int)                    :: numTrue

    !/* internal objects    */

    INTEGER(our_int)                :: counts
    INTEGER(our_int)                :: i

!------------------------------------------------------------------------------
!   algorithm
!------------------------------------------------------------------------------

    !/* antibugging */

    CALL assert_eq(SIZE(indices), numTrue)

    !/* main    */

    counts = 0

    DO i = 1, SIZE(bool)

        IF(bool(i) .EQV. truthValue) THEN

            counts = counts + 1

            indices(counts) = i

        END IF

    END DO


END SUBROUTINE
!******************************************************************************
!******************************************************************************
SUBROUTINE assert_eq_1(arg1, arg2)

    !/* external objects    */

    INTEGER, INTENT(IN)                 :: arg1
    INTEGER, INTENT(IN)                 :: arg2

!------------------------------------------------------------------------------
!   algorithm
!------------------------------------------------------------------------------

    IF(arg1 /= arg2) THEN

        PRINT *, 'error in assert_eq'
        STOP
    END IF

END SUBROUTINE
!******************************************************************************
!******************************************************************************
SUBROUTINE assert_eq_2(arg1, arg2)

    !/* external objects    */

    REAL(our_dble), INTENT(IN)  :: arg1
    REAL(our_dble), INTENT(IN)  :: arg2

!------------------------------------------------------------------------------
!   algorithm
!------------------------------------------------------------------------------


    IF(arg1 /= arg2) THEN

        PRINT *, 'error in assert_eq'
        STOP

    END IF

END SUBROUTINE
!******************************************************************************
!******************************************************************************
SUBROUTINE assert_true_1(arg)

    !/* external objects    */

    LOGICAL, INTENT(IN)  :: arg

!------------------------------------------------------------------------------
!   algorithm
!------------------------------------------------------------------------------


    IF(arg .EQV. .False.) THEN

        PRINT *, 'error in assert_true'
        STOP

    END IF

END SUBROUTINE
!******************************************************************************
!******************************************************************************
SUBROUTINE assert_lt_1(arg1, arg2)

    !/* external objects    */

    REAL(our_dble), INTENT(IN)          :: arg1
    REAL(our_dble), INTENT(IN)          :: arg2

!------------------------------------------------------------------------------
!   algorithm
!------------------------------------------------------------------------------

    IF(arg1 >= arg2) THEN

        PRINT *, 'error in assert_lt'

        STOP

    END IF

END SUBROUTINE
!******************************************************************************
!******************************************************************************
SUBROUTINE assert_lt_2(arg1, arg2)

    !/* external objects    */

    INTEGER(our_int), INTENT(IN)    :: arg1
    INTEGER(our_int), INTENT(IN)    :: arg2

!------------------------------------------------------------------------------
!   algorithm
!------------------------------------------------------------------------------


    IF(arg1 >= arg2) THEN

        PRINT *, 'error in assert_lt'
        STOP

    END IF

END SUBROUTINE
!******************************************************************************
!******************************************************************************
SUBROUTINE assert_gt_1(arg1, arg2)

    !/* external objects    */

    REAL(our_dble), INTENT(IN)  :: arg1
    REAL(our_dble), INTENT(IN)  :: arg2

!------------------------------------------------------------------------------
!   algorithm
!------------------------------------------------------------------------------


    IF(arg1 <= arg2) THEN

        PRINT *, 'error in assert_gt'
        STOP

    END IF

END SUBROUTINE
!******************************************************************************
!******************************************************************************
SUBROUTINE assert_gt_2(arg1, arg2)

    !/* external objects    */

    INTEGER(our_int), INTENT(IN)  :: arg1
    INTEGER(our_int), INTENT(IN)  :: arg2

!------------------------------------------------------------------------------
!   algorithm
!------------------------------------------------------------------------------


    IF(arg1 <= arg2) THEN

        PRINT *, 'error in assert_gt'
        STOP

    END IF

END SUBROUTINE
!******************************************************************************
!******************************************************************************
SUBROUTINE assert_egt_1(arg1, arg2)

    !/* external objects    */

    REAL(our_dble), INTENT(IN)  :: arg1
    REAL(our_dble), INTENT(IN)  :: arg2

!------------------------------------------------------------------------------
!   algorithm
!------------------------------------------------------------------------------


    IF(arg1 < arg2) THEN

        PRINT *, 'error in assert_egt'
        STOP

    END IF

END SUBROUTINE
!******************************************************************************
!******************************************************************************
FUNCTION exp_wrapper(arg)
    !
    !   Upper bound set ot intrinsic function HUGE().
    !

    !/* setup    */

    IMPLICIT NONE

    !/* external objects    */

    REAL(our_dble)                  :: exp_wrapper
    REAL(our_dble), INTENT(IN)      :: arg

    !/* internal objects    */

    REAL(our_dble)                  :: rslt

!------------------------------------------------------------------------------
! Algorithm
!------------------------------------------------------------------------------

    rslt = EXP(arg)

    !/* handling of overflow    */

    IF(ABS(rslt) > HUGE(arg)) THEN

        rslt = HUGE(arg)

    END IF


    !/* finishing   */

    exp_wrapper = rslt

END FUNCTION
!******************************************************************************
!******************************************************************************
END MODULE
