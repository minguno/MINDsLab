import pandas as pd


def convert_excel_to_txt(file, output, model, wav, speaker):
    df = pd.read_excel(file)
    
    f = open(output, 'w', encoding='UTF-8')

    for i in range(len(df.values)):
        row = df.values[i]
        if row[3] != 'Y':
            line = f'{model}/{wav}/{row[0]}|{row[1]}|{speaker}\n'
            f.write(line)

    f.close()


if __name__ == '__main__':
    file = '향기작가_스크립트_1155개.xlsx'
    output = 'eargada_hyanggi_total.txt'
    model = 'eargada_hyanggi_1155'
    wav = '22k_wav'
    speaker = 'hyanggi'
    convert_excel_to_txt(file, output, model, wav, speaker)