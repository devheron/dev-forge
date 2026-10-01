"""Adaptive desktop layout and shared presentation helpers."""
import tkinter as tk
import os
import webbrowser
from tkinter import ttk
from catalog import CATALOG, PROFILES
from updater import METADATA
from runtime import RESOURCES

BG = '#101927'
PANEL = '#172334'
TEXT = '#e7edf5'
MUTED = '#98aac0'
ACCENT = '#64dab6'

def scrollable_text(parent, **kwargs):
    frame = ttk.Frame(parent)
    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)
    text = tk.Text(frame, bg='#0b1422', fg='#cee7ef', insertbackground='white',
                   wrap='word', width=1, height=1, bd=0, highlightthickness=0,
                   font=('Consolas', 10), padx=16, pady=14, **kwargs)
    scrollbar = ttk.Scrollbar(frame, orient='vertical', command=text.yview)
    text.configure(yscrollcommand=scrollbar.set)
    text.grid(row=0, column=0, sticky='nsew')
    scrollbar.grid(row=0, column=1, sticky='ns')
    return frame, text

def build_ui(app, icon_factory):
    root = app.root
    root.title(f"Dev Forge {METADATA['version']}")
    root.configure(bg=BG)
    icon_path = RESOURCES / 'assets' / 'dev-forge.png'
    if icon_path.exists():
        app.window_icon = tk.PhotoImage(master=root, data=icon_path.read_bytes(), format='png')
        root.iconphoto(True, app.window_icon)
    width = min(1180, root.winfo_screenwidth() - 80)
    height = min(840, root.winfo_screenheight() - 100)
    root.geometry(f'{width}x{height}+30+30')
    dpi_factor = max(1.0, float(root.tk.call('tk', 'scaling')) / 1.334)
    root.minsize(min(round(720 * dpi_factor), width), min(round(640 * dpi_factor), height))
    style = ttk.Style(root)
    style.theme_use('clam')
    style.configure('.', background=BG, foreground=TEXT, font=('Segoe UI', 10))
    style.configure('TFrame', background=BG)
    style.configure('Panel.TFrame', background=PANEL)
    style.configure('Panel.TLabel', background=PANEL)
    style.configure('Muted.TLabel', foreground=MUTED)
    style.configure('PanelMuted.TLabel', background=PANEL, foreground=MUTED, font=('Segoe UI', 9))
    style.configure('TButton', background='#26384e', borderwidth=0, relief='flat', padding=(12, 8))
    style.map('TButton', background=[('active', '#344c66'), ('disabled', '#1d2b3d')], foreground=[('disabled', '#61758b')])
    style.configure('Primary.TButton', background=ACCENT, foreground=BG, font=('Segoe UI', 10, 'bold'))
    style.map('Primary.TButton', background=[('active', '#92e8ce')])
    style.configure('TEntry', fieldbackground='#0b1422', foreground=TEXT, padding=7, borderwidth=0)
    style.configure('Vertical.TScrollbar', background='#34465d', troughcolor='#101927', borderwidth=0, arrowsize=12)
    style.configure('TNotebook', background=PANEL, borderwidth=0)
    style.configure('TNotebook.Tab', padding=(16, 8), background='#26384e', foreground=MUTED)
    style.map('TNotebook.Tab', background=[('selected', '#0b1422')], foreground=[('selected', ACCENT)])

    app.frame = frame = ttk.Frame(root, padding=20)
    frame.pack(fill='both', expand=True)
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(4, weight=1)

    header = ttk.Frame(frame)
    header.grid(row=0, column=0, sticky='ew')
    header.columnconfigure(0, weight=1)
    ttk.Label(header, text='DEV FORGE', font=('Segoe UI', 23, 'bold'), foreground=ACCENT).grid(row=0, column=0, sticky='w')
    ttk.Label(header, text=f"v{METADATA['version']}  ·  {METADATA['release_date']}", style='Muted.TLabel').grid(row=0, column=1, sticky='e')
    app.subtitle = ttk.Label(header, text='Prepare seu ambiente. Escolha as ferramentas e revise cada instalação.', style='Muted.TLabel')
    app.subtitle.grid(row=1, column=0, columnspan=2, sticky='w', pady=(4, 12))

    updates = ttk.Frame(frame)
    updates.grid(row=1, column=0, sticky='ew', pady=(0, 14))
    updates.columnconfigure(0, weight=1)
    app.update_label = ttk.Label(updates, text='Atualização opcional', style='Muted.TLabel', font=('Segoe UI', 9))
    app.update_label.grid(row=0, column=0, sticky='w')
    update_controls = ttk.Frame(updates)
    update_controls.grid(row=0, column=1, sticky='e')
    ttk.Button(update_controls, text='Histórico', command=app.show_history).pack(side='left', padx=3)
    ttk.Button(update_controls, text='Repositório', command=app.configure_updates).pack(side='left', padx=3)
    ttk.Button(update_controls, text='Atalho', command=app.make_shortcut).pack(side='left', padx=3)
    app.update_button = ttk.Button(update_controls, text='↓ Verificar versão', command=app.check_updates)
    app.update_button.pack(side='left', padx=(3, 0))

    options = ttk.Frame(frame)
    options.grid(row=2, column=0, sticky='ew', pady=(0, 12))
    options.columnconfigure(0, weight=1)
    options.columnconfigure(1, weight=2)
    os_card = ttk.Frame(options, style='Panel.TFrame', padding=12)
    profile_card = ttk.Frame(options, style='Panel.TFrame', padding=12)
    ttk.Label(os_card, text='SISTEMA OPERACIONAL', style='PanelMuted.TLabel').pack(anchor='w', pady=(0, 8))
    os_row = ttk.Frame(os_card, style='Panel.TFrame')
    os_row.pack(fill='x')
    app.platform = tk.StringVar(value='windows' if os.name == 'nt' else 'linux')
    app.os_icons = {key: icon_factory(key) for key in ('windows', 'linux')}
    app.os_buttons = {}
    for key, label in [('windows', ' Windows'), ('linux', ' Linux')]:
        button = tk.Button(os_row, text=label, image=app.os_icons[key], compound='left',
                           command=lambda k=key: app.platform.set(k), relief='flat', bd=0,
                           padx=12, pady=6, font=('Segoe UI', 10), cursor='hand2')
        button.pack(side='left', expand=True, fill='x', padx=(0, 5))
        app.os_buttons[key] = button
    ttk.Label(profile_card, text='COMECE COM UM PERFIL', style='PanelMuted.TLabel').pack(anchor='w', pady=(0, 8))
    profiles = ttk.Frame(profile_card, style='Panel.TFrame')
    profiles.pack(fill='x')
    profile_buttons = []
    for name in list(PROFILES) + ['Limpar']:
        button = ttk.Button(profiles, text=name, command=lambda n=name: app.profile(None if n == 'Limpar' else n))
        profile_buttons.append(button)

    app.hint = ttk.Label(frame, text='As versões dependem do canal de cada pacote. Downloads e atualizações são feitos por sua escolha.', style='Muted.TLabel', font=('Segoe UI', 9))
    app.hint.grid(row=3, column=0, sticky='ew', pady=(0, 12))

    app.body = body = ttk.Frame(frame)
    body.grid(row=4, column=0, sticky='nsew')
    app.left_panel = left = ttk.Frame(body, style='Panel.TFrame', padding=12)
    app.right_panel = right = ttk.Frame(body, style='Panel.TFrame', padding=12)
    left.columnconfigure(0, weight=1)
    left.rowconfigure(2, weight=1)
    right.columnconfigure(0, weight=1)
    right.rowconfigure(1, weight=1)
    ttk.Label(left, text='Ferramentas', style='Panel.TLabel', font=('Segoe UI', 12, 'bold')).grid(row=0, column=0, sticky='w', pady=(0, 10))
    app.search = tk.StringVar()
    entry = ttk.Entry(left, textvariable=app.search, width=1)
    entry.grid(row=1, column=0, sticky='ew', pady=(0, 10))
    app.search.set('')
    list_frame = ttk.Frame(left, style='Panel.TFrame')
    list_frame.grid(row=2, column=0, sticky='nsew')
    list_frame.columnconfigure(0, weight=1)
    list_frame.rowconfigure(0, weight=1)
    app.canvas = canvas = tk.Canvas(list_frame, bg=PANEL, width=1, height=1, highlightthickness=0)
    scroll = ttk.Scrollbar(list_frame, command=canvas.yview)
    canvas.grid(row=0, column=0, sticky='nsew')
    scroll.grid(row=0, column=1, sticky='ns')
    canvas.configure(yscrollcommand=scroll.set)
    inner = ttk.Frame(canvas, style='Panel.TFrame')
    window_id = canvas.create_window((0, 0), window=inner, anchor='nw')
    inner.bind('<Configure>', lambda event: canvas.configure(scrollregion=canvas.bbox('all')))
    app.vars, app.tool_rows, app.group_labels = {}, {}, {}
    def scroll_tools(event):
        canvas.yview_scroll(-1 if event.delta > 0 or getattr(event, 'num', None) == 4 else 1, 'units')
        return 'break'
    for group in dict.fromkeys(item['group'] for item in CATALOG.values()):
        heading = ttk.Label(inner, text=group.upper(), style='PanelMuted.TLabel', foreground=ACCENT)
        heading.pack(anchor='w', pady=(12, 6))
        app.group_labels[group] = heading
        for key, item in CATALOG.items():
            if item['group'] != group:
                continue
            row = ttk.Frame(inner, style='Panel.TFrame')
            row.pack(fill='x', pady=1)
            row.columnconfigure(0, weight=1)
            var = tk.BooleanVar()
            app.vars[key] = var
            check = tk.Checkbutton(row, text=item['name'], variable=var, command=app.refresh,
                                   bg=PANEL, fg=TEXT, activebackground=PANEL, activeforeground=ACCENT,
                                   selectcolor='#26384e', bd=0, highlightthickness=0, anchor='w', justify='left',
                                   font=('Segoe UI', 10), padx=2, pady=6, wraplength=220)
            check.grid(row=0, column=0, sticky='ew')
            link = tk.Button(row, text='↗', command=lambda u=item['url']: webbrowser.open(u),
                             bg=PANEL, fg=MUTED, activebackground='#26384e', activeforeground=ACCENT,
                             relief='flat', bd=0, cursor='hand2', width=2, font=('Segoe UI', 11))
            link.grid(row=0, column=1, sticky='e', padx=(4, 2))
            app.tool_rows[key] = (row, check)
            for widget in (row, check, link):
                widget.bind('<MouseWheel>', scroll_tools)
                widget.bind('<Button-4>', scroll_tools)
                widget.bind('<Button-5>', scroll_tools)
    canvas.bind('<MouseWheel>', scroll_tools)
    def resize_list(event):
        canvas.itemconfigure(window_id, width=event.width)
        for row, check in app.tool_rows.values():
            check.configure(wraplength=max(100, event.width - 65))
    canvas.bind('<Configure>', resize_list)
    def filter_tools(*args):
        query = app.search.get().casefold().strip()
        if query == 'buscar ferramentas...':
            query = ''
        for key, (row, check) in app.tool_rows.items():
            row.pack_forget()
        for group, heading in app.group_labels.items():
            heading.pack_forget()
            matches = [key for key, item in CATALOG.items() if item['group'] == group and query in (item['name'] + ' ' + group).casefold()]
            if matches:
                heading.pack(anchor='w', pady=(12, 6))
                for key in matches:
                    app.tool_rows[key][0].pack(fill='x', pady=1)
        canvas.yview_moveto(0)
    app.search.trace_add('write', filter_tools)
    def search_focus(event):
        if app.search.get() == 'Buscar ferramentas...':
            app.search.set('')
    def search_blur(event):
        if not app.search.get():
            app.search.set('Buscar ferramentas...')
    entry.bind('<FocusIn>', search_focus)
    entry.bind('<FocusOut>', search_blur)
    app.search.set('Buscar ferramentas...')

    ttk.Label(right, text='Seu plano de instalação', style='Panel.TLabel', font=('Segoe UI', 12, 'bold')).grid(row=0, column=0, sticky='w', pady=(0, 10))
    app.notebook = notebook = ttk.Notebook(right)
    notebook.grid(row=1, column=0, sticky='nsew')
    command_frame, app.preview = scrollable_text(notebook)
    steps_frame, app.steps = scrollable_text(notebook)
    notebook.add(command_frame, text='Comandos')
    notebook.add(steps_frame, text='Etapas complementares')
    app.source_label = ttk.Label(right, text='Fontes: WinGet, repositórios apt e documentação oficial.', style='PanelMuted.TLabel')
    app.source_label.grid(row=2, column=0, sticky='ew', pady=(10, 0))
    for tag, color in [('heading', ACCENT), ('comment', '#8597ac'), ('command', '#79beff'), ('guard', '#e2b77c'), ('link', '#c7a2ff'), ('body', '#cee7ef')]:
        app.preview.tag_configure(tag, foreground=color, spacing1=2, spacing3=2)
    app.preview.tag_configure('heading', font=('Consolas', 11, 'bold'), background='#15283a', spacing1=10, spacing3=8)
    app.status = ttk.Label(frame, text='', style='Muted.TLabel', font=('Segoe UI', 9))
    app.status.grid(row=5, column=0, sticky='ew', pady=(12, 8))
    app.actions = actions = ttk.Frame(frame)
    actions.grid(row=6, column=0, sticky='ew')
    app.action_buttons = [
        ttk.Button(actions, text='Copiar comandos', command=app.copy),
        ttk.Button(actions, text='Salvar script', command=app.save),
        ttk.Button(actions, text='Etapas após instalação', command=app.show_next_steps),
        ttk.Button(actions, text='Instalar selecionados', style='Primary.TButton', command=app.install),
    ]
    app.layout_mode = None
    def layout(event=None):
        if event is not None and event.widget is not root:
            return
        available = max(1, frame.winfo_width() - 40)
        compact = available < 920
        app.subtitle.configure(wraplength=available)
        app.hint.configure(wraplength=available)
        app.status.configure(wraplength=available)
        app.update_label.configure(wraplength=max(150, available - 400))
        app.source_label.configure(wraplength=max(120, right.winfo_width() - 30))
        if app.layout_mode == compact:
            return
        app.layout_mode = compact
        left.grid_forget()
        right.grid_forget()
        body.columnconfigure(0, weight=1, minsize=0)
        body.columnconfigure(1, weight=0 if compact else 2, minsize=0)
        body.rowconfigure(0, weight=1)
        body.rowconfigure(1, weight=1 if compact else 0)
        left.grid(row=0, column=0, sticky='nsew', padx=(0, 0 if compact else 12), pady=(0, 10 if compact else 0))
        right.grid(row=1 if compact else 0, column=0 if compact else 1, sticky='nsew')
        os_card.grid(row=0, column=0, sticky='nsew', padx=(0, 12), pady=0)
        profile_card.grid(row=0, column=1, sticky='nsew')
        for index, button in enumerate(profile_buttons):
            button.grid(row=index // (3 if compact else 5), column=index % (3 if compact else 5), sticky='ew', padx=2, pady=2)
        for index in range(5):
            profiles.columnconfigure(index, weight=1 if index < (3 if compact else 5) else 0)
        for index, button in enumerate(app.action_buttons):
            button.grid(row=index // (2 if compact else 4), column=index % (2 if compact else 4), sticky='ew', padx=(0, 6 if index % 2 == 0 or not compact else 0), pady=3)
        for index in range(4):
            actions.columnconfigure(index, weight=1 if index < (2 if compact else 4) else 0, uniform='actions' if index < (2 if compact else 4) else '')
    app.layout = layout
    def schedule_layout(event):
        if event.widget is root:
            root.after_idle(layout)
    root.bind('<Configure>', schedule_layout, add='+')
    root.after_idle(layout)
