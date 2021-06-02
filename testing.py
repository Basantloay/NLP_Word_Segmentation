
from WordSegmentation import slice_result
from chattymarkov import ChattyMarkov
import time

# insert these sentences in memory to generate different sentences
markov = ChattyMarkov("memory://")
markov.learn("My favorite animal is the crocodile")
markov.learn("The word animal is six letters long")
markov.learn("the longest list of the longest stuff at the longest domain name at the longest last . com")
markov.learn("The author and publisher of this book have used their best efforts in preparing this book.")
markov.learn("After receiving his PhD there in 1951 and working for two years as an instructor, McCarthy moved to Stanford and then to College, which was to become the official birthplace of the field.")
markov.learn("he convinced them to help him bring together U.S. researchers interested in automata theory, neural nets, and the study of intelligence.")
markov.learn("They organized a two-month workshop at Dartmouth in the summer of 1956.")
markov.learn("Up to now, we have not been very careful to distinguish between nodes and states, but in writing detailed algorithms it’s important to make that distinction.")
markov.learn('far out in the uncharted backwaters of the unfashionable end of the western spiral arm of the galaxy lies a small unregarded yellow sun')
markov.learn("Admissible heuristics can also be derived from the solution cost of a subproblem of a given problem")
markov.learn('Moreover, sensorless agents can be surprisingly useful, primarily because they don’t rely on sensors working properly')
markov.learn('in a hole in the ground there lived a hobbit not a nasty dirty wet hole filled with the ends of worms and an oozy smell nor.')
markov.learn('yet a dry bare sandy hole with nothing in it to sit down on or to eat it was a hobbit hole and that means comfort')
markov.learn('These pins are powered from the analog supply and serve as 10-bit ADC channels')


# call function and calculate time taken and accuracy
totaltime=float((time.time() * 1000))
totalaccuracy=0.0
for i in range(100):
    originalsentence=(markov.generate())
    unspacedsentence = originalsentence.replace(" ", "")
    originalist=(list(originalsentence.split()))
    print("The original list:",originalist)
    milliseconds1 = float((time.time() * 1000))
    accuracy=slice_result(originalist,unspacedsentence)
    print("Taken Time in milliseconds :",float((time.time() * 1000))-milliseconds1)
    print('accuracy : ', accuracy)
    totalaccuracy+=accuracy
    print('-------------------------------------------------------------------------------')

print("Taken Time in milliseconds to Run 100 process:",float((time.time() * 1000))-totaltime)
print("Accuracy over 100 random process",totalaccuracy/100)


######################## plotting ###################################

'''from sklearn.datasets import make_circles
from keras.models import Sequential
from keras.layers import Dense
from matplotlib import pyplot
# generate dataset
X, y = make_circles(n_samples=1000, noise=0.1, random_state=1)
# split into train and test
n_test = 500
trainX, testX = X[:n_test, :], X[n_test:, :]
trainy, testy = y[:n_test], y[n_test:]
# define model
model = Sequential()
model.add(Dense(100, input_dim=2, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
# compile model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
# fit model
history = model.fit(trainX, trainy, validation_data=(testX, testy), epochs=300, verbose=0)
# evaluate the model
_, train_acc = model.evaluate(trainX, trainy, verbose=0)
_, test_acc = model.evaluate(testX, testy, verbose=0)
print('Train: %.3f, Test: %.3f' % (train_acc, test_acc))
# plot loss during training
pyplot.subplot(211)
pyplot.title('Loss')
pyplot.plot(history.history['loss'], label='train')
pyplot.plot(history.history['val_loss'], label='test')
pyplot.legend()
# plot accuracy during training
pyplot.subplot(212)
pyplot.title('Accuracy')
pyplot.plot(history.history['accuracy'], label='train')
pyplot.plot(history.history['val_accuracy'], label='test')
pyplot.legend()
pyplot.show()'''''