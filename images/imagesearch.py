import bingimagesearch
import image_api2
import os


def name_generator():
    # Generates list of names to search. Removes names already stored in facedb/

    names2search = []
    # Read list of names to search
    with open("namelist.txt", 'rb') as f:
        names2search = f.read().splitlines()
    f.close

    # Get list of names already stored
    facedbnames = os.listdir("facedb/")
    # Removes names from already stored in database
    names2search = [x for x in names2search if x not in facedbnames]

    for name in names2search:
        newname = 'facedb/'+name
        # Create face folder if necessary
        if not os.path.exists(newname):
            print "Create new face - ", newname
            os.mkdir(newname)
    print names2search
    return names2search


if __name__ == "__main__":

    names = name_generator()
    for name in names:
        print '-------- ', name,
        urls = []
        urls = bingimagesearch.main(name.replace('_',' '))
        try:
            for url in urls:
                image_api2.urldownload(name, url)
        except IOError,TypeError:
            pass
