"""
Конфигурация демо-наполнения БД.

Идентификаторы — явные UUID версии 4 (строки), как в остальных моделях проекта (``uuid.uuid4``).
Значения сгенерированы один раз и зафиксированы в файле, чтобы ссылки между сущностями не расходились.

Связи задаются полями ``*_id`` / ``id`` на dataclass-спеках.
"""

from __future__ import annotations

from dataclasses import dataclass

# --- UUID v4 (фиксированные литералы) ---

LIB_MOSCOW_ID = "b5bda3da-710d-441c-bfe4-756b402fa563"
LIB_SPB_ID = "6047f025-ca4a-491e-8732-c2776eb554cd"

STAFF_CEO_ID = "ad9d361e-14c6-4e71-b0d7-dfbbc78a8e97"
STAFF_BRANCH_DIRECTOR_ID = "4be0fc1a-7ff0-4573-bff4-6356b134f475"
STAFF_BOOKING_MANAGER_ID = "dc0bb6c7-6bc7-4253-9a35-e67613a27854"
STAFF_SUPPLY_MANAGER_ID = "4aa3d88b-b9fa-4404-a5a9-896ad41f2fd9"

VENDOR_COFFEE_ID = "9d7b8cf7-d00e-4626-8a26-0374f8bf8449"
VENDOR_TEA_ID = "6091baab-b3de-4a74-966f-b7c1d4a2deb6"

SUPPLIER_WAREHOUSE_ID = "829083a5-12d2-4c4b-8bb2-8087a868ac13"
SUPPLIER_CLASSIC_IP_ID = "2c4fdc69-2bcc-4f35-85da-5b6c039172c6"

AMENITY_COFFEE_MOSCOW_ID = "7e780c94-fe24-4958-a61b-dbf957966509"
AMENITY_COFFEE_SPB_ID = "72fdf19d-4f85-470f-9ad2-7f4acd802ac3"
AMENITY_TEA_MOSCOW_ID = "a967dbad-7cc4-4f76-9a67-34eae2f46a6d"
AMENITY_TEA_SPB_ID = "a9e285f9-a5b7-441b-b9ec-b26a373df7d4"

G_GENRE_RUSSIAN_ID = "0ff3d7a1-06f7-4fc9-9c75-712dfd827fab"
G_GENRE_WORLD_ID = "d067d40a-4b01-435d-b1e9-4ccd194b85d2"

BB_WAR_PEACE_ID = "31e0641a-d716-4f54-bc28-cec8013629c2"
BB_CRIME_PUNISHMENT_ID = "6ca994d1-a3a4-41da-9da4-034a26dc6ec3"
BB_MASTER_MARGARITA_ID = "e79f917c-7bc9-4abd-9a5f-2df107a84717"
BB_PRIDE_PREJUDICE_ID = "9a1f6915-007b-4ec6-9c5c-fccb75435bae"
BB_1984_ID = "1504d5f7-689a-4204-87fa-8ce095e21513"

AUTH_TOLSTOY_ID = "a1000000-0000-4000-8000-000000000001"
AUTH_DOSTOEVSKY_ID = "a1000000-0000-4000-8000-000000000002"
AUTH_BULGAKOV_ID = "a1000000-0000-4000-8000-000000000003"
AUTH_AUSTEN_ID = "a1000000-0000-4000-8000-000000000004"
AUTH_ORWELL_ID = "a1000000-0000-4000-8000-000000000005"

# Порядок: для каждого BOOK_BASES сначала LIBRARY_BRANCHES[0], затем [1], …
_BOOK_INSTANCE_IDS: tuple[str, ...] = (
    "de5259c2-b14b-4d39-a6ec-52976fd68b43",
    "988f1b6b-f2a2-4d29-b525-c076cad7c0db",
    "ae7f8c79-ab15-42e4-837f-270a9bdef23a",
    "38e2b4e8-cf45-4726-b049-71a9746f311f",
    "924eda50-8b79-4154-99f6-2993316b932e",
    "d150443c-648d-4c1f-a148-5ade649e2e86",
    "ce065b76-9226-4e87-9889-6c015cb494fc",
    "80b65de0-48f6-45b3-b9ab-ec8950e421b0",
    "ad18b633-bb7b-4220-911c-871fbfde5df3",
    "fd1aee57-dc3e-4da7-8b77-6b88d9a207bc",
)

# Порядок как у BOOK_INSTANCES / INVENTORY_IN: для каждого BOOK_BASES × LIBRARY_BRANCHES
_INVENTORY_MOVEMENT_IDS: tuple[str, ...] = (
    "4f33ce0d-5a8b-46fb-ae72-d276562643f6",
    "e278c9de-6df8-47a0-903c-1f9d7941f750",
    "a3f9f499-e4dc-4abb-bc12-cb854265d246",
    "76b1f264-b78c-43c1-9e97-1fdcf6e11757",
    "add4d90b-fe66-47b3-b455-e817ac0b038f",
    "5a86e86f-20c0-49a6-be2f-17ccc1622c13",
    "570f640b-4a10-405a-bd00-539a73fbc17d",
    "1f05eb6a-f972-4e51-b893-b4c158d09fda",
    "d3b8e8b3-f1d6-44ee-a93d-1804139641a3",
    "7e5bc759-a6e6-409f-8d0f-430dcd324fb6",
)

DEFAULT_DEMO_PASSWORD = "demo_demo"
DEFAULT_SUPER_ADMIN_PASSWORD = "demo_demo"

# Контрольный филиал демо (московский) — для ссылок в конфиге и документации.
DEMO_PRESENCE_LIBRARY_ID = LIB_MOSCOW_ID


@dataclass
class StaffPositionSpec:
    id: str
    name: str


@dataclass
class LibraryBranchSpec:
    id: str
    address: str


@dataclass
class AmenityVendorSpec:
    id: str
    amenity_name: str
    vendor_name: str
    preview_link: str


@dataclass
class AmenityLinkSpec:
    id: str
    vendor_id: str
    library_id: str


@dataclass
class SupplierSpec:
    id: str
    name: str


@dataclass
class GenreSpec:
    id: str
    title: str


@dataclass
class AuthorSpec:
    id: str
    name: str


@dataclass
class BookBasisSpec:
    id: str
    title: str
    author_id: str
    publisher: str
    created_year: int
    genre_id: str
    description: str


@dataclass
class BookInstanceSpec:
    id: str
    book_basis_id: str
    library_id: str


@dataclass
class InventoryMovementInSpec:
    id: str
    book_basis_id: str
    library_id: str
    supplier_id: str
    quantity: int


@dataclass
class BookBasisFeedbackSeedSpec:
    """Один клиент — один отзыв на книгу (см. unique в модели)."""

    book_basis_id: str
    client_email: str
    score: int
    comment: str | None = None


@dataclass
class LibraryBranchFeedbackSeedSpec:
    """Один клиент — один отзыв на филиал."""

    library_branch_id: str
    client_email: str
    score: int
    comment: str | None = None


@dataclass
class ClientUserSpec:
    email: str
    first_name: str
    last_name: str


@dataclass
class StaffUserSpec:
    email: str
    first_name: str
    last_name: str
    library_id: str
    position_id: str


STAFF_POSITIONS: list[StaffPositionSpec] = [
    StaffPositionSpec(id=STAFF_CEO_ID, name="Генеральный директор"),
    StaffPositionSpec(id=STAFF_BRANCH_DIRECTOR_ID, name="Директор филиала"),
    StaffPositionSpec(id=STAFF_BOOKING_MANAGER_ID, name="Менеджер по бронированию"),
    StaffPositionSpec(id=STAFF_SUPPLY_MANAGER_ID, name="Менеджер по поставкам"),
]

LIBRARY_BRANCHES: list[LibraryBranchSpec] = [
    LibraryBranchSpec(id=LIB_MOSCOW_ID, address="г. Москва, ул. Литературная, д. 1"),
    LibraryBranchSpec(id=LIB_SPB_ID, address="г. Санкт-Петербург, Невский пр., д. 42"),
]

AMENITY_VENDORS: list[AmenityVendorSpec] = [
    AmenityVendorSpec(
        id=VENDOR_COFFEE_ID,
        amenity_name="Кофе",
        vendor_name="CoffeeVendor",
        preview_link="",
    ),
    AmenityVendorSpec(
        id=VENDOR_TEA_ID,
        amenity_name="Чай",
        vendor_name="TeaVendor",
        preview_link="",
    ),
]

SUPPLIERS: list[SupplierSpec] = [
    SupplierSpec(id=SUPPLIER_WAREHOUSE_ID, name="ООО «Книжный склад»"),
    SupplierSpec(id=SUPPLIER_CLASSIC_IP_ID, name="ИП Поставщик классики"),
]

AMENITIES: list[AmenityLinkSpec] = [
    AmenityLinkSpec(id=AMENITY_COFFEE_MOSCOW_ID, vendor_id=VENDOR_COFFEE_ID, library_id=LIB_MOSCOW_ID),
    AmenityLinkSpec(id=AMENITY_COFFEE_SPB_ID, vendor_id=VENDOR_COFFEE_ID, library_id=LIB_SPB_ID),
    AmenityLinkSpec(id=AMENITY_TEA_MOSCOW_ID, vendor_id=VENDOR_TEA_ID, library_id=LIB_MOSCOW_ID),
    AmenityLinkSpec(id=AMENITY_TEA_SPB_ID, vendor_id=VENDOR_TEA_ID, library_id=LIB_SPB_ID),
]

GENRES: list[GenreSpec] = [
    GenreSpec(id=G_GENRE_RUSSIAN_ID, title="Русская классика"),
    GenreSpec(id=G_GENRE_WORLD_ID, title="Зарубежная классика"),
]

AUTHORS: list[AuthorSpec] = [
    AuthorSpec(id=AUTH_TOLSTOY_ID, name="Л.Н. Толстой"),
    AuthorSpec(id=AUTH_DOSTOEVSKY_ID, name="Ф.М. Достоевский"),
    AuthorSpec(id=AUTH_BULGAKOV_ID, name="М.А. Булгаков"),
    AuthorSpec(id=AUTH_AUSTEN_ID, name="Дж. Остен"),
    AuthorSpec(id=AUTH_ORWELL_ID, name="Дж. Оруэлл"),
]

BOOK_BASES: list[BookBasisSpec] = [
    BookBasisSpec(
        id=BB_WAR_PEACE_ID,
        title="Война и мир",
        author_id=AUTH_TOLSTOY_ID,
        publisher="Эксмо",
        created_year=1869,
        description="Роман-эпопея",
        genre_id=G_GENRE_RUSSIAN_ID,
    ),
    BookBasisSpec(
        id=BB_CRIME_PUNISHMENT_ID,
        title="Преступление и наказание",
        author_id=AUTH_DOSTOEVSKY_ID,
        publisher="АСТ",
        created_year=1866,
        description="",
        genre_id=G_GENRE_RUSSIAN_ID,
    ),
    BookBasisSpec(
        id=BB_MASTER_MARGARITA_ID,
        title="Мастер и Маргарита",
        author_id=AUTH_BULGAKOV_ID,
        publisher="АСТ",
        created_year=1967,
        description="",
        genre_id=G_GENRE_RUSSIAN_ID,
    ),
    BookBasisSpec(
        id=BB_PRIDE_PREJUDICE_ID,
        title="Гордость и предубеждение",
        author_id=AUTH_AUSTEN_ID,
        publisher="Penguin",
        created_year=1813,
        description="",
        genre_id=G_GENRE_WORLD_ID,
    ),
    BookBasisSpec(
        id=BB_1984_ID,
        title="1984",
        author_id=AUTH_ORWELL_ID,
        publisher="ACT",
        created_year=1949,
        description="",
        genre_id=G_GENRE_WORLD_ID,
    ),
]

BOOK_INSTANCES: list[BookInstanceSpec] = [
    BookInstanceSpec(
        id=_BOOK_INSTANCE_IDS[i * len(LIBRARY_BRANCHES) + j],
        book_basis_id=bb.id,
        library_id=lb.id,
    )
    for i, bb in enumerate(BOOK_BASES)
    for j, lb in enumerate(LIBRARY_BRANCHES)
]

INVENTORY_IN: list[InventoryMovementInSpec] = [
    InventoryMovementInSpec(
        id=_INVENTORY_MOVEMENT_IDS[i * len(LIBRARY_BRANCHES) + j],
        book_basis_id=bb.id,
        library_id=lb.id,
        supplier_id=SUPPLIERS[(i + j) % 2].id,
        quantity=5 + (i + j) % 4,
    )
    for i, bb in enumerate(BOOK_BASES)
    for j, lb in enumerate(LIBRARY_BRANCHES)
]

CLIENT_USER = ClientUserSpec(
    email="client@demo.local",
    first_name="Иван",
    last_name="Клиентов",
)

BOOK_BASIS_FEEDBACKS: list[BookBasisFeedbackSeedSpec] = [
    BookBasisFeedbackSeedSpec(
        book_basis_id=BB_WAR_PEACE_ID,
        client_email=CLIENT_USER.email,
        score=5,
        comment="Очень сильное произведение, читал не спеша — рекомендую.",
    ),
    BookBasisFeedbackSeedSpec(
        book_basis_id=BB_1984_ID,
        client_email=CLIENT_USER.email,
        score=4,
        comment="Актуально и по сей день, атмосфера давит в хорошем смысле.",
    ),
]

LIBRARY_BRANCH_FEEDBACKS: list[LibraryBranchFeedbackSeedSpec] = [
    LibraryBranchFeedbackSeedSpec(
        library_branch_id=LIB_MOSCOW_ID,
        client_email=CLIENT_USER.email,
        score=5,
        comment="Уютный зал, персонал помог с выбором. Часто захожу.",
    ),
    LibraryBranchFeedbackSeedSpec(
        library_branch_id=LIB_SPB_ID,
        client_email=CLIENT_USER.email,
        score=4,
        comment="Удобное расположение, много свободных мест для чтения.",
    ),
]

MANAGERS: list[StaffUserSpec] = [
    StaffUserSpec(
        email="manager.moscow@demo.local",
        first_name="Пётр",
        last_name="Менеджеров",
        library_id=LIB_MOSCOW_ID,
        position_id=STAFF_BOOKING_MANAGER_ID,
    ),
    StaffUserSpec(
        email="manager.spb@demo.local",
        first_name="Анна",
        last_name="Записей",
        library_id=LIB_SPB_ID,
        position_id=STAFF_SUPPLY_MANAGER_ID,
    ),
]

LIBRARY_ADMINS: list[StaffUserSpec] = [
    StaffUserSpec(
        email="admin.moscow@demo.local",
        first_name="Сергей",
        last_name="Админов",
        library_id=LIB_MOSCOW_ID,
        position_id=STAFF_BRANCH_DIRECTOR_ID,
    ),
    StaffUserSpec(
        email="admin.spb@demo.local",
        first_name="Ольга",
        last_name="Директорова",
        library_id=LIB_SPB_ID,
        position_id=STAFF_BRANCH_DIRECTOR_ID,
    ),
]
