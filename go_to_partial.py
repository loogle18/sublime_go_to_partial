import os
from re import findall
from fnmatch import filter
from sublime_plugin import TextCommand

class GoToPartialCommand(TextCommand):
  global partial_in_render_partial_line
  global get_all_html_files_from_project

  def run(self, edit):
    view = self.view
    window = view.window()
    region = view.sel()[0]
    current_line = view.substr(view.line(region))
    text_at_cursor = view.substr(view.word(region))
    target_partial_path = partial_in_render_partial_line(current_line, text_at_cursor)

    if target_partial_path != None:
      file = get_all_html_files_from_project(window.folders()[0], target_partial_path)

      if file != None:
        window.open_file(file)

  def partial_in_render_partial_line(line, text):
    if 'render' in line:
      matched_list = findall(r"['\"](.*?)['\"]", line)

      for partial_name in matched_list:
        if text in partial_name:
          return partial_name

  def get_all_html_files_from_project(project_dir, partial_name):
    files = []
    project_dir += '/app/views'

    for root, _, filenames in os.walk(project_dir):
      for filename in filter(filenames, '*.html*'):
        file_path = os.path.join(root, filename)
        if partial_name in file_path.replace('/_', '/'):
          return file_path
