# expertSystems
Application to match applicants to job description, papers to reviewers. 

Collaborators: 
  - Ashutosh Upadhye
  - Amish Ranjan Singh
  - Vishal Kumar Chaudhary

Repository structure: 
  - scripts : Contains the scripts for clustering and assigning experts.
  - datasets : Contains various datasets to test.
  
Code Specifications: 
  - Input 
    - Training : papers/training.txt; reviewers' papers.
    - Testing : papers/abstracts.txt; papers to be reviewed. 
  - Output
    - terminal : the start time, knn time and stop time are printed. 
    - out.txt : intermidiate output file.
    - paper_reviewer_score.txt : final output file, to be parsed in evaluate.py.
