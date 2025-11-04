import re
import sys
import json

EMAIL_REGEX = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b')
PHONE_REGEX = re.compile(
    r'(?:(?:\+?(\d{1,3}))?[-.\s]?)?(?:\(?(\d{3})\)?[-.\s]?)?(\d{3})[-.\s]?(\d{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?'
)

def extract_contacts_from_html(html_content):
    emails = EMAIL_REGEX.findall(html_content)
    phones = PHONE_REGEX.findall(html_content)

    formatted_phones = []
    for phone in phones:
        country_code = phone[0] or ''
        area_code = phone[1] or ''
        central_office_code = phone[2]
        line_number = phone[3]
        extension = phone[4] or ''

        formatted_phone = ""
        if country_code:
            formatted_phone += f"+{country_code} "
        if area_code:
            formatted_phone += f"({area_code}) "
        formatted_phone += f"{central_office_code}-{line_number}"
        if extension:
            formatted_phone += f" ext. {extension}"

        formatted_phones.append(formatted_phone.strip())

    return {
        "emails": sorted(set(emails)),
        "phone_numbers": sorted(set(formatted_phones))
    }

if __name__ == "__main__":
    html_file_path = "contacts.html"  # default test file

    try:
        with open(html_file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()

        contacts = extract_contacts_from_html(html_content)
        print(json.dumps(contacts, indent=4))
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

