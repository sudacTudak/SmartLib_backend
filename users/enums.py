from common_core.enums import AppStrEnum, AppIntEnum


class UserRole(AppStrEnum):
    Admin = 'admin'
    Manager = 'manager'
    Client = 'client'


class Gender(AppStrEnum):
    Male = 'male'
    Female = 'female'


class UserPermissions(AppIntEnum):
    ManagerAdministration = 0
    ManagerModification = 1
    EditManagerOnlyPermissions = 2
    EditAdminPermissions = 3
    UsersModification = 4
    UsersAdministration = 5
    BookBasesAdministration = 6
    BookBasesModification = 7
    LibraryBranchesAdministration = 8
    LibraryBranchesModification = 9
    BookMovementManagement = 10
    BookReservationManagement = 11
    PositionsModification = 12
    PositionsAdministration = 13
    StaffPositionsAdministration = 14
    ManageSuppliers = 15
