from tkinter import Tk, Canvas, Frame, BOTH, Label, PhotoImage
import xml.etree.ElementTree as ET


from argparse import ArgumentParser
import os.path


def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg


parser = ArgumentParser(description="ikjMatrix multiplication")
parser.add_argument("-i", dest="filename", required=True,
                    help="input file with two matrices", metavar="racing_chnl_osd_win.xml",
                    type=lambda x: is_valid_file(parser, x))

args = parser.parse_args()

print(args.filename)

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
  
        #color = (0,0,0)
        #canvas = Canvas(self)
        #canvas = Canvas(self,width=1440,height=810)
        
        #for row in range(14):            
        #    pos_x1 = eval("int(row) * int(100)")
        #    pos_x2 = eval("int(pos_x1) + int(100)")
        #    #print(pos_x1, pos_x2)
        #    for column in range(8):
        #        #print(column)
        #        pos_y1 = eval("int(column) * int(100)")
        #        pos_y2 = eval("int(pos_y1) + int(100)")
        #        canvas.create_rectangle(pos_x1, pos_y1, pos_x2, pos_y2, fill="#ffffff")
        #canvas.create_rectangle(0, 810, 0, 1440, fill="#ff0000")       
        
        #canvas.pack()
   
        
        labels = []
        for type_tag in root.findall('rootwindow/childwindow'):
            #print(type_tag)
            name = type_tag.get('name')
            show = type_tag.get('show')
            dx = type_tag.get('dx').replace("px", "")
            dy = type_tag.get('dy').replace("px", "")
            w = type_tag.get('w').replace("px", "")
            h = type_tag.get('h').replace("px", "")
            alignment = type_tag.get('alignment')
            
            if alignment == 'bottom-right':
                dx = eval("int(dx) - int(w) + 1440")
                dy = eval("int(dy) - int(h) + 810")

            if alignment == 'center':
                dx = eval("1440 / 2 - int(w)/ 2")
                dy = eval("810/ 2 - int(h) / 2")
                
            
            if show == 'true' or 'false':
                print('\nchildwindow:', name, dx, dy, w, h, show, alignment)
                
                pixel_img = PhotoImage(width=w, height=h)
                self.label = Label(self, width=w, height=h, image=pixel, text=name, borderwidth=2, relief="groove", background='#68a3db', compound='center')
                self.label.place(x=dx,y=dy)   
                labels.append(self.label)
                #### HBOX Level 1                         
                #for hbox_level1 in type_tag.findall('hbox'):
                #    dy_vbox_level1 = dy
                #    
                #    
                #    #### GAP (count number of gaps in VBOX
                #    count_gap_level1 = 0                        
                #    for gap_level1 in hbox_level1.findall('vbox/gap'):
                #        count_gap_level1+=1                   
                #    if count_gap_level1 > 0:
                #        high_vbox_level1 = eval("int(h) / int(count_gap_level1)")
                #    else:
                #        high_vbox_level1 = 1
                #    #print('  count_gap_level1:', count_gap_level1 , ' high_vbox_level1:',  high_vbox_level1)
                #    
                #    
                #    #### VOBX Level 2 
                #    for vbox_level1 in hbox_level1.findall('vbox'):
                #        size_vbox_level1 = vbox_level1.get('size').replace("px", "")   
                #        #### Generate Lable
                #        #self.label = Label(self, width=size_vbox_level1, height=high_vbox_level1, image=pixel, text='vbox', borderwidth=2, relief="groove", background='#ffffff', compound='center')                    
                #        #self.label.place(x=dx,y=dy_vbox_level1)
                #        dy_vbox_level1 = eval("int(dy_vbox_level1)+int(high_vbox_level1)")
                #        print('dy_vbox_level1 ', dy_vbox_level1)
                #        labels.append(self.label)
                #        print('  size_vbox_level1:', size_vbox_level1)
                #        
                #        dx_vbox_level2 = dx
                #        #### GAP (count number of gaps in VBOX
                        # count_gap_level2 = 0                        
                        # for gap_level2 in vbox_level1.findall('hbox/gap'):
                            # count_gap_level2+=1                   
                        # if count_gap_level2 > 0:
                            # width_vbox_level2 = eval("int(w) / int(count_gap_level2)")
                        # else:
                            # width_vbox_level2 = 1
                        # #print('  count_gap_level2:', count_gap_level2 , ' width_vbox_level1:',  width_vbox_level1)
                        
                        
                        # #### VBOX Level 2
                        # for hbox_level2 in vbox_level1.findall('hbox'):
                            # size_hbox_level2 = hbox_level2.get('size').replace("px", "")
                            # #### Generate Lable
                            # #self.label = Label(self, width=size_hbox_level2, height=high_vbox_level1, image=pixel, text='hbox', borderwidth=1, relief="groove", background='#ffffff', compound='center')                    
                            # #self.label.place(x=dx_vbox_level2,y=dy_vbox_level1)
                            # dx_vbox_level2 = eval("int(dx_vbox_level2)+int(width_vbox_level2)")
                            # print('dx_vbox_level2 ', dx_vbox_level2)
                            # labels.append(self.label)
                            # print('    size_hbox_level2:',size_hbox_level2)
                            
                            # for image_level1 in hbox_level2.findall('image'):
                                # name_img_level1 = image_level1.get('name')
                                # print('      name_img_level1:', name_img_level1)


        #canvas.pack(fill=BOTH, expand=1)
    
def main():

    root = Tk()
    ex = Example()
    root.geometry("1440x810")    
    root.mainloop()
    


if __name__ == '__main__':
    main()
