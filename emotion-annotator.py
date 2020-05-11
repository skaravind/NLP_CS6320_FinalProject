import tkinter as tk
import json
import sys
from enum import Enum
from html import unescape



class HPVUseRB(Enum):
  ANGER = 0,
  ANTICIPATION = 1
  DISGUST = 2,
  FEAR = 3,
  JOY = 4,
  LOVE = 5,
  OPTIMISM = 6,
  PESSIMISM = 7,
  SADNESS = 8,
  SURPRISE = 9
  TRUST = 10,
  NEUTRAL = 11


emotion_list = ['ANGER', 'ANTICIPATION', 'DISGUST', 'FEAR', 'JOY', 'LOVE',
                'OPTIMISM', 'PESSIMISM', 'SADNESS', 'SURPRISE', 'TRUST', 'NEUTRAL']
emotion_dict = {}

class Application(tk.Tk):
  def __init__(self, parent):
    tk.Tk.__init__(self, parent)
    self.parent = parent
    self.initialize()

  def initialize(self):
    self.data_indexer = 0
    self.covid_19_data = self.populateData()
    self.variable_declaration()
    self.create_widgets()
    self.UpdateDataToGui()

  def populateData(self):
    file_path = sys.argv[1]
    with open(file_path, 'r+') as json_file:
      return json.load(json_file)

  def variable_declaration(self):
    '''
    variable declaration will create all of the variables needed to be displayed from the json file. We also need to keep
    track of what post we are on.
    :return:
    '''
    self.body_text = tk.Text(borderwidth=1, bg='white', padx=10)
    self.id_var = tk.StringVar()
    self.radioButton_value = tk.IntVar()
    self.emotion_dict = {}
    self.completeVar = tk.BooleanVar(value=bool(self.covid_19_data[self.data_indexer]['complete']))



  def create_widgets(self):
    self.grid()

    id_label = tk.Label(self, text='ID: ', anchor='w', bg='white', font="Arial 12 bold")
    id_string = tk.Label(self, textvariable=self.id_var, anchor='w', bg='white', font="Arial 12 bold")

    completedCB = tk.Checkbutton(self, text="Completed Annotation", variable=self.completeVar,
                                 command=self.update_check_boxes, bg="white")

    # All posts, Annotated Posts, Unannotated Posts
    allPostsButton = tk.Button(self, text="All Posts", command=self.all_posts())
    annotatedButton = tk.Button(self, text="Annotated Posts", command=self.annotated_posts())
    unannotatedButton = tk.Button(self, text="Unannotated Posts", command=self.unannotated_posts())

    # Previous Post, Save Posts, Next Posts
    prevButton = tk.Button(self, text="Previous Post", command=self.previous_post)
    saveButton = tk.Button(self, text="Save Annotations", command=self.save_annotations)
    nextButton = tk.Button(self, text="Next Post", command=self.next_post)

    scrollb = tk.Scrollbar(self, command=self.body_text.yview)

    # Annotation Completed


    # Create Emotions
    emotion_counter = 0
    emo_colm = 8
    for emotion in self.covid_19_data[self.data_indexer]['emotion']:
      self.emotion_dict[emotion] = tk.BooleanVar(value=self.covid_19_data[self.data_indexer]['emotion'][emotion])
      #print(emotion,  self.covid_19_data[self.data_indexer]['emotion'][emotion])
      #cb = tk.Checkbutton(self, text=str(emotion), variable=self.emotion_dict[emotion])
      #cb.pack()
      # self.emotion_list.append(tk.IntVar(value=int(self.covid_19_data[self.data_indexer]['emotion_list'][emotion])))
      # self.emotion_dict[key] = tk.IntVar(value=100+emotion_counter)
      checkbox = tk.Checkbutton(self, text=str(emotion), variable=self.emotion_dict[emotion], indicatoron=0,
                                 background="white", selectcolor='#d2b4de', command=self.update_check_boxes)
      checkbox.grid(row=emotion_counter+1, column=emo_colm, sticky="NSEW")
      emotion_counter += 1
      # if emotion_counter >= 7:
      #   emotion_counter = 1
      #   emo_colm += 1







    ''' Note that the grid we are defining is going to be 12 rows 9 columns'''
    id_label.grid(row=0, column=1)
    id_string.grid(row=0, column=2)
    completedCB.grid(row=0, column=8, columnspan = 1)

    self.body_text.grid(row = 1, rowspan = 12, column = 0, columnspan = 6, sticky='NSEW')
    scrollb.grid(row=1, rowspan=12, column=7, sticky='nsew')
    self.body_text['yscrollcommand'] = scrollb.set

    prevButton.grid(row = 14, column = 0, columnspan = 1)
    saveButton.grid(row = 14, column = 2, columnspan = 2)
    nextButton.grid(row = 14, column = 5, columnspan = 1)

    for gridNum in range(6):
      self.grid_columnconfigure(gridNum, weight=2, minsize=100)
    self.grid_columnconfigure(7, weight=1, minsize=10)
    self.grid_columnconfigure(8, weight=2, minsize=100)

    for gridNum in range(1, 14):
      self.grid_rowconfigure(gridNum, weight=1, minsize=20)





  def update_check_boxes(self):
    for emotion in self.covid_19_data[self.data_indexer]['emotion']:
      self.covid_19_data[self.data_indexer]['emotion'][emotion] = self.emotion_dict[emotion].get()
    self.covid_19_data[self.data_indexer]['complete'] = self.completeVar.get()
    #print(self.covid_19_data[self.data_indexer]['emotion'])


  def all_posts(self):
    pass
  def annotated_posts(self):
    pass
  def unannotated_posts(self):
    pass

  def previous_post(self):
    if(self.data_indexer > 0):
      #self.save_annotations()
      self.data_indexer -= 1
      self.completeVar.set(self.covid_19_data[self.data_indexer]['complete'])
      for emotion in self.covid_19_data[self.data_indexer]['emotion']:
        self.emotion_dict[emotion].set(self.covid_19_data[self.data_indexer]['emotion'][emotion])
      self.UpdateDataToGui()

  def save_annotations(self):
    with open(sys.argv[1], 'w+') as outstream:
      json.dump(self.covid_19_data, outstream)

  def next_post(self):
    if(self.data_indexer < len(self.covid_19_data)):
      #self.save_annotations()
      self.data_indexer += 1
      self.completeVar.set(self.covid_19_data[self.data_indexer]['complete'])

      for emotion in self.covid_19_data[self.data_indexer]['emotion']:
        self.emotion_dict[emotion].set(self.covid_19_data[self.data_indexer]['emotion'][emotion])
      self.UpdateDataToGui()




  def UpdateDataToGui(self):
    self.id_var.set(self.covid_19_data[self.data_indexer]['id'])
    try:
      self.bodyVar = unescape(self.covid_19_data[self.data_indexer]['body'])#.encode(encoding='UTF-8', errors='strict').decode()
    except:
      self.bodyVar = (self.covid_19_data[self.data_indexer]['body']).encode(encoding='UTF-8', errors='strict').decode()
    self.body_text.config(state=tk.NORMAL, font=("times", 20, 'bold'), spacing1="2")
    self.body_text.delete("1.0", "end")
    self.body_text.insert("1.0", self.bodyVar)
    self.body_text.config(state=tk.DISABLED)


if __name__ == '__main__':
  app = Application(None)
  app.configure(bg='white')
  app.title('Emotion Annotator')
  app.mainloop()
