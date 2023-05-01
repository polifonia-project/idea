"""
Main entry point to IDEA's features.

"""
import logging
import argparse

from embeddings import compute_embeddings, SemanticSearch
from extractor import process_stories, add_status_tags
from documentation import update_dataset_docs
from utils import set_logger

logger = logging.getLogger("idea.runner")


def extract_cq_dataset(args):
    """
    Extract competency questions from stories and create the PolifoniaCQ dataset
    after running sanity checks. An extra column is added to the dataset table
    to account for any evident inconsistency found in the CQs. This will also
    update the documentation on the online dashboard.

    Parameters
    ----------
    args : parsed args
        Command-line inputs from argparse. Here, `input_dir` is assumed to hold
        the path to the root of each persona-stories.

    """
    cq_store_df = process_stories(stories_dir=args.input_dir, as_pandas=True)
    logger.info(f"Found {len(cq_store_df)} CQs in {args.input_dir}")
    cq_store_df["issues"] = cq_store_df["cq"].apply(add_status_tags)
    # Saving the CQ dataset with extra column containing sanity checks
    cq_store_df.to_csv("../data/cq_sanity_checks.csv", index=False)

    if args.validate:  # validation of competency questions based on heuristics
        cq_issues = cq_store_df[cq_store_df["issues"] != "pass"]
        # Save in CSV export in markdown for the update
        cq_issues.to_csv("../data/cq_with_issues.csv", index=False)
        cq_issues_md = cq_issues.to_markdown(index=False)
        update_dataset_docs(cq_issues_md)

    return cq_store_df


def compute_cq_embeddings(args):
    """
    Pre-process and embed CQs using the given parameters; and dump everything
    into cleaned CQs, persona (as metadata) and embeddings.

    Parameters
    ----------
    args : parsed args
        Command-line inputs from argparse. Here, `model` is assumed to hold
        the name of the sentence-level embedding model to use.
    
    """
    if args.input_dir is None:
        args.input_dir = "../data/cq_sanity_checks.csv"
    # to dump embeddings
    cleaned_questions, personas, cq_embeddings = compute_embeddings(
        dataset_cq=args.input_dir, model=args.model,
        device=args.device, out_dir="../data/projections/")
    logger.info(f"CQ embeddings computed and dumped at {args.out_dir}")

    return cleaned_questions, personas, cq_embeddings


def semantic_search(args, finder: SemanticSearch = None):
    """
    Implement multi-lingual semantic search.

    Parameters
    ----------
    args : parsed args
        Command-line inputs from argparse. Here, the `model` will recompute the
        embeddings and used for semantic search with the given queries.
    finder : SemanticSearch, optional
        If this was previously initialised, then it will be reused for search.       

    Returns
    -------
    result : list
        Each record holding a similarity score and a matched CQ.
    finder : SemanticSearch
        Stateful object initialised with model and CQ dataset for search.

    """
    if finder is None:  # this initialiases and embeddings
        # This recomputes the embeddings, but should try loading first
        cleaned_questions, _, cq_embeddings = compute_embeddings(
            dataset_cq="../data/cq_sanity_checks.csv",
            model=args.model, as_tblog=False)
        finder = SemanticSearch(
            questions=cleaned_questions,
            embeddings=cq_embeddings,
            model=args.model)

    if not args.as_session:  # a single search is expected
        return finder.search(args.search_query), finder
    while True: # keep session alive for multiple searches
        search_query = input("Provide a search query ('q' to exit): ")
        if 'q' == search_query.rstrip(): last_results = None; break
        last_results = finder.search(search_query, top_k=args.search_topk)

    return last_results, finder


command_map = {
    "dataset": extract_cq_dataset,
    "embed": compute_cq_embeddings,
    "search": semantic_search,
}

def main():
    """
    Main function to read the arguments and use IDEA's current features.
    """
    parser = argparse.ArgumentParser(
        description='Command line interface of the IDEA framework.')

    parser.add_argument('cmd', type=str, choices=list(command_map.keys()),
                        help=f"Either {', '.join(command_map.keys())}.")

    parser.add_argument('input_dir', type=str,
                        help='Directory where the input files will be read.')
    parser.add_argument('--out_dir', type=str,
                        help='Directory where output will be saved.')

    parser.add_argument('--model', action='store', type=str,
                        default='all-MiniLM-L6-v2',
                        help='Name of the language model to use.')
    # dataset params
    parser.add_argument('--validate', action='store_true',
                        help='Whether to validate the competency questions.')
    # search params
    parser.add_argument('--search_query', action='store', type=str,
                        help='A textual query to search against the CQs.')
    parser.add_argument('--as_session', action='store_true',
                        help='Whether to keep a session for more searches.')
    parser.add_argument('--search_topk', action='store', type=int, default=5,
                        help='Number of CQs to retrieve per semantic search.')
    parser.add_argument('--search_threshold', action='store', type=float,
                        help='Similarity threshold for semantic search.')

    parser.add_argument('--device', action='store', type=str, default='cpu',
                        help='The default device to use for computation.')
    parser.add_argument('--n_workers', action='store', type=int, default=1,
                        help='Number of workers for parallel computation.')

    args = parser.parse_args()
    set_logger("idea", log_console=True)
    command_map.get(args.cmd)(args)


if __name__ == "__main__":
    main()
