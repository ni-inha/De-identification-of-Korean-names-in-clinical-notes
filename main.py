# -*- coding: utf-8 -*-

import os.path
import pandas as pd
import re

anonymization_pattern = {}

# 의사OOO, 의사OO, 의사 OOO, 의사 OO, 의사.OOO
anonymization_pattern["의사\.?\s?\(?\s?[가-힣]+\s?\)?"] = "의사"
anonymization_pattern["간호사\.?\s?\(?\s?[가-힣]+\s?\)?"] = "간호사"
anonymization_pattern["간호\s?조무사\.?\s?\(?\s?[가-힣]+\s?\)?"] = "간호조무사"

# prof.ooo, pro.ooo, Prof.ooo, Pro.ooo
anonymization_pattern["[Pp][Rr][Oo][Ff]\.?\s?\(?\s?[가-힣]+\s?\)?"] = "의사"
# pf.ooo, Pf.ooo
anonymization_pattern["[Pp][Ff]\.?\s?\(?\s?[가-힣]+\s?\)?"] = "의사"
# dr.ooo, Dr. ooo
anonymization_pattern["[Dd][Rr]\.?\s?\(?\s?[가-힣]+\s?\)?"] = "의사"
# R1 ooo 또는 r1 OOO, R2 ooo 또는 r2 OOO, R3 ooo 또는 r3 OOO, R4OOO
anonymization_pattern["[Rr][1-4]\.?\s?\(?\s?[가-힣]+\s?\)?"] = "의사"
# d.i.OOO, di.OOO, D.I.OOO, Di.OOO
anonymization_pattern["[Dd]\.?[Ii]\.?\s?\(?\s?[가-힣]+\s?\)?"] = "의사"
anonymization_pattern["[Pp][Ff]\.?\s?\(?\s?[가-힣]+\s?\)?"] = "의사"  # pf.(OOO)
anonymization_pattern["[Dd]1\.?\s?\(?\s?[가-힣]+\s?\)?"] = "의사"  # D1 OOO
# int OOO,  int. OOO
anonymization_pattern["[Ii][Nn][Tt]\.?\s?\(?\s?[가-힣]+\s?\)?"] = "간호사"
anonymization_pattern["[Pp][Aa]\.?\s?\(?\s?[가-힣]+\s?\)?"] = "간호사"  # PA OOO
anonymization_pattern["[Nn][Aa]\.?\s?\(?\s?[가-힣]+\s?\)?"] = "간호조무사"  # NA OOO

anonymization_pattern["[가-힣]+\s?교수님"] = "의사"  # OOO 교수님
anonymization_pattern["주치의\.?\s?\(?\s?[가-힣]+\s?\)?"] = "의사"  # 주치의 홍길동, 주치의 OO
# 당직의 OOO, 당직의사 OOO, 당직의 OO
anonymization_pattern["당직의사?\.?\s?\(?\s?[가-힣]+\s?\)?"] = "의사"
anonymization_pattern["인턴\.?\s?\(?\s?[가-힣]+\s?\)?"] = "의사"  # 인턴 OOO, 인턴 OO
anonymization_pattern["전문의\.?\s?\(?\s?[가-힣]+\s?\)?"] = "의사"
anonymization_pattern["인턴의\.?\s?\(?\s?[가-힣]+\s?\)?"] = "의사"
anonymization_pattern["담당의\.?\s?\(?\s?[가-힣]+\s?\)?"] = "의사"
# 당직 인턴의 OOO, 당직인턴의 OOO
anonymization_pattern["당직\s?인턴의\.?\s?\(?\s?[가-힣]+\s?\)?"] = "의사"

# 전담 간호사 OOO, 전담간호사OOO
anonymization_pattern["전담\s?간호사\.?\s?\(?\s?[가-힣]+\s?\)?"] = "간호사"
anonymization_pattern["보조원\.?\s?\(?\s?[가-힣]+\s?\)?"] = "간호사"  # 보조원 OOO, 보조원OOO


def data_anonymization(input_str, anonymization_pattern):
    for p, r in anonymization_pattern.items():
        input_str = re.sub(pattern=p, repl=r, string=input_str)

    return input_str


def job(FILE_NAME):
    FREETEXT_COL = "emr_NSGREC"

    if FILE_NAME[-4:] != ".csv":
        print(f"입력한 {FILE_NAME} 파일의 형식이 \".csv\"가 아닙니다!!")
        exit(1)

    pd.set_option('mode.chained_assignment',  None)
    df = pd.read_csv(FILE_NAME).fillna(0)

    print("\ncsv 파일에서 freetext가 담긴 열을 대소문자를 구분하여 입력해주세요.")
    print(f"입력하지 않고, 엔터를 누르면 \"{FREETEXT_COL}\"가 사용됩니다.")
    FREETEXT_COL_input = input()
    if FREETEXT_COL_input != "" and FREETEXT_COL_input != "\n" and FREETEXT_COL_input != " ":
        FREETEXT_COL = FREETEXT_COL_input
    if FREETEXT_COL not in df.columns:
        print(f"입력한 \"{FREETEXT_COL}\"가 파일 내에 존재하지 않습니다!")
        exit(1)
    DEIDENTIFIED_COL = "de-identified_"+FREETEXT_COL
    df.rename(columns={FREETEXT_COL: DEIDENTIFIED_COL}, inplace=True)
    print(f"\n데이터의 입력 열 : {FREETEXT_COL},\t데이터의 출력 열 : {DEIDENTIFIED_COL}")

    print(f"\n{len(df[DEIDENTIFIED_COL])}개의 데이터에 대해 익명화 작업을 시작합니다.")
    for i in range(len(df[DEIDENTIFIED_COL])):
        df[DEIDENTIFIED_COL][i] = data_anonymization(
            str(df[DEIDENTIFIED_COL][i]), anonymization_pattern)

    EXPORT_FILE_NAME = FILE_NAME[:-4]+"_de-identified"+FILE_NAME[-4:]
    df.to_csv(EXPORT_FILE_NAME, index=False, mode='w')
    print(f"익명화 작업이 완료되어 \"{EXPORT_FILE_NAME}\"으로 저장하였습니다.")


def main():
    print("익명화 할 파일 이름을 '.csv'를 포함하여 입력해주세요. (절대경로, 상대경로 가능)")
    print("file name : ", end="")
    FILE_NAME = input()

    if os.path.isfile(FILE_NAME):
        print(f"익명화에 사용되는 파일은 \"{FILE_NAME}\" 입니다.")
        job(FILE_NAME)
        exit(0)
    elif os.path.isdir(FILE_NAME):
        print(f"입력한 \"{FILE_NAME}\"은 존재하지 않습니다.")
        exit(1)
    elif os.path.exists(FILE_NAME):
        print("파일이 존재하지만, 입력한 경로로부터 파일을 읽으면서 발생한 알 수 없는 에러입니다.")
        exit(1)
    else:
        print(f"입력한 \"{FILE_NAME}\" 파일이 존재하지 않거나, 경로가 올바르지 않습니다.")
        exit(1)


if __name__ == "__main__":
    main()
