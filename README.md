# Structured dataset for Singapore's Parliament Speeches
This project aims to make parliament speeches from Singapore's Parliament Hansard structured and accessible. 

A structured format is an enabler. There are applications in computational linguistic analysis, classification, and political science *(Dritsa et. al., 2022)*. Further empirical research on parliamentary discourse and its wider societal impact in recent times is ever more important, given the decisive role of parlimanets and their rapidly changing relations with the public and media *(Erjavec et. al., 2023)*.

This effort addresses the lack of a centralised dataset for Singapore's parliamentary data analysis. *Rauh et. al. (2022)* observed that while more and more political text is available online in principle, bringing the various, often only rather loosely structured sources into a machine-readable format that is readily amenable to automated analysis still presents a major hurdle. Therefore, this initiative seeks to overcome that hurdle.

## Disclaimer

Please note that this is an entirely independent effort, and this initiative is by no means affiliated with the Singapore Parliament nor Singapore Government.

While best efforts are made to ensure the information is accurate, there may be inevitable parsing errors. Please use the information here with caution and check the underlying data.

# This repository

This repository contains code for the data pipeline which performs the following:

1. **Extract** information from the Singapore parliament's API into a JSON file.
2. **Transform** the information, primarily by way of cleaning speech text and standardising the member's names.
3. **Load** raw files into a database (BigQuery), which are modelled in a [dbt repository](https://github.com/jeremychia/singapore-parliament-speeches-dbt).

The raw data which is generated includes the following:

| model | description |
|-------|-------------|
|attendance|By member, by sitting date, whether the member attended the parliamentary sitting or not.|
|sittings|By sitting date, the associated parliamentary sitting information (parliament number, session number, etc.)
|topics|Each row represents one topic which was discussed during the parliamentary sitting.|
|speeches|Each row represents one paragraph of text, based on the hansard, during the parliamentary sitting. This text corresponds to a speech (or part of a speech) made by a Member of Parliament on a given topic.|

# How to contribute

If you are interested to contribute, please reach out to jeremyjchia@gmail.com. 

# References
* *Dritsa, K., Thoma, A., Pavlopoulos, I., & Louridas, P. (2022). A Greek Parliament Proceedings Dataset for Computational Linguistics and Political Analysis. Advances in Neural Information Processing Systems, 35, 28874-28888.*
* *Erjavec, T., Ogrodniczuk, M., Osenova, P., Ljubešić, N., Simov, K., Pančur, A., ... & Fišer, D. (2023). The ParlaMint corpora of parliamentary proceedings. Language resources and evaluation, 57(1), 415-448.*
* *Rauh, C., & Schwalbach, J. (2020). The ParlSpeech V2 data set: Full-text corpora of 6.3 million parliamentary speeches in the key legislative chambers of nine representative democracies.*