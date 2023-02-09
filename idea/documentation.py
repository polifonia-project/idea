"""
Update the documentation on the website every time new data is published.
"""
from extractor import process_stories, add_status_tags

DOCS_CQ_ISSUES = "../dashboard/docs/competency-questions/problematic-cqs.md"


def create_competency_questions(stories_path: str, validate=False):
    """
    Create a dataset of raw competency questions extracted from a directory of
    stories. No structure is assumed for this as long as stories/CQs are found
    in markdown files using the convention of the Polifonia project.

    Parameters
    ----------
    stories_path : str
        Path to the directory containing the stories to process.
    validate : bool
        Whether to validate the competency questions for simple errors.

    """
    cq_store_df = process_stories(stories_dir=stories_path, as_pandas=True)
    cq_store_df["issues"] = cq_store_df["cq"].apply(add_status_tags)
    # Dumping competency questions to a CSV file
    cq_store_df.to_csv("../data/cq_sanity_checks.csv", index=False)

    if validate:  # validation of competency questions based on heuristics
        cq_issues = cq_store_df[cq_store_df["issues"] != "pass"]
        # Save in CSV export in markdown for the update
        cq_issues.to_csv("../data/cq_with_issues.csv", index=False)
        cq_issues_md = cq_issues.to_markdown(index=False)
        # Now update the documentation accordingly
        with open(DOCS_CQ_ISSUES, "r") as handle:
            old_cq_issues_md = handle.read()
        table_start = old_cq_issues_md.find("| persona")
        cq_issues_md = old_cq_issues_md[:table_start] + cq_issues_md
        # Re-save the new documentation file to disk
        with open(DOCS_CQ_ISSUES, "w") as handle:
            handle.write(cq_issues_md)  # new version


def main():
    create_competency_questions(
        stories_path="../../stories/",
        validate=True,
    )

if __name__ == "__main__":
    main()
