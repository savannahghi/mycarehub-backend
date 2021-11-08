from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from mycarehub.common.models import AbstractBase
from mycarehub.common.models.common_models import Facility


class Identifier(AbstractBase):
    # TODO consider uniqueness of identifiers
    # TODO Identifier types e.g CCC number
    # ID             *string // globally unique identifier
    # ClientID       string  // TODO: FK to client
    # IdentifierType string  // TODO: Enum; start with basics e.g CCC number, ID number
    # IdentifierUse  string  // TODO: Enum; e.g official, temporary, old (see FHIR Person for enum)

    # // TODO: Validate identifier value against type e.g format of CCC number
    # // TODO: Unique together: identifier value & type i.e the same identifier can't be used for
    # more than one client
    # IdentifierValue     string // the actual identifier e.g CCC number
    # Description         string
    # ValidFrom           *time.Time
    # ValidTo             *time.Time
    # Active              bool
    # IsPrimaryIdentifier bool
    pass


class Address(AbstractBase):
    # TODO consider moving this to common
    # TODO implement address model
    # Type       string // TODO: enum; postal, physical or both
    # Text       string // actual address, can be multi-line
    # Country    string // TODO: enum
    # PostalCode string
    # County     string // TODO: counties belong to a country
    pass


class Contact(AbstractBase):
    # TODO Consider moving this to common
    # TODO Implement contacts model
    # type Contact struct {
    # ID string

    # Type string // TODO enum

    # Contact string // TODO Validate: phones are E164, emails are valid

    # Active bool

    # // a user may opt not to be contacted via this contact
    # // e.g if it's a shared phone owned by a teenager
    # OptedIn bool
    # }
    pass


class TermsOfService(AbstractBase):
    # TODO Consider moving this to common
    # TODO Implement terms model
    # ID        string
    # Text      string
    # Flavour   string
    # ValidFrom time.Time
    # ValidTo   time.Time
    pass


class SecurityQuestion(AbstractBase):
    # TODO Implement security question model
    # type SecurityQuestion struct {
    #     ID           string
    #     QuestionStem string
    #     Description  string // help text
    #     ResponseType string // TODO: Enum
    #     Flavour      string // TODO: Enum
    #     Active       bool
    #     Sequence     *int // for sorting
    # }
    pass


class SecurityQuestionResponse(AbstractBase):
    # TODO Implement security question response model
    # type SecurityQuestionResponse struct {
    #     ID string

    #     TimeStamp          time.Time
    #     UserID             string // foreign key to question
    #     SecurityQuestionID string // foreign key to question
    #     Response           string // TODO: ensure we can encode/decode different response types
    # }
    pass


class AuditLog(AbstractBase):
    """
    AuditLog is used to record all senstive changes

    e.g
        - changing a client's treatment buddy
        - changing a client's facility
        - deactivating a client
        - changing a client's assigned community health volunteer

    Rules of thumb: is there a need to find out what/when/why something
    occured? Is a mistake potentially serious? Is there potential for
    fraud?
    """

    # TODO consider moving this to common
    # TODO implement audit model
    # type AuditLog struct {
    #     ID         string
    #     TimeStamp  time.Time
    #     RecordType string // e.g auditing facility changes etc
    #     Notes      string

    #     // this will vary by context
    #     // should not identify the user (there's a UID field)
    #     // focus on the actual event
    #     Payload map[string]string
    # }
    pass


class Metric(AbstractBase):
    # TODO consider moving this to common
    # ID string // ensures we don't re-save the same metric; opaque; globally unique

    # Type string // TODO Metric types should be a controlled list i.e enum

    # // this will vary by context
    # // should not identify the user (there's a UID field)
    # // focus on the actual event
    # Payload map[string]string

    # Timestamp time.Time

    # // a user identifier, can be hashed for anonymity
    # // with a predictable one way hash
    # UserID string
    pass


class RelatedPerson(AbstractBase):
    # TODO: implement this model
    # ID string
    # Active           bool
    # RelatedTo        string // TODO: FK to client
    # RelationshipType string // TODO: enum
    # FirstName        string
    # LastName         string
    # OtherName        string // TODO: optional
    # Gender           string // TODO: enum

    # DateOfBirth *time.Time // TODO: optional
    # Addresses   []*Address // TODO: optional
    # Contacts    []*Contact // TODO: optional
    pass


class Client(AbstractBase):
    """
    A client is a patient or non-professional end user.
    """

    class ClientType(models.TextChoices):
        """
        The client types shown below can be expanded over time:

            - PMTCT: Prevention of mother-to-child transmission;
            all pregnant and breastfeeding women living with HIV.
            Exit when baby turns 2 years.

            - OTZ:  Operation Tripple Zero – for Zero Missed Appointments, zero
            missed Drugs and Zero Viral Load – all HIV positive persons aged
            between 0-19 years

            - OTZ Plus: All women aged between 10-24 years who are pregnant or
            breastfeeding. Exit when baby turns 2 years

            - HVL: High Viral Load – All HIV positive clients with a viral load
            >1,000 copies per ml. Exit when VL is <1,000 copies/ml

            - OVC: Orphans and Vulnerable Children – all children and
            adolescents aged 0-17 years who are enrolled with an OVC partner.
            Exit when they 18 years

            - DREAMS: Determined, Resilient, Empowered, AIDS-free, mentored and
            Safe – all HIV positive 9-24 year old women enroll with a DREAMS
            partner. Exit when they turn 25 years

            - High Risk Clients: all paediatric patients 0-4 yrs, all 0-4 year
            olds with a HIV negative guardian, all clients with low viremia
            (50-999 copies/ml). TI and new in the last 1 year, RTC in the last
            6 months.

            - Spouses of PMTCT mothers who have disclosed – exit when the
            baby turns 2 years

            - Youth: 20–24-year-olds both male and female. Exit when they turn
            25 years
        """

        PMTCT = "PMTCT", _("PMTCT")
        OTZ = "OTZ", _("OTZ")
        OTZ_PLUS = "OTZ_PLUS", _("OTZ Plus")
        HVL = "HVL", _("HVL")
        OVC = "OVC", _("OVC")
        DREAMS = "DREAMS", _("DREAMS")
        HIGH_RISK = "HIGH_RISK", _("High Risk Clients")
        SPOUSES = "SPOUSES", _("SPOUSES")
        YOUTH = "YOUTH", _("Youth")

    client_type = models.CharField(
        max_length=64,
        choices=ClientType.choices,
        null=False,
        blank=False,
    )

    # a client is a user, hence the one-to-one mapping
    # however, the client can be created (e.g via an integration) before
    # the user is invited. This is the reason why this field is nullable.
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    # a client must have an enrollment date.
    # if it is not known, integration code should set a sensible default.
    enrollment_date = models.DateTimeField(null=False, blank=False, auto_now_add=True)

    # the client's FHIR health record ID
    # optional because the client's FHIR health record is created after the client is enrolled
    fhir_patient_id = models.TextField(null=True, blank=True, unique=True)

    # the client's EMR ID
    # optional because it can be updated after the client is added e.g via an integration
    emr_health_record_id = models.TextField(null=True, blank=True, unique=True)

    # each client is assigned to a facility
    current_facility = models.ForeignKey(
        Facility,
        on_delete=models.PROTECT,
        null=False,
        blank=False,
    )

    # a client can be assigned a community health volunteer
    chv = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    # a client can be assigned a treatment buddy
    treatment_buddy = models.TextField(blank=True)

    # a client should only be invited to the platform after they have been
    # counselled
    counselled = models.BooleanField(default=False)

    # a client can have multiple unique identifiers
    identifiers = models.ManyToManyField(Identifier, related_name="client_identifiers")

    addresses = models.ManyToManyField(Address, related_name="client_addresses")

    contacts = models.ManyToManyField(Contact, related_name="client_contacts")

    related_persons = models.ManyToManyField(RelatedPerson, related_name="client_related_persons")

    # TODO Client registration validation
    #   has at least one identifier
    #   has an enrollment date
    # TODO Create a FHIR patient record
    # TODO: Languages []string ? should this be on the client profile ?


# TODO Track client's past facilities
# TODO Client biodata
# TODO Client PINs
# TODO Admin for all these
# TODO Client security questions
# TODO Client registration API
# TODO Only allow invites for a client who's been counselled...send invite link

# TODO: API: AddIdentifier(clientID string, idType string, idValue string, isPrimary bool)
# TODO: API: implement full CRUD, including patch (so that inactivate/reactivate are "automatic")
# TODO: API: client search...across identifiers and human readable fields
# TODO: API: transfer client...origin, destination, reason, notes
# TODO: API: inline identifiers when rendering a client
# TODO: API: generate Swagger/OpenAPI and enable REST Framework editable
# TODO: API: add client identifiers
# TODO: API: CRUD for identifiers, including patch...borrow utilities from ERP or IS
# TODO: API: CRUD and admin for related persons
# TODO: API: add related person
# TODO: API: remove related person
# TODO: API: filters for all models...including client by facility
# TODO: Link this to user and make it a profile...client user profile API
# TODO: inline a calculated treatment duration field?
# TODO: API, CRUD, admin for audit logs
# TODO: API, CRUD, admin for addresses
# TODO: API, CRUD, admin for metrics...metrics collection is just CRUD
# TODO: API, CRUD, admin for security questions and responses
# TODO: API: GetSecurityQuestions(userID string, flavour string, n int)
# TODO: API: RecordSecurityQuestionResponses(responses []*SecurityQuestionResponse,) (bool, error)
# TODO: API: VerifySecurityQuestionResponses(responses []*SecurityQuestionResponse,) (bool, error)
# TODO: model and CRUD and admin for terms
# TODO: model, crud, admin for contacts
# TODO: API to get current terms by flavour
# TODO: Bring facilities API up to spec
# TODO: document OAUth app setup + how to authenticate against this
# TODO: CRUD API for faclities, with list, search, filter, patch
