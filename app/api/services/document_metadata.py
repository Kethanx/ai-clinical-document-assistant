DOCUMENT_METADATA = {
    "joglar-et-al-2023-2023-acc-aha-accp-hrs-guideline-for-the-diagnosis-and-management-of-atrial-fibrillation-a-report-of.pdf": {
        "document_title": "2023 ACC/AHA/ACCP/HRS Guideline for the Diagnosis and Management of Atrial Fibrillation",
        "publication_date": "2023",
        "authors": "Joglar JA, et al.",
    },
    "heidenreich-et-al-2022-2022-aha-acc-hfsa-guideline-for-the-management-of-heart-failure-a-report-of-the-american-college.pdf": {
        "document_title": "2022 AHA/ACC/HFSA Guideline for the Management of Heart Failure",
        "publication_date": "2022",
        "authors": "Heidenreich PA, et al.",
    },
    "whelton-et-al-2017-2017-acc-aha-aapa-abc-acpm-ags-apha-ash-aspc-nma-pcna-guideline-for-the-prevention-detection.pdf": {
        "document_title": "2017 ACC/AHA/AAPA/ABC/ACPM/AGS/APhA/ASH/ASPC/NMA/PCNA Guideline for the Prevention, Detection, Evaluation, and Management of High Blood Pressure in Adults",
        "publication_date": "2017",
        "authors": "Whelton PA, et al.",
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