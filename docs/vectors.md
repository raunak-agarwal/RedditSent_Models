*RedditSent* comes with dense word vectors (100d) trained on unsupervised subword features (between 3 and 6 characters). These vectors were trained using Facebook's [*fasttext*](https://fasttext.cc/). 

## Part 1. Recreate the unsupervised model:

**Note**: This section needs a file `dump.txt` which is just a bunch of sentences escaped with a `\n` )

`git clone https://github.com/facebookresearch/fastText & cd fastText`


`./fasttext skipgram -input dump.txt -output r/result -thread 24 -epoch 20`

This will create two files: `result.bin` and `result.vec`. The first file is the trainable binary while the second file is a hashtable of words and their corresponding vectors. `result.vec` can be used for further downstream tasks (such as text classification) as described in Part 2. 

## Part 2. Run a supervised model with pretrained vectors

**Note**: You need files in fasttext's format to train these.

The files need to be in the following format:

`__label__l1  sentence 1
`

`
__label__l2  sentence 2
`


### Train:
`./fasttext supervised -input \ path_to_trainfile_in_fasttext_format -output output \ -lr 0.05 -epoch 25 -wordNgrams 4 -pretrainedVectors \ path_to_vectors.vec -thread 24  -dim 100 -loss softmax -ws 10`

### Dev:
`./fasttext test path_to_model.vec path_to_dev_in_fasttext_format`

This will print the precision and recall. 