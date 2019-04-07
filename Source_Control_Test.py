import shutil
import unittest
import os
import datetime
from wiki import git_integration
from git import Repo, Actor


class TestSourceControl(unittest.TestCase):
    def setUp(self):
        self.repo = Repo.init('/testRepo')
        file = open('/testRepo/test.txt', 'w+')
        file.write("test");
        file.close()
        self.repo.index.add(['test.txt'])
        author = Actor('Tester', 'Tester' + "@Riki.com")
        self.repo.index.commit('changed', author=author, committer=author);

    def test_get_repo_path(self):
        path = 'Users/user/doc/project/project'
        self.assertTrue(git_integration.get_repo_path(path), 'Users/user/doc/project')

    def test_get_differences_in_file(self):
        differences = git_integration.get_difference_in_file(self.repo)

        self.assertTrue(differences[0], 'changed made by Tester on ' + datetime.datetime.now().strftime('%d, %b  %Y'))


if __name__ == '__main__':
    unittest.main()
