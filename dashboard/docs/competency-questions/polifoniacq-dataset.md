---
sidebar_position: 1
---

# The PolifoniaCQ dataset

The PolifoniaCQ dataset comprehend all the competency questions that have been contributed so far within the Polifonia project. It is an ongoing effort to iteratively improve the corpus of questions, to facilitate the design, development and testing of ontologies. This allows to link elements of design (then triples) back to competency questions.

> :floppy_disk: The latest version of the dataset is currently available in CSV format at [this link](https://github.com/polifonia-project/idea/blob/main/data/cq_sanity_checks.csv). 

An excerpt of the dataset is given below.

```csv
persona,story,id,cq,issues
Brendan,1_FindTraditionalMusic,CQ1,What tunes have similar geographic origin as tune X?,pass
Brendan,1_FindTraditionalMusic,CQ2,"What tunes are similar to tune X, given similarity measure Y?",pass
Brendan,1_FindTraditionalMusic,CQ3,"Given a set of tunes, from which collections are these tunes?",pass
Brendan,1_FindTraditionalMusic,CQ4,"Given a set of tunes, what tunes are from collection X?",pass
Brendan,1_FindTraditionalMusic,CQ5,What are the metadata for collection X?,pass
Laurent,1_MusicArchives,CQ1,"Can I search for a musical content by applying filters (genre, historical period ...)?",pass
Laurent,1_MusicArchives,CQ2,What types of resources can I find?,pass
Laurent,1_MusicArchives,CQ3,Is the music resource X complete or incomplete?,pass
Laurent,1_MusicArchives,CQ4,Is a dataset attached to resource X?,pass
Laurent,1_MusicArchives,CQ5,Can I add resources as a user?,pass
Laurent,1_MusicArchives,CQ6,How can I share what I find on the site?,pass
Andrea,1_Serendipity,CQ1,Can I find interesting materials without applying filters?,pass
Andrea,1_Serendipity,CQ2,What types of resources can I find?,pass
Andrea,1_Serendipity,CQ3,Is there a way of visualizing all the materials connected to my interests?,pass
```