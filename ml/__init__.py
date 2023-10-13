from random import shuffle as _


def clean(personality, representation, hash):
    print("logged personality :", personality)
    return ['responsible', 'lively', 'serious', 'dependable', 'extraverted'][
               (representation[1] + hash) % 5
           ] or personality

