MODULE struct_modLinearAlgebra

    !/* external modules    */

    USE struct_modProgramConstants

    !/* setup   */

    IMPLICIT NONE

    PRIVATE

    PUBLIC :: cholesky

CONTAINS
!******************************************************************************
!******************************************************************************
SUBROUTINE cholesky(matrix, factor)
!
!This subroutine generates the cholesky factor of the argument 'matrix' and stores
!the result in the argument 'factor'.
!
IMPLICIT NONE
!Defining arguments
REAL(our_dble), INTENT(IN)     :: matrix(:,:)
REAL(our_dble), INTENT(INOUT)  :: factor(:,:)

!Definition of local variables
REAL(our_dble)                 :: sums
REAL(our_dble), ALLOCATABLE    :: clon(:,:)

INTEGER(our_int)               :: i
INTEGER(our_int)               :: n
INTEGER(our_int)               :: k
INTEGER(our_int)               :: j


!------------------------------------------------------------------------------
!   algorithm
!------------------------------------------------------------------------------

    ! Auxillary objects.
    n = size(matrix,1)

    ! Allocate arrays.
    ALLOCATE(clon(n,n)); clon = matrix

    ! Main algorithm.
    DO j = 1, n

        sums = 0.0

        DO k = 1, (j - 1)

            sums = sums + clon(j,k)**two_dble

        END DO

        clon(j,j) = sqrt(clon(j,j) - sums)

        DO i = (j + 1), n

            sums = zero_dble

            DO k = 1, (j - 1)

                sums = sums + clon(j,k)*clon(i,k)

            END DO

            clon(i,j) = (clon(i,j) - sums)/clon(j,j)

        END DO

    END DO

    !Transfer information from matrix to factor.

    DO i = 1, n

        DO j = 1, n

            IF(i <= j) factor(j,i) = clon(j,i)

        END DO

    END DO

END SUBROUTINE
!******************************************************************************
!******************************************************************************
END MODULE 
