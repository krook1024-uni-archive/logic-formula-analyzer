import subprocess
import os

class TeX:
    header = r'''
\documentclass[a4paper]{article}

\usepackage[utf8]{inputenc}
\usepackage[magyar]{babel}
\usepackage[T1]{fontenc}
\usepackage[a4paper, margin=2cm]{geometry}
\usepackage{textcomp}
\usepackage{forest}
\usepackage[magyar]{babel}
\usepackage{amsmath, amssymb}
\usepackage{forest}
\usepackage{calc}

\pdfsuppresswarningpagegroup=1
\setlength{\parindent}{0em}
\pagenumbering{gobble}
\date{}
    '''

    body = r'''
\begin{document}
\maketitle
\vspace{-1.5cm}

    '''

    footer = r'''

\end{document}
    '''
    def __str__(self):
        return self.header + self.body + self.footer

    def __init__(self, title):
        self.header += (r'''\title{''' + title + r'''}''')

    def add_box(self, content):
        self.body += r'''
\fbox{
    \begin{minipage}{\textwidth - 2\fboxsep}
        '''
        self.body += content
        self.body += r'''\end{minipage}
} \vspace{5mm}
        '''

    def prep_content(self, formula, binfa, szerkfa, minimized, rf, complexity):
        ret = r'''\textbf{Formula:} '''
        ret += "$" + str(formula) + "$" + '\n\n'

        ret += r'''\textbf{Bináris fája:}
\begin{center}\begin{forest}
        '''
        ret += binfa + '\n'
        ret += r'''\end{forest}\end{center}'''

        ret += r'''\textbf{Szerkezeti fája:}
\begin{center}\begin{forest}
        '''
        ret += szerkfa + '\n'
        ret += r'''\end{forest}\end{center}'''

        ret += r'''\textbf{Zárójelelhagyással:} '''
        ret += "$" + minimized + "$" + '\n\n'

        ret += r'''\textbf{Részformuláinak halmaza:} '''
        ret += "$\{" + rf + "\}$" + '\n\n'

        ret += r'''\textbf{Logikai összetettsége:} '''
        ret += str(complexity)

        return ret

    def save(self, name):
        self.name = name
        with open(name, 'w') as f:
            f.write(str(self))

    def render(self):
        self.basename = os.path.splitext(self.name)[0]
        commandLine = subprocess.Popen(
                ['pdflatex', self.name],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL)
        commandLine.communicate()

    def clean(self):
        for ext in ['.tex', '.log', '.aux']:
            try:
                os.unlink(self.basename + ext)
            except:
                pass
