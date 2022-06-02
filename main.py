import time
import tkinter as tk
from PIL import Image
from threading import Thread, Event
import PIL.ImageTk
from multiprocessing import Process, Manager
BTN_BG = "#05445E"
BTN_FG = "#75E6DA"
BG = "#D4F1F4"


class AppGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("PiStation")
        self.window.geometry("480x800")
        self.mainFrame = tk.Frame(self.window, width=480, height=800, bg="#D4F1F4")
        self.mainFrame.pack()
        self.containerFrame = tk.Frame(self.mainFrame, width=435, height=600, bg=BG)
        self.containerFrame.place(relx=.05, rely=.03)
        self.window.resizable(False, False)
        # self.window.attributes("-fullscreen",True)
        # self.openPage()
        self.pages = []
        self.page1 = lambda: self.openPage()
        self.page2 = lambda: self.digiCodePage()
        self.page3 = lambda: self.demoEntreprisePage()
        self.pages.append(self.page1)
        self.pages.append(self.page2)
        self.pages.append(self.page3)
        self._chainNumber = ""  # Variable pour sauvegarder la code entree par clavier
        self.hidePassword = ""
        self.__currentPage = 0
        self.listEntreprise=[['./logo/logo.png','Lanestel','For exemple detail just dont have any idea','1231'],['./logo/logo2.png','UBO','For exemple detail just dont have any idea','1111']]

        for e in self.listEntreprise:
            self.autoGeneratePage(e[0],e[1],e[2],e[3])



        self.pages[self.__currentPage]()
        self.navBar()
        self.stop_threads = Event()
        self.action = False  # pour verifier si il y a un action quand touche sur un bouton de clavier, Si oui ne efface pas la memory, sinon efface
        self.t1 = None
        self.t2 = None
        self.activated = False  # Pour controler les 2 threads il est activee, True si activee, sinon False
        # self.update()


        self.window.mainloop()

    def navBar(self):
        self.activated = True
        # arrow button
        self.navButtonFrame = tk.Frame(self.mainFrame, width=400, height=100, bg=BG)
        self.navButtonFrame.place(relx=.5, rely=.9, anchor="center")
        self.leftArrow = tk.Button(self.navButtonFrame, text="<", font=("Helveltica", 30), width=3, bg="#05445E",
                                   fg="#75E6DA")
        self.leftArrow.config(command=lambda: self.leftArrowAction())
        self.leftArrow.grid(column=0, row=1, padx=10, pady=10)
        self.centerButton = tk.Button(self.navButtonFrame, text="O", font=("Helveltica", 30), width=3, bg="#05445E",
                                      fg="#75E6DA")
        self.centerButton.grid(column=1, row=1, padx=10, pady=10)
        self.centerButton.config(command=lambda: self.buttonOaction())
        self.rightArrow = tk.Button(self.navButtonFrame, text=">", font=("Helveltica", 30), width=3, bg="#05445E",
                                    fg="#75E6DA")
        self.rightArrow.grid(column=2, row=1, padx=10, pady=10)
        self.rightArrow.config(command=lambda: self.rightArrowAction())

    def leftArrowAction(self):
        if self.activated:
            self.stop_threads.set()
            self.t1.join()
            self.t2.join()
            self.t1 = None
            self.t2 = None
        self.__currentPage -= 1
        if self.__currentPage < 0:
            self.__currentPage = len(self.pages) - 1
        elif self.__currentPage >= len(self.pages):
            self.__currentPage = 0
        for widget in self.containerFrame.winfo_children():
            widget.destroy()
        self.pages[self.__currentPage]()

    def rightArrowAction(self):
        if self.activated:
            self.stop_threads.set()
            self.t1.join()
            self.t2.join()
            self.t1 = None
            self.t2 = None
        self.__currentPage += 1

        if self.__currentPage >= len(self.pages):
            self.__currentPage = 0
        for widget in self.containerFrame.winfo_children():
            widget.destroy()
        self.pages[self.__currentPage]()

    def buttonOaction(self):
        self.__currentPage = 0
        if self.activated:
            self.stop_threads.set()
            self.t1.join()
            self.t2.join()
            self.t1 = None
            self.t2 = None
        for widget in self.containerFrame.winfo_children():
            widget.destroy()

        self.pages[self.__currentPage]()

    def openPage(self):

        # header
        self.logoCanvas = tk.Canvas(self.containerFrame, bg=BG, height=130, width=200, highlightthickness=0)
        self.logoCanvas.place(relx=.5, rely=.1, anchor="center")
        self.l = PIL.ImageTk.PhotoImage(Image.open("brestmetropole.png"))
        self.logo = self.logoCanvas.create_image(100, 130 / 2, image=self.l)
        # body

        textH1 = tk.Label(self.containerFrame, text="Bienvenue à Mezheven", font=("Arial", 25), bg=BG)
        textH1.place(relx=.5, rely=.25, anchor="center")

        text1 = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
        detailFrame = tk.Frame(self.containerFrame, width=400, height=350, highlightthickness=0, bg=BG)
        detailFrame.place(relx=.5, rely=.57, anchor="center")
        textLabel = tk.Label(detailFrame, font=("Helveltica", 15), text=text1, bg=BG, wraplength=400,
                           justify="left", fg="#189AB4")
        textLabel.place(relx=0.01, rely=.2)

    def digiCodePage(self):
        self.action = False
        self.__stopThread = False
        buttons = {}
        button_layouts = [["7", "8", "9"],
                          ["4", "5", "6"],
                          ["1", "2", "3"],
                          ["Del", "0", "Ok"]]
        text = tk.Label(self.containerFrame, text="Digi Code", font=("Helveltica", 30), bg=BG, fg="#189AB4")
        text.place(relx=.5, rely=.1, anchor="center")
        screenCode = tk.Label(self.containerFrame, text=self._chainNumber, font=("Arial", 30), bg=BG, fg="#189AB4")
        screenCode.place(relx=.5, rely=.3, anchor="center")
        buttonsFrame = tk.Frame(self.containerFrame, bg=BG, width=345, height=600, relief="ridge",
                                highlightthickness=0)
        buttonsFrame.place(relx=.5, rely=.7, anchor="center")
        for i in range(0, len(button_layouts)):
            for j in range(0, len(button_layouts[i])):
                button_label = button_layouts[i][j]
                buttons["button_" + str(i) + "_" + str(j)] = tk.Button(buttonsFrame, text=button_label,
                                                                       font=("Helveltica", 30), width=3,
                                                                       bg="#05445E", fg="#75E6DA")
                buttons["button_" + str(i) + "_" + str(j)].config(
                    command=lambda button=button_label: self.button_action(button, screenCode))
                buttons["button_" + str(i) + "_" + str(j)].grid(column=j, row=i + 1, sticky="news", padx=3, pady=3)
        self.stop_threads.clear()
        self.t1 = Thread(target=self.autoClearMemory, args=(screenCode,))
        self.t2 = Thread(target=self.checkAction, args=())
        self.t1.start()
        self.t2.start()

    def button_action(self, button_pressed, textLabel):
        self.action = True

        if button_pressed == "Ok":
            if (self._chainNumber == ""):
                textLabel.configure(text="Need Code")
            else:
                if self.verifyCode():
                    textLabel.configure(text="Code OK")
                    self._chainNumber = ""
                    self.hidePassword = ""
                else:
                    textLabel.configure(text="Code KO")
                    self._chainNumber = ""
                    self.hidePassword = ""
        elif button_pressed == "Del":
            self._chainNumber = ""
            textLabel.configure(text=self._chainNumber)
        else:
            self._chainNumber += button_pressed
            self.hidePassword += "*"
            textLabel.configure(text=self.hidePassword)

    def checkAction(self):
        while not self.stop_threads.is_set():
            while True:
                if self.action:
                    time.sleep(7)
                    self.action = False
                    time.sleep(0.1)

    def autoClearMemory(self, textLabel):
        while not self.stop_threads.is_set():
            while True:
                if (self._chainNumber != "") and self.action == False:
                    self._chainNumber = ""
                    self.hidePassword = ""
                    textLabel.configure(text=self.hidePassword)
                else:
                    continue
                    time.sleep(0.1)

    def verifyCode(self):
        self.codes = ["1234", "4123", "5671"]
        verified = False
        for code in self.codes:
            if self._chainNumber == code:
                verified = True
        return verified

    def demoEntreprisePage(self):
        logoEntreprise = "./logo/logo.png"
        nomEntreprise = "Lanestel"
        detailEntreprise = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
        numeroEntreprise = "1013"
        # header
        self.logoCanvas = tk.Canvas(self.containerFrame, bg=BG, height=130, width=200, highlightthickness=0)
        self.logoCanvas.place(relx=.5, rely=.1, anchor="center")
        self.l = PIL.ImageTk.PhotoImage(Image.open(logoEntreprise))
        self.logo = self.logoCanvas.create_image(100, 130 / 2, image=self.l)

        # Detail de l'entreprise
        detailFrame = tk.Frame(self.containerFrame, width=400, height=350, highlightthickness=0, bg=BG)
        detailFrame.place(relx=.5, rely=.54, anchor="center")
        nameE = tk.Label(detailFrame, text=nomEntreprise, font=("Helveltica", 20), bg=BG, fg="#05445E")
        nameE.place(relx=0.01, rely=0.01)
        detailE = tk.Label(detailFrame, font=("Helveltica", 15), text=detailEntreprise, bg=BG, wraplength=400,
                           justify="left", fg="#189AB4")
        detailE.place(relx=0.01, rely=.2)

        # button appeler/racrocher
        buttonsFrame = tk.Frame(self.containerFrame, width=400, height=80, bg=BG)
        buttonsFrame.place(relx=.5, rely=.95, anchor="center")
        buttonAppel = tk.Button(buttonsFrame, text="Appel", font=("Helveltica", 20), width=10, bg="#5FD068",
                                activebackground="#4B8673", fg='#189AB4')
        buttonAppel.grid(column=0, row=1, padx=10, pady=10)
        buttonAppel.config(command=lambda: self.appelAction(numeroEntreprise))
        buttonRacrocher = tk.Button(buttonsFrame, text="Racrocher", font=('Helveltica', 20), width=10, bg='#FF8C8C',
                                    activebackground='#FF5D5D', fg='#189AB4')
        buttonRacrocher.grid(column=1, row=1, padx=10, pady=10)
        buttonRacrocher.config(command=lambda: self.racrocherAction())

    def appelAction(self, numero):
        print("Appel a", numero)

    def racrocherAction(self):
        print("Racrocher l'appel")

    def autoGeneratePage(self,logo_entreprise, name_entreprise, detail_entreprise, num_entreprise):
        def page(self):
            logoEntreprise = logo_entreprise
            nomEntreprise = name_entreprise
            detailEntreprise = detail_entreprise
            numeroEntreprise = num_entreprise
            # header
            self.logoCanvas = tk.Canvas(self.containerFrame, bg=BG, height=130, width=200, highlightthickness=0)
            self.logoCanvas.place(relx=.5, rely=.1, anchor="center")
            self.l = PIL.ImageTk.PhotoImage(Image.open(logoEntreprise))
            self.logo = self.logoCanvas.create_image(100, 130 / 2, image=self.l)

            # Detail de l'entreprise
            detailFrame = tk.Frame(self.containerFrame, width=400, height=350, highlightthickness=0, bg=BG)
            detailFrame.place(relx=.5, rely=.54, anchor="center")
            nameE = tk.Label(detailFrame, text=nomEntreprise, font=("Helveltica", 20), bg=BG, fg="#05445E")
            nameE.place(relx=0.01, rely=0.01)
            detailE = tk.Label(detailFrame, font=("Helveltica", 15), text=detailEntreprise, bg=BG, wraplength=400,
                               justify="left", fg="#189AB4")
            detailE.place(relx=0.01, rely=.2)

            # button appeler/racrocher
            buttonsFrame = tk.Frame(self.containerFrame, width=400, height=80, bg=BG)
            buttonsFrame.place(relx=.5, rely=.95, anchor="center")
            buttonAppel = tk.Button(buttonsFrame, text="Appel", font=("Helveltica", 20), width=10, bg="#5FD068",
                                    activebackground="#4B8673", fg='#189AB4')
            buttonAppel.grid(column=0, row=1, padx=10, pady=10)
            buttonAppel.config(command=lambda: self.appelAction(numeroEntreprise))
            buttonRacrocher = tk.Button(buttonsFrame, text="Racrocher", font=('Helveltica', 20), width=10, bg='#FF8C8C',
                                        activebackground='#FF5D5D', fg='#189AB4')
            buttonRacrocher.grid(column=1, row=1, padx=10, pady=10)
            buttonRacrocher.config(command=lambda: self.racrocherAction())
        self.pages.append(lambda: page(self))

app = AppGUI()
