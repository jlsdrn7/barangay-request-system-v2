from ui.register_resident import RegisterResident
from ui.request_document import RequestDocument
from ui.view_requests import ViewRequests
from ui.certificates import Certificates
from ui.manage_residents import ManageResidents
from ui.pending_requests import PendingRequests
from ui.approved_requests import ApprovedRequests
from ui.issued_certificates import IssuedCertificates

def clear_content(content):
    for widget in content.winfo_children():
        widget.destroy()

def go_to_register(content):
    clear_content(content)
    RegisterResident(content).pack(fill="both", expand=True)

def go_to_request(content):
    clear_content(content)
    RequestDocument(content).pack(fill="both", expand=True)

def go_to_view(content):
    clear_content(content)
    ViewRequests(content).pack(fill="both", expand=True)

def go_to_certificates(content):
    clear_content(content)
    Certificates(content).pack(fill="both", expand=True)


def go_to_manage_residents(content):
    clear_content(content)
    ManageResidents(content).pack(fill="both", expand=True)

def go_to_pending_requests(content):
    clear_content(content)
    PendingRequests(content).pack(fill="both", expand=True)

def go_to_approved_requests(content):
    clear_content(content)
    ApprovedRequests(content).pack(fill="both", expand=True)

def go_to_issued_certificates(content):
    clear_content(content)
    IssuedCertificates(content).pack(fill="both", expand=True)
