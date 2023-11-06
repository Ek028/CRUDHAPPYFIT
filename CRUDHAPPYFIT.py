from tkinter import *
from tkinter import ttk
import sqlite3

root = Tk()

class Funcs():
    def limpa_cliente(self):
        self.codigo_entry.delete(0, END)
        self.nome_entry.delete(0, END)
        self.idade_entry.delete(0, END)
        self.altura_entry.delete(0, END)
        self.endereco_entry.delete(0, END)
        self.tel_entry.delete(0, END)
        self.funcao_entry.delete(0, END)
        self.sexo_entry.delete(0, END)
    def conecta_bd(self):
        self.conn = sqlite3.connect("clientes.db")
        self.cursor = self.conn.cursor(); print("Conectando ao banco de dados")
    def desconecta_bd(self):
        self.conn.close(); print("Desconectando ao banco de dados")
    def montaTabelas(self):
        self.conecta_bd()
        ### Criar tabela
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                cod INTEGER PRIMARY KEY,
                nome_cliente CHAR(40) NOT NULL,
                endereco CHAR(40),
                tel INTEGER(40),
                altura INTEGER(40),
                sexo CHAR(20),
                idade INTEGER(40),
                funcao CHAR(40)                
            );
        """)
        self.conn.commit(); print("Banco de dados criado")
        self.desconecta_bd()

    def variaveis(self):
        self.codigo = self.codigo_entry.get()
        self.nome = self.nome_entry.get()
        self.endereco = self.endereco_entry.get()
        self.idade = self.idade_entry.get()
        self.altura = self.altura_entry.get()
        self.tel = self.tel_entry.get()
        self.funcao = self.funcao_entry.get()
        self.sexo = self.sexo_entry.get()
    def OnDoubleClick(self, event):
        self.limpa_cliente()
        self.listaCli.selection()

        for n in self.listaCli.selection():
            col1, col2, col3, col4, col5, col6, col7, col8 = self.listaCli.item(n, 'values')
            self.codigo_entry.insert(END, col1)
            self.nome_entry.insert(END, col2)
            self.endereco_entry.insert(END, col3)
            self.tel_entry.insert(END, col4)
            self.altura_entry.insert(END, col5)
            self.sexo_entry.insert(END, col6)
            self.idade_entry.insert(END, col7)
            self.funcao_entry.insert(END, col8)

    def add_cliente(self):
        self.variaveis()
        self.conecta_bd()

        self.cursor.execute(""" INSERT INTO clientes (nome_cliente, endereco, tel, altura, sexo, idade, funcao)
            VALUES (?, ?, ?, ?, ?, ?, ?)""", (self.nome, self.endereco, self.tel, self.altura, self.sexo, self.idade, self.funcao))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_cliente()
    def altera_cliente(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute(""" UPDATE clientes SET nome_cliente = ?, endereco = ?, tel = ?, altura = ?, sexo = ?, idade = ?, funcao = ?
            WHERE cod = ? """,
                            (self.nome, self.endereco, self.tel, self.altura, self.sexo, self.idade, self.funcao, self.codigo))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_cliente()
    def deleta_cliente(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute("""DELETE FROM clientes WHERE cod = ? """, (self.codigo))
        self.conn.commit()
        self.desconecta_bd()
        self.limpa_cliente()
        self.select_lista()

    def select_lista(self):
        self.listaCli.delete(*self.listaCli.get_children())
        self.conecta_bd()
        lista = self.cursor.execute(""" SELECT cod, nome_cliente, endereco, tel, altura, sexo, idade, funcao FROM clientes
            ORDER BY nome_cliente ASC; """)
        for i in lista:
            self.listaCli.insert("", END, values=i)
        self.desconecta_bd()


class Application(Funcs):
    def __init__(self):
        self.root = root
        self.tela()
        self.frames_da_tela()
        self.widgets_frame1()
        self.lista_frame2()
        self.montaTabelas()
        self.select_lista()
        root.mainloop()
    def tela(self):
        self.root.title("Cadastro de Clientes")
        self.root.configure(background= '#1e3743')
        self.root.geometry("700x500")
        self.root.resizable(True, True)
        self.root.maxsize(width= 900, height= 700)
        self.root.minsize(width=500, height= 400)
    def frames_da_tela(self):
        self.frame_1 = Frame(self.root, bd = 4, bg= '#dfe3ee',
                             highlightbackground= '#759fe6', highlightthickness=3 )
        self.frame_1.place(relx= 0.02, rely=0.02, relwidth= 0.96, relheight= 0.46)

        self.frame_2 = Frame(self.root, bd=4, bg='#dfe3ee',
                             highlightbackground='#759fe6', highlightthickness=3)
        self.frame_2.place(relx=0.02, rely=0.5, relwidth=0.96, relheight=0.46)
    def widgets_frame1(self):
        ### Criação do botao limpar
        self.bt_limpar = Button(self.frame_1, text= "Limpar", bd=2, bg = '#107db2',fg = 'white'
                                , font = ('verdana', 8, 'bold'), command= self.limpa_cliente)
        self.bt_limpar.place(relx= 0.9, rely=0.0, relwidth=0.1, relheight= 0.15)
        ### Criação do botao buscar
        self.bt_buscar = Button(self.frame_1, text="Buscar", bd=2, bg = '#107db2',fg = 'white'
                                , font = ('verdana', 8, 'bold'))
        self.bt_buscar.place(relx=0.9, rely=0.2, relwidth=0.1, relheight=0.15)
        ### Criação do botao novo
        self.bt_novo = Button(self.frame_1, text="Novo", bd=2, bg = '#107db2',fg = 'white'
                                , font = ('verdana', 8, 'bold'), command= self.add_cliente)
        self.bt_novo.place(relx=0.9, rely=0.4, relwidth=0.1, relheight=0.15)
        ### Criação do botao alterar
        self.bt_alterar = Button(self.frame_1, text="Alterar", bd=2, bg = '#107db2',fg = 'white'
                                , font = ('verdana', 8, 'bold'), command=self.altera_cliente)
        self.bt_alterar.place(relx=0.9, rely=0.6, relwidth=0.1, relheight=0.15)
        ### Criação do botao apagar
        self.bt_apagar = Button(self.frame_1, text="Apagar", bd=2, bg = '#107db2',fg = 'white'
                                , font = ('verdana', 8, 'bold'), command=self.deleta_cliente)
        self.bt_apagar.place(relx=0.9, rely=0.8, relwidth=0.1, relheight=0.15)

        ## Criação da label e entrada do codigo
        self.lb_codigo = Label(self.frame_1, text = "Código", bg= '#dfe3ee', fg = '#107db2')
        self.lb_codigo.place(relx= 0.05, rely= 0.05 )

        self.codigo_entry = Entry(self.frame_1 )
        self.codigo_entry.place(relx= 0.05, rely= 0.15, relwidth= 0.08)

        ## Criação da label e entrada do nome
        self.lb_nome = Label(self.frame_1, text="Nome", bg='#dfe3ee', fg='#107db2')
        self.lb_nome.place(relx=0.05, rely=0.25)

        self.nome_entry = Entry(self.frame_1)
        self.nome_entry.place(relx=0.05, rely=0.35, relwidth=0.5)

        ## Criação da label e Idade
        self.lb_idade = Label(self.frame_1, text="Idade", bg='#dfe3ee', fg='#107db2')
        self.lb_idade.place(relx=0.2, rely=0.05)

        self.idade_entry = Entry(self.frame_1)
        self.idade_entry.place(relx=0.2, rely=0.15, relwidth=0.09)

        ## Criação da label altura
        self.lb_altura = Label(self.frame_1, text="Altura", bg='#dfe3ee', fg='#107db2')
        self.lb_altura.place(relx=0.4, rely=0.05)
        self.lb_altura = Label(self.frame_1, text="Ex: 1.75", bg='#dfe3ee', fg='#107db2')
        self.lb_altura.place(relx=0.5, rely=0.15)

        self.altura_entry = Entry(self.frame_1)
        self.altura_entry.place(relx=0.4, rely=0.15, relwidth=0.1)

        ## Criação da label e Endereço
        self.lb_endereco = Label(self.frame_1, text="Endereço", bg='#dfe3ee', fg='#107db2')
        self.lb_endereco.place(relx=0.05, rely=0.45)

        self.endereco_entry = Entry(self.frame_1)
        self.endereco_entry.place(relx=0.05, rely=0.55, relwidth=0.5)

        ## Criação da label Telefone
        self.lb_tel = Label(self.frame_1, text="Telefone", bg='#dfe3ee', fg='#107db2')
        self.lb_tel.place(relx=0.05, rely=0.65)

        self.tel_entry = Entry(self.frame_1)
        self.tel_entry.place(relx=0.05, rely=0.75, relwidth=0.2)

        ## Criação da label Posiçao
        self.lb_funcao = Label(self.frame_1, text="Aluno ou Professor", bg='#dfe3ee', fg='#107db2')
        self.lb_funcao.place(relx=0.3, rely=0.65)

        self.funcao_entry = Entry(self.frame_1)
        self.funcao_entry.place(relx=0.3, rely=0.75, relwidth=0.1)

        ## Criação da label Sexo
        self.lb_sexo = Label(self.frame_1, text="Sexo", bg='#dfe3ee', fg='#107db2')
        self.lb_sexo.place(relx=0.5, rely=0.65)
        self.lb_sexo = Label(self.frame_1, text="M=Masculino ou F=Feminino", bg='#dfe3ee', fg='#107db2')
        self.lb_sexo.place(relx=0.6, rely=0.75)

        self.sexo_entry = Entry(self.frame_1)
        self.sexo_entry.place(relx=0.5, rely=0.75, relwidth=0.1)


    def lista_frame2(self):
        self.listaCli = ttk.Treeview(self.frame_2, height=3,
                                     column=("col1", "col2", "col3", "col4", "col5", "col6", "col7", "col8"))
        self.listaCli.heading("#0", text="")
        self.listaCli.heading("#1", text="Cod")
        self.listaCli.heading("#2", text="nome")
        self.listaCli.heading("#3", text="Endereço")
        self.listaCli.heading("#4", text="Tel")
        self.listaCli.heading("#5", text="Altura")
        self.listaCli.heading("#6", text="Sexo")
        self.listaCli.heading("#7", text="Idade")
        self.listaCli.heading("#8", text="Funçao")
        self.listaCli.column("#0", width=1)
        self.listaCli.column("#1", width=30)
        self.listaCli.column("#2", width=125)
        self.listaCli.column("#3", width=125)
        self.listaCli.column("#4", width=50)
        self.listaCli.column("#5", width=30)
        self.listaCli.column("#6", width=30)
        self.listaCli.column("#7", width=30)
        self.listaCli.column("#8", width=40)
        self.listaCli.place(relx=0.01, rely=0.1, relwidth=0.95, relheight=0.85)

        self.scroolLista = Scrollbar(self.frame_2, orient='vertical')
        self.listaCli.configure(yscroll=self.scroolLista.set)
        self.scroolLista.place(relx=0.96, rely=0.1, relwidth=0.04, relheight=0.85)
        self.listaCli.bind("<Double-1>", self.OnDoubleClick)



Application()