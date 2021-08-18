try:
    import PIL

except ImportError:
    from sys import executable
    from os import system
    system(f"{executable} -m pip install pillow")
    import PIL



def resize_image(image_path:str, basewidth=1280, baseheight=1080) -> None:
    img = PIL.Image.open(image_path)
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)

    hpercent = (baseheight / float(img.size[1]))
    wsize = int((float(img.size[0]) * float(hpercent)))
    img = img.resize((wsize, baseheight), PIL.Image.ANTIALIAS)
    
    img.save(image_path)