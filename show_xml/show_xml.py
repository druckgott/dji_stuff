from tkinter import Tk, Canvas, Frame, BOTH, Label, PhotoImage
import xml.etree.ElementTree as ET

from argparse import ArgumentParser
import os.path

def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return open(arg, 'r')  # return an open file handle


parser = ArgumentParser(description="ikjMatrix multiplication")
parser.add_argument("-i", dest="filename", required=True,
                    help="input file with two matrices", metavar="racing_chnl_osd_win.xml",
                    type=lambda x: is_valid_file(parser, x))
args = parser.parse_args()

tree = ET.parse(args.filename)
root = tree.getroot()
   

class Example(Frame):

    def __init__(self):
        super().__init__()

        self.initUI()

  
    
    def initUI(self):

        self.master.title("xml_viewer")
        #self.pack(fill=BOTH, expand=1)
        self.pack(fill='both', expand=True)
        
        pixel = PhotoImage(width=1, height=1)

        labels = []
        for type_tag in root.findall('rootwindow/childwindow'):
            name = type_tag.get('name')
            show = type_tag.get('show')
            dx = type_tag.get('dx').replace("px", "")
            dy = type_tag.get('dy').replace("px", "")
            w = type_tag.get('w').replace("px", "")
            h = type_tag.get('h').replace("px", "")
            print(name, dx, dy, w, h, show)
            if show == 'true':
                self.label = Label(self, width=w, height=h, image=pixel, text=name, borderwidth=2, relief="groove", background='#ffffff', compound='center')
                self.label.place(x=dx,y=dy)   
                labels.append(self.label)                
           

        #canvas.pack(fill=BOTH, expand=1)
    
def main():

    root = Tk()
    ex = Example()
    root.geometry("1440x810")    
    root.mainloop()



if __name__ == '__main__':
    main()
