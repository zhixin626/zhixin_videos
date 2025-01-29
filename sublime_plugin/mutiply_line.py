import sublime
import sublime_plugin


class PlusLineCommand(sublime_plugin.TextCommand):
	def run(self, edit, lines = 10):
		(row,col) = self.view.rowcol(self.view.sel()[0].begin())
		self.view.run_command("goto_line", {"line": row+1 + lines})


class MinusLineCommand(sublime_plugin.TextCommand):
	def run(self, edit, lines = 10):
		(row,col) = self.view.rowcol(self.view.sel()[0].begin())
		self.view.run_command("goto_line", {"line": row+1 - lines})

class GoToBeginCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		(row,col) = self.view.rowcol(self.view.sel()[0].begin())
		self.view.run_command("goto_line", {"line": row+1})

class GoToEndCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		(row,col) = self.view.rowcol(self.view.sel()[0].end())
		self.view.run_command("goto_line", {"line": row+1})
		self.view.run_command("move_to",{"to":"eol"})
class SelectBetweenCursorsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        start=self.view.sel()[0].begin()
        end=self.view.sel()[0].end()
        start_line=self.view.line(start)
        end_line=self.view.line(end)
        new_start=start_line.begin()
        new_end=end_line.end()
        self.view.sel().add(sublime.Region(new_start, new_end))

