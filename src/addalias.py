#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
from PyQt4 import QtGui, QtCore

ERR_SAME = "You have same alias, try different."
SUCCESS = "Success!"

class Operations:
    def __init__(self):
        self.bash_file = os.path.expanduser("~/.bashrc")
        self.path = os.path.realpath(__file__)
        self.install_dir = os.path.expanduser("~/.local/share/addalias")
        self.install_path = os.path.join(self.install_dir, __file__)

    def check(self, lines, alias):
        for line in lines:
            if line.startswith("alias " + alias + "="):
                return False
        return True

    def add_alias(self, alias, command):
        with open(self.bash_file, 'a+') as f:
            if self.check(f.readlines(), alias):
                txt = ""
                if str(command).startswith("'") and str(command).endswith("'"):
                    txt = "alias %s=%s\n" % (alias, command)
                else:
                    txt = "alias %s='%s'\n" % (alias, command)
                f.write(txt)
                print SUCCESS
                return True
            else:
                return False

    def delete(self, alias):
        #TODO: delete by id
        f = open(self.bash_file, "r")
        lines = f.readlines()
        f.close()

        f = open(self.bash_file,"w")

        for line in lines:
            if not line.startswith("alias " + alias + "="):
                f.write(line)

        f.close()
        print SUCCESS

    def aliaslist(self):
        aliases = []
        if not os.path.isfile(self.bash_file):
            open(self.bash_file, 'a').close()
        with open(self.bash_file, 'r') as f:
            for line in f.readlines():
                if line.startswith("alias"):
                    cmdline = line.replace("alias", "", 1).strip()
                    aliases.append(cmdline)
        return  aliases


    def print_aliases(self):
        i = 0
        for line in self.aliaslist():
            print "[" + str(i) + "] " + line
            i += 1

    def install(self):
        import shutil

        if not os.path.exists(self.install_dir): os.mkdir(self.install_dir)
        if os.path.isfile(self.install_path): os.remove(self.install_path)

        shutil.copyfile(self.path, self.install_path)
        self.add_alias("addalias", "python " + self.install_path)
        print "\tnow you can use 'addalias -parameters'"
        print "\tbefore using you have to close this terminal window and reopen"
        print "\tfor example"
        print '\t\taddalias -add "my-alias" "my-command"'

    def uninstall(self):
        self.delete("addalias")
        os.remove(self.install_path)
        os.rmdir(self.install_dir)
        print SUCCESS



operations = Operations()


class AddEditAlias(QtGui.QWidget):
    def __init__(self, parent = None):
        super(AddEditAlias, self).__init__(parent)
        self.old_alias = None

        self.setWindowTitle("Edit Alias")
        self.gridLayout = QtGui.QGridLayout(self)
        self.buttons_addalias = QtGui.QDialogButtonBox(self)
        self.buttons_addalias.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.gridLayout.addWidget(self.buttons_addalias, 3, 0, 1, 1)
        self.layout_addalias = QtGui.QFormLayout()
        self.layout_addalias.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.lbl_command = QtGui.QLabel(self)
        self.layout_addalias.setWidget(1, QtGui.QFormLayout.LabelRole, self.lbl_command)
        self.lbl_alias = QtGui.QLabel(self)
        self.layout_addalias.setWidget(0, QtGui.QFormLayout.LabelRole, self.lbl_alias)
        self.line_alias = QtGui.QLineEdit(self)
        self.layout_addalias.setWidget(0, QtGui.QFormLayout.FieldRole, self.line_alias)
        self.line_command = QtGui.QLineEdit(self)
        self.layout_addalias.setWidget(1, QtGui.QFormLayout.FieldRole, self.line_command)
        self.gridLayout.addLayout(self.layout_addalias, 1, 0, 1, 1)
        self.line_1 = QtGui.QFrame(self)
        self.line_1.setFrameShape(QtGui.QFrame.HLine)
        self.line_1.setFrameShadow(QtGui.QFrame.Sunken)
        self.gridLayout.addWidget(self.line_1, 2, 0, 1, 1)

        self.lbl_alias.setText("Alias:")
        self.lbl_command.setText("Command:")


class GUI(QtGui.QMainWindow):
    def __init__(self, parent = None):
        super(GUI, self).__init__(parent)
        self.setWindowTitle("Add alias")
        self.load_tabwidget()
        self.setCentralWidget(self.tabwidget)
        self.load_windowedit()
        self.load_list()
        self.show()

    def load_windowedit(self):
        self.window_edit = AddEditAlias()
        self.connect(self.window_edit.buttons_addalias, QtCore.SIGNAL("accepted()"), self.alias_edit_ok)
        self.connect(self.window_edit.buttons_addalias, QtCore.SIGNAL("rejected()"), self.window_edit.hide)

    def load_tabwidget(self):
        self.tabwidget = QtGui.QTabWidget()
        self.load_tabaddalias()
        self.load_tabalias()

        self.tabwidget.addTab(self.tab_addalias, "Add New Alias")
        self.tabwidget.addTab(self.tab_alias, "Edit Aliases")

    def load_tabaddalias(self):
        self.tab_addalias = AddEditAlias()

        self.connect(self.tab_addalias.buttons_addalias, QtCore.SIGNAL("accepted()"), self.alias_add)
        self.connect(self.tab_addalias.buttons_addalias, QtCore.SIGNAL("rejected()"), QtGui.qApp.quit)

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
        try:
            alias = self.list_alias.selectedItems()[0].text().split("=", 1)[0]
            operations.delete(alias)
            self.load_list()
        except IndexError:
            pass

    def alias_edit(self):
        try:
            _alias = self.list_alias.selectedItems()[0].text().split("=", 1)
            self.window_edit.line_alias.setText(_alias[0])
            self.window_edit.line_command.setText(_alias[1])
            self.window_edit.old_alias = _alias[0]
            self.window_edit.show()
            self.load_list()
        except IndexError:
            pass

    def alias_edit_ok(self):
        if self.window_edit.old_alias != None:
            operations.delete(self.window_edit.old_alias)
            operations.add_alias(self.window_edit.line_alias.text(), self.window_edit.line_command.text())
            self.window_edit.old_alias = None
            self.load_list()
            self.window_edit.hide()

    def alias_add(self):
        if operations.add_alias(self.tab_addalias.line_alias.text(), self.tab_addalias.line_command.text()):
            self.load_list()
            QtGui.QMessageBox.information(self, SUCCESS, "You have successfully added new alias!")
        else:
            QtGui.QMessageBox.warning(self, "Error", ERR_SAME)

def main(argv):
    if argv is None:
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
            print '\t\tinstall:         python addalias.py --install (Installs for only this user)'
            print '\t\tuninstall:       addalias --uninstall         (If you installed with --install command, use this to uninstall)'
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
            operations.install()

        elif argv[1] == "--uninstall":
            operations.uninstall()

        else:
            print 'wrong usage, try typing --help'

    elif number == 3 and argv[1] == "-rm":
        operations.delete(argv[2])

    elif number == 4 and argv[1] == "-add":
        if not operations.add_alias(argv[2], argv[3]):
            print ERR_SAME

    else:
        print 'wrong usage, try typing --help'

if __name__ == '__main__':
    main()
