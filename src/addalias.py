#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
from PyQt4 import QtGui, QtCore

class Operations:
    def __init__(self):
        self.bash_file = os.path.expanduser("~/.bashrc")

    def add_alias(self, alias, command):
        with open(self.bash_file, 'a') as f:
            f.write("alias %s='%s'\n" % (alias, command))
        print "success!"

    def delete(self, alias):
        #TODO: delete by id
        f = open(self.bash_file, "r")
        lines = f.readlines()
        f.close()

        f = open(self.bash_file,"w")

        for line in lines:
            if line.startswith("alias " + alias + "=") == False:
                f.write(line)

        f.close()
        print "success!"

    def aliaslist(self):
        aliases = []
        with open(self.bash_file, 'r') as f:
            for line in f.readlines():
                if line.startswith("alias"):
                    cmdline = line.replace("alias", "").strip()
                    aliases.append(cmdline)
        return  aliases


    def print_aliases(self):
        i = 0
        for line in self.aliaslist():
            cmdline = line.replace("alias", "").strip()
            print "[" + str(i) + "] " + cmdline
            i += 1

    def setup(self):
        import shutil
        setup_dir = os.path.expanduser("~/.local/share/addalias")
        script = os.path.realpath(__file__)
        script_name = __file__
        newpath = os.path.join(setup_dir, script_name)
        if not os.path.exists(setup_dir):
            os.mkdir(setup_dir)
        shutil.copyfile(script, newpath)
        self.add_alias("addalias", "python " + newpath)
        print "\tnow you can use 'addalias -parameters'"
        print "\tbefore using you have to close this terminal window and reopen"
        print "\tfor example"
        print '\t\taddalias -add "my-alias" "my-command"'



operations = Operations()


class GUI(QtGui.QMainWindow):
    def __init__(self, parent = None):
        super(GUI, self).__init__(parent)
        self.setWindowTitle("Add alias")
        self.load_tabwidget()
        self.setCentralWidget(self.tabwidget)
        self.load_list()
        self.show()


    def load_tabwidget(self):
        self.tabwidget = QtGui.QTabWidget()
        self.load_tabaddalias()
        self.load_tabalias()

        self.tabwidget.addTab(self.tab_addalias, "Add New Alias")
        self.tabwidget.addTab(self.tab_alias, "Edit Aliases")

    def load_tabaddalias(self):
        self.tab_addalias = QtGui.QWidget()
        self.gridLayout = QtGui.QGridLayout(self.tab_addalias)
        self.buttons_addalias = QtGui.QDialogButtonBox(self.tab_addalias)
        self.buttons_addalias.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.gridLayout.addWidget(self.buttons_addalias, 3, 0, 1, 1)
        self.layout_addalias = QtGui.QFormLayout()
        self.layout_addalias.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.lbl_command = QtGui.QLabel(self.tab_addalias)
        self.layout_addalias.setWidget(1, QtGui.QFormLayout.LabelRole, self.lbl_command)
        self.lbl_alias = QtGui.QLabel(self.tab_addalias)
        self.layout_addalias.setWidget(0, QtGui.QFormLayout.LabelRole, self.lbl_alias)
        self.line_alias = QtGui.QLineEdit(self.tab_addalias)
        self.layout_addalias.setWidget(0, QtGui.QFormLayout.FieldRole, self.line_alias)
        self.line_command = QtGui.QLineEdit(self.tab_addalias)
        self.layout_addalias.setWidget(1, QtGui.QFormLayout.FieldRole, self.line_command)
        self.gridLayout.addLayout(self.layout_addalias, 1, 0, 1, 1)
        self.line_1 = QtGui.QFrame(self.tab_addalias)
        self.line_1.setFrameShape(QtGui.QFrame.HLine)
        self.line_1.setFrameShadow(QtGui.QFrame.Sunken)
        self.gridLayout.addWidget(self.line_1, 2, 0, 1, 1)

        self.lbl_alias.setText("Alias:")
        self.lbl_command.setText("Command:")

        self.connect(self.buttons_addalias, QtCore.SIGNAL("accepted()"), self.alias_add)
        self.connect(self.buttons_addalias, QtCore.SIGNAL("rejected()"), QtGui.qApp.quit)

    def load_tabalias(self):
        self.tab_alias = QtGui.QWidget()

        self.gridLayout = QtGui.QGridLayout(self.tab_alias)
        self.layout_vertical2 = QtGui.QVBoxLayout()
        self.lbl_aliases = QtGui.QLabel(self.tab_alias)
        self.layout_vertical2.addWidget(self.lbl_aliases)
        self.list_alias = QtGui.QListWidget(self.tab_alias)
        self.layout_vertical2.addWidget(self.list_alias)
        self.gridLayout.addLayout(self.layout_vertical2, 0, 0, 1, 1)
        self.layout_vertical = QtGui.QVBoxLayout()
        self.btn_edit = QtGui.QPushButton(self.tab_alias)
        self.layout_vertical.addWidget(self.btn_edit)
        self.btn_delete = QtGui.QPushButton(self.tab_alias)
        self.layout_vertical.addWidget(self.btn_delete)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.layout_vertical.addItem(spacerItem)
        self.gridLayout.addLayout(self.layout_vertical, 0, 2, 1, 1)
        self.line_2 = QtGui.QFrame(self.tab_alias)
        self.line_2.setFrameShape(QtGui.QFrame.VLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.gridLayout.addWidget(self.line_2, 0, 1, 1, 1)

        self.lbl_aliases.setText("Aliases:")
        self.btn_edit.setText("Edit")
        self.btn_delete.setText("Delete")

        self.btn_delete.clicked.connect(self.alias_delete)
        self.btn_edit.clicked.connect(self.alias_edit)

    def load_list(self):
        self.list_alias.clear()
        for alias in operations.aliaslist():
            self.list_alias.addItem(alias)

    def alias_delete(self):
        alias = self.list_alias.selectedItems()[0].text().split("=", 1)[0]
        operations.delete(alias)
        self.load_list()

    def alias_edit(self):
        #TODO: edit aliases with edit dialog(using addalias tab widget)
        pass

    def alias_add(self):
        operations.add_alias(self.line_alias.text(), self.line_command.text())
        self.load_list()

def main():
    argv = sys.argv
    number = len(argv)

    if number == 1:
        print 'try typing --help'

    elif number == 2:
        if argv[1] == '--help':
            print ""
            print '\tusage:'
            print '\t\tadd new alias:   python addalias.py -add "<title>" "<alias>"'
            print '\t\tremove alias:    python addalias.py -rm "<title>"'
            print '\t\tlist aliases:    python addalias.py -list'
            print '\t\topen gui:        python addalias.py -gui'
            print '\t\tsetup:           python addalias.py --install'
            print ""
            print "\t\texample:"
            print '\t\t\tpython addalias.py -add "myalias" "my-real-command"'
            print '\t\t\tpython addalias.py -rm "myalias"'
            print ""
            print "\t\tif you installed the script, you can write 'addalias' instead of  'python addalias.py'"
            print ""

        elif argv[1] == "-list":
            operations.print_aliases()

        elif argv[1] == "-gui":
            app = QtGui.QApplication(sys.argv)
            gui = GUI()
            sys.exit(app.exec_())

        elif argv[1] == "--install":
            operations.setup()

        elif argv[1] == "--uninstall":
            #TODO: uninstall
            pass

        else:
            print 'wrong usage, try typing --help'

    elif number == 3 and argv[1] == "-rm":
        operations.delete(argv[2])

    elif number == 4 and argv[1] == "-add":
        operations.add_alias(argv[2], argv[3])

    else:
        print 'wrong usage, try typing --help'

if __name__ == '__main__':
    main()