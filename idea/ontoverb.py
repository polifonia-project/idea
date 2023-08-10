"""
Utilities for the verbalisation of an ontology for LM prompting.

Examples of possible uses cases for ontology verbalisation:
- Summarising the features provided by the ontology (doc)
- Using a LM to extract competency questions from the ontology.
- Asking a LM if the ontology can be used for certain requirements.

****************** Note: code is under refactoring! ******************
"""
import logging
from typing import List

import rdflib
from rdflib import Graph
from rdflib import URIRef
from rdflib.namespace import RDF, RDFS, OWL

from queries import NE_QUERY

logger = logging.getLogger("idea.ontoverb")


def verbalise_ontology(ontology_path: str, onto_about : str, onto_desc : str):

    g = Graph()
    g.parse(ontology_path)

    # Everything that has a label is mapped here, otherwise we get a URI label
    label_dict = {s: str(o) for s, _, o in g.triples((None, RDFS.label, None))}
    label_fn = lambda x: label_dict[x] if x in label_dict \
        else str(x).split("/")[-1]  # just get the last part of the URI otw
    comment_dict = {s: str(o) for s, _, o in g.triples((None, RDFS.comment, None))}

    logger.info("Class verbalisation: start")
    class_vrbs = verbalise_classes(g, label_fn, comment_dict)
    logger.info(f"Class verbalisation: found {len(class_vrbs)} classes")

    logger.info("Named entity verbalisation: start")
    nament_vrbs = verbalise_named_entities(g, label_fn, comment_dict)
    logger.info(f"Named entity verbalisation: found {len(class_vrbs)} entities")

    logger.info("Class verbalisation: start")
    relat_vrbs = verbalise_relations(g, label_fn, comment_dict)
    logger.info(f"Class verbalisation: found {len(class_vrbs)} classes")

    return collate_verbalisations(class_vrbs, nament_vrbs, relat_vrbs,
                                  onto_about, onto_desc)



def create_relation_dict(g, relation):
    relation_dict = {}  # subject to all possible objects via relation
    for s, p, o in g.triples((None, relation, None)):
        if isinstance(o, rdflib.term.BNode):
            continue  # skip blank node
        if s not in relation_dict:
            relation_dict[s] = []
        relation_dict[s].append(o)
    return relation_dict



def verbalise_classes(g: rdflib.Graph, label, comment_dict: dict):

    # Classes are first to be extracted, subclasses follow
    classes = [s for s, _, _ in g.triples((None, RDF.type, OWL.Class))]
    subclasses = create_relation_dict(g, relation=RDFS.subClassOf)

    # Step 1: Verbalisation of classes, one by one
    verbalisation_hist = []
    class_verbalisations = []
    for base_class in classes:
        # The base verbalisation is the class label, if available
        vrbn = f"{label(base_class)}"

        if base_class in subclasses:  # list all parent classes
            vrbn += " (subconcept of "  # opening parenthesis
            vrbn += ", ".join([label(u) for u in subclasses[base_class]])
            vrbn += ")"  # closing parenthesis

        if base_class in comment_dict:  # include comment
            vrbn += f": {comment_dict[base_class]}"

        verbalisation_hist.append(base_class)
        class_verbalisations.append(vrbn)

    # Step 2: verbalisation of remaining subclasses
    for subclass in subclasses:  # check remaining subclasses
        if subclass not in verbalisation_hist["classes"]:
            raise NotImplementedError(subclass)

    return class_verbalisations


def verbalise_named_entities(g: rdflib.Graph, label, comment_dict: dict):
    """
    Note: TODO append NE comment (if available) to each named entity.
    Note: FIXME still, a named entity can have more than 1 parent class.
    """
    qres = g.query(NE_QUERY)
    named_entities = {n: c for n, c in list(qres)}

    nentities_verbalisations = []
    for named_entity, named_type in named_entities.items():
        verbalisation = f"{label(named_entity)} is an instance "\
                        f"of class {label(named_type)}."
        nentities_verbalisations.append(verbalisation)

    return nentities_verbalisations


def verbalise_relations(g: rdflib.Graph, label, comment_dict: dict):

    properties  = [s for s, _, _ in g.triples((None,  RDF.type, OWL.ObjectProperty))]
    subprops = create_relation_dict(g, relation=RDFS.subPropertyOf)
    domains = create_relation_dict(g, relation=RDFS.domain)
    ranges = create_relation_dict(g, relation=RDFS.range)

    # Step 1: Verbalisation of classes
    verbalisation_hist = []
    relation_verbalisations = []

    for base_prop in properties:

        # The base verbalisation is the class label, if available
        verbalisation = f"{label(base_prop)}"

        if base_prop in subprops:
            verbalisation += " (subproperty of "  # opening parenthesis
            verbalisation += ", and".join([label(u) for u in subprops[base_prop]])
            verbalisation += ")"  # closing parenthesis

        if base_prop in comment_dict:  # include
            verbalisation += f": {comment_dict[base_prop]}"

        if base_prop in domains:
            verbalisation += f" The domain of this relation can be: "
            verbalisation += ", or ".join([label(u) for u in domains[base_prop]])
            verbalisation += "."

        if base_prop in ranges:
            verbalisation += f" The range of this relation can be: "
            verbalisation += ", or ".join([label(u) for u in ranges[base_prop]])
            verbalisation += "."

        verbalisation_hist.append(base_prop)
        relation_verbalisations.append(verbalisation)

    for subprop in subprops:  # check remaining subclasses
        if subprop not in verbalisation_hist["relations"]:
            raise NotImplementedError(subprop)


def collate_verbalisations(class_verbalisations : List[str],
                           relation_verbalisations : List[str],
                           nentities_verbalisations : List[str],
                           onto_about : str, onto_desc : str):

    ontoverb = ""  # This is the basic prompt with the ontology description
    ontoverb += f"You are given an ontology about {onto_about}. {onto_desc}\n"

    ontoverb += "\n"

    ontoverb += "The main classes of the ontology are listed below:\n"
    for class_verb in class_verbalisations:
        ontoverb += f"- {class_verb}\n"

    ontoverb += "\n"

    ontoverb += "The main named entities (individuals) are listed below:\n"

    for ne_verb in nentities_verbalisations:
        ontoverb += f"- {ne_verb}\n"

    ontoverb += "\n"

    ontoverb += "The main relations of the ontology are listed below:\n"
    for rel_verb in relation_verbalisations:
        ontoverb += f"- {rel_verb}\n"

    return ontoverb
