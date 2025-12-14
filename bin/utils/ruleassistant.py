import re
import string
import subprocess
import os
import tkinter as tk
from tkinter import filedialog as fdlg
from tkinter import simpledialog as sdlg
from tkinter import messagebox as msg

from gmltools.modimport import mod, mod_loc

if not os.path.exists("./out"):
    os.makedirs("./out")


class App:
    """
    simple program for improving workflow
    while creating GML rules
    """

    def __init__(self):
        self.root = None
        self.path = None
        self.id_label = None
        self.last_modified = None

    def run(self):
        self.root = tk.Tk()
        menu = tk.Menu(self.root)
        self.root.title("Rule Assistant")
        self.root.config(menu=menu)
        menu.add_command(label="New", command=self.create_rule)
        menu.add_command(label="Open", command=self.switch_rule)
        self.id_label = tk.Label(self.root, text="")
        self.id_label.pack()
        self.switch_rule()
        self.root.after(0, self.auto_recompile)
        self.root.mainloop()

    def create_template(self, reaction_id, smiles):
        gml_str = mod.smiles(smiles).getGMLString()
        gml_rows = gml_str.split('\n')
        gml_rows = gml_rows[1:-2]
        gml_rows = [row.replace("\t", "  ") for row in gml_rows]
        gml_str = "\n".join(gml_rows)
        gml_output = (
            ' rule [\n'
            f' ruleID "{reaction_id}"\n'
            ' labelType "term"\n'
            ' left [\n\n ]\n'
            f' context [\n{gml_str}\n ]\n'
            ' right [\n\n ]\n'''
            ' constrainLabelAny[\n  label ""\n  labels [\n   label "" \n]\n]\n]'
        )
        chars = iter(string.ascii_uppercase)
        gml_output = re.sub(r'"\*"', lambda x: f'"_{next(chars)}"', gml_output)
        file_name = f"data/rules/{reaction_id.split(' ')[0].replace('.', '_')}.gml"
        with open(file_name, "x") as f:
            f.write(gml_output)
        self.path = file_name

    def auto_recompile(self):
        mtime = os.path.getmtime(self.path)
        if mtime != self.last_modified:
            self.last_modified = mtime
            self.recompile_pdf()
        self.root.after(1000, self.auto_recompile)

    def recompile_pdf(self):
        with open(self.path, 'r') as file:
            file_str = file.read()
        if '{Template}' in file_str:
            start = file_str.find('{Template}') + 10
            end = file_str.find('{Group:', start)
            end = end if end != -1 else len(file_str)
            gml_string = file_str[start:end]
        else:
            gml_string = file_str
        try:
            r = mod.ruleGMLString(gml_string)
            p = mod.GraphPrinter()
            p.setReactionDefault()
            p.withIndex = True
            r.print(p)
        except:
            mod.post.summaryRaw('Compilation unsuccessful.')
        finally:
            mod.post.flushCommands()
            with open("out/mod_post.log", "w") as f:
                subprocess.run([mod_loc + "_post"], stdout=f,
                               stderr=f)
            mod.post.reopenCommandFile()


    def switch_rule(self):
        while True:
            self.path = fdlg.askopenfilename(
                title="Open GML Rule",
                filetypes=[("GML", "*.gml")],
                initialdir="./data/rules"
            )
            with open(self.path, "r") as f:
                gml_rule = f.read()
            match = re.search(r'ruleID\s*"(.+?)"', gml_rule)
            if match:
                id_str = match.group(1)
                label_text = f"ID String: {id_str}"
                self.id_label.config(text=label_text)
                self.recompile_pdf()
                break
            else:
                msg.showerror("No ruleID found.", "No ruleID was found,"
                                                  "please try again.")
            self.last_modified = os.path.getmtime(self.path)

    def create_rule(self):
        reaction_id = sdlg.askstring("ID String", "Please enter an "
                                                   "ID String:")
        smiles = sdlg.askstring("SMILES", "Please enter a Template-SMILES:")
        self.create_template(reaction_id, smiles)
        label_text = f"ID String:{reaction_id}"
        self.id_label.config(text=label_text)
        self.auto_recompile()


if __name__ == "__main__":
    app = App()
    app.run()
