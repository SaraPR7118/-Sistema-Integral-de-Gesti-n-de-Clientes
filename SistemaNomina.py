'''
Ejercicio 3: Sistema de Nómina -  Fase 3 de curso de Programación 
Grupo: 213023A_2201
Nombre: Sara Brisney Pareja Rojas
'''
# Importaciones
import tkinter as tk
from tkinter import messagebox, ttk



# =====================================================
# CLASE BASE: Empleado
# Clase padre con atributos y métodos comunes para
# todos los tipos de empleados
# =====================================================
class Empleado:
    def __init__(self, nombre, identificacion, salario_base):
        # Atributos generales de todo empleado
        self.nombre = nombre
        self.identificacion = identificacion
        self.salario_base = salario_base

    def calcular_salario(self):
        """
        Cada clase hija lo sobrescribe con su propia lógica.
        La clase base retorna solo el salario_base.
        """
        return self.salario_base


    def mostrar_informacion(self, mostrar_salario=False, mostrar_detalles=False):
        """
        Sobrecarga simulada:
        - Sin params     -> solo datos básicos
        - mostrar_salario=True -> agrega salario total
        - mostrar_detalles=True -> agrega información extra de cada tipo
        """
        # Datos básicos (siempre se muestran)
        info = (
            f"Name: {self.nombre}\n"
            f"ID: {self.identificacion}\n"
            f"Base Salary: ${self.salario_base:,.0f}"
        )
        # Nivel 2: muestra salario calculado total
        if mostrar_salario:
            info += f"\nTotal Salary: ${self.calcular_salario():,.0f}"

        # Nivel 3: detalles extras (cada subclase añade los suyos)
        if mostrar_detalles:
            info += self._detalles_extra()

        return info

    def _detalles_extra(self):
        """Método auxiliar para que subclases añadan detalles propios."""
        return ""

    def tipo_empleado(self):
        """Retorna el tipo de empleado (para mostrar en la lista)."""
        return "Employee"


# =====================================================
# CLASE HIJA 1: EmpleadoTiempoCompleto
# Hereda de Empleado
# Salario = salario_base + bonificacion por desempeño
# =====================================================
class EmpleadoTiempoCompleto(Empleado):
    def __init__(self, nombre, identificacion, salario_base, bonificacion_desempeno):
        # Llama al constructor del padre con super()
        super().__init__(nombre, identificacion, salario_base)
        # Atributo específico de este tipo
        self.bonificacion_desempeno = bonificacion_desempeno

    def calcular_salario(self):
        """POLIMORFISMO: salario fijo + bono de desempeño."""
        return self.salario_base + self.bonificacion_desempeno

    def _detalles_extra(self):
        return f"\nPerformance Bonus: ${self.bonificacion_desempeno:,.0f}"

    def tipo_empleado(self):
        return "Full-Time"


# =====================================================
# CLASE HIJA 2: EmpleadoPorHoras
# Hereda de Empleado
# Salario = horas_trabajadas × tarifa_hora
# =====================================================
class EmpleadoPorHoras(Empleado):
    def __init__(self, nombre, identificacion, tarifa_hora, horas_trabajadas):
        # El salario_base se calcula dinámicamente
        super().__init__(nombre, identificacion, tarifa_hora)
        self.tarifa_hora = tarifa_hora
        self.horas_trabajadas = horas_trabajadas

    def calcular_salario(self):
        """POLIMORFISMO: pago según horas trabajadas."""
        return self.tarifa_hora * self.horas_trabajadas

    def _detalles_extra(self):
        return (
            f"\nHourly Rate: ${self.tarifa_hora:,.0f}"
            f"\nHours Worked: {self.horas_trabajadas}"
        )

    def tipo_empleado(self):
        return "Hourly"


# =====================================================
# CLASE HIJA 3: EmpleadoComision
# Hereda de Empleado
# Salario = salario_base + (ventas_totales × porcentaje/100)
# =====================================================
class EmpleadoComision(Empleado):
    def __init__(self, nombre, identificacion, salario_base, ventas_totales, porcentaje_comision):
        super().__init__(nombre, identificacion, salario_base)
        self.ventas_totales = ventas_totales
        self.porcentaje_comision = porcentaje_comision  # ej: 10 = 10%

    def calcular_salario(self):
        """POLIMORFISMO: base + comisión por ventas."""
        comision = self.ventas_totales * (self.porcentaje_comision / 100)
        return self.salario_base + comision

    def _detalles_extra(self):
        comision = self.ventas_totales * (self.porcentaje_comision / 100)
        return (
            f"\nTotal Sales: ${self.ventas_totales:,.0f}"
            f"\nCommission ({self.porcentaje_comision}%): ${comision:,.0f}"
        )

    def tipo_empleado(self):
        return "Commission"


# =====================================================
# HERENCIA MÚLTIPLE: EmpleadoTiempoCompletoBonificado
# Hereda de EmpleadoTiempoCompleto Y de Bonificable
# Combina salario fijo + bono desempeño + bonificaciones extra
# =====================================================

class Bonificable:
    """
    Tiene la capacidad de manejar bonificaciones.
    
    """
    def __init__(self):
        # Lista interna de bonificaciones acumuladas
        self._bonificaciones = []

    def agregar_bonificacion(self, monto):
        """Agrega un monto de bonificación a la lista interna."""
        self._bonificaciones.append(monto)

    def obtener_bonificaciones(self):
        """Retorna el total sumado de todas las bonificaciones."""
        return sum(self._bonificaciones)

class EmpleadoTiempoCompletoBonificado(EmpleadoTiempoCompleto, Bonificable):
    def __init__(self, nombre, identificacion, salario_base, bonificacion_desempeno):
        # Inicializa AMBAS clases padre
        EmpleadoTiempoCompleto.__init__(self, nombre, identificacion, salario_base, bonificacion_desempeno)
        Bonificable.__init__(self)  # Inicializa la lista de bonificaciones

    def calcular_salario(self):
        """
        HERENCIA MÚLTIPLE + POLIMORFISMO:
        Salario = base + bono desempeño + todas las bonificaciones extras
        """
        salario_base_full = super().calcular_salario()  # base + desempeño
        return salario_base_full + self.obtener_bonificaciones()

    def _detalles_extra(self):
        return (
            super()._detalles_extra()
            + f"\nExtra Bonuses: ${self.obtener_bonificaciones():,.0f}"
        )

    def tipo_empleado(self):
        return "Full-Time + Bonuses"


# =====================================================
# CLASE USUARIO - LOGIN (requerimiento del documento)
# =====================================================
class Usuario:
    def __init__(self):
        self._usuario = "programación"
        self._password = "programación"

    def validar(self, usuario_ingresado, password_ingresada):
        return (usuario_ingresado == self._usuario and
                password_ingresada == self._password)


# =====================================================
# VENTANA DE LOGIN
# =====================================================
class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Payroll System - Login")
        self.root.geometry("420x300")
        self.root.resizable(False, False)
        self.usuario = Usuario()
        self._construir_login()

    def _construir_login(self):
        tk.Label(self.root, text="Payroll System", font=("Arial", 18, "bold")).pack(pady=25)

        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Label(frame, text="Username:", font=("Arial", 11)).grid(row=0, column=0, padx=10, pady=8, sticky="e")
        self.entry_user = tk.Entry(frame, font=("Arial", 12), width=22)
        self.entry_user.grid(row=0, column=1, padx=10, pady=8)
        self.entry_user.focus()

        tk.Label(frame, text="Password:", font=("Arial", 11)).grid(row=1, column=0, padx=10, pady=8, sticky="e")
        self.entry_pass = tk.Entry(frame, font=("Arial", 12), width=22, show="*")
        self.entry_pass.grid(row=1, column=1, padx=10, pady=8)

        frame_btn = tk.Frame(self.root)
        frame_btn.pack(pady=18)

        tk.Button(frame_btn, text="Login", command=self._validar,
                  bg="#2e7d32", fg="white", font=("Arial", 12), width=10).pack(side="left", padx=8)
        tk.Button(frame_btn, text="Exit", command=self.root.quit,
                  bg="#c62828", fg="white", font=("Arial", 12), width=10).pack(side="left", padx=8)

        # Enter también activa el login
        self.root.bind('<Return>', lambda e: self._validar())

    def _validar(self):
        u = self.entry_user.get().strip()
        p = self.entry_pass.get().strip()
        if self.usuario.validar(u, p):
            self.root.destroy()
            root2 = tk.Tk()
            Aplicacion(root2)
            root2.mainloop()
        else:
            messagebox.showerror("Login Error", "Invalid credentials.\n\nUser: programación\nPassword: programación")
            self.entry_user.delete(0, tk.END)
            self.entry_pass.delete(0, tk.END)
            self.entry_user.focus()


# =====================================================
# APLICACIÓN PRINCIPAL - SISTEMA DE NÓMINA
# =====================================================
class Aplicacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Payroll Management System")
        self.root.geometry("820x620")

        # Lista interna de empleados (polimorfismo)
        self.lista_empleados = []

        self._construir_interfaz()

    def _construir_interfaz(self):
        # ---- ENCABEZADO ----
        tk.Label(self.root, text="Payroll Management System",
                 font=("Arial", 16, "bold"), bg="#1565C0", fg="white").pack(fill="x", pady=4)

        # ---- FRAME TIPO DE EMPLEADO ----
        frame_tipo = tk.LabelFrame(self.root, text="Employee Type", padx=8, pady=6)
        frame_tipo.pack(fill="x", padx=10, pady=4)

        self.tipo_var = tk.StringVar(value="Full-Time")
        tipos = ["Full-Time", "Hourly", "Commission", "Full-Time + Bonuses"]
        for t in tipos:
            tk.Radiobutton(frame_tipo, text=t, variable=self.tipo_var,
                           value=t, command=self._actualizar_campos).pack(side="left", padx=10)

        # ---- FRAME DATOS COMUNES ----
        frame_datos = tk.LabelFrame(self.root, text="Employee Data", padx=8, pady=6)
        frame_datos.pack(fill="x", padx=10, pady=4)

        tk.Label(frame_datos, text="Name:").grid(row=0, column=0, sticky="e", padx=5, pady=4)
        self.entry_nombre = tk.Entry(frame_datos, width=22, font=("Arial", 11))
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=4)

        tk.Label(frame_datos, text="ID:").grid(row=0, column=2, sticky="e", padx=5)
        self.entry_id = tk.Entry(frame_datos, width=15, font=("Arial", 11))
        self.entry_id.grid(row=0, column=3, padx=5, pady=4)

        tk.Label(frame_datos, text="Base Salary / Rate:").grid(row=1, column=0, sticky="e", padx=5)
        self.entry_salario = tk.Entry(frame_datos, width=22, font=("Arial", 11))
        self.entry_salario.grid(row=1, column=1, padx=5, pady=4)

        # ---- FRAME CAMPOS DINÁMICOS (según tipo) ----
        self.frame_extra = tk.LabelFrame(self.root, text="Additional Data", padx=8, pady=6)
        self.frame_extra.pack(fill="x", padx=10, pady=4)
        self._actualizar_campos()

        # ---- BOTONES DE ACCIÓN ----
        frame_btns = tk.Frame(self.root)
        frame_btns.pack(pady=6)

        tk.Button(frame_btns, text="Add Employee", command=self._agregar_empleado,
                  bg="#2e7d32", fg="white", font=("Arial", 11), width=14).pack(side="left", padx=6)
        tk.Button(frame_btns, text="Show Info", command=self._mostrar_info,
                  bg="#1565C0", fg="white", font=("Arial", 11), width=14).pack(side="left", padx=6)
        tk.Button(frame_btns, text="Monthly Payroll", command=self._calcular_nomina,
                  bg="#6a1b9a", fg="white", font=("Arial", 11), width=14).pack(side="left", padx=6)
        tk.Button(frame_btns, text="Remove", command=self._eliminar,
                  bg="#c62828", fg="white", font=("Arial", 11), width=10).pack(side="left", padx=6)

        # ---- LISTBOX DE EMPLEADOS ----
        frame_lista = tk.LabelFrame(self.root, text="Registered Employees", padx=6, pady=6)
        frame_lista.pack(fill="both", expand=True, padx=10, pady=4)

        self.listbox = tk.Listbox(frame_lista, font=("Courier", 10), height=8)
        self.listbox.pack(side="left", fill="both", expand=True)

        sb = tk.Scrollbar(frame_lista, orient="vertical", command=self.listbox.yview)
        sb.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=sb.set)

    # =====================================================
    # ACTUALIZA CAMPOS DINÁMICOS SEGÚN TIPO SELECCIONADO
    # =====================================================
    def _actualizar_campos(self):
        # Borra campos extra anteriores
        for widget in self.frame_extra.winfo_children():
            widget.destroy()

        tipo = self.tipo_var.get()

        if tipo == "Full-Time" or tipo == "Full-Time + Bonuses":
            tk.Label(self.frame_extra, text="Performance Bonus:").grid(row=0, column=0, sticky="e", padx=5)
            self.entry_extra1 = tk.Entry(self.frame_extra, width=20, font=("Arial", 11))
            self.entry_extra1.grid(row=0, column=1, padx=5, pady=4)
            # Campo adicional para bonificaciones extra
            if tipo == "Full-Time + Bonuses":
                tk.Label(self.frame_extra, text="Extra Bonus:").grid(row=0, column=2, sticky="e", padx=5)
                self.entry_extra2 = tk.Entry(self.frame_extra, width=20, font=("Arial", 11))
                self.entry_extra2.grid(row=0, column=3, padx=5, pady=4)

        elif tipo == "Hourly":
            tk.Label(self.frame_extra, text="Hours Worked:").grid(row=0, column=0, sticky="e", padx=5)
            self.entry_extra1 = tk.Entry(self.frame_extra, width=20, font=("Arial", 11))
            self.entry_extra1.grid(row=0, column=1, padx=5, pady=4)

        elif tipo == "Commission":
            tk.Label(self.frame_extra, text="Total Sales:").grid(row=0, column=0, sticky="e", padx=5)
            self.entry_extra1 = tk.Entry(self.frame_extra, width=20, font=("Arial", 11))
            self.entry_extra1.grid(row=0, column=1, padx=5, pady=4)
            tk.Label(self.frame_extra, text="Commission %:").grid(row=0, column=2, sticky="e", padx=5)
            self.entry_extra2 = tk.Entry(self.frame_extra, width=10, font=("Arial", 11))
            self.entry_extra2.grid(row=0, column=3, padx=5, pady=4)

    # =====================================================
    # AGREGAR EMPLEADO A LA LISTA INTERNA
    # =====================================================
    def _agregar_empleado(self):
        nombre = self.entry_nombre.get().strip()
        eid = self.entry_id.get().strip()
        tipo = self.tipo_var.get()

        if not nombre or not eid:
            messagebox.showerror("Error", "Name and ID are required.")
            return

        try:
            salario = float(self.entry_salario.get())

            # Crear el objeto correcto según el tipo (POLIMORFISMO)
            if tipo == "Full-Time":
                bono = float(self.entry_extra1.get())
                emp = EmpleadoTiempoCompleto(nombre, eid, salario, bono)

            elif tipo == "Hourly":
                horas = float(self.entry_extra1.get())
                emp = EmpleadoPorHoras(nombre, eid, salario, horas)

            elif tipo == "Commission":
                ventas = float(self.entry_extra1.get())
                pct = float(self.entry_extra2.get())
                emp = EmpleadoComision(nombre, eid, salario, ventas, pct)

            elif tipo == "Full-Time + Bonuses":
                bono = float(self.entry_extra1.get())
                extra = float(self.entry_extra2.get())
                emp = EmpleadoTiempoCompletoBonificado(nombre, eid, salario, bono)
                emp.agregar_bonificacion(extra)  # Usa método de Bonificable

        except ValueError:
            messagebox.showerror("Error", "All numeric fields must be valid numbers.")
            return

        # Guardar en lista interna
        self.lista_empleados.append(emp)

        # Mostrar en Listbox con POLIMORFISMO: tipo_empleado() difiere por clase
        texto = f"[{emp.tipo_empleado():18}] {emp.nombre:20} ID: {emp.identificacion}"
        self.listbox.insert(tk.END, texto)

        # Limpiar campos
        self.entry_nombre.delete(0, tk.END)
        self.entry_id.delete(0, tk.END)
        self.entry_salario.delete(0, tk.END)
        self.entry_extra1.delete(0, tk.END)
        if hasattr(self, 'entry_extra2'):
            self.entry_extra2.delete(0, tk.END)

    # =====================================================
    # MOSTRAR INFORMACIÓN DE EMPLEADO SELECCIONADO
    # SOBRECARGA: muestra datos + salario + detalles
    # =====================================================
    def _mostrar_info(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showwarning("Warning", "Select an employee from the list.")
            return
        emp = self.lista_empleados[sel[0]]

        # Llama mostrar_informacion() con SOBRECARGA COMPLETA (todos los detalles)
        info = emp.mostrar_informacion(mostrar_salario=True, mostrar_detalles=True)
        messagebox.showinfo("Employee Information", info)

    # =====================================================
    # CALCULAR NÓMINA MENSUAL - DEMUESTRA POLIMORFISMO
    # El mismo método calcular_salario() responde diferente
    # en cada tipo de empleado
    # =====================================================
    def _calcular_nomina(self):
        if not self.lista_empleados:
            messagebox.showwarning("Warning", "No employees registered.")
            return

        resumen = "====== MONTHLY PAYROLL ======\n\n"
        total_nomina = 0

        # POLIMORFISMO: recorre la lista sin saber el tipo exacto
        # cada empleado calcula su salario con sus propias reglas
        for emp in self.lista_empleados:
            salario = emp.calcular_salario()
            total_nomina += salario
            resumen += (
                f"{emp.nombre} ({emp.tipo_empleado()})\n"
                f"  Salary: ${salario:,.0f}\n"
            )

        resumen += f"\n{'='*30}\n"
        resumen += f"TOTAL PAYROLL: ${total_nomina:,.0f}"

        messagebox.showinfo("Monthly Payroll", resumen)

    # =====================================================
    # ELIMINAR EMPLEADO SELECCIONADO
    # =====================================================
    def _eliminar(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showwarning("Warning", "Select an employee to remove.")
            return
        idx = sel[0]
        nombre = self.lista_empleados[idx].nombre
        self.listbox.delete(idx)
        del self.lista_empleados[idx]
        messagebox.showinfo("Removed", f"{nombre} has been removed.")


# =====================================================
# PUNTO DE ENTRADA - INICIA CON LOGIN
# =====================================================
if __name__ == "__main__":
    root_login = tk.Tk()
    LoginWindow(root_login)
    root_login.mainloop()
