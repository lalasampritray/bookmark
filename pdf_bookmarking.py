#! python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 26 15:35:56 2020

@author: Lala Samprit Ray
"""
import os
from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger


class MyDictionary(dict):
    """

    Inheritance
    -----------
    dict : inherits from class dict

    Methods
    -----------
    add : adds an add method to My_dictionary class so that dictionaries can be added by just saying My_dictionary.add(key,value)

    """
    def add(self, key, value):
        """


        Parameters
        ----------
        key : string preferred
            accepts a string as key for dictionary
        value : int
            pagenum is stored here.

        Returns
        -------
        None.

        """
        self[key] = value


def title_page(string):
    """
    Takes in path of the .txt file and outputs a dict.

    Parameters
    ----------
    string : string
        Takes the path of the .txt file as input string.

    Returns
    -------
    res_dct : dictionary
        Outputs dictionary in the format {title:pagenum}
        The title is a string and the pagenum is integer.

    """
    file1 = open(string, "r")
    lst = file1.readlines()
    file1.close()
    lst1 = []
    lst2 = []
    res_dct = MyDictionary()
    for i, j in enumerate(lst):
        if "@" in lst[i].strip():
            line = j.strip("\n")
            title, page = line.split("@")

            lst1.append(title.strip())
            try:
                lst2.append(int(page.strip()) - 1)
            except TypeError:
                raise Exception(
"Check all values after @ perhaps there are non integer values, that is, alphabetical characters present. Remove those characters to proceed."
                )

            res_dct.add(lst1[i], lst2[i])
        else:
            raise Exception(
                "There are empty lines and/or lines without '@' character in the supplied text file. Please remove the empty lines and correct the lines by using @ to separate bookmark title and page num"
            )

    return res_dct


def filesplitter(src, dft):
    """
    splits files into individual pages

    Parameters
    ----------
    src : string
        include input file with its location like
        "c://tepelasticity.pdf"
        This is the file which has to be split/bookmarked
    dft : string
        the folder where all files are to be placed after splitting for merging.

    Returns
    -------
    None.

    """
    sourcefilepath = src
    destinationfolderpath = dft

    inputpdf = PdfFileReader(open(sourcefilepath, "rb"))

    for i in range(inputpdf.numPages):
        output = PdfFileWriter()
        output.addPage(inputpdf.getPage(i))
        with open(
            destinationfolderpath + "\\" + "page%s.pdf" % i, "wb"
        ) as output_stream:
            output.write(output_stream)


def bookmark(srcff, book):
    """
    merges all the files in the directory while adding bookmarks from the supplied book dictionary.

    Parameters
    ----------
    srcff :  string
        include input file with its location like
        "c://tepelasticity.pdf"
        This is the file which has to be split/bookmarked
    book : dict
        keys store the titles in string format.
        values store the page number in integer format.
        {key:value}
    Returns
    -------
    None.

    """

    os.chdir(srcff)
    merger = PdfFileMerger()
    visual_feedback = "creating bookmark..."
    num = 0
    key_list = list(book.keys())
    val_list = list(book.values())
    while num != len(os.listdir(".")):
        pdf = "page%s.pdf" % num
        check = (
            num in book.values()
        ) 

        if num and check:
            title = key_list[val_list.index(num)]
            merger.append(pdf, title)
            num += 1
            try:
                print(
                    visual_feedback,
                    key_list[num] + ".....@.....page number....." + str(num),
                )
            except IndexError:
                print("......@....page number...." + str(num))
        else:
            merger.append(pdf)
            num += 1
    merger.setPageMode("/UseOutlines")
    print("your bookmarked pdf will be stored at...", srcff)
    print("what do you want to call this pdf file?(do not use .pdf at end)\n")
    result = input()
    merger.write(result + ".pdf")
    merger.close()
    return result + ".pdf"


def main():
    """
This is where the main operation occurs
Change the title_page argument to your current .txt file
The format of the text file should be as shown in the example

    Raises
    ------
    Exception
        If there is any file in the destination folder this program will not work hence it stops and gives a chance to the user to clear the space before running the program again.

    Returns
    -------
    None.

    Example line in the text file
    -----------------------------
    Differential Equation of Equilibrium @ 12

    The part before @ is the title and the part after @ is the page number. You cannot use characters after the @ symbol.

    """
    source = input("Paste the source pdf file location here(include.pdf)-->")
    text_file=input("Paste the text file location here(include.txt)------>")
    book=title_page(text_file)
    destination = "C:\\Users\\User_name\\pdfJatra" # Paste path of where you want to create the final pdf file
    if len(os.listdir(destination)) > 0:
        raise Exception(
            "There are files in destination folder please move or delete files in >>"
            + destination
            + "<< this location and run the program again"
        )
    print(book)
    print("Hoping that you used only positive integers to denote page number.")
    filesplitter(source, destination)
    final_file = bookmark(destination, book)
    os.chdir(destination)
    for file in os.listdir("."):
        if file != final_file:
            os.remove(file)
    print("bookmarked pdf at" + " ---> " + destination)


if __name__ == "__main__":
    main()
