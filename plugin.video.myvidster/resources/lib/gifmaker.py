#!/usr/bin/env python
#
# The Python Imaging Library
# $Id$
#
# convert sequence format to GIF animation
#
# history:
#       97-01-03 fl     created
#
# Copyright (c) Secret Labs AB 1997.  All rights reserved.
# Copyright (c) Fredrik Lundh 1997.
#
# See the README file for information on usage and redistribution.
#
#from PIL import Image
from PIL import Image
from . import urlquick
import os

def make(gifname='poster.gif', images=[]):
    imageframes = []
    for img in images:
        frame = Image.open(fp=open(img))
        imageframes.append(frame)
    try:
        imageframes[0].save(gifname, save_all=True, append_images=imageframes[1:], duration=500, loop=1)
    except:
        gifname = None
    return gifname


def from_urls(images=[], tempdir='.'):
    gifname = images[0].replace('https://', '').replace('http://', '').partition('/')[-1].split('/',1)[0] + '.gif'
    #images.remove('')
    imgfiles = []
    vidster_headers = {'referer': 'https://www.myvidster.com/',
                       'Cookie': '__cfduid=d913c54b56fe95616689ce1f1fc683a231559474798; sm_dapi_session=1; _gat=1; PHPSESSID=r1aptmhcmicd179f94v7o72id2; referral=myvidster.com; _ga=GA1.2.638511231.1559474803; _gid=GA1.2.142664491.1559474803; __atuvc=1%7C23; __atuvs=5cf3b2727692eeb9000; user_name=Skyler32UK; user_id=2219807; password=46c53b8a852c4ee94f458dc99786e23ebd666bd1; cc_data=2219807; auto_refresh=1'}
    for img in images:
        tempfilename = img.rpartition('/')[-1]
        #tempfile = os.path.join(tempdir, tempfilename)
        tempfile = tempdir + tempfilename
        resp = urlquick.get(img, params={'headers': vidster_headers})
        if resp.ok:
            try:
                output = open(tempfile, "wb")
                output.write(resp.raw.read())
                output.close()
                imgfiles.append(tempfile)
            except:
                print("Error writing frame jpg to " + tempfile + "\nDIR: "+tempdir+"\n"+tempfilename)
    return make(os.path.join(tempdir, gifname), imgfiles)
