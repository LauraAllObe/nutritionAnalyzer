Nutrition Analyzer
==================
This jupyter notebook project features ingredient list tokenization, fuzzy matching, ingredient pluralization (for added aliases), and common and scientific name equivalent alias retrieval. 

Semantic filters, such as SciSpacy NER, ingredient aliases, health keyword matching, and further filtering are used for data collection from PubMed, OpenFDA, RxNorm, and Google CSE (custom search engine) of each ingredient.

Data is then filtered and cleaned up on a sentence by sentence basis to be used by the LLM Mistral-7B-GPTQ for summary generation of health-effects and dietary restrictions of each ingredient.
The results are evaluated using a human survey, ROUGE-1, ROUGE-L, and BERTScore-F1. Overall, the results show that the model generalizes well and have a competitive edge when compared to the ChatGPT-4o generate summaries from the survey.

This leads us to infer that, with proper preprocessing and finetuning, small, less complex models are able to perform comparatively well with large, complex models for specialized tasks. Given the rise of hallucination with increased complexity and size in recent commercialiized models ([NYTimes article for reference](https://www.nytimes.com/2025/05/05/technology/ai-hallucinations-chatgpt-google.html#:~:text=Is%20Getting%20More%20Powerful%2C%20but,companies%20don't%20know%20why.)), this leads us to infer that maybe, model specialization is needed.

Table of Contents:
==================
1. [project description](https://github.com/LauraAllObe/nutritionAnalyzer?tab=readme-ov-file#nutrition-analyzer)  
2. [demonstration video](https://github.com/LauraAllObe/nutritionAnalyzer?tab=readme-ov-file#demonstration-video)  
3. [file structure](https://github.com/LauraAllObe/nutritionAnalyzer?tab=readme-ov-file#file-structure)  
4. [installation and configuration](https://github.com/LauraAllObe/nutritionAnalyzer?tab=readme-ov-file#installation-and-configuration)  

Demonstration Video:
====================
[![](https://drive.google.com/uc?export=view&id=1RPSXifWlm0xd_eKwdeeEKpIYbI-A3Zop)](https://youtu.be/VEnfEZ0Mcxs)

File Structure:
===============
    nutritionAnalyzer/
    │ ├── .gitignore
    │ ├── environment.yml
    │ ├── nutritionAnalyzer.ipynb
    │ ├── projectReport-may5th2025.pdf
    │ └── README.md
    └── .env

Installation and Configuration:
===============================
Please refer to environment.yml
