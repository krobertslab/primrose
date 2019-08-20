#bin/bash
#This file runs a run and then evaluates it
set -e
for VARIABLE in {0..5}
do
    echo $VARIABLE
    python main.py -b -X $VARIABLE
    perl Evaluation/sample_eval.pl -q Evaluation/abstractsv2.txt out.txt > Abs/resDeep${VARIABLE}.txt
	#python main.py -t -X $VARIABLE 
    #/Users/samshenoi/Documents/CPRIT/trec_eval/trec_eval -q -m official ../trec_eval/qrels-final-trials.txt out.txt >Abs/Trials${VARIABLE}resM.txt
done
#python main.py -b -X 11 > out.txt
#python main.py -t -X 7 > out.txt
#perl Evaluation/sample_eval.pl -q Evaluation/abstractsv2.txt out.txt > res.txt 
#/Users/samshenoi/Documents/CPRIT/trec_eval/trec_eval -q -m official ../trec_eval/qrels-final-trials.txt out.txt >res.txt
#./a.out < out.txt > res2.txt
#Rscript -e "rmarkdown::render('/Users/samshenoi/Documents/CPRIT/CPRIT/Evaluation/ER.Rmd')"
#open ./Evaluation/ER.html