"""
Update the documentation on the website every time new data is published.
"""

DOCS_CQ_ISSUES = "../dashboard/docs/competency-questions/problematic-cqs.md"


def update_dataset_docs(cq_issues_md):
    """
    Updates the documentation of the dataset on the website with the new
    list of problematic competency questions that need improvement/revision.

    Parameters
    ----------
    cq_issues_md : str 
        The markdown string containing the list of problematic CQs to append.
    
    """
    with open(DOCS_CQ_ISSUES, "r") as handle:
        old_cq_issues_md = handle.read()
    table_start = old_cq_issues_md.find("| persona")
    cq_issues_md = old_cq_issues_md[:table_start] + cq_issues_md
    # Re-save the new documentation file to disk
    with open(DOCS_CQ_ISSUES, "w") as handle:
        handle.write(cq_issues_md)  # new version


def main():

    # This will update the dashboard with the current problematic CQs
    with open("../data/cq_with_issues.csv", "r") as handle:
        cq_issues_md = handle.read()
    update_dataset_docs(cq_issues_md)


if __name__ == "__main__":
    main()
