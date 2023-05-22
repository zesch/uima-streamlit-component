import os
import re

import numpy as np
import pandas as pd
import streamlit.components.v1 as components
import streamlit as st
from xml.etree import ElementTree as ET
from cassis import *
from operator import itemgetter
import numpy
import pandas
import mainMethods

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
        # We give the component a simple, descriptive name
        "testUimaStreamlitComponent",
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
    _component_func = components.declare_component("testUimaStreamlitComponent", path=build_dir)


# Create a wrapper function for the component. This is an optional
# best practice - we could simply expose the component function returned by
# `declare_component` and call it done. The wrapper allows us to customize
# our component's API: we can pre-process its input args, post-process its
# output value, and add a docstring for users.






# Add some test code to play with the component while it's in development.
# During development, we can run this just as we would any other Streamlit
# app: `$ streamlit run testUimaStreamlitComponent/__init__.py`
if not _RELEASE:
    st.title('Visualisierung Textmerkmale')
    #st.write("""*TODO: find better title*""")
    file = st.sidebar.file_uploader("Upload cas.xmi")
    file2 = st.sidebar.file_uploader("Upload typesystem.xml")
    #enter type to highlight here
    typeFromFile = "frequencyBand"
    testtext = "Cars driving cars? I never thought that the day would come when cars are driving themselves, yet it is right around the corner. Which leads me to be scared do to malfuntions of machines causing injury, But still very excited because of the techonology is very fascinating. Their are so many cars with people driving that get in accidents due to impairment and i believe that this technology can really benefit our society. " \
               "Their are many things that a car with no driver can lead people to think. Like it may lead people to think that maybe sitting in a car and not driving may get boring. Although if they are a passenger in a car are they bored? "
    pathSen = "de.tudarmstadt.ukp.dkpro.core.api.segmentation.type.Sentence"
    pathTok = "de.tudarmstadt.ukp.dkpro.core.api.segmentation.type.Token"
    pathPos = "de.tudarmstadt.ukp.dkpro.core.api.lexmorph.type.pos.POS"
    pathFreq = "org.lift.type.Frequency"
    testarray = [
        ["Lead", 0, 46],
        ["Position", 47, 72],
        ["Counterclaim", 75, 108],
        ["Rebuttal", 109, 120],
        ["Rebuttal", 123, 138],
        ["Claim", 139, 155],
        ["Counterclaim", 156, 169],
        ["Rebuttal", 170, 219],
        ["Evidence", 220, 246],
        ["Claim", 247, 265],
        ["Concluding Statement", 268, 330]
    ]

    testFreqList = ["NNP", "VBD", "IN", "DT", "NN", ".", "JJ"]


#changes: uima_Reader_Try is now uima_reader, same for freq

    if file is not None:
        visualRep = st.sidebar.radio("Choose a visual representation:", ('Multiselect', 'Table', 'UIMA-Cassis-Reader', 'SimpleHighlightPassage', 'FrequencyHighlighting', 'FreqAndPos'))
        if visualRep == 'Multiselect':
            mainMethods.xmi_app_two(file, typeFromFile)
        if visualRep == 'Table':
            mainMethods.xmi_app_table_version(file, typeFromFile)
        if visualRep == 'UIMA-Cassis-Reader':
            mainMethods.uima_Reader_Try(file, file2)
        if visualRep == 'SimpleHighlightPassage':
            mainMethods.simpleHighlightingPassages(testtext, testarray)
        if visualRep == 'FrequencyHighlighting':
            mainMethods.freqencyHighlighting(file, file2, testFreqList)
        if visualRep == 'FreqAndPos':
            mainMethods.freq_and_pos(file, file2, pathSen, pathPos, pathFreq, pathTok)
            #mockTagCompLing()


