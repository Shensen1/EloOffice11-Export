import tkinter as tk
from tkinter import filedialog
import os
from datetime import datetime






def core(path):
    impath=path


    settings = {
        "debugmode" : True,

        "user_preferences": {
            "rename_impath": False,
            

        },
        "date": { # without function yet
            "include": True,
            "format" : 0,
        }
    }



    def namextract(path, fofi, ext = ".ESW", kwords = ["SHORTDESC=","DOCDATE="]):
        #extract human readable file/folder name and docdate from ESW
        oldext = ""
        isfile = 0

        #different path assembles for files and dirs

        if "." in fofi:
            oldext = fofi.rsplit(".", 1)[1]

            #build path to the ESW
            fofi = fofi.rsplit(".", 1)[0]
            path = path + os.path.sep + fofi + ext
            isfile = 1
            print(path)
        else:
            path = path + os.path.sep + fofi + ext
            print(path)
            isfile = 0


        #fallback if ESW doesnt exist

        if os.path.exists(path):
            

            #read name and date of the document



            with open (path, "r", encoding="latin-1") as fp:
                nexport =[]
                lines = fp.readlines()
                for line in lines:
                    for kword in kwords:
                        if kword in line:
                            
                            nexport.append(line.replace(kword, ""))
                        
                #for i in nexport:
                #    print("that wath is in the linez: ", i)



                

                #format the date to YYMMDD

                date_str = nexport[1].strip()


                #fallback if Docdate is empty:

                if date_str != "":
                    date_str = date_str.replace("/", ".")
                    #print(date_str)
                    date_obj = datetime.strptime(date_str, "%d.%m.%Y")

                    day = str(date_obj.day).zfill(2)
                    month = str(date_obj.month).zfill(2)
                    year = str(date_obj.year)[2:]

                    formatted_date = year + month + day
                    #print(formatted_date)
                else:
                    formatted_date = ""


                #format new filename string  

                forbiddens = ["/", "<", ">", ":", "\\", "?", "*", "\""]
                newfilename = nexport[0]
                for fstr in forbiddens:
                    newfilename = newfilename.replace(fstr, "-")
                
                newfoldername = newfilename.strip()
                if isfile == 1:
                    newfilename = formatted_date + "_" + newfilename.strip() + "." + oldext
                    return str(newfilename)
                else:
                    return str(newfoldername)
            
        else:
            print(path, "no linked ESW file found")





    dirlist=[]
    nudirlist=[]


    for root, dirs, files in os.walk(impath):



        for file in files:
            if file.endswith(".ESW") or file.endswith(".ini") or file.endswith(".exr"):
                continue

            else:
                nuname = namextract(root, file)
                print(nuname)

                #fallback
                if nuname == None:
                    continue
                else:
                    os.rename(os.path.join(root, file), os.path.join(root, nuname))


        for dir in dirs:
            if dir == "buzzwds":
                continue

            else:
                nuname = namextract(root, dir)
                print(nuname)


                if nuname == None:
                    continue
                else:
                    dirlist.append(os.path.join(root, dir))
                    nudirlist.append(os.path.join(root, nuname))




    # Zip the lists and sort them by the length of the first element
    sorted_lists = sorted(zip(dirlist, nudirlist), key=lambda x: len(x[0]), reverse=True)
    # Unzip the sorted lists
    folderpath, newfoldername = zip(*sorted_lists)


    n=0
    for i in folderpath:
        os.rename(folderpath[n], newfoldername[n])
        n+=1


    for root, dirs, files in os.walk(impath):
        for file in files:
            if file.endswith(".ESW"):
                os.remove(os.path.join(root, file))
            else:
                continue
    

    return


folder_path = None

def choose_folder():
    global folder_path
    # Open a file dialog to choose a folder
    folder_path = filedialog.askdirectory()
    # Update the label with the chosen folder path
    label['text'] = folder_path



def confirm_choice():
    # Open a message box to confirm the choice
    result = tk.messagebox.askyesno('Confirm', 'by clicking ok you will change every filename inside the choosen backup path and delete every ESW file. Are you sure you want to continue?')
    if result:
        core(folder_path)
        tk.messagebox.showinfo('Success', 'Your backup got extracted!')
    else:
        tk.messagebox.showinfo('Aborted', 'Folder choice cancelled')

# Create the main window
root = tk.Tk()
root.title('Choose Folder')

# Create a label to display the chosen folder path
label = tk.Label(root, text='Choose the folder of your EloOffice11 Backup that you want to extract.')
label.pack()

# Create a button to open the file dialog
choose_button = tk.Button(root, text='Choose Folder', command=choose_folder)
choose_button.pack()

# Create an OK button to confirm the choice
ok_button = tk.Button(root, text='OK', command=confirm_choice)
ok_button.pack()

# Create an Abort button to cancel the choice
abort_button = tk.Button(root, text='Abort', command=root.destroy)
abort_button.pack()

# Run the main loop
root.mainloop()




