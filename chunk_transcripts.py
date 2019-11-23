import pandas as pd

MAX_CHUNK = 500 # Word length

def numWords(sentence):
    return len(sentence.split())

def transcript_to_chunks(transcript, maxChunkSize):
    sentences = str(transcript).split('.')

    # Array of arrays of string
    chunks = []

    chunk = []
    currentLength = 0
    for sentence in sentences:
        wordsInSentence = numWords(sentence)

        # If adding this one will make it too large, end chunk
        if (currentLength + wordsInSentence) > maxChunkSize:
            chunks.append(chunk) # End chunk

            # Start new chunk with this sentence
            chunk = [sentence]
            currentLength = wordsInSentence
        
        else: # Can add sentence safely to current chunk
            chunk.append(sentence)
            currentLength += wordsInSentence
    
    if (len(chunk) > 0):
        chunks.append(chunk)

    return [' '.join(chunk) for chunk in chunks]

if __name__ == "__main__":
    test = "Hello world. This is a really large string. This is my last chunk"
    print(transcript_to_chunks(test, 10))
