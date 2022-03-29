# Gerador de planilhas
#
# By: Victor Vasconcelos
#
import os
import time
from PyQt5 import uic, QtWidgets, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from Conection import *

from PyQt5.QtWidgets import *


def changeColor():
    css= """
        #progressBar{
    
        border_style: solid;
        border-color: grey;
        border-radius:7px;
        border-width:2px;
        text-align:center;	
        
        
    }
    
    #progressBar::chunk{
        width:5px;
        margin: 5px;
        background-color:rgb(0, 170, 0)
    }
    """
    main.progressBar.setStyleSheet(css)


class Planilha:

    def __init__(self):

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Ui/pasta-.icon.ico"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        main.setWindowIcon(icon)
        main.setWindowTitle('Gerador de Planilhas')
        main.btn_gerar.setIcon(QIcon('Ui/pasta.png'))

        main.show()


    def saveFile(self):
        main.progressBar.setValue(0)
        css = """
                        #progressBar{

                        border_style: solid;
                        border-color: grey;
                        border-radius:7px;
                        border-width:2px;
                        text-align:center;	


                    }

                    #progressBar::chunk{
                        width:5px;
                        margin: 5px;
                        background-color:rgb(255, 255, 57)
                    }
                    """
        main.progressBar.setStyleSheet(css)
        sector = main.setor.text()
        area = main.area.text()
        print(area, sector)
        if area != '' and sector !='':
            sql_update = f"""begin transaction;
                                delete from stage.consulta where setor = {sector}; 
                                insert into stage.consulta(
                                     numero_porta, complemento, nome_proprietario, unidade_id, setor, geom, cpf, quadra, lote, lote_id, area_trabalho)
                                select u.numero, u.complemento, c.nome, u.ctiid, u.setor_id,u.geom,
                                right(cpf, 4) as cpf, lpad(quadra::text,4,'0') as quadra, lpad(l.lote,4,'0') as lote ,u.lote_id, u.area_trabalho
                                from cadastro.unidade u
                                join cadastro.contribuinte c on c.ctgid = u.ctictgid
                                join cadastro.lote l on l.id = u.lote_id where u.setor_id = {sector};
                                commit;"""

            commit(sql_update)

            sql = f"""select quadra, numero,
                             complemento,nome,
                              cpf, setor_id,
                               lote_id, area_trabalho 
                                from stage.vw_planilha_campo where setor_id = {sector} and area_trabalho ={area}"""

            result = query(sql)

            """
            Create File
            """

            try:


                path = QFileDialog.getSaveFileName(main.btn_gerar, "Salvar", "Desktop\\")
                #path2 = QFileDialog.getExistingDirectory(main.btn_gerar,"Salvar", "Desktop\\" )
                print(path)
                if not os.path.exists(path[0]):
                     os.makedirs(f'{path[0]}/Setor_{sector}/Area_{area}')

                cont=0
                for linha in result:
                    cont+= 0.020
                    main.progressBar.setValue(int(cont))
                    if cont>= 60:
                        changeColor()
                    with open(
                              f'{path[0]}/Setor_{sector}/Area_{area}/setor_{sector}_quadra_{linha[0]}-Area_{area}.csv', 'a+', encoding='utf-8') as documento:
                          print(f'{str(linha[0])}, {str(linha[1])},{str(linha[2])}, {str(linha[3])}, {str(linha[4])}, {str(linha[5])},{str(linha[6])}',file=documento)
                          print(str(linha[6]))
                print(path)
                main.progressBar.setValue(100)



            except Exception as e:
                print(e)

        else:
            QMessageBox. about(None, "Erro!!", "Você esqueceu de digitar os campos :(" )
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    main = uic.loadUi("Ui/Cordenadorcampo.ui")
    Planilha()
    main.btn_gerar.clicked.connect(Planilha.saveFile)
    app.exec()