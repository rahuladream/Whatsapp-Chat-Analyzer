import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='wanalyzer',  
     version='0.2',
     scripts=['wanalyzer'] ,
     author="Rahul Singh",
     author_email="rahul.singh4800@gmail.com",
     description="A WhatsApp Chat Analyzer Script",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/rahuladream/Whatsapp-Chat-Analyzer/",
     packages=setuptools.find_packages(),
     py_modules=['chat_decode', 'color'],
         install_requires=[
        'emoji', 'python-dateutil'
    ],
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )