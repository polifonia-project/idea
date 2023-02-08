"""
Utilities for creating a CQ dataset from textual sources.

"""
import re
import logging
from pathlib import Path

from tqdm import tqdm
import pandas as pd

logger = logging.getLogger("idea.extractor")


class IllegalStoryError(Exception):
    pass  # raised whenever a story is not well-formatted

class NoCompetencyQuestionError(Exception):
    pass  # raised when no competency questions are found


def preprocess_question(question: str):
    question = re.sub(r"^CQ\d+:", "", question)
    question = question.strip()
    return question


def extract_competency_questions(story_path: str, cq_re="CQ\d+"):
    """
    Extract the competency questions that can be found from a textual sorce.
    Competency questions are assumed to be identified by a `CQx:` token and
    span until the next CQ starts.
    
    Notes
    -----
    (*) Metadata extraction to be improve using the component header.

    """
    with open(story_path, "r") as handle:
        stotext = handle.read()
    
    meta = re.search(r"# (.+)#(.+)", stotext)
    if meta is None or len(meta.groups()) != 2:
        raise IllegalStoryError("Story title not well-formatted")
    persona, title = meta.group(1), meta.group(2)  # story meta

    if not re.search(cq_re, stotext):  # no competency questions found
        raise NoCompetencyQuestionError(f"No CQs in {story_path}")
    # Detect starting indexes of competency questions
    matches = re.finditer(rf"({cq_re})", stotext)
    cq_names, cq_idxs = zip(*[(s.group(1), s.span()[0]) for s in matches])
    logger.info(f"Found {len(cq_idxs)} CQs in story {story_path}")
    cq_store = [stotext[cq_idxs[i]:cq_idxs[i+1]] 
                for i in range(len(cq_idxs) - 1)]
    # Assume that the last quesstions ends after a double return
    last_chunk = stotext[cq_idxs[-1]:]
    cq_store.append(last_chunk[:last_chunk.find("\n\n")])
    # Minimal textual processing of competency questions
    cq_store = list(map(preprocess_question, cq_store))
    return persona, title, cq_names, cq_store


def extract_competency_questions_table(story_path: str, as_pandas=False):
    """
    A variant of `extract_competency_questions` with output as a table of CQs.
    """
    persona, title, ids, cqs = extract_competency_questions(story_path)
    cq_table = [[persona, title, id, cq] for id, cq in zip(ids, cqs)]

    return pd.DataFrame(cq_table) if as_pandas else cq_table


def process_stories(stories_dir: str, black_list=None, as_pandas=False):
    
    if black_list is None:  # these md files are expected
        black_list = ["readme", "license", "story"]
    stories_paths = [p for p in list(Path(stories_dir).rglob("*.md")) 
                    if p.name.split('.')[0].lower() not in  black_list]
    logger.info(f"Found {len(stories_paths)} stories in {stories_dir}")

    cq_store = []
    for story_path in tqdm(stories_paths):
        try:  # attempt to extract competency questions from text
            cq_store = cq_store + extract_competency_questions_table(story_path)
        except (NoCompetencyQuestionError, IllegalStoryError) as error:
            logger.error(f"No CQs - {error}")

    if as_pandas:
        cq_store = pd.DataFrame(
            cq_store, columns=["persona", "story", "id", "cq"])
    
    return cq_store


def add_status_tags(cq_str: str):

    tags = []
    if "?" not in cq_str:
        tags.append("incomplete")
    if cq_str.count("?") > 1:
        tags.append("to-split")
    if cq_str.count("\n") > 1:
        tags.append("complex")
    if len(cq_str) > 120:
        tags.append("hard")

    return tags if len(tags) > 0 else "pass"
