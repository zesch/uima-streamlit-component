import setuptools

setuptools.setup(
    name="testUimaStreamlitComponent",
    version="0.0.3",
    author="",
    author_email="",
    description="",
    long_description="",
    long_description_content_type="text/plain",
    url="",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.6",
    install_requires=[
        # By definition, a Custom Component depends on Streamlit.
        # If your component has other Python dependencies, list
        # them here.
        "streamlit >= 0.63",
        "numpy >= 1.22.2",
        "pandas >= 1.4.0",
        "dkpro_cassis"
    ],
)
