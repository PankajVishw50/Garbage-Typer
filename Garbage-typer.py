from tkinter import *
import sqlite3
from modules import Letter, Session, Features
from datetime import datetime
import time
from PIL import ImageTk, Image
from tkinter import ttk
import webbrowser

root = Tk()
root.geometry("1080x720")
root.resizable(False, False)
root.iconbitmap("Resources/Logo.ico")
root.title("G-Typer")

global key_index
key_index = 0

# Redirects to my social accounts 
def redirect(x):  # Redirecting to my Profile
    links = ["https://github.com/PankajVishw50", "https://www.linkedin.com/in/pankaj-vishw-4802a9232/"]
    webbrowser.open(links[x])


# Function bounded to start button 
def start():
	global key_index 
	position = user.user_position

	if position == "file_area" and my_tree.selection():
		tree_index = my_tree.selection()

		user.current_page_index = 0
		key_index = 0 

		if tree_index:
			tree_index = int(tree_index[0])
			print('worked')
			user.convert_to_pages(user.data_record[tree_index]) 
			run_setting()
	else:
		features.get_random() 
		user.current_page_index = 0
		user.convert_to_pages(user.data_record[features.random])
		run_setting() 


# to setup New File page 
def new_file(): 
	global send_inac_img, send_inac_image, count_inac_img, count_inac_image
	global new_frame

	developer.configure(bg="#A5BECC")

	user.user_position = ""
	root.unbind("<Key>") 
	user.del_frame() 

	print(f"User_current_frame inside new_frame func = {user.current_frame}")

	new_frame = Frame(content_frame, width=1080, height=650, bg="#A5BECC")
	new_frame.grid_propagate(0)
	new_frame.grid(row=2, column=1)

	edit_panel = Text(new_frame, width=75, height=16, relief="ridge",
	 bd=3, font="arial 15")
	edit_panel.grid(row=1, column=1, padx=120, pady=50, columnspan=3)

	counter = len(edit_panel.get("1.0", END))
	count_label = Label(new_frame, text=f"( {len(edit_panel.get('1.0', END)) - 1} )",
	 bg="#A5BECC", width=5,
	 fg="Gray", font="8")
	count_label.grid(row=2, column=2)

	send_inac_img = Image.open("Resources/Save_inac_image.png")
	send_inac_image = ImageTk.PhotoImage(send_inac_img)
	send_button = Button(new_frame, image=send_inac_image, 
		bd=0, bg="#A5BECC",
		command= lambda: [features.send_database(edit_panel.get('1.0', END)),
		user.load_database()
		])


	count_inac_img = Image.open("Resources/Count_inac_image.png")
	count_inac_image = ImageTk.PhotoImage(count_inac_img)
	count_button = Button(new_frame, image=count_inac_image,
		bd=0, bg="#A5BECC",
		command= lambda: count_label.configure(
			text=f" ( {len(edit_panel.get('1.0', END)) - 1} )"
			))
	send_button.grid(row=2, column=1, sticky=E)
	count_button.grid(row=2, column=3, sticky=W)



	user.current_frame = new_frame
	print(f"new_frame = {user.current_frame}")
	

# To setup Files view page 
def treeview_setup():
	global text_frame , my_tree, tree_frame

	user.user_position = "file_area"
	developer.configure(bg="#C6DCE4")



	user.del_frame()

	style.theme_use("default")
	style.configure("Treeview.Heading", font="Arial 12 bold", foreground="White", 
		background="black",)
	style.map('Treeview', background=[('selected', '#BDE6F1')])


	tree_frame = LabelFrame(content_frame, height=550, bg="White")
	tree_frame.grid_propagate(0)
	tree_frame.grid(row=2, column=1)


	my_tree = ttk.Treeview(tree_frame, selectmode="browse", height=20)

	my_tree['columns'] = ("ID", "Text Preview", "Length")

	my_tree.column("#0", width=0, stretch=NO)
	my_tree.column("ID", width=100, anchor=CENTER)
	my_tree.column("Text Preview", width=800, anchor=W)
	my_tree.column("Length", width=180, anchor=CENTER)

	my_tree.heading("ID", text="ID", anchor=CENTER)
	my_tree.heading("Text Preview", text="Text Preview", anchor=W)
	my_tree.heading("Length", text="Text Length", anchor=CENTER)
	my_tree.pack()


	hint_label = Label(tree_frame, 
		text="*Select and Press Start button to Start Typing.",
		fg="Gray", bg="White" )

	hint_label.pack(pady=(30, 75)) 



	for index, file in user.data_record.items():
		file = file.lstrip()
		my_tree.insert(parent="", index="end", iid=index,
				 values=(index, f"{file[:50]}...", len(file)))

	user.current_frame = tree_frame 


# Result function 
def result_page(start, end):
	global errors , result_frame 

	user.user_position = ""
	root.unbind("<Key>")

	user.del_frame()

	total_time = end - start 
	time_in_s = total_time.total_seconds() 
	time_in_min = float(f"{time_in_s/60:.2f}")

	total_letters = 0 
	for x in user.pages:
		x = x.replace(" ", "")
		total_letters += len(x)

	words = total_letters/5

	if time_in_min == 0:
		print("min is 0 ")
		time_in_min = 0.001
		print(time_in_min)

	print("error ", errors)

	error_rate = (errors/5) / time_in_min
	WPM = float(f"{ ((words/time_in_min) - error_rate):.2f}")
	accuracy = int( f"{ ((total_letters-errors)/total_letters) * 100:.0f} ")

	print("\n----------")

	print(f"Total Words: {words:>15}")
	print(f"Errors(W): {errors/5:>15}")
	print(f"Total Time: {str(total_time):>15}")
	print(f"Time in seconds: {time_in_s:>15}")
	print(f"Time in minute: {time_in_min:>15}")
	print(f"Accuracy: {accuracy:>15}%")
	print(f"WPM: {WPM:>15} WPM")
	print(f"gross wpm: {words/time_in_min}")


	print("\n----------")


	result_frame = LabelFrame(content_frame, width=1080, height=550,
		 bg="Black", bd=0) 
	result_frame.grid_propagate(0)
	result_frame.grid(row=2, column=1)

	label_frame = LabelFrame(result_frame, width=300, height=350,
	 	bg="#BDF2D5")
	label_frame.grid_propagate(0)
	label_frame.grid(row=1, column=1, padx=(240, 0), pady=(50, 0))

	data_frame = LabelFrame(result_frame, width=300, height=350, 
		bg="#FFDAAF")
	data_frame.grid_propagate(0)
	data_frame.grid(row=1, column=2, pady=(50, 0))

	second_label = Label(data_frame, text=time_in_s, font="consolas 20", 
		bg="#FFDAAF")
	minute_label = Label(data_frame, text=time_in_min, font="consolas 20", 
		bg="#FFDAAF")
	accuracy_label = Label(data_frame, text=str(accuracy)+"%",  font="consolas 20", 
		bg="#FFDAAF")
	letters_label = Label(data_frame, text=total_letters,  font="consolas 20", 
		bg="#FFDAAF")
	errors_label = Label(data_frame, text=errors,  font="Roboto 20", 
		bg="#FFDAAF")
	WPM_label = Label(result_frame, text=str(WPM)+ " WPM",  font="concolas 20",
		bg="#BDF2D5", height=2, width=18, fg="black")


	# result_placeholder = Label(data_frame, text="Result",
	# 		 font=("Arial", 20), bg="black", fg="white")
	# result_placeholder.grid(row=1, column=1, columnspan=2, 
	# 	padx=500, pady=(25, 50), ipadx=10)

	second_placeholder = Label(label_frame, text="Time in Seconds: ", font="Roboto 20",
			bg="#BDF2D5")
	second_placeholder.grid(row=1, column=1, padx=50, pady=(50, 10)) 
	second_label.grid(row=1, column=1, padx=100, pady=(50, 10)) 

	minute_placeholder = Label(label_frame, text="Time in Minutes: ", font="Roboto 20",
			bg="#BDF2D5")
	minute_placeholder.grid(row=2, column=1, pady=(0, 10)) 
	minute_label.grid(row=2, column=1, pady=(0, 10))

	letters_placeholder = Label(label_frame, text="Total Letters: ", font="Roboto 20",
			bg="#BDF2D5")
	letters_placeholder.grid(row=3, column=1, pady=(0, 10)) 
	letters_label.grid(row=3, column=1, pady=(0, 10)) 

	errors_placeholder = Label(label_frame, text="Errors: ", font="Roboto 20",
			bg="#BDF2D5")
	errors_placeholder.grid(row=4, column=1, pady=(0, 10))
	errors_label.grid(row=4, column=1, pady=(0, 10))

	accuracy_placeholder = Label(label_frame, text="Accuracy: ", font="Roboto 20",
			bg="#BDF2D5")
	accuracy_placeholder.grid(row=5, column=1, pady=(0, 10))
	accuracy_label.grid(row=5, column=1, pady=(0, 10))

	WPM_placeholder = Label(result_frame, text="WPM: ", font="Roboto 20 bold",
		bg="#FFDAAF", width=18, height=2)
	WPM_placeholder.grid(row=2, column=1, pady=(25, 25),
			padx=(235, 0))
	WPM_label.grid(row=2, column=2)

	user.current_frame = result_frame 


# Binding Function 
def change(event):
	global key_index, errors, start, index 

	# print(f"Key_index = {key_index}")
	# print(f"Index = {index}")

	if key_index == 0 and user.current_page_index == 0:
		print("countdown started.....")
		errors = 0 
		start = datetime.now()

	if (user.current_page_index + 1) == len(user.pages) and key_index == (index+1):
		key_index = 0 

		end = datetime.now() 
		return result_page(start, end)


	if key_index in zero_column and letter_data[key_index].letter == " ":
		key_index += 1


	if len(letter_data) > key_index:
		if event.char == letter_data[key_index].letter:
			letter_data[key_index].letter_widget.configure(bg="#5FD068", fg='White')
		elif event.keysym == "Shift_R" or event.keysym == "Shift_L" :
			key_index -= 1
			print(event)
		else:
			try:
				letter_data[key_index].letter_widget.configure(bg="#F15412")
			except:
				pass

			if letter_data[key_index].letter != " ":
				errors += 1
				# print(f"Errrors = {errors}")

		key_index += 1


	if key_index == (index+1) and (user.current_page_index+1) < len(user.pages):
		user.current_page_index += 1

		return run_setting()


	if key_index == index:
		key_index += 1


def typing_space(file):
	global zero_column, index
	global text_frame, key_index , index 
	key_index = 0  

	user.user_position = "typing_area"
	root.bind("<Key>", change) 

	try:
		user.del_frame()
	except:
		pass


	text_frame = LabelFrame(content_frame, width=1080, height=550)
	text_frame.grid_propagate(0)
	text_frame.grid(row=2, column=1)

	# Creating Words Mapping  
	word_list = file.split()
	word_list_index = 0 
	waste = list()
	temp_index = 0 

	# Redirecting to Initialize required classes
	load_script(file) 


	index = 0
	temp_word = ""
	zero_column = list()
	

	# Main loop to setup all characters on Frame 

	for row in range(14):
		for column in range(34):

			if (len(word_list[word_list_index]) - len(temp_word)) < (34 - column+1):
				if index < len(letter_data):
					if column == 0 and letter_data[index].letter ==  " ":
						zero_column.append(column)
						index += 1  
		
					letter_data[index].show(row, column)

					if letter_data[index].letter != " ":
						temp_word += file[index]


					if word_list[word_list_index] == temp_word:
						if len(word_list) > word_list_index+1:
							word_list_index += 1 
						temp_word = ""
					index += 1 
			else:
				if index < len(letter_data):
					waste.append(Letter(text_frame, " "))
					waste[-1].show(row=row, column=column)

	user.current_frame = text_frame 


# Initializing Letter classes 
def load_script(files):
	global letter_data

	letter_data = dict()

	for index, letterx in enumerate(files):
		letter_data[index] = Letter(text_frame, letterx)


def run_setting():
	global cur_page, key_index, index 

	developer.configure(bg="#C6DCE4")
	key_index = 0 
	cur_page = user.pages[user.current_page_index]

	typing_space(cur_page)



def main():
	global user, features

	user = Session()
	features = Features(len(user.data_record)) 
	features.get_random() 


	user.convert_to_pages(user.data_record[features.random]) 

	run_setting()

errors = 0 
style = ttk.Style()


# Base Frames 
header_frame = LabelFrame(root, height=100, bg="#4B5D67", width=1080, bd=0)
header_frame.grid_propagate(0)
header_frame.grid(row=1, column=1)

content_frame = LabelFrame(root, height=600, bg="#C6DCE4", width=1080, bd=0)
content_frame.grid(row=2, column=1)
content_frame.grid_propagate(0)


# Images and Button Setup 
logo_img = Image.open("Resources/Logo.png")
logo_image = ImageTk.PhotoImage(logo_img)
logo_label = Label(header_frame, image=logo_image, bg="#4B5D67")
logo_label.place(x=50, y=15)

file_inac_img = Image.open("Resources/File_inac_image.png")
file_inac_image = ImageTk.PhotoImage(file_inac_img)

file_button = Button(header_frame, image=file_inac_image,
	bd=0, relief=None, bg="#4B5D67", activebackground="#4B5D67",
	command=treeview_setup)
file_button.grid(row=1, column=1, padx=(850,0), pady=25)


start_inac_img = Image.open("Resources/Start_inac_image.png")
start_inac_image = ImageTk.PhotoImage(start_inac_img)
start_button = Button(header_frame, image=start_inac_image, 
	bd=0, relief=None, bg="#4B5D67", activebackground="#4B5D67",
	command=start)
start_button.grid(row=1, column=2)


new_inac_img = Image.open("Resources/New_inac_image.png")
new_inac_image = ImageTk.PhotoImage(new_inac_img)
new_button = Button(header_frame, image=new_inac_image, 
	bd=0, relief=None, bg="#4B5D67", activebackground="#4B5D67",
	command=new_file)
new_button.grid(row=1, column=3)

developer = Label(root, text="Developer:", font="100", fg="gray", bg="#C6DCE4")
developer.place(x=5, y=675)

github_button = Button(root, text="GitHub", bg="Black", fg="White",
	relief="ridge",
	command= lambda: redirect(0))
github_button.place(x=100, y=669)

linkedin_button = Button(root, text="LinkedIn", bg="Black", fg="White",
	relief="ridge",
	command= lambda: redirect(1))
linkedin_button.place(x=150, y=669)



# Footer 
main() 

root.mainloop() 