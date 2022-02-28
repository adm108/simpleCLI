import tempfile
import click, zipfile, pathlib
import os
import tempfile
from datetime import date

@click.command()
@click.option('--zipname', '-zn', help="Zip file name", required=True, prompt="Zip file name please")
@click.option('--data', '-d', help="Example data", required=True, prompt="Example text for VERSION.txt file please")
@click.option('--value', '-v', help="Update the date in updated.txt file", required=True, prompt="Updated the date? Yes - 1, No - 2")
def supercli(zipname, data, value):
    path = str(pathlib.Path().resolve()) + '\\' + zipname + ".zip"
    try:
        zipfile.ZipFile(path, 'r')
    except FileNotFoundError:
        print("Wrong file name.")
        return
    except zipfile.BadZipFile:
        print("The file is corrupted.")
        return
    
    tmpfd, tmpname = tempfile.mkstemp(dir=os.path.dirname(zipname))
    os.close(tmpfd)

    zipname = zipname + '.zip'
    with zipfile.ZipFile(zipname, 'r') as zin:
         with zipfile.ZipFile(tmpname, 'w') as zout:
             for item in zin.infolist():
                 if str(value) != '1' and item.filename != 'VERSION.txt':
                     zout.writestr(item, zin.read('updated.txt'))

    os.remove(zipname)
    os.rename(tmpname, zipname)

    with zipfile.ZipFile(zipname, mode='a', compression=zipfile.ZIP_DEFLATED) as zf:
        files = 0
        for file in zf.infolist():
            files = files + 1
        if files == 0:
            zf.writestr('VERSION.txt', data)
            if str(value) == '1':
                zf.writestr('updated.txt', str(date.today()))
        else:
            if str(value) == '1':
                zf.writestr('VERSION.txt', data)
                zf.writestr('updated.txt', str(date.today()))
            else:
                zf.writestr('VERSION.txt', data)
