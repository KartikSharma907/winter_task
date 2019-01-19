from . import models
import logging
import os
from django.conf import settings

#file = os.path.join(BASE_DIR,'home.social_networking_website.mysite.blog.records.log')
#r = os.path.abspath(os.path.dirname(__file__))
#file = os.path.join('records.log',r)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file = os.path.join(BASE_DIR, 'post_records.log')


def keep_record(action_on, action, id):

    logging.basicConfig(
        filename=file,
        level=logging.INFO,
        format='%(asctime)s %(message)s'
    )

    if action_on == "post":
        p = models.Post.objects.get(pk=id)
        inf = (", Name of user : {}, action : {},Post Title : {} , Post Text : {} " .format(p.user.username,action,p.title,p.text))


    logging.info(inf)
