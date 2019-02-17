Lexicons were taken from multiple sources.
1. SocialSent
2. SCL-OPP 

### To Build From Scratch

`wget https://nlp.stanford.edu/projects/socialsent/files/socialsent_subreddits.zip -P data/lexicons`

`unzip data/lexicons/socialsent_subreddits.zip -d data/lexicons`

`
python utils/build_lexicons -lexicon_file data/lexicons/lexicon_file.txt -outfile data/lexicons/new_lexicons.txt 
`

[SocialSent Lexicon Example](../img/lexicon_1.png)