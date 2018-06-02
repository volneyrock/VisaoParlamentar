# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

# ---- example index page ----
def index():
    projects = db(Project).select()

    return dict(projects=projects)


@auth.requires_login()
def proj_detail():
    projId = request.args[0]
    projData = db(Project.id == projId).select().first()
    you_vote = db((Vote.project == projId)&(Vote.created_by == auth.user_id)&(Vote.vote != None)).select(Vote.id, Vote.vote).first()
    y_vote = db((Vote.project == projId)&(Vote.vote == True)).count()
    n_vote = db((Vote.project == projId)&(Vote.vote == False)).count()

    return dict(projData=projData, you_vote=you_vote,
                y_vote=y_vote, n_vote=n_vote,
    )


@auth.requires_login()
def yes_vote():
    projId = request.args[0]
    Vote.update_or_insert((Vote.project==projId)&(Vote.created_by==auth.user_id),
                project=projId, vote=True)
    session.flash = 'Você votou Sim!'
    redirect(URL('default', 'proj_detail', args=projId))


@auth.requires_login()
def no_vote():
    projId = request.args[0]
    Vote.update_or_insert((Vote.project==projId)&(Vote.created_by==auth.user_id),
                project=projId, vote=False)
    session.flash = 'Você votou Não!'
    redirect(URL('default', 'proj_detail', args=projId))


@auth.requires_login()
def neutral_vote():
    voteId = request.args[0]
    projId = request.args[1]
    db((Vote.id==voteId)&(Vote.created_by==auth.user_id)).update(vote=None)
    redirect(URL('default', 'proj_detail', args=projId))


# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})


# ---- Smart Grid (example) -----
# @auth.requires_membership('admin') # can only be accessed by members of admin groupd
def grid():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)


# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu() # add the wiki to the menu
    return auth.wiki() 


# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)
