import pandas as pd


# --- CONSTS ---
FILE_NAME = "zeitbogen.xlsx"
OUT_FILE_NAME = "newtests.xlsx"
NAME = "Max Mustermann"
WOCHEN_ARBEITSSTUNDEN = 10
JAHR = 23
DIENSTSTELLE = "MA ..."
MONATE = [x + f" {JAHR}" for x in [
    "Januar",
    "Februar",
    "März",
    "April",
    "Mai",
    "Juni",
    "Juli",
    "August",
    "September",
    "Oktober",
    "November",
    "Dezember" ]
]

dfs = pd.read_excel(FILE_NAME, sheet_name=None, header=None)

jan = dfs[MONATE[0]]

jan[0][4] = 69

dfs[MONATE[0]] = jan

print(dfs)

odfs = pd.DataFrame(dfs[MONATE[0]], index=range(13))

with pd.ExcelWriter(OUT_FILE_NAME) as writer:
    odfs.to_excel(writer)
