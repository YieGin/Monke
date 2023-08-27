# liblBS_orig.py

from tkinter import filedialog
from tkinter.ttk import Combobox
from tkinter import Toplevel
from tkinter import Label
from datetime import datetime
from datetime import date
import tkinter as tk
import ctypes
import smtplib, ssl
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from genericpath import exists
import os
from difflib import Differ
from csv import reader
from pdf2jpg import pdf2jpg
from docx.text.paragraph import Paragraph
from docx.oxml.xmlchemy import OxmlElement
from docx.shared import Pt
from typing import Iterable, Any, Tuple
import pandas as pd
import csv
from lxml import etree as et


def date_yyyymmdd_hhmmss():
    now = datetime.now()
    # jaar = now.strftime("%Y")
    # maand = now.strftime("%m")
    # dag = now.strftime("%d")
    # tijd = now.strftime("%H:%M:%S")
    return now.strftime("%Y%m%d_%H%M%S")
    """"
        Directive	Meaning	Example
        %a  Abbreviated weekday name.	                                Sun, Mon, ...
        %A	Full weekday name.	                                        Sunday, Monday, ...
        %w	Weekday as a decimal number.	                            0, 1, ..., 6
        %d	Day of the month as a zero-padded decimal.	                01, 02, ..., 31
        %-d	Day of the month as a decimal number.	                    1, 2, ..., 30
        %b	Abbreviated month name.	                                    Jan, Feb, ..., Dec
        %B	Full month name.	                                        January, February, ...
        %m	Month as a zero-padded decimal number.	                    01, 02, ..., 12
        %-m	Month as a decimal number.	                                1, 2, ..., 12
        %y	Year without century as a zero-padded decimal number.	    00, 01, ..., 99
        %-y	Year without century as a decimal number.	                0, 1, ..., 99
        %Y	Year with century as a decimal number.	                    2013, 2019 etc.
        %H	Hour (24-hour clock) as a zero-padded decimal number.	    00, 01, ..., 23
        %-H	Hour (24-hour clock) as a decimal number.	                0, 1, ..., 23
        %I	Hour (12-hour clock) as a zero-padded decimal number.	    01, 02, ..., 12
        %-I	Hour (12-hour clock) as a decimal number.	                1, 2, ... 12
        %p	Locale’s AM or PM.	                                        AM, PM
        %M	Minute as a zero-padded decimal number.	                    00, 01, ..., 59
        %-M	Minute as a decimal number.	                                0, 1, ..., 59
        %S	Second as a zero-padded decimal number.	                    00, 01, ..., 59
        %-S	Second as a decimal number.	                                0, 1, ..., 59
        %f	Microsecond as a decimal number, zero-padded on the left.	000000 - 999999
        %z	UTC offset in the form                                      +HHMM or -HHMM.	 
        %Z	Time zone name.	 
        %j	Day of the year as a zero-padded decimal number.	        001, 002, ..., 366
        %-j	Day of the year as a decimal number.	                    1, 2, ..., 366
        %U	Week number of the year 
            (Sunday as the first day of the week). 
            All days in a new year preceding the first Sunday 
            are considered to be in week 0.	                            00, 01, ..., 53
        %W	Week number of the year 
            (Monday as the first day of the week). 
            All days in a new year preceding the first Monday 
            are considered to be in week 0.	                            00, 01, ..., 53
        %c	Locale appropriate date and time representation.	        Mon Sep 30 07:06:05 2013
        %x	Locale appropriate date representation.	                    09/30/13
        %X	Locale appropriate time representation.	                    07:06:05
        %%	A literal '%' character.	                                %
    """


def current_date():
    return date.today()


def current_year():
    return current_date().year


def current_month():
    return current_date().month


def current_day():
    return current_date().day


def string_to_date(inputDate):  # string in yyyy-mm-dd of yyyy/mm/dd
    dateList = inputDate.split(" ")
    inputDate = dateList[0]
    inputDate = inputDate.replace("-", "/")
    dateList = inputDate.split("/")
    try:
        outputDate = datetime(int(dateList[0]), int(dateList[1]), int(dateList[2]))
    except:
        outputDate = None
    return outputDate


def monthnumber(month):
    monthNo = 0
    months = {
        "januari": 1,
        "februari": 2,
        "maart": 3,
        "april": 4,
        "mei": 5,
        "juni": 6,
        "juli": 7,
        "augustus": 8,
        "september": 9,
        "oktober": 10,
        "november": 11,
        "december": 12,
    }
    month = month.lower()
    if month in months:
        monthNo = months[month]
    return monthNo


def display_message(title, text, style=0):
    """
    :param title:   Titel van de messagebox
    :param text:    Tekst om weer te geven in messageBox
    :param style:   Optioneel, heeft meerdere mogelijkheden:
                    0 - Default, alleen button OK
                    1 - Buttons OK - Annuleren
                    2 - Buttons Afbreken - Opnieuw - Negeren
                    3 - Buttons Ja - Nee - Annuleren
                    4 - Buttons Ja - Nee
                    5 - Buttons Opnieuw - Annuleren
                    6 - Buttons Annuleren - Opnieuw - Doorgaan
    :return:        int - afhankelijk van geklikte button:
                    1 = OK
                    2 = Annuleren
                    3 = Afbreken
                    4 = Opnieuw
                    5 = Negeren
                    6 = Ja
                    7 = Nee
                    10 = Opnieuw  (alleen bij style 6)
                    11 = Doorgaan (alleen bij style 6)
    """
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)


class simple_choicebox:
    def __init__(self, title, text, choices):
        self.t = Toplevel()
        self.t.title(title if title else "")
        self.selection = None
        Label(self.t, text=text if text else "").grid(row=0, column=0)
        self.c = Combobox(self.t, value=choices if choices else [], state="readonly")
        self.c.grid(row=0, column=1)
        self.c.bind("<<ComboboxSelected>>", self.combobox_select)

    def combobox_select(self):
        self.selection = self.c.get()
        self.t.destroy()


def select_file(fileTypes, initialDir, Title, Multiple=False):
    if Multiple:
        filename = filedialog.askopenfilenames(
            title=Title, initialdir=initialDir, filetypes=fileTypes
        )
    else:
        filename = filedialog.askopenfilename(
            title=Title, initialdir=initialDir, filetypes=fileTypes
        )
    return filename


def saveas_filename(fileTypes, initialDir, Title, initialFile=""):
    filename = filedialog.asksaveasfilename(
        title=Title,
        initialdir=initialDir,
        filetypes=fileTypes,
        initialfile=initialFile,
        defaultextension=fileTypes,
        confirmoverwrite=True,
    )
    return filename


def ask_directory(titel, mustExist=False):
    directory = filedialog.askdirectory(title=titel, mustexist=mustExist)
    return directory


def create_popup(root, title, height, width):
    # Create a Toplevel window
    popup = Toplevel(root)
    size = "{}x{}".format(height, width)
    popup.geometry(size)
    # popup.resizable(False, False)
    popup.iconbitmap("img/SIVI_Blokken.ico")
    popup.title(title)
    return popup


# Show the window
def show_window(window):
    window.deiconify()


# Hide the window
def hide_window(window):
    window.withdraw()


def clear_window(window):
    if window is not None:
        for widgets in window.winfo_children():
            widgets.destroy()
        window.update()
    return


# Define a function to close the popup window
def close_window(window):
    try:
        window.destroy()
    except:
        pass


def send_mail(receiverEmail, subject, bodyText="", bodyHtml="", document=""):
    port = 587
    smtpServer = "smtp.gmail.com"
    senderEmail = "sivimailhandler@gmail.com"  # password voor de site: Pyth101@
    password = "ofefdiwbzqhtgrdt"  # voor gebruik vanuit Python

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = senderEmail
    message["To"] = receiverEmail

    # Turn these into plain/html MIMEText objects
    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    if bodyText != "":
        partText = MIMEText(bodyText, "plain")
        message.attach(partText)
    if bodyHtml != "":
        partHtml = MIMEText(bodyHtml, "html")
        message.attach(partHtml)

    if document != "" and exists(document):
        # Open document in binary mode
        with open(document, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            partAttach = MIMEBase("application", "octet-stream")
            partAttach.set_payload(attachment.read())

        if partAttach is not None:
            # Encode file in ASCII characters to send by email
            encoders.encode_base64(partAttach)

            # Add header as key/value pair to attachment part
            documentName = document.replace(os.path.dirname(document), "")
            partAttach.add_header(
                "Content-Disposition", f"attachment; filename= {documentName}"
            )

            # Add attachment to message and convert message to string
            message.attach(partAttach)

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP(smtpServer, port) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(senderEmail, password)
            server.sendmail(senderEmail, receiverEmail, message.as_string())
            mailSent = True
    except:
        mailSent = False

    return mailSent


def compare_files(leftFile, rightFile):
    with open(leftFile, encoding="utf-8") as f:
        left_lines = f.readlines()
    with open(rightFile, encoding="utf-8") as f:
        right_lines = f.readlines()
    d = Differ()
    difference = list(d.compare(left_lines, right_lines))

    return difference


def convert_excel_to_xml(fileName, sheetName, rootName, header, outputFile):
    try:
        xmlObject = ""
        headerNames = header.split(",")
        columnHeader = []

        xlsData = pd.read_excel(fileName, sheetName)
        root = et.Element("root")

        for row in xlsData.iterrows():
            root_tags = et.SubElement(root, rootName)
            for item in range(len(headerNames)):
                columnHeader.append(et.SubElement(root_tags, headerNames[item]))
                columnHeader[item].text = str(row[1][headerNames[item]])

        # output the data to an xml file
        xmlObject = et.ElementTree(root)
        et.indent(xmlObject, space="\t", level=0)  # format XML
        xmlObject.write(outputFile, encoding="utf-8")
        success = True
    except:
        success = False

    return success


def convert_csv_to_xml(inputCsv, outputXml):
    with open(inputCsv, "r") as inFile:
        with open(outputXml, "w"):
            csv_reader = reader(inFile)
            header = next(csv_reader)
            if header != None:
                for row in csv_reader:
                    print(row)


def csv_to_list(inputCsv, delimiter):
    content = []
    width = []
    filled = []
    maxCols = 1
    currentRow = 0
    maxRows = get_max_rows(inputCsv)

    with open(inputCsv, mode="r", encoding="utf-8") as f:
        csvReader = reader(f, delimiter=delimiter)
        currentRow = 0
        for row in csvReader:
            if currentRow == 0:
                maxCols = len(row)
                for col in range(maxCols):
                    header = row[col]
                    width.append(len(header) + 3)
                    header = header.lower()
                    exec("content.append(['' for i in range(0, %d)])" % (maxRows + 10))
            for col in range(maxCols):
                if (
                    currentRow != 0
                    and row[col] is not None
                    and row[col] != ""
                    and not col in filled
                ):
                    filled.append(col)
                content[col][currentRow] = row[col]
                width[col] = max(width[col], len(row[col]) + 3)
            currentRow += 1
        f.close()

    return (
        content,
        maxRows,
        maxCols,
        width,
        filled,
    )


def read_csv(csvFile):
    content = None
    if csvFile != "" and exists(csvFile):
        with open(csvFile, mode="r", encoding="utf-8") as f:
            csvReader = csv.reader(f, delimiter="\t")
            content = []
            for row in csvReader:
                content.append(row)
            f.close()

    return content


def get_max_rows(csvFile):
    with open(csvFile, mode="r") as content:
        csvReader = csv.reader(content)
        maxRows = sum(1 for row in csvReader)
        content.close()
    return maxRows


def cell_value(ws, row, col, form="", default=""):
    value = ws[row - 1][col - 1]
    if value is not None:
        value = str(value)
        value = value.replace("\xc2", "")
        check = value.split(".")
        if len(check) == 2:
            if check[1] == "0":
                value = check[0]
        if "unnamed" in value.lower():
            value = ""
        value = value.strip()
        if form == "upper":
            value = value.upper()
        if form == "lower":
            value = value.lower()
        if form == "capitalize":
            value = value.capitalize()
    else:
        value = default

    return value


def excel_to_csv(excelFile, sheetname="sheetname"):
    csvFile = excelFile + "." + sheetname + ".csv"

    # Excel tabbladen naar csv
    try:
        fileContent = pd.read_excel(excelFile, sheet_name=sheetname)
        fileContent.to_csv(csvFile, index=None, header=True, sep="\t", encoding="utf-8")
    except:
        display_message(
            "*** Fout ***", 'Tabblad "{}" kan niet gevonden worden!'.format(sheetname)
        )
        csvFile = ""

    return csvFile


def get_max_rows(csvFile):
    maxRows = 0
    try:
        with open(csvFile, mode="r") as content:
            csvReader = csv.reader(content)
            maxRows = sum(1 for row in csvReader)
            content.close()
    except:
        pass
    return maxRows


def convert_backslash(widgetObject):
    item = widgetObject.get()
    item = item.replace("\\", "/")
    return item


def delete_paragraph(paragraph):
    p = paragraph._element
    p.getparent().remove(p)
    paragraph._p = paragraph._element = None


def insert_paragraph_after(paragraph, style=None):
    """Insert a new paragraph after the given paragraph."""
    new_p = OxmlElement("w:p")
    paragraph._p.addnext(new_p)
    new_par = Paragraph(new_p, paragraph._parent)
    if style is not None:
        new_par.style = style
    return new_par


def insert_run_after(paragraph, settings):
    # volgorde gelijk aan parSettings en runSettings
    text = 0
    font = 1
    size = 2
    run = paragraph.add_run(settings[text])
    run.font.name = settings[font]
    run.font.size = Pt(settings[size])

    return paragraph


def docx_replace(document, searchArg, replaceArg):
    # document style, font, size, etc.
    docStyles = document.styles
    docStyle = document.styles["Normal"]
    docFont = docStyle.font
    docFontName = docFont.name
    docFontSize = 12.0
    if docFont.size is not None:
        docFontSize = docFont.size.pt

    for paragraph in document.paragraphs:
        # paragraph style, font, size, etc.
        parStyle = paragraph.style
        parStyleName = parStyle.name
        parFont = parStyle.font
        parFontName = parFont.name
        parFontSize = parFont.size.pt
        if parFontName is None:
            parFontName = docFontName
        if parFontSize is None:
            parFontSize = docFontSize

        searchText = paragraph.text
        replacedText = searchText.replace(searchArg, replaceArg)
        parSettings = [
            replacedText,
            parFontName,
            parFontSize,
        ]  # zelfde opbouw als runSettings

        if replacedText != searchText:  # search is gevonden en vervangen
            # nu de juiste instellingen van de runs (gedeelte van de paragraph) zoeken en bewaren
            text = 0
            font = 1
            size = 2
            runSettings = []
            runNumber = 0
            charNumber = 0
            textStart = searchText.find(searchArg)
            textEnd = textStart + len(searchArg)

            for run in paragraph.runs:
                runNumber += 1
                runFont = run.font
                runFontName = runFont.name
                if runFont.size is None:
                    runFontSize = None
                else:
                    runFontSize = runFont.size.pt
                runText = run.text
                settings = [
                    runText,
                    runFontName,
                    runFontSize,
                ]  # zelfde opbouw als parSettings
                runSettings.append(settings)

            newParagraph = insert_paragraph_after(paragraph, docStyles[parStyleName])
            # font en size overrule van de run
            runNumber = 0
            charNumber = 0
            for run in paragraph.runs:
                runNumber += 1
                runText = run.text
                runSetting = run_setting(parSettings, runSettings[runNumber - 1])
                if charNumber == textStart:  # precies op het replace gebied
                    runSetting[text] = replaceArg
                    newParagraph = insert_run_after(newParagraph, runSetting)
                    textPosition = charNumber + len(searchArg) + 1
                    if textPosition < len(runText):
                        runSetting[text] = runText[textPosition:]
                        newParagraph = insert_run_after(newParagraph, runSetting)
                else:
                    if (
                        charNumber < textStart
                        and charNumber + len(runText) <= textStart
                    ) or charNumber >= textEnd:  # buiten het replace gebied
                        newParagraph = insert_run_after(newParagraph, runSetting)
                    else:
                        if (
                            charNumber < textStart
                            and charNumber + len(runText) > textStart
                        ):  # run begint voor en gaat over het replace gebied heen
                            endChar = textStart - charNumber + 1
                            if endChar > 0:
                                runSetting[text] = runText[:endChar]
                                newParagraph = insert_run_after(
                                    newParagraph, runSetting
                                )
                                runSetting[text] = replaceArg
                                newParagraph = insert_run_after(
                                    newParagraph, runSetting
                                )
                                if textEnd < len(runText):
                                    runSetting[text] = runText[textEnd:]
                                    newParagraph = insert_run_after(
                                        newParagraph, runSetting
                                    )
                        else:  # run is in het replace gebied
                            endChar = len(runText) + charNumber + 1
                            if endChar > textEnd:
                                runSetting[text] = runText[textEnd + 1 :]
                                newParagraph = insert_run_after(
                                    newParagraph, runSetting
                                )

                charNumber += len(runText)  # einde run, naar de volgende

            # oude paragrpah verwijderen
            delete_paragraph(paragraph)

    return document


def run_setting(parSettings, runSetting):
    for s in range(1, len(runSetting)):  # niet de text (1e) overnemen van de paragraph
        if runSetting[s] is None:
            runSetting[s] = parSettings[s]  # overnemen van de paragraph
    return runSetting


def add_diff(action, line, nextLine, exceptions, nw, ch, dl, old, unsort):
    lineDiff = line[2:]
    if no_exception(exceptions, lineDiff):
        unsort.append([action, lineDiff])
        match action:
            case "new":
                nw.append(lineDiff)
            case "change":
                if nextLine is not None:
                    ch.append(nextLine[2:])
                    old.append(lineDiff)
            case "delete":
                dl.append(lineDiff)

    return nw, ch, dl, old, unsort


def get_difference(left, right, exceptions=None):
    nw = []
    ch = []
    dl = []
    old = []
    unsort = []
    difference = compare_files(left, right)
    maxLines = len(difference)
    nextLineNo = 0
    for lineNo in range(maxLines):
        if lineNo > nextLineNo:
            nextLineNo = lineNo
            nextLine = None
            line = difference[lineNo]
            line = line.strip("\n")
            action = line[:1]
            if action == "-":
                if lineNo + 1 < maxLines:
                    nextLine = difference[lineNo + 1]
                    nextLine = nextLine.strip("\n")
                    nextAction = nextLine[:1]
                    if nextAction == " ":  # dit is een delete
                        nw, ch, dl, old, unsort = add_diff(
                            "delete",
                            line,
                            nextLine,
                            exceptions,
                            nw,
                            ch,
                            dl,
                            old,
                            unsort,
                        )
                    else:
                        if nextAction == "?":  # dit is een change
                            nextLineNo += 2
                            nextLine = difference[lineNo + 2]
                            nextLine = nextLine.strip("\n")
                            nw, ch, dl, old, unsort = add_diff(
                                "change",
                                line,
                                nextLine,
                                exceptions,
                                nw,
                                ch,
                                dl,
                                old,
                                unsort,
                            )
                            if lineNo + 3 <= maxLines:
                                nextAction = difference[lineNo + 3][:1]
                                if nextAction == "?":  # deze hoort nog bij de change
                                    nextLineNo += 1
                        else:
                            if (
                                nextAction == "-"
                            ):  # die behandelen we in de volgende iteratie, maar deze is een delete
                                nw, ch, dl, old, unsort = add_diff(
                                    "delete",
                                    line,
                                    nextLine,
                                    exceptions,
                                    nw,
                                    ch,
                                    dl,
                                    old,
                                    unsort,
                                )
                            else:  # volgende is dus een +
                                if lineNo + 2 < maxLines:
                                    nextAction = difference[lineNo + 2][:1]
                                    if nextAction == "?":  # dit is dus een change
                                        nextLineNo += 2
                                        nw, ch, dl, old, unsort = add_diff(
                                            "change",
                                            line,
                                            nextLine,
                                            exceptions,
                                            nw,
                                            ch,
                                            dl,
                                            old,
                                            unsort,
                                        )
                                    else:  # dit is een delete en de volgende een new maar die behandelen we in de volgende iteratie
                                        check1 = line[2:].split(",")
                                        check2 = nextLine[2:].split(",")
                                        if (
                                            check1[0] == check2[0] and len(check2) == 2
                                        ):  # in dit geval is de puo er af
                                            nextLineNo += 1
                                            nw, ch, dl, old, unsort = add_diff(
                                                "change",
                                                line,
                                                nextLine,
                                                exceptions,
                                                nw,
                                                ch,
                                                dl,
                                                old,
                                                unsort,
                                            )
                                        else:
                                            nw, ch, dl, old, unsort = add_diff(
                                                "delete",
                                                line,
                                                nextLine,
                                                exceptions,
                                                nw,
                                                ch,
                                                dl,
                                                old,
                                                unsort,
                                            )  # totale puv is verwijderd
                                else:  # dit is een delete en de volgende een new maar die behandelen we in de volgende iteratie
                                    nw, ch, dl, old, unsort = add_diff(
                                        "delete",
                                        line,
                                        nextLine,
                                        exceptions,
                                        nw,
                                        ch,
                                        dl,
                                        old,
                                        unsort,
                                    )  # totale puv is verwijderd
                else:  # laatste regel dus automatisch een delete
                    nw, ch, dl, old, unsort = add_diff(
                        "delete", line, nextLine, exceptions, nw, ch, dl, old, unsort
                    )
            else:
                if action == "+":
                    nw, ch, dl, old, unsort = add_diff(
                        "new", line, nextLine, exceptions, nw, ch, dl, old, unsort
                    )
    return nw, ch, dl, old, unsort


def no_exception(exceptions, line):
    if exceptions is not None:
        for exception in exceptions:
            if exception in line:
                return False
    return True


def loop_with_first_last(it: Iterable[Any]) -> Iterable[Tuple[bool, Any]]:
    # aanroep: for first, last, items in ibs.loop_with_first_last(items):
    first = True
    last = False
    iterable = iter(it)
    returnVar = next(iterable)
    for value in iterable:
        yield first, last, returnVar
        first = False
        returnVar = value
    last = True
    yield first, last, returnVar


def convert_pdf2jpg(fileName, outputDir, pages="ALL"):
    result = pdf2jpg.convert_pdf2jpg(
        fileName, outputDir, pages=pages
    )  # nog niet uitgetest!
    return result


def create_root():
    root = tk.Tk()

    # load image file
    logo = tk.PhotoImage(file="img/Logo_SIVI.png")

    # Adjust size
    root.geometry("680x334")
    root.iconbitmap("img/SIVI_Blokken.ico")
    root.title("Interne Beheer Services")

    # Show image using label
    displayLogo = tk.Label(root, image=logo)
    displayLogo.place(x=0, y=0)

    return root
