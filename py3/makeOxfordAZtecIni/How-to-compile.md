## pyinstaller for python 3.5

From [stackoverflow](http://stackoverflow.com/questions/33168229/how-to-create-standalone-executable-file-from-python-3-5-scripts):

> You can use PyInstaller which support python 3.5. To install it with pip execute in terminal:

```
pip install pyinstaller
```

To build **makeOxfordAZtecIni.exe**: First make sure you have the environment
variable **EDS_ROOT** set. You want everything in **%EDS_ROOT%/Oxford/py**

```
pyinstaller --onefile makeOxfordAZtecIni.py
```
