make

time ./word2vec -train Train_segmented.txt -output vectors112.bin -cbow 5 -size 112 -window 8 -negative 25 -hs 0 -sample 1e-4 -threads 20 -binary 1 -iter 15

