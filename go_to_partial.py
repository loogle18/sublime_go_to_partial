import os
from re import findall
from fnmatch import filter
from sublime_plugin import TextCommand


class GoToPartialCommand(TextCommand):
    def run(self, edit):
        view = self.view
        window = view.window()
        region = view.sel()[0]
        # Only for cases when we have single project
        project_folder_path = window.folders()[0]
        target_partial_path = self.partial_name(region)

        if target_partial_path:
            file = self.partial_path(project_folder_path, target_partial_path)

            if file:
                window.open_file(file)

    def partial_name(self, region):
        view = self.view
        line_region = view.line(region)
        content = view.substr(line_region)

        if 'render' in content:
            matched_list = findall(r"['\"](.*?)['\"]", content)
            line_range = list(range(tuple(line_region)[0],
                                    tuple(line_region)[1] + 1))

            if matched_list:
                # Partial name is always the first element with quotes, e.g.:
                # = render partial: 'partial_name', locals: { data: 'name' }
                partial = matched_list[0]
                partial_region = view.find(partial, line_range[0])
                # Both values of region are identical, so we need only one
                cursor_at = tuple(region)[0]
                partial_range = list(range(tuple(partial_region)[0],
                                           tuple(partial_region)[1] + 1))

                if cursor_at in partial_range:
                    return partial

    def partial_path(self, project_dir, partial_name):
        project_dir += '/app/views'

        for root, _dirnames, filenames in os.walk(project_dir):
            for filename in filter(filenames, '*.html*'):
                file_path = os.path.join(root, filename)
                if partial_name in file_path.replace('/_', '/'):
                    return file_path
