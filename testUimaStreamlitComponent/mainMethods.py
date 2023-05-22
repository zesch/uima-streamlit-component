import numpy as np
import pandas as pd
import streamlit as st
from xml.etree import ElementTree as ET
from cassis import *
from operator import itemgetter


st.set_page_config(layout="wide")
# starter
# method for visualising both freq and pos
def freq_and_pos(casFile, typesys, pathSen, pathPos, pathFreq, pathTok):
    pick = st.radio("Do you want to highlight part of speech types or frequency bands?", ("POS", "Frequency Bands"))

    if pick == "POS":
        uima_reader(casFile, typesys, pathSen, pathPos, pathTok)
    else:
        uima_reader_freq(casFile, typesys, pathSen, pathTok, pathFreq)


# main functions
def uima_reader(casFile, typesys, pathSen, pathPos, pathTok):
    possibleTypes, finalRep, sofaString = uima_read_preprocessing(casFile, typesys, pathSen, pathPos, pathTok)
    new_multiselect(possibleTypes, finalRep, sofaString)


def uima_reader_freq(casFile, typesys, pathSen, pathTok, pathFreq):
    possibleTypes, finalRep, sofaString = uima_freq_read_preprocessing(casFile, typesys, pathSen, pathTok, pathFreq)
    new_freq_multiselect(possibleTypes, finalRep, sofaString)

#todo table version x uima

#todo farbauswahl/schema

#todo überschneidungen regeln


# preprocessing etc
def uima_freq_read_preprocessing(casFile, typesys, pathSen, pathTok, pathFreq):
    typesystem = load_typesystem(typesys)
    cas = load_cas_from_xmi(casFile, typesystem=typesystem)

    possibleTypes = []
    sofaString = ""
    tokenText = []
    tokenType = []
    tokenBegin = []
    toBeSorted = []

    oldtokenText = []
    oldtokenType = []
    oldtokenBegin = []
    oldtoBeSorted = []
    oldpossibleTypes = []
    oldsortedArray = []

    for sentence in cas.select(pathSen):  # sentence
        for token in cas.select_covered(pathFreq, sentence):  # freq
            if token.frequencyBand not in possibleTypes:
                possibleTypes.append(token.frequencyBand)
            toBeSorted.append([token.begin, token.get_covered_text(), token.frequencyBand])
            sortedArray = sorted(toBeSorted, key=itemgetter(0))

        for token in cas.select_covered(pathTok, sentence):  # pos
            # if token.frequencyBand not in possibleTypes:
            #    possibleTypes.append(token.frequencyBand)
            oldtoBeSorted.append([token.begin, token.get_covered_text()])
            oldsortedArray = sorted(oldtoBeSorted, key=itemgetter(0))

    finalSortedArray = []
    # st.write(len(sortedArray))
    # st.write(len(oldsortedArray))

    # for sortedItem in sortedArray:
    #    if [sortedItem[0], sortedItem[1]] in oldsortedArray:

    flag = 0
    for oldsortedItem in oldsortedArray:

        for sortedItem in sortedArray:
            if oldsortedItem[0] == sortedItem[0]:
                finalSortedArray.append([sortedItem[0], sortedItem[1], sortedItem[2]])
                flag = 1
                break
        if flag == 0:
            finalSortedArray.append([oldsortedItem[0], oldsortedItem[1], "noType"])
        flag = 0

    sortedFinalSortedArray = sorted(finalSortedArray, key=itemgetter(0))
    # st.write(sortedFinalSortedArray)
    for word in sortedFinalSortedArray:
        sofaString = sofaString + word[1] + " "
    # finalRep = get_array_rep(sofaString, tokenBegin, tokenType)
    return possibleTypes, sortedFinalSortedArray, sofaString


def uima_read_preprocessing(casFile, typesys, pathSen, pathPos, pathTok):
    # st.write(typesys.getvalue())
    # st.write(casFile.getvalue())
    typesystem = load_typesystem(typesys)
    cas = load_cas_from_xmi(casFile, typesystem=typesystem)
    # st.write(cas.sofas)

    possibleTypes = ["noType"]
    sofaString = ""
    tokenText = []
    tokenType = []
    tokenBegin = []
    toBeSorted = []
    allToken = []
    for sentence in cas.select(pathSen):  # sentence

        for t in cas.select_covered(pathTok, sentence):
            allToken.append([t.begin, t.get_covered_text(), "noType"])

        for token in cas.select_covered(pathPos, sentence):  # pos
            if token.coarseValue not in possibleTypes:
                possibleTypes.append(token.coarseValue)
            toBeSorted.append([token.begin, token.get_covered_text(), token.coarseValue])
            sortedArray = sorted(toBeSorted, key=itemgetter(0))

        for tokA in allToken:
            for tokB in sortedArray:
                if tokA[0] == tokB[0]:
                    tokA[2] = tokB[2]
    # st.write(sortedArray)
    # st.write(allToken)

    for sortedItem in allToken:
        tokenBegin.append(sortedItem[0])
        tokenText.append(sortedItem[1])
        tokenType.append(sortedItem[2])

        # tokenText.append(token.get_covered_text())
        # tokenType.append(token.coarseValue)
        # tokenBegin.append(token.begin)
        # st.write(token.get_covered_text())
        # sofaString = sofaString + token.get_covered_text() + " "
        # Annotation values can be accessed as properties
        # st.write('Token: begin={0}, end={1}, id={2}, pos={3}'.format(token.begin, token.end, token.id, token.pos))
    # st.write(tokenText)
    # st.write(tokenType)
    for word in tokenText:
        sofaString = sofaString + word + " "
    finalRep = get_array_rep(sofaString, tokenBegin, tokenType)
    # st.write(sortedArray)
    # st.write(sofaString)
    # st.write (tokenBegin)
    return possibleTypes, allToken, sofaString


def new_multiselect(typeArray, sortedArray, sofaString):
    # get all types
    alreadySeen = []
    for t in typeArray:
        if t not in alreadySeen:
            alreadySeen.append(t)

    alreadySeenWithoutNoType = alreadySeen.copy()
    alreadySeenWithoutNoType.remove('noType')
    currentType = st.multiselect("Select Type: ", alreadySeenWithoutNoType, alreadySeenWithoutNoType)
    # availableColors = ["coral", "chartreuse", "orchid", "gold", "cornflowerblue", "lightseagreen",
    #                   "mediumpurple", "springgreen", "indianred", "hotpink", "darkorange", "palevioletred",
    #                   "darkkhaki", "greenyellow", "palegreen"]
    # st.write(alreadySeen)
    availableColors = ["lightcoral", "pink", "palevioletred", "lightsalmon", "gold", "lightskyblue", "lavender", "plum",
                       "palegreen", "mediumaquamarine", "darkseagreen", "paleturquoise", "lightsteelblue", "rosybrown",
                       "gainsboro"]

    typeWithColor = []
    textWithColor = []
    if len(currentType) > 15 or len(currentType) == 0:
        st.write("Nothing selected! Or too much (max 15).")
        st.write(sofaString)
    else:
        for types in alreadySeen:
            typeWithColor.append([types, availableColors[alreadySeen.index(types)]])

        for elements in sortedArray:
            # if elements[2] in currentType: ####HERE!!!!!!!!!!!!
            # st.write(elements[2] + " " + elements[1])
            for colorPair in typeWithColor:
                if colorPair[0] == elements[2]:
                    textWithColor.append([elements[1], colorPair[1], elements[2], elements[0]])
                    # st.write("Geschafft!!!")
        finalString = ""
        finalTypeString = ""
        # st.write(sofaString)
        # st.write(len(sortedArray))
        # st.write(textWithColor[0])

        for types in typeWithColor:
            if types[0] in currentType and types[0] != "noType":
                finalTypeString = finalTypeString + "<span style=\"border-radius: 25px; padding-left:10px; padding-right:10px; background-color: " + \
                                  types[1] + "\">" + str(types[0]) + "</span> "
            # st.write(types)

        for triple in textWithColor:
            # st.write(triple)
            if triple[2] != "noType" and triple[2] in currentType:
                if triple[2] == "PUNCT":
                    finalString = finalString + "<span style=\"border-radius: 25px; padding-left:10px; padding-right:10px; background-color: " + \
                                  triple[1] + "\">" + triple[0] + "</span>"
                else:
                    if finalString == "":
                        finalString = finalString + "<span style=\"border-radius: 25px; padding-left:10px; padding-right:10px; background-color: " + \
                                      triple[1] + "\">" + triple[0] + "</span>"
                    else:
                        finalString = finalString + " " + "<span style=\"border-radius: 25px; padding-left:10px; padding-right:10px; background-color: " + \
                                      triple[1] + "\">" + triple[0] + "</span>"
            else:
                if finalString == "":
                    finalString = triple[0]
                else:
                    finalString = finalString + " " + triple[0]
        st.write(finalTypeString, unsafe_allow_html=True)
        st.write("---------------------")
        st.write(finalString, unsafe_allow_html=True)
        # st.write(textWithColor)

    # st.write(sortedArray)


def new_freq_multiselect(typeArray, sortedArray, sofaString):
    # st.write(sortedArray)
    # st.write(typeArray)
    # get all types
    alreadySeen = []
    for t in typeArray:
        if t not in alreadySeen:
            alreadySeen.append(t)

    currentType = st.multiselect("Select Type: ", alreadySeen, alreadySeen)

    numOfTypes = len(alreadySeen)
    b = 255
    rMax = 232
    gMax = 241
    rMin = 45
    gMin = 90

    rDist = rMax - rMin
    gDist = gMax - gMin

    rFac = round(rDist / numOfTypes)
    gFac = round(gDist / numOfTypes)

    typesWithFreqColors = []
    iterable = 0
    availableFreqColors = []
    alreadySeen.sort(reverse=True)
    alreadySeen.append("noType")
    # st.write(len(sortedArray))
    for types in alreadySeen:
        r = rMin + iterable * rFac
        g = gMin + iterable * gFac
        rgb = "rgb(" + str(r) + "," + str(g) + "," + str(b) + ")"
        # st.write(rgb)
        availableFreqColors.append(rgb)
        # typesWithFreqColors.append([freqType, rgb])
        iterable += 1
    availableFreqColors.append(["noType", "rgb(149, 255, 132)"])
    availableColors = ["coral", "chartreuse", "orchid", "gold", "cornflowerblue", "lightseagreen",
                       "mediumpurple", "springgreen", "indianred", "hotpink", "darkorange", "palevioletred",
                       "darkkhaki", "greenyellow", "palegreen"]

    typeWithColor = []
    textWithColor = []

    if len(currentType) > 15 or len(currentType) == 0:
        st.write("Nothing selected!")
        st.write(sofaString)
    else:
        for types in alreadySeen:
            typeWithColor.append([types, availableFreqColors[alreadySeen.index(types)]])

        for elements in sortedArray:
            # if elements[2] in currentType: ####HERE!!!!!!!!!!!!
            # st.write(elements[2] + " " + elements[1])
            for colorPair in typeWithColor:
                if colorPair[0] == elements[2]:
                    textWithColor.append([elements[1], colorPair[1], elements[2], elements[0]])
                    # st.write("Geschafft!!!")
        finalString = ""
        finalTypeString = ""
        # st.write(sofaString)
        # st.write(sortedArray[0])
        # st.write(textWithColor[0])

        for types in typeWithColor:
            if types[0] in currentType:
                finalTypeString = finalTypeString + "<span style=\"border-radius: 25px; padding-left:10px; padding-right:10px; background-color: " + \
                                  types[1] + "\">" + str(types[0]) + "</span> "
            # st.write(types)

        for triple in textWithColor:
            # st.write(triple)
            if triple[0] != "noType" and triple[2] in currentType:
                if triple[2] == "PUNCT":
                    finalString = finalString + "<span style=\"border-radius: 25px; padding-left:10px; padding-right:10px; background-color: " + \
                                  triple[1] + "\">" + triple[0] + "</span>"
                else:
                    if finalString == "":
                        finalString = finalString + "<span style=\"border-radius: 25px; padding-left:10px; padding-right:10px; background-color: " + \
                                      triple[1] + "\">" + triple[0] + "</span>"
                    else:
                        finalString = finalString + " " + "<span style=\"border-radius: 25px; padding-left:10px; padding-right:10px; background-color: " + \
                                      triple[1] + "\">" + triple[0] + "</span>"
            else:
                if finalString == "":
                    finalString = triple[0]
                else:
                    finalString = finalString + " " + triple[0]
        st.write(finalTypeString, unsafe_allow_html=True)
        # st.write("---------------------")
        st.write(finalString, unsafe_allow_html=True)
        # st.write(textWithColor)

    # st.write(sortedArray)


# not sorted and/or old

# create list representation
def get_array_rep(sofaString, beginArray, typeArray):
    splitSofaString = sofaString.split()
    actualIndex = 0
    wordIndexList = []
    for word in splitSofaString:
        wordlength = len(word)
        index = sofaString.index(word, actualIndex)
        wordIndexList.append([word, index])
        actualIndex = index + wordlength

    finalXmiListRep = []
    for couple in wordIndexList:
        if int(couple[1]) in beginArray:
            indexNow = beginArray.index(couple[1])
            posNow = typeArray[indexNow]
            finalXmiListRep.append([str(couple[0]), posNow])
        else:
            finalXmiListRep.append([str(couple[0]), "noType"])

    return finalXmiListRep


def multiselect(typeArray, finalRep, sofaString):
    # get all needed types
    alreadySeen = []
    for t in typeArray:
        if t not in alreadySeen:
            alreadySeen.append(t)

    currentType = st.multiselect("Select Type: ", alreadySeen, alreadySeen)
    if currentType is not None:
        # limitReached = ""
        # st.write(limitReached)
        chosenTypes = []

        for element in currentType:
            chosenTypes.append(str(element))
        # current max: 7
        # TODO: dark theme support DONE
        availableColors = []
        chosenTheme = st.radio("Choose used theme: ", ["light", "dark"])
        if chosenTheme == "light":
            availableColors = ["coral", "chartreuse", "orchid", "gold", "cornflowerblue", "lightseagreen",
                               "mediumpurple", "lightseagreen", "IndianRed", "HotPink", "DarkOrange", "LemonChiffon",
                               "DarkKhaki", "GreenYellow", "PaleGreen"]
        else:
            availableColors = ["maroon", "seagreen", "darkmagenta", "teal", "slategrey", "chocolate", "darkgoldenrod"]

        # here the html part is done
        typesWithColors = []
        stringWithTypes = ""
        stringWithColors = ""
        if len(chosenTypes) == 0:
            limitReached = "Currently only seven Types can be displayed at the same time!"
            st.write(sofaString)
        else:
            finalText = ""
            for wordTypePair in finalRep:
                if wordTypePair[1] != "noType" and wordTypePair[1] in chosenTypes:
                    typePosition = chosenTypes.index(str(wordTypePair[1]))
                    if [wordTypePair[1], availableColors[typePosition]] not in typesWithColors:
                        typesWithColors.append([wordTypePair[1], availableColors[typePosition]])
                    wordTypePair[
                        0] = "<span style=\"border-radius: 25px; padding-left:10px; padding-right:10px; background-color: " + \
                             availableColors[typePosition] + "\">" + wordTypePair[0] + "</span>"

            for typeColorPair in typesWithColors:
                stringWithTypes = stringWithTypes + " <span style=\"border-radius: 25px; padding-left:10px; padding-right:10px; background-color: " + \
                                  typeColorPair[1] + "\">" + typeColorPair[0] + "</span>"
            for finalWord in finalRep:
                stringWithColors = stringWithColors + finalWord[0] + " "
            if len(chosenTypes) == 0:
                st.write(sofaString)
            else:
                st.write(stringWithTypes, unsafe_allow_html=True)
                st.write(stringWithColors, unsafe_allow_html=True)

    else:
        st.write("Nothing was selected!")
    # for child in root:
    # if child.attrib.get('sofaString') is not None:
    # content = stringWithColors
    if sofaString is not None:
        content = stringWithColors


def freqColors(typeArray, finalRep, sofaString, freqList):
    # get all needed types
    alreadySeen = []
    for t in typeArray:
        if t not in alreadySeen:
            alreadySeen.append(t)

    currentType = st.multiselect("Select Type: ", alreadySeen)
    if currentType is not None:
        limitReached = ""
        st.write(limitReached)
        chosenTypes = []
        for element in currentType:
            chosenTypes.append(str(element))

        numOfTypes = len(freqList)
        b = 255
        rMax = 222
        gMax = 231
        rMin = 53
        gMin = 109

        rDist = rMax - rMin
        gDist = gMax - gMin

        rFac = round(rDist / numOfTypes)
        gFac = round(gDist / numOfTypes)

        typesWithFreqColors = []
        iterable = 1
        for freqType in freqList:
            r = rMin + iterable * rFac
            g = gMin + iterable * gFac
            rgb = str(r) + "," + str(g) + "," + str(b)
            st.write(rgb)
            typesWithFreqColors.append([freqType, rgb])
            iterable += 1

        # here the html part is done

        typesWithColors = []
        stringWithTypes = ""
        stringWithColors = ""
        if len(chosenTypes) == 0:
            st.write(sofaString)
        else:
            print("FinalRep:")
            print(finalRep)
            print("----------------------")
            print("TypesWithFreqColors:")
            print(typesWithFreqColors)
            print("----------------------")
            print("ChosenTypes:")
            print(chosenTypes)
            print("----------------------")
            finalText = ""
            for wordTypePair in finalRep:
                # if wordTypePair[1] != "noType" and wordTypePair[1] in chosenTypes:
                #    print("WordTypePair: " + str(wordTypePair[1]))
                #    typePosition = typesWithFreqColors.index(str(wordTypePair[1]))
                # print(typePosition)

                x = 0
                colorPick = ""
                # print(wordTypePair[1])
                for ctype in chosenTypes:
                    for typeColorPair in typesWithFreqColors:
                        if ctype == wordTypePair[1] and ctype == typeColorPair[0]:
                            print(ctype + " = " + wordTypePair[1] + " = " + typeColorPair[0])

            #        if [wordTypePair[1], availableColors[typePosition]] not in typesWithColors:
            #            typesWithColors.append([wordTypePair[1], availableColors[typePosition]])
            #        wordTypePair[
            #            0] = "<span style=\"border-radius: 25px; padding-left:10px; padding-right:10px; background-color: " + \
            #                 availableColors[typePosition] + "\">" + wordTypePair[0] + "</span>"

            for typeColorPair in typesWithFreqColors:
                stringWithTypes = stringWithTypes + " <span style=\"border-radius: 25px; padding-left:10px; padding-right:10px; background-color: rgb(" + \
                                  typeColorPair[1] + ")\">" + typeColorPair[0] + "</span>"
            for finalWord in finalRep:
                stringWithColors = stringWithColors + finalWord[0] + " "
            if len(chosenTypes) == 0:
                st.write(sofaString)
            else:
                st.write(stringWithTypes, unsafe_allow_html=True)
                st.write(stringWithColors, unsafe_allow_html=True)

    else:
        st.write("Nothing was selected!")
    if sofaString is not None:
        content = stringWithColors


#mock for CompLingDay, probably not needed anymore
def mockTagCompLing():
    x = ""
    z = ""
    y = [
        ["Peter", "NE", "coral"],
        ["buys", "Verb", "chartreuse"],
        ["two", "Num", "gold"],
        ["old", "ADJ", "orchid"],
        ["books", "NN", "cornflowerblue"],
        [".", "PUNCT", "lightseagreen"]
    ]

    for triple in y:
        x = x + " <span style=\"border-radius: 25px; padding-left:10px; padding-right:10px; background-color: " + \
            triple[2] + "\">" + triple[0] + "</span>"
        z = z + " <span style=\"border-radius: 25px; padding-left:10px; padding-right:10px; background-color: " + \
            triple[2] + "\">" + triple[1] + "</span>"
    st.write(z, unsafe_allow_html=True)
    st.write(x, unsafe_allow_html=True)


def freqencyHighlighting(file, type, freqlist):
    possibleTypes, finalRep, sofaString = uima_read_preprocessing(file, type)
    freqColors(possibleTypes, finalRep, sofaString, freqlist)


def simpleHighlightingPassages(text, highlights):
    splitText = text.split()
    actualIndex = 0
    wordIndexList = []
    for word in splitText:
        wordlength = len(word)
        index = text.index(word, actualIndex)
        wordIndexList.append([word, index])
        actualIndex = index + wordlength

    return "Hi"


def xmi_app_two(fileToProcess, typeToShow):
    myf = ET.parse(fileToProcess)
    root = myf.getroot()
    beginArray = []
    endArray = []
    typeArray = []
    sofaString = ''
    content = ''

    for child in root:
        if child.attrib.get('sofaString') is not None:
            sofaString = child.attrib.get('sofaString')
        if child.attrib.get(typeToShow) is not None:
            typeArray.append(str(child.attrib.get(typeToShow)))
            beginArray.append(int(child.attrib.get('begin')))
            endArray.append(int(child.attrib.get('end')))
    #
    # splitSofaString = sofaString.split()
    # actualIndex = 0
    # wordIndexList = []
    # for word in splitSofaString:
    #     wordlength = len(word)
    #     index = sofaString.index(word, actualIndex)
    #     wordIndexList.append([word, index])
    #     actualIndex = index + wordlength
    #
    # finalXmiListRep = []
    # for couple in wordIndexList:
    #     if int(couple[1]) in beginArray:
    #         indexNow = beginArray.index(couple[1])
    #         posNow = typeArray[indexNow]
    #         finalXmiListRep.append([str(couple[0]), posNow])
    #     else:
    #         finalXmiListRep.append([str(couple[0]), "noType"])

    finalXmiListRep = get_array_rep(sofaString, beginArray, typeArray)

    # get all needed types
    # alreadySeen = []
    # for t in typeArray:
    #     if t not in alreadySeen:
    #         alreadySeen.append(t)
    #
    # currentType = st.multiselect("Select Type: ", alreadySeen)
    # if currentType is not None:
    #     limitReached = ""
    #     st.write(limitReached)
    #     chosenTypes = []
    #
    #     for element in currentType:
    #         chosenTypes.append(str(element))
    #     # current max: 7
    #     # TODO: dark theme support DONE
    #     availableColors = []
    #     chosenTheme = st.radio("Choose used theme: ", ["light", "dark"])
    #     if chosenTheme == "light":
    #         availableColors = ["coral", "chartreuse", "orchid", "gold", "cornflowerblue", "lightseagreen",
    #                            "mediumpurple"]
    #     else:
    #         availableColors = ["maroon", "seagreen", "darkmagenta", "teal", "slategrey", "chocolate", "darkgoldenrod"]
    #
    #     # here the html part is done
    #     typesWithColors = []
    #     stringWithTypes = ""
    #     stringWithColors = ""
    #     if len(chosenTypes) > 7 or len(chosenTypes) == 0:
    #         limitReached = "Currently only seven Types can be displayed at the same time!"
    #         st.write(sofaString)
    #     else:
    #         finalText = ""
    #         for wordTypePair in finalXmiListRep:
    #             if wordTypePair[1] != "noType" and wordTypePair[1] in chosenTypes:
    #                 typePosition = chosenTypes.index(str(wordTypePair[1]))
    #                 if [wordTypePair[1], availableColors[typePosition]] not in typesWithColors:
    #                     typesWithColors.append([wordTypePair[1], availableColors[typePosition]])
    #                 wordTypePair[
    #                     0] = "<span style=\"border-radius: 25px; padding-left:10px; padding-right:10px; background-color: " + \
    #                          availableColors[typePosition] + "\">" + wordTypePair[0] + "</span>"
    #
    #         for typeColorPair in typesWithColors:
    #             stringWithTypes = stringWithTypes + " <span style=\"border-radius: 25px; padding-left:10px; padding-right:10px; background-color: " + \
    #                               typeColorPair[1] + "\">" + typeColorPair[0] + "</span>"
    #         for finalWord in finalXmiListRep:
    #             stringWithColors = stringWithColors + finalWord[0] + " "
    #         if len(chosenTypes) == 0:
    #             st.write(sofaString)
    #         else:
    #             st.write(stringWithTypes, unsafe_allow_html=True)
    #             st.write(stringWithColors, unsafe_allow_html=True)
    #
    # else:
    #     st.write("Nothing was selected!")
    # #for child in root:
    #     #if child.attrib.get('sofaString') is not None:
    #         #content = stringWithColors
    # if sofaString is not None:
    #     content = stringWithColors
    multiselect(typeArray, finalXmiListRep, sofaString)


def xmi_app_table_version(fileToProcess, typeToShow):
    st.write("Table Version!")

    myf = ET.parse(fileToProcess)
    root = myf.getroot()
    beginArray = []
    endArray = []
    typeArray = []
    sofaString = ''
    content = ''

    for child in root:
        if child.attrib.get('sofaString') is not None:
            sofaString = child.attrib.get('sofaString')
        if child.attrib.get(typeToShow) is not None:
            typeArray.append(str(child.attrib.get(typeToShow)))
            beginArray.append(int(child.attrib.get('begin')))
            endArray.append(int(child.attrib.get('end')))

    finalXmiListRep = get_array_rep(sofaString, beginArray, typeArray)

    # st.write(finalXmiListRep)

    df = pd.DataFrame(np.asarray(finalXmiListRep), columns=['token', 'type'])
    st.table(df)


def xmi_app():
    # Call through to our private component function. Arguments we pass here
    # will be sent to the frontend, where they'll be available in an "args"
    # dictionary.
    #
    # "default" is a special argument that specifies the initial return
    # value of the component before the user has interacted with it.

    # TEST START ------------------------------------------------------------------------------

    st.title('UIMA XMI APP')
    st.write("""*TODO: find better title*""")

    # File uploader
    file = st.sidebar.file_uploader("Upload xmi file")
    name = ""
    type = ""
    content = ""
    if file is not None:
        myf = ET.parse(file)
        root = myf.getroot()
        name = file.name
        type = file.type

        content = ''

        typeArray = []
        beginArray = []
        endArray = []
        idArray = []
        sofaString = ''
        levelArray = []

        # get all needed infos from the cas
        for child in root:
            # st.write(child)
            # st.write(child.attrib.get('pos'))
            # st.write(child.attrib.get('level'))
            if child.attrib.get('sofaString') is not None:
                sofaString = child.attrib.get('sofaString')
                # st.write(sofaString)
            # original
            # if child.attrib.get('pos') is not None:
            # typeArray.append(str(child.attrib.get('pos')))
            # beginArray.append(int(child.attrib.get('begin')))
            # endArray.append(int(child.attrib.get('end')))
            # idArray.append(int(child.attrib.get('id')))
            # andrea
            if child.attrib.get('level') is not None:
                levelArray.append(str(child.attrib.get('level')))
                beginArray.append(int(child.attrib.get('begin')))
                endArray.append(int(child.attrib.get('end')))
                # idArray.append(int(child.attrib.get('xmi:id')))
        alreadySeen = []
        # st.write(levelArray)
        # original
        # for pos in typeArray:
        # if pos not in alreadySeen:
        #  alreadySeen.append(pos)
        # # st.button(pos)
        # andrea
        for pos in levelArray:
            if pos not in alreadySeen:
                alreadySeen.append(pos)
                # st.button(pos)

        # currentPoss = st.radio("Select Type: ", alreadySeen)
        currentType = st.sidebar.multiselect("Select Type: ", alreadySeen)

        # st.write(currentPos)
        # st.write(posArray)
        # st.write(beginArray)

        # TODO xmi to array conversion DONE
        # here, the sofa string gets converted in a (word, index) list

        xmiArray = []
        alreadyAddedId = []
        alreadyAddedPosition = []
        splitSofaString = sofaString.split()
        # st.write(splitSofaString)

        actualIndex = 0
        wordIndexList = []
        for word in splitSofaString:
            wordlength = len(word)
            index = sofaString.index(word, actualIndex)
            # preindex = re.search(r'\b({})\b'.format(word), sofaString)
            # index = preindex.start()
            # st.write("index:")
            # st.write(index)
            wordIndexList.append([word, index])
            actualIndex = index + wordlength

        # st.write("wordindexlist:")
        # st.write(wordIndexList)

        # match the types to the occurrences in the sofastring
        finalXmiListRep = []
        for couple in wordIndexList:
            # st.write(couple[1])
            if int(couple[1]) in beginArray:
                indexNow = beginArray.index(couple[1])

                # original
                # posNow = typeArray[indexNow]
                # andrea
                posNow = levelArray[indexNow]

                finalXmiListRep.append([str(couple[0]), posNow])
            else:
                finalXmiListRep.append([str(couple[0]), "noType"])
        # st.write(finalXmiListRep)

        # TODO multiselect marking DONE
        if currentType is not None:
            limitReached = ""
            st.write(limitReached)
            chosenTypes = []
            # st.write("Hello I do work!")

            for element in currentType:
                chosenTypes.append(str(element))
            # current max: 7
            # TODO: dark theme support DONE
            availableColors = []
            chosenTheme = st.sidebar.radio("Choose used theme: ", ["light", "dark"])
            if chosenTheme == "light":
                availableColors = ["coral", "chartreuse", "orchid", "gold", "cornflowerblue", "lightseagreen",
                                   "mediumpurple"]
            else:
                availableColors = ["maroon", "seagreen", "darkmagenta", "teal", "slategrey", "chocolate",
                                   "darkgoldenrod"]

            # here the html part is done
            typesWithColors = []
            stringWithTypes = ""
            stringWithColors = ""
            if len(chosenTypes) > 7 or len(chosenTypes) == 0:
                limitReached = "Currently only seven Types can be displayed at the same time!"
                st.write(sofaString)
            else:
                finalText = ""
                for wordTypePair in finalXmiListRep:
                    if wordTypePair[1] != "noType" and wordTypePair[1] in chosenTypes:
                        typePosition = chosenTypes.index(str(wordTypePair[1]))
                        # st.write(typePosition)
                        if [wordTypePair[1], availableColors[typePosition]] not in typesWithColors:
                            typesWithColors.append([wordTypePair[1], availableColors[typePosition]])
                        wordTypePair[
                            0] = "<span style=\"border-radius: 25px; padding-left:10px; padding-right:10px; background-color: " + \
                                 availableColors[typePosition] + "\">" + wordTypePair[0] + "</span>"
                        # st.write(wordTypePair[0])

                for typeColorPair in typesWithColors:
                    stringWithTypes = stringWithTypes + " <span style=\"border-radius: 25px; padding-left:10px; padding-right:10px; background-color: " + \
                                      typeColorPair[1] + "\">" + typeColorPair[0] + "</span>"
                for finalWord in finalXmiListRep:
                    stringWithColors = stringWithColors + finalWord[0] + " "
                if len(chosenTypes) == 0:
                    st.write(sofaString)
                else:
                    st.write(stringWithTypes, unsafe_allow_html=True)
                    st.write(stringWithColors, unsafe_allow_html=True)

            # getPositionInArray = [i for i, x in enumerate(typeArray) if x in chosenTypes]
            # st.write(getPositionInArray)
            # # coloredArray = []
            # # todo multi color and each word in array representation
            # coloredString = ""
            # if len(getPositionInArray) == 1:
            #     st.write("i do work too")
            #     if beginArray[getPositionInArray[0]] != 0:
            #         beginning = (sofaString[0:int(beginArray[getPositionInArray[0]])])
            #         innerPart = sofaString[int(beginArray[getPositionInArray[0]]):int(endArray[getPositionInArray[0]])]
            #         annoInnerPart = "<span style=\"background-color: darkseagreen\">" + str(innerPart) + "<sup>" + str(
            #             currentType) + "</sup></span>"
            #         middle = (str(annoInnerPart))
            #         ending = (sofaString[int(endArray[getPositionInArray[0]]):len(sofaString)])
            #     coloredString = beginning + middle + ending
            # if len(getPositionInArray) > 1:
            #     # TODO
            #     for j in getPositionInArray:
            #         st.write("More than one occurence!")
        else:
            st.write("Nothing was selected!")

        for child in root:
            if child.attrib.get('sofaString') is not None:
                # content = child.attrib.get('sofaString')
                # content = "<b>" + content + "</b>"
                # content = coloredString
                content = stringWithColors
    # TEST END ------------------------------------------------------------------------------

    # only needed for the react part, for pure streamlit only the above code is needed
    # component_value = _component_func(name=name, type=type, content=content, default=0)
    # return component_value
