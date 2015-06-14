# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, verbose_name=b'Criado')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name=b'Atualizado')),
                ('number', models.IntegerField(serialize=False, verbose_name=b'N\xc3\xbamero', primary_key=True)),
                ('text', models.TextField(verbose_name=b'Texto', db_index=True)),
                ('deleted', models.BooleanField(default=False, verbose_name=b'Deletado?')),
            ],
            options={
                'verbose_name': 'Registro',
                'verbose_name_plural': 'Registros',
            },
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name=b'Criado')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name=b'Atualizado')),
                ('old_text', models.TextField(null=True, verbose_name=b'Texto Antigo', db_index=True)),
                ('log_type', models.CharField(max_length=10, verbose_name=b'Tipo de Log', choices=[(b'VIEW', b'VIEW'), (b'CREATE', b'CREATE'), (b'EDIT', b'EDIT'), (b'DELETE', b'DELETE')])),
                ('entry', models.ForeignKey(related_name='logs', verbose_name=b'Registro', to='core.Entry')),
            ],
            options={
                'verbose_name': 'Log',
                'verbose_name_plural': 'Logs',
            },
        ),
    ]
