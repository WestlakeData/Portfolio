! pip install -q kaggle
! pip install emoji

from google.colab import files, drive

files.upload() # Select Kaggle.json for API key
drive.mount('/content/drive') #mount google drive to colab /content/
! mkdir ~/.kaggle
! cp kaggle.json ~/.kaggle/
! chmod 600 ~/.kaggle/kaggle.json
# Download dataset from Kaggle
! kaggle datasets download -d swaptr/turkey-earthquake-tweets
! unzip turkey-earthquake-tweets.zip

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import emoji
from gensim.parsing.preprocessing import remove_stopwords
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import gensim
from tensorflow.keras.layers import *
from tensorflow.keras.models import *
from keras.optimizers import *

# Import Data to train the sentiment analysis model
train = pd.read_csv('/PATH/TO/TRAINING/DATA/train.csv')
train = train[[0,5]] # Select columns of interest
train.columns = ['sentiment','content'] # Name Columns
train.sentiment = train.sentiment.replace([4], 1) #Update DV
train.sentiment = train.sentiment.astype('bool')
# Import Data for classification
data = pd.read_csv('tweets.csv')
data = data.loc[data['language'] =='en'] # Select only English Tweets
data = data.loc[(data['source'] == 'Twitter for iPhone') | (data['source'] == 'Twitter for Android') | (data['source'] == 'Twitter Web App')] # Select only mobile and web app tweets

# Function to retrieve top few number of each category
def getTrainSample(top_n = 5000):
    trainSample_positive = train[train['sentiment'] == 1].head(top_n)
    trainSample_negative = train[train['sentiment'] == 0].head(top_n)
    trainSample_small = pd.concat([trainSample_positive, trainSample_negative])
    return trainSample_small

# Function call to get the top 50000 from each sentiment
train = getTrainSample(top_n=50000)
train = train.sample(frac=1) # random shuffle of data set

# Function to clean tweet data prior to conversion to embeddings
def cleaner(tweet):
    tweet = re.sub("@[A-Za-z0-9]+","",tweet) #Remove @ sign
    tweet = re.sub("#[A-Za-z0-9]+","",tweet) #Remove # sign
    tweet = re.sub(r"(?:\@|http?\://|https?\://|www)\S+", "", tweet) #Remove http links
    tweet = ''.join(c for c in tweet if c not in emoji.EMOJI_DATA) #Remove Emojis
    tweet = re.sub(r'[^\w\s]', '', tweet) #Remove Punctuation
    tweet = remove_stopwords(tweet) #Remove Stopwords
    return tweet

train['content'] = train['content'].map(lambda x: cleaner(x)) # Clean Training Data set
data['content'] = data['content'].map(lambda x: cleaner(x)) # Clean Classification Data set

#Create Tokenizer
tokenizer = Tokenizer(num_words= 25)
#Build Training Word Index
tokenizer.fit_on_texts(train.content)
#Convert strings to list of indexes
train_seq = tokenizer.texts_to_sequences(train.content)
#Create word index Vocabulary
train_wordIndex = tokenizer.word_index

#Create Tokenizer
tokenizer2 = Tokenizer(num_words= 25)
#Build Word Index
tokenizer2.fit_on_texts(data['content'])
#Convert strings to list of indexes
data_seq = tokenizer2.texts_to_sequences(data['content'])

# Identify max length of tweet in both sets
train_max_length = 0
for tweetNum in range(len(train_seq)):
  lenTweet = len(train_seq[tweetNum])
  if lenTweet > train_max_length:
    train_max_length = lenTweet
data_max_length = 0
for tweetNum in range(len(data_seq)):
  lenTweet = len(data_seq[tweetNum])
  if lenTweet > data_max_length:
    data_max_length = lenTweet

max_length = max(train_max_length, data_max_length)

# Padding seq for tweets where len < max_length
tweets_train = pad_sequences(train_seq, maxlen = max_length)
# Get word2vec embeddings from binary file
wordEmbeddings = gensim.models.KeyedVectors.load_word2vec_format('PATH/TO/GoogleNews-vectors-negative300.bin', binary = True)

# Create embedding matrix, where nrows = vocabulary + 1, ncol = 300
uniqueWords = len(train_wordIndex)
totalWords = uniqueWords + 1
skippedWords = 0
embeddingDim = 300
embeddingMatrix = np.zeros((totalWords, embeddingDim))
for word, index in tokenizer.word_index.items():
  try:
    embeddingVector = wordEmbeddings[word]
  except:
    skippedWords += 1
    pass
  if embeddingVector is not None:
    embeddingMatrix[index] = embeddingVector

# Create embedding layer
embeddingLayer = Embedding(totalWords, embeddingDim, weights = [embeddingMatrix], input_length = max_length, trainable = False)

# Define Model
model = Sequential()
model.add(embeddingLayer)
model.add(SimpleRNN(256, activation = 'relu', return_sequences = True))
model.add(SimpleRNN(512, activation = 'relu'))
model.add(Dense(1, activation = 'sigmoid'))

# Compile Network
opt = SGD(learning_rate= 0.01, decay = 1e-3)
model.compile(loss = 'binary_crossentropy', optimizer = opt, metrics = ['accuracy'])
# Fit Network
history = model.fit(tweets_train, train.sentiment, validation_split = 0.25, epochs = 100, verbose = 1)

# summarize history for accuracy
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.savefig('/PATH/TO/PLOTS/accuracy_plot.jpg')
plt.show()
# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train','test'], loc='upper left')
plt.savefig('/PATH/TO/PLOTS/loss_plot.jpg')

# Padding seq for tweets where len < max_length
tweets_class = pad_sequences(data_seq, maxlen = max_length)
# Predict sentiment on test data
data['pred_sentiment'] = model.predict(tweets_class)
# Save data to file
data.to_csv('/PATH/TO/DATA_FILES/classified_earthquake_data.csv', index = False)