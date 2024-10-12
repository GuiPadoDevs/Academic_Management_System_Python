import tkinter as tk
from tkinter import messagebox, ttk
from mysql.connector import connect, Error
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Database:
    def __init__(self):
        self.connection = connect(
            host="localhost",
            user="root",
            password="",
            database="escola"
        )
        self.cursor = self.connection.cursor()

    def close(self):
        self.cursor.close()
        self.connection.close()


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Escola")
        self.geometry("450x350")
        
        tk.Label(self, text="Sistema Escolar", font=("Arial", 16, "bold")).pack(pady=5)
        tk.Label(self, text="ITE", font=("Arial", 16, "bold")).pack(pady=5)

        tk.Button(self, text="Area do professor", command=self.open_professores).pack(pady=5)
        tk.Button(self, text="Area da disciplina", command=self.open_disciplinas).pack(pady=5)
        tk.Button(self, text="Area do aluno", command=self.open_alunos).pack(pady=5)
        tk.Button(self, text="Area das notas", command=self.open_notas).pack(pady=5)
        tk.Button(self, text="Consultar notas dos alunos", command=self.open_consulta_notas).pack(pady=5)
        tk.Button(self, text="Gráfico de médias", command=self.open_grafico).pack(pady=5)

    def open_grafico(self):
        self.new_window(Grafico)

    def open_consulta_notas(self):
        self.new_window(ConsultaNotas)

    def open_professores(self):
        self.new_window(Professores)

    def open_disciplinas(self):
        self.new_window(Disciplinas)

    def open_alunos(self):
        self.new_window(Alunos)

    def open_notas(self):
        self.new_window(Notas)

    def new_window(self, page_class):
        new_page = page_class(self)
        new_page.grab_set()  


class Professores(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Area do professor")
        self.geometry("900x600")

        self.db = Database()

        tk.Label(self, text="ID").pack()
        self.id_entry = tk.Entry(self)
        self.id_entry.pack()

        tk.Label(self, text="Nome").pack()
        self.nome_entry = tk.Entry(self)
        self.nome_entry.pack()

        tk.Label(self, text="Email").pack()
        self.email_entry = tk.Entry(self)
        self.email_entry.pack()

        tk.Label(self, text="Telefone").pack()
        self.telefone_entry = tk.Entry(self)
        self.telefone_entry.pack()

        tk.Button(self, text="Adicionar Professor", command=self.add_professor).pack(pady=5)
        tk.Button(self, text="Alterar Professor", command=self.update_professor).pack(pady=5)
        tk.Button(self, text="Deletar Professor", command=self.delete_professor).pack(pady=5)

        self.professores_list = ttk.Treeview(self, columns=("ID", "Nome", "Email", "Telefone"), show="headings")
        self.professores_list.heading("ID", text="ID")
        self.professores_list.heading("Nome", text="Nome")
        self.professores_list.heading("Email", text="Email")
        self.professores_list.heading("Telefone", text="Telefone")
        self.professores_list.pack(pady=10)
        self.professores_list.bind("<Double-1>", self.on_select)

        self.list_professores()

    def on_select(self, event):
        selected_item = self.professores_list.selection()[0]
        values = self.professores_list.item(selected_item, "values")
        self.id_entry.delete(0, tk.END)
        self.id_entry.insert(0, values[0])
        self.nome_entry.delete(0, tk.END)
        self.nome_entry.insert(0, values[1])
        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(0, values[2])
        self.telefone_entry.delete(0, tk.END)
        self.telefone_entry.insert(0, values[3])

    def add_professor(self):
        nome = self.nome_entry.get()
        email = self.email_entry.get()
        telefone = self.telefone_entry.get()
        if nome and email and telefone:
            try:
                self.db.cursor.execute("INSERT INTO PROFESSORES (NOME, EMAIL, FONE) VALUES (%s, %s, %s)",
                                       (nome, email, telefone))
                self.db.connection.commit()
                messagebox.showinfo("Sucesso", "Professor adicionado com sucesso!")
                self.clear_entries()
                self.list_professores()
            except Error as e:
                messagebox.showerror("Erro", str(e))
        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos.")

    def update_professor(self):
        id_prof = self.id_entry.get()
        nome = self.nome_entry.get()
        email = self.email_entry.get()
        telefone = self.telefone_entry.get()
        if id_prof and nome and email and telefone:
            try:
                self.db.cursor.execute("UPDATE PROFESSORES SET NOME=%s, EMAIL=%s, FONE=%s WHERE ID_PROF=%s",
                                       (nome, email, telefone, id_prof))
                self.db.connection.commit()
                messagebox.showinfo("Sucesso", "Professor alterado com sucesso!")
                self.clear_entries()
                self.list_professores()
            except Error as e:
                messagebox.showerror("Erro", str(e))
        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos.")

    def delete_professor(self):
        id_prof = self.id_entry.get()
        if id_prof:
            try:
                self.db.cursor.execute("DELETE FROM PROFESSORES WHERE ID_PROF=%s", (id_prof,))
                self.db.connection.commit()
                messagebox.showinfo("Sucesso", "Professor deletado com sucesso!")
                self.clear_entries()
                self.list_professores()
            except Error as e:
                messagebox.showerror("Erro", str(e))
        else:
            messagebox.showwarning("Atenção", "Preencha o ID do professor.")

    def list_professores(self):
        for i in self.professores_list.get_children():
            self.professores_list.delete(i)
        self.db.cursor.execute("SELECT * FROM PROFESSORES")
        for row in self.db.cursor.fetchall():
            self.professores_list.insert("", "end", values=row)

    def clear_entries(self):
        self.id_entry.delete(0, tk.END)
        self.nome_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.telefone_entry.delete(0, tk.END)


class Disciplinas(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Area da disciplina")
        self.geometry("900x600")

        self.db = Database()

        tk.Label(self, text="ID").pack()
        self.id_entry = tk.Entry(self)
        self.id_entry.pack()

        tk.Label(self, text="Disciplina").pack()
        self.disciplina_entry = tk.Entry(self)
        self.disciplina_entry.pack()

        tk.Label(self, text="Carga Horária").pack()
        self.carga_horaria_entry = tk.Entry(self)
        self.carga_horaria_entry.pack()

        tk.Label(self, text="Professor").pack()
        self.professores_combobox = ttk.Combobox(self, state="readonly")
        self.professores_combobox.pack()
        self.fill_professores_combobox()

        tk.Button(self, text="Adicionar Disciplina", command=self.add_disciplina).pack(pady=5)
        tk.Button(self, text="Alterar Disciplina", command=self.update_disciplina).pack(pady=5)
        tk.Button(self, text="Deletar Disciplina", command=self.delete_disciplina).pack(pady=5)

        self.disciplinas_list = ttk.Treeview(self, columns=("ID", "Disciplina", "Carga Horária", "Professor"), show="headings")
        self.disciplinas_list.heading("ID", text="ID")
        self.disciplinas_list.heading("Disciplina", text="Disciplina")
        self.disciplinas_list.heading("Carga Horária", text="Carga Horária")
        self.disciplinas_list.heading("Professor", text="Professor")
        self.disciplinas_list.pack(pady=10)
        self.disciplinas_list.bind("<Double-1>", self.on_select)

        self.list_disciplinas()

    def on_select(self, event):
        selected_item = self.disciplinas_list.selection()[0]
        values = self.disciplinas_list.item(selected_item, "values")
        self.id_entry.delete(0, tk.END)
        self.id_entry.insert(0, values[0])
        self.disciplina_entry.delete(0, tk.END)
        self.disciplina_entry.insert(0, values[1])
        self.carga_horaria_entry.delete(0, tk.END)
        self.carga_horaria_entry.insert(0, values[2])
        self.professores_combobox.set(values[3])

    def fill_professores_combobox(self):
        try:
            self.db.cursor.execute("SELECT ID_PROF, NOME FROM PROFESSORES")
            professores = self.db.cursor.fetchall()
            self.professores_combobox["values"] = [f"{prof[0]} - {prof[1]}" for prof in professores]
        except Error as e:
            messagebox.showerror("Erro", str(e))

    def add_disciplina(self):
        disciplina = self.disciplina_entry.get()
        carga_horaria = self.carga_horaria_entry.get()
        id_prof = self.professores_combobox.get().split(" - ")[0]
        if disciplina and carga_horaria and id_prof:
            try:
                self.db.cursor.execute("INSERT INTO DISCIPLINAS (DISCIPLINA, CARGA_HORARIA, ID_PROF_FK) VALUES (%s, %s, %s)",
                                       (disciplina, carga_horaria, id_prof))
                self.db.connection.commit()
                messagebox.showinfo("Sucesso", "Disciplina adicionada com sucesso!")
                self.clear_entries()
                self.list_disciplinas()
            except Error as e:
                messagebox.showerror("Erro", str(e))
        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos.")

    def update_disciplina(self):
        id_disc = self.id_entry.get()
        disciplina = self.disciplina_entry.get()
        carga_horaria = self.carga_horaria_entry.get()
        id_prof = self.professores_combobox.get().split(" - ")[0]
        if id_disc and disciplina and carga_horaria and id_prof:
            try:
                self.db.cursor.execute("UPDATE DISCIPLINAS SET DISCIPLINA=%s, CARGA_HORARIA=%s, ID_PROF_FK=%s WHERE ID_DISCI=%s",
                                       (disciplina, carga_horaria, id_prof, id_disc))
                self.db.connection.commit()
                messagebox.showinfo("Sucesso", "Disciplina alterada com sucesso!")
                self.clear_entries()
                self.list_disciplinas()
            except Error as e:
                messagebox.showerror("Erro", str(e))
        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos.")

    def delete_disciplina(self):
        id_disc = self.id_entry.get()
        if id_disc:
            try:
                self.db.cursor.execute("DELETE FROM DISCIPLINAS WHERE ID_DISCI=%s", (id_disc,))
                self.db.connection.commit()
                messagebox.showinfo("Sucesso", "Disciplina deletada com sucesso!")
                self.clear_entries()
                self.list_disciplinas()
            except Error as e:
                messagebox.showerror("Erro", str(e))
        else:
            messagebox.showwarning("Atenção", "Preencha o ID da disciplina.")

    def list_disciplinas(self):
        for i in self.disciplinas_list.get_children():
            self.disciplinas_list.delete(i)
        self.db.cursor.execute("SELECT D.ID_DISCI, D.DISCIPLINA, D.CARGA_HORARIA, P.NOME FROM DISCIPLINAS D JOIN PROFESSORES P ON D.ID_PROF_FK = P.ID_PROF")
        for row in self.db.cursor.fetchall():
            self.disciplinas_list.insert("", "end", values=row)

    def clear_entries(self):
        self.id_entry.delete(0, tk.END)
        self.disciplina_entry.delete(0, tk.END)
        self.carga_horaria_entry.delete(0, tk.END)
        self.professores_combobox.set("")


class Alunos(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Area do aluno")
        self.geometry("900x600")

        self.db = Database()

        tk.Label(self, text="ID").pack()
        self.id_entry = tk.Entry(self)
        self.id_entry.pack()

        tk.Label(self, text="Nome").pack()
        self.nome_entry = tk.Entry(self)
        self.nome_entry.pack()

        tk.Label(self, text="Email").pack()
        self.email_entry = tk.Entry(self)
        self.email_entry.pack()

        tk.Label(self, text="Telefone").pack()
        self.telefone_entry = tk.Entry(self)
        self.telefone_entry.pack()

        tk.Button(self, text="Adicionar Aluno", command=self.add_aluno).pack(pady=5)
        tk.Button(self, text="Alterar Aluno", command=self.update_aluno).pack(pady=5)
        tk.Button(self, text="Deletar Aluno", command=self.delete_aluno).pack(pady=5)

        self.alunos_list = ttk.Treeview(self, columns=("ID", "Nome", "Email", "Telefone"), show="headings")
        self.alunos_list.heading("ID", text="ID")
        self.alunos_list.heading("Nome", text="Nome")
        self.alunos_list.heading("Email", text="Email")
        self.alunos_list.heading("Telefone", text="Telefone")
        self.alunos_list.pack(pady=10)
        self.alunos_list.bind("<Double-1>", self.on_select)

        self.list_alunos()

    def on_select(self, event):
        selected_item = self.alunos_list.selection()[0]
        values = self.alunos_list.item(selected_item, "values")
        self.id_entry.delete(0, tk.END)
        self.id_entry.insert(0, values[0])
        self.nome_entry.delete(0, tk.END)
        self.nome_entry.insert(0, values[1])
        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(0, values[2])
        self.telefone_entry.delete(0, tk.END)
        self.telefone_entry.insert(0, values[3])

    def add_aluno(self):
        nome = self.nome_entry.get()
        email = self.email_entry.get()
        telefone = self.telefone_entry.get()
        if nome and email and telefone:
            try:
                self.db.cursor.execute("INSERT INTO ALUNOS (NOME, EMAIL, FONE) VALUES (%s, %s, %s)",
                                       (nome, email, telefone))
                self.db.connection.commit()
                messagebox.showinfo("Sucesso", "Aluno adicionado com sucesso!")
                self.clear_entries()
                self.list_alunos()
            except Error as e:
                messagebox.showerror("Erro", str(e))
        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos.")

    def update_aluno(self):
        id_aluno = self.id_entry.get()
        nome = self.nome_entry.get()
        email = self.email_entry.get()
        telefone = self.telefone_entry.get()
        if id_aluno and nome and email and telefone:
            try:
                self.db.cursor.execute("UPDATE ALUNOS SET NOME=%s, EMAIL=%s, FONE=%s WHERE ID_ALUNO=%s",
                                       (nome, email, telefone, id_aluno))
                self.db.connection.commit()
                messagebox.showinfo("Sucesso", "Aluno alterado com sucesso!")
                self.clear_entries()
                self.list_alunos()
            except Error as e:
                messagebox.showerror("Erro", str(e))
        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos.")

    def delete_aluno(self):
        id_aluno = self.id_entry.get()
        if id_aluno:
            try:
                self.db.cursor.execute("DELETE FROM ALUNOS WHERE ID_ALUNO=%s", (id_aluno,))
                self.db.connection.commit()
                messagebox.showinfo("Sucesso", "Aluno deletado com sucesso!")
                self.clear_entries()
                self.list_alunos()
            except Error as e:
                messagebox.showerror("Erro", str(e))
        else:
            messagebox.showwarning("Atenção", "Preencha o ID do aluno.")

    def list_alunos(self):
        for i in self.alunos_list.get_children():
            self.alunos_list.delete(i)
        self.db.cursor.execute("SELECT * FROM ALUNOS")
        for row in self.db.cursor.fetchall():
            self.alunos_list.insert("", "end", values=row)

    def clear_entries(self):
        self.id_entry.delete(0, tk.END)
        self.nome_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.telefone_entry.delete(0, tk.END)


class Notas(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Area das notas")
        self.geometry("1100x600")

        self.db = Database()

        tk.Label(self, text="ID").pack()
        self.id_entry = tk.Entry(self)
        self.id_entry.pack()

        tk.Label(self, text="Disciplina").pack()
        self.disciplina_combobox = ttk.Combobox(self, state="readonly")
        self.disciplina_combobox.pack()
        self.fill_disciplinas_combobox()

        tk.Label(self, text="Aluno").pack()
        self.aluno_combobox = ttk.Combobox(self, state="readonly")
        self.aluno_combobox.pack()
        self.fill_alunos_combobox()

        tk.Label(self, text="Nota Final").pack()
        self.nota_entry = tk.Entry(self)
        self.nota_entry.pack()

        tk.Label(self, text="Faltas").pack()
        self.faltas_entry = tk.Entry(self)
        self.faltas_entry.pack()

        tk.Button(self, text="Adicionar Nota", command=self.add_nota).pack(pady=5)
        tk.Button(self, text="Alterar Nota", command=self.update_nota).pack(pady=5)
        tk.Button(self, text="Deletar Nota", command=self.delete_nota).pack(pady=5)

        self.notas_list = ttk.Treeview(self, columns=("ID", "Disciplina", "Aluno", "Nota Final", "Faltas"), show="headings")
        self.notas_list.heading("ID", text="ID")
        self.notas_list.heading("Disciplina", text="Disciplina")
        self.notas_list.heading("Aluno", text="Aluno")
        self.notas_list.heading("Nota Final", text="Nota Final")
        self.notas_list.heading("Faltas", text="Faltas")
        self.notas_list.pack(pady=10)
        self.notas_list.bind("<Double-1>", self.on_select)

        self.list_notas()

    def on_select(self, event):
        selected_item = self.notas_list.selection()[0]
        values = self.notas_list.item(selected_item, "values")
        self.id_entry.delete(0, tk.END)
        self.id_entry.insert(0, values[0])
        self.nota_entry.delete(0, tk.END)
        self.nota_entry.insert(0, values[3])
        self.faltas_entry.delete(0, tk.END)
        self.faltas_entry.insert(0, values[4])
        
        disciplina_id = self.db.cursor.execute("SELECT ID_DISCI FROM DISCIPLINAS WHERE DISCIPLINA=%s", (values[1],))
        disciplina_id = self.db.cursor.fetchone()[0]
        self.disciplina_combobox.set(values[1])
        
        aluno_id = self.db.cursor.execute("SELECT ID_ALUNO FROM ALUNOS WHERE NOME=%s", (values[2],))
        aluno_id = self.db.cursor.fetchone()[0]
        self.aluno_combobox.set(values[2])

    def fill_disciplinas_combobox(self):
        try:
            self.db.cursor.execute("SELECT DISCIPLINA FROM DISCIPLINAS")
            disciplinas = self.db.cursor.fetchall()
            self.disciplina_combobox["values"] = [disc[0] for disc in disciplinas]
        except Error as e:
            messagebox.showerror("Erro", str(e))

    def fill_alunos_combobox(self):
        try:
            self.db.cursor.execute("SELECT NOME FROM ALUNOS")
            alunos = self.db.cursor.fetchall()
            self.aluno_combobox["values"] = [aluno[0] for aluno in alunos]
        except Error as e:
            messagebox.showerror("Erro", str(e))

    def add_nota(self):
        disciplina = self.disciplina_combobox.get()
        aluno = self.aluno_combobox.get()
        nota = self.nota_entry.get()
        faltas = self.faltas_entry.get()

        if disciplina and aluno and nota and faltas:
            try:
                id_disciplina = self.db.cursor.execute("SELECT ID_DISCI FROM DISCIPLINAS WHERE DISCIPLINA=%s", (disciplina,))
                id_disciplina = self.db.cursor.fetchone()[0]

                id_aluno = self.db.cursor.execute("SELECT ID_ALUNO FROM ALUNOS WHERE NOME=%s", (aluno,))
                id_aluno = self.db.cursor.fetchone()[0]

                self.db.cursor.execute("INSERT INTO NOTAS (ID_DISCI_FK, ID_ALUNO_FK, NOTA_FINAL, FALTAS) VALUES (%s, %s, %s, %s)",
                                       (id_disciplina, id_aluno, nota, faltas))
                self.db.connection.commit()
                messagebox.showinfo("Sucesso", "Nota adicionada com sucesso!")
                self.clear_entries()
                self.list_notas()
            except Error as e:
                messagebox.showerror("Erro", str(e))
        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos.")

    def update_nota(self):
        id_nota = self.id_entry.get()
        disciplina = self.disciplina_combobox.get()
        aluno = self.aluno_combobox.get()
        nota = self.nota_entry.get()
        faltas = self.faltas_entry.get()

        if id_nota and disciplina and aluno and nota and faltas:
            try:
                id_disciplina = self.db.cursor.execute("SELECT ID_DISCI FROM DISCIPLINAS WHERE DISCIPLINA=%s", (disciplina,))
                id_disciplina = self.db.cursor.fetchone()[0]

                id_aluno = self.db.cursor.execute("SELECT ID_ALUNO FROM ALUNOS WHERE NOME=%s", (aluno,))
                id_aluno = self.db.cursor.fetchone()[0]

                self.db.cursor.execute("UPDATE NOTAS SET ID_DISCI_FK=%s, ID_ALUNO_FK=%s, NOTA_FINAL=%s, FALTAS=%s WHERE ID_NOTA=%s",
                                       (id_disciplina, id_aluno, nota, faltas, id_nota))
                self.db.connection.commit()
                messagebox.showinfo("Sucesso", "Nota alterada com sucesso!")
                self.clear_entries()
                self.list_notas()
            except Error as e:
                messagebox.showerror("Erro", str(e))
        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos.")

    def delete_nota(self):
        id_nota = self.id_entry.get()
        if id_nota:
            try:
                self.db.cursor.execute("DELETE FROM NOTAS WHERE ID_NOTA=%s", (id_nota,))
                self.db.connection.commit()
                messagebox.showinfo("Sucesso", "Nota deletada com sucesso!")
                self.clear_entries()
                self.list_notas()
            except Error as e:
                messagebox.showerror("Erro", str(e))
        else:
            messagebox.showwarning("Atenção", "Preencha o ID da nota.")

    def list_notas(self):
        for i in self.notas_list.get_children():
            self.notas_list.delete(i)
        self.db.cursor.execute("SELECT N.ID_NOTA, D.DISCIPLINA, A.NOME, N.NOTA_FINAL, N.FALTAS FROM NOTAS N JOIN DISCIPLINAS D ON N.ID_DISCI_FK = D.ID_DISCI JOIN ALUNOS A ON N.ID_ALUNO_FK = A.ID_ALUNO")
        for row in self.db.cursor.fetchall():
            self.notas_list.insert("", "end", values=row)

    def clear_entries(self):
        self.id_entry.delete(0, tk.END)
        self.nota_entry.delete(0, tk.END)
        self.faltas_entry.delete(0, tk.END)
        self.disciplina_combobox.set("")
        self.aluno_combobox.set("")
    
class ConsultaNotas(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Consultar notas dos alunos")
        self.geometry("1100x600")

        self.db = Database()

        tk.Label(self, text="ID do Aluno").pack(pady=10)
        self.id_aluno_entry = tk.Entry(self)
        self.id_aluno_entry.pack(pady=5)

        tk.Label(self, text="Nome do Aluno").pack(pady=10)
        self.nome_aluno_entry = tk.Entry(self, state='readonly')
        self.nome_aluno_entry.pack(pady=5)

        tk.Button(self, text="Consultar Notas", command=self.consultar_notas).pack(pady=5)

        self.notas_list = ttk.Treeview(self, columns=("ID", "Disciplina", "Professor", "Nota Final", "Faltas"), show="headings")
        self.notas_list.heading("ID", text="ID")
        self.notas_list.heading("Disciplina", text="Disciplina")
        self.notas_list.heading("Professor", text="Professor")
        self.notas_list.heading("Nota Final", text="Nota Final")
        self.notas_list.heading("Faltas", text="Faltas")
        self.notas_list.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def consultar_notas(self):
        id_aluno = self.id_aluno_entry.get()
        if id_aluno:
            for i in self.notas_list.get_children():
                self.notas_list.delete(i)

            try:
                self.db.cursor.execute("SELECT NOME FROM ALUNOS WHERE ID_ALUNO = %s", (id_aluno,))
                resultado = self.db.cursor.fetchone()

                if resultado:
                    self.nome_aluno_entry.config(state='normal')
                    self.nome_aluno_entry.delete(0, tk.END)
                    self.nome_aluno_entry.insert(0, resultado[0])
                    self.nome_aluno_entry.config(state='readonly')
                    query = """
                    SELECT N.ID_NOTA, D.DISCIPLINA, P.NOME, N.NOTA_FINAL, N.FALTAS
                    FROM NOTAS N
                    JOIN DISCIPLINAS D ON N.ID_DISCI_FK = D.ID_DISCI
                    JOIN ALUNOS A ON N.ID_ALUNO_FK = A.ID_ALUNO
                    JOIN PROFESSORES P ON D.ID_PROF_FK = P.ID_PROF
                    WHERE A.ID_ALUNO = %s
                    """
                    self.db.cursor.execute(query, (id_aluno,))
                    for row in self.db.cursor.fetchall():
                        self.notas_list.insert("", "end", values=row)
                else:
                    messagebox.showwarning("Atenção", "Aluno não encontrado.")
                    self.nome_aluno_entry.config(state='normal')
                    self.nome_aluno_entry.delete(0, tk.END)
                    self.nome_aluno_entry.config(state='readonly')

            except Error as e:
                messagebox.showerror("Erro", str(e))
        else:
            messagebox.showwarning("Atenção", "Preencha o ID do Aluno.")

class Grafico(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gráfico de Médias")
        self.geometry("1100x600")

        self.gerar_grafico()

    def gerar_grafico(self):
        try:
            query = """
            SELECT D.DISCIPLINA, AVG(N.NOTA_FINAL) AS MEDIA
            FROM NOTAS N
            JOIN DISCIPLINAS D ON N.ID_DISCI_FK = D.ID_DISCI
            GROUP BY D.DISCIPLINA
            """
            db = Database()
            db.cursor.execute(query)
            resultados = db.cursor.fetchall()

            disciplinas = [row[0] for row in resultados]
            medias = [row[1] for row in resultados]

            fig, ax = plt.subplots()
            ax.bar(disciplinas, medias, color='#191970')
            ax.set_title('Média de Notas por Disciplina')
            ax.set_xlabel('Disciplinas')
            ax.set_ylabel('Média de Notas')
            ax.set_xticklabels(disciplinas, rotation=45)
            plt.tight_layout()

            canvas = FigureCanvasTkAgg(fig, master=self)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        except Error as e:
            messagebox.showerror("Erro", str(e))

if __name__ == "__main__":
    app = App()
    app.mainloop()