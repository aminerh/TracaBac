
# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from modules import *
from widgets import *



# from widgets import *
os.environ["QT_FONT_DPI"] = Settings.DPI #96 FIX Problem for High DPI and Scale above 100%

# SET AS GLOBAL WIDGETS
# ///////////////////////////////////////////////////////////////
widgets = None

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        # setting the reflex connection object 
        self.RefConenctor = ReflexConenctor()

        self.Dataframe = pd.DataFrame()
        # SET AS GLOBAL WIDGETS
        # ///////////////////////////////////////////////////////////////
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui

        # USE CUSTOM TITLE BAR | USE AS "False" FOR MAC OR LINUX
        # ///////////////////////////////////////////////////////////////
        Settings.ENABLE_CUSTOM_TITLE_BAR = True

        # APP NAME
        # ///////////////////////////////////////////////////////////////
        title = "Solvix Traca Bac"
       
        # APPLY TEXTS
        self.setWindowTitle(title)
       

        # TOGGLE MENU
        # ///////////////////////////////////////////////////////////////
        widgets.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))

        # SET UI DEFINITIONS
        # ///////////////////////////////////////////////////////////////
        UIFunctions.uiDefinitions(self)

        # QTableWidget PARAMETERS
        # ///////////////////////////////////////////////////////////////
        widgets.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # BUTTONS CLICK
        # ///////////////////////////////////////////////////////////////

        # LEFT MENUS
        widgets.btn_home.clicked.connect(self.buttonClick)
     
        widgets.btn_login.clicked.connect(self.buttonClick)
       
        # login funtion to btn
        widgets.login_button.clicked.connect(self.login)
        

        #refresh function to btn
        # widgets.refresh.clicked.connect(self.RefreshTraca)

        #logout function to btn
        widgets.btn_logout.clicked.connect(self.logout)

     
        widgets.refresh.clicked.connect(self.buttonClick)


        #add function to print button   
        widgets.btn_print.clicked.connect(self.printCurrentData)
                
        widgets.cptFilter.currentIndexChanged.connect(self.filter_data)
      
        widgets.searchTSX.clicked.connect(self.filter_data_tsx)
        widgets.searchValue.returnPressed.connect(self.filter_data_tsx)


        #Enter commands 
        widgets.password.returnPressed.connect(self.login)
        widgets.username.returnPressed.connect(self.login)



        # EXTRA RIGHT BOX
        def openCloseRightBox():
            UIFunctions.toggleRightBox(self, True)
        widgets.settingsTopBtn.clicked.connect(openCloseRightBox)

        # SHOW APP
        # ///////////////////////////////////////////////////////////////
        self.show()

        # SET HOME PAGE AND SELECT MENU
        # ///////////////////////////////////////////////////////////////
        widgets.stackedWidget.setCurrentWidget(widgets.login)
        widgets.btn_login.setStyleSheet(UIFunctions.selectMenu(widgets.btn_login.styleSheet()))
        widgets.btn_home.setVisible(False)
       

    # BUTTONS CLICK
    # Post here your functions for clicked buttons
    # ///////////////////////////////////////////////////////////////
    def buttonClick(self):
        # GET BUTTON CLICKED
        btn = self.sender()
        btnName = btn.objectName()

        # SHOW HOME PAGE
        if btnName == "btn_home":
            widgets.stackedWidget.setCurrentWidget(widgets.home)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))
            
           
        # SHOW WIDGETS PAGE
        if btnName == "btn_widgets":
            widgets.stackedWidget.setCurrentWidget(widgets.widgets)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW NEW PAGE
        if btnName == "btn_login" :
            widgets.stackedWidget.setCurrentWidget(widgets.login) # SET PAGE
            UIFunctions.resetStyle(self, btnName) # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet())) # SELECT MENU
        

       # btn search surplus
        if btnName == "refresh" :
            self.getTRacaBAC()
        
        
       
   

    # RESIZE EVENTS
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        # Update Size Grips
        UIFunctions.resize_grips(self)

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()

        # PRINT MOUSE EVENTS
        if event.buttons() == Qt.LeftButton:
            print('Mouse click: LEFT CLICK')
        if event.buttons() == Qt.RightButton:
            print('Mouse click: RIGHT CLICK')



    def login(self):
        btn = self.sender()
        btnName = btn.objectName()

        username = widgets.username.text()
        password = widgets.password.text()
        User.REFUSER=username
        User.REFPWD=password
        if len(username) != 8:
            toast = Toast(self)
            toast.setDuration(5000)  # Hide after 5 seconds
            toast.setTitle('Erreur ! R520 ou mot de passe incorrecte ')
            toast.applyPreset(ToastPreset.ERROR)  # Apply style preset
            toast.setBackgroundColor(QColor('#282C34'))
            toast.setTitleColor(QColor('#FFFFFF'))
            toast.setDurationBarColor(QColor('#F39E4E'))
            toast.setIconColor(QColor('#F39E4E'))
            toast.setIconSeparatorColor(QColor('#F39E4E'))
            toast.setCloseButtonIconColor(QColor('#F39E4E'))
            toast.show()            
            return 

        if btnName == "login_button":
            print("connection btn clicked")
            
            if self.RefConenctor.connect() : 
                self.getTRacaBAC()
                UIFunctions.getuserinfo(self)
                # self.GetBDD_Surplus()
                widgets.UserInfo.setText(User.REFFULLNAME)
                widgets.btn_home.setVisible(True)
             
                widgets.btn_login.setVisible(False)
                widgets.stackedWidget.setCurrentWidget(widgets.home) # SET PAGE
                widgets.btn_home.setStyleSheet(UIFunctions.selectMenu(widgets.btn_home.styleSheet()))
                toast = Toast(self)
                toast.setDuration(5000)  # Hide after 5 seconds
                toast.setTitle('Succès ! Bienvenue '+ User.REFFULLNAME)
                toast.applyPreset(ToastPreset.SUCCESS)  # Apply style preset
                toast.setBackgroundColor(QColor('#282C34'))
                toast.setTitleColor(QColor('#FFFFFF'))
                toast.setDurationBarColor(QColor('#F39E4E'))
                toast.setIconColor(QColor('#F39E4E'))
                toast.setIconSeparatorColor(QColor('#F39E4E'))
                toast.setCloseButtonIconColor(QColor('#F39E4E'))
                toast.show()
            else : 
                toast = Toast(self)
                toast.setDuration(5000)  # Hide after 5 seconds
                toast.setTitle('Erreur ! R520 ou mot de passe incorrecte ')
                toast.applyPreset(ToastPreset.ERROR)  # Apply style preset
                toast.setBackgroundColor(QColor('#282C34'))
                toast.setTitleColor(QColor('#FFFFFF'))
                toast.setDurationBarColor(QColor('#F39E4E'))
                toast.setIconColor(QColor('#F39E4E'))
                toast.setIconSeparatorColor(QColor('#F39E4E'))
                toast.setCloseButtonIconColor(QColor('#F39E4E'))
                toast.show()


    def getTRacaBAC(self):

        df = UIFunctions.getStatusBac(self)

        min_cpt_df = df.groupby(['BAC', 'Type', 'Support Reflex', 'Emplacement', 'Fermeture du bac'])['CPT'].min().reset_index()
        min_cpt_df = min_cpt_df.rename(columns={'CPT': 'Min_CPT'})


        idx = df.groupby(['BAC', 'Type', 'Support Reflex', 'Emplacement', 'Fermeture du bac'])['PVHVPR'].idxmax()
        max_pvhvpr_df = df.loc[idx, ['BAC', 'Type', 'Support Reflex', 'Emplacement', 'Fermeture du bac', 'Utilisateur', 'ASIN', 'EMP_LPICK', 'PVHVPR']]

        result_df = pd.merge(min_cpt_df, max_pvhvpr_df, on=['BAC', 'Type', 'Support Reflex', 'Emplacement', 'Fermeture du bac'])

        result_df['Fermeture du bac'] = pd.to_datetime(result_df['Fermeture du bac'], errors='coerce')

        now = datetime.now()
        result_df["Etat"] = result_df["Fermeture du bac"].apply(
            lambda x: "Bac éventuellement perdu" if pd.notnull(x) and x < now - timedelta(minutes=60) else "Pas de risque"
        )

        # Step 5: Rename columns for final output
        df_merged = result_df.rename(columns={"EMP_LPICK": "Dernier Emp Pick"})
        df_merged = df_merged.rename(columns={"Min_CPT": "CPT"})
        df_merged = df_merged.drop(columns=["PVHVPR"])
        
        self.Dataframe=df_merged.sort_values(by="CPT", ascending=True)
        
        widgets.cptFilter.clear()

        widgets.cptFilter.addItem("Sélectionner tout")

        widgets.cptFilter.addItems(df_merged["CPT"].unique())

        self.load_data(df_merged)
       
                
    def filter_data(self):
             
        selected_category = widgets.cptFilter.currentText()

        if selected_category == "Sélectionner tout":
            filtered_df =  self.Dataframe  # Show all data
        else:
            filtered_df =  self.Dataframe[ self.Dataframe['CPT'] == selected_category]  # Filter data by selected category

        self.load_data(filtered_df)


    def filter_data_tsx(self):
             
        searchedTSXbac = widgets.searchValue.text()
    
        df = self.Dataframe
        if df is not None and not df.empty:
            # Apply filter only if the 'filtre' parameter is not empty
            if searchedTSXbac.strip():  # .strip() removes any leading/trailing whitespace
                df = df[
                    (df['BAC'].str.contains(searchedTSXbac, case=False, na=False)) |
                    (df['Support Reflex'].str.contains(searchedTSXbac, case=False, na=False))
                ]
                if not df.empty : 
                    self.load_data(df)
              
                else:    
                    print("tsx or support not found")
            elif searchedTSXbac=="" :
                self.load_data(self.Dataframe)


        


    def load_data(self, data_frame):
        red_brush = QBrush(QColor(255, 0, 0)) 
        widgets.TracaBac.clear()
        
        if data_frame is not None and not data_frame.empty:
            # Set the number of rows and columns
            widgets.TracaBac.setRowCount(len(data_frame))
            widgets.TracaBac.setColumnCount(len(data_frame.columns))
            widgets.TracaBac.setHorizontalHeaderLabels(data_frame.columns.tolist())

            for row in range(len(data_frame)):
                for col in range(len(data_frame.columns)):
                    item = QTableWidgetItem(str(data_frame.iat[row, col]))
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    widgets.TracaBac.setItem(row, col, item)
                    etat = str(data_frame.iat[row, len(data_frame.columns)-1])
           
                    if "Bac éventuellement perdu" in etat :
                        widgets.TracaBac.item(row, col).setBackground(red_brush)         

    def logout(self):
        btn = self.sender()
        btnName = btn.objectName()
     
        if btnName == "btn_logout":
            widgets.username.setText("")
            widgets.password.setText("")
            User.REFUSER=''
            User.REFPWD=''
            User.REFFULLNAME=''
            widgets.TracaBac.clear()
            widgets.stackedWidget.setCurrentWidget(widgets.login)
            widgets.btn_home.setVisible(False)
            widgets.btn_login.setVisible(True)
            widgets.btn_login.setStyleSheet(UIFunctions.selectMenu(widgets.btn_login.styleSheet()))


    def get_table_data(self, table_widget):

        row_count = table_widget.rowCount()
        col_count = table_widget.columnCount()

        data = {}
        for col in range(col_count):
            header = table_widget.horizontalHeaderItem(col).text()
            data[header] = []
            for row in range(row_count):
                item = table_widget.item(row, col)
                data[header].append(item.text() if item else '')

        return pd.DataFrame(data)
    
    def printCurrentData(self):
        current_index = widgets.stackedWidget.currentIndex()
        print(current_index)
        if current_index == 1:
            print("TRACA Data:")
            df =self.get_table_data(widgets.TracaBac)
            df.to_excel("TracabiliteBAC.xlsx", index=False)
            toast = Toast(self)
            toast.setDuration(5000)  # Hide after 5 seconds
            toast.setTitle('Fichier TracabiliteBAC.xlsx a été télécharger')
            toast.setPosition(ToastPosition.TOP_RIGHT)  # Default: ToastPosition.BOTTOM_RIGHT
            toast.applyPreset(ToastPreset.SUCCESS)  # Apply style preset
            toast.setBackgroundColor(QColor('#282C34'))
            toast.setTitleColor(QColor('#FFFFFF'))
            toast.setDurationBarColor(QColor('#F39E4E'))
            toast.setIconColor(QColor('#F39E4E'))
            toast.setIconSeparatorColor(QColor('#F39E4E'))
            toast.setCloseButtonIconColor(QColor('#F39E4E'))
            toast.show()


        
        else :
            toast = Toast(self)
            toast.setDuration(5000)  # Hide after 5 seconds
            toast.setTitle('Aucune donnée disponible pour le téléchargement')
            toast.setPosition(ToastPosition.TOP_RIGHT)  # Default: ToastPosition.BOTTOM_RIGHT
            toast.applyPreset(ToastPreset.ERROR)  # Apply style preset
            toast.setBackgroundColor(QColor('#282C34'))
            toast.setTitleColor(QColor('#FFFFFF'))
            toast.setDurationBarColor(QColor('#F39E4E'))
            toast.setIconColor(QColor('#F39E4E'))
            toast.setIconSeparatorColor(QColor('#F39E4E'))
            toast.setCloseButtonIconColor(QColor('#F39E4E'))
            toast.show()



                
        
  

           



if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()
    sys.exit(app.exec())
