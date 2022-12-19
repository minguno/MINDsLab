import re
import Levenshtein as Lev

from tqdm import tqdm
from contextlib import closing
from multiprocessing import Pool
from unicodedata import normalize

def normalize_text(text, lang='kor'):
    if lang == 'kor':
        text = re.sub(r'[^가-힣 ]+', r' ', text)
        text = re.sub(r'\s+', r' ', text)
        text = normalize('NFKD', text)
    elif lang == 'eng':
        text = text.lower()
        text = re.sub(r'[^a-z\' ]+', r' ', text)
        text = re.sub(r'\s+', r' ', text)
    else:
        raise RuntimeError('{} is the wrong language.'.format(lang))
    text = text.strip()
    return text


def parallel_run(fn, items, desc="", n_cpu=1):
    results = []

    if n_cpu > 1:
        with closing(Pool(n_cpu)) as pool:
            for out in tqdm(pool.imap_unordered(
                    fn, items), total=len(items), desc=desc):
                if out is not None:
                    results.append(out)
    else:
        for item in tqdm(items, total=len(items), desc=desc):
            out = fn(item)
            if out is not None:
                results.append(out)

    return results


def ler(prediction, target, lang='kor'):
    """
    Computes the Letter Error Rate, defined as the edit distance.
    Arguments:
        prediction (string): space-separated sentence
        target (string): space-separated sentence
        lang (string): language
    """
    # prediction, target, = prediction.replace(' ', ''), target.replace(' ', '')
    prediction = normalize_text(prediction, lang)
    target = normalize_text(target, lang)
    return Lev.distance(prediction, target), len(target)


def wer(prediction, target, lang='kor'):
    """
    Computes the Word Error Rate, defined as the edit distance between the
    two provided sentences after tokenizing to words.
    Arguments:
        prediction (string): space-separated sentence
        target (string): space-separated sentence
        lang (string): language
    """
    prediction = normalize_text(prediction, lang)
    target = normalize_text(target, lang)
    # build mapping of words to integers
    b = set(prediction.split() + target.split())
    word2char = dict(zip(b, range(len(b))))

    # map the words to a char array (Levenshtein packages only accepts
    # strings)
    prediction = [chr(word2char[w]) for w in prediction.split()]
    target = [chr(word2char[w]) for w in target.split()]

    return Lev.distance(''.join(prediction), ''.join(target)), len(target)
