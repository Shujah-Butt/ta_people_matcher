import re


def normalize_cnic(cnic):
    """
    Normalize CNIC by removing all non-digit characters.
    Example:
        35202-1234567-8 -> 3520212345678
    """
    if not cnic or str(cnic).strip() == "":
        return None

    return re.sub(r"\D", "", str(cnic))


def normalize_email(email):
    """
    Normalize email by trimming spaces and converting to lowercase.
    """
    if not email or str(email).strip() == "":
        return None

    return str(email).strip().lower()


def normalize_phone(phone):
    """
    Normalize Pakistani phone numbers.

    Examples:
        03001234567
        +92-3001234567
        923001234567

    All become:
        923001234567
    """
    if not phone or str(phone).strip() == "":
        return None

    phone = re.sub(r"\D", "", str(phone))

    if phone.startswith("0"):
        phone = "92" + phone[1:]

    return phone


def normalize_name(name):
    """
    Normalize names by:
    - Lowercasing
    - Removing punctuation
    - Removing extra spaces
    """

    if not name or str(name).strip() == "":
        return None

    name = name.lower()

    name = re.sub(r"[^a-z0-9 ]", "", name)

    name = " ".join(name.split())

    return name