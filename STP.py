#!/usr/bin/python
from biplist import *
import json
import os
import re


class SourceTree:
    homePath = os.path.expanduser('~')
    filePath = homePath + "/Library/Application Support/SourceTree/browser.plist"

    def _camel_case_split(self, title):
        result = []
        pattern = '.[^A-Z]*'
        matches = re.finditer(pattern, title)
        regex_parts = [m.group(0) for m in matches]
        for part in regex_parts:
            result.append(part.replace(".", ""))

        return result

    def _split_match_words(self, title):
        res = set()
        res.add(title)

        dot_parts = self._split_by_dot(title)
        for p in dot_parts:
            res.add(p)

        cam = self._camel_case_split(title)
        for m in cam:
            ret = re.split('-|_| |.|', m)
            for n in ret:
                res.add(n)
        return ' '.join(res)

    def _split_by_dot(self, title):
        return title.split(".")

    def _get_projects(self):
        try:
            plist = readPlist(self.filePath)
            temp_name = ""
            res = []
            for item in plist['$objects']:
                if type(item) is str and item[:1] == '/':
                    res.append([temp_name, item])
                elif type(item) is str:
                    temp_name = item
            return res
        except:
            return []

    def get_suggestions(self):
        items = []
        projects = self._get_projects()
        for p in projects:
            item = {
                'title': p[0],
                'subtitle': p[1],
                'arg': p[1],
                'match': self._split_match_words(p[0])
            }
            items.append(item)
        result = {'items': items}
        print(json.dumps(result))

    def clone_repo(self, url):
        parts = url.split('/')
        project_name = parts[-1].replace('.git', '')
        projects_path = self.homePath + "/Projects/"
        new_project_path = projects_path + project_name

        if os.path.isdir(new_project_path):
            print('Directory already exists.')

        os.chdir(projects_path)
        os.system('git clone ' + url)
        print(project_name + ' cloned successfully!')
