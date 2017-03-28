import os
from re import findall
from fnmatch import filter
from sublime_plugin import TextCommand


class GoToPartialCommand(TextCommand):
    def run(self, edit):
        view = self.view
        window = view.window()
        region = view.sel()[0]
        current_line = view.substr(view.line(region))
        text_at_cursor = view.substr(view.word(region))
        target_partial_path = self.partial_name(current_line, text_at_cursor)

        if target_partial_path:
            file = self.partial_path(window.folders()[0], target_partial_path)

            if file:
                window.open_file(file)

    def partial_name(self, line, text):
        if 'render' in line:
            matched_list = findall(r"['\"](.*?)['\"]", line)

            for partial_name in matched_list:
                if text in partial_name:
                    return partial_name

    def partial_path(self, project_dir, partial_name):
        project_dir += '/app/views'

        for root, _dirnames, filenames in os.walk(project_dir):
            for filename in filter(filenames, '*.html*'):
                file_path = os.path.join(root, filename)
                if partial_name in file_path.replace('/_', '/'):
                    return file_path
