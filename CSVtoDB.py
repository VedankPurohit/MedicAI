import pandas
from json import dumps
from Modules.Database import psycoProb


def remove_non_printable(value: str) -> str:
  return ''.join(i for i in value if i.isprintable())


def format_data(data_path):
  df = pandas.read_csv(data_path, encoding='utf-8')
  dict_representation = {}

  for entry in df.iterrows():
    ele = entry[1]

    if pandas.isna(ele.topics):
      continue

    question_title = str(ele.questionTitle).replace(
        "\r", "").replace('\n', ' ').replace('"', "'")
    question_text = str(ele.questionText).replace(
        "\r", "").replace('\n', ' ').replace('"', "'")

    dict_representation[question_title] = remove_non_printable(ele.topics)
    dict_representation[question_text] = remove_non_printable(ele.topics)

  # file = open("dataset.json", 'w', encoding="utf-8")
  # file.write(dumps(dict_representation, ensure_ascii=False, indent=4))
  # file.close()
  return dict_representation


path = "20200325_counsel_chat.csv"  # change the path with actual data file path
Result = format_data(path)

print(len(Result))

keys = Result.keys()

for k in keys:
  print(k, Result[k])
  psycoProb(k,Result[k])