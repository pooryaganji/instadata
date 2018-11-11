from github import Github
import github
# First create a Github instance:

# using username and password
g = Github('6ebb4ab25abab19bb7ce987c3a1074a2d607a980')

# or using an access token
repo=g.get_user().get_repo('instadata')
commit_message = 'Add simple regression analysis'

file_list = [
    
    "shahrzadseries.csv"
]

file_names = [
    
    'margin_table.html'
]
commit_message = 'python update 2'
master_ref = repo.get_git_ref('heads/master')
master_sha = master_ref.object.sha
base_tree = repo.get_git_tree(master_sha)
element_list = list()
for i, entry in enumerate(file_list):
    with open(entry) as input_file:
        data = input_file.read()

    element = github.InputGitTreeElement(file_names[i], '100644', 'blob', data)
    element_list.append(element)
tree = repo.create_git_tree(element_list, base_tree)
parent = repo.get_git_commit(master_sha)
commit = repo.create_git_commit(commit_message, tree, [parent])
master_ref.edit(commit.sha)

