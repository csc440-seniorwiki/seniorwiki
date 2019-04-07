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
        difference = difference + [commit.summary + " made by " + commit.author.name + " on "
                                   + commit.authored_datetime.strftime('%d, %b  %Y')]
    return difference


def revert(repo, position):
    x = 0
    for commit in repo.iter_commits():
        if int(position) > x:
            repo.git.revert(commit, no_edit=True)
        x += 1
