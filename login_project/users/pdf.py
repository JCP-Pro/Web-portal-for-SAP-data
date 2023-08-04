from pypdf import PdfReader
# https://wellsr.com/python/read-pdf-files-with-python-using-pypdf2/
# https://blog.didierstevens.com/programs/pdf-tools/ (optional)

with open(r"C:\Users\jpineda\Downloads\xrf.pdf", mode='rb') as test_pdf:
    pdfdoc = PdfReader(test_pdf)
    print("----------------------------------------------")
    print(f"THIS IS DOCUMENT INFO: {pdfdoc}")
    print("----------------------------------------------")
    
    print(" ")
    print(f"METADATA(HEAD) of pdf doc.  {pdfdoc.metadata}")
    page_one = pdfdoc.pages[0]
    for i in range(len(pdfdoc.pages)):
        current_page = pdfdoc.pages[i]
        print("===================")
        print("Content on page:" + str(i + 1))
        print("===================")
        print(current_page.extract_text())
    

print("-----------------------------------------------------------------")
# print(f"This is out of loop: {current_page.extractText}")
print("")
print("end script")