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
G_GENRE_ROMANCE_ID = "777f15b1-9f4d-4921-b5f1-c75c535a1ecb"
G_GENRE_DETECTIVE_ID = "2065cecf-bfcd-43e2-94aa-7091ba49d4d6"
G_GENRE_THRILLER_ID = "44983b84-70f4-4bd4-8b3f-c302a036607b"

BB_WAR_PEACE_ID = "31e0641a-d716-4f54-bc28-cec8013629c2"
BB_CRIME_PUNISHMENT_ID = "6ca994d1-a3a4-41da-9da4-034a26dc6ec3"
BB_MASTER_MARGARITA_ID = "e79f917c-7bc9-4abd-9a5f-2df107a84717"
BB_PRIDE_PREJUDICE_ID = "9a1f6915-007b-4ec6-9c5c-fccb75435bae"
BB_1984_ID = "1504d5f7-689a-4204-87fa-8ce095e21513"

BB_ANNA_KARENINA_ID = "34f5756c-7c2c-4942-b58c-df94b2946e11"
BB_IDIOT_ID = "8c124723-5860-4e2b-b1bb-f6811ae312c9"
BB_FATHERS_SONS_ID = "cce21cc9-0797-4ecc-9cce-f529ba3f99f6"
BB_THREE_COMRADES_ID = "52fa26ed-5bb4-4d11-91f1-c37f9877dc81"
BB_DOG_HEART_ID = "4c8e8487-29fb-4072-876a-0c1e017c1fd5"
BB_ORIENT_EXPRESS_ID = "fe4510fb-a79a-45da-80d4-ee4653189c36"
BB_AND_THERE_NONE_ID = "37a34f44-5b28-40a4-ae23-e1ae4e184d92"
BB_DA_VINCI_CODE_ID = "2db8008c-69d3-4533-b28e-7a84284c1fe9"
BB_GONE_GIRL_ID = "45aca3b4-fc82-4286-9905-bfd0c0cf320f"
BB_DRAGON_TATTOO_ID = "9335cb60-afcd-436a-9d70-ca8f9b9eaaf4"

AUTH_TOLSTOY_ID = "a1000000-0000-4000-8000-000000000001"
AUTH_DOSTOEVSKY_ID = "a1000000-0000-4000-8000-000000000002"
AUTH_BULGAKOV_ID = "a1000000-0000-4000-8000-000000000003"
AUTH_AUSTEN_ID = "a1000000-0000-4000-8000-000000000004"
AUTH_ORWELL_ID = "a1000000-0000-4000-8000-000000000005"

AUTH_TURGENEV_ID = "a1000000-0000-4000-8000-000000000006"
AUTH_REMARQUE_ID = "a1000000-0000-4000-8000-000000000007"
AUTH_CHRISTIE_ID = "a1000000-0000-4000-8000-000000000008"
AUTH_BROWN_ID = "a1000000-0000-4000-8000-000000000009"
AUTH_FLYNN_ID = "a1000000-0000-4000-8000-000000000010"
AUTH_LARSSON_ID = "a1000000-0000-4000-8000-000000000011"
AUTH_HUGO_ID = "a1000000-0000-4000-8000-000000000012"

# Порядок: для каждого WORKS сначала LIBRARY_BRANCHES[0], затем [1], …
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
    "8a51abad-662d-48b3-b26b-6847d43e69a2",
    "695da9ee-c7d2-4c38-91aa-ff80ab51b946",
    "61c37db6-bf87-4da5-9a39-b10a3cf7f399",
    "08ed0dcb-fe44-476a-b1d2-a7088c8ed8e4",
    "cf72ee00-464f-425a-9dbe-8a7cf959fbdc",
    "a05deab9-fd68-4aab-a827-7d10fd26207a",
    "9938b428-38c0-438b-a75d-95020835494c",
    "ee134beb-0bab-4ee4-a6e4-c37df30d9266",
    "3f06ac37-1787-4cff-a055-bb696f3d21cb",
    "8f859f8e-4b5a-4261-9fad-01787ef24a59",
    "ff3b4ac5-fdf7-47a6-ae29-9b30264cdcd4",
    "87b14f33-bafd-42af-bcd0-b7e0323035cb",
    "a4ffd9ee-a853-4df8-bbdc-73d08e1fa2c7",
    "50b66a9c-190d-454a-90d2-45295378045c",
    "5220736b-b9de-4ecb-b1f8-bdd0e7d498ee",
    "7f5e3c08-4e56-4d24-8a70-f3bde8e541db",
    "8d5dbf49-2584-4a00-ba12-914ce0783142",
    "7bd14904-e8ec-467f-8736-af0ded89e65e",
    "4a8b06f8-252c-41e7-bbf8-816537f5dd28",
    "579f5fa0-6687-4d2a-b397-a1dc14370554",
)

# Порядок как у WORK_ITEMS / INVENTORY_IN: для каждого WORKS × LIBRARY_BRANCHES
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
    "18377fc1-21a9-4975-818a-7bb6d52630df",
    "30d8075c-588d-430e-aa35-5adcb381816b",
    "9f037131-176f-4486-b447-d1927192a23d",
    "68e48c5f-e611-4712-a98b-3d80146413a7",
    "a3278801-16b6-48f5-88f1-7ef9dfd9c24d",
    "104d0b4c-7379-40b6-bc45-85fbcd682491",
    "2ac6411e-ff1d-4a1f-85ef-26ee81d69d1f",
    "5e7b73bd-425f-47e0-91a6-1679e6b196cb",
    "4af3ca9b-a706-4bd6-ae9e-dfb753eba799",
    "cf8483ae-8adf-4e19-8d9f-618262530da3",
    "16459eb0-acbf-44a8-96e5-fec22fcabf6b",
    "d62b71a6-20d4-4585-8d13-edb85f5041db",
    "b6e269e0-97c5-4b47-ae10-81d22ec8fd68",
    "e849ca75-50e3-4edc-9b36-be7868ebd752",
    "da5ff968-47b2-42e7-881c-4b22af534d60",
    "7dad9dd8-da5f-4ff0-895a-3bbaaf850cba",
    "51c50b03-c8ef-43af-9cfc-4237c13f2205",
    "ffc93e8a-f573-4e9e-92a5-ad29922acfc1",
    "1e07ba77-dfde-4ddd-b830-6fdceb3b64c1",
    "2575f7e6-8ea2-44ce-9492-9139f4d57ab8",
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
class WorkSpec:
    id: str
    title: str
    author_ids: list[str]
    category: str
    publisher: str
    created_year: int
    genre_ids: list[str]
    description: str
    online_version_link: str | None = None


@dataclass
class WorkItemSpec:
    id: str
    work_id: str
    library_id: str


@dataclass
class InventoryMovementInSpec:
    id: str
    work_id: str
    library_id: str
    supplier_id: str
    quantity: int


@dataclass
class WorkFeedbackSeedSpec:
    """Один клиент — один отзыв на книгу (см. unique в модели)."""

    work_id: str
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
    GenreSpec(id=G_GENRE_ROMANCE_ID, title="Роман"),
    GenreSpec(id=G_GENRE_DETECTIVE_ID, title="Детектив"),
    GenreSpec(id=G_GENRE_THRILLER_ID, title="Триллер"),
]

AUTHORS: list[AuthorSpec] = [
    AuthorSpec(id=AUTH_TOLSTOY_ID, name="Л.Н. Толстой"),
    AuthorSpec(id=AUTH_DOSTOEVSKY_ID, name="Ф.М. Достоевский"),
    AuthorSpec(id=AUTH_BULGAKOV_ID, name="М.А. Булгаков"),
    AuthorSpec(id=AUTH_AUSTEN_ID, name="Дж. Остен"),
    AuthorSpec(id=AUTH_ORWELL_ID, name="Дж. Оруэлл"),
    AuthorSpec(id=AUTH_TURGENEV_ID, name="И.С. Тургенев"),
    AuthorSpec(id=AUTH_REMARQUE_ID, name="Э.М. Ремарк"),
    AuthorSpec(id=AUTH_CHRISTIE_ID, name="Агата Кристи"),
    AuthorSpec(id=AUTH_BROWN_ID, name="Дэн Браун"),
    AuthorSpec(id=AUTH_FLYNN_ID, name="Гиллиан Флинн"),
    AuthorSpec(id=AUTH_LARSSON_ID, name="Стиг Ларссон"),
    AuthorSpec(id=AUTH_HUGO_ID, name="Виктор Гюго"),
]

WORKS: list[WorkSpec] = [
    WorkSpec(
        id=BB_WAR_PEACE_ID,
        title="Война и мир",
        author_ids=[AUTH_TOLSTOY_ID],
        category="book",
        publisher="Эксмо",
        created_year=1869,
        description="Роман-эпопея",
        genre_ids=[G_GENRE_RUSSIAN_ID],
    ),
    WorkSpec(
        id=BB_CRIME_PUNISHMENT_ID,
        title="Преступление и наказание",
        author_ids=[AUTH_DOSTOEVSKY_ID],
        category="book",
        publisher="АСТ",
        created_year=1866,
        description="",
        genre_ids=[G_GENRE_RUSSIAN_ID],
    ),
    WorkSpec(
        id=BB_MASTER_MARGARITA_ID,
        title="Мастер и Маргарита",
        author_ids=[AUTH_BULGAKOV_ID],
        category="book",
        publisher="АСТ",
        created_year=1967,
        description="",
        genre_ids=[G_GENRE_RUSSIAN_ID],
    ),
    WorkSpec(
        id=BB_PRIDE_PREJUDICE_ID,
        title="Гордость и предубеждение",
        author_ids=[AUTH_AUSTEN_ID],
        category="book",
        publisher="Penguin",
        created_year=1813,
        description="",
        genre_ids=[G_GENRE_WORLD_ID],
    ),
    WorkSpec(
        id=BB_1984_ID,
        title="1984",
        author_ids=[AUTH_ORWELL_ID],
        category="book",
        publisher="ACT",
        created_year=1949,
        description="",
        genre_ids=[G_GENRE_WORLD_ID],
    ),
    WorkSpec(
        id=BB_ANNA_KARENINA_ID,
        title="Анна Каренина",
        author_ids=[AUTH_TOLSTOY_ID],
        category="book",
        publisher="Эксмо",
        created_year=1877,
        description="Роман о любви, выборе и последствиях.",
        genre_ids=[G_GENRE_ROMANCE_ID],
        online_version_link="https://example.com/anna-karenina",
    ),
    WorkSpec(
        id=BB_IDIOT_ID,
        title="Идиот",
        author_ids=[AUTH_DOSTOEVSKY_ID],
        category="book",
        publisher="АСТ",
        created_year=1869,
        description="",
        genre_ids=[G_GENRE_RUSSIAN_ID],
    ),
    WorkSpec(
        id=BB_FATHERS_SONS_ID,
        title="Отцы и дети",
        author_ids=[AUTH_TURGENEV_ID],
        category="book",
        publisher="Азбука",
        created_year=1862,
        description="",
        genre_ids=[G_GENRE_ROMANCE_ID],
    ),
    WorkSpec(
        id=BB_THREE_COMRADES_ID,
        title="Три товарища",
        author_ids=[AUTH_REMARQUE_ID],
        category="book",
        publisher="Азбука",
        created_year=1936,
        description="",
        genre_ids=[G_GENRE_ROMANCE_ID],
        online_version_link="https://example.com/three-comrades",
    ),
    WorkSpec(
        id=BB_DOG_HEART_ID,
        title="Собачье сердце",
        author_ids=[AUTH_BULGAKOV_ID],
        category="book",
        publisher="АСТ",
        created_year=1925,
        description="",
        genre_ids=[G_GENRE_RUSSIAN_ID],
    ),
    WorkSpec(
        id=BB_ORIENT_EXPRESS_ID,
        title="Убийство в «Восточном экспрессе»",
        author_ids=[AUTH_CHRISTIE_ID],
        category="book",
        publisher="Эксмо",
        created_year=1934,
        description="Классический детектив с закрытым кругом подозреваемых.",
        genre_ids=[G_GENRE_DETECTIVE_ID],
        online_version_link="https://example.com/orient-express",
    ),
    WorkSpec(
        id=BB_AND_THERE_NONE_ID,
        title="И никого не стало",
        author_ids=[AUTH_CHRISTIE_ID],
        category="book",
        publisher="Эксмо",
        created_year=1939,
        description="",
        genre_ids=[G_GENRE_DETECTIVE_ID],
    ),
    WorkSpec(
        id=BB_DA_VINCI_CODE_ID,
        title="Код да Винчи",
        author_ids=[AUTH_BROWN_ID],
        category="book",
        publisher="ACT",
        created_year=2003,
        description="",
        genre_ids=[G_GENRE_THRILLER_ID],
        online_version_link="https://example.com/da-vinci-code",
    ),
    WorkSpec(
        id=BB_GONE_GIRL_ID,
        title="Исчезнувшая",
        author_ids=[AUTH_FLYNN_ID],
        category="book",
        publisher="АСТ",
        created_year=2012,
        description="",
        genre_ids=[G_GENRE_THRILLER_ID],
    ),
    WorkSpec(
        id=BB_DRAGON_TATTOO_ID,
        title="Девушка с татуировкой дракона",
        author_ids=[AUTH_LARSSON_ID],
        category="book",
        publisher="Эксмо",
        created_year=2005,
        description="",
        genre_ids=[G_GENRE_THRILLER_ID],
    ),
]

WORK_ITEMS: list[WorkItemSpec] = [
    WorkItemSpec(
        id=_BOOK_INSTANCE_IDS[i * len(LIBRARY_BRANCHES) + j],
        work_id=w.id,
        library_id=lb.id,
    )
    for i, w in enumerate(WORKS)
    for j, lb in enumerate(LIBRARY_BRANCHES)
]

INVENTORY_IN: list[InventoryMovementInSpec] = [
    InventoryMovementInSpec(
        id=_INVENTORY_MOVEMENT_IDS[i * len(LIBRARY_BRANCHES) + j],
        work_id=w.id,
        library_id=lb.id,
        supplier_id=SUPPLIERS[(i + j) % 2].id,
        quantity=5 + (i + j) % 4,
    )
    for i, w in enumerate(WORKS)
    for j, lb in enumerate(LIBRARY_BRANCHES)
]

CLIENT_USER = ClientUserSpec(
    email="client@demo.local",
    first_name="Иван",
    last_name="Клиентов",
)

WORK_FEEDBACKS: list[WorkFeedbackSeedSpec] = [
    WorkFeedbackSeedSpec(
        work_id=BB_WAR_PEACE_ID,
        client_email=CLIENT_USER.email,
        score=5,
        comment="Очень сильное произведение, читал не спеша — рекомендую.",
    ),
    WorkFeedbackSeedSpec(
        work_id=BB_1984_ID,
        client_email=CLIENT_USER.email,
        score=4,
        comment="Актуально и по сей день, атмосфера давит в хорошем смысле.",
    ),
    WorkFeedbackSeedSpec(
        work_id=BB_MASTER_MARGARITA_ID,
        client_email=CLIENT_USER.email,
        score=5,
        comment="Перечитываю раз в пару лет — каждый раз замечаю новые детали.",
    ),
    WorkFeedbackSeedSpec(
        work_id=BB_CRIME_PUNISHMENT_ID,
        client_email=CLIENT_USER.email,
        score=4,
        comment="Тяжело, но очень мощно. Хорошо раскрыта психология.",
    ),
    WorkFeedbackSeedSpec(
        work_id=BB_PRIDE_PREJUDICE_ID,
        client_email=CLIENT_USER.email,
        score=5,
        comment="Лёгкий и ироничный роман, отличный перевод.",
    ),
    WorkFeedbackSeedSpec(
        work_id=BB_ORIENT_EXPRESS_ID,
        client_email=CLIENT_USER.email,
        score=5,
        comment="Очень люблю такие детективы — финал не ожидал.",
    ),
    WorkFeedbackSeedSpec(
        work_id=BB_AND_THERE_NONE_ID,
        client_email=CLIENT_USER.email,
        score=4,
        comment="Держит напряжение до последней главы.",
    ),
    WorkFeedbackSeedSpec(
        work_id=BB_DA_VINCI_CODE_ID,
        client_email=CLIENT_USER.email,
        score=3,
        comment="Динамично, но местами слишком киношно.",
    ),
    WorkFeedbackSeedSpec(
        work_id=BB_GONE_GIRL_ID,
        client_email=CLIENT_USER.email,
        score=5,
        comment="Впечатлило. Повороты сюжета — огонь.",
    ),
    WorkFeedbackSeedSpec(
        work_id=BB_THREE_COMRADES_ID,
        client_email=CLIENT_USER.email,
        score=5,
        comment="Очень трогательно. Пронзительная атмосфера.",
    ),
    WorkFeedbackSeedSpec(
        work_id=BB_ANNA_KARENINA_ID,
        client_email=CLIENT_USER.email,
        score=4,
        comment="Классика, но читается удивительно современно.",
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
