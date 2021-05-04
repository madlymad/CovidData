#!/usr/bin/env python3
from xlsxwriter.utility import xl_range_abs
import os.path
from os import path
from pandas import DataFrame
import pandas as pd
import xlsxwriter
from pathlib import Path
from shutil import copyfile


def backupFilename(filename):
    extension = "".join(Path(filename).suffixes)
    filename = filename.replace(extension, "")
    filename = filename + "_bck" + extension
    return filename


def writeData(filename, data: list, identifier: str, columns: list):
    sheetname = "data"
    exist = False
    if path.exists(filename):
        copyfile(filename, backupFilename(filename))
        exist = True
        tableData = pd.read_excel(filename, sheet_name=sheetname)

        if not set(columns).issubset(set(tableData.columns)):
            if exist:
                print("Existing excel is corrupted, creating from scratch.")
            tableData = pd.DataFrame(columns=columns)
    else:
        tableData = pd.DataFrame(columns=columns)

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    # pylint: disable=abstract-class-instantiated
    writer = pd.ExcelWriter(filename, engine='xlsxwriter',
                            date_format='dd/mm/YYYY', datetime_format='dd/mm/YYYY')
    xbook = writer.book
    xbook.strings_to_numbers = True

    for i in range(len(data)):
        unique = data[i][0]
        #unique = unique.strftime("%d/%m/%Y")
        found = tableData.index[tableData[identifier] == unique]
        if len(found) == 0:
            number_of_rows = len(tableData.index)
            tableData.loc[number_of_rows, columns] = data[i]
        else:
            tableData.loc[tableData[identifier] == unique, columns] = data[i]

    tableData[identifier] = pd.to_datetime(
        tableData[identifier], format='%d/%m/%Y', infer_datetime_format=True)  # .dt.strftime("%d/%m/%Y")
    tableData.sort_values(by=[identifier], inplace=True, ascending=False)

    tableData.to_excel(excel_writer=writer,
                       sheet_name=sheetname, index=False, encoding="UTF-8")
    worksheet = writer.sheets[sheetname]

    _fix_column_with(tableData, worksheet)

    writer.save()
    # Editing complete close the xls book
    # xbook.close()


def _fix_column_with(dataframe, worksheet):
    # loop through the columns in the dataframe to get the width of the column
    for j, col in enumerate(dataframe.columns):
        max_width = max([len(str(s))
                         for s in dataframe[col].values] + [len(str(col)) + 2])
        # define a max width to not get to wide column
        if max_width > 50:
            max_width = 50
        worksheet.set_column(j, j, max_width)
