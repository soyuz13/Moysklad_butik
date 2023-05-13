from typing import List, Optional
from pydantic import BaseModel, Field

# организация
class Meta(BaseModel):
    href: str
    type_: str = Field(..., alias='type')
    media_type: str = Field(..., alias='mediaType')
    metadata_href: Optional[str] = Field(None, alias='metadataHref')
    uuid_href: Optional[str] = Field(None, alias='uuidHref')
    size: Optional[int]
    limit: Optional[int]
    offset: Optional[int]


class Employee(BaseModel):
    meta: Meta


class Context(BaseModel):
    employee: Employee


class Owner(BaseModel):
    meta: Meta


class Group(BaseModel):
    meta: Meta


class Accounts(BaseModel):
    meta: Meta


class Organization(BaseModel):
    meta: Optional[Meta]
    id: Optional[str]
    account_id: Optional[str] = Field(None, alias='accountId')
    owner: Optional[Owner]
    shared: Optional[bool]
    group: Optional[Group]
    updated: Optional[str]
    name: Optional[str]
    external_code: Optional[str] = Field(None, alias='externalCode')
    archived: Optional[bool]
    created: Optional[str]
    company_type: Optional[str] = Field(None, alias='companyType')
    legal_title: Optional[str] = Field(None, alias='legalTitle')
    email: Optional[str]
    accounts: Optional[Accounts]
    is_egais_enable: Optional[bool] = Field(None, alias='isEgaisEnable')
    payer_vat: Optional[bool] = Field(None, alias='payerVat')
    director: Optional[str]
    director_position: Optional[str] = Field(None, alias='directorPosition')
    chief_accountant: Optional[str] = Field(None, alias='chiefAccountant')


class AllOrganizations(BaseModel):
    context: Optional[Context] = None
    meta: Optional[Meta] = None
    rows: Optional[List[Organization]] = None


#склады
class Zones(BaseModel):
    meta: Meta


class Slots(BaseModel):
    meta: Meta


class Store(BaseModel):
    meta: Optional[Meta]
    id: Optional[str]
    account_id: Optional[str] = Field(None, alias='accountId')
    owner: Optional[Owner]
    shared: Optional[bool]
    group: Optional[Group]
    updated: Optional[str]
    name: Optional[str]
    external_code: Optional[str] = Field(None, alias='externalCode')
    archived: Optional[bool]
    path_name: Optional[str] = Field(None, alias='pathName')
    address: Optional[str]
    zones: Optional[Zones]
    slots: Optional[Slots]


class AllStores(BaseModel):
    context: Optional[Context] = None
    meta: Optional[Meta] = None
    rows: Optional[List[Store]] = None


# скидки
class Level(BaseModel):
    amount: float
    discount: float


class Discount(BaseModel):
    meta: Meta
    id: str
    account_id: str = Field(..., alias='accountId')
    name: str
    active: bool
    all_agents: Optional[bool] = Field(None, alias='allAgents')
    agent_tags: Optional[List] = Field(None, alias='agentTags')
    all_products: Optional[bool] = Field(None, alias='allProducts')
    levels: Optional[List[Level]] = None


class AllDiscounts(BaseModel):
    context: Optional[Context] = None
    meta: Optional[Meta] = None
    rows: Optional[List[Discount]] = None


# контрагенты
class Contactpersons(BaseModel):
    meta: Meta


class Notes(BaseModel):
    meta: Meta


class Files(BaseModel):
    meta: Meta


class Disc(BaseModel):
    meta: Meta


class DiscountContragent(BaseModel):
    discount: Disc
    demand_sum_correction: float = Field(None, alias='demandSumCorrection')
    accumulation_discount: float = Field(None, alias='accumulationDiscount')


class Contragent(BaseModel):
    meta: Optional[Meta]
    id: Optional[str]
    account_id: Optional[str] = Field(None, alias='accountId')
    owner: Optional[Owner]
    shared: Optional[bool]
    group: Optional[Group]
    updated: Optional[str]
    name: Optional[str]
    code: Optional[str]
    external_code: Optional[str] = Field(None, alias='externalCode')
    archived: Optional[bool]
    created: Optional[str]
    company_type: Optional[str] = Field(None, alias='companyType')
    phone: Optional[str]
    accounts: Optional[Accounts]
    tags: Optional[List[str]]
    discounts: Optional[List[DiscountContragent]]
    contactpersons: Optional[Contactpersons]
    notes: Optional[Notes]
    discount_card_number: Optional[str] = Field(None, alias='discountCardNumber')
    sales_amount: Optional[float] = Field(None, alias='salesAmount')
    files: Optional[Files]


class AllContragents(BaseModel):
    context: Optional[Context] = None
    meta: Optional[Meta] = None
    rows: Optional[List[Contragent]] = None


#new discount

class NewClientDiscounts(BaseModel):
    discounts: Optional[List[DiscountContragent]] = None


#отгрузки

class Assortment(BaseModel):
    meta: Meta


class TrackingCode(BaseModel):
    cis: str
    type: str


class TrackingCodes(BaseModel):
    cis: str
    type: str
    tracking_codes: List[TrackingCode] = Field(..., alias='trackingCodes')


class Pack(BaseModel):
    id: str


class Position(BaseModel):
    quantity: Optional[int]
    price: Optional[float]
    discount: Optional[int]
    vat: Optional[int]
    assortment: Optional[Assortment]
    tracking_codes: Optional[List[TrackingCodes]] = Field(None, alias='trackingCodes')
    reserve: Optional[int]
    overhead: Optional[int]
    pack: Optional[Pack] = None
    cost: Optional[int] = None


class Demand(BaseModel):
    organization: Organization
    agent: Contragent
    store: Store
    name: Optional[str]
    code: Optional[str]
    moment: Optional[str]
    applicable: Optional[bool]
    vat_enabled: Optional[bool] = Field(None, alias='vatEnabled')
    vat_included: Optional[bool] = Field(None, alias='vatIncluded')
    positions: Optional[List[Position]]


# товары
class ProductFolder(BaseModel):
    meta: Meta


class Uom(BaseModel):
    meta: Meta


class Images(BaseModel):
    meta: Meta


class Currency(BaseModel):
    meta: Meta


class MinPrice(BaseModel):
    value: float
    currency: Currency


class PriceType(BaseModel):
    meta: Meta
    id: str
    name: str
    external_code: str = Field(..., alias='externalCode')


class SalePrice(BaseModel):
    value: float
    currency: Currency
    price_type: PriceType = Field(..., alias='priceType')


class BuyPrice(BaseModel):
    value: float
    currency: Currency


class Barcode(BaseModel):
    ean13: str


class Product(BaseModel):
    meta: Optional[Meta]
    id: Optional[str]
    account_id: Optional[str] = Field(None, alias='accountId')
    owner: Optional[Owner] = None
    shared: Optional[bool] = None
    group: Optional[Group] = None
    updated: Optional[str] = None
    name: Optional[str] = None
    code: Optional[str] = None
    external_code: Optional[str] = Field(None, alias='externalCode')
    archived: Optional[bool] = None
    path_name: Optional[str] = Field(None, alias='pathName')
    product_folder: Optional[ProductFolder] = Field(None, alias='productFolder')
    effective_vat: Optional[int] = Field(None, alias='effectiveVat')
    effective_vat_enabled: Optional[bool] = Field(None, alias='effectiveVatEnabled')
    vat: Optional[int] = None
    vat_enabled: Optional[bool] = Field(None, alias='vatEnabled')
    use_parent_vat: Optional[bool] = Field(None, alias='useParentVat')
    uom: Optional[Uom] = None
    images: Optional[Images] = None
    min_price: Optional[MinPrice] = Field(None, alias='minPrice')
    sale_prices: Optional[List[SalePrice]] = Field(None, alias='salePrices')
    buy_price: Optional[BuyPrice] = Field(None, alias='buyPrice')
    barcodes: Optional[List[Barcode]] = None
    payment_item_type: Optional[str] = Field(None, alias='paymentItemType')
    discount_prohibited: Optional[bool] = Field(None, alias='discountProhibited')
    article: Optional[str] = None
    weighed: Optional[bool] = None
    weight: Optional[float] = None
    volume: Optional[float] = None
    variants_count: Optional[int] = Field(None, alias='variantsCount')
    is_serial_trackable: Optional[bool] = Field(None, alias='isSerialTrackable')
    tracking_type: Optional[str] = Field(None, alias='trackingType')
    files: Optional[Files] = None


class Products(BaseModel):
    context: Optional[Context] = None
    meta: Optional[Meta] = None
    rows: Optional[List[Product]] = None


#платеж
class Operation(BaseModel):
    meta: Optional[Meta]
    linked_sum: Optional[int] = Field(None, alias='linkedSum')


class Operations(BaseModel):
    operations: Optional[List[Operation]] = None


# получение шаблона платежа
class Rate(BaseModel):
    currency: Currency


class Agent(BaseModel):
    meta: Meta


class AgentAccount(BaseModel):
    meta: Meta


class OrganizationAccount(BaseModel):
    meta: Meta


class PaymentInTemplate(BaseModel):
    applicable: Optional[bool] = None
    created: Optional[str] = None
    printed: Optional[bool] = None
    published: Optional[bool] = None
    rate: Optional[Rate] = None
    sum: Optional[int] = None
    agent: Optional[Agent] = None
    organization: Optional[Organization] = None
    agent_account: Optional[AgentAccount] = Field(None, alias='agentAccount')
    organization_account: Optional[OrganizationAccount] = Field(
        None, alias='organizationAccount'
    )
    payment_purpose: Optional[str] = Field(None, alias='paymentPurpose')
    operations: Optional[List[Operation]] = None
    moment: Optional[str]
    name: Optional[str]
