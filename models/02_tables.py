# -*- coding: utf-8 -*-

PARTY = ['MDB', 'PT', 'PSDB', 'PP', 'PDT', 'PTB', 'DEM',
         'PR', 'PSB', 'PPS', 'PSC', 'PCdoB', 'PRB', 'PV',
         'PSD', 'PRP', 'PSL', 'PMN', 'PHS', 'PTC', 'SD',
         'DC', 'AVANTE', 'PODE', 'PSOL', 'PRTB', 'PROS',
         'PATRI', 'PPL', 'PMB', 'REDE', 'PSTU', 'PCB',
         'NOVO', 'PCO', 'Sem Partido'
]


Parlamentar = db.define_table('parliamentary',
    Field('name', 'string', label=T('Name')),
    Field('party', 'string', label=T('Political Party')),
)
Parlamentar.name.requires = IS_NOT_EMPTY(error_message='Cannot be empty')
Parlamentar.name.requires = IS_NOT_IN_DB(db, 'parliamentary.name')
Parlamentar.party.requires = IS_IN_SET(PARTY, zero=T('Choose one...'))


Project = db.define_table('project',
    Field('name', 'string', label=T('Name')),
    Field('title', 'string', Label=T('Title')),
    Field('description', 'text', Label=T('Description')),
    Field('presentation_date', 'date', Label=T('Date of the presentation')),
    Field('parliamentary', 'reference parliamentary', Label=T('Parliamentary')),
    Field('original', 'string', Label=T('Original'))
)
Project.name.requires = IS_NOT_EMPTY(error_message='Cannot be empty')
Project.title.requires = IS_NOT_EMPTY(error_message='Cannot be empty')
Project.parliamentary.requires = IS_IN_DB(db, 'parliamentary.id', '%(name)s')


Vote = db.define_table('vote',
    Field('project', 'reference project', Label=T('Project')),
    Field('vote', 'boolean'),
    auth.signature,
)