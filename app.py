#!/usr/bin/env python3
"""Local desktop installer. Python standard library only."""
import os
import shutil
import subprocess
import sys
import tempfile
import queue
import threading
import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import webbrowser
from pathlib import Path
from catalog import CATALOG, PROFILES
from ui import build_ui
from engine import generate, notes, resolve
from updater import METADATA, BASE, load_settings, save_settings, validate_repository, check_release, download_update

def system_icon(system):
    image = tk.PhotoImage(width=20, height=22)
    if system == 'windows':
        for rectangle in [(1, 3, 9, 11), (11, 3, 19, 11), (1, 13, 9, 21), (11, 13, 19, 21)]:
            image.put('#4ca9ed', to=rectangle)
    else:
        # Compact penguin silhouette; drawn locally without external assets.
        for color, rectangle in [('#233044', (6, 1, 14, 8)), ('#233044', (3, 7, 17, 19)), ('#edf2fa', (6, 9, 14, 18)), ('#edf2fa', (7, 4, 9, 6)), ('#edf2fa', (11, 4, 13, 6)), ('#e9b956', (8, 6, 12, 8)), ('#e9b956', (2, 18, 9, 21)), ('#e9b956', (11, 18, 18, 21))]:
            image.put(color, to=rectangle)
    return image

class App:
    def __init__(self, root):
        self.root = root
        self.settings = load_settings()
        self.release = None
        self.events = queue.Queue()
        self.busy = False
        build_ui(self, system_icon)
        self.platform.trace_add('write', lambda *a: self.refresh())
        self.refresh()
        root.after(150, self.poll_events)
        if self.settings.get('check_on_start') and self.settings.get('repository'):
            root.after(800, self.check_updates)

    def keys(self):
        return [k for k, v in self.vars.items() if v.get()]

    def profile(self, name):
        for k, v in self.vars.items():
            v.set(k in PROFILES.get(name, []))
        self.refresh()

    def refresh(self):
        for key, button in self.os_buttons.items():
            active = key == self.platform.get()
            button.configure(bg='#62e4bd' if active else '#263a51', fg='#0b1422' if active else '#edf2fa', activebackground='#91eed3')
        keys = self.keys()
        self.script, manual = generate(keys, self.platform.get())
        text = 'COMANDOS DE INSTALAÇÃO\n' + self.script if keys else 'Escolha ferramentas ou um perfil para preparar seu ambiente.'
        step_text = notes(keys, self.platform.get()) if keys else 'As etapas das ferramentas selecionadas aparecerão aqui.'
        if manual:
            step_text += '\n\nINSTALAÇÃO MANUAL / REFERÊNCIAS\n\n' + '\n\n'.join(i['name'] + '\n' + i['url'] for i in manual)
        self.steps.configure(state='normal')
        self.steps.delete('1.0', 'end')
        self.steps.insert('1.0', step_text)
        self.steps.configure(state='disabled')
        self.preview.configure(state='normal')
        self.preview.delete('1.0', 'end')
        self.preview.insert('1.0', text)
        for index, line in enumerate(text.splitlines(), 1):
            if line.startswith(('COMANDOS DE', 'ETAPAS COMPLEMENTARES', 'INSTALACAO /')):
                tag = 'heading'
            elif line.startswith('#'):
                tag = 'comment'
            elif line.startswith(('winget ', 'sudo ', 'npm', 'wsl ')):
                tag = 'command'
            elif line.startswith(('if ', 'set ', 'case ', '[ ', 'try', '} finally', '$Error', 'Start-Transcript')):
                tag = 'guard'
            elif 'https://' in line:
                tag = 'link'
            else:
                tag = 'body'
            self.preview.tag_add(tag, f'{index}.0', f'{index}.end')
        self.preview.configure(state='disabled')
        self.status.configure(text=f'{len(keys)} selecionadas  ·  {len(resolve(keys))} com dependências  ·  {len(manual)} referências manuais')

    def show_history(self):
        window = tk.Toplevel(self.root)
        window.title('Histórico de versões')
        window.geometry('720x520')
        text = tk.Text(window, bg='#0b1422', fg='#cee7ef', wrap='word', padx=20, pady=18)
        text.pack(fill='both', expand=True)
        content = (BASE / 'CHANGELOG.md').read_text(encoding='utf-8')
        if self.release:
            content = f"Nova versão: {self.release['version']} | {self.release['date']}\n\n{self.release['notes']}\n\n" + content
        text.insert('1.0', content)
        text.configure(state='disabled')

    def show_next_steps(self):
        keys = self.keys()
        if not keys:
            return messagebox.showinfo('Etapas complementares', 'Selecione as ferramentas para ver as etapas correspondentes.')
        window = tk.Toplevel(self.root)
        window.title('Etapas após instalação')
        window.geometry('780x600')
        ttk.Label(window, text='Confira o terminal antes de seguir. A abertura do instalador não confirma sua conclusão.', wraplength=730, padding=15).pack(fill='x')
        text = tk.Text(window, bg='#0b1422', fg='#cee7ef', wrap='word', padx=20, pady=15)
        text.pack(fill='both', expand=True)
        text.insert('1.0', notes(keys, self.platform.get()))
        _, manual = generate(keys, self.platform.get())
        if manual:
            text.insert('end', '\n\nETAPAS MANUAIS / REFERÊNCIAS\n\n' + '\n\n'.join(i['name'] + '\n' + i['url'] for i in manual))
        text.configure(state='disabled')

    def configure_updates(self):
        repository = simpledialog.askstring('Atualizações do projeto', 'Repositório público GitHub (usuario/repositorio):', initialvalue=self.settings.get('repository', ''), parent=self.root)
        if repository is None:
            return
        try:
            repository = repository.strip()
            if repository:
                validate_repository(repository)
            check = bool(repository) and messagebox.askyesno('Consultar ao abrir', 'Consultar novas versões ao abrir? Apenas versão pública será consultada. Downloads e instalação dependem do seu clique.')
            self.settings = {'repository': repository, 'check_on_start': check}
            save_settings(self.settings)
            self.release = None
            self.update_button.configure(text='↓ Verificar versão', command=self.check_updates)
            self.update_label.configure(text='Repositório configurado' if repository else 'Repositório não configurado')
        except (ValueError, OSError):
            messagebox.showerror('Configuração', 'Use usuario/repositorio e uma pasta com permissão de escrita.')

    def run_task(self, kind, action):
        if self.busy:
            return
        self.busy = True
        self.update_button.configure(state='disabled')
        def worker():
            try:
                self.events.put((kind, action(), None))
            except Exception:
                self.events.put((kind, None, 'Não foi possível concluir. Confira conexão, repositório, release publicada e integridade do pacote.'))
        threading.Thread(target=worker, daemon=True).start()

    def check_updates(self):
        repository = self.settings.get('repository', '')
        if not repository:
            self.configure_updates()
            return
        self.update_label.configure(text='Consultando GitHub...')
        self.run_task('check', lambda: check_release(repository))

    def apply_update(self):
        release = self.release
        if not release or 'url' not in release:
            return messagebox.showinfo('Pacote indisponível', 'Publique dev-forge.zip como asset da release com digest SHA-256. Consulte o histórico para detalhes.')
        if not messagebox.askyesno('Atualizar Dev Forge', f"Baixar e abrir a versão {release['version']} de {release['repository']}? A versão atual será preservada e as seleções serão reiniciadas. Confira o histórico antes de continuar."):
            return
        self.update_label.configure(text='Baixando e verificando...')
        self.run_task('download', lambda: download_update(release, BASE.parent))

    def poll_events(self):
        try:
            kind, result, error = self.events.get_nowait()
        except queue.Empty:
            self.root.after(150, self.poll_events)
            return
        self.busy = False
        self.update_button.configure(state='normal')
        if error:
            self.update_label.configure(text='Consulta/atualização não concluída')
            messagebox.showerror('Atualizações', error)
        elif kind == 'check':
            self.release = result
            self.update_label.configure(text=f"Nova versão disponível: {result['version']}" if result else 'Você está na versão mais recente', foreground='#62e4bd')
            self.update_button.configure(text='↓ Baixar e atualizar' if result else '↓ Verificar versão', command=self.apply_update if result else self.check_updates)
        else:
            try:
                (result / 'settings.local.json').write_text(json.dumps(self.settings, indent=2), encoding='utf-8')
                subprocess.Popen([sys.executable, str(result / 'app.py')], cwd=str(result))
                self.root.destroy()
                return
            except OSError:
                self.update_label.configure(text='Pacote baixado; não foi possível abrir')
                messagebox.showerror('Atualizações', 'A versão atual foi preservada. Confira permissão de execução na pasta do projeto.')
        self.root.after(150, self.poll_events)

    def copy(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.script)
        self.status.configure(text='Comandos copiados.')

    def save(self):
        ext = '.ps1' if self.platform.get() == 'windows' else '.sh'
        name = filedialog.asksaveasfilename(defaultextension=ext, initialfile='dev-forge-install' + ext)
        if name:
            Path(name).write_text(self.script, encoding='utf-8-sig' if ext == '.ps1' else 'utf-8')

    def install(self):
        if not self.keys():
            return messagebox.showinfo('Selecione ferramentas', 'Escolha ao menos uma ferramenta.')
        actual = 'windows' if os.name == 'nt' else 'linux'
        if self.platform.get() != actual:
            return messagebox.showinfo('Outro sistema', 'Salve o script e execute no sistema de destino.')
        if not messagebox.askyesno('Instalar na maquina', 'Executar o plano mostrado? Downloads exigem internet, aceitam licencas dos pacotes e podem pedir administrador/sudo e reinicializacao. As etapas manuais permanecem na lista.'):
            return
        directory = Path(tempfile.mkdtemp(prefix='dev-forge-'))
        path = directory / ('install.ps1' if actual == 'windows' else 'install.sh')
        path.write_text(self.script, encoding='utf-8-sig' if actual == 'windows' else 'utf-8')
        try:
            if actual == 'windows':
                # Elevation is explicit; only our generated, allowlisted file is executed.
                escaped = str(path).replace("'", "''")
                command = f"Start-Process powershell.exe -Verb RunAs -ArgumentList @('-NoProfile','-ExecutionPolicy','Bypass','-File','\"{escaped}\"')"
                subprocess.run(['powershell.exe', '-NoProfile', '-Command', command], check=True)
            else:
                terminal = next((t for t in ['x-terminal-emulator', 'gnome-terminal', 'konsole', 'xterm'] if shutil.which(t)), None)
                if not terminal:
                    return messagebox.showinfo('Terminal necessario', f'Script salvo em {path}. Execute: bash "{path}"')
                args = [terminal, '--'] if terminal == 'gnome-terminal' else [terminal, '-e']
                subprocess.Popen(args + ['bash', '-c', 'bash "$1"; result=$?; echo "Codigo de saida: $result"; read -r -p "Enter para fechar"', 'dev-forge', str(path)], cwd=str(directory))
            self.status.configure(text=f'Terminal aberto. Acompanhe resultado e log nele. Script: {path}')
            self.show_next_steps()
        except (OSError, subprocess.CalledProcessError):
            messagebox.showerror('Não foi possível iniciar', 'Confira a permissão de execução, a disponibilidade do terminal e a solicitação de administrador.')

if __name__ == '__main__':
    App(tk.Tk()).root.mainloop()
