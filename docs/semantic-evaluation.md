# Semantic search: initial evaluation

CareerPulse ranks Madrid job offers with non-empty descriptions using
`intfloat/multilingual-e5-small`.

On 12 October 2026, I inspected offers stored in PostgreSQL and wrote four
Spanish queries based on their descriptions. For each query, I checked whether
one known relevant offer appeared among the first three results.

| Query topic | Relevant job ID | Found in top 3 |
| --- | ---: | --- |
| Turning raw data into useful information | 13 | Yes |
| Data platforms with Azure and Databricks | 22 | Yes |
| AI solutions for banking and insurance | 27 | Yes |
| Loans and customers' ability to repay | 31 | No |

Three of the four known relevant offers appeared in the top three. This was
an exploratory check, not a measurement of general search accuracy: the
examples were selected after inspecting the offers, other results may also
have been relevant, and the dataset is small.

The search currently excludes offers without descriptions. In the inspected
sample, stored descriptions were 500 characters long and sometimes contained
company introductions instead of details about the role. These limitations
may affect ranking.

A stronger evaluation would use a fixed, larger set of queries and manually
label every relevant offer before comparing ranking methods. Similarity
scores express relative ranking; they are not probabilities.