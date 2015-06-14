# coding=utf-8
from django.db import models

__author__ = 'alexandreferreira'


class BaseModel(models.Model):
    created = models.DateTimeField('Criado', auto_now_add=True)
    updated = models.DateTimeField('Atualizado', auto_now=True)

    class Meta:
        abstract = True


class EntryManager(models.Manager):

    def all(self):
        return self.filter()

    def filter(self, *args, **kwargs):
        if 'deleted' not in kwargs:
            kwargs['deleted'] = False
        return super(EntryManager, self).filter(*args, **kwargs)

    def create(self, number, text):
        """
        This function create a Entry instance and save into DB
        :param number: A number for the Entry
        :type number: long
        :param text: The text of Entry
        :type text: str or unicode
        :return: A saved Entry instance
        :rtype: core.models.Entry
        """

        entry = super(EntryManager, self).create(
            **{'number': number,
               'text': text})
        from core.tasks import register_log_entry_create
        register_log_entry_create.delay(entry.number, entry.text)
        return entry

    def search_text(self, text):
        """
        This function search into db for a text
        :param text: entry name
        :type text: str
        :return: A list of entries that match with the given text
        :rtype: list of core.models.Entry
        """
        return self.get_queryset().filter(text__icontains=text)


class Entry(BaseModel):
    number = models.IntegerField('Número', primary_key=True)
    text = models.TextField('Texto', db_index=True)

    deleted = models.BooleanField('Deletado?', default=False)

    objects = EntryManager()

    class Meta:
        verbose_name = 'Registro'
        verbose_name_plural = 'Registros'

    def __unicode__(self):
        return "%d" % self.number

    def delete(self, using=None):
        from core.tasks import register_log_entry_deleted
        self.deleted = True
        self.save()
        register_log_entry_deleted.delay(self.number, self.text)


class LogManager(models.Manager):

    def create(self, entry_number, old_text, log_type):
        """
        This function create a new Log
        :param entry_number: Number of Entry instance
        :type entry_number: long
        :param old_text: Old text of Entry
        :type old_text: str or unicode
        :param log_type: The log_type
        :type log_type: str
        :return: a Log instance
        :rtype: core.models.Log
        """
        return super(LogManager, self).create(
            **{'entry_id':entry_number,
               'old_text': old_text,
               'log_type': log_type})

    def register_create_entry(self, entry_number, old_text):
        """
        Add a log when the Entry was edited
        :param entry_number: Entry instance
        :type entry_number: long
        :param old_text: Old text of entry
        :type old_text: str or unicode
        :return: A Log instance
        :rtype: core.models.Log
        """
        return self.create(entry_number, old_text, Log.CREATE)

    def register_edit_entry(self, entry_number, old_text):
        """
        Add a log when the Entry was edited
        :param entry_number: Entry instance number
        :type entry_number: long
        :param old_text: Old text of entry
        :type old_text: str or unicode
        :return: A Log instance
        :rtype: core.models.Log
        """
        return self.create(entry_number, old_text, Log.EDIT)

    def register_view_entry(self, entry_number, old_text):
        """
        Add a log when the Entry was viewed
        :param entry_number: Entry number
        :type entry_number: long
        :param old_text: Entry text
        :type old_text: str or unicode
        :return: A Log instance
        :rtype: core.models.Log
        """
        return self.create(entry_number, old_text, Log.VIEW)

    def register_delete_entry(self, entry_number, old_text):
        """
        Add a log when the Entry was deleted
        :param entry_number: Entry number
        :type entry_number: long
        :param old_text: Entry text
        :type old_text: str or unicode
        :return: A Log instance
        :rtype: core.models.Log
        """
        return self.create(entry_number, old_text, Log.DELETE)


class Log(BaseModel):
    VIEW, CREATE, EDIT, DELETE = 'VIEW', 'CREATE', 'EDIT', 'DELETE'
    LOG_TYPE = ((VIEW, VIEW), (CREATE, CREATE), (EDIT, EDIT), (DELETE, DELETE))

    entry = models.ForeignKey('Entry', verbose_name='Registro', related_name='logs')
    old_text = models.TextField('Texto Antigo', db_index=True, null=True)
    log_type = models.CharField('Tipo de Log', max_length=10, choices=LOG_TYPE)

    objects = LogManager()

    class Meta:
        verbose_name = 'Log'
        verbose_name_plural = 'Logs'

    def __unicode__(self):
        return "%s - %s" % (self.entry, self.get_log_type_display())
