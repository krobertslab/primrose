# primrose
PRecIsion Medicine Robust Oncology Search Engine (PRIMROSE). Based on the TREC Precision Medicine track data.

## Background 
* Precision medicine (PM), as defined by the Precision Medicine Initiative, is “an emerging approach for disease treatment and prevention that takes into account individual variability in genes, environment, and lifestyle for each person”
* The inaccessibility of precision oncology scientific abstracts and clinical trials has made translating precision treatments into clinical practice challenging
* PRIMROSE seeks to address these challenges by retrieving relavent PM abstracts and clinical trials

## Goal 
 * Implement a search engine that is able to retrieve relavent PM abstracts and clinical trials
  
 ## Data 
 ### Documents
 * 2017 TREC Precision Medicine Track files: http://www.trec-cds.org/2017.html 
 * 2018 TREC Preicison Medicine Track files: http://www.trec-cds.org/2018.html

### Evaluation
 * 2017 TREC Precision Medicine Track files: https://trec.nist.gov/data/precmed2017.html
 * 2018 TREC Precision Medicine Track files: https://trec.nist.gov/data/precmed2018.html
 
 
 ## Whats included in this repository
 * ReactJS PRIMROSE frontend (`src/` and `public/` directories)
 * BioBERT Machine Learning Models (`BiobertNERModelTraining/` directory)
 * Primrose Information Retrival and Deep Learning/Learning to Rank Machine Learning Models (`BackendWebAPI/`) 
 
 ## How to Run 
 Each subfolder contains a README.md file with how to run the code for that specific part of the code. Since the reactJS frontend is located on the root folder, the instructions of how to run it can be seen below. 
 
 1. Make sure that you have node installed (https://nodejs.org). Node installation should come with a npm installation. 
 2. On the command line run the following commands: 
      *  `npm install`
      *  `npm start`
      This should start the ReactJS app which can then be accessed by going to `http://localhost:3000`
      

 ### ReactJS Frontend 
 * Dependencies: Nodejs 
 
 ## Citations 
 Please cite our work! The code for the following two publications are included in this repository, so please check them out for further information about the project!
 
 * Shenoi SJ, Ly V, Soni S, Roberts K. Developing a Search Engine for Precision Medicine. AMIA Jt Summits Transl Sci Proc. 2020 May 30;2020:579-588. PMID: 32477680; PMCID: PMC7233032.
 
 * Greenspan, N., Si, Y., & Roberts, K. (2020). Extracting Concepts for Precision Oncology from the Biomedical Literature. arXiv preprint arXiv:2010.00074.


 

