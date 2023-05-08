import os
import smbclient
 
def get_files(server, username, password, share_name, directory):
    # Configure the library with the SMB server credentials
    smbclient.ClientConfig(username=username, password=password)

    # List files in the shared directory
    files = []
    remote_dir = r"\\{}\{}".format(server, share_name)
    for file_info in smbclient.listdir(remote_dir):
        ext = os.path.splitext(file_info)[1]
        if ext.lower() in ['.docx', '.xlsx', '.pdf']:
            files.append(file_info)

    return files
