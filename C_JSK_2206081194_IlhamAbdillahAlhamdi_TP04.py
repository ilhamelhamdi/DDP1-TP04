import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkfont
from PIL import Image, ImageTk      # pip install pillow
from urllib.request import urlopen
from io import BytesIO
import random
from typing import Literal


class Menu:
    menu_list = []

    def __init__(self, id, name, price, additional_info) -> None:
        self.id = id
        self.name = name
        self.price = int(price)
        self.additional_info = additional_info
        Menu.menu_list.append(self)

    def get_data(self) -> list:
        return [self.id, self.name, self.price, self.additional_info]


class Meals(Menu):
    additional_info_name = "Kegurihan"

    def __init__(self, id, name, price, tingkat_kegurihan) -> None:
        super().__init__(id, name, price, tingkat_kegurihan)


class Drinks(Menu):
    additional_info_name = "Kemanisan"

    def __init__(self, id, name, price, tingkat_kemanisan) -> None:
        super().__init__(id, name, price, tingkat_kemanisan)


class Sides(Menu):
    additional_info_name = "Keviralan"

    def __init__(self, id, name, price, tingkat_keviralan) -> None:
        super().__init__(id, name, price, tingkat_keviralan)


class OrderedMenu:
    def __init__(self, menu: Meals | Drinks | Sides, quantity: int) -> None:
        self.menu = menu
        self.quantity = quantity


class Order:
    def __init__(self, table_number: int, username: tk.StringVar, menu_list: list[OrderedMenu]) -> None:
        self.table_number = table_number
        self.username = username
        self.menu_list = menu_list


class Table:
    all_tables: dict[int, Order] = dict(
        (number, None) for number in range(1, 11))

    @staticmethod
    def book(table_number: int, order: Order) -> None:
        Table.all_tables[table_number] = order

    @staticmethod
    def get_available() -> list[int]:
        return [number for number in Table.all_tables if Table.all_tables[number] == None]

    @staticmethod
    def get_booked() -> list[int]:
        return [number for number in Table.all_tables if Table.all_tables[number] != None]

    @staticmethod
    def checkout(table_number) -> None:
        Table.all_tables[table_number] = None


class CustomImage():
    """Image from URL (fetched and cached on memory)"""
    cached_images = {}

    def __init__(self, url: str, size: tuple[int] = (1024, 576)) -> None:
        try:
            if url in CustomImage.cached_images:
                self.image_tk = CustomImage.cached_images[url]
                return

            self.requested_data = urlopen(url).read()
            self.raw_image = Image.open(
                BytesIO(self.requested_data)).resize(size)
            self.image_tk = ImageTk.PhotoImage(image=self.raw_image)
            CustomImage.cached_images[url] = self.image_tk
        except:
            print('Failed to fetch image.')
            raise ConnectionError

    def get_image(self):
        return self.image_tk


class Style:
    """Tkinter widgets styles configuration"""

    def __init__(self) -> None:
        Style.font_heading = tkfont.Font(
            family='Arial', size=32,  weight="bold")
        Style.font_large = tkfont.Font(family='Arial', size=16)
        Style.font_base = tkfont.Font(family='Arial', size=12)
        Style.font_small = tkfont.Font(family='Arial', size=10)
        Style.font_small_bold = tkfont.Font(
            family='Arial', size=10, weight='bold')

        Style.button = {
            'fg': 'white',
            'activeforeground': 'white',
            'bd': 0,
            'highlightthickness': 0,
            'cursor': 'hand2'
        }
        Style.button_red = {
            'bg': '#bb1f1b',
            'activebackground': '#871613',
            **Style.button
        }
        Style.button_green = {
            'bg': '#497660',
            'activebackground': '#294336',
            **Style.button
        }
        Style.button_purple = {
            'bg': '#901b67',
            'activebackground': '#5d1142',
            **Style.button
        }
        Style.button_blue = {
            'bg': '#1f3258',
            'activebackground': '#0d1524',
            **Style.button
        }


class MainApp(tk.Tk):
    """Base of app window and routes"""
    container = None
    page_stack = []
    window_width = 1024
    window_height = 576

    def __init__(self) -> None:
        super().__init__()
        self.geometry(f"{MainApp.window_width}x{MainApp.window_height}")
        self.title("Kafe Daun-Daun Pacilkom v2.0 🌿")

        Style()  # configure widget styles
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TCombobox",
                        fieldbackground='#ffcd7e',
                        background='#ffcd7e',
                        disabledbackground='#ffcd7e')
        style.map("TCombobox",
                  fieldbackground=[('readonly', '#ffcd7e')],
                  background=[('readonly', '#ffcd7e')])

        MainApp.container = tk.Frame(self)
        MainApp.container.pack(fill=tk.BOTH, expand=True)

        initial_page = LandingPage(MainApp.container)
        MainApp.page_stack.append(initial_page)
        initial_page.pack()

    @staticmethod
    def show_page(to_page: tk.Frame) -> None:
        """Add page to app stack pages"""
        if len(MainApp.page_stack) > 0:
            MainApp.page_stack[-1].pack_forget()
        MainApp.page_stack.append(to_page)
        to_page.pack()

    @staticmethod
    def back() -> None:
        """Go back to previous page"""
        current_page = MainApp.page_stack.pop()
        current_page.pack_forget()
        previous_page = MainApp.page_stack[-1]
        previous_page.pack()

    @staticmethod
    def clear() -> None:
        """Clear pages stack and display landing page"""
        for page in reversed(MainApp.page_stack):
            page.destroy()
        MainApp.page_stack = [LandingPage(MainApp.container)]
        MainApp.page_stack[0].pack()

    @staticmethod
    def show_toast(message: str) -> None:
        """Show notification in 3 seconds"""
        toast = tk.Frame(MainApp.container, bg='#c1559f', padx=3, pady=3)
        label = tk.Label(toast, text=message, font=Style.font_base,
                         bg='#3e2645', fg='white', padx=10, pady=10, bd=0)
        toast.place(relx=.5, rely=.03, anchor='n')
        label.pack(side='top')
        toast.after(3000, toast.destroy)


class LandingPage(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, width=MainApp.window_width, height=MainApp.window_height)

        try:
            self.background_image = CustomImage(
                url='https://res.cloudinary.com/elhamdi/image/upload/v1670668326/landing_page_iycqcn.png').get_image()
            background_image_label = tk.Label(
                self, image=self.background_image)
            background_image_label.place(relx=.5, rely=.5, anchor='center')
        except:
            pass

        button1 = tk.Button(self, text="Buat Pesanan", width=30,
                            font=Style.font_large, command=self.create_order, **Style.button_red, )
        button2 = tk.Button(self, text="Selesai Gunakan Meja", width=30,
                            font=Style.font_large, command=self.checkout, **Style.button_red, )
        button1.place(relx=.5, rely=.5, anchor=tk.CENTER)
        button2.place(relx=.5, rely=.6, anchor=tk.CENTER)

    def create_order(self):
        MainApp.show_page(CreateOrderPage(MainApp.container))

    def checkout(self):
        MainApp.show_page(Checkout(MainApp.container))


class CreateOrderPage(tk.Frame):
    def __init__(self, master=None):
        self.bg_color = '#ce7475'
        super().__init__(master, width=MainApp.window_width,
                         height=MainApp.window_height, bg=self.bg_color)

        username = tk.StringVar()
        order_list = [OrderedMenu(menu, 0)
                      for menu in Menu.menu_list]
        available_tables = Table.get_available()
        # Give random available table
        table_number = random.choice(
            available_tables) if available_tables else -1
        self.order = Order(table_number, username, order_list)

        try:
            self.background_image = CustomImage(
                url='https://res.cloudinary.com/elhamdi/image/upload/v1670658201/nama_vvegdu.png').get_image()
            background_image_label = tk.Label(
                self, image=self.background_image)
            background_image_label.place(relx=.5, rely=.5, anchor='center')
        except:
            pass

        self.frame = tk.Frame(self, background=self.bg_color)
        self.frame.place(relx=.5, rely=.4, anchor=tk.CENTER)

        self.label_username = tk.Label(
            self.frame, text="Siapa nama Anda?", font=Style.font_heading, background=self.bg_color, fg='#fff')
        self.label_username.grid(
            column=0, row=0, columnspan=2, sticky='nsew', pady=10)

        self.input_field = tk.Entry(
            self.frame, textvariable=self.order.username, font=Style.font_large, justify='center')
        self.input_field.bind('<Return>', self.display_menu)
        self.input_field.grid(
            column=0, row=1, columnspan=2, sticky='nsew', pady=10)
        self.input_field.focus_set()

        self.button_back = tk.Button(
            self.frame, text="Kembali", width=15, font=Style.font_large, **Style.button_red, command=MainApp.back)
        self.button_back.grid(column=0, row=2, pady=10)

        self.button_next = tk.Button(
            self.frame, text="Lanjut", width=15, font=Style.font_large, **Style.button_red, command=self.display_menu)
        self.button_next.grid(column=1, row=2, pady=10)

    def display_menu(self, event: tk.Event = None) -> None:
        """Go to display menu page"""
        if not self.validate_username():
            return

        if Table.get_available():
            MainApp.show_page(DisplayMenuPage(
                MainApp.container, mode="order", order=self.order))
        else:
            MainApp.clear()
            MainApp.show_toast(
                "Mohon maaf, meja sedang penuh. Silakan datang kembali di lain kesempatan.")

    def validate_username(self) -> bool:
        """Username must be unique and not empty"""
        if self.order.username.get() == '':
            MainApp.show_toast('Nama tidak boleh kosong.')
            return False

        booked_table = Table.get_booked()
        for i in booked_table:
            if self.order.username.get() == Table.all_tables[i].username.get():
                MainApp.show_toast('Nama sudah dipakai.')
                return False
        return True


class DisplayMenuPage(tk.Frame):
    def __init__(self, master, mode: Literal["order", "checkout"], order: Order):
        self.bg_color = '#ffcd7e'  # light orange
        self.order = order
        self.mode = mode
        super().__init__(master, width=MainApp.window_width,
                         height=MainApp.window_height, bg=self.bg_color)

        try:
            self.background_image = CustomImage(
                url='https://res.cloudinary.com/elhamdi/image/upload/v1670665588/menu_a0yjvn.png').get_image()
            background_image_label = tk.Label(
                self, image=self.background_image)
            background_image_label.place(relx=.5, rely=.5, anchor='center')
        except:
            pass

        # Customer name
        self.label_name = ttk.Label(
            self, text=f"Nama pemesan: \n{self.order.username.get()}", font=Style.font_base, background=self.bg_color)
        self.label_name.place(relx=0.12, rely=0.12, anchor='nw')

        # Table number
        self.table_number = tk.Frame(self, bg=self.bg_color)
        self.label_table_number = ttk.Label(
            self.table_number, text=f"No Meja: {self.order.table_number}", font=Style.font_base, background=self.bg_color)
        self.label_table_number.grid(row=0, column=0)
        if self.mode == "order":
            self.button_change_table = tk.Button(
                self.table_number, text="Ubah", font=Style.font_base, **Style.button_red, command=self.change_table, padx=20)
            self.button_change_table.grid(row=0, column=1, padx=5)
        self.table_number.place(relx=0.88, rely=0.12, anchor='ne')

        # ================ main frame ==================
        self.main_frame = tk.Frame(self, bg=self.bg_color)
        self.main_frame.place(relx=.5, rely=.5, anchor=tk.CENTER)

        # Menu category
        self.category_menu_container = tk.Frame(
            self.main_frame, bg=self.bg_color)
        self.category_menu_container.pack(side='top')
        self.category_menu_label = tk.Label(
            self.category_menu_container, text="Kategori :", bg=self.bg_color, font=Style.font_small_bold)
        self.category_menu_label.pack(side=tk.LEFT)
        self.category_menu_combobox = ttk.Combobox(
            self.category_menu_container, values=("ALL", "MEALS", "DRINKS", "SIDES"), font=Style.font_small)
        self.category_menu_combobox.pack(side=tk.LEFT)
        self.category_menu_combobox.insert(0, "ALL")
        self.category_menu_combobox['state'] = 'readonly'
        self.category_menu_combobox.bind(
            "<<ComboboxSelected>>", self.change_category)

        # Scrollable table of menu
        self.canvas = tk.Canvas(self.main_frame, width=740, height=300)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar = ttk.Scrollbar(
            self.main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.menu_table = tk.Frame(self.canvas, bg=self.bg_color, bd=0)
        self.menu_table.bind(
            "<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.menu_table, anchor='nw')
        self.canvas.configure(
            yscrollcommand=self.scrollbar.set, bg=self.bg_color, bd=0, highlightthickness=0,)

        self.generate_all_tables()
        self.bind_children(widget=self.main_frame, event="<MouseWheel>",
                           callback=self.on_mouse_wheel)

        # ================= main frame ====================

        # Total price
        self.label_total_price = tk.Label(
            self, text=f"Total harga: Rp{self.dot(self.calculate_total_price())}", bg=self.bg_color, font=Style.font_large)
        self.label_total_price.place(relx=0.5, rely=0.8, anchor='center')

        # Navigation button
        self.button_back = tk.Button(
            self, text="Kembali", width=20, font=Style.font_large, **Style.button_red, command=MainApp.back)
        self.button_back.place(relx=0.2, rely=0.9, anchor='nw')

        if self.mode == "order":
            self.button_ok = tk.Button(
                self, text="OK", width=20, font=Style.font_large, **Style.button_red, command=self.book)
            self.button_ok.place(relx=0.8, rely=0.9, anchor='ne')
        else:
            self.button_checkout = tk.Button(
                self, text="Selesai Gunakan Meja", width=20, font=Style.font_large, **Style.button_red, command=self.checkout)
            self.button_checkout.place(relx=0.8, rely=0.9, anchor='ne')

    def generate_all_tables(self) -> None:
        categories = []
        active_category = self.category_menu_combobox.get()
        if active_category in ("ALL", "MEALS"):
            meals = [order for order in self.order.menu_list if isinstance(
                order.menu, Meals)]
            categories.append(meals)
        if active_category in ("ALL", "DRINKS"):
            drinks = [order for order in self.order.menu_list if isinstance(
                order.menu, Drinks)]
            categories.append(drinks)
        if active_category in ("ALL", "SIDES"):
            sides = [order for order in self.order.menu_list if isinstance(
                order.menu, Sides)]
            categories.append(sides)

        for menu_list in categories:
            self.generate_table(menu_list)

    def generate_table(self, order_list: list[OrderedMenu]) -> None:
        """Generate table per category"""
        tk.Label(self.menu_table,
                 bg=self.bg_color,
                 font=Style.font_base,
                 text=order_list[0].menu.__class__.__name__.upper()
                 ).pack(anchor='w')

        category_table = tk.Frame(self.menu_table, bg=self.bg_color)
        category_table.pack(pady=(0, 10))
        total_rows = len(order_list)
        total_columns = 5
        header = ["Kode", "Nama", "Harga",
                  order_list[0].menu.additional_info_name, "Jumlah"]

        # Table header
        for i in range(total_columns):
            entry = tk.Entry(category_table,
                             font=Style.font_small_bold,
                             relief="flat",
                             readonlybackground=self.bg_color)
            entry.grid(row=0, column=i)
            entry.insert(tk.END, header[i])
            entry['state'] = 'readonly'

        # Table data
        for i in range(total_rows):
            ordered_menu = order_list[i]
            ordered_menu_data = ordered_menu.menu.get_data()
            ordered_menu_data[2] = self.dot(ordered_menu_data[2])

            for j in range(total_columns-1):
                entry = tk.Entry(category_table, font=Style.font_small,
                                 relief="flat", readonlybackground=self.bg_color)
                entry.grid(row=i+1, column=j)
                entry.insert(tk.END, ordered_menu_data[j])
                entry['state'] = 'readonly'

            # Column jumlah
            if self.mode == "order":
                values = tuple(range(10))
                opsi_jumlah = ttk.Combobox(
                    category_table,
                    font=Style.font_small,
                    values=values,
                    validate='key',
                    validatecommand=(self.register(
                        lambda x, y: self.validate_input(x, y)), '%P', '%S')
                )
                opsi_jumlah.grid(row=i+1, column=total_columns-1)
                opsi_jumlah.insert(0, ordered_menu.quantity)
                events = ("<<ComboboxSelected>>", "<FocusOut>", "<KeyRelease>")
                for event in events:
                    opsi_jumlah.bind(event,
                                     lambda event, val=ordered_menu: self.change_menu_quantity(event, ordered_menu=val))
                opsi_jumlah.unbind_class("TCombobox", "<MouseWheel>")
            else:  # checkout mode
                entry = tk.Entry(category_table, font=Style.font_small,
                                 relief="flat", readonlybackground=self.bg_color)
                entry.grid(row=i+1, column=total_columns-1)
                entry.insert(tk.END, ordered_menu.quantity)
                entry['state'] = 'readonly'

    def change_category(self, event: tk.Event = None) -> None:
        """Filter menu based on category"""
        for child in self.menu_table.winfo_children():
            child.destroy()
        self.generate_all_tables()
        self.bind_children(self.main_frame, '<MouseWheel>',
                           self.on_mouse_wheel)

    def change_menu_quantity(self, event: tk.Event = None, ordered_menu: OrderedMenu = None, *args, **kwargs) -> None:
        """Update quantity of ordered menu and total price"""
        try:
            value = event.widget.get()
            ordered_menu.quantity = int(value) if value != '' else 0
            self.label_total_price['text'] = f"Total harga: Rp{self.dot(self.calculate_total_price())}"
            # Change empty string to 0 in input text on FocusOut event
            if event.type != '10' and value == '':
                return
            event.widget.set(ordered_menu.quantity)
        except:
            pass

    def validate_input(self, value_if_allowed, text) -> bool:
        """Ensure input is only number"""
        if text not in '0123456789':
            return False
        try:
            int(value_if_allowed if value_if_allowed != '' else 0)
            return True
        except:
            return False

    def calculate_total_price(self) -> int:
        total = 0
        for order in self.order.menu_list:
            total += order.quantity * order.menu.price
        return total

    def change_table(self) -> None:
        """UBAH MEJA"""
        MainApp.show_page(TableDisplayPage(
            MainApp.container, mode="order", order=self.order))

    def bind_children(self, widget: tk.Widget, event: str, callback) -> None:
        """Bind event to it's children recursively"""
        children = widget.winfo_children()
        if len(children) == 0:
            return
        for child in children:
            child.bind(event, callback)
            self.bind_children(child, event, callback)

    def book(self) -> None:
        """Finish creating order"""
        Table.book(table_number=self.order.table_number,
                   order=self.order)
        MainApp.clear()
        MainApp.show_toast("Berhasil membuat pesanan!")

    def checkout(self) -> None:
        """SELESAI MENGGUNAKAN MEJA"""
        Table.checkout(self.order.table_number)
        MainApp.back()
        MainApp.show_toast("Berhasil melakukan checkout!")

    def on_mouse_wheel(self, event: tk.Event) -> None:
        """Table scrolling effect"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), 'units')

    def dot(self, num: int) -> str:
        """Separate thousand integer with dot"""
        return f"{num:,}".replace(',', '.')

    def pack(self) -> None:
        """Update table number label while repacking"""
        self.label_table_number['text'] = f"No Meja: {self.order.table_number}"
        super().pack()
        super().pack_propagate(False)


class TableDisplayPage(tk.Frame):
    def __init__(self, master, mode: Literal["order", "checkout"], order: Order = None):
        self.mode = mode
        self.order = order
        self.available_tables = Table.get_available()
        self.selected_table = order.table_number if order else None
        self.bg_color = '#ffc4a4'  # light orange
        super().__init__(master, width=MainApp.window_width,
                         height=MainApp.window_height, bg=self.bg_color)

        try:
            self.background_image = CustomImage(
                url='https://res.cloudinary.com/elhamdi/image/upload/v1670679681/table_cgbpoe.png').get_image()
            background_image_label = tk.Label(
                self, image=self.background_image)
            background_image_label.place(relx=.5, rely=.5, anchor='center')
        except:
            pass

        self.frame = tk.Frame(self, bg=self.bg_color)
        self.frame.place(relx=.5, rely=.21, anchor='n')

        text_label_title = "Silakan klik meja kosong yang diinginkan" \
            if self.mode == "order" \
            else "Silakan klik meja yang selesai digunakan"
        self.label_title = tk.Label(
            self.frame, text=text_label_title, bg=self.bg_color, font=Style.font_base)
        self.label_title.pack()

        self.container_tables = tk.Frame(self.frame, bg=self.bg_color)
        self.container_tables.pack()
        self.button_tables = {}
        table_numbers = list(Table.all_tables.keys())
        half = len(table_numbers)//2
        for col in range(2):
            for row in range(half):
                curr_table_number = table_numbers[col*half+row]
                self.button_tables[curr_table_number] = tk.Button(
                    self.container_tables,
                    text=curr_table_number,
                    width=15, padx=10, pady=5,
                    font=Style.font_large,
                    **Style.button,
                    command=lambda i=curr_table_number: self.click_table_number(i))
                self.button_tables[curr_table_number].grid(
                    row=row, column=col, sticky='nsew', padx=5, pady=5)
        self.update_button_style()

        self.container_info = tk.Frame(self.frame, bg=self.bg_color)
        self.container_info.pack(fill=tk.BOTH, expand=True)
        ttk.Label(self.container_info, text="Keterangan :",
                  font=Style.font_base, background=self.bg_color).pack(side=tk.TOP, anchor='w')
        tk.Button(self.container_info, text="Kosong",
                  font=Style.font_large, padx=10, width=10 if self.mode == "order" else 15, **Style.button_green).pack(side=tk.LEFT, padx=5)
        tk.Button(self.container_info,
                  text="Terisi", font=Style.font_large, padx=10, width=10 if self.mode == "order" else 15, **Style.button_purple).pack(side=tk.LEFT, padx=5)
        if self.mode == "order":
            tk.Button(self.container_info,
                      text="Meja Anda", font=Style.font_large, padx=10, width=10, **Style.button_blue).pack(side=tk.LEFT, padx=5)

        self.container_navigation = tk.Frame(self.frame, bg=self.bg_color)
        self.container_navigation.pack(pady=(20, 0))
        tk.Button(self.container_navigation, text="Kembali", width=15, padx=5, pady=5, font=Style.font_large, **Style.button_red,
                  command=MainApp.back).grid(row=0, column=0, sticky='e', padx=5)
        if self.mode == "order":
            tk.Button(self.container_navigation, text="OK", width=15, padx=5, pady=5, font=Style.font_large, **Style.button_red,
                      command=self.click_ok).grid(row=0, column=1, sticky='w', padx=5)

    def click_ok(self) -> None:
        """Update table number in the order"""
        self.order.table_number = self.selected_table
        MainApp.back()

    def click_table_number(self, table_number) -> None:
        """ Order mode: Click on available table to select table
            Checkout mode: Click on booked table to checkout
        """
        if self.mode == "order":
            if table_number in self.available_tables:
                self.selected_table = table_number
                self.update_button_style()
            else:
                MainApp.show_toast("Meja telah terisi!")

        if self.mode == "checkout":
            if table_number not in self.available_tables:
                MainApp.show_page(DisplayMenuPage(MainApp.container,
                                                  "checkout", Table.all_tables[table_number]))
            else:
                MainApp.show_toast("Meja ini kosong!")

    def update_button_style(self) -> None:
        """Update button color.

            Green: available
            Purple: booked
            Blue: selected
        """
        for key, button in self.button_tables.items():
            if key in Table.get_available():
                bg_color = Style.button_green['bg']
                active_bg_color = Style.button_green['activebackground']
            else:
                bg_color = Style.button_purple['bg']
                active_bg_color = Style.button_purple['activebackground']
            if self.mode == "order":
                if key == self.selected_table:
                    bg_color = Style.button_blue['bg']
                    active_bg_color = Style.button_blue['activebackground']
            button['background'] = bg_color
            button['activebackground'] = active_bg_color

    def pack(self) -> None:
        self.available_tables = Table.get_available()
        self.update_button_style()
        super().pack(fill=None, expand=False)
        super().pack_propagate(0)


class Checkout():
    def __init__(self, master=None) -> None:
        self.table_display = TableDisplayPage(master, mode='checkout')
        self.table_display.pack()

    def pack(self) -> None:
        self.table_display.pack()

    def pack_forget(self) -> None:
        self.table_display.pack_forget()


def fetch_menu():
    """Fetch menu from 'menu.txt'"""
    with open('menu.txt') as file:
        for line in file.readlines():
            # Menu type
            if line.startswith("==="):
                menu_type = line.replace("===", '', 1).strip()
                continue
            # Menu data
            menu_data = line.split(';')
            menu_data[2], menu_data[3] = int(menu_data[2]), int(
                menu_data[3])  # price, additional_info

            match menu_type:
                case "MEALS":  Meals(*menu_data)
                case "DRINKS":  Drinks(*menu_data)
                case "SIDES":  Sides(*menu_data)


def main():
    fetch_menu()
    app = MainApp()
    app.mainloop()


if __name__ == '__main__':
    main()
