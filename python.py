import pathlib, os
from typing import Union, AnyStr

def secure_delete(path: Union[AnyStr, pathlib.Path], passes: int =3) -> None:
    '''
    At first it write the file with some random data , even repeatedly, then delete it
    Meaning the entire contents of the file were still intact and every pass just added to the overall size of the file. So it ended up being [Original Contents][Random Data of that Size][Random Data of that Size][Random Data of that Size] which is not the desired effect obviously
    Firstopen the file in append to find the length, 
    then reopen in r+ so that it can seek to the beginning 
    (in append mode it seems like what caused the undesired effect is that it was not actually possible to seek to 0)
    
    Answer was copied from stackoverflow with some type hinting changes :) 
    https://stackoverflow.com/questions/17455300/python-securely-remove-file
    '''
    with open(path, "ba+", buffering=0) as delfile:
        length: int = delfile.tell()
    delfile.close()
    with open(path, "br+", buffering=0) as delfile:
        for i in range(passes):
            delfile.seek(0,0)
            delfile.write(os.urandom(length))
        delfile.seek(0)
        for x in range(length):
            delfile.write(b'\x00')
    os.remove(path)

if __name__ == '__main__':
    path = input('Enter the file path to be deleted: ')
    if os.path.isfile(path.strip(' ').strip('\n')):
        secure_delete(path)
        print('Securely Deleted:', path)
    else:
        print('The given file does not exists in the system')