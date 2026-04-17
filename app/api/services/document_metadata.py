DOCUMENT_METADATA = {
    "joglar-et-al-2023-2023-acc-aha-accp-hrs-guideline-for-the-diagnosis-and-management-of-atrial-fibrillation-a-report-of.pdf": {
        "document_title": "2023 ACC/AHA/ACCP/HRS Guideline for the Diagnosis and Management of Atrial Fibrillation",
        "publication_date": "2023",
        "authors": "Joglar JA, et al.",
    },
    "evaluation-and-management-of-the-child-with-acute-decompensated-heart-failure-a-scientific-statement-from-the-american-heart-association.pdf": {
        "document_title": "Evaluation and Management of the Child With Acute Decompensated Heart Failure",
        "publication_date": "Apr 2026",
        "authors": "Cabrera AG, Price JF, Hong BJ, et al.",
    },
}


def get_document_metadata(document_name: str) -> dict:
    return DOCUMENT_METADATA.get(
        document_name,
        {
            "document_title": document_name,
            "publication_date": "Unknown",
            "authors": "Unknown",
        },
    )