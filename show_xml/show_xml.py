from tkinter import Tk, Canvas, Frame, BOTH, Label, PhotoImage
#import xml.etree.ElementTree as ET
from lxml import etree as ET


from argparse import ArgumentParser
import os.path

from PIL import Image


import sys



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
        #self.setMouseTracking(True)

    def motion(self, event):
        x, y = event.x, event.y
        #print('{}, {}'.format(x, y))
        #self.label_mouse.set("Tkinter Change Label Text Example") 
        pixel = PhotoImage(width=1, height=1)
        new_pos = 'x: {}, y: {}'.format(x, y)
        new_pos_neg = '-x: {}, -y: {}'.format(eval("1440-x"), eval("810-y"))
        new = new_pos + '\n' + new_pos_neg
        self.label_mouse.config(text=new, image=pixel, width=80, height=30)
        
        if x > 1440/2:
            x=eval("x-80")
        if y > 810/2:
            y=eval("y-30")
        
        self.label_mouse.place(x=x,y=y)
        #self.label_mouse.configure(text=x)
        #self.label_mouse.after(1000, self.update)


    
    def initUI(self):

       
        
        self.master.title('Test')
        #self.pack(fill=BOTH, expand=1)
        self.pack(fill='both', expand=True)
        
        pixel = PhotoImage(width=1, height=1)
  
        color = (0,0,0)
        canvas = Canvas(self,width=1440,height=810)
        
        #self.mouse_var = "test"
        #self.mouse_var.set("Test")
        
        
        #for row in range(144):            
        #    pos_x1 = eval("int(row) * int(10)")
        #    pos_x2 = eval("int(pos_x1) + int(10)")
        #    #print(pos_x1, pos_x2)
        #    for column in range(81):
        #        #print(column)
        #        pos_y1 = eval("int(column) * int(10)")
        #        pos_y2 = eval("int(pos_y1) + int(10)")
        #        canvas.create_rectangle(pos_x1, pos_y1, pos_x2, pos_y2, fill="#ffffff", stipple="gray50")   
        #canvas.create_rectangle(0, 0, 1440, 810, fill="#34eb58", stipple="gray50")        
        
        
        labels = []       
        
        
        self.label_mouse = Label(self, width=100, height=30, image=pixel, text="Klick with mouse\nto get coordinates", borderwidth=2, relief="groove", background='#68ffdb', compound='center')
        self.label_mouse.place(x=0,y=0)   
        
        #labels.append(self.label_mouse)

        for type_tag in root.findall('rootwindow/childwindow'):
            #print(type_tag)
            name = type_tag.get('name')
            show = type_tag.get('show')
            dx = type_tag.get('dx').replace("px", "")
            dy = type_tag.get('dy').replace("px", "")
            w = type_tag.get('w').replace("px", "")
            h = type_tag.get('h').replace("px", "")
            alignment = type_tag.get('alignment')

            r=5
            center_ovalx1 = eval('int(dx) - int(r)')
            center_ovalx2 = eval('int(dx) + int(r)')
            center_ovaly1 = eval('int(dy) - int(r)')
            center_ovaly2 = eval('int(dy) + int(r)')
            
            if alignment == 'bottom-right':
                dx = eval("int(dx) - int(w) + 1440")
                dy = eval("int(dy) - int(h) + 810")
                center_ovalx1 =  eval('int(center_ovalx1) + 1440')
                center_ovalx2 =  eval('int(center_ovalx2) + 1440')
                center_ovaly1 =  eval('int(center_ovaly1) + 810')
                center_ovaly2 =  eval('int(center_ovaly2) + 810')

            
            if alignment == 'center':
                dx = eval("1440 / 2 - int(w)/ 2")
                dy = eval("810/ 2 - int(h) / 2")

            #print(center_ovalx1, center_ovaly1, center_ovalx2, center_ovaly2)
            canvas.create_oval(center_ovalx1, center_ovaly1, center_ovalx2, center_ovaly2, fill="#FF0000")
            
            if show == 'true' or 'false':
                print('\nchildwindow:', name, dx, dy, w, h, show, alignment)
                
                pixel_img = PhotoImage(width=w, height=h)
                
                dx1 = eval("int(dx) - int(1)")
                dy1 = eval("int(dy) - int(1)")
                dx2 = eval("int(dx) + int(w)")
                dy2 = eval("int(dy) + int(h)")
                
                dx3 = eval("int(dx) + int(w) / 2")
                dy3 = eval("int(dy) + int(h) / 2")
                canvas.create_rectangle(dx1, dy1, dx2, dy2, fill="#34eb58", stipple="gray25")
                canvas.create_text(dx3, dy3, text=name, anchor="center")

                
                #self.label = Label(self, width=w, height=h, image=pixel, text=name, borderwidth=2, relief="groove", background='#68a3db', compound='center')
                #self.label.place(x=dx,y=dy)   
                #labels.append(self.label)
                #### HBOX Level 1                         
                for hbox_level1 in type_tag.findall('hbox'):
                    
                    dx_sub_hbox_level1 = dx
                    #for sub_hbox_level1 in hbox_level1.findall('gap|') + hbox_level1.findall('image') + hbox_level1.findall('label'):
                    for sub_hbox_level1 in hbox_level1.xpath("gap|image|label"):


                        #print(sub_hbox_level1.tag)
                        if sub_hbox_level1.tag == 'gap':
                            hbox_level1_gap_size = sub_hbox_level1.get('size')                            
                            #wenn None 0px setzen
                            if hbox_level1_gap_size == None:
                                hbox_level1_gap_size = '0px'
                                #print ('Null: ', hbox_level1_gap_size)                               
                            hbox_level1_gap_size = hbox_level1_gap_size.replace("px", "") 
                            print('gap size: ', hbox_level1_gap_size)
                            dx_sub_hbox_level1 = eval("int(dx_sub_hbox_level1) + int(hbox_level1_gap_size)")
                            #print('gap', dx_sub_hbox_level1)


                        if sub_hbox_level1.tag == 'image':
                            hbox_level1_image_size = sub_hbox_level1.get('size')
                            #wenn None 0px setzen
                            if hbox_level1_image_size == None:
                                hbox_level1_image_size = '0px'
                                #print ('Null: ', hbox_level1_gap_size)                               
                            hbox_level1_image_size = hbox_level1_image_size.replace("px", "") 
                            #print(hbox_level1_image_size)
                            
                            file=os.path.join(os.getcwd(), "system\gui\image", sub_hbox_level1.get('image.name'))
                            if os.path.isfile(file):
                                print ('File gefunden')
                            else:
                                print("\nFile not accessible:", os.path.join(os.getcwd(), "system\gui\image", sub_hbox_level1.get('image.name')))                               
                                sys.exit("Download all files from your dji goggle to here: adb pull /system/gui/image/")

                            
                            self.image = PhotoImage(file=os.path.join(os.getcwd(), "system\gui\image", sub_hbox_level1.get('image.name')))                            
                            self.label = Label(self, image=self.image, background='#DAF7A6')
                            self.label.place(x=dx_sub_hbox_level1,y=dy)
                           
                            
                            labels.append(self.label)
                            # Save every image
                            self.label.image = self.image                           
                            dx_sub_hbox_level1 = eval("int(dx_sub_hbox_level1) + int(hbox_level1_image_size)")
                            print('img:', sub_hbox_level1.get('image.name'), ' img size: ', hbox_level1_image_size)


                        if sub_hbox_level1.tag == 'label':
                            hbox_level1_lable_name = sub_hbox_level1.get('name')
                            hbox_level1_lable_size = sub_hbox_level1.get('size')
                            hbox_level1_lable_color = sub_hbox_level1.get('color')
                            hbox_level1_lable_alignment = sub_hbox_level1.get('alignment')
                            hbox_level1_lable_text = sub_hbox_level1.get('text')
                            
                            #wenn None 0px setzen
                            if hbox_level1_lable_size == None:
                                hbox_level1_lable_size = '0px'
                                #print ('Null: ', hbox_level1_gap_size)                               
                            hbox_level1_lable_size = hbox_level1_lable_size.replace("px", "") 
                            
                            
                            dx1_lab_level1 = eval("int(dx_sub_hbox_level1) - int(1)")
                            dy1_lab_level1 = eval("int(dy) - int(1)")
                            dx2_lab_level1 = eval("int(dx_sub_hbox_level1) + int(hbox_level1_lable_size)")
                            dy2_lab_level1 = eval("int(dy) + int(h)")
                            canvas.create_rectangle(dx1_lab_level1, dy1_lab_level1, dx2_lab_level1, dy2_lab_level1, fill="#eecafa", stipple="gray25", activefill='cyan')
                            
                            dx3_lab_level1 = eval("int(dx_sub_hbox_level1) + int(hbox_level1_lable_size) / 2")
                            dy3_lab_level1 = eval("int(dy) + int(h) / 2")
                            canvas.create_text(dx3_lab_level1, dy3_lab_level1, text=name, anchor="center") 
                
                            #self.label = Label(self, width=hbox_level1_lable_size, height=h, image=pixel, text=hbox_level1_lable_name, borderwidth=2, relief="groove", background='#eecafa', compound=hbox_level1_lable_alignment, textvariable=hbox_level1_lable_name)
                            #self.label.place(x=dx_sub_hbox_level1,y=dy)   
                            #labels.append(self.label)

                            dx_sub_hbox_level1 = eval("int(dx_sub_hbox_level1) + int(hbox_level1_lable_size)")
                            print('lable', hbox_level1_lable_name, ' lable size: ', hbox_level1_lable_size)
                        #print('dx_sub_hbox_level1: ', dx_sub_hbox_level1)    
                    
                    
                    dy_vbox_level1 = dy

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
                    for vbox_level1 in hbox_level1.findall('vbox'):

                        #size_vbox_level1 = vbox_level1.get('size').replace("px", "")   
                        #print('size_vbox_level1:', size_vbox_level1)
                #       # #### Generate Lable
                        #x1 = eval("int(dx)")
                        #x2 = eval("int(dx) + int(size_vbox_level1)")
                        #y1 = eval("int(dy_vbox_level1)")
                        #y2 = eval("int(dy_vbox_level1) + int(size_vbox_level1)")
                        #canvas.create_rectangle(x1, y1, x2, y2, fill="#34eb58", stipple="gray50")
                        #self.label = Label(self, width=w, height=size_vbox_level1, image=pixel, text='vbox', borderwidth=2, relief="groove", background='#ffffff', compound='center')                    
                        #self.label.place(x=dx,y=dy_vbox_level1)
                        #labels.append(self.label)
                #        dy_vbox_level1 = eval("int(dy_vbox_level1)+int(high_vbox_level1)")
                #        print('dy_vbox_level1 ', dy_vbox_level1)
                #        
                        #print('size_vbox_level1:', size_vbox_level1)
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
                        for hbox_level2 in vbox_level1.findall('hbox'):
                            # size_hbox_level2 = hbox_level2.get('size').replace("px", "")
                            # #### Generate Lable
                            # #self.label = Label(self, width=size_hbox_level2, height=high_vbox_level1, image=pixel, text='hbox', borderwidth=1, relief="groove", background='#ffffff', compound='center')                    
                            # #self.label.place(x=dx_vbox_level2,y=dy_vbox_level1)
                            # dx_vbox_level2 = eval("int(dx_vbox_level2)+int(width_vbox_level2)")
                            # print('dx_vbox_level2 ', dx_vbox_level2)
                            # labels.append(self.label)
                            # print('    size_hbox_level2:',size_hbox_level2)
                             
                            for image_hbox_level2 in hbox_level2.findall('image'):
                            
                                 file=os.path.join(os.path.join(os.getcwd(), "system\gui\image", image_hbox_level2.get('image.name')))
                                 if os.path.isfile(file):
                                    print ('File gefunden')
                                 else:
                                    print("\nFile not accessible:", os.path.join(os.getcwd(), "system\gui\image", image_hbox_level2.get('image.name')))                               
                                    sys.exit("Download all files from your dji goggle to here: adb pull /system/gui/image/")
                            
                                 self.image = PhotoImage(file=os.path.join(os.getcwd(), "system\gui\image", image_hbox_level2.get('image.name')))
                                 print('      img:', image_hbox_level2.get('image.name'))
                                 
                                 self.label = Label(self, image=self.image, bg='black')
                                 self.label.place(x=dx,y=dy)
                                 labels.append(self.label)
                                 self.label.image = self.image
                                 

        canvas.pack()
        #canvas.bind('<Motion>', self.motion)
        canvas.bind('<Button-1>', self.motion)
        #canvas.pack(fill=BOTH, expand=1)
    
#def motion(event):
#    x, y = event.x, event.y
#    print('{}, {}'.format(x, y))
#    
def main():

    root = Tk()
    
    ex = Example()
    root.geometry("1440x810")    
    #root.bind('<Motion>', motion)
    #root.bind('<Motion>', motion))
    root.mainloop()


if __name__ == '__main__':
    main()
