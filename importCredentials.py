def importCredentials(filename):
    credentials = []
    
    with open(filename, 'r') as cred:
        credentials = [line[:-1] for line in cred]
    
    return credentials
