def get_triple(line):
    triple = line.split(';;;;ll;;;;')
    if len(triple) == 3:
        return triple[0], triple[1], triple[2].strip()

def get_bigram(line):
    triple = line.split(';;;;ll;;;;')
    if len(triple) == 2:
        return triple[0], triple[1].strip()