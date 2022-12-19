import os
import time

from functools import partial
from glob import glob
from utils import parallel_run, ler, wer

def test(txt, **kwargv):
    lang = kwargv["lang"]
    encoding = kwargv["encoding"]
    start_time = time.perf_counter()
    result_file = txt.replace(".txt", ".result")
    fp = open(result_file, encoding=encoding)

    lines = []
    for line in fp:
        lines.append(line.replace('\n', ''))

    prediction = ' '.join(lines)
    use_txt = True

    if use_txt:
        txt_path = '{}.txt'.format(os.path.splitext(txt)[0])
        with open(txt_path, 'r', encoding=encoding) as rf:
            target = rf.read()

        letter_err_cnt, letter_target_cnt = ler(prediction, target, lang)
        word_err_cnt, word_target_cnt = wer(prediction, target, lang)
        if letter_target_cnt == 0:
            letter_target_cnt = 1
        if word_target_cnt == 0:
            word_target_cnt = 1

        print('ler: {:.2f}%, wer: {:.2f}%, file: {}'.format(
            letter_err_cnt / letter_target_cnt * 100,
            word_err_cnt / word_target_cnt * 100,
            txt)
        )
        proc_time = time.perf_counter() - start_time
        return letter_err_cnt, letter_target_cnt, word_err_cnt, word_target_cnt, proc_time
    else:
        print('{}: {}'.format(prediction, txt))

def batch_eval(txt_list, **kargv):
    n_cpu = 4
    test_fn = partial(test, **kargv)
    results = parallel_run(test_fn, txt_list,
                           desc="evaluation", n_cpu=n_cpu)
    if len(results) > 0:
        letter_err_tot_cnt = 0
        letter_target_tot_cnt = 0
        word_err_tot_cnt = 0
        word_target_tot_cnt = 0
        proc_time_tot = 0
        for letter_err_cnt, letter_target_cnt, word_err_cnt, word_target_cnt, proc_time in results:
            letter_err_tot_cnt += letter_err_cnt
            letter_target_tot_cnt += letter_target_cnt
            word_err_tot_cnt += word_err_cnt
            word_target_tot_cnt += word_target_cnt
            proc_time_tot += proc_time
        letter_err_rate = letter_err_tot_cnt / letter_target_tot_cnt
        word_err_rate = word_err_tot_cnt / word_target_tot_cnt
        proc_time_avg = proc_time_tot / len(results)
        print('letter error rate: {:.2f}%, word error rate: {:.2f}%, processing time average / n_cpu: {}s'.format(
            letter_err_rate * 100,
            word_err_rate * 100,
            proc_time_avg / n_cpu
        ))

def eval_results(folder, lang, encoding):
    print("Evaluation Data Path:", folder)
    
    if not os.path.exists(folder):
        os.mkdir(folder + '/')
    
    flist = os.listdir(folder)
    txt_list = []
    for f in flist:
        if f.find(".txt") != -1:
            txt_list.append(folder + '/' + f)
    for file_name in txt_list:
        print("\t%s" % (file_name.replace('.txt', ".result")))
    batch_eval(txt_list, lang=lang, encoding=encoding)

if __name__ == '__main__':
    folder = "data"
    lang = "kor"  # "eng"
    encodings = "utf8"  # or "euc-kr"
    eval_results(folder, lang, encodings)
