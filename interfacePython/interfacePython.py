"""
Nome: Interface Serial com Salvamento em SqLite3
Data: 11/08/2019
Objetivo: Tratar dados enviados na Porta Serial e salva-los em um banco SqLite3
"""

import serial
import sys
import glob

import sqlite3
import time
import datetime


class InterfaceSerial():
    def conectar(porta, velocidade):
        conexao = serial.Serial(porta,velocidade)#Abertura de conexão serial
        return conexao

    def serial_ports():
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Sistema não suportado')

        port_list = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                port_list.append(port)
            except (OSError, serial.SerialException):
                pass
        return port_list

class BancoDeDados():
    def conect_db(bd_name):#Criação da conexão do banco de dados
        connection = sqlite3.connect(bd_name) #Inicia uma conexão com o banco e cria caso não exista
        return connection
    
    def create_cursor(connection):
        cursor = connection.cursor() #cursor de ações do banco de dados
        return cursor
     
    def create_table(cursor, tbl_name): #Para criar uma tabela caso não exista
        cursor.execute("CREATE TABLE IF NOT EXISTS " + tbl_name + " (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, dado text, data text)")
         
    def data_save(cursor, tbl_name, dado, data):  #Para inserir dados na tabela       
        sql = "INSERT INTO " + tbl_name + "(dado, data) VALUES ('"+dado+"','"+data+"')"   
        cursor.execute(sql)
        connection.commit()

    

if __name__ == '__main__':
    while(1): #Loop de Inserção de Dados
        print("Qual porta você deseja conectar?")
        port = input("Tecle '?' para ver a lista de portas disponíveis \n")       

        if(port == "?"): #Printar todas as portas disponíveis
            ports = InterfaceSerial.serial_ports()
            if(ports):
                print("Portas Disponíveis: ")
                for port in ports:
                    print(port)
                print("\n")
            else:
                print("Nenhuma porta encontrada!")
                print("\n"*2)

        else: #Tentar conexão com a porta selecionada
            velocidade = input("Qual é a velocidade (BaudRate) empregada? \n")
            print("\n")
            baud_rate = ["110", 
                                "300", 
                                "600", 
                                "1200", 
                                "2400", 
                                "4800", 
                                "9600", 
                                "14400", 
                                "19200", 
                                "38400", 
                                "57600", 
                                "115200", 
                                "128000", 
                                "256000"]

            if(velocidade in baud_rate):
                conexao = InterfaceSerial.conectar(port,velocidade) #Conexão Serial
                conexao.flushInput() #Limpar Entrada
                conexao.flushOutput() #Limpar Saída                

                while(conexao):

                    dado_recebido=str(conexao.readline().decode('ascii')) #Leitura da porta Serial

                    if(dado_recebido != 0):                
                        connection = BancoDeDados.conect_db("registros.db")
                        cursor = BancoDeDados.create_cursor(connection)

                        data = str(datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S')) #Data do registro

                        BancoDeDados.create_table(cursor, "water_detect")
                        BancoDeDados.data_save(cursor, "water_detect", dado_recebido, data) #Salvamento dos dados
                        
                        connection.close() #Encerra a conexão com o Bnaoc de Dados
                        print("Registro " + dado_recebido + " inserido às: " + data)
                    
                time.sleep(.1) #Delay de 100ms             
            else:
                print("Velocidade não suportada")
                print("\n")


                