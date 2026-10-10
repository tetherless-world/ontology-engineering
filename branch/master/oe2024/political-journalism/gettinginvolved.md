---
layout: default
title: About
---


## Maintenenance Policy

Our maintainance policy is primarily focused on ensuring that our data remains available for use as long as possible. We will never change the name of our ontology or its URL. This will ensure that references to our ontology will always be valid and that we will not break applications that may come to rely on our ontology in the future. Any future changes to the ontology will be appropriately documented both in the headers of the ontology itself and in accompanying documentation. Future versions of the ontology with “breaking changes” will be hosted at new URLs so that previous versions of the ontology continue to be available.

## Getting Involved

### Standardized Article Keywords
One of the questions that initially inspired this project was
whether media bias can be observed in the coverage
patterns for specific topics across different news outlets. A
major challenge in answering this question was defining
what constitutes a media outlet “covering” a specific
person, topic, or event. The problem is that each news
outlet has its own process for generating keywords,
maintaining an internal taxonomy, and assigning known
keywords to describe articles. Another way to
conceptualize this problem is that if the same exact article
was published by The New York Times and Fox News it is
likely that each publisher would associate a different set of
keywords to the article. Ideally, there exists a way to use
each news outlet’s taxonomy of keywords to bridge the gap
in how the same article might be represented. In the
following sections we will cover some of the potential
solutions to this problem that we hope to continue in future
work.
### Keyword Statistics
Before we attempt to standardize article keywords it is
useful to quantify the scale of the problem by looking at
the unique keywords tagged in NYT articles from 2020 to
2022.
We can see that over 80,000 unique tags are used to
describe the articles with over half of these tags being used
only once. There are 123 keywords that were used to tag
more than 1000 unique articles. These heavily used
keywords often reflect overarching topics like “'United
States Politics and Government'” or commonly written
about people like “'Trump, Donald J.”
6.3 Tag Generation from Mining Relative Use
One solution we explored was to extract how often the
most commonly used keywords appeared in the same
articles. First, we filtered out all keywords that were used
to tag less than 100 unique articles. Then, with the
remaining 1141 keywords we generate a 1141 x 1141
matrix, N, where entry represents how many articles𝑁𝑖𝑗
contain keyword i and do not contain keyword j. We then
normalize by the total number of times keyword i𝑁𝑖𝑗
appears in any article to get our exclusive use ratio. This
exclusive use ratio tells us how often a keyword is used
independently of another keyword. The assumption here is
that if keyword_1 almost always appears in articles with
keyword_2 but there exist a relatively larger number of
articles where keyword_2 is used without keyword_1 then
we might infer that keyword_1 has some subclass
relationship to keyword_2.
We’ll use the following example with keywords
“TikTok” and “Social Media” to illustrate this idea.
“TikTok” has an exclusive use ratio of .21 with respect to
“Social Media.” This means 21 percent of articles with
“TikTok” as a keyword do not have “Social Media” as a
keyword. Additionally, when manually examining the
content of articles that contain both keywords and articles
that contain only “TikTok” there does not appear to be any
obvious difference in the other keywords used or the topic
of the article.
By applying an exclusive use ratio of 0.25 to all
keywords we automatically generate the following
potential subclasses of “Social Media.”
['Facebook Inc', 'Instagram Inc', 'TikTok
(ByteDance)', 'Twitter', 'Zuckerberg, Mark
E']
We acknowledge that this approach for generating topic
and keyword subclasses is not perfect and can be corrupted
by concentrated media cycles when two distinct topics
happen to be connected by a major news story. For
example, this algorithm incorrectly assumes
“Impeachment” is a subclass of “Trump, Donald J”
because almost all articles involving impeachment over the
time span we looked at were referring to the impeachment
of Donald Trump. Still this system allowed us to infer 105
top level article classes with over 300 subclasses.
Additionally, there is no theoretical reason that this process
cannot be applied recursively on less and less common
keywords to generate more levels to the taxonomy. The
most straightforward solution to the problem of incorrectly
generated subclasses is to gather data over a greater time
horizon to prevent influence from specific news cycles.
Another idea is to use the simple taxonomy provided by
the NYT to create rules preventing certain subclass
relationships. An example of such a rule would be
preventing subclasses of descriptors (e.g. impeachment)
from becoming a subclass of any person (e.g. Donald
Trump).
### Tag Generation from Keyword Embeddings
Another approach to generating keywords from the articles
involved a fusion of word embedding techniques taken
from Natural Language Processing and dimensionality
reduction techniques. We used Google’s Bidirectional
Encoder Representations from Transformers (BERT)
model to transform each keyword into a 768 dimension
vector embedding. While the exact generation of these
embeddings from the keyword is a somewhat black box
process, many of the dimensions in the embedding space
connect to real world concepts like person names and
broader topics in government. Our approach was to convert
the most common keywords into embedding vectors, scale
each of these vectors by the number of unique articles
containing that keyword, and then combine these vectors as
columns of a large, 768 x 1141 matrix (768 is from the
dimension of the embeddings vectors and 1141 is from the
number of commonly used keywords). We perform
principal component analysis on this scaled embedding
matrix to get the principal components (i.e. directions) that
capture the most variance in the keywords. Finally, we
search for the keyword with the embedding that has the
closest cosine similarity to each principal component. This
gives us a list of the most likely top level keywords in
order of how much they capture the variance in the article
keywords. The following are the top level keywords
corresponding to the 20 largest principal components.
['Politics and Government', 'Coronavirus
Aid, Relief, and Economic Security Act
(2020)', 'Coronavirus (2019-nCoV)', 'United
States Politics and Government', 'Biden,
Joseph R Jr', 'Books and Literature',
'Republican Party', 'New York City',
'Demonstrations, Protests and Riots',
'Content Type: Personal Profile', 'Social
Media', 'Race and Ethnicity', 'New York
State', 'Presidential Election of 2020',
'Immigration and Emigration', 'Economic
Conditions and Trends', 'Hygiene and
Cleanliness', 'Immigration and Emigration',
'United States Defense and Military
Forces',...
We were initially concerned that these results were simply
the 20 most commonly used keywords, but 7 out of 20
automatically selected keywords do not appear in the list of
commonly used keywords. Furthermore, the ordering of
the automatically selected keywords is not simply based on
the occurrence count. The goal of this approach was that
we could generate a basis of keywords for each media
outlet’s keyword taxonomy and then perform a change of
basis to convert articles from one publisher’s tags to
another. However, this technique quickly loses
effectiveness on most proper names, lesser known events,
and for distinguishing keywords that have similar words or
spellings but refer to very different concepts.
### General Ontology Additions
An important addition is the support for terms of political
offices existing over a certain time interval and a person
would play that role for that time interval.
An important semantic addition would be to infer an
election winner agent probably plays the role of a term of
office. The reason the general election winner can only be
a probable office holder is due to the threat that the winner
may die before taking office or be otherwise unable to take
office. Another reason is that the winner may simply
decline appointment to the office, although this mainly
happens for write-ins at the local level.
Another semantic addition would be to infer a primary
candidate is probably a candidate in the general election.
The reason the primary election winner can only be a
probable candidate is likewise due to the threat of the
candidate being unable to fill the role or declining that role.

- Avery Iorio (iorioa@rpi.edu)
- Kirk Olkowski (olkowk@rpi.edu)
- Nathaniel Adair (adairn@rpi.edu)
