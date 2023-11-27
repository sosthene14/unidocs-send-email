import dropbox
from dropbox import Dropbox

tokene = "xAOwNU3i7vEAAAAAAAAAAYqYXb9oz2MSAFpmZvRgDY5qdy5NQGWGMzmPucCAnPTn"


def i_am_dropbox(token):
    my_client = Dropbox(token)
    file_list = my_client.files_list_folder('', recursive=True)
    folder_list = [x.name for x in file_list.entries if 'size' not in dir(x)]
    list_of_files = [x.name for x in file_list.entries]
    return folder_list, list_of_files


print(i_am_dropbox(tokene))
