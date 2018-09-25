#
# @Email:  jmaggio14@gmail.com
#
# MIT License
#
# Copyright (c) 2018 Jeff Maggio, Nathan Dileas, Ryan Hartzell
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#



def format_dict(dictionary):
    """
    creates a formatted string that represents a dictionary on multiple lines

    >>> a = "{'d': 4, 'b': 2, 'c': 3, 'a': {'d': 4, 'b': 2, 'c': 3, 'a': {'d': 4, 'b': 2, 'c': 3, 'a': 1}}}"
    >>> a
        {
        'a' : {
              'a' : {
                    'a' : 1,
                    'b' : 2,
                    'c' : 3,
                    'd' : 4,},
              'b' : 2,
              'c' : 3,
              'd' : 4,},
        'b' : 2,
        'c' : 3,
        'd' : 4,}
    """
    formatted = ""
    for key in sorted(dictionary):
        val = dictionary[key]

        if isinstance(key,str):
            key = "'{}'".format(key)

        if isinstance(val,dict):
            val = format_dict(val).replace('\n','\n' + ' ' * (len(key)+3))

        formatted += "\n{} : {},".format(key,val)

    return '{' + formatted + '}'

def main():
    import copy
    import imsciutils as iu
    a = {'a':1,'b':2,'c':3,'d':4}
    b = copy.deepcopy(a)
    b['a'] = copy.deepcopy(a)
    b['a']['a'] = copy.deepcopy(a)
    print( iu.util.format_dict(b) )

if __name__ == "__main__":
    main()
