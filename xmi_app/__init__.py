import os
import re

import streamlit.components.v1 as components
import streamlit as st
from xml.etree import ElementTree as ET

# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
# (This is, of course, optional - there are innumerable ways to manage your
# release process.)
_RELEASE = False

# Declare a Streamlit component. `declare_component` returns a function
# that is used to create instances of the component. We're naming this
# function "_component_func", with an underscore prefix, because we don't want
# to expose it directly to users. Instead, we will create a custom wrapper
# function, below, that will serve as our component's public API.

# It's worth noting that this call to `declare_component` is the
# *only thing* you need to do to create the binding between Streamlit and
# your component frontend. Everything else we do in this file is simply a
# best practice.

if not _RELEASE:
    _component_func = components.declare_component(
        # We give the component a simple, descriptive name ("xmi_app"
        # does not fit this bill, so please choose something better for your
        # own component :)
        "xmi_app",
        # Pass `url` here to tell Streamlit that the component will be served
        # by the local dev server that you run via `npm run start`.
        # (This is useful while your component is in development.)
        url="http://localhost:3001",
    )
else:
    # When we're distributing a production version of the component, we'll
    # replace the `url` param with `path`, and point it to to the component's
    # build directory:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("xmi_app", path=build_dir)


# Create a wrapper function for the component. This is an optional
# best practice - we could simply expose the component function returned by
# `declare_component` and call it done. The wrapper allows us to customize
# our component's API: we can pre-process its input args, post-process its
# output value, and add a docstring for users.
def xmi_app():
    """Create a new instance of "xmi_app".

    Parameters
    ----------
    name: str
        The name of the thing we're saying hello to. The component will display
        the text "Hello, {name}!"
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.

    Returns
    -------
    int
        The number of times the component's "Click Me" button has been clicked.
        (This is the value passed to `Streamlit.setComponentValue` on the
        frontend.)

    """
    # Call through to our private component function. Arguments we pass here
    # will be sent to the frontend, where they'll be available in an "args"
    # dictionary.
    #
    # "default" is a special argument that specifies the initial return
    # value of the component before the user has interacted with it.

    #TEST START ------------------------------------------------------------------------------

    st.title('UIMA XMI APP')
    st.write("""*TODO: find better title*""")

    file = st.sidebar.file_uploader("Upload xmi file")
    # plaintext = "here will be text"
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

        # radio buttons
        for child in root:
            #st.write(child)
            #st.write(child.attrib.get('pos'))
            #st.write(child.attrib.get('level'))
            if child.attrib.get('sofaString') is not None:
                sofaString = child.attrib.get('sofaString')
                #st.write(sofaString)
            #original
            #if child.attrib.get('pos') is not None:
               # typeArray.append(str(child.attrib.get('pos')))
               # beginArray.append(int(child.attrib.get('begin')))
               # endArray.append(int(child.attrib.get('end')))
                #idArray.append(int(child.attrib.get('id')))
            #andrea
            if child.attrib.get('level') is not None:
                levelArray.append(str(child.attrib.get('level')))
                beginArray.append(int(child.attrib.get('begin')))
                endArray.append(int(child.attrib.get('end')))
                #idArray.append(int(child.attrib.get('xmi:id')))
        alreadySeen = []
        #st.write(levelArray)
        #original
        #for pos in typeArray:
           # if pos not in alreadySeen:
              #  alreadySeen.append(pos)
               # # st.button(pos)
        #andrea
        for pos in levelArray:
            if pos not in alreadySeen:
                alreadySeen.append(pos)
                # st.button(pos)



        #currentPoss = st.radio("Select Type: ", alreadySeen)
        currentType = st.sidebar.multiselect("Select Type: ", alreadySeen)

        #st.write("Radio " + currentPoss)
        #st.write(currentPos)
        #st.write(posArray)
        #st.write(beginArray)

        # TODO xmi to array conversion DONE

        xmiArray = []
        alreadyAddedId = []
        alreadyAddedPosition = []
        splitSofaString = sofaString.split()
        #st.write(splitSofaString)

        actualIndex = 0
        wordIndexList = []
        for word in splitSofaString:
            wordlength = len(word)
            index = sofaString.index(word, actualIndex)
            #preindex = re.search(r'\b({})\b'.format(word), sofaString)
            #index = preindex.start()
            #st.write("index:")
            #st.write(index)
            wordIndexList.append([word, index])
            actualIndex = index + wordlength

        #st.write("wordindexlist:")
        #st.write(wordIndexList)

        finalXmiListRep = []
        for couple in wordIndexList:
            #st.write(couple[1])
            if int(couple[1]) in beginArray:
                indexNow = beginArray.index(couple[1])

                #original
                #posNow = typeArray[indexNow]
                #andrea
                posNow = levelArray[indexNow]

                finalXmiListRep.append([str(couple[0]), posNow])
            else:
                finalXmiListRep.append([str(couple[0]), "noType"])
        #st.write(finalXmiListRep)


        # TODO multiselect marking DONE
        if currentType is not None:
            limitReached = ""
            st.write(limitReached)
            chosenTypes = []
            #st.write("Hello I do work!")

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
                availableColors = ["maroon", "seagreen", "darkmagenta", "teal", "slategrey", "chocolate", "darkgoldenrod"]

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
                        #st.write(typePosition)
                        if [wordTypePair[1], availableColors[typePosition]] not in typesWithColors:
                            typesWithColors.append([wordTypePair[1], availableColors[typePosition]])
                        wordTypePair[0] = "<span style=\"border-radius: 25px; padding-left:10px; padding-right:10px; background-color: " + availableColors[typePosition] + "\">" + wordTypePair[0] + "</span>"
                        #st.write(wordTypePair[0])

                for typeColorPair in typesWithColors:
                    stringWithTypes = stringWithTypes + " <span style=\"border-radius: 25px; padding-left:10px; padding-right:10px; background-color: " + typeColorPair[1] + "\">" + typeColorPair[0] + "</span>"
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
    #TEST END ------------------------------------------------------------------------------

    component_value = _component_func(name=name, type=type, content=content, default=0)

    return component_value



# Add some test code to play with the component while it's in development.
# During development, we can run this just as we would any other Streamlit
# app: `$ streamlit run xmi_app/__init__.py`
if not _RELEASE:
    # import streamlit as st
    # from xml.dom import minidom
    # from xml.etree import ElementTree as ET
    #
    # st.title('UIMA XMI APP')
    #
    # file = st.file_uploader("Upload xmi file")
    # # plaintext = "here will be text"
    # if file is not None:
    #     myf = ET.parse(file)
    #     root = myf.getroot()
    #     name = file.name
    #     type = file.type
    #
    #     content = ''
    #
    #     posArray = []
    #     beginArray = []
    #     endArray = []
    #     sofaString = ''
    #
    #     # radio buttons
    #     for child in root:
    #         #    st.write(child)
    #         # st.write(child.attrib.get('pos'))
    #         if child.attrib.get('sofaString') is not None:
    #             sofaString = child.attrib.get('sofaString')
    #         if child.attrib.get('pos') is not None:
    #             posArray.append(child.attrib.get('pos'))
    #             beginArray.append(child.attrib.get('begin'))
    #             endArray.append(child.attrib.get('end'))
    #     alreadySeen = []
    #     for pos in posArray:
    #         if pos not in alreadySeen:
    #             alreadySeen.append(pos)
    #             # st.button(pos)
    #
    #     currentPos = st.radio("Select Pos: ", alreadySeen)
    #
    #     # simple marking
    #     if currentPos is not None:
    #         getPositionInArray = [i for i, x in enumerate(posArray) if x == currentPos]
    #         st.write(getPositionInArray)
    #         # coloredArray = []
    #         coloredString = ""
    #         if len(getPositionInArray) == 1:
    #             if beginArray[getPositionInArray[0]] != 0:
    #                 beginning = (sofaString[0:int(beginArray[getPositionInArray[0]])])
    #                 innerPart = sofaString[int(beginArray[getPositionInArray[0]]):int(endArray[getPositionInArray[0]])]
    #                 annoInnerPart = "<span style=\"background-color: red\">" + str(innerPart) + "<sup>" + str(currentPos) + "</sup></span>"
    #                 middle = (str(annoInnerPart))
    #                 ending = (sofaString[int(endArray[getPositionInArray[0]]):len(sofaString)])
    #             coloredString = beginning + middle + ending
    #         if len(getPositionInArray) > 1:
    #
    #             for j in getPositionInArray:
    #                 st.write("More than one occurence!")
    #
    #
    #     for child in root:
    #         if child.attrib.get('sofaString') is not None:
    #             content = child.attrib.get('sofaString')
    #             #content = "<b>" + content + "</b>"
    #             content = coloredString

        xmi_app()

