from datetime import datetime
import pyodbc
from sqlalchemy import create_engine, text

class User():
    REFUSER=""
    REFPWD=""
    REFFULLNAME =""

class ReflexConenctor():
    ReflexConn = None
    ReflexCursor = None  
    def __init__(self) :
        self.ReflexConn = None
        self.ReflexCursor = None  
    def connect(self):
        try:
            self.ReflexConn = pyodbc.connect(
                    'DRIVER={iSeries Access ODBC Driver};'
                    f'SYSTEM=TDCRFX52;'
                    f'UID={User.REFUSER};' # to replace with inputs 
                    f'PWD={User.REFPWD}'  # Remplace par ton mot de passe
            )
            self.ReflexCursor = self.ReflexConn.cursor()
            return 1
        except Exception as error:
            print(f"Error while connecting to REFLEX: {error}")
            return 0


class Settings():
    # APP SETTINGS
    # ///////////////////////////////////////////////////////////////

    DPI ="96"

    ENABLE_CUSTOM_TITLE_BAR = True
    MENU_WIDTH = 240
    LEFT_BOX_WIDTH = 240
    RIGHT_BOX_WIDTH = 240
    TIME_ANIMATION = 500

    # BTNS LEFT AND RIGHT BOX COLORS
    BTN_LEFT_BOX_COLOR = "background-color: rgb(44, 49, 58);"
    BTN_RIGHT_BOX_COLOR = "background-color: rgb(243, 158, 78) ;"

    # MENU SELECTED STYLESHEET
    MENU_SELECTED_STYLESHEET = """
    background-color: rgb(243, 158, 78);
    """

   


    current_date = datetime.now().strftime('%Y-%m-%d')

    #  ' loc AS "Emplacement avec quantité",
    #  ' qty AS "Quantité sans prélèvement" ,
    #   npcmnp AS "Reason Code",
    

  
    TRACA_BAC = """SELECT  ARNBAC  AS "BAC",
        OECMOP AS "Type",                                           
        DIGITS(GENSUP) AS "Support Reflex",                                
        EMC1EM CONCAT ' ' CONCAT EMC2EM CONCAT ' ' CONCAT EMC3EM CONCAT ' '
        CONCAT EMC4EM CONCAT ' ' CONCAT EMC5EM AS "Emplacement",           
        TO_TIMESTAMP(
            SUSPSP CONCAT SUAPSP CONCAT '-' CONCAT SUMPSP CONCAT '-' CONCAT SUJPSP CONCAT ' ' CONCAT
                    CASE
                        WHEN  CHARACTER_LENGTH(SUHPSP) = 5 THEN
                                '0' CONCAT SUBSTR(SUHPSP, 1, 1) CONCAT ':' CONCAT SUBSTR(SUHPSP, 2, 2) CONCAT ':' CONCAT SUBSTR(SUHPSP, 4, 2)
                        WHEN  CHARACTER_LENGTH(SUHPSP) = 6   THEN
                                SUBSTR(SUHPSP, 1, 2) CONCAT ':' CONCAT SUBSTR(SUHPSP, 3, 2) CONCAT ':' CONCAT SUBSTR(SUHPSP, 5, 2)
                    END
            , 'YYYY-MM-DD HH24:MI:SS'
            ) AS "Fermeture du bac",                                      
        TO_TIMESTAMP(
        CONCAT(ORCPOD, CONCAT(' ', ORCPOT )) , 'DD/MM/YYYY HH24:MI:SS'
        ) AS CPT,                                                     
        PREP.PVCUVP AS "Utilisateur",
        PREP.PVCART as "ASIN",
        PREP.PVC1EM CONCAT ' ' CONCAT 
        PREP.PVC2EM CONCAT ' ' CONCAT 
        PREP.PVC3EM CONCAT ' ' CONCAT 
        PREP.PVC4EM CONCAT ' ' CONCAT 
        PREP.PVC5EM AS EMP_LPICK  ,
        PREP.PVHVPR                         
        FROM AMAZONBD.HLPRPLP                                              
        INNER JOIN AMAZONBD.HLODPEP ON OECACT = P1CACT AND OECDPO = P1CDPO 
        AND OENANN = P1NANO AND OENODP = P1NODP                            
        LEFT  JOIN AMAZONBD.HLPLLPP ON PPCACP = P1CACT AND PPCDPP = P1CDPO 
        AND PPNANP = P1NANN AND PPNLPR = P1NLPR       
        LEFT JOIN AMAZONBD.HLPRELP AS PREP  
        ON PVNANN = PPNANN AND PVNPRL = PPNPRL 

        LEFT  JOIN AMAZONBD.HLLPRGP ON LGCACT = P1CACT AND LGCDPO = P1CDPO 
        AND LGNANN = P1NANN AND LGNLPR = P1NLPR
        LEFT  JOIN AMAZONBD.HLGEINP ON GECACT = LGCACT AND GENGEI = LGNGEI
        AND GENAPL = PPNANN AND GENPRL =PPNPRL                         
        LEFT  JOIN AMAZONBD.HLSUPPP ON SUCACT = GECACT AND SUNSUP = GENSUP
        LEFT  JOIN AMAZONBD.HLEMPLP ON EMCDPO = SUCDPO AND EMNEMP = SUNEMP
        LEFT  JOIN AMRFXDD.AICRXRP ON ARNSRX = SUNSUP AND ARTVAL = '1'    
        left  join amrfxdd.aiordep on orrodp = oerodp                     
        where ARNBAC IS NOT NULL   and OECMOP IN('STD','MIT')"""

