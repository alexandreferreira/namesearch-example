from core.models import Entry, Log

__author__ = 'alexandreferreira'

from rest_framework import serializers


class EntrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Entry
        fields = ('number', 'text')


class LogSerializer(serializers.Serializer):

    entry = serializers.IntegerField()
    text = serializers.CharField()
    text_actual = serializers.CharField()
    log_type = serializers.CharField()
    updated = serializers.DateTimeField()


