from scanner  import Scanner 
# Set your file path or directory path
path = 'files/' 

def scanning_pdf():
    # Process documents
    scanning=Scanner()
    df=scanning.process_documents(path)
    print(df)

scanning_pdf()

