from git import Repo


def get_repo_path(path):
    path = path.replace('\\\\', '/').replace('\\', '/')
    url_array = path.split("/")
    del url_array[len(url_array) - 1]
    repo_path = ""
    for word in url_array:
        if word != url_array[len(url_array) - 1]:
            repo_path += word + "/"
    return repo_path + url_array[len(url_array) - 1]


def get_difference_in_file(repo):
    difference = []
    for commit in repo.iter_commits():
        difference = [commit.summary] + difference
    return difference

