from git import Repo


def get_repo_path(url):
    url = url.replace('\\\\', '/').replace('\\', '/')
    url_array = url.split("/")
    del url_array[len(url_array) - 1]
    repo_path = ""
    for word in url_array:
        repo_path += word + "/"
    return repo_path + url_array[len(url_array) - 2]




