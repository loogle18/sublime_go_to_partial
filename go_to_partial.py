import os
from re import findall
from fnmatch import filter
from sublime_plugin import TextCommand


class GoToPartialCommand(TextCommand):
    def run(self, edit):
        view = self.view
        window = view.window()
        region = view.sel()[0]
        project_folder_path = self.get_project_path(view, window)
        target_partial_path = self.partial_name(view, region)

        if target_partial_path:
            file = self.partial_path(project_folder_path, target_partial_path)

            if file:
                window.open_file(file)

    def get_project_path(self, view, window):
        current_view_path = view.file_name()
        all_projects = window.folders()

        if '/app' in current_view_path:
            current_view_path = current_view_path.split('/app')[0]

        for project in all_projects:
            if current_view_path == project:
                return project
        return all_projects[0]

    def partial_name(self, view, region):
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
