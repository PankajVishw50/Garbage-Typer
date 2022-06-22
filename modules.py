from tkinter import * 
from PIL import ImageTk, Image
from tkinter import messagebox
import sqlite3
import random


class Letter:
	id = 0 

	def __init__(self, master, letter):
		self.master = master
		self.letter = letter 
		self.color = "White"
		self.status = None
		self.letter_widget = Label(self.master)

		Letter.id += 1 
		self.letter_id = Letter.id

		self.letter_widget = Label(self.master, text=self.letter, font="candara 17",
		 fg="black", bg="White",
		 width=1)



	def show(self, row, column):

		self.letter_widget.grid(row=row, column=column, padx=1/2,
		 pady=1, ipadx=6, ipady=1)

	

class Session:
	def __init__(self):

		self.current_page_index = 0 
		self.current_file_index = 0

		# 3 Position Available 1. typing_area 2. file_area 3.new_area
		#	 default is typing_area
		''' 
		3 Position Available 
		1. typing_area	2. file_area	3.new_area 
		'''
		self.current_frame = None
		self.user_position = "typing_area"
		self.pages = list()


		self.load_database() 


	# Loading data from Database
	def load_database(self):
		self.conn = sqlite3.connect("Text.db")
		self.c = self.conn.cursor()

		self.c.execute("SELECT * FROM text")
		self.data = self.c.fetchall()
		self.data_record = dict()

		for index, files in enumerate(self.data):
			new_file = list(files)[0]
			new_file = new_file.strip()
			new_file = new_file.replace("\n", " ")
			
			while new_file.count("  ") > 0:
				new_file = new_file.replace("  ", " ")

			self.data_record[index] = new_file
		
		self.conn.commit()
		self.conn.close()



	def convert_to_pages(self, file):
		self.pages = list() 
		
		if len(file) < 400:
			self.pages.append(file)
		else:
			for index, x in enumerate(range(len(file) // 400 + 1)):
				query = file[index*400:400*(index+1)]
				query.replace("\n", " ")
				self.pages.append(query)

				print(f"This page length = {len(query)}")

		print('Self.Pages ===== ')
		print("0-------")
		print(self.pages)
		print(len(self.pages))
		# print("1------")
		# print(self.pages[1])
		# print(len(self.pages))

	def del_frame(self):
		try:
			self.current_frame.destroy() 
		except: 
			pass 




class Features:

	def __init__(self, max):
		self.random = 0 
		self.max = max - 1
		self.send_process = False

	def send_database(self, file):
		self.send_process = True 
		print("------ Sending to database --------")

		if len(file) < 5:
			print("Too small to send")
			return messagebox.showerror("Failed", "Try to add some more letters")

		file = file.replace("\n", " ")
		file = file.strip() 
		
		while file.count("  ") > 0:
			file = file.replace("  ", " ")

		print("File-----" + "\n" + file)
		print("Length of file: " + str(len(file)))

		conn = sqlite3.connect("Text.db")
		c = conn.cursor()

		c.execute("INSERT INTO text VALUES(:data)", {"data": file})

		conn.commit()
		conn.close()


		return messagebox.showinfo("Successfully", "It was saved succefully")

	def delete_database(self, file_index): 
		file_index += 1 

		conn = sqlite3.connect("Text.db")
		c = conn.cursor()

		c.execute(f"DELETE FROM text WHERE oid={file_index}")

	def get_random(self):
		number = random.randint(0, self.max)

		self.random = number




