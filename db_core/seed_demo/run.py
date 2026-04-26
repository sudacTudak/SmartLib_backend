from __future__ import annotations

import uuid
from io import StringIO
from typing import TYPE_CHECKING, Any

from django.conf import settings
from django.core.management import call_command
from django.db import transaction

from amenity.models import Amenity
from amenity.models.amenity_vendor.model import AmenityVendor
from authors.models import Author
from books_model.models import Book, BookBasis, Genre
from feedback.models import BookBasisFeedback, LibraryBranchFeedback
from db_core.seed_demo import data as seed_data
from inventory_movement.enums import InventoryMovementType
from inventory_movement.models import InventoryMovement
from library.models import LibraryBranch
from positions.models import StaffPosition
from suppliers.models import Supplier
from users.enums import UserRole
from users.models import CustomUser, UserPermission

if TYPE_CHECKING:
    from django.core.management.base import OutputWrapper


def _validate_demo_config() -> None:
    library_ids = {b.id for b in seed_data.LIBRARY_BRANCHES}
    position_ids = {p.id for p in seed_data.STAFF_POSITIONS}
    genre_ids = {g.id for g in seed_data.GENRES}
    author_ids = {a.id for a in seed_data.AUTHORS}
    book_basis_ids = {bb.id for bb in seed_data.BOOK_BASES}
    vendor_ids = {v.id for v in seed_data.AMENITY_VENDORS}
    supplier_ids = {s.id for s in seed_data.SUPPLIERS}

    if seed_data.DEMO_PRESENCE_LIBRARY_ID not in library_ids:
        raise ValueError("DEMO_PRESENCE_LIBRARY_ID должен совпадать с id одного из LIBRARY_BRANCHES")

    for spec in seed_data.MANAGERS + seed_data.LIBRARY_ADMINS:
        if spec.library_id not in library_ids:
            raise ValueError(f"Неизвестный library_id у пользователя {spec.email!r}")
        if spec.position_id not in position_ids:
            raise ValueError(f"Неизвестный position_id у пользователя {spec.email!r}")

    for bb in seed_data.BOOK_BASES:
        if bb.genre_id not in genre_ids:
            raise ValueError(f"Неизвестный genre_id у BookBasis id={bb.id}")
        if not bb.author_ids:
            raise ValueError(f"Пустой author_ids у BookBasis id={bb.id}")
        for aid in bb.author_ids:
            if aid not in author_ids:
                raise ValueError(f"Неизвестный author_id {aid!r} у BookBasis id={bb.id}")

    for fb in seed_data.BOOK_BASIS_FEEDBACKS:
        if fb.book_basis_id not in book_basis_ids:
            raise ValueError(f"Неизвестный book_basis_id в BOOK_BASIS_FEEDBACKS: {fb.book_basis_id}")
        if fb.client_email != seed_data.CLIENT_USER.email:
            raise ValueError(f"Неизвестный client_email в BOOK_BASIS_FEEDBACKS: {fb.client_email!r}")

    for lf in seed_data.LIBRARY_BRANCH_FEEDBACKS:
        if lf.library_branch_id not in library_ids:
            raise ValueError(f"Неизвестный library_branch_id в LIBRARY_BRANCH_FEEDBACKS: {lf.library_branch_id}")
        if lf.client_email != seed_data.CLIENT_USER.email:
            raise ValueError(f"Неизвестный client_email в LIBRARY_BRANCH_FEEDBACKS: {lf.client_email!r}")

    inv_movement_ids: set[str] = set()
    for row in seed_data.INVENTORY_IN:
        if row.id in inv_movement_ids:
            raise ValueError(f"Дублирующийся id поступления в INVENTORY_IN: {row.id}")
        inv_movement_ids.add(row.id)
        if row.book_basis_id not in book_basis_ids:
            raise ValueError(f"Неизвестный book_basis_id в INVENTORY_IN: {row.book_basis_id}")
        if row.library_id not in library_ids:
            raise ValueError("Неизвестный library_id в INVENTORY_IN")
        if row.supplier_id not in supplier_ids:
            raise ValueError("Неизвестный supplier_id в INVENTORY_IN")

    amenity_ids: set[str] = set()
    for row in seed_data.AMENITIES:
        if row.vendor_id not in vendor_ids:
            raise ValueError(f"Неизвестный vendor_id в AMENITIES: {row.vendor_id}")
        if row.library_id not in library_ids:
            raise ValueError("Неизвестный library_id в AMENITIES")
        if row.id in amenity_ids:
            raise ValueError(f"Дублирующийся id amenity: {row.id}")
        amenity_ids.add(row.id)

    if not vendor_ids:
        raise ValueError("Должен быть хотя бы один AMENITY_VENDORS")

    book_instance_ids: set[str] = set()
    for bi in seed_data.BOOK_INSTANCES:
        if bi.book_basis_id not in book_basis_ids:
            raise ValueError(f"Неизвестный book_basis_id в BOOK_INSTANCES: {bi.book_basis_id}")
        if bi.library_id not in library_ids:
            raise ValueError("Неизвестный library_id в BOOK_INSTANCES")
        if bi.id in book_instance_ids:
            raise ValueError(f"Дублирующийся id книги (экземпляр): {bi.id}")
        book_instance_ids.add(bi.id)


@transaction.atomic
def run_seed_demo(
    stdout: OutputWrapper | Any,
    style: Any,
) -> None:
    _validate_demo_config()

    pwd = seed_data.DEFAULT_DEMO_PASSWORD

    positions_by_id: dict[str, StaffPosition] = {}
    for row in seed_data.STAFF_POSITIONS:
        uid = uuid.UUID(row.id)
        pos = StaffPosition.objects.filter(pk=uid).first()
        if pos is None:
            pos = StaffPosition.objects.create(id=uid, name=row.name)
        positions_by_id[row.id] = pos

    if not settings.SUPER_ADMIN.get("password"):
        settings.SUPER_ADMIN["password"] = seed_data.DEFAULT_SUPER_ADMIN_PASSWORD
    call_command("create_admin", stdout=StringIO(), verbosity=0)

    branches_by_id: dict[str, LibraryBranch] = {}
    for row in seed_data.LIBRARY_BRANCHES:
        uid = uuid.UUID(row.id)
        br = LibraryBranch.objects.filter(pk=uid).first()
        if br is None:
            br = LibraryBranch.objects.create(id=uid, address=row.address)
        branches_by_id[row.id] = br

    vendors_by_id: dict[str, AmenityVendor] = {}
    for row in seed_data.AMENITY_VENDORS:
        uid = uuid.UUID(row.id)
        v = AmenityVendor.objects.filter(pk=uid).first()
        if v is None:
            v = AmenityVendor.objects.create(
                id=uid,
                amenity_name=row.amenity_name,
                vendor_name=row.vendor_name,
                preview_link=row.preview_link,
            )
        vendors_by_id[row.id] = v

    for row in seed_data.AMENITIES:
        aid = uuid.UUID(row.id)
        if Amenity.objects.filter(pk=aid).exists():
            continue
        Amenity.objects.create(
            id=aid,
            vendor=vendors_by_id[row.vendor_id],
            library_branch=branches_by_id[row.library_id],
            preview_link="",
        )

    suppliers_by_id: dict[str, Supplier] = {}
    for row in seed_data.SUPPLIERS:
        uid = uuid.UUID(row.id)
        s = Supplier.objects.filter(pk=uid).first()
        if s is None:
            s = Supplier.objects.create(id=uid, name=row.name)
        suppliers_by_id[row.id] = s

    genres_by_id: dict[str, Genre] = {}
    for row in seed_data.GENRES:
        gid = uuid.UUID(row.id)
        g = Genre.objects.filter(pk=gid).first()
        if g is None:
            g = Genre.objects.create(id=gid, title=row.title)
        genres_by_id[row.id] = g

    authors_by_id: dict[str, Author] = {}
    for row in seed_data.AUTHORS:
        aid = uuid.UUID(row.id)
        a = Author.objects.filter(pk=aid).first()
        if a is None:
            a = Author.objects.create(id=aid, name=row.name)
        authors_by_id[row.id] = a

    book_bases_by_id: dict[str, BookBasis] = {}
    for row in seed_data.BOOK_BASES:
        bid = uuid.UUID(row.id)
        bb = BookBasis.objects.filter(pk=bid).first()
        if bb is None:
            bb = BookBasis.objects.create(
                id=bid,
                title=row.title,
                publisher=row.publisher,
                created_year=row.created_year,
                description=row.description,
                genre=genres_by_id[row.genre_id],
                online_version_link=row.online_version_link,
            )
            bb.authors.set(authors_by_id[aid] for aid in row.author_ids)
        book_bases_by_id[row.id] = bb

    for spec in seed_data.BOOK_INSTANCES:
        book_pk = uuid.UUID(spec.id)
        if Book.objects.filter(pk=book_pk).exists():
            continue
        Book.objects.create(
            id=book_pk,
            library_branch=branches_by_id[spec.library_id],
            book_basis=book_bases_by_id[spec.book_basis_id],
            total_count=0,
            available_count=0,
        )

    for row in seed_data.INVENTORY_IN:
        mid = uuid.UUID(row.id)
        if InventoryMovement.objects.filter(pk=mid).exists():
            continue
        basis = book_bases_by_id[row.book_basis_id]
        br = branches_by_id[row.library_id]
        supplier = suppliers_by_id[row.supplier_id]
        qty = row.quantity
        InventoryMovement.objects.create(
            id=mid,
            type=InventoryMovementType.In.value,
            library_branch=br,
            book_basis=basis,
            supplier=supplier,
            quantity=qty,
            reason="",
            comment="Демо-поступление (seed_demo)",
        )
        book = Book.objects.get(book_basis=basis, library_branch=br)
        book.total_count = qty
        book.available_count = qty
        book.save()

    if not CustomUser.objects.filter(email=seed_data.CLIENT_USER.email).exists():
        CustomUser.objects.create_user(
            email=seed_data.CLIENT_USER.email,
            password=pwd,
            first_name=seed_data.CLIENT_USER.first_name,
            last_name=seed_data.CLIENT_USER.last_name,
            role=UserRole.Client.value,
            is_staff=False,
        )

    client_demo = CustomUser.objects.get(email=seed_data.CLIENT_USER.email)
    for spec in seed_data.BOOK_BASIS_FEEDBACKS:
        if BookBasisFeedback.objects.filter(book_basis_id=uuid.UUID(spec.book_basis_id), client=client_demo).exists():
            continue
        BookBasisFeedback.objects.create(
            book_basis=book_bases_by_id[spec.book_basis_id],
            client=client_demo,
            score=spec.score,
            comment=spec.comment,
        )

    for spec in seed_data.LIBRARY_BRANCH_FEEDBACKS:
        branch = branches_by_id[spec.library_branch_id]
        if LibraryBranchFeedback.objects.filter(library_branch=branch, client=client_demo).exists():
            continue
        LibraryBranchFeedback.objects.create(
            library_branch=branch,
            client=client_demo,
            score=spec.score,
            comment=spec.comment,
        )

    admin_only_codes = {p.value for p in CustomUser.admin_only_permissions}
    manager_perms = UserPermission.objects.exclude(code__in=admin_only_codes)
    all_perms = UserPermission.objects.all()

    for spec in seed_data.MANAGERS:
        if CustomUser.objects.filter(email=spec.email).exists():
            continue
        br = branches_by_id[spec.library_id]
        pos = positions_by_id[spec.position_id]
        user = CustomUser.objects.create_staff(
            email=spec.email,
            password=pwd,
            first_name=spec.first_name,
            last_name=spec.last_name,
            role=UserRole.Manager.value,
            is_staff=True,
            profile_data={"library_branch": br, "position": pos},
        )
        user.user_permissions.set(manager_perms)

    for spec in seed_data.LIBRARY_ADMINS:
        if CustomUser.objects.filter(email=spec.email).exists():
            continue
        br = branches_by_id[spec.library_id]
        pos = positions_by_id[spec.position_id]
        user = CustomUser.objects.create_staff(
            email=spec.email,
            password=pwd,
            first_name=spec.first_name,
            last_name=spec.last_name,
            role=UserRole.Admin.value,
            is_staff=True,
            is_superuser=False,
            profile_data={"library_branch": br, "position": pos},
        )
        user.user_permissions.set(all_perms)

    stdout.write(style.SUCCESS("Демо-данные применены (отсутствующие записи созданы, существующие не трогались)."))
