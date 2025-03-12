# RequestClustering

A super simple script to cluster requests (e.g, feature requests) using an LLM to first generate
candidate clusters, and then group items into the most relevant clusters.

Created with repl.it, using the following prompt:

Create a CLI application in python that can be given a CSV, and clusters the CSV rows into thematic clusters, each with a brief descriptive label.
The intended usage is that each CSV row represents a request of some type, for example, a product feature request from a customer, or a suggestion from an employee. In any given use of the app, all of the CSV rows will represent the same type of request. Each CSV row has three fields, first an ID that can be used to link back to the original request, second a title for the request, and third a description of the text. The title will be brief, generally one sentence or less. The description can be up to 4KB but will on average be around 1KB or less.
The app operates like this:
- It reads the rows in the CSV one by one and uses the OpenAI API to get a set of candidate “Clusters” for the rows.
- As it iterates over the rows, it maintains as set of candidate cluster labels based on what has been suggested so far.
- With each new row it passes into the API, it also includes a prompt saying what cluster labels have been seen so far, and instructing the LLM to re-use prior clusters if possible and relevant for the current row, so that the scan avoids creating similar or redundant clusters.
- After this first scan, the app takes a second scan throw all rows passing into the API the current row and the final set of cluster labels, and prompting the API to select which cluster the current row goes into. We’d like to pick the single best cluster for each row.
- Finally, the app outputs the set of cluster labels, and lists the set of row IDs that go in each one.
