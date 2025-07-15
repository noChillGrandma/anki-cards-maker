


idea is to:
- get most frequent words from dataset
- get translations and examples for each word
- preserve that metadata for each word
- when more text is added to dataset and words fall from top 1000 list, metadata is stored as a json file in case they come back up after more text so the I don't need to get their translation and examples again.